# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Pipeline Orchestration: End-to-End Fraud Detection Pipeline
# MAGIC ## Real-Time Credit Card Fraud Risk Scoring Pipeline
# MAGIC
# MAGIC This master notebook orchestrates all three Medallion layers in sequence.
# MAGIC It can be scheduled as a Databricks Job on a recurring trigger (e.g., every 5 minutes)
# MAGIC to achieve near real-time fraud detection.
# MAGIC
# MAGIC ```
# MAGIC  transaction.csv
# MAGIC       │
# MAGIC       ▼
# MAGIC  ┌─────────────┐     Auto Loader      ┌──────────────────────────┐
# MAGIC  │  LANDING    │ ─── (streaming) ───► │  BRONZE: raw_transactions│
# MAGIC  │   ZONE      │                      │  + ingestion metadata     │
# MAGIC  └─────────────┘                      └────────────┬─────────────┘
# MAGIC                                                    │ readStream
# MAGIC                customer_profile.csv                ▼
# MAGIC                       │              ┌──────────────────────────────┐
# MAGIC                       └──────────── ►│  SILVER: clean + enriched    │
# MAGIC                       (static join)  │  + spend_ratio, flags, etc.  │
# MAGIC                                      └────────────┬─────────────────┘
# MAGIC                                                   │ batch read
# MAGIC                                                   ▼
# MAGIC                                      ┌──────────────────────────────┐
# MAGIC                                      │  GOLD: fraud_alerts          │
# MAGIC                                      │  risk_score + fraud_label    │
# MAGIC                                      └────────────┬─────────────────┘
# MAGIC                                                   │
# MAGIC                                          ┌────────┴────────┐
# MAGIC                                          │   Dashboards /  │
# MAGIC                                          │   Alerts / API  │
# MAGIC                                          └─────────────────┘
# MAGIC ```

# COMMAND ----------
# MAGIC %md
# MAGIC ### Global Configuration
# MAGIC Update these paths to match your Databricks environment.

# COMMAND ----------

# ── File Paths (Unity Catalog Volumes) ────────────────────────────────────────
DATA_PATH         = "/Volumes/workspace/default/fraud_data/transactions/"
CUSTOMER_CSV_PATH = "/Volumes/workspace/default/fraud_data/customer_profile.csv"

# ── Delta Tables ─────────────────────────────────────────────────────────────
BRONZE_TABLE      = "fraud_pipeline.bronze_transactions"
SILVER_TABLE      = "fraud_pipeline.silver_transactions"
GOLD_TABLE        = "fraud_pipeline.gold_fraud_alerts"

# ── Checkpoints (separate Volume, avoids storage-overlap errors) ─────────────
CHECKPOINT_BRONZE = "/Volumes/workspace/default/fraud_checkpoints/bronze"
CHECKPOINT_SILVER = "/Volumes/workspace/default/fraud_checkpoints/silver"
SCHEMA_LOCATION   = "/Volumes/workspace/default/fraud_checkpoints/schema/bronze"

# ── Scoring Config ────────────────────────────────────────────────────────────
SPEND_RATIO_THRESHOLD   = 3.0
VELOCITY_WINDOW_SECONDS = 600
SCORE_HIGH_AMOUNT       = 40
SCORE_LOCATION_MISMATCH = 20
SCORE_ODD_HOURS         = 20
SCORE_CATEGORY_MISMATCH = 15
SCORE_VELOCITY          = 30
MAX_SCORE               = 100
THRESHOLD_HIGH          = 70
THRESHOLD_MEDIUM        = 40

# COMMAND ----------

import time
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Layer 1: Bronze — Raw Ingestion

# COMMAND ----------

log("Starting BRONZE layer...")

spark.sql("CREATE DATABASE IF NOT EXISTS fraud_pipeline")

transaction_schema = StructType([
    StructField("transaction_id",    StringType(), True),
    StructField("customer_id",       StringType(), True),
    StructField("card_id",           StringType(), True),
    StructField("transaction_time",  StringType(), True),
    StructField("amount",            StringType(), True),
    StructField("merchant",          StringType(), True),
    StructField("merchant_category", StringType(), True),
    StructField("location",          StringType(), True),
])

