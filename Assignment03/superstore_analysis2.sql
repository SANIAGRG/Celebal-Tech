
-- STEP 1: Load CSV into superstore_raw

CREATE OR REPLACE TABLE superstore_raw AS
SELECT * FROM read_csv_auto(
    'C:/Users/Asus/OneDrive/Celebal tech/Assignment03/dataset/superstore_utf8.csv',
    header = true
);

SELECT 'superstore_raw loaded - row count:' AS info, COUNT(*) AS total_rows FROM superstore_raw;


-- STEP 2: Create normalized tables

CREATE OR REPLACE TABLE customers AS
SELECT DISTINCT
    "Customer ID"   AS customer_id,
    "Customer Name" AS customer_name,
    "Segment"       AS segment
FROM superstore_raw;

CREATE OR REPLACE TABLE products AS
SELECT DISTINCT
    "Product ID"   AS product_id,
    "Product Name" AS product_name,
    "Category"     AS category,
    "Sub-Category" AS sub_category
FROM superstore_raw;

CREATE OR REPLACE TABLE orders AS
SELECT
    CAST("Row ID"       AS INTEGER) AS row_id,
    "Order ID"                      AS order_id,
    "Order Date"                    AS order_date,
    "Ship Date"                     AS ship_date,
    "Ship Mode"                     AS ship_mode,
    "Customer ID"                   AS customer_id,
    "Product ID"                    AS product_id,
    CAST("Sales"    AS DOUBLE)      AS sales,
    CAST("Quantity" AS INTEGER)     AS quantity,
    CAST("Discount" AS DOUBLE)      AS discount,
    CAST("Profit"   AS DOUBLE)      AS profit,
    "City"                          AS city,
    "State"                         AS state,
    "Region"                        AS region
FROM superstore_raw;

SELECT 'customers table rows:' AS info, COUNT(*) AS cnt FROM customers;
SELECT 'products table rows:'  AS info, COUNT(*) AS cnt FROM products;
SELECT 'orders table rows:'    AS info, COUNT(*) AS cnt FROM orders;


-- SECTION 1: SUBQUERIES

-- Query 1: Customers whose total sales exceed the overall average customer sales
SELECT
    c.customer_name,
    ROUND(SUM(o.sales), 2) AS total_sales
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
HAVING SUM(o.sales) > (
    SELECT AVG(cust_total)
    FROM (
        SELECT SUM(sales) AS cust_total
        FROM orders
        GROUP BY customer_id
    ) sub
)
ORDER BY total_sales DESC;

-- Query 2: Single highest-value order line per customer (correlated subquery)
SELECT
    c.customer_name,
    o.order_id,
    o.product_id,
    ROUND(o.sales, 2) AS max_sale_in_order
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.sales = (
    SELECT MAX(o2.sales)
    FROM orders o2
    WHERE o2.customer_id = o.customer_id
)
ORDER BY max_sale_in_order DESC
LIMIT 20;


-- SECTION 2: CTEs

-- Query 3: Total sales and order count per customer
WITH customer_sales AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.segment,
        SUM(o.sales)              AS total_sales,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(o.profit), 2)   AS total_profit
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name, c.segment
)
SELECT
    customer_name,
    segment,
    ROUND(total_sales, 2) AS total_sales,
    total_orders,
    total_profit
FROM customer_sales
ORDER BY total_sales DESC;

-- Query 4: Customers who placed only a single order
WITH order_counts AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT
    c.customer_name,
    c.segment,
    oc.order_count
FROM customers c
JOIN order_counts oc ON c.customer_id = oc.customer_id
WHERE oc.order_count = 1
ORDER BY c.customer_name;


-- SECTION 3: WINDOW FUNCTIONS

-- Query 5: ROW_NUMBER — top 5 orders by sales within each region
SELECT *
FROM (
    SELECT
        o.region,
        c.customer_name,
        o.order_id,
        ROUND(o.sales, 2)                                              AS sales,
        ROW_NUMBER() OVER (PARTITION BY o.region ORDER BY o.sales DESC) AS row_num
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
) ranked
WHERE row_num <= 5
ORDER BY region, row_num;

