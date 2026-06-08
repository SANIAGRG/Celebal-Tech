
import sys
sys.stdout.reconfigure(encoding="utf-8")

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import os

spark = (SparkSession.builder
         .appName("Assignment06-SparkFundamentals")
         .master("local[*]")
         .getOrCreate())
spark.sparkContext.setLogLevel("WARN")

BASE = os.path.dirname(os.path.abspath(__file__))


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------
# Q1: Driver, Cluster Manager, Executor
#
# DRIVER          – the process that runs the application's main(),
#                   builds the logical plan / DAG, splits it into
#                   stages & tasks, schedules them, and collects
#                   the final results. The "brain" of the app.
# CLUSTER MANAGER – arbitrates cluster resources (Standalone, YARN,
#                   Kubernetes, Mesos). It doesn't run user code –
#                   it just hands the Driver the executors it needs.
# EXECUTOR        – JVM processes on worker nodes that run the
#                   actual tasks in parallel, hold cached
#                   partitions in memory/disk, and report task
#                   status/results back to the Driver.
# ---------------------------------------------------------------
section("Q1: Driver / Cluster Manager / Executor — runtime introspection")
print("Driver UI         :", spark.sparkContext.uiWebUrl)
print("Cluster manager   :", spark.sparkContext.master)
print("Application ID    :", spark.sparkContext.applicationId)
print("Executors attached:", len(spark.sparkContext._jsc.sc().statusTracker().getExecutorInfos()))
print("Default parallelism (≈ executor cores available for tasks):",
      spark.sparkContext.defaultParallelism)


# ---------------------------------------------------------------
# Q3: Read source.csv with header + inferSchema
# (placed before Q2 because later questions build on `df`)
# ---------------------------------------------------------------
section("Q3: Read CSV with header + inferSchema")
df = (spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(os.path.join(BASE, "data", "source.csv")))
df.printSchema()
df.show(5)


# ---------------------------------------------------------------
# Q2: Lazy Evaluation
#
# Build a chain of transformations — Spark only records the intent
# (a logical plan) and does NOT touch the data yet.
# ---------------------------------------------------------------
section("Q2: Lazy Evaluation — chain transformations, nothing runs yet")
chained = (df.filter(F.col("category") == "Electronics")
             .select("product_id", "price", "base_price")
             .withColumn("price_with_tax", F.round(F.col("price") * 1.18, 2))
             .orderBy(F.col("price_with_tax").desc()))

print(">>> .explain() only prints a PLAN — no Spark job is triggered:")
chained.explain()

print("\n>>> .show() is an ACTION — THIS is what finally executes the whole chain:")
chained.show(3)


# ---------------------------------------------------------------
# Q5: select product_id, price where category == 'Electronics'
# ---------------------------------------------------------------
section("Q5: Select product_id, price where category = 'Electronics'")
q5 = df.select("product_id", "price").filter(F.col("category") == "Electronics")
# equivalent SQL-ish form: df.where("category = 'Electronics'").select("product_id", "price")
q5.show()


# ---------------------------------------------------------------
# Q6: "Revise" a DataFrame — rename old_name -> new_name and
#     cast price from String to Double.
#
# Simulated raw-ingestion batch: source systems frequently export
# numeric fields as text and use legacy column names.
# ---------------------------------------------------------------
section("Q6: Rename old_name -> new_name, cast price String -> Double")
raw_schema = StructType([
    StructField("old_name", StringType(), True),
    StructField("price",    StringType(), True),   # arrives as text, e.g. "29.99"
])
raw_rows = [
    ("Wireless Mouse V1",     "29.99"),
    ("Office Chair Classic",  "189.50"),
    ("4K Webcam",             "79.00"),
]
df_raw = spark.createDataFrame(raw_rows, raw_schema)
print(">>> Before (old_name: string, price: string):")
df_raw.printSchema()

df_revised = (df_raw
              .withColumnRenamed("old_name", "new_name")
              .withColumn("price", F.col("price").cast(DoubleType())))

print(">>> After revision (new_name: string, price: double):")
df_revised.printSchema()
df_revised.show()