df_raw = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", SCHEMA_LOCATION)
    .option("cloudFiles.partitionColumns", "")
    .option("header", "true")
    .schema(transaction_schema)
    .load(DATA_PATH)
)

df_bronze = (
    df_raw
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("ingestion_date",      F.to_date(F.current_timestamp()))
    .withColumn("source_file",         F.col("_metadata.file_path"))
    .withColumn("pipeline_version",    F.lit("v1.0"))
)

(
    df_bronze.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_BRONZE)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .table(BRONZE_TABLE)
    .awaitTermination()
)

bronze_count = spark.read.format("delta").table(BRONZE_TABLE).count()
log(f"BRONZE complete. Records ingested: {bronze_count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Layer 2: Silver — Cleaning & Enrichment

# COMMAND ----------

log("Starting SILVER layer...")

customer_schema = StructType([
    StructField("customer_id",        StringType(), True),
    StructField("home_location",      StringType(), True),
    StructField("avg_spend_per_day",  DoubleType(), True),
    StructField("preferred_category", StringType(), True),
])

df_customer = (
    spark.read.format("csv")
    .option("header", "true")
    .schema(customer_schema)
    .load(CUSTOMER_CSV_PATH)
)

df_bronze_stream = spark.readStream.format("delta").table(BRONZE_TABLE)

df_cleaned = (
    df_bronze_stream
    .withColumn("transaction_time", F.to_timestamp("transaction_time", "yyyy-MM-dd HH:mm:ss"))
    .withColumn("amount",           F.col("amount").cast(DoubleType()))
    .dropna(subset=["transaction_id", "customer_id", "card_id", "transaction_time", "amount"])
    .withColumn("location",          F.trim(F.col("location")))
    .withColumn("merchant_category", F.trim(F.col("merchant_category")))
    .withColumn("merchant",          F.trim(F.col("merchant")))
    .filter(F.col("amount") > 0)
)

df_enriched = df_cleaned.join(df_customer, on="customer_id", how="left")

df_silver = (
    df_enriched
    .withColumn("hour_of_day",   F.hour("transaction_time"))
    .withColumn("day_of_week",   F.dayofweek("transaction_time"))
    .withColumn("is_weekend",    F.col("day_of_week").isin([1, 7]))
    .withColumn("is_odd_hours",  (F.col("hour_of_day") < 6) | (F.col("hour_of_day") >= 23))
    .withColumn(
        "spend_ratio",
        F.round(
            F.col("amount") / F.when(F.col("avg_spend_per_day") > 0, F.col("avg_spend_per_day")).otherwise(F.lit(1)),
            4
        )
    )
    .withColumn("location_mismatch", F.lower(F.col("location")) != F.lower(F.col("home_location")))
    .withColumn("category_mismatch", F.lower(F.col("merchant_category")) != F.lower(F.col("preferred_category")))
    .withColumn("silver_timestamp", F.current_timestamp())
    .select(
        "transaction_id", "customer_id", "card_id", "transaction_time",
        "amount", "merchant", "merchant_category", "location",
        "home_location", "avg_spend_per_day", "preferred_category",
        "hour_of_day", "day_of_week", "is_weekend", "is_odd_hours",
        "spend_ratio", "location_mismatch", "category_mismatch",
        "ingestion_timestamp", "source_file", "silver_timestamp",
    )
)

(
    df_silver.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_SILVER)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .table(SILVER_TABLE)
    .awaitTermination()
)

