# Assignment Summary — Delta Lake Incremental Processing

## Objective
Perform incremental data processing using Delta Lake: load a customer dataset into a Delta table, clean it, simulate an incremental batch of new/changed data, and apply `MERGE` to update existing records and insert new ones — demonstrating both SCD Type 1 (overwrite) and SCD Type 2 (history-preserving) update strategies.

## Approach
The assignment was implemented with [`deltalake`](https://delta-io.github.io/delta-rs/) (the delta-rs Python package) instead of PySpark + `delta-spark`, since it provides the same Delta Lake transaction log and `MERGE` semantics without requiring a JVM/Spark cluster.

Two datasets were used, both derived from the Superstore sales dataset's unique customers:
- **`customer_master.csv`** — 151 rows, with a couple of missing `segment`/`city` values and one duplicate row intentionally left in.
- **`customer_incremental.csv`** — 15 rows simulating a new batch: 10 existing customers with a changed `segment` and/or `city`, plus 5 brand-new customers.

## What was done
1. **Load** — `customer_master.csv` written into a Delta table at `delta/customer_table`.
2. **Clean** — identified 1 null in `segment`, 1 null in `city`, and 1 duplicate `customer_id` row; filled nulls with `"Unknown"` and dropped the duplicate. 151 → 150 rows.
3. **Incremental batch** — loaded the 15-row incremental CSV representing the next data drop.
4. **SCD1 MERGE** — matched rows overwritten in place, unmatched rows inserted. Result: 155 rows, no history retained.
5. **SCD2 MERGE** — a second table (`customer_table_scd2`) tracks `effective_start_date`, `effective_end_date`, `is_current`. Changed rows were expired (`is_current = 0`) and a new current row inserted; new customers inserted as current. Result: 165 total rows (155 current + 10 expired historical versions).
6. **Validation** — row counts and duplicate checks confirmed both tables matched expectations exactly.
7. **Final output** — both final tables displayed and screenshotted.

## Results
| Metric | Value |
|---|---|
| Master rows (raw) | 151 |
| Master rows (cleaned) | 150 |
| Incremental batch rows | 15 (10 updates + 5 inserts) |
| SCD1 final row count | 155 |
| SCD1 duplicate customer_ids | 0 |
| SCD2 final row count (current + history) | 165 |
| SCD2 current rows | 155 |
| SCD2 history rows | 10 |
| SCD2 duplicate customer_ids among current rows | 0 |

## SCD1 vs SCD2 — key takeaway
**SCD1** is simpler and cheaper — it just overwrites, so it's the right call when only the current state matters. **SCD2** keeps a full audit trail by expiring old rows instead of overwriting them, at the cost of more storage and a two-step merge (expire, then insert) — necessary whenever you need to answer "what did this record look like before the change?"

## Issue encountered and resolved
`deltalake` 1.6.0 has a bug computing MERGE statistics on boolean columns (`Schema error: No such field: minValues`). Worked around by storing `is_current` as an integer flag (`1`/`0`) instead of a boolean — documented inline in the notebook.

## Screenshots
See `../screenshots/` — one image per pipeline stage (`data_loading`, `data_cleaning`, `scd1`, `scd2`, `validation`, `final_output`), each captured directly from the executed notebook.
