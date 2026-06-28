"""
PART 4: CLI REPORTING TOOL
Uses only sqlite3 (no pandas, no other external libs).
Prompts for report_type, start_date, end_date and prints a formatted report.
"""
import sqlite3
import sys
from datetime import datetime, timedelta

DB_NAME = "ecommerce.db"
REVENUE_EXPR = "oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)"


def parse_date(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d")


def get_period_stats(conn, start_date, end_date):
    cur = conn.cursor()

    cur.execute(
        f"""
        SELECT COUNT(DISTINCT o.order_id), COALESCE(SUM({REVENUE_EXPR}), 0),
               COUNT(DISTINCT o.customer_id)
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        """,
        (start_date, end_date),
    )
    total_orders, total_revenue, unique_customers = cur.fetchone()
    total_revenue = total_revenue or 0.0

    cur.execute(
        f"""
        SELECT p.product_name, SUM({REVENUE_EXPR}) AS revenue
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 3
        """,
        (start_date, end_date),
    )
    top_products = cur.fetchall()

    return total_orders, total_revenue, unique_customers, top_products


def main():
    print("=" * 60)
    print("PART 4: CLI ORDER ANALYTICS REPORT")
    print("=" * 60)

    try:
        report_type = input("Enter report_type (daily/weekly/monthly): ").strip().lower()
        if report_type not in ("daily", "weekly", "monthly"):
            print(f"WARNING: unrecognized report_type '{report_type}', defaulting to 'daily'")
            report_type = "daily"

        start_raw = input("Enter start_date (YYYY-MM-DD): ").strip()
        end_raw = input("Enter end_date (YYYY-MM-DD): ").strip()

        start_dt = parse_date(start_raw)
        end_dt = parse_date(end_raw)
    except ValueError as e:
        print(f"ERROR: invalid date input - {e}")
        sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        sys.exit(0)

    if start_dt > end_dt:
        print("ERROR: start_date must be on or before end_date")
        sys.exit(1)

    period_days = (end_dt - start_dt).days + 1
    prev_end_dt = start_dt - timedelta(days=1)
    prev_start_dt = prev_end_dt - timedelta(days=period_days - 1)

    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")
    prev_start_date = prev_start_dt.strftime("%Y-%m-%d")
    prev_end_date = prev_end_dt.strftime("%Y-%m-%d")

    try:
        conn = sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"ERROR: could not connect to database '{DB_NAME}' - {e}")
        sys.exit(1)

    try:
        total_orders, total_revenue, unique_customers, top_products = get_period_stats(
            conn, start_date, end_date
        )
        prev_orders, prev_revenue, prev_customers, _ = get_period_stats(
            conn, prev_start_date, prev_end_date
        )
    except sqlite3.Error as e:
        print(f"ERROR querying database: {e}")
        conn.close()
        sys.exit(1)

    if prev_revenue and prev_revenue != 0:
        pct_change = (total_revenue - prev_revenue) * 100.0 / prev_revenue
        pct_change_str = f"{pct_change:+.2f}%"
    else:
        pct_change_str = "N/A (no revenue in previous period)"

    print("\n" + "=" * 60)
    print(f"REPORT TYPE   : {report_type.upper()}")
    print(f"PERIOD        : {start_date} to {end_date} ({period_days} day(s))")
    print(f"PREVIOUS PERIOD: {prev_start_date} to {prev_end_date}")
    print("=" * 60)
    print(f"Total Orders        : {total_orders}")
    print(f"Total Revenue       : {total_revenue:,.2f}")
    print(f"Unique Customers    : {unique_customers}")
    print(f"Revenue % vs Prev   : {pct_change_str}")
    print("-" * 60)
    print("Top 3 Products by Revenue:")
    if top_products:
        for rank, (name, revenue) in enumerate(top_products, start=1):
            print(f"  {rank}. {name:<40} {revenue:,.2f}")
    else:
        print("  (no products found in this date range)")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    main()