silver_count = spark.read.format("delta").table(SILVER_TABLE).count()
log(f"SILVER complete. Records processed: {silver_count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Layer 3: Gold — Fraud Scoring

# COMMAND ----------

log("Starting GOLD layer...")

df_silver_batch = spark.read.format("delta").table(SILVER_TABLE)

velocity_window = (
    Window
    .partitionBy("customer_id")
    .orderBy(F.col("transaction_time").cast("long"))
    .rangeBetween(-VELOCITY_WINDOW_SECONDS, 0)
)

df_gold = (
    df_silver_batch
    .withColumn("txn_count_10min", F.count("transaction_id").over(velocity_window))

    .withColumn("high_amount_flag",       F.when(F.col("spend_ratio") > SPEND_RATIO_THRESHOLD, 1).otherwise(0))
    .withColumn("high_amount_score",      F.when(F.col("spend_ratio") > SPEND_RATIO_THRESHOLD, SCORE_HIGH_AMOUNT).otherwise(0))

    .withColumn("location_mismatch_flag",  F.when(F.col("location_mismatch") == True, 1).otherwise(0))
    .withColumn("location_mismatch_score", F.when(F.col("location_mismatch") == True, SCORE_LOCATION_MISMATCH).otherwise(0))

    .withColumn("odd_hours_flag",          F.when(F.col("is_odd_hours") == True, 1).otherwise(0))
    .withColumn("odd_hours_score",         F.when(F.col("is_odd_hours") == True, SCORE_ODD_HOURS).otherwise(0))

    .withColumn("category_mismatch_flag",  F.when(F.col("category_mismatch") == True, 1).otherwise(0))
    .withColumn("category_mismatch_score", F.when(F.col("category_mismatch") == True, SCORE_CATEGORY_MISMATCH).otherwise(0))

    .withColumn("velocity_flag",           F.when(F.col("txn_count_10min") > 1, 1).otherwise(0))
    .withColumn("velocity_score",          F.when(F.col("txn_count_10min") > 1, SCORE_VELOCITY).otherwise(0))

    .withColumn(
        "risk_score",
        F.least(
            F.col("high_amount_score") + F.col("location_mismatch_score") +
            F.col("odd_hours_score")   + F.col("category_mismatch_score") +
            F.col("velocity_score"),
            F.lit(MAX_SCORE)
        )
    )
    .withColumn(
        "fraud_label",
        F.when(F.col("risk_score") >= THRESHOLD_HIGH,   "HIGH")
         .when(F.col("risk_score") >= THRESHOLD_MEDIUM, "MEDIUM")
         .otherwise("LOW")
    )
    .withColumn(
        "rules_triggered",
        F.col("high_amount_flag") + F.col("location_mismatch_flag") +
        F.col("odd_hours_flag")   + F.col("category_mismatch_flag") +
        F.col("velocity_flag")
    )
    .withColumn("gold_timestamp", F.current_timestamp())
    .select(
        "transaction_id", "customer_id", "card_id", "transaction_time",
        "amount", "merchant", "merchant_category", "location",
        "home_location", "avg_spend_per_day", "preferred_category",
        "spend_ratio", "hour_of_day", "is_weekend", "is_odd_hours", "txn_count_10min",
        "high_amount_flag", "location_mismatch_flag", "odd_hours_flag",
        "category_mismatch_flag", "velocity_flag",
        "high_amount_score", "location_mismatch_score", "odd_hours_score",
        "category_mismatch_score", "velocity_score",
        "risk_score", "fraud_label", "rules_triggered", "gold_timestamp",
    )
)

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLE)
)

gold_count = spark.read.format("delta").table(GOLD_TABLE).count()
log(f"GOLD complete. Fraud alerts generated: {gold_count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Pipeline Summary

# COMMAND ----------

print("\n" + "=" * 65)
print("   REAL-TIME CREDIT CARD FRAUD RISK SCORING PIPELINE")
print("   EXECUTION SUMMARY")
print("=" * 65)

summary = spark.sql(f"""
    SELECT
        fraud_label                                          AS risk_level,
        COUNT(*)                                             AS transactions,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1)  AS pct_of_total,
        ROUND(AVG(risk_score), 1)                           AS avg_score,
        ROUND(SUM(amount), 2)                               AS total_amount
    FROM {GOLD_TABLE}
    GROUP BY fraud_label
    ORDER BY avg_score DESC
""")

summary.show(truncate=False)

high_risk = spark.sql(f"SELECT COUNT(*) AS cnt FROM {GOLD_TABLE} WHERE fraud_label = 'HIGH'").collect()[0]["cnt"]
total     = spark.sql(f"SELECT COUNT(*) AS cnt FROM {GOLD_TABLE}").collect()[0]["cnt"]

print(f"  Total transactions scored : {total}")
print(f"  HIGH risk alerts          : {high_risk}")
print(f"  Tables written            : {BRONZE_TABLE}, {SILVER_TABLE}, {GOLD_TABLE}")
print("=" * 65)
