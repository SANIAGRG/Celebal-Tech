"""
PART 3: SQL ANALYSIS
Loads cleaned CSVs into SQLite (ecommerce.db) and runs all analytical queries.
"""
import sqlite3
import pandas as pd

DB_NAME = "ecommerce.db"
DATASET_DIR = "dataset"


def load_data(conn):
    orders = pd.read_csv(f"{DATASET_DIR}/orders_cleaned.csv")
    products = pd.read_csv(f"{DATASET_DIR}/products_cleaned.csv")
    customers = pd.read_csv(f"{DATASET_DIR}/customers_cleaned.csv")
    order_items = pd.read_csv(f"{DATASET_DIR}/order_items_cleaned.csv")

    orders.to_sql("orders", conn, if_exists="replace", index=False)
    products.to_sql("products", conn, if_exists="replace", index=False)
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    order_items.to_sql("order_items", conn, if_exists="replace", index=False)
    conn.commit()


def run_query(conn, title, sql, params=None):
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)
    try:
        df = pd.read_sql_query(sql, conn, params=params)
        if df.empty:
            print("(no rows)")
        else:
            print(df.to_string(index=False))
    except Exception as e:
        print(f"ERROR running query: {e}")


def main():
    print("=" * 70)
    print("PART 3: SQL ANALYSIS")
    print("=" * 70)

    conn = sqlite3.connect(DB_NAME)
    load_data(conn)

    revenue_expr = "oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)"

    # 1. Total revenue per category
    run_query(
        conn,
        "1. Total revenue per category",
        f"""
        SELECT p.category, ROUND(SUM({revenue_expr}), 2) AS total_revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
        """,
    )

    # 2. Top 10 customers by total order value
    run_query(
        conn,
        "2. Top 10 customers by total order value",
        f"""
        SELECT o.customer_id, ROUND(SUM({revenue_expr}), 2) AS total_order_value
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.customer_id != 'UNKNOWN'
        GROUP BY o.customer_id
        ORDER BY total_order_value DESC
        LIMIT 10;
        """,
    )

    # 3. Month-wise order count for last 12 months
    run_query(
        conn,
        "3. Month-wise order count for last 12 months",
        """
        SELECT strftime('%Y-%m', order_date) AS month, COUNT(*) AS order_count
        FROM orders
        WHERE order_date >= date('now', '-12 months')
        GROUP BY month
        ORDER BY month;
        """,
    )

    # 4. Customers who placed orders but never had any DELIVERED item
    run_query(
        conn,
        "4. Customers who placed orders but never had a DELIVERED order",
        """
        SELECT DISTINCT customer_id
        FROM orders
        WHERE customer_id != 'UNKNOWN'
          AND customer_id NOT IN (
              SELECT customer_id FROM orders WHERE status = 'DELIVERED'
          );
        """,
    )

    # 5. Products with more returns (negative quantity) than purchases
    run_query(
        conn,
        "5. Products with more returns than purchases",
        """
        SELECT product_id,
               SUM(CASE WHEN quantity < 0 THEN -quantity ELSE 0 END) AS total_returns,
               SUM(CASE WHEN quantity > 0 THEN quantity ELSE 0 END) AS total_purchases
        FROM order_items
        GROUP BY product_id
        HAVING total_returns > total_purchases
        ORDER BY total_returns DESC;
        """,
    )

    # 6. Return rate per category
    run_query(
        conn,
        "6. Return rate per category",
        """
        SELECT p.category,
               ROUND(
                   SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) * 1.0
                   / SUM(ABS(oi.quantity)), 4
               ) AS return_rate
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY return_rate DESC;
        """,
    )

    # 7. Running total of revenue per region ordered by date
    run_query(
        conn,
        "7. Running total of revenue per region ordered by date",
        f"""
        WITH daily AS (
            SELECT o.region_code,
                   date(o.order_date) AS order_date,
                   SUM({revenue_expr}) AS daily_revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY o.region_code, date(o.order_date)
        )
        SELECT region_code, order_date, ROUND(daily_revenue, 2) AS daily_revenue,
               ROUND(SUM(daily_revenue) OVER (
                   PARTITION BY region_code ORDER BY order_date
               ), 2) AS running_total
        FROM daily
        ORDER BY region_code, order_date;
        """,
    )

    # 8. DENSE_RANK products by total revenue within each category
    run_query(
        conn,
        "8. DENSE_RANK of products by total revenue within category",
        f"""
        WITH prod_rev AS (
            SELECT p.category, p.product_name,
                   SUM({revenue_expr}) AS total_revenue
            FROM order_items oi
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY p.category, p.product_id, p.product_name
        )
        SELECT category, product_name, ROUND(total_revenue, 2) AS total_revenue,
               DENSE_RANK() OVER (
                   PARTITION BY category ORDER BY total_revenue DESC
               ) AS rank_in_category
        FROM prod_rev
        ORDER BY category, rank_in_category
        LIMIT 50;
        """,
    )

    # 9. LAG analysis: days between consecutive orders per customer
    run_query(
        conn,
        "9. LAG analysis - days gap between consecutive orders (At Risk if avg gap > 30)",
        """
        WITH gaps AS (
            SELECT customer_id,
                   order_date,
                   LAG(order_date) OVER (
                       PARTITION BY customer_id ORDER BY order_date
                   ) AS previous_order_date
            FROM orders
            WHERE customer_id != 'UNKNOWN'
        ),
        gaps_calc AS (
            SELECT customer_id, order_date, previous_order_date,
                   CASE WHEN previous_order_date IS NOT NULL
                        THEN julianday(order_date) - julianday(previous_order_date)
                        ELSE NULL END AS days_gap
            FROM gaps
        ),
        cust_avg AS (
            SELECT customer_id, AVG(days_gap) AS avg_gap
            FROM gaps_calc
            WHERE days_gap IS NOT NULL
            GROUP BY customer_id
        )
        SELECT g.customer_id, g.order_date, g.previous_order_date,
               ROUND(g.days_gap, 2) AS days_gap,
               CASE WHEN ca.avg_gap > 30 THEN 'At Risk' ELSE 'OK' END AS risk_flag
        FROM gaps_calc g
        LEFT JOIN cust_avg ca ON ca.customer_id = g.customer_id
        ORDER BY g.customer_id, g.order_date
        LIMIT 60;
        """,
    )

    # 10. Multi-level CTE: monthly revenue per customer -> category -> count
    run_query(
        conn,
        "10. Monthly revenue per customer categorized High/Medium/Low (counts per month)",
        f"""
        WITH monthly_rev AS (
            SELECT o.customer_id,
                   strftime('%Y-%m', o.order_date) AS month,
                   SUM({revenue_expr}) AS monthly_revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.customer_id != 'UNKNOWN'
            GROUP BY o.customer_id, month
        ),
        categorized AS (
            SELECT month, customer_id, monthly_revenue,
                   CASE WHEN monthly_revenue > 10000 THEN 'High'
                        WHEN monthly_revenue >= 5000 THEN 'Medium'
                        ELSE 'Low' END AS revenue_category
            FROM monthly_rev
        )
        SELECT month, revenue_category, COUNT(*) AS customer_count
        FROM categorized
        GROUP BY month, revenue_category
        ORDER BY month, revenue_category;
        """,
    )

    # 11. NTILE(4) quartiles by lifetime value
    run_query(
        conn,
        "11. Customer quartiles by lifetime value (Platinum/Gold/Silver/Bronze)",
        f"""
        WITH ltv AS (
            SELECT o.customer_id, SUM({revenue_expr}) AS lifetime_value
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.customer_id != 'UNKNOWN'
            GROUP BY o.customer_id
        ),
        quart AS (
            SELECT customer_id, lifetime_value,
                   NTILE(4) OVER (ORDER BY lifetime_value DESC) AS quartile
            FROM ltv
        )
        SELECT customer_id, ROUND(lifetime_value, 2) AS lifetime_value,
               CASE quartile WHEN 1 THEN 'Platinum'
                              WHEN 2 THEN 'Gold'
                              WHEN 3 THEN 'Silver'
                              ELSE 'Bronze' END AS tier
        FROM quart
        ORDER BY lifetime_value DESC
        LIMIT 30;
        """,
    )

    # 12. Year-over-Year comparison
    run_query(
        conn,
        "12. Year-over-Year revenue comparison by month",
        f"""
        WITH monthly AS (
            SELECT CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
                   CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
                   SUM({revenue_expr}) AS revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY year, month
        )
        SELECT m.year, m.month, ROUND(m.revenue, 2) AS revenue,
               ROUND(p.revenue, 2) AS prev_year_revenue,
               CASE WHEN p.revenue IS NULL OR p.revenue = 0 THEN NULL
                    ELSE ROUND((m.revenue - p.revenue) * 100.0 / p.revenue, 2)
               END AS yoy_growth_percent
        FROM monthly m
        LEFT JOIN monthly p ON p.year = m.year - 1 AND p.month = m.month
        ORDER BY m.year, m.month;
        """,
    )

    # 13. FIRST_VALUE / LAST_VALUE category shift per customer
    run_query(
        conn,
        "13. First vs most recent purchased category per customer (category_shift)",
        """
        WITH cust_cat AS (
            SELECT o.customer_id, o.order_date, p.category,
                   FIRST_VALUE(p.category) OVER (
                       PARTITION BY o.customer_id ORDER BY o.order_date
                   ) AS first_category,
                   LAST_VALUE(p.category) OVER (
                       PARTITION BY o.customer_id ORDER BY o.order_date
                       RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                   ) AS last_category
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            JOIN products p ON p.product_id = oi.product_id
            WHERE o.customer_id != 'UNKNOWN'
        )
        SELECT DISTINCT customer_id, first_category, last_category,
               CASE WHEN first_category != last_category THEN 'Yes' ELSE 'No' END AS category_shift
        FROM cust_cat
        ORDER BY customer_id
        LIMIT 30;
        """,
    )

    # 14. Cumulative distribution of revenue per customer
    run_query(
        conn,
        "14. Cumulative revenue distribution per customer",
        f"""
        WITH cust_rev AS (
            SELECT o.customer_id, SUM({revenue_expr}) AS revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            WHERE o.customer_id != 'UNKNOWN'
            GROUP BY o.customer_id
        ),
        total AS (
            SELECT SUM(revenue) AS grand_total FROM cust_rev
        )
        SELECT customer_id, ROUND(revenue, 2) AS revenue,
               ROUND(SUM(revenue) OVER (ORDER BY revenue DESC), 2) AS cumulative_revenue,
               ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) * 100.0 / (SELECT grand_total FROM total), 2) AS cumulative_percent
        FROM cust_rev
        ORDER BY revenue DESC
        LIMIT 30;
        """,
    )

    # 15. Cohort analysis
    run_query(
        conn,
        "15. Cohort analysis - retention by registration month cohort",
        """
        WITH cohorts AS (
            SELECT customer_id, strftime('%Y-%m', registration_date) AS cohort_month
            FROM customers
        ),
        cust_orders AS (
            SELECT o.customer_id, c.cohort_month, strftime('%Y-%m', o.order_date) AS order_month
            FROM orders o
            JOIN cohorts c ON c.customer_id = o.customer_id
            WHERE o.customer_id != 'UNKNOWN'
        ),
        month_diff AS (
            SELECT customer_id, cohort_month, order_month,
                   (CAST(strftime('%Y', order_month || '-01') AS INTEGER) -
                    CAST(strftime('%Y', cohort_month || '-01') AS INTEGER)) * 12 +
                   (CAST(strftime('%m', order_month || '-01') AS INTEGER) -
                    CAST(strftime('%m', cohort_month || '-01') AS INTEGER)) AS month_index
            FROM cust_orders
        ),
        cohort_size AS (
            SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
            FROM cohorts
            GROUP BY cohort_month
        ),
        active_in_month AS (
            SELECT cohort_month, month_index, COUNT(DISTINCT customer_id) AS active_customers
            FROM month_diff
            WHERE month_index BETWEEN 0 AND 3
            GROUP BY cohort_month, month_index
        )
        SELECT a.cohort_month, a.month_index, a.active_customers, cs.cohort_customers,
               ROUND(a.active_customers * 100.0 / cs.cohort_customers, 2) AS retention_rate_pct
        FROM active_in_month a
        JOIN cohort_size cs ON cs.cohort_month = a.cohort_month
        ORDER BY a.cohort_month, a.month_index
        LIMIT 60;
        """,
    )

    # 16. Self-join: products frequently bought together
    run_query(
        conn,
        "16. Products frequently bought together (top 20 pairs)",
        """
        SELECT a.product_id AS product_a, b.product_id AS product_b,
               COUNT(*) AS times_bought_together
        FROM order_items a
        JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
        GROUP BY a.product_id, b.product_id
        ORDER BY times_bought_together DESC
        LIMIT 20;
        """,
    )

    conn.close()
    print("\n" + "=" * 70)
    print("Analysis complete. Database saved as ecommerce.db")
    print("=" * 70)


if __name__ == "__main__":
    main()