-- Query 6: RANK — customers ranked by total sales (with ties handled)
WITH customer_sales AS (
    SELECT
        c.customer_name,
        c.segment,
        ROUND(SUM(o.sales), 2) AS total_sales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name, c.segment
)
SELECT
    RANK()       OVER (ORDER BY total_sales DESC) AS sales_rank,
    DENSE_RANK() OVER (ORDER BY total_sales DESC) AS dense_rank,
    customer_name,
    segment,
    total_sales
FROM customer_sales
ORDER BY sales_rank
LIMIT 20;

-- Query 7: Running total of sales per customer ordered by order date
WITH ordered_sales AS (
    SELECT
        c.customer_name,
        o.order_date,
        o.order_id,
        ROUND(o.sales, 2) AS sale_amount
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
)
SELECT
    customer_name,
    order_date,
    order_id,
    sale_amount,
    ROUND(SUM(sale_amount) OVER (
        PARTITION BY customer_name
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM ordered_sales
ORDER BY customer_name, order_date
LIMIT 30;


-- SECTION 4: BUSINESS QUERIES

-- Query 8: Top 10 customers by total sales
WITH customer_summary AS (
    SELECT
        c.customer_name,
        c.segment,
        ROUND(SUM(o.sales), 2)  AS total_sales,
        ROUND(SUM(o.profit), 2) AS total_profit,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name, c.segment
)
SELECT customer_name, segment, total_sales, total_profit, total_orders
FROM customer_summary
ORDER BY total_sales DESC
LIMIT 10;

-- Query 9: Bottom 10 customers by total sales
WITH customer_summary AS (
    SELECT
        c.customer_name,
        c.segment,
        ROUND(SUM(o.sales), 2) AS total_sales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name, c.segment
)
SELECT customer_name, segment, total_sales
FROM customer_summary
ORDER BY total_sales ASC
LIMIT 10;

-- Query 10: Customers with above-average total sales (CTE + subquery combo)
WITH customer_sales AS (
    SELECT
        c.customer_name,
        c.segment,
        ROUND(SUM(o.sales), 2) AS total_sales
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name, c.segment
),
avg_sales AS (
    SELECT ROUND(AVG(total_sales), 2) AS avg_total FROM customer_sales
)
SELECT
    cs.customer_name,
    cs.segment,
    cs.total_sales,
    av.avg_total AS average_across_all_customers
FROM customer_sales cs
CROSS JOIN avg_sales av
WHERE cs.total_sales > av.avg_total
ORDER BY cs.total_sales DESC;

-- Query 11: Sales performance by category and region
SELECT
    o.region,
    p.category,
    ROUND(SUM(o.sales), 2)           AS total_sales,
    ROUND(SUM(o.profit), 2)          AS total_profit,
    ROUND(AVG(o.discount) * 100, 1)  AS avg_discount_pct,
    COUNT(DISTINCT o.order_id)        AS num_orders
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY o.region, p.category
ORDER BY o.region, total_sales DESC;


-- FINAL QUERY: Customer Name + Total Sales + Rank
-- (JOIN + CTE + Window Functions combined)

WITH customer_sales AS (
    -- Aggregate total sales and supporting metrics per customer
    SELECT
        c.customer_name,
        c.segment,
        ROUND(SUM(o.sales), 2)         AS total_sales,
        COUNT(DISTINCT o.order_id)      AS total_orders,
        ROUND(SUM(o.profit), 2)         AS total_profit,
        ROUND(AVG(o.discount) * 100, 1) AS avg_discount_pct
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name, c.segment
),
ranked_customers AS (
    -- Apply RANK and DENSE_RANK window functions over total_sales
    SELECT
        customer_name,
        segment,
        total_sales,
        total_orders,
        total_profit,
        avg_discount_pct,
        RANK()        OVER (ORDER BY total_sales DESC) AS rank,
        DENSE_RANK()  OVER (ORDER BY total_sales DESC) AS dense_rank,
        NTILE(4)      OVER (ORDER BY total_sales DESC) AS sales_quartile
    FROM customer_sales
)
SELECT
    rank,
    dense_rank,
    customer_name,
    segment,
    total_sales,
    total_orders,
    total_profit,
    avg_discount_pct,
    CASE sales_quartile
        WHEN 1 THEN 'Top 25%'
        WHEN 2 THEN 'Upper-Mid 25%'
        WHEN 3 THEN 'Lower-Mid 25%'
        WHEN 4 THEN 'Bottom 25%'
    END AS sales_tier
FROM ranked_customers
ORDER BY rank;
