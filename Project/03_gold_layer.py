# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Gold Layer: Fraud Scoring, Risk Labelling & Alerts
# MAGIC ## Real-Time Credit Card Fraud Risk Scoring Pipeline
# MAGIC ### Medallion Architecture - Layer 3 (Gold)
# MAGIC
# MAGIC **Objective:**
# MAGIC - Read enriched transactions from the Silver Delta table
# MAGIC - Apply five fraud detection rules to compute a `risk_score` (0–100)
# MAGIC - Assign a `fraud_label`: HIGH / MEDIUM / LOW
# MAGIC - Detect transaction velocity (multiple txns from same customer within 10 minutes)
# MAGIC - Write fraud alerts to the Gold Delta table for dashboards and downstream alerting
# MAGIC
# MAGIC **Input:**  `fraud_pipeline.silver_transactions`
# MAGIC **Output:** `fraud_pipeline.gold_fraud_alerts`
# MAGIC
# MAGIC ---
# MAGIC ### Fraud Scoring Rules
# MAGIC
# MAGIC | Rule                  | Condition                                      | Score |
# MAGIC |-----------------------|------------------------------------------------|-------|
# MAGIC | High Amount           | `spend_ratio > 3` (amount > 3x daily baseline) | +40   |
# MAGIC | Location Mismatch     | Transaction city != home city                  | +20   |
# MAGIC | Odd Hours             | Transaction between 00:00–05:59 or 23:00+      | +20   |
# MAGIC | Category Mismatch     | Merchant category != preferred category         | +15   |
# MAGIC | Velocity              | >1 transaction from same customer in 10 min    | +30   |
# MAGIC
# MAGIC **Risk Labels:**
# MAGIC - `HIGH`   → risk_score >= 70
# MAGIC - `MEDIUM` → risk_score 40–69
# MAGIC - `LOW`    → risk_score < 40

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 1: Configuration

# COMMAND ----------

SILVER_TABLE      = "fraud_pipeline.silver_transactions"
GOLD_TABLE        = "fraud_pipeline.gold_fraud_alerts"
CHECKPOINT_GOLD   = "/tmp/fraud_pipeline/checkpoints/gold"

# Scoring weights (tune as needed)
SCORE_HIGH_AMOUNT       = 40
SCORE_LOCATION_MISMATCH = 20
SCORE_ODD_HOURS         = 20
SCORE_CATEGORY_MISMATCH = 15
SCORE_VELOCITY          = 30
MAX_SCORE               = 100

SPEND_RATIO_THRESHOLD   = 3.0    # flag if amount > 3x avg daily spend
VELOCITY_WINDOW_SECONDS = 600    # 10-minute velocity window

# Risk label thresholds
THRESHOLD_HIGH   = 70
THRESHOLD_MEDIUM = 40

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 2: Read Silver Table (Batch)
# MAGIC
# MAGIC Gold uses a **batch read** from Silver because the velocity rule requires
# MAGIC comparing each transaction against other transactions from the same customer
# MAGIC within a rolling time window — a window function that needs the full partition.
# MAGIC The pipeline is triggered on a schedule so "near real-time" latency is achieved
# MAGIC via frequent batch triggers (e.g., every 1–5 minutes).

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

df_silver = spark.read.format("delta").table(SILVER_TABLE)

print(f"Records read from Silver: {df_silver.count()}")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 3: Velocity Detection
# MAGIC
# MAGIC For each transaction, count how many transactions the same customer made
# MAGIC in the 10 minutes **before and including** this transaction.
# MAGIC A count > 1 indicates rapid successive transactions — a common fraud signal.

# COMMAND ----------

# Window ordered by transaction_time (cast to Unix seconds for rangeBetween)
velocity_window = (
    Window
    .partitionBy("customer_id")
    .orderBy(F.col("transaction_time").cast("long"))
    .rangeBetween(-VELOCITY_WINDOW_SECONDS, 0)
)

