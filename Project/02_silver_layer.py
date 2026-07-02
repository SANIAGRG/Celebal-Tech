# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Silver Layer: Cleaning, Enrichment & Feature Engineering
# MAGIC ## Real-Time Credit Card Fraud Risk Scoring Pipeline
# MAGIC ### Medallion Architecture - Layer 2 (Silver)
# MAGIC
# MAGIC **Objective:**
# MAGIC - Read raw transactions from the Bronze Delta table (streaming)
# MAGIC - Cast and validate data types; drop nulls and duplicates
# MAGIC - Enrich each transaction with customer profile data (stream-static join)
# MAGIC - Derive fraud-detection features (spend ratio, location mismatch, odd hours, etc.)
# MAGIC
# MAGIC **Input:**  `fraud_pipeline.bronze_transactions`
# MAGIC **Output:** `fraud_pipeline.silver_transactions`

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 1: Configuration

# COMMAND ----------

BRONZE_TABLE      = "fraud_pipeline.bronze_transactions"
SILVER_TABLE      = "fraud_pipeline.silver_transactions"
CUSTOMER_CSV_PATH = "/FileStore/fraud_pipeline/data/customer_profile.csv"
CHECKPOINT_SILVER = "/tmp/fraud_pipeline/checkpoints/silver"

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 2: Load Customer Profile as a Static DataFrame
# MAGIC
# MAGIC Customer profile is a small, slowly-changing lookup table.
# MAGIC Loading it as a static DataFrame allows a stream-static join with the
# MAGIC transaction stream — no watermarking required on the static side.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql import functions as F

customer_schema = StructType([
    StructField("customer_id",        StringType(), True),
    StructField("home_location",      StringType(), True),
    StructField("avg_spend_per_day",  DoubleType(), True),
    StructField("preferred_category", StringType(), True),
])

df_customer = (
    spark.read
    .format("csv")
    .option("header", "true")
    .schema(customer_schema)
    .load(CUSTOMER_CSV_PATH)
)

# Cache since it will be reused on every micro-batch
df_customer.cache()

print("Customer profile loaded:")
df_customer.show(truncate=False)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 3: Read Bronze Table as Stream

# COMMAND ----------

