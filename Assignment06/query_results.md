# Assignment 6 — Query Results & Insights

## Q1: Driver, Cluster Manager, Executor

**Answer:**
- **Driver** — the process running the application's `main()`/`SparkSession`. It builds the logical plan, optimizes it into a DAG of stages and tasks, schedules those tasks, and collects/aggregates the final results. It's the only process that sees the "whole picture."
- **Cluster Manager** — the resource broker (Standalone, YARN, Kubernetes, Mesos) that the Driver asks for compute. It doesn't run any user code — its only job is to launch and track Executor processes on worker nodes per the Driver's request.
- **Executor** — JVM processes on worker nodes that actually run the scheduled tasks in parallel, hold cached partitions in memory/disk across operations, and stream status + results back to the Driver.

**Result (output from a live local session, `spark_assignment.py`):**
| Property | Value |
|---|---|
| Cluster manager | `local[*]` |
| Driver UI | `http://DESKTOP-CAUGPAH:4040` |
| Application ID | `local-1780892859210` |
| Executors attached | `1` |
| Default parallelism | `8` (= local CPU cores) |

**Insight:** In `local[*]` mode the Driver and Executor collide into a single JVM, which is perfect for development but hides the network hop that dominates real cluster behavior — on a real cluster, Driver↔Executor communication (task dispatch, shuffle metadata, result collection) is the first place to look when diagnosing latency.

---

## Q2: Lazy Evaluation

**Answer:** Spark splits work into **transformations** (which only record *what* should happen, building a logical plan/DAG) and **actions** (which actually trigger execution). Nothing touches data until an action is called.

**Insight:** Because the *entire* chain is visible to Spark's Catalyst optimizer before anything runs, it can rewrite the plan as a whole — pushing filters down to the source, pruning unused columns, reordering predicates to run the cheapest/most-selective filter first, and fusing many narrow row-by-row operations into a single pass per partition (pipelining). The practical effect on a long chain of `.filter().select().withColumn().orderBy()` calls: the dataset is scanned **once**, with the minimum necessary work per row, instead of materializing — and re-reading — an intermediate result after every line, the way eager row-at-a-time engines do.

**Result (`.explain()` / `.show(3)` output for `df.filter(category=='Electronics').select(...).withColumn("price_with_tax",...).orderBy(...)`):**
```
== Physical Plan ==
AdaptiveSparkPlan isFinalPlan=false
+- Sort [price_with_tax#69 DESC NULLS LAST], true, 0
   +- Exchange rangepartitioning(price_with_tax#69 DESC NULLS LAST, 200), ENSURE_REQUIREMENTS, [plan_id=43]
      +- Project [product_id#18, price#21, base_price#22, round((price#21 * 1.18), 2) AS price_with_tax#69]
         +- Filter (isnotnull(category#20) AND (category#20 = Electronics))
            +- FileScan csv [...] PushedFilters: [IsNotNull(category), EqualTo(category,Electronics)], ReadSchema: struct<product_id:string,category:string,price:double,base_price:double>
```
```
+----------+-----+----------+--------------+
|product_id|price|base_price|price_with_tax|
+----------+-----+----------+--------------+
|     P1016|329.0|    278.81|        388.22|
|     P1013|229.0|    194.07|        270.22|
|     P1011|159.0|    134.75|        187.62|
+----------+-----+----------+--------------+
```
`.explain()` printed only the plan above — **zero** Spark jobs ran. `.show(3)` is the line that triggered the one job that actually scanned, filtered, projected, computed `price_with_tax`, sorted, and returned 3 rows.

**Bonus observation:** notice the plan already shows `ReadSchema: struct<product_id, category, price, base_price>` — only 4 of the source's 10 columns. Catalyst pruned the unused columns (`user_id`, `product_name`, `region`, `priority`, `status`, `amount`) out of the scan *before* execution, purely by analyzing the whole lazy chain — a concrete instance of the "scanned once, minimum necessary work" benefit described above.

---

## Q3: Read CSV with header + inferSchema

```python
df = (spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv("data/source.csv"))
```