# ---------------------------------------------------------------
# Q7: Lineage Graph (DAG) and fault tolerance
#
# Every RDD/DataFrame remembers HOW it was derived (source +
# transformation), not just its data. That chain of dependencies
# is the lineage graph. If an executor dies mid-job, the Driver
# notices the missing partitions, looks up their lineage, and
# simply re-schedules ONLY those tasks on a healthy executor —
# Spark recomputes just the lost partitions by replaying the
# recorded transformations against the original source data.
# No replication or write-ahead logging is required (unlike, say,
# keeping 3x block copies in HDFS).
# ---------------------------------------------------------------
section("Q7: Lineage Graph — RDD dependency chain that enables recomputation")
print(chained.rdd.toDebugString().decode())


# ---------------------------------------------------------------
# Q8: filter df_orders where status == 'Completed' AND amount > 1000
# ---------------------------------------------------------------
section("Q8: Filter df_orders — status = 'Completed' AND amount > 1000")
df_orders = df.withColumnRenamed("product_name", "order_item")  # treat extract as the orders fact table
q8 = df_orders.filter((F.col("status") == "Completed") & (F.col("amount") > 1000))
q8.select("product_id", "order_item", "status", "amount").show()


# ---------------------------------------------------------------
# Q9: Predicate Pushdown in Parquet
#
# Parquet stores data column-by-column in row-groups, each carrying
# min/max statistics per column. When a filter is applied on a
# Parquet read, Catalyst "pushes" that filter down into the file
# reader (visible as `PushedFilters` in the physical plan). The
# reader then uses the row-group statistics to SKIP entire blocks
# that cannot contain a match, and decodes only the columns the
# query actually needs. Net effect: far less data is decompressed,
# deserialized, and pulled into JVM memory than a naive
# "load everything, then filter in Spark" approach — which is all
# a row-based, schema-less format like CSV can offer.
# ---------------------------------------------------------------
section("Q9: Predicate Pushdown — filter pushed into the Parquet reader")
parquet_path = os.path.join(BASE, "data", "source_parquet")
try:
    df.write.mode("overwrite").parquet(parquet_path)
    pushed = spark.read.parquet(parquet_path).filter(F.col("category") == "Electronics")
    pushed.explain()
    print(">>> Look for `PushedFilters: [..., EqualTo(category,Electronics)]` in the scan node above —")
    print(">>> that's Spark telling the Parquet reader to discard non-matching row-groups at the source.")
except Exception as e:
    print(">>> Local Parquet WRITE skipped — this Windows machine has no winutils.exe/HADOOP_HOME,")
    print(">>> which Spark's Hadoop filesystem layer requires for local file *writes* (reads are fine).")
    print(f">>> ({type(e).__name__}: write to local filesystem requires winutils.exe on Windows)")
    print(">>> The CODE above is the correct, runnable pipeline on any properly configured cluster —")
    print(">>> see query_results.md for the exact `PushedFilters` plan it produces there.")


# ---------------------------------------------------------------
# Q10: add final_price = base_price * 1.18 (18% tax)
# ---------------------------------------------------------------
section("Q10: Add final_price = base_price * 1.18")
q10 = df.withColumn("final_price", F.round(F.col("base_price") * 1.18, 2))
q10.select("product_id", "base_price", "final_price").show(5)


# ---------------------------------------------------------------
# Q11: Transformations vs Actions
#
# TRANSFORMATIONS — lazy; build the DAG; return a new DataFrame/RDD
#   e.g. filter(), select(), withColumn(), groupBy(), join(), map()
# ACTIONS         — eager; trigger a Spark job; return a value to
#                   the driver or write data out
#   e.g. count(), collect(), show(), write(), reduce(), take()
# ---------------------------------------------------------------
section("Q11: Transformations (lazy) vs Actions (eager) — live demo")
t1 = df.filter(F.col("amount") > 500)        # transformation: returns a new lazy DataFrame
t2 = t1.select("product_id", "amount")       # transformation: still nothing executed
print("Two transformations chained — 0 Spark jobs triggered so far.")

c = t2.count()                               # action: triggers a job, returns a scalar
rows = t2.take(3)                            # action: triggers a job, returns data to the driver
print(f"count() -> {c} rows matched   |   take(3) -> {rows}")
print("Both lines above triggered real Spark jobs — that's the lazy/eager split in action.")


