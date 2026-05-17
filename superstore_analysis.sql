
-- STEP 1: LOAD DATASET INTO SQL DATABASE
CREATE OR REPLACE TABLE superstore AS
SELECT
    "Row ID"::INTEGER         AS row_id,
    "Order ID"                AS order_id,
    strptime("Order Date", '%m/%d/%Y')::DATE AS order_date,
    strptime("Ship Date",  '%m/%d/%Y')::DATE AS ship_date,
    "Ship Mode"               AS ship_mode,
    "Customer ID"             AS customer_id,
    "Customer Name"           AS customer_name,
    "Segment"                 AS segment,
    "Country"                 AS country,
    "City"                    AS city,
    "State"                   AS state,
    "Postal Code"::INTEGER    AS postal_code,
    "Region"                  AS region,
    "Product ID"              AS product_id,
    "Category"                AS category,
    "Sub-Category"            AS sub_category,
    "Product Name"            AS product_name,
    "Sales"::DOUBLE           AS sales,
    "Quantity"::INTEGER       AS quantity,
    "Discount"::DOUBLE        AS discount,
    "Profit"::DOUBLE          AS profit
FROM read_csv_auto(
    'C:/Users/Asus/OneDrive/Celebal tech/Assignment02/dataset/superstore_utf8.csv',
    header      = true,
    all_varchar = true
);


-- STEP 2: EXPLORE TABLE — SCHEMA & SAMPLE DATA

-- 2.1 Table Schema
DESCRIBE superstore;

-- 2.2 First 10 rows
SELECT * FROM superstore LIMIT 10;

-- 2.3 Total row count
SELECT COUNT(*) AS total_rows FROM superstore;

-- 2.4 High-level dataset summary
SELECT
    COUNT(*)                        AS total_rows,
    COUNT(DISTINCT order_id)        AS unique_orders,
    COUNT(DISTINCT customer_id)     AS unique_customers,
    COUNT(DISTINCT product_id)      AS unique_products,
    MIN(order_date)                 AS earliest_order,
    MAX(order_date)                 AS latest_order,
    COUNT(DISTINCT region)          AS regions,
    COUNT(DISTINCT state)           AS states,
    COUNT(DISTINCT category)        AS categories,
    COUNT(DISTINCT sub_category)    AS sub_categories
FROM superstore;


-- STEP 3: WHERE FILTERS

-- 3.1 Orders from the West region
SELECT order_id, customer_name, product_name, sales, profit, region
FROM superstore
WHERE region = 'West'
LIMIT 15;

-- 3.2 Technology category orders
SELECT order_id, customer_name, product_name, category, sales, profit
FROM superstore
WHERE category = 'Technology'
LIMIT 15;

-- 3.3 Orders placed in 2016
SELECT order_id, order_date, customer_name, sales, profit
FROM superstore
WHERE YEAR(order_date) = 2016
LIMIT 15;

-- 3.4 High-value orders (Sales > $1,000)
SELECT order_id, customer_name, product_name, sales, profit
FROM superstore
WHERE sales > 1000
ORDER BY sales DESC
LIMIT 15;

-- 3.5 Orders with high discount (>= 30%)
SELECT order_id, product_name, category, discount, sales, profit
FROM superstore
WHERE discount >= 0.30
ORDER BY discount DESC
LIMIT 15;

-- 3.6 Loss-making orders (Profit < 0)
SELECT order_id, product_name, category, sales, discount, profit
FROM superstore
WHERE profit < 0
ORDER BY profit ASC
LIMIT 15;


-- STEP 4: GROUP BY AGGREGATIONS

-- 4.1 Sales, Profit and Order Count by Region
SELECT
    region,
    COUNT(*)                                           AS total_orders,
    ROUND(SUM(sales), 2)                               AS total_sales,
    ROUND(SUM(profit), 2)                              AS total_profit,
    ROUND(AVG(sales), 2)                               AS avg_sale,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- 4.2 Sales, Quantity and Discount by Category
