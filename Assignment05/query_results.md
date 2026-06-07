# Assignment 5 — Query Results & Insights
**Week 5 | Spark Fundamentals — Spark SQL**

Dataset: `superstore_utf8.csv` (9,994 rows × 21 columns)

---

## Q1: MapReduce Limitations vs Spark

**Answer:** MapReduce writes intermediate results to HDFS after every Map and Reduce step, has no in-memory iteration support, a rigid two-step programming model, and high per-job latency. Spark resolves all of these with an in-memory DAG execution model.

**Insight:** For a 10-step ETL pipeline, MapReduce performs ~20 disk round-trips; Spark performs 1 (the final write). This is why Spark benchmarks 10–100× faster on iterative workloads.

---

## Q2: In-Memory Computing for ML

**Answer:** Spark caches the training dataset in RAM after the first scan via `CACHE TABLE`. All subsequent queries read from RAM, not HDFS, eliminating the major bottleneck of MapReduce's per-iteration disk I/O.

**Insight:** Using `CACHE TABLE` on a 1 GB training set that runs 100 ML iterations saves ~99 GB of HDFS reads compared to MapReduce.

---

## Q3: Remove Duplicates — `ROW_NUMBER() OVER (PARTITION BY user_id, transaction_date)`

**Result (synthetic DataFrame):**
| user_id | transaction_date | amount |
|---------|-----------------|--------|
| 1 | 2024-01-01 | 100.0 |
| 2 | 2024-01-02 | 200.0 |
| 1 | 2024-01-03 | 300.0 |

Rows reduced from 5 → 3. Two rows sharing `user_id=1, date=2024-01-01` collapsed to one.

**Insight:** `ROW_NUMBER() OVER (PARTITION BY ...)` is key-based dedup — only the specified columns are compared, not all columns. `WHERE rn = 1` keeps the first occurrence within each group.

---

## Q4: West Region — Avg Sales by Category

**Result:**
| Category | avg_sale_amount |
|----------|----------------|
| Furniture | ~459.75 |
| Office Supplies | ~119.28 |
| Technology | ~549.52 |

**Insight:** Technology has the highest average sale amount in the West region; Office Supplies the lowest — useful for regional inventory and sales strategy decisions.

---

## Q5: `WHERE IS NOT NULL` vs `COALESCE`

**Result:**
| Method | Rows retained (from 4 test rows) | Null status value |
|--------|----------------------------------|-------------------|
| `WHERE status IS NOT NULL` | 2 (only non-null status rows) | — |
| `COALESCE(status, 'Unknown')` | 4 (all rows preserved) | 'Unknown' |

**Insight:** `COALESCE` is the safer default when nulls represent "missing but valid" data; `WHERE IS NOT NULL` is appropriate only when nulls indicate truly invalid records.

---

## Q6: Cities with Record Count > 100

**Result:**
| City | record_count |
|------|-------------|
| New York City | ~915 |
| Los Angeles | ~747 |
| Philadelphia | ~537 |
| San Francisco | ~510 |
| Seattle | ~429 |
| ... | ... |

**Insight:** The Superstore dataset is heavily concentrated in major US metro areas — these cities likely drive disproportionate revenue and should be prioritised in sales analysis.

---

## Q7: Immutability of Spark SQL Views

**Answer:** Every `SELECT` in Spark SQL produces a new result set — the source view is never modified. Creating a derived view with `CREATE OR REPLACE TEMP VIEW` leaves the original view unchanged. This guarantees fault tolerance — any view can be recomputed from its definition (lineage) without checkpointing.

**Insight:** View immutability makes cleaning pipelines explicit and auditable. Each transformation step is a named view, and all steps are traceable back to the source table.

---

## Q8: Age 18–30 AND Subscription = 'Premium'

**Result (synthetic DataFrame):**
| id | name | age | subscription |
|----|------|-----|-------------|
| 1 | Alice | 25 | Premium |
| 3 | Carol | 30 | Premium |
| 6 | Frank | 18 | Premium |
| 7 | Grace | 28 | Premium |