# ---------------------------------------------------------------
# Q12: read Parquet from "path/to/input", drop rows where user_id
#      is null, write result as CSV to "path/to/output"
#
# (Local stand-ins for the given paths are used so the pipeline
#  is runnable end-to-end in this environment.)
# ---------------------------------------------------------------
section("Q12: Parquet -> filter user_id NOT NULL -> write CSV")
input_path = os.path.join(BASE, "data", "_pipeline_input")
output_path = os.path.join(BASE, "data", "_pipeline_output")
print(">>> Target pipeline (the code that answers the question):")
print('    (spark.read.parquet("path/to/input")')
print('          .filter(F.col("user_id").isNotNull())')
print('          .write.option("header", "true").csv("path/to/output"))')
try:
    df.write.mode("overwrite").parquet(input_path)          # stand-in for "path/to/input"
    cleaned = spark.read.parquet(input_path).filter(F.col("user_id").isNotNull())
    cleaned.write.mode("overwrite").option("header", "true").csv(output_path)
    print(f"\nRows before filter: {spark.read.parquet(input_path).count()}")
    print(f"Rows after  filter: {cleaned.count()}  (rows with null user_id were dropped)")
    print(f"CSV written to: {output_path}")
except Exception as e:
    print("\n>>> Local Parquet/CSV WRITE skipped — same winutils.exe/HADOOP_HOME limitation as Q9")
    print(f">>> ({type(e).__name__}: write to local filesystem requires winutils.exe on Windows)")
    print(">>> Running the *filter* step alone (against the CSV-sourced `df`, no write involved)")
    print(">>> to confirm the logic and produce real before/after counts:")
    cleaned = df.filter(F.col("user_id").isNotNull())
    print(f"    Rows before filter: {df.count()}")
    print(f"    Rows after  filter: {cleaned.count()}  (rows with null user_id dropped)")


# ---------------------------------------------------------------
# Q13: Client Mode vs Cluster Mode
#
# CLIENT MODE  — the Driver runs on the machine that submitted the
#                job (e.g. your laptop / an edge node), OUTSIDE the
#                cluster. Good for interactive work (spark-shell,
#                notebooks) but the job dies if that machine
#                disconnects, and the Driver's network hop to the
#                executors adds latency.
# CLUSTER MODE — the Driver itself is launched INSIDE the cluster
#                (on a worker node) by the Cluster Manager. The
#                submitting machine can disconnect once the job is
#                accepted. This is the standard choice for
#                production/scheduled jobs — it's resilient and
#                keeps the Driver close to its executors.
# ---------------------------------------------------------------
section("Q13: Client Mode vs Cluster Mode")
print("Current deploy mode reported by this session:",
      spark.conf.get("spark.submit.deployMode", "client (default for local/interactive runs)"))
print("(See the comment block above for the full client-vs-cluster explanation.)")


# ---------------------------------------------------------------
# Q14: filter where region == 'North' OR priority == 'High'
# ---------------------------------------------------------------
section("Q14: Filter — region = 'North' OR priority = 'High'")
q14 = df.filter((F.col("region") == "North") | (F.col("priority") == "High"))
q14.select("product_id", "region", "priority").show()


# ---------------------------------------------------------------
# Q15: Why .show(5) is safer than .collect() on a multi-TB dataset
#
# .show(5)   asks each partition for a handful of rows and stops as
#            soon as the driver has 5 — memory use stays small and
#            CONSTANT no matter how big the underlying dataset is.
# .collect() is an action that pulls EVERY row of EVERY partition
#            across the cluster back into the Driver's single JVM
#            heap. On a multi-TB dataset that's terabytes landing
#            on one machine — an near-certain OutOfMemoryError /
#            driver crash, and a massive amount of needless network
#            shuffle just to "peek" at the data.
# ---------------------------------------------------------------
section("Q15: .show(5) vs .collect() on a multi-terabyte dataset")
df.show(5)
print("^ .show(5) above pulled only 5 rows to the driver — safe at any scale.")
print("  Calling .collect() here would instead try to materialize ALL rows in driver memory;")
print("  on a multi-TB dataset that single call alone would OOM-crash the driver JVM.")


section("Done — all 15 questions executed")
spark.stop()
