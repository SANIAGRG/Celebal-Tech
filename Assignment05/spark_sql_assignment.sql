-- =============================================================
-- Assignment 5: Spark Fundamentals — Spark SQL
-- Week 5 | Celebal Technologies
-- Dataset: superstore_utf8.csv
-- Run with: spark-sql -f spark_sql_assignment.sql
--           or paste into a spark-sql / Databricks SQL session
-- =============================================================


-- ---------------------------------------------------------------
-- SETUP: Load dataset and register as a queryable temp view
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW superstore
USING csv
OPTIONS (
    path        'dataset/superstore_utf8.csv',
    header      'true',
    inferSchema 'true'
);

SELECT COUNT(*) AS total_rows FROM superstore;
DESCRIBE superstore;
SELECT * FROM superstore LIMIT 5;


-- ---------------------------------------------------------------
-- Q1: Key Limitations of MapReduce vs Spark
--
-- MapReduce writes intermediate results to HDFS after every Map
-- and Reduce step, has no in-memory iteration, a rigid two-step
-- model, and high per-job latency. Spark resolves all of these
-- with an in-memory DAG execution model.
--
-- EXPLAIN shows the physical plan with no intermediate HDFS
-- writes between stages.
-- ---------------------------------------------------------------
EXPLAIN
SELECT Region, ROUND(AVG(Sales), 2) AS avg_sales
FROM   superstore
WHERE  Sales > 100
GROUP  BY Region;

SELECT Region, ROUND(AVG(Sales), 2) AS avg_sales
FROM   superstore
WHERE  Sales > 100
GROUP  BY Region;


-- ---------------------------------------------------------------
-- Q2: In-Memory Computing for Iterative ML
--
-- CACHE TABLE pins a derived table in RAM after the first scan.
-- All subsequent queries read from memory, not disk — equivalent
-- to Spark's .cache() / .persist() and the core reason Spark
-- outperforms MapReduce on iterative ML workloads (10–100×).
-- ---------------------------------------------------------------
CACHE TABLE cached_subset AS
SELECT Sales, Profit, Quantity FROM superstore;

SELECT ROUND(AVG(Sales),  2) AS avg_sales   FROM cached_subset;
SELECT ROUND(AVG(Profit), 2) AS avg_profit  FROM cached_subset;
SELECT SUM(Quantity)          AS total_qty   FROM cached_subset;

UNCACHE TABLE cached_subset;


-- ---------------------------------------------------------------
-- Q3: Remove Duplicates on Specific Columns
--     (user_id, transaction_date)
--
-- ROW_NUMBER() OVER (PARTITION BY ...) assigns rank 1 to the
-- first occurrence within each group. Filtering WHERE rn = 1
-- keeps only that row — equivalent to .dropDuplicates(subset).
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW transactions AS
SELECT * FROM VALUES
    (1, '2024-01-01', 100.0),
    (1, '2024-01-01', 100.0),
    (1, '2024-01-01', 150.0),
    (2, '2024-01-02', 200.0),
    (1, '2024-01-03', 300.0)
AS t(user_id, transaction_date, amount);

SELECT COUNT(*) AS before_dedup FROM transactions;

SELECT user_id, transaction_date, amount
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY user_id, transaction_date
               ORDER BY amount
           ) AS rn
    FROM transactions
)
WHERE rn = 1;

-- Applied to Superstore: deduplicate by Order ID + Order Date
SELECT COUNT(*) AS before_dedup FROM superstore;

SELECT COUNT(*) AS after_dedup
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY `Order ID`, `Order Date`
               ORDER BY Sales
           ) AS rn
    FROM superstore
)
WHERE rn = 1;


-- ---------------------------------------------------------------
-- Q4: Filter Region = 'West', GroupBy Category, Avg Sales
--
-- WHERE filters before the GROUP BY shuffle, so only West rows
-- are redistributed across executors — matching Spark's
-- predicate pushdown behaviour.
-- ---------------------------------------------------------------
SELECT   Category, ROUND(AVG(Sales), 2) AS avg_sale_amount
FROM     superstore
WHERE    Region = 'West'
GROUP BY Category
ORDER BY Category;


