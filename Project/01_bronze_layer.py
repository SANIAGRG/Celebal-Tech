# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Layer: Raw Transaction Ingestion
# MAGIC ## Real-Time Credit Card Fraud Risk Scoring Pipeline
# MAGIC ### Medallion Architecture - Layer 1 (Bronze)
# MAGIC
# MAGIC **Objective:**
# MAGIC Ingest raw credit card transaction data using Auto Loader (cloudFiles) in streaming mode
# MAGIC and persist it to a Delta table with zero transformations — only ingestion metadata is added.
# MAGIC
# MAGIC **Input:**  Raw CSV files from the landing zone
# MAGIC **Output:** `fraud_pipeline.bronze_transactions` Delta table

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 1: Configuration

# COMMAND ----------

# ── Paths (update to match your Databricks DBFS / Unity Catalog mount) ──────
DATA_PATH         = "/FileStore/fraud_pipeline/data/"          # folder containing transaction.csv
BRONZE_TABLE      = "fraud_pipeline.bronze_transactions"
CHECKPOINT_BRONZE = "/tmp/fraud_pipeline/checkpoints/bronze"
SCHEMA_LOCATION   = "/tmp/fraud_pipeline/schema/bronze"

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 2: Create Database / Schema

# COMMAND ----------

spark.sql("CREATE DATABASE IF NOT EXISTS fraud_pipeline")
print("Database 'fraud_pipeline' ready.")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 3: Define Schema
# MAGIC
# MAGIC Explicit schema prevents Auto Loader from re-inferring on every run.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType

transaction_schema = StructType([
    StructField("transaction_id",    StringType(), True),
    StructField("customer_id",       StringType(), True),
    StructField("card_id",           StringType(), True),
    StructField("transaction_time",  StringType(), True),   # cast to Timestamp in Silver
    StructField("amount",            StringType(), True),   # cast to Double in Silver
    StructField("merchant",          StringType(), True),
    StructField("merchant_category", StringType(), True),
    StructField("location",          StringType(), True),
])

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 4: Read Transaction Data via Auto Loader (Streaming)
# MAGIC
# MAGIC Auto Loader (`cloudFiles`) efficiently tracks which files have been ingested
# MAGIC and processes only new files on each trigger — no duplicate ingestion.

# COMMAND ----------

from pyspark.sql import functions as F

df_raw_stream = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("cloudFiles.schemaLocation", SCHEMA_LOCATION)
    .option("header", "true")
    .schema(transaction_schema)
    .load(DATA_PATH)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 5: Add Ingestion Metadata
# MAGIC
# MAGIC Bronze stores data as-is; only system metadata columns are appended.

# COMMAND ----------

df_bronze = (
    df_raw_stream
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("ingestion_date",      F.to_date(F.current_timestamp()))
    .withColumn("source_file",         F.input_file_name())
    .withColumn("pipeline_version",    F.lit("v1.0"))
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 6: Write to Bronze Delta Table
# MAGIC
# MAGIC `trigger(availableNow=True)` processes all pending files in one micro-batch
# MAGIC then stops — ideal for scheduled jobs. Switch to `trigger(processingTime="10 seconds")`
# MAGIC for continuous low-latency streaming.

# COMMAND ----------

bronze_query = (
    df_bronze.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", CHECKPOINT_BRONZE)
    .option("mergeSchema", "true")
    .trigger(availableNow=True)
    .table(BRONZE_TABLE)
)

bronze_query.awaitTermination()
print("Bronze layer ingestion complete.")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 7: Validate Bronze Table

# COMMAND ----------

print("=== Bronze Table: Row Count ===")
spark.sql(f"SELECT COUNT(*) AS total_records FROM {BRONZE_TABLE}").show()

print("=== Bronze Table: Sample Records ===")
spark.sql(f"SELECT * FROM {BRONZE_TABLE} LIMIT 10").show(truncate=False)

print("=== Bronze Table: Schema ===")
spark.sql(f"DESCRIBE {BRONZE_TABLE}").show(truncate=False)

print("=== Bronze Table: Ingestion Summary by Date ===")
spark.sql(f"""
    SELECT
        ingestion_date,
        COUNT(*)          AS records_ingested,
        MIN(ingestion_timestamp) AS first_ingested,
        MAX(ingestion_timestamp) AS last_ingested
    FROM {BRONZE_TABLE}
    GROUP BY ingestion_date
    ORDER BY ingestion_date
""").show(truncate=False)