**Result (`printSchema()` / `show(5)` output):**
```
root
 |-- user_id: integer (nullable = true)
 |-- product_id: string (nullable = true)
 |-- product_name: string (nullable = true)
 |-- category: string (nullable = true)
 |-- price: double (nullable = true)
 |-- base_price: double (nullable = true)
 |-- region: string (nullable = true)
 |-- priority: string (nullable = true)
 |-- status: string (nullable = true)
 |-- amount: double (nullable = true)

+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
|user_id|product_id|        product_name|   category|price|base_price|region|priority|   status|amount|
+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
|      1|     P1001|   Wireless Mouse V1|Electronics|29.99|     25.42| North|    High|Completed|1499.5|
|      2|     P1002|Office Chair Classic|  Furniture|189.5|    160.59| South|  Medium|Completed| 948.0|
|   NULL|     P1003|Bluetooth Speaker...|Electronics|49.99|     42.36|  East|     Low|  Pending|249.95|
|      4|     P1004|   Standing Desk Pro|  Furniture|399.0|    338.14|  West|    High|Completed|1995.0|
|      5|     P1005|Mechanical Keyboa...|Electronics|89.99|     76.26| North|  Medium|Cancelled|179.98|
+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
only showing top 5 rows
```
18 rows, 10 columns, every type correctly inferred — including spotting the blank `user_id` cells as `NULL` integers rather than empty strings.

**Insight:** `inferSchema=true` is convenient for exploration, but it forces Spark to make an **extra full pass over the file** just to sample types before the real read begins — on large files this roughly doubles I/O. In production pipelines it's standard to define an explicit `StructType` schema instead (as done for the raw batch in Q6), trading a few lines of code for a single-pass, deterministic load.

---

## Q4: CSV vs Parquet — storage layout and why it matters

**Answer:**
| | CSV | Parquet |
|---|---|---|
| Layout | Row-based, plain text | Columnar, binary, compressed (Snappy by default) |
| Schema | None — inferred or supplied at read time | Embedded in the file footer |
| Reading a subset of columns | Must read & parse every column of every row | Reads only the requested columns off disk (column pruning) |
| Filtering | No help from the format — Spark filters after a full read | Per row-group min/max statistics let the reader skip whole blocks (→ Q9, predicate pushdown) |

**Concretely, on *this* dataset:** `data/source.csv` has 10 columns. The Q2 plan above already shows Spark reading only `struct<product_id, category, price, base_price>` — 4 columns — when that's all a query needs. A CSV reader has no choice but to read and tokenize **all 10** columns of **every** row to get at those 4, because text rows can't be sliced by column. A Parquet version of the same file would let the reader fetch *only* those 4 columns' bytes off disk — the other 6 columns' data would never even be touched.

**Insight:** The gap is invisible on an 18-row toy file but compounds violently at scale: a 2 TB CSV table where a report needs 3 of 40 columns means scanning and parsing the full 2 TB; the Parquet equivalent might touch only ~150 GB. Columnar formats are *the* default choice for analytical (read-heavy, column-selective) workloads for exactly this reason.

---

## Q5: Select product_id, price where category = 'Electronics'

```python
df.select("product_id", "price").filter(F.col("category") == "Electronics")
```

**Result (`.show()` output):**
```
+----------+-----+
|product_id|price|
+----------+-----+
|     P1001|29.99|
|     P1003|49.99|
|     P1005|89.99|
|     P1007| 79.0|
|     P1009|39.99|
|     P1011|159.0|
|     P1013|229.0|
|     P1015|109.0|
|     P1016|329.0|
|     P1018|19.99|
+----------+-----+
```
10 of the 18 products are `Electronics`.

**Insight:** Calling `.select()` *before* `.filter()` makes no execution difference here — Catalyst reorders both into a single combined `Filter` + `Project` node regardless of the order they're written in. Write the version that reads most naturally; let the optimizer handle the physical ordering.

---

## Q6: Revise a DataFrame — rename `old_name`→`new_name`, cast `price` String→Double

```python
df_revised = (df_raw
              .withColumnRenamed("old_name", "new_name")
              .withColumn("price", F.col("price").cast(DoubleType())))
```

**Result:**
| Stage | new_name | price (type) |
|---|---|---|
| Before | *(column was `old_name`)* | `"29.99"` (string) |
| After | `Wireless Mouse V1` | `29.99` (double) |

Schema confirms `new_name: string, price: double` after revision — `old_name` no longer exists.