-- ---------------------------------------------------------------
-- Q5: WHERE IS NOT NULL vs COALESCE
--
--   WHERE col IS NOT NULL  → removes null rows  (.na.drop())
--   COALESCE(col, default) → replaces nulls     (.na.fill())
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW users AS
SELECT * FROM VALUES
    ('Alice', 'Active'),
    ('Bob',   CAST(NULL AS STRING)),
    ('Carol', 'Inactive'),
    ('Dave',  CAST(NULL AS STRING))
AS t(username, status);

SELECT * FROM users;

-- Drop nulls
SELECT * FROM users WHERE status IS NOT NULL;

-- Fill nulls
SELECT username, COALESCE(status, 'Unknown') AS status FROM users;


-- ---------------------------------------------------------------
-- Q6: Total Records per City — Only Cities with Count > 100
--
-- HAVING is the SQL equivalent of filtering on an aggregated
-- column. It runs after GROUP BY, unlike WHERE which runs before.
-- ---------------------------------------------------------------
SELECT   City, COUNT(*) AS record_count
FROM     superstore
GROUP BY City
HAVING   COUNT(*) > 100
ORDER BY record_count DESC;


-- ---------------------------------------------------------------
-- Q7: Immutability of Spark SQL Views
--
-- Every SELECT produces a new result set — the source view is
-- never mutated. Creating a derived view leaves the original
-- unchanged, preserving full lineage (Spark can recompute any
-- view from its definition).
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW superstore_subset AS
SELECT `Order ID`, Sales, Discount FROM superstore;

SHOW COLUMNS IN superstore_subset;

CREATE OR REPLACE TEMP VIEW superstore_no_discount AS
SELECT `Order ID`, Sales FROM superstore;

-- superstore_subset still has Discount — original is unchanged
SHOW COLUMNS IN superstore_subset;
SHOW COLUMNS IN superstore_no_discount;


-- ---------------------------------------------------------------
-- Q8: Filter Age Between 18 and 30 AND Subscription = 'Premium'
--
-- BETWEEN is inclusive. Multiple conditions use AND / OR with
-- well-defined SQL precedence — no parenthesis pitfalls.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW subscribers AS
SELECT * FROM VALUES
    (1, 'Alice',  25, 'Premium'),
    (2, 'Bob',    17, 'Basic'),
    (3, 'Carol',  30, 'Premium'),
    (4, 'Dave',   31, 'Premium'),
    (5, 'Eve',    22, 'Basic'),
    (6, 'Frank',  18, 'Premium'),
    (7, 'Grace',  28, 'Premium')
AS t(id, name, age, subscription);

SELECT * FROM subscribers
WHERE  age BETWEEN 18 AND 30
  AND  subscription = 'Premium';


-- ---------------------------------------------------------------
-- Q9: Why Handle Nulls Before Mathematical Aggregations?
--
-- AVG() silently skips nulls, shrinking the denominator and
-- inflating the result. COALESCE inside the aggregation makes
-- null intent explicit without a separate cleaning step.
--
--   avg_with_nulls = (100+200+400)/3 = 233.33  (biased)
--   avg_fill_zero  = (100+200+0+400)/4 = 175.0  (correct)
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW prices AS
SELECT * FROM VALUES
    (100.0),
    (200.0),
    (CAST(NULL AS DOUBLE)),
    (400.0)
AS t(price);

SELECT
    ROUND(AVG(price),               2) AS avg_with_nulls,
    ROUND(AVG(COALESCE(price, 0.0)), 2) AS avg_fill_zero
FROM prices;