df_with_velocity = df_silver.withColumn(
    "txn_count_10min",
    F.count("transaction_id").over(velocity_window)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 4: Apply Fraud Scoring Rules
# MAGIC
# MAGIC Each rule contributes a fixed score. Scores are summed and capped at 100.

# COMMAND ----------

df_scored = (
    df_with_velocity

    # ── Rule 1: High Amount (spend_ratio > 3x baseline) ──────────────────────
    .withColumn(
        "high_amount_flag",
        F.when(F.col("spend_ratio") > SPEND_RATIO_THRESHOLD, 1).otherwise(0)
    )
    .withColumn(
        "high_amount_score",
        F.when(F.col("spend_ratio") > SPEND_RATIO_THRESHOLD, SCORE_HIGH_AMOUNT).otherwise(0)
    )

    # ── Rule 2: Location Mismatch ─────────────────────────────────────────────
    .withColumn(
        "location_mismatch_flag",
        F.when(F.col("location_mismatch") == True, 1).otherwise(0)
    )
    .withColumn(
        "location_mismatch_score",
        F.when(F.col("location_mismatch") == True, SCORE_LOCATION_MISMATCH).otherwise(0)
    )

    # ── Rule 3: Odd Hours ─────────────────────────────────────────────────────
    .withColumn(
        "odd_hours_flag",
        F.when(F.col("is_odd_hours") == True, 1).otherwise(0)
    )
    .withColumn(
        "odd_hours_score",
        F.when(F.col("is_odd_hours") == True, SCORE_ODD_HOURS).otherwise(0)
    )

    # ── Rule 4: Category Mismatch ─────────────────────────────────────────────
    .withColumn(
        "category_mismatch_flag",
        F.when(F.col("category_mismatch") == True, 1).otherwise(0)
    )
    .withColumn(
        "category_mismatch_score",
        F.when(F.col("category_mismatch") == True, SCORE_CATEGORY_MISMATCH).otherwise(0)
    )

    # ── Rule 5: Velocity ──────────────────────────────────────────────────────
    .withColumn(
        "velocity_flag",
        F.when(F.col("txn_count_10min") > 1, 1).otherwise(0)
    )
    .withColumn(
        "velocity_score",
        F.when(F.col("txn_count_10min") > 1, SCORE_VELOCITY).otherwise(0)
    )
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 5: Compute Total Risk Score & Fraud Label

# COMMAND ----------

df_gold = (
    df_scored

    # ── Sum all rule scores, cap at MAX_SCORE ─────────────────────────────────
    .withColumn(
        "risk_score",
        F.least(
            F.col("high_amount_score")       +
            F.col("location_mismatch_score") +
            F.col("odd_hours_score")         +
            F.col("category_mismatch_score") +
            F.col("velocity_score"),
            F.lit(MAX_SCORE)
        )
    )

    # ── Assign fraud label ────────────────────────────────────────────────────
    .withColumn(
        "fraud_label",
        F.when(F.col("risk_score") >= THRESHOLD_HIGH,   "HIGH")
         .when(F.col("risk_score") >= THRESHOLD_MEDIUM, "MEDIUM")
         .otherwise("LOW")
    )

    # ── Count how many rules were triggered ───────────────────────────────────
    .withColumn(
        "rules_triggered",
        F.col("high_amount_flag")       +
        F.col("location_mismatch_flag") +
        F.col("odd_hours_flag")         +
        F.col("category_mismatch_flag") +
        F.col("velocity_flag")
    )

    # ── Audit column ──────────────────────────────────────────────────────────
    .withColumn("gold_timestamp", F.current_timestamp())

    # ── Select final Gold columns ─────────────────────────────────────────────
    .select(
        # Identity
        "transaction_id",
        "customer_id",
        "card_id",
        "transaction_time",

        # Transaction context
        "amount",
        "merchant",
        "merchant_category",
        "location",
        "home_location",
        "avg_spend_per_day",
        "preferred_category",

        # Derived features
        "spend_ratio",
        "hour_of_day",
        "is_weekend",
        "is_odd_hours",
        "txn_count_10min",

        # Rule flags (1 = triggered, 0 = not triggered)
        "high_amount_flag",
        "location_mismatch_flag",
        "odd_hours_flag",
        "category_mismatch_flag",
        "velocity_flag",

        # Scoring
        "high_amount_score",
        "location_mismatch_score",
        "odd_hours_score",
        "category_mismatch_score",
        "velocity_score",
        "risk_score",
        "fraud_label",
        "rules_triggered",

        # Audit
        "gold_timestamp",
    )
)

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 6: Write to Gold Delta Table

# COMMAND ----------

(
    df_gold.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(GOLD_TABLE)
)

print("Gold layer fraud scoring complete.")

# COMMAND ----------
# MAGIC %md
# MAGIC ### Step 7: Fraud Alert Summary Dashboard
# MAGIC
# MAGIC These queries power the monitoring dashboards and alerting systems.

# COMMAND ----------

print("=" * 60)
print("   FRAUD RISK SCORING PIPELINE - RESULTS SUMMARY")
print("=" * 60)

# ── Overall distribution ──────────────────────────────────────────────────────
print("\n=== Risk Label Distribution ===")
spark.sql(f"""
    SELECT
        fraud_label,
        COUNT(*)                        AS total_transactions,
        ROUND(AVG(risk_score), 1)       AS avg_risk_score,
        MIN(risk_score)                 AS min_score,
        MAX(risk_score)                 AS max_score,
        ROUND(SUM(amount), 2)           AS total_amount_at_risk
    FROM {GOLD_TABLE}
    GROUP BY fraud_label
    ORDER BY avg_risk_score DESC
""").show(truncate=False)

# ── HIGH risk transactions (requires immediate action) ────────────────────────
print("\n=== HIGH Risk Transactions ===")
spark.sql(f"""
    SELECT
        transaction_id,
        customer_id,
        amount,
        merchant,
        location,
        risk_score,
        high_amount_flag,
        location_mismatch_flag,
        odd_hours_flag,
        category_mismatch_flag,
        velocity_flag,
        rules_triggered
    FROM {GOLD_TABLE}
    WHERE fraud_label = 'HIGH'
    ORDER BY risk_score DESC
""").show(truncate=False)

# ── Rule trigger frequency ────────────────────────────────────────────────────
print("\n=== Fraud Rule Trigger Frequency ===")
spark.sql(f"""
    SELECT
        'High Amount (>3x baseline)'  AS rule,
        SUM(high_amount_flag)         AS triggered,
        ROUND(SUM(high_amount_flag) * 100.0 / COUNT(*), 1) AS pct
    FROM {GOLD_TABLE}
    UNION ALL
    SELECT
        'Location Mismatch',
        SUM(location_mismatch_flag),
        ROUND(SUM(location_mismatch_flag) * 100.0 / COUNT(*), 1)
    FROM {GOLD_TABLE}
    UNION ALL
    SELECT
        'Odd Hours (00-05 or 23+)',
        SUM(odd_hours_flag),
        ROUND(SUM(odd_hours_flag) * 100.0 / COUNT(*), 1)
    FROM {GOLD_TABLE}
    UNION ALL
    SELECT
        'Category Mismatch',
        SUM(category_mismatch_flag),
        ROUND(SUM(category_mismatch_flag) * 100.0 / COUNT(*), 1)
    FROM {GOLD_TABLE}
    UNION ALL
    SELECT
        'Velocity (>1 txn in 10 min)',
        SUM(velocity_flag),
        ROUND(SUM(velocity_flag) * 100.0 / COUNT(*), 1)
    FROM {GOLD_TABLE}
    ORDER BY triggered DESC
""").show(truncate=False)

# ── Per-customer risk summary ─────────────────────────────────────────────────
print("\n=== Per-Customer Risk Summary ===")
spark.sql(f"""
    SELECT
        customer_id,
        COUNT(*)                              AS total_transactions,
        SUM(CASE WHEN fraud_label = 'HIGH'   THEN 1 ELSE 0 END) AS high_risk_count,
        SUM(CASE WHEN fraud_label = 'MEDIUM' THEN 1 ELSE 0 END) AS medium_risk_count,
        ROUND(MAX(risk_score), 0)             AS max_risk_score,
        ROUND(SUM(amount), 2)                 AS total_spend
    FROM {GOLD_TABLE}
    GROUP BY customer_id
    ORDER BY high_risk_count DESC, max_risk_score DESC
""").show(truncate=False)

# ── Top 5 riskiest transactions ───────────────────────────────────────────────
print("\n=== Top 5 Highest Risk Transactions ===")
spark.sql(f"""
    SELECT
        transaction_id,
        customer_id,
        amount,
        merchant,
        merchant_category,
        location,
        hour_of_day,
        txn_count_10min,
        risk_score,
        fraud_label
    FROM {GOLD_TABLE}
    ORDER BY risk_score DESC
    LIMIT 5
""").show(truncate=False)