df_bronze_stream = (
    spark.readStream
    .format("delta")
    .table(BRONZE_TABLE)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 4: Clean & Cast Types
# MAGIC
# MAGIC | Raw Column         | Issue                  | Fix                            |
# MAGIC |--------------------|------------------------|--------------------------------|
# MAGIC | `transaction_time` | Stored as String       | Cast to Timestamp              |
# MAGIC | `amount`           | Stored as String       | Cast to Double                 |
# MAGIC | All columns        | Possible nulls         | Drop rows missing critical IDs |
# MAGIC | `transaction_id`   | Possible duplicates    | Drop duplicates                |

# COMMAND ----------

df_cleaned = (
    df_bronze_stream

    # ── Type casts ───────────────────────────────────────────────────────────
    .withColumn("transaction_time", F.to_timestamp("transaction_time", "yyyy-MM-dd HH:mm:ss"))
    .withColumn("amount",           F.col("amount").cast(DoubleType()))

    # ── Drop rows with nulls in business-critical columns ────────────────────
    .dropna(subset=["transaction_id", "customer_id", "card_id", "transaction_time", "amount"])

    # ── Standardise string columns (trim whitespace, lower-case location) ────
    .withColumn("location",          F.trim(F.col("location")))
    .withColumn("merchant_category", F.trim(F.col("merchant_category")))
    .withColumn("merchant",          F.trim(F.col("merchant")))

    # ── Remove negative or zero amounts (data quality guard) ─────────────────
    .filter(F.col("amount") > 0)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 5: Stream-Static Join — Enrich with Customer Profile

# COMMAND ----------

df_enriched = (
    df_cleaned
    .join(df_customer, on="customer_id", how="left")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 6: Feature Engineering
# MAGIC
# MAGIC Derived columns used as inputs to the fraud scoring rules in the Gold layer.
# MAGIC
# MAGIC | Feature               | Description                                                  |
# MAGIC |-----------------------|--------------------------------------------------------------|
# MAGIC | `hour_of_day`         | Hour extracted from transaction_time (0–23)                  |
# MAGIC | `day_of_week`         | Day number (1=Sun … 7=Sat in Spark)                          |
# MAGIC | `is_weekend`          | True if Saturday or Sunday                                   |
# MAGIC | `is_odd_hours`        | True if transaction between 00:00–05:59 or 23:00–23:59      |
# MAGIC | `spend_ratio`         | amount / avg_spend_per_day — how far above baseline          |
# MAGIC | `location_mismatch`   | True if transaction city != customer home city               |
# MAGIC | `category_mismatch`   | True if merchant_category != customer preferred_category     |
# MAGIC | `silver_timestamp`    | When this Silver record was created                          |

# COMMAND ----------

df_silver = (
    df_enriched

    # ── Temporal features ─────────────────────────────────────────────────────
    .withColumn("hour_of_day",   F.hour("transaction_time"))
    .withColumn("day_of_week",   F.dayofweek("transaction_time"))
    .withColumn("is_weekend",    F.col("day_of_week").isin([1, 7]))
    .withColumn("is_odd_hours",  (F.col("hour_of_day") < 6) | (F.col("hour_of_day") >= 23))

    # ── Spend feature ─────────────────────────────────────────────────────────
    .withColumn(
        "spend_ratio",
        F.round(
            F.col("amount") / F.when(F.col("avg_spend_per_day") > 0, F.col("avg_spend_per_day")).otherwise(F.lit(1)),
            4
        )
    )

    # ── Location & category mismatch flags ───────────────────────────────────
    .withColumn(
        "location_mismatch",
        F.lower(F.col("location")) != F.lower(F.col("home_location"))
    )
    .withColumn(
        "category_mismatch",
        F.lower(F.col("merchant_category")) != F.lower(F.col("preferred_category"))
    )

    # ── Audit column ──────────────────────────────────────────────────────────
    .withColumn("silver_timestamp", F.current_timestamp())

    # ── Select final Silver columns in logical order ──────────────────────────
    .select(
        "transaction_id",
        "customer_id",
        "card_id",
        "transaction_time",
        "amount",
        "merchant",
        "merchant_category",
        "location",
        "home_location",
        "avg_spend_per_day",
        "preferred_category",
        "hour_of_day",
        "day_of_week",
        "is_weekend",
        "is_odd_hours",
        "spend_ratio",
        "location_mismatch",
        "category_mismatch",
        "ingestion_timestamp",
        "source_file",
        "silver_timestamp",
    )
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 7: Write to Silver Delta Table

# COMMAND ----------

silver_query = (
    df_silver.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_SILVER)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .table(SILVER_TABLE)
)

silver_query.awaitTermination()
print("Silver layer processing complete.")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 8: Validate Silver Table

# COMMAND ----------

print("=== Silver Table: Row Count ===")
spark.sql(f"SELECT COUNT(*) AS total_records FROM {SILVER_TABLE}").show()

print("=== Silver Table: Sample Enriched Records ===")
spark.sql(f"""
    SELECT
        transaction_id, customer_id, amount, spend_ratio,
        location, home_location, location_mismatch,
        merchant_category, preferred_category, category_mismatch,
        hour_of_day, is_odd_hours, is_weekend
    FROM {SILVER_TABLE}
    LIMIT 10
""").show(truncate=False)

print("=== Silver Table: Null Check on Key Columns ===")
spark.sql(f"""
    SELECT
        SUM(CASE WHEN transaction_id IS NULL THEN 1 ELSE 0 END)    AS null_txn_id,
        SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END)       AS null_customer_id,
        SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)            AS null_amount,
        SUM(CASE WHEN transaction_time IS NULL THEN 1 ELSE 0 END)  AS null_txn_time,
        SUM(CASE WHEN home_location IS NULL THEN 1 ELSE 0 END)     AS null_home_location
    FROM {SILVER_TABLE}
""").show()

print("=== Silver Table: Feature Distribution ===")
spark.sql(f"""
    SELECT
        COUNT(*)                                      AS total,
        SUM(CAST(location_mismatch AS INT))           AS location_mismatches,
        SUM(CAST(category_mismatch AS INT))           AS category_mismatches,
        SUM(CAST(is_odd_hours AS INT))                AS odd_hour_txns,
        SUM(CAST(is_weekend AS INT))                  AS weekend_txns,
        ROUND(AVG(spend_ratio), 2)                    AS avg_spend_ratio,
        ROUND(MAX(spend_ratio), 2)                    AS max_spend_ratio
    FROM {SILVER_TABLE}
""").show()
