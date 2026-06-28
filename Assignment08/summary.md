# Assignment 08 — E-Commerce Order Analytics System

A complete end-to-end data pipeline combining Python data generation, pandas-based cleaning, SQL analytics (SQLite), and a CLI reporting tool — with edge case tests covering common data-quality failure modes.

## Folder Structure

```
Assignment08/
├── dataset/                       # all CSV data (raw + cleaned)
│   ├── customers.csv / customers_cleaned.csv
│   ├── products.csv / products_cleaned.csv
│   ├── orders.csv / orders_cleaned.csv
│   └── order_items.csv / order_items_cleaned.csv
├── ecommerce.db                   # SQLite DB loaded from cleaned CSVs
├── generate_data.py               # Part 1: synthetic data generation
├── clean_data.py                  # Part 2: data cleaning functions
├── analysis.py                    # Part 3: 16 SQL analytics queries
├── report_tool.py                 # Part 4: interactive CLI report
├── test_edge_cases.py             # Part 5: edge case tests
├── run_all.py                     # master pipeline runner
└── summary.md                     # this file
```

## Part 1 — Data Generation (`generate_data.py`)

Uses `faker` + `random` only. Generates 4 CSVs into `dataset/`:

| File | Rows | Notes |
|---|---|---|
| `customers.csv` | 520 | customer_type REGULAR/PREMIUM/VIP; ~2% invalid emails (missing `@` or domain dot) |
| `products.csv` | 540 | categories Electronics/Clothing/Home/Books; some names have extra spaces / inconsistent casing (intentional dirty data) |
| `orders.csv` | 600 | status PLACED/SHIPPED/DELIVERED/CANCELLED/RETURNED; ~5% wrong date format (`DD-MM-YYYY`); ~5% missing customer_id |
| `order_items.csv` | 1512 | every order_id references a valid order; discount_percent 0–100; ~3% negative quantity (returns) |

## Part 2 — Data Cleaning (`clean_data.py`)

Pandas-based cleaning functions, each returning the cleaned DataFrame plus a list of issues found:

- **`clean_orders(df)`** — detects `DD-MM-YYYY` dates and converts to `YYYY-MM-DD HH:MM:SS`; replaces null/empty `customer_id` with `"UNKNOWN"`.
- **`clean_products(df)`** — strips whitespace and applies title case to `product_name`.
- **`validate_emails(df)`** — flags emails missing `@` or missing a dot in the domain.
- **`check_referential_integrity(orders_df, order_items_df)`** — finds `order_items` rows whose `order_id` doesn't exist in `orders`.

**Verified run results:** fixed 24 bad-format dates, replaced 28 missing customer_ids, found 3 invalid emails, found 0 orphan order_items. Cleaned files saved back to `dataset/`.

## Part 3 — SQL Analysis (`analysis.py`)

Loads the 4 cleaned CSVs into `ecommerce.db` (SQLite) and runs **16 queries**, all verified to execute without errors:

**Basic**
1. Total revenue per category
2. Top 10 customers by total order value
3. Month-wise order count for the last 12 months

**Intermediate**
4. Customers who never had a DELIVERED order
5. Products with more returns than purchases
6. Return rate per category

**Advanced (window functions / CTEs)**
7. Running total of revenue per region over time
8. `DENSE_RANK` of products by revenue within category
9. `LAG`-based gap analysis between consecutive orders per customer, flagging "At Risk" customers (avg gap > 30 days)
10. Multi-level CTE: monthly revenue per customer → High/Medium/Low buckets → counts per month
11. `NTILE(4)` customer quartiles by lifetime value, labeled Platinum/Gold/Silver/Bronze
12. Year-over-year revenue comparison with `yoy_growth_percent` (NULL-safe)
13. `FIRST_VALUE`/`LAST_VALUE` category-shift detection per customer
14. Cumulative revenue distribution and cumulative percent per customer
15. Cohort analysis — retention by registration-month cohort across months 0–3
16. Self-join — products frequently bought together in the same order

## Part 4 — CLI Reporting Tool (`report_tool.py`)

Built with **only** `sqlite3` (no pandas). Interactively prompts for:
- `report_type` (daily/weekly/monthly)
- `start_date`, `end_date`

Then prints: total orders, total revenue, unique customers, top 3 products by revenue, and % change vs. the previous equivalent period (divide-by-zero handled). Verified working with sample input (monthly report for 2025).

## Part 5 — Edge Case Tests (`test_edge_cases.py`)

Plain Python test functions, each prints PASS/FAIL:

| Test | What it checks | Result |
|---|---|---|
| `test_orphan_order_items` | injected order_item with non-existent order_id is caught by `check_referential_integrity` | PASS |
| `test_discount_over_100` | discount_percent=150 is flagged and clamped so revenue isn't negative-inflated | PASS |
| `test_zero_quantity` | quantity=0 rows are excluded from both purchase and return counts | PASS |
| `test_future_order_date` | order_date 1 year in the future is detected | PASS |

## Master Runner (`run_all.py`)

Runs `generate_data.py` → `clean_data.py` → `analysis.py` → `test_edge_cases.py` in sequence and prints a pass/fail summary for each step. Verified end-to-end run: **all 4 steps passed**.

## How to Run

```bash
cd Assignment08
python run_all.py          # runs the full pipeline
python report_tool.py      # run separately (interactive CLI)
```