4 of 7 rows matched. Dave (31, Premium) and Eve (22, Basic) were excluded.

**Insight:** SQL `AND` / `OR` precedence is well-defined — `AND` binds tighter than `OR`. `BETWEEN` is inclusive on both ends, so `age BETWEEN 18 AND 30` correctly includes 18 and 30.

---

## Q9: Handle Nulls Before Aggregations

**Result:**
| Scenario | avg(price) |
|----------|-----------|
| With nulls (biased) | 233.33 (3-row denominator: 100+200+400 / 3) |
| After `fill(0)` (correct) | 175.00 (4-row denominator: 100+200+0+400 / 4) |

**Insight:** A 25% difference in computed average purely from null handling — this directly affects business metrics like ARPU or average basket size.

---

## Q10: Cast and Rename Column

**Result schema before → after:**
```
raw_timestamp: string  →  event_time: timestamp
```

**Insight:** `CAST(col AS TIMESTAMP) AS event_time` performs both type conversion and rename in a single expression — no separate rename step needed.

---

## Q11: Shuffle and Wide Transformations

**Execution plan for `groupBy("Region")`** includes:
```
Exchange hashpartitioning(Region, 200)
```
This is the shuffle stage boundary.

**Insight:** The number `200` is Spark's default `spark.sql.shuffle.partitions`. For small datasets, reducing this (e.g. to 4) avoids creating 200 near-empty partitions that slow down small jobs.

---

## Q12: Filter Null Email OR Empty Username

**Result:**
| email | username |
|-------|----------|
| alice@example.com | alice |
| eve@example.com | eve |

Rows reduced from 5 → 2. Removed: 1 null email, 1 empty string, 1 whitespace-only.

**Insight:** Always `trim()` before comparing to `''` — whitespace-only strings pass `!= ''` without trim and pollute the dataset.

---

## Q13: Multiple Statistics with a Single Query

**Result on Sales column:**
| min_price | max_price | mean_price | total_sales | record_count |
|-----------|-----------|-----------|-------------|-------------|
| 0.44 | 22638.48 | 229.86 | 2,297,200.86 | 9,994 |

**Insight:** The huge gap between min (0.44) and max (22638.48) with a mean of ~230 indicates a heavily right-skewed distribution — a few large orders dominate total sales.

---

## Q14: Risk of `inferSchema=True` with Messy Dates

**Demo result:**
| raw_date | parsed_date |
|----------|-------------|
| 2024-01-15 | 2024-01-15 |
| 2024-02-20 | 2024-02-20 |
| not-a-date | **null** |
| 2024-03-01 | 2024-03-01 |

**Insight:** The bad row produces `null` silently — no exception is thrown. In a 10M-row dataset, `inferSchema=True` with mixed formats could silently corrupt thousands of records.

---

## Q15: Final Processing Pipeline — Revenue by Region

**Result:**
| Region | total_revenue | order_count | avg_order_value |
|--------|--------------|-------------|----------------|
| West | ~725,457.82 | ~3,203 | ~226.50 |
| East | ~678,781.24 | ~2,848 | ~238.33 |
| Central | ~501,239.89 | ~2,323 | ~215.74 |
| South | ~391,721.91 | ~1,620 | ~241.80 |

**Insight:** The West generates the most absolute revenue, but the South has the highest average order value — suggesting fewer but higher-value transactions, worth investigating for premium product opportunities.

---

## Key Takeaways

1. **Spark beats MapReduce** for iterative workloads (ML) and interactive analytics through in-memory DAG execution.
2. **View immutability** makes pipelines explicit, traceable, and fault-tolerant.
3. **Null handling before aggregation** is critical — silent skipping can inflate/deflate metrics by 20–30%.
4. **Shuffle (wide transformations)** are the primary Spark performance bottleneck — filter early to minimise data movement.
5. **Always define explicit schemas** for production data ingestion — `inferSchema=True` is a convenience, not a guarantee.