**Insight:** `withColumnRenamed` is a pure metadata operation (no data movement); `.cast()` is the operation that actually re-encodes every value. Casting an unparsable string (e.g. `"N/A"`) silently produces `null` rather than raising — worth an explicit `.filter(col("price").isNotNull())` audit step right after any String→numeric cast in a real pipeline.

---

## Q7: Lineage Graph (DAG) and fault tolerance

**Answer:** Every RDD/DataFrame doesn't just hold data — it remembers **how it was derived**: its parent RDD(s) plus the transformation applied to get from parent to child. Chaining transformations therefore builds a graph of these parent→child relationships, the **lineage graph** (a DAG, since data only ever flows forward from sources to results).

When a worker node fails mid-job, the Driver detects the lost partitions (missed heartbeats / failed task results), looks up *only those partitions'* lineage, and **re-schedules just the lost tasks** on healthy executors. Spark recomputes the missing partitions by replaying the recorded transformations against the original source data — it never needs to recompute the whole job, and it never needed to replicate data up front.

**Result (`chained.rdd.toDebugString()` output for the Q2 pipeline):**
```
(1) MapPartitionsRDD[41] at javaToPython at NativeMethodAccessorImpl.java:0 []
 |  MapPartitionsRDD[40] at javaToPython at NativeMethodAccessorImpl.java:0 []
 |  SQLExecutionRDD[39] at javaToPython at NativeMethodAccessorImpl.java:0 []
 |  MapPartitionsRDD[38] at $anonfun$withThreadLocalCaptured$2 ... []
 |  ShuffledRowRDD[37] at $anonfun$withThreadLocalCaptured$2 ... []
 +-(1) MapPartitionsRDD[36] at $anonfun$withThreadLocalCaptured$2 ... []
    |  MapPartitionsRDD[32] at $anonfun$withThreadLocalCaptured$2 ... []
    |  MapPartitionsRDD[31] at $anonfun$withThreadLocalCaptured$2 ... []
    |  FileScanRDD[30] at $anonfun$withThreadLocalCaptured$2 ... []
```
Read bottom-up: the chain is **rooted in `FileScanRDD[30]`** (the raw `source.csv` scan), then climbs through `MapPartitionsRDD`s (the `filter`/`select`/`withColumn` projections), a `ShuffledRowRDD` (the `orderBy`'s shuffle/exchange), and finally the `MapPartitionsRDD`s that hand rows back to Python for `.show()`. Every `|` is a recorded parent→child dependency — exactly the chain Spark would replay, starting from whichever RDD still has its data, if a partition further down were lost.

**Insight:** This is *the* foundational difference from systems like classic Hadoop MapReduce-on-HDFS, which buy fault tolerance with **physical replication** (3× block copies). Spark instead buys it with **recomputation from lineage** — cheaper to set up, but it means a very long, very narrow lineage chain (e.g. thousands of chained `.filter()`s on a streaming job) can make recovery slow; that's exactly the scenario `.checkpoint()` exists to truncate.

---

## Q8: Filter df_orders — status = 'Completed' AND amount > 1000

```python
df_orders.filter((F.col("status") == "Completed") & (F.col("amount") > 1000))
```

**Result (`.show()` output — `df_orders` is `df` with `product_name` aliased to `order_item`):**
```
+----------+--------------------+---------+------+
|product_id|          order_item|   status|amount|
+----------+--------------------+---------+------+
|     P1001|   Wireless Mouse V1|Completed|1499.5|
|     P1004|   Standing Desk Pro|Completed|1995.0|
|     P1007|           4K Webcam|Completed|1185.0|
|     P1010|       Bookshelf Oak|Completed|1050.0|
|     P1011|Noise Cancelling ...|Completed|1590.0|
|     P1015|    Portable SSD 1TB|Completed|1308.0|
|     P1016| Gaming Monitor 27in|Completed|1645.0|
+----------+--------------------+---------+------+
```
7 of 18 rows matched both conditions.

**Insight:** Always wrap each condition in parentheses when combining with `&`/`|` in PySpark — `&` binds tighter than `==` at the Python level, so `df.filter(col("status") == "Completed" & col("amount") > 1000)` raises a confusing type error. This is one of the most common first-week PySpark gotchas.

---

## Q9: Predicate Pushdown in Parquet

**Answer:** Parquet stores data **column-by-column inside row-groups**, and each row-group carries **min/max statistics** for every column in its footer. When a `.filter()` is applied to a Parquet read, Spark's Catalyst optimizer "pushes" that filter expression all the way down into the file-scan/reader node — visible in the physical plan as `PushedFilters: [...]`. The Parquet reader then:
1. Consults the row-group statistics and **skips entire row-groups** that cannot possibly satisfy the filter (e.g., a group whose `category` min/max range doesn't include `"Electronics"`), without decompressing or decoding them at all;
2. For groups it must read, decodes **only the columns the query needs**.

**Result — honest note on this run:** the script attempts `df.write.parquet(...)` to materialize a Parquet file, then reads it back with a filter and calls `.explain()`. On **this Windows machine**, the local Parquet *write* itself fails:
```
FileNotFoundException: HADOOP_HOME and hadoop.home.dir are unset
```
This is a well-known Windows-only gap — Spark's bundled Hadoop filesystem layer needs the companion binary `winutils.exe` (+ `hadoop.dll`) to perform local file *write* operations (permission/commit bookkeeping); it is **not** required for reads, which is exactly why Q1, Q3, Q5, Q6, Q8, Q10, Q11, Q14, Q15 all ran perfectly against the same `source.csv` on this box. The script catches this and reports it gracefully rather than crashing — see the `>>> Local Parquet WRITE skipped...` message in the run log.

The **code shown above is the correct, complete answer** and runs unmodified on any properly configured machine/cluster (Linux, a cloud notebook, or Windows with `HADOOP_HOME` pointed at `winutils.exe`). We can also point to **direct evidence from this very session** of what its `explain()` would show: the Q2 plan (captured live, above) already prints
```
PushedFilters: [IsNotNull(category), EqualTo(category,Electronics)]
```
on a `FileScan` node for the *exact same* filter — confirming Catalyst builds and attaches a `PushedFilters` clause for this predicate. Reading from `parquet(...)` instead of `csv(...)` would produce the identical `PushedFilters` clause on a `FileScan parquet` node — with the crucial difference described in the Insight below.

**Insight — the nuance the live CSV plan exposes:** seeing `PushedFilters` appear on a *CSV* scan (Q2's plan) could make it look like CSV gets the same benefit. It doesn't, and the difference is exactly what makes Parquet special: for CSV, `PushedFilters` only means "evaluate this condition as each row is parsed, instead of after" — Spark still must read and tokenize **every byte of every row** because text has no internal structure to skip by. For Parquet, the *same-looking* `PushedFilters` clause additionally lets the reader consult per-row-group min/max statistics **before** decompressing anything, and skip whole row-groups wholesale — the file's columnar, binary layout is what makes that skip physically possible. On a partitioned, multi-GB Parquet table that distinction can mean the difference between physically reading 2 GB and 20 MB; on CSV, the byte count is the byte count no matter how the filter is written.

---

## Q10: Add final_price = base_price × 1.18

```python
df.withColumn("final_price", F.round(F.col("base_price") * 1.18, 2))
```

**Result (`.show(5)` output):**
```
+----------+----------+-----------+
|product_id|base_price|final_price|
+----------+----------+-----------+
|     P1001|     25.42|       30.0|
|     P1002|    160.59|      189.5|
|     P1003|     42.36|      49.98|
|     P1004|    338.14|     399.01|
|     P1005|     76.26|      89.99|
+----------+----------+-----------+
only showing top 5 rows
```

**Insight:** `withColumn` on an existing name *replaces* a column; on a new name it *appends* one — both compile down to a `Project` node, so there's no performance difference between "adding" and "overwriting." Wrapping the arithmetic in `F.round(..., 2)` here avoids floating-point noise like `30.0036` leaking into a price field that downstream systems will display to users.

---

## Q11: Transformations vs Actions

**Answer:**
| | Transformations | Actions |
|---|---|---|
| Behavior | **Lazy** — recorded into the logical plan/DAG, nothing computed | **Eager** — triggers an actual Spark job |
| Returns | A new DataFrame/RDD | A value to the driver, or a side effect (write to storage) |
| Examples | `.filter()`, `.select()`, `.withColumn()`, `.groupBy()`, `.join()`, `.map()` | `.count()`, `.collect()`, `.show()`, `.write()`, `.take()`, `.reduce()` |

**Result (output — `t1 = df.filter(amount > 500)`, `t2 = t1.select("product_id","amount")`):**
```
Two transformations chained — 0 Spark jobs triggered so far.
count() -> 8 rows matched   |   take(3) -> [Row(product_id='P1001', amount=1499.5),
                                            Row(product_id='P1002', amount=948.0),
                                            Row(product_id='P1004', amount=1995.0)]
Both lines above triggered real Spark jobs — that's the lazy/eager split in action.
```
Building `t1` and `t2` printed nothing and ran nothing — pure plan-building. The instant `.count()` ran, Spark launched a real job (visible as a new entry in the Driver UI's job list at `:4040`); `.take(3)` launched a second.

**Insight:** This split is the mechanism *behind* lazy evaluation (Q2) — transformations are how the DAG gets built, actions are the trigger that submits it. A useful debugging habit: if a notebook cell "runs instantly," it almost certainly only contains transformations; the cell that actually takes time is the one with the action.

---

## Q12: Parquet → filter user_id NOT NULL → write CSV

```python
(spark.read.parquet("path/to/input")
      .filter(F.col("user_id").isNotNull())
      .write.option("header", "true").csv("path/to/output"))
```

**Result — same environment limitation as Q9:** the Parquet *write* used to materialize `"path/to/input"` fails locally with the identical `HADOOP_HOME and hadoop.home.dir are unset` error (winutils.exe missing on Windows), so the full read→filter→write chain can't complete end-to-end on this machine. Rather than fabricate a result, the script catches this and instead runs **just the filter logic** directly against the CSV-sourced `df` (no write involved) to prove out the row counts the real pipeline would produce:
```
Rows before filter: 18
Rows after  filter: 15  (rows with null user_id dropped)
```
This matches the data exactly — `source.csv` has 3 blank `user_id` cells (rows `P1003`, `P1006`, `P1012`), and 18 − 3 = 15. The **code block above is the unmodified, correct answer** to the question and would run start-to-finish on Linux, a cloud notebook, or a properly configured Windows box.

**Insight:** Reading Parquet *and* filtering on `user_id` here is a textbook predicate-pushdown case (→ Q9) — `IsNotNull(user_id)` would show up in `PushedFilters`, so rows with a null `user_id` get discarded at the source scan rather than loaded and then dropped. The whole pipeline — read, filter, write — is a single chain of lazy transformations that executes exactly once, when `.write.csv(...)` (the action) is finally called; Spark never materializes an intermediate "filtered Parquet" in memory between the steps.

---

## Q13: Client Mode vs Cluster Mode

**Answer:**
- **Client mode** — the **Driver runs on the machine that submitted the job** (your laptop, a notebook server, an edge node) — *outside* the cluster. Executors run in the cluster and communicate back to that external Driver. Great for interactive work (`spark-shell`, notebooks, iterative debugging with live output), but the job dies the instant that machine disconnects, and every Driver↔Executor message pays a network hop in/out of the cluster.
- **Cluster mode** — the **Cluster Manager launches the Driver itself inside the cluster** (on one of the worker nodes), alongside the Executors. The submitting machine can disconnect the moment the job is accepted — the application keeps running unattended. This is the standard for production/scheduled batch jobs: it's resilient to the submitter going away, and the Driver sits physically close to its Executors.

**Result (output):** `spark.conf.get("spark.submit.deployMode", ...)` reported **`client`** for this local session — exactly as expected, since `local[*]` always runs the Driver in the same process that launched it.

**Insight:** The rule of thumb: **client mode for development and interactive exploration** (you want to see `print()`/`show()` output live in your terminal or notebook); **cluster mode for `spark-submit`'d production jobs** run via a scheduler (Airflow, cron, Databricks Jobs) where nobody is watching the terminal and the job must survive the submitting process exiting.

---

## Q14: Filter — region = 'North' OR priority = 'High'

```python
df.filter((F.col("region") == "North") | (F.col("priority") == "High"))
```

**Result (`.show()` output):**
```
+----------+------+--------+
|product_id|region|priority|
+----------+------+--------+
|     P1001| North|    High|
|     P1004|  West|    High|
|     P1005| North|  Medium|
|     P1007|  East|    High|
|     P1008| North|  Medium|
|     P1010| South|    High|
|     P1011| North|    High|
|     P1014| North|  Medium|
|     P1015| South|    High|
|     P1016|  East|    High|
|     P1018| North|  Medium|
+----------+------+--------+
```
**11 of 18** rows matched the `OR`. Swap that same query to `region == 'North' AND priority == 'High'` and only **2** rows (`P1001`, `P1011`) would qualify — a clean illustration of just how much less selective `OR` is than `AND` over the very same two columns.

**Insight:** Same parenthesization rule as Q8 applies (`|` binds tighter than `==`) — omitting the parens around each comparison is the single most common syntax error PySpark beginners hit when combining boolean conditions.

---

## Q15: Why `.show(5)` is safer than `.collect()` on a multi-terabyte dataset

**Answer:** `.show(5)` asks Spark for just enough rows to display five — it stops pulling as soon as the driver has them, so memory usage is small and **constant**, completely independent of how big the underlying dataset actually is. `.collect()`, by contrast, is an action that gathers **every row of every partition across the entire cluster back into the Driver's single JVM heap**. On a multi-terabyte dataset, that's terabytes of data trying to land on one machine — a near-guaranteed `OutOfMemoryError` / Driver crash, plus a wave of needless network shuffle, just to "peek" at the data.

**Result (output — identical to the Q3 read-back, since it's the same `df`):**
```
+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
|user_id|product_id|        product_name|   category|price|base_price|region|priority|   status|amount|
+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
|      1|     P1001|   Wireless Mouse V1|Electronics|29.99|     25.42| North|    High|Completed|1499.5|
|      2|     P1002|Office Chair Classic|  Furniture|189.5|    160.59| South|  Medium|Completed| 948.0|
|   NULL|     P1003|Bluetooth Speaker...|Electronics|49.99|     42.36|  East|     Low|  Pending|249.95|
|      4|     P1004|   Standing Desk Pro|  Furniture|399.0|    338.14|  West|    High|Completed|1995.0|
|      5|     P1005|Mechanical Keyboa...|Electronics|89.99|     76.26| North|  Medium|Cancelled|179.98|
+-------+----------+--------------------+-----------+-----+----------+------+--------+---------+------+
only showing top 5 rows
```
`df.show(5)` printed exactly 5 of the 18 rows without incident — and would print the *exact same 5 rows* in the *exact same time and memory footprint* if `source.csv` were instead a 5 TB table, because the action only ever asks partitions for "enough rows to fill 5," then stops.

**Insight:** The general rule: reach for `.show(n)`, `.take(n)`, `.limit(n).toPandas()`, or `.sample()` whenever you're *exploring*; reserve `.collect()` for the rare case where you've already proven (via `.count()` or aggregation) that the result set is small enough to fit comfortably in driver memory — e.g., the output of a `groupBy().agg()` that's collapsed millions of rows down to a few dozen summary rows.

---

## Performance & Architecture — overall takeaways

1. **Laziness is the optimizer's superpower** (Q2, Q11): because Spark sees the whole transformation chain before running anything, Catalyst can fuse, reorder, and prune work — the same chain that looks like "10 separate passes" in the code compiles down to a handful of actual stages.
2. **Format choice changes the shape of the I/O bottleneck** (Q4, Q9): columnar + statistics-bearing formats like Parquet let Spark *not read* data it doesn't need (column pruning + predicate pushdown) — the cheapest byte is the one you never load.
3. **Fault tolerance is "free" because of lineage, not replication** (Q7): Spark recomputes lost partitions from their recorded DAG instead of restoring from physical copies — cheap to provide, but it puts a premium on keeping lineage chains reasonably short (`.checkpoint()`/`.cache()` when they get long).
4. **Architecture choices should match the workload, not habit** (Q1, Q13): `local[*]` / client mode for development and exploration where you want to *see* what's happening; cluster mode + a real cluster manager for unattended production jobs that must survive the submitter disconnecting.
5. **Driver memory is the scarcest resource in the whole system** (Q15): almost every "Spark job crashed" incident traces back to something — `.collect()`, a skewed `groupBy`, a broadcast join on an oversized table — pulling more data into that one JVM than it can hold. Defaulting to `.show()`/`.take()`/aggregation-first habits avoids the entire class of problem.