SELECT
    category,
    COUNT(*)                        AS total_orders,
    ROUND(SUM(sales), 2)            AS total_sales,
    SUM(quantity)                   AS total_quantity,
    ROUND(AVG(sales), 2)            AS avg_sale,
    ROUND(SUM(profit), 2)           AS total_profit,
    ROUND(AVG(discount) * 100, 2)   AS avg_discount_pct
FROM superstore
GROUP BY category
ORDER BY total_sales DESC;

-- 4.3 Sales and Profit by Sub-Category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)                                AS total_sales,
    ROUND(SUM(profit), 2)                               AS total_profit,
    SUM(quantity)                                       AS total_quantity,
    ROUND(SUM(profit) / NULLIF(SUM(sales),0) * 100, 2) AS profit_margin_pct
FROM superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC;

-- 4.4 Sales by Customer Segment
SELECT
    segment,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(sales), 2)        AS total_sales,
    ROUND(AVG(sales), 2)        AS avg_order_value,
    ROUND(SUM(profit), 2)       AS total_profit
FROM superstore
GROUP BY segment
ORDER BY total_sales DESC;

-- 4.5 Sales by Ship Mode
SELECT
    ship_mode,
    COUNT(*)                AS order_count,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(AVG(sales), 2)    AS avg_sales
FROM superstore
GROUP BY ship_mode
ORDER BY order_count DESC;


-- STEP 5: SORT & LIMIT — TOP PRODUCTS & CATEGORIES

-- 5.1 Top 10 Products by Total Sales
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit,
    SUM(quantity)           AS total_quantity
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 10;

-- 5.2 Top 10 Products by Total Profit
SELECT
    product_name,
    category,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit
FROM superstore
GROUP BY product_name, category
ORDER BY total_profit DESC
LIMIT 10;

-- 5.3 Bottom 10 Products by Profit (biggest loss-makers)
SELECT
    product_name,
    category,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit
FROM superstore
GROUP BY product_name, category
ORDER BY total_profit ASC
LIMIT 10;

-- 5.4 Top 5 Sub-Categories by Profit
SELECT
    category,
    sub_category,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC
LIMIT 5;

-- 5.5 Top 10 States by Sales
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)                AS total_sales,
    ROUND(SUM(profit), 2)               AS total_profit,
    COUNT(DISTINCT order_id)            AS unique_orders
FROM superstore
GROUP BY state, region
ORDER BY total_sales DESC
LIMIT 10;


-- STEP 6: BUSINESS USE CASES

-- 6.1 Monthly Sales and Profit Trends (all years)
SELECT
    YEAR(order_date)    AS year,
    MONTH(order_date)   AS month,
    COUNT(*)            AS total_orders,
    ROUND(SUM(sales), 2)   AS monthly_sales,
    ROUND(SUM(profit), 2)  AS monthly_profit
FROM superstore
GROUP BY year, month
ORDER BY year, month;

-- 6.2 Year-over-Year (YoY) Sales by Category
SELECT
    YEAR(order_date) AS year,
    category,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit
FROM superstore
GROUP BY year, category
ORDER BY year, category;

-- 6.3 Top 10 Customers by Total Sales
SELECT
    customer_id,
    customer_name,
    segment,
    state,
    COUNT(DISTINCT order_id)            AS total_orders,
    ROUND(SUM(sales), 2)                AS total_sales,
    ROUND(SUM(profit), 2)               AS total_profit,
    ROUND(AVG(discount) * 100, 2)       AS avg_discount_pct
FROM superstore
GROUP BY customer_id, customer_name, segment, state
ORDER BY total_sales DESC
LIMIT 10;

-- 6.4 Top 10 Customers by Profit Contribution
SELECT
    customer_id,
    customer_name,
    segment,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit
FROM superstore
GROUP BY customer_id, customer_name, segment
ORDER BY total_profit DESC
LIMIT 10;

-- 6.5 Orders containing more than one line item (multi-product orders)
SELECT
    order_id,
    COUNT(*)                    AS line_items,
    ROUND(SUM(sales), 2)        AS order_total_sales,
    COUNT(DISTINCT product_id)  AS unique_products