-- ---------------------------------------------------------------
-- Q10: Cast raw_timestamp to TIMESTAMP, Rename to event_time
--
-- CAST + AS alias performs both type conversion and rename in
-- one expression — no separate rename step needed.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW events AS
SELECT * FROM VALUES
    ('2024-01-15 10:30:00'),
    ('2024-02-20 14:45:00'),
    ('2024-03-01 09:00:00')
AS t(raw_timestamp);

DESCRIBE events;

SELECT CAST(raw_timestamp AS TIMESTAMP) AS event_time
FROM   events;


-- ---------------------------------------------------------------
-- Q11: Shuffle and Wide Transformations
--
-- EXPLAIN shows 'Exchange hashpartitioning' — the shuffle stage
-- boundary where rows are redistributed across executors by
-- GROUP BY key. This is a wide transformation: each output
-- partition depends on rows from multiple input partitions.
-- ---------------------------------------------------------------
EXPLAIN
SELECT Region, COUNT(*) AS order_count
FROM   superstore
GROUP  BY Region;

SELECT Region, COUNT(*) AS order_count
FROM   superstore
GROUP  BY Region;


-- ---------------------------------------------------------------
-- Q12: Remove Rows Where Email is Null OR Username is Empty
--
-- TRIM() strips whitespace before !='' comparison, catching
-- both empty strings and whitespace-only strings in one step.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW contacts AS
SELECT * FROM VALUES
    ('alice@example.com', 'alice'),
    (CAST(NULL AS STRING), 'bob'),
    ('carol@example.com',  ''),
    ('dave@example.com',   '   '),
    ('eve@example.com',    'eve')
AS t(email, username);

SELECT COUNT(*) AS before_cleaning FROM contacts;

SELECT * FROM contacts
WHERE  email IS NOT NULL
  AND  TRIM(username) != '';


-- ---------------------------------------------------------------
-- Q13: Multiple Statistics with a Single Query
--
-- All aggregations run in one pass — more efficient than
-- issuing separate queries for each statistic.
-- ---------------------------------------------------------------
SELECT
    ROUND(MIN(Sales),  2) AS min_price,
    ROUND(MAX(Sales),  2) AS max_price,
    ROUND(AVG(Sales),  2) AS mean_price,
    ROUND(SUM(Sales),  2) AS total_sales,
    COUNT(Sales)           AS record_count
FROM superstore;


-- ---------------------------------------------------------------
-- Q14: Risk of inferSchema=True with Inconsistent Date Formats
--
-- TO_DATE silently returns NULL for unparseable values — no
-- exception is thrown. Best practice: load as STRING and cast
-- explicitly so bad rows are visible, not silently lost.
-- ---------------------------------------------------------------
CREATE OR REPLACE TEMP VIEW raw_dates AS
SELECT * FROM VALUES
    ('2024-01-15'),
    ('2024-02-20'),
    ('not-a-date'),
    ('2024-03-01')
AS t(raw_date);

SELECT raw_date,
       TO_DATE(raw_date, 'yyyy-MM-dd') AS parsed_date
FROM   raw_dates;


-- ---------------------------------------------------------------
-- Q15: Complete Data Processing Pipeline (CTE)
--
-- A production-style pipeline using Common Table Expressions:
--   1. Deduplicate on Order ID with ROW_NUMBER()
--   2. Fill null Sales with 0 using COALESCE
--   3. Aggregate revenue by Region
-- ---------------------------------------------------------------
WITH deduped AS (
    SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY `Order ID`
                   ORDER BY Sales
               ) AS rn
        FROM superstore
    )
    WHERE rn = 1
),
filled AS (
    SELECT *,
           COALESCE(Sales, 0.0) AS sales_clean
    FROM deduped
)
SELECT
    Region,
    ROUND(SUM(sales_clean), 2) AS total_revenue,
    COUNT(*)                    AS order_count,
    ROUND(AVG(sales_clean), 2) AS avg_order_value
FROM   filled
GROUP  BY Region
ORDER  BY total_revenue DESC;