FROM superstore
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY line_items DESC
LIMIT 10;

-- 6.6 Discount Impact Analysis (profit by discount band)
SELECT
    CASE
        WHEN discount = 0          THEN '0 - No Discount'
        WHEN discount < 0.20       THEN '1 - Low  (0-20%)'
        WHEN discount < 0.40       THEN '2 - Medium (20-40%)'
        ELSE                            '3 - High (40%+)'
    END                         AS discount_band,
    COUNT(*)                    AS order_count,
    ROUND(SUM(sales), 2)        AS total_sales,
    ROUND(SUM(profit), 2)       AS total_profit,
    ROUND(AVG(profit), 2)       AS avg_profit_per_order
FROM superstore
GROUP BY discount_band
ORDER BY discount_band;

-- 6.7 States with Net Loss (total profit < 0)
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)    AS total_sales,
    ROUND(SUM(profit), 2)   AS total_profit
FROM superstore
GROUP BY state, region
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- 6.8 Average shipping delay by Ship Mode
SELECT
    ship_mode,
    ROUND(AVG(DATEDIFF('day', order_date, ship_date)), 1) AS avg_days_to_ship,
    MIN(DATEDIFF('day', order_date, ship_date))           AS min_days,
    MAX(DATEDIFF('day', order_date, ship_date))           AS max_days
FROM superstore
GROUP BY ship_mode
ORDER BY avg_days_to_ship;


-- STEP 7: DATA VALIDATION

-- 7.1 Row count confirmation
SELECT COUNT(*) AS total_rows FROM superstore;

-- 7.2 Null check for every column
SELECT
    SUM(CASE WHEN row_id       IS NULL THEN 1 ELSE 0 END) AS null_row_id,
    SUM(CASE WHEN order_id     IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN order_date   IS NULL THEN 1 ELSE 0 END) AS null_order_date,
    SUM(CASE WHEN ship_date    IS NULL THEN 1 ELSE 0 END) AS null_ship_date,
    SUM(CASE WHEN customer_id  IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_name,
    SUM(CASE WHEN sales        IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit       IS NULL THEN 1 ELSE 0 END) AS null_profit,
    SUM(CASE WHEN quantity     IS NULL THEN 1 ELSE 0 END) AS null_quantity,
    SUM(CASE WHEN discount     IS NULL THEN 1 ELSE 0 END) AS null_discount
FROM superstore;

-- 7.3 Statistical summary (min / max / avg)
SELECT
    ROUND(MIN(sales), 2)     AS min_sales,
    ROUND(MAX(sales), 2)     AS max_sales,
    ROUND(AVG(sales), 2)     AS avg_sales,
    ROUND(MIN(profit), 2)    AS min_profit,
    ROUND(MAX(profit), 2)    AS max_profit,
    ROUND(AVG(profit), 2)    AS avg_profit,
    ROUND(MIN(discount), 2)  AS min_discount,
    ROUND(MAX(discount), 2)  AS max_discount,
    ROUND(AVG(discount), 4)  AS avg_discount
FROM superstore;

-- 7.4 Distinct value counts per categorical column
SELECT
    COUNT(DISTINCT region)       AS distinct_regions,
    COUNT(DISTINCT category)     AS distinct_categories,
    COUNT(DISTINCT sub_category) AS distinct_subcategories,
    COUNT(DISTINCT state)        AS distinct_states,
    COUNT(DISTINCT segment)      AS distinct_segments,
    COUNT(DISTINCT ship_mode)    AS distinct_ship_modes
FROM superstore;

-- 7.5 Discount validity check (all values must be in [0, 1])
SELECT
    COUNT(*) FILTER (WHERE discount < 0)  AS invalid_negative_discount,
    COUNT(*) FILTER (WHERE discount > 1)  AS invalid_over_100_pct
FROM superstore;

-- 7.6 Negative sales check (should not exist)
SELECT COUNT(*) AS negative_sales_count
FROM superstore
WHERE sales < 0;
