# Assignment 3 — Query Results

## Step 1 — Load CSV into superstore_raw

### Query 1
```sql
CREATE OR REPLACE TABLE superstore_raw AS
SELECT * FROM read_csv_auto(
    'C:/Users/Asus/OneDrive/Celebal tech/Assignment03/dataset/superstore_utf8.csv',
    header = true
)
```

**Rows returned: 1**

| Count |
|-------|
| 9994  |

### Query 2

```sql
SELECT 'superstore_raw loaded - row count:' AS info, COUNT(*) AS total_rows FROM superstore_raw
```

**Rows returned: 1**

| info                               | total_rows |
|------------------------------------|------------|
| superstore_raw loaded - row count: | 9994       |


## Step 2 — Create Normalized Tables

### Query 3
```sql
CREATE OR REPLACE TABLE customers AS
SELECT DISTINCT
    "Customer ID"   AS customer_id,
    "Customer Name" AS customer_name,
    "Segment"       AS segment
FROM superstore_raw
```

**Rows returned: 1**

| Count |
|-------|
| 793   |

### Query 4

```sql
CREATE OR REPLACE TABLE products AS
SELECT DISTINCT
    "Product ID"   AS product_id,
    "Product Name" AS product_name,
    "Category"     AS category,
    "Sub-Category" AS sub_category
FROM superstore_raw
```

**Rows returned: 1**

| Count |
|-------|
| 1894  |

### Query 5

```sql
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
FROM superstore_raw
```

**Rows returned: 1**

| Count |
|-------|
| 9994  |

### Query 6

```sql
SELECT 'customers table rows:' AS info, COUNT(*) AS cnt FROM customers
```

**Rows returned: 1**

| info                  | cnt |
|-----------------------|-----|
| customers table rows: | 793 |

### Query 7

```sql
SELECT 'products table rows:'  AS info, COUNT(*) AS cnt FROM products
```

**Rows returned: 1**

| info                 | cnt  |
|----------------------|------|
| products table rows: | 1894 |

### Query 8

```sql
SELECT 'orders table rows:'    AS info, COUNT(*) AS cnt FROM orders
```

**Rows returned: 1**

| info               | cnt  |
|--------------------|------|
| orders table rows: | 9994 |


## Section 1 — Subqueries

### Query 9
```sql
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
ORDER BY total_sales DESC
```

**Rows returned: 294**

| customer_name        | total_sales |
|----------------------|-------------|
| Sean Miller          | 25043.05    |
| Tamara Chand         | 19052.22    |
| Raymond Buch         | 15117.34    |
| Tom Ashbrook         | 14595.62    |
| Adrian Barton        | 14473.57    |
| Ken Lonsdale         | 14175.23    |
| Sanjit Chand         | 14142.33    |
| Hunter Lopez         | 12873.3     |
| Sanjit Engle         | 12209.44    |
| Christopher Conant   | 12129.07    |
| Todd Sumrall         | 11891.75    |
| Greg Tran            | 11820.12    |
| Becky Martin         | 11789.63    |
| Seth Vernon          | 11470.95    |
| Caroline Jumper      | 11164.97    |
| Clay Ludtke          | 10880.55    |
| Maria Etezadi        | 10663.73    |
| Karen Ferguson       | 10604.27    |
| Bill Shonely         | 10501.65    |
| Edward Hooks         | 10310.88    |
| John Lee             | 9799.92     |
| Grant Thornton       | 9351.21     |
| Helen Wasserman      | 9300.25     |
| Tom Boeckenhauer     | 9133.99     |
| Peter Fuller         | 9062.86     |
| Christopher Martinez | 8954.02     |
| Justin Deggeller     | 8828.03     |
| Joe Elijah           | 8697.84     |
| Laura Armstrong      | 8673.22     |
| Pete Kriz            | 8646.93     |
| Daniel Raglin        | 8350.87     |
| Natalie Fritzler     | 8322.83     |
| Karen Daniels        | 8282.36     |
| Nick Crebassa        | 8241.74     |
| Harry Marie          | 8236.76     |
| Keith Dawkins        | 8181.26     |
| Sean Braxton         | 8057.89     |
| Zuschuss Carroll     | 8025.71     |
| Joseph Holt          | 7955.0      |
| Nora Preis           | 7903.18     |
| Anna Häberlin        | 7888.29     |
| Adam Bellavance      | 7755.62     |
| Jim Epp              | 7754.98     |
| Jane Waco            | 7721.71     |
| Lena Creighton       | 7663.13     |
| John Murray          | 7625.08     |
| Jonathan Doherty     | 7610.86     |
| Patrick O'Brill      | 7473.83     |
| Maribeth Schnelling  | 7443.69     |
| Rick Wilson          | 7397.4      |
| Brian Moss           | 7294.19     |
| Paul Prost           | 7252.61     |
| Natalie Webber       | 7234.01     |
| Dean percer          | 7198.76     |
| Fred Hopkins         | 6987.2      |
| Rick Huthwaite       | 6979.18     |
| Penelope Sewall      | 6843.63     |
| Brenda Bowman        | 6765.73     |
| Joel Eaton           | 6760.81     |
| Yana Sorensen        | 6720.44     |
| Andy Reiter          | 6608.45     |
| Dan Reichenbach      | 6528.03     |
| Grace Kelly          | 6497.27     |
| Joseph Airdo         | 6491.03     |
| Nathan Mautz         | 6459.34     |
| Valerie Dominguez    | 6442.25     |
| Sarah Brown          | 6411.0      |
| James Galang         | 6366.39     |
| Darrin Martin        | 6345.1      |
| Corinna Mitchell     | 6339.56     |
| Max Jones            | 6320.75     |
| Brosina Hoffman      | 6255.35     |
| Rob Lucas            | 6234.91     |
| William Brown        | 6160.1      |
| Victoria Wilson      | 6134.04     |
| Shirley Daniels      | 6121.11     |
| Quincy Jones         | 6108.34     |
| Alan Dominguez       | 6106.88     |
| Cassandra Brandow    | 6076.14     |
| Greg Maxwell         | 6049.97     |
| Shahid Collister     | 5992.54     |
| Kristen Hastings     | 5990.8      |
| Robert Marley        | 5979.1      |
| Keith Herrera        | 5952.86     |
| Ben Ferrer           | 5907.97     |
| Christine Phan       | 5888.28     |
| Bill Donatelli       | 5718.52     |
| Cindy Stewart        | 5690.05     |
| Anne McFarland       | 5664.02     |
| Ross Baird           | 5633.32     |
| Katherine Murray     | 5620.19     |
| Alex Avila           | 5563.56     |
| Suzanne McNair       | 5563.39     |
| Naresj Patel         | 5529.62     |
| Amy Cox              | 5527.85     |
| Mick Hernandez       | 5503.09     |
| Dennis Pardue        | 5480.72     |
| Emily Phan           | 5478.06     |
| Yoseph Carroll       | 5454.35     |
| Stefania Perrino     | 5440.32     |
| Luke Weiss           | 5420.51     |
| Cathy Prescott       | 5402.25     |
| Thomas Seio          | 5371.09     |
| Tonja Turnell        | 5364.81     |
| Mitch Webber         | 5341.9      |
| Tom Prescott         | 5329.0      |
| Tamara Willingham    | 5278.83     |
| Dianna Wilson        | 5271.63     |
| Mitch Willingham     | 5253.88     |
| Harold Ryan          | 5248.79     |
| Steven Cartwright    | 5226.21     |
| Resi Pölking         | 5153.08     |
| Lena Radford         | 5142.89     |
| Mike Pelletier       | 5087.92     |
| Anna Andreadi        | 5086.94     |
| Ivan Liston          | 5040.74     |
| Kelly Lampkin        | 5016.49     |
| Laurel Beltran       | 4985.68     |
| Dave Hallsten        | 4932.87     |
| Irene Maddox         | 4930.47     |
| Ted Trevino          | 4915.6      |
| Kunst Miller         | 4909.47     |
| Philisse Overcash    | 4893.04     |
| Heather Kirkland     | 4877.78     |
| Anthony Jacobs       | 4867.34     |
| Joe Kamberova        | 4867.2      |
| Alan Hwang           | 4805.34     |
| Dean Katz            | 4802.39     |
| Russell Applegate    | 4793.54     |
| Sue Ann Reed         | 4767.34     |
| Jim Kriz             | 4760.43     |
| Bart Watters         | 4750.36     |
| Tracy Blumstein      | 4737.49     |
| Giulietta Baptist    | 4716.29     |
| Rick Bensley         | 4715.47     |
| Erin Smith           | 4657.92     |
| Deborah Brumfield    | 4655.9      |
| Kean Thornton        | 4642.09     |
| Sample Company A     | 4624.57     |
| Eugene Moren         | 4588.44     |
| Dave Brooks          | 4531.65     |
| Anthony Rawles       | 4523.34     |
| Arthur Gainer        | 4510.8      |
| Anthony Johnson      | 4501.39     |
| Linda Cazamias       | 4492.95     |
| Stewart Carmichael   | 4492.66     |
| Theone Pippenger     | 4454.06     |
| Mark Cousins         | 4432.14     |
| Jamie Kunitz         | 4427.14     |
| Katrina Willman      | 4416.52     |
| Bradley Drucker      | 4411.24     |
| Arianne Irving       | 4375.79     |
| Scot Coram           | 4371.96     |
| Ellis Ballard        | 4358.13     |
| Gary Zandusky        | 4355.15     |
| Steven Roelle        | 4345.89     |
| Natalie DeCherney    | 4326.14     |
| Matt Abelman         | 4299.16     |
| Sung Pak             | 4282.94     |
| Dana Kaydos          | 4282.18     |
| Rick Duston          | 4272.93     |
| Toby Carlisle        | 4266.81     |
| Alan Schoenberger    | 4260.78     |
| Frank Hawley         | 4256.27     |
| Claudia Bergmann     | 4246.46     |
| Tracy Hopkins        | 4234.1      |
| Bill Eplett          | 4204.68     |
| Jill Fjeld           | 4198.33     |
| Gary Hwang           | 4172.85     |
| Roland Schwarz       | 4159.77     |
| Muhammed Yedwab      | 4152.7      |
| Peter McVee          | 4115.66     |
| Stewart Visinsky     | 4105.31     |
| Denise Monton        | 4074.47     |
| Frank Preis          | 4046.75     |
| Susan Pistek         | 3990.69     |
| Craig Molinari       | 3984.45     |
| Michael Paige        | 3983.64     |
| Sean Christensen     | 3979.06     |
| Sanjit Jacobs        | 3949.66     |
| Luke Foster          | 3930.51     |
| Pierre Wener         | 3922.41     |
| George Ashbrook      | 3919.78     |
| Ken Heidel           | 3918.97     |
| Chris Cortes         | 3913.42     |
| Dorothy Badders      | 3908.8      |
| Nora Paige           | 3908.4      |
| Kelly Collister      | 3908.26     |
| Fred Chung           | 3889.37     |
| Bill Stewart         | 3887.83     |
| John Stevenson       | 3868.02     |
| Ruben Ausman         | 3832.31     |
| Annie Thurman        | 3831.86     |
| Olvera Toch          | 3818.62     |
| Rose O'Brian         | 3815.48     |
| Michael Chen         | 3805.71     |
| Michael Moore        | 3794.08     |
| Carol Adams          | 3789.72     |
| Matthew Grinstein    | 3785.28     |
| Maribeth Dona        | 3766.38     |
| Jim Karlsson         | 3760.03     |
| Juliana Krohn        | 3747.67     |
| Frank Merwin         | 3736.2      |
| Scott Cohen          | 3729.79     |
| Hunter Glantz        | 3690.28     |
| Ben Peterman         | 3675.86     |
| Liz Preis            | 3653.4      |
| Christopher Schild   | 3651.86     |
| Ed Braxton           | 3644.98     |
| Jeremy Pistek        | 3635.59     |
| Sam Zeldin           | 3625.33     |
| Rick Hansen          | 3621.38     |
| Thomas Boland        | 3589.3      |
| Gary McGarr          | 3582.82     |
| Dionis Lloyd         | 3539.32     |
| Erica Smith          | 3510.46     |
| Robert Waldorf       | 3495.65     |
| Anna Gayman          | 3489.04     |
| Emily Ducich         | 3484.92     |
| Pauline Webber       | 3454.92     |
| Sarah Foster         | 3422.79     |
| Frank Carlisle       | 3418.74     |
| Sally Hughsby        | 3406.84     |
| Sandra Glassco       | 3406.58     |
| Trudy Schmidt        | 3368.09     |
| Sam Craven           | 3362.96     |
| Victoria Pisteka     | 3360.53     |
| Doug Jacobs          | 3356.4      |
| Dianna Vittorini     | 3341.59     |
| Sylvia Foulston      | 3336.54     |
| Dan Campbell         | 3336.17     |
| Arthur Prichep       | 3323.56     |
| Dennis Kane          | 3318.49     |
| Katharine Harms      | 3312.86     |
| Randy Ferguson       | 3309.15     |
| Rick Reed            | 3302.26     |
| Brian Dahlen         | 3288.47     |
| Brian Stugart        | 3288.11     |
| Rob Williams         | 3279.75     |
| Daniel Lacy          | 3272.2      |
| Damala Kotsonis      | 3256.48     |
| Adam Shillingsburg   | 3255.31     |
| Jack O'Briant        | 3254.95     |
| Adam Hart            | 3250.34     |
| Henry Goldwyn        | 3247.64     |
| Lindsay Castell      | 3246.63     |
| Carol Triggs         | 3241.9      |
| Edward Becker        | 3236.31     |
| Sharelle Roach       | 3233.48     |
| Lindsay Williams     | 3230.31     |
| Ricardo Sperren      | 3221.29     |
| Alejandro Savely     | 3214.24     |
| Mark Packer          | 3206.13     |
| Christine Sundaresam | 3202.16     |
| Brian Thompson       | 3196.75     |
| Deirdre Greer        | 3195.82     |
| Jeremy Lonsdale      | 3173.87     |
| Greg Matthias        | 3163.63     |
| Janet Martin         | 3159.12     |
| Chloris Kastensmidt  | 3154.86     |
| Karen Bern           | 3152.62     |
| Maxwell Schwartz     | 3144.68     |
| Ruben Dartt          | 3133.92     |
| Tanja Norvell        | 3130.22     |
| Steve Nguyen         | 3127.96     |
| Speros Goranitis     | 3124.83     |
| Katherine Hughes     | 3100.61     |
| Patrick Gardner      | 3086.91     |
| Eugene Hildebrand    | 3082.65     |
| Gary Mitchum         | 3078.62     |
| Eugene Barchas       | 3071.13     |
| Mike Gockenbach      | 3061.54     |
| Toby Gnade           | 3058.37     |
| Kean Takahito        | 3057.1      |
| Shahid Shariari      | 3056.81     |
| Sara Luxemburg       | 3053.01     |
| Aaron Smayling       | 3050.69     |
| Cynthia Arntzen      | 3041.57     |
| Carlos Soltero       | 3036.55     |
| Lindsay Shagiari     | 2988.67     |
| Michelle Huthwaite   | 2984.95     |
| Frank Atkinson       | 2984.05     |
| David Bremer         | 2973.09     |
| Noel Staavos         | 2964.82     |
| Tamara Manning       | 2955.23     |
| Christine Kargatis   | 2945.32     |
| Thea Hudgings        | 2942.77     |
| Liz Thompson         | 2936.25     |
| Becky Castell        | 2933.68     |
| Julie Kriz           | 2932.48     |
| Shaun Weien          | 2921.54     |
| Maris LaWare         | 2921.5      |
| Rob Dowd             | 2912.89     |
| Craig Yedwab         | 2900.03     |

### Query 10: Query 2: Single highest-value order line per customer (correlated subquery)

```sql
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
LIMIT 20
```

**Rows returned: 20**

| customer_name        | order_id       | product_id      | max_sale_in_order |
|----------------------|----------------|-----------------|-------------------|
| Sean Miller          | CA-2014-145317 | TEC-MA-10002412 | 22638.48          |
| Tamara Chand         | CA-2016-118689 | TEC-CO-10004722 | 17499.95          |
| Raymond Buch         | CA-2017-140151 | TEC-CO-10004722 | 13999.96          |
| Tom Ashbrook         | CA-2017-127180 | TEC-CO-10004722 | 11199.97          |
| Hunter Lopez         | CA-2017-166709 | TEC-CO-10004722 | 10499.97          |
| Adrian Barton        | CA-2016-117121 | OFF-BI-10000545 | 9892.74           |
| Sanjit Chand         | CA-2014-116904 | OFF-BI-10001120 | 9449.95           |
| Bill Shonely         | US-2016-107440 | TEC-MA-10001047 | 9099.93           |
| Sanjit Engle         | CA-2016-158841 | TEC-MA-10001127 | 8749.95           |
| Christopher Conant   | CA-2016-143714 | TEC-CO-10004722 | 8399.98           |
| Ken Lonsdale         | CA-2014-143917 | OFF-SU-10000151 | 8187.65           |
| Becky Martin         | CA-2014-139892 | TEC-MA-10000822 | 8159.95           |
| Grant Thornton       | US-2017-168116 | TEC-MA-10004125 | 7999.98           |
| Tom Boeckenhauer     | CA-2014-145541 | TEC-MA-10001127 | 6999.96           |
| Christopher Martinez | CA-2015-145352 | OFF-BI-10003527 | 6354.95           |
| Andy Reiter          | CA-2017-138289 | OFF-BI-10004995 | 5443.96           |
| Daniel Raglin        | US-2016-140158 | TEC-CO-10001449 | 5399.91           |
| Todd Sumrall         | CA-2017-143112 | TEC-MA-10001047 | 5199.96           |
| Jane Waco            | CA-2017-135909 | OFF-BI-10003527 | 5083.96           |
| Edward Hooks         | CA-2016-136301 | OFF-SU-10000151 | 4912.59           |


## Section 2 — CTEs (Common Table Expressions)

### Query 11
```sql
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
ORDER BY total_sales DESC
```

**Rows returned: 793**

| customer_name          | segment     | total_sales | total_orders | total_profit |
|------------------------|-------------|-------------|--------------|--------------|
| Sean Miller            | Home Office | 25043.05    | 5            | -1980.74     |
| Tamara Chand           | Corporate   | 19052.22    | 5            | 8981.32      |
| Raymond Buch           | Consumer    | 15117.34    | 6            | 6976.1       |
| Tom Ashbrook           | Home Office | 14595.62    | 4            | 4703.79      |
| Adrian Barton          | Consumer    | 14473.57    | 10           | 5444.81      |
| Ken Lonsdale           | Consumer    | 14175.23    | 12           | 806.86       |
| Sanjit Chand           | Consumer    | 14142.33    | 9            | 5757.41      |
| Hunter Lopez           | Consumer    | 12873.3     | 6            | 5622.43      |
| Sanjit Engle           | Consumer    | 12209.44    | 11           | 2650.68      |
| Christopher Conant     | Consumer    | 12129.07    | 5            | 2177.05      |
| Todd Sumrall           | Corporate   | 11891.75    | 6            | 2371.71      |
| Greg Tran              | Consumer    | 11820.12    | 11           | 2163.43      |
| Becky Martin           | Consumer    | 11789.63    | 4            | -1659.96     |
| Seth Vernon            | Consumer    | 11470.95    | 10           | 1199.42      |
| Caroline Jumper        | Consumer    | 11164.97    | 8            | 858.74       |
| Clay Ludtke            | Consumer    | 10880.55    | 12           | 1933.78      |
| Maria Etezadi          | Home Office | 10663.73    | 10           | 1859.47      |
| Karen Ferguson         | Home Office | 10604.27    | 7            | 1660.14      |
| Bill Shonely           | Corporate   | 10501.65    | 5            | 2616.06      |
| Edward Hooks           | Corporate   | 10310.88    | 12           | 1393.52      |
| John Lee               | Consumer    | 9799.92     | 11           | 228.91       |
| Grant Thornton         | Corporate   | 9351.21     | 3            | -4108.66     |
| Helen Wasserman        | Corporate   | 9300.25     | 8            | 2164.16      |
| Tom Boeckenhauer       | Consumer    | 9133.99     | 7            | 2798.37      |
| Peter Fuller           | Consumer    | 9062.86     | 4            | -614.29      |
| Christopher Martinez   | Consumer    | 8954.02     | 4            | 3899.89      |
| Justin Deggeller       | Corporate   | 8828.03     | 8            | 1619.52      |
| Joe Elijah             | Consumer    | 8697.84     | 10           | 1262.29      |
| Laura Armstrong        | Corporate   | 8673.22     | 11           | 2059.12      |
| Pete Kriz              | Consumer    | 8646.93     | 12           | 2038.27      |
| Daniel Raglin          | Home Office | 8350.87     | 8            | 2869.08      |
| Natalie Fritzler       | Consumer    | 8322.83     | 7            | -1695.97     |
| Karen Daniels          | Consumer    | 8282.36     | 5            | 1107.7       |
| Nick Crebassa          | Corporate   | 8241.74     | 7            | 1314.76      |
| Harry Marie            | Corporate   | 8236.76     | 10           | 2437.98      |
| Keith Dawkins          | Corporate   | 8181.26     | 12           | 3038.63      |
| Sean Braxton           | Corporate   | 8057.89     | 7            | -2082.75     |
| Zuschuss Carroll       | Consumer    | 8025.71     | 13           | -1032.15     |
| Joseph Holt            | Consumer    | 7955.0      | 6            | -644.7       |
| Nora Preis             | Consumer    | 7903.18     | 7            | 631.23       |
| Anna Häberlin          | Corporate   | 7888.29     | 12           | 1298.02      |
| Adam Bellavance        | Home Office | 7755.62     | 8            | 2054.59      |
| Jim Epp                | Corporate   | 7754.98     | 7            | 1623.4       |
| Jane Waco              | Corporate   | 7721.71     | 6            | 2173.71      |
| Lena Creighton         | Consumer    | 7663.13     | 12           | 1288.35      |
| John Murray            | Consumer    | 7625.08     | 7            | 1574.62      |
| Jonathan Doherty       | Corporate   | 7610.86     | 11           | 1050.27      |
| Patrick O'Brill        | Consumer    | 7473.83     | 11           | 38.48        |
| Maribeth Schnelling    | Consumer    | 7443.69     | 10           | 844.94       |
| Rick Wilson            | Corporate   | 7397.4      | 7            | 1586.63      |
| Brian Moss             | Corporate   | 7294.19     | 11           | 2199.28      |
| Paul Prost             | Home Office | 7252.61     | 10           | 1495.09      |
| Natalie Webber         | Consumer    | 7234.01     | 7            | 1023.12      |
| Dean percer            | Home Office | 7198.76     | 11           | 333.36       |
| Fred Hopkins           | Corporate   | 6987.2      | 8            | 2050.28      |
| Rick Huthwaite         | Home Office | 6979.18     | 6            | 1289.45      |
| Penelope Sewall        | Home Office | 6843.63     | 7            | 1742.73      |
| Brenda Bowman          | Corporate   | 6765.73     | 9            | 1015.08      |
| Joel Eaton             | Consumer    | 6760.81     | 13           | 221.8        |
| Yana Sorensen          | Corporate   | 6720.44     | 8            | 1778.29      |
| Andy Reiter            | Consumer    | 6608.45     | 6            | 2884.62      |
| Dan Reichenbach        | Corporate   | 6528.03     | 9            | 1641.86      |
| Grace Kelly            | Corporate   | 6497.27     | 9            | 1448.55      |
| Joseph Airdo           | Consumer    | 6491.03     | 8            | -819.42      |
| Nathan Mautz           | Home Office | 6459.34     | 7            | 2751.68      |
| Valerie Dominguez      | Consumer    | 6442.25     | 6            | 1617.79      |
| Sarah Brown            | Consumer    | 6411.0      | 6            | 885.46       |
| James Galang           | Consumer    | 6366.39     | 11           | 1415.67      |
| Darrin Martin          | Consumer    | 6345.1      | 7            | 1677.39      |
| Corinna Mitchell       | Home Office | 6339.56     | 6            | 1572.46      |
| Max Jones              | Consumer    | 6320.75     | 7            | 1054.55      |
| Brosina Hoffman        | Consumer    | 6255.35     | 8            | 802.79       |
| Rob Lucas              | Consumer    | 6234.91     | 8            | 488.15       |
| William Brown          | Consumer    | 6160.1      | 11           | 714.33       |
| Victoria Wilson        | Corporate   | 6134.04     | 10           | -874.66      |
| Shirley Daniels        | Home Office | 6121.11     | 9            | 1985.17      |
| Quincy Jones           | Corporate   | 6108.34     | 9            | 1203.68      |
| Alan Dominguez         | Home Office | 6106.88     | 8            | 1869.93      |
| Cassandra Brandow      | Consumer    | 6076.14     | 10           | 150.21       |
| Greg Maxwell           | Corporate   | 6049.97     | 3            | 188.72       |
| Shahid Collister       | Consumer    | 5992.54     | 9            | 236.66       |
| Kristen Hastings       | Corporate   | 5990.8      | 7            | 1227.51      |
| Robert Marley          | Home Office | 5979.1      | 5            | 1902.54      |
| Keith Herrera          | Consumer    | 5952.86     | 7            | 656.12       |
| Ben Ferrer             | Home Office | 5907.97     | 11           | 1538.21      |
| Christine Phan         | Corporate   | 5888.28     | 8            | -1850.3      |
| Bill Donatelli         | Consumer    | 5718.52     | 12           | 1094.5       |
| Cindy Stewart          | Consumer    | 5690.05     | 6            | -6626.39     |
| Anne McFarland         | Consumer    | 5664.02     | 8            | 1085.73      |
| Ross Baird             | Home Office | 5633.32     | 8            | -461.73      |
| Katherine Murray       | Home Office | 5620.19     | 8            | 973.79       |
| Alex Avila             | Consumer    | 5563.56     | 5            | -362.88      |
| Suzanne McNair         | Corporate   | 5563.39     | 12           | 581.57       |
| Naresj Patel           | Consumer    | 5529.62     | 6            | 1208.89      |
| Amy Cox                | Consumer    | 5527.85     | 7            | 1366.01      |
| Mick Hernandez         | Home Office | 5503.09     | 9            | 170.97       |
| Dennis Pardue          | Home Office | 5480.72     | 9            | 1571.83      |
| Emily Phan             | Consumer    | 5478.06     | 17           | 144.96       |
| Yoseph Carroll         | Corporate   | 5454.35     | 5            | 1305.63      |
| Stefania Perrino       | Corporate   | 5440.32     | 9            | -270.43      |
| Luke Weiss             | Consumer    | 5420.51     | 7            | 837.24       |
| Cathy Prescott         | Corporate   | 5402.25     | 8            | 427.03       |
| Thomas Seio            | Corporate   | 5371.09     | 7            | 862.89       |
| Tonja Turnell          | Home Office | 5364.81     | 7            | 1124.5       |
| Mitch Webber           | Consumer    | 5341.9      | 7            | 1238.42      |
| Tom Prescott           | Consumer    | 5329.0      | 5            | -1087.39     |
| Tamara Willingham      | Home Office | 5278.83     | 7            | 737.39       |
| Dianna Wilson          | Home Office | 5271.63     | 5            | 1348.76      |
| Mitch Willingham       | Corporate   | 5253.88     | 2            | 1665.52      |
| Harold Ryan            | Corporate   | 5248.79     | 7            | 1196.95      |
| Steven Cartwright      | Consumer    | 5226.21     | 11           | 1276.65      |
| Resi Pölking           | Consumer    | 5153.08     | 12           | 465.25       |
| Lena Radford           | Consumer    | 5142.89     | 6            | 535.48       |
| Mike Pelletier         | Home Office | 5087.92     | 9            | 226.45       |
| Anna Andreadi          | Consumer    | 5086.94     | 6            | 857.8        |
| Ivan Liston            | Consumer    | 5040.74     | 7            | 1121.94      |
| Kelly Lampkin          | Corporate   | 5016.49     | 8            | -182.78      |
| Laurel Beltran         | Home Office | 4985.68     | 8            | -52.19       |
| Dave Hallsten          | Corporate   | 4932.87     | 6            | 1193.74      |
| Irene Maddox           | Consumer    | 4930.47     | 7            | 514.65       |
| Ted Trevino            | Consumer    | 4915.6      | 7            | 751.96       |
| Kunst Miller           | Consumer    | 4909.47     | 8            | 745.77       |
| Philisse Overcash      | Home Office | 4893.04     | 9            | 1155.43      |
| Heather Kirkland       | Corporate   | 4877.78     | 8            | 956.95       |
| Anthony Jacobs         | Corporate   | 4867.34     | 7            | 150.71       |
| Joe Kamberova          | Consumer    | 4867.2      | 10           | 55.05        |
| Alan Hwang             | Consumer    | 4805.34     | 9            | 1308.55      |
| Dean Katz              | Corporate   | 4802.39     | 9            | 209.9        |
| Russell Applegate      | Consumer    | 4793.54     | 9            | 304.87       |
| Sue Ann Reed           | Consumer    | 4767.34     | 10           | 610.15       |
| Jim Kriz               | Home Office | 4760.43     | 9            | 1172.53      |
| Bart Watters           | Corporate   | 4750.36     | 8            | 921.26       |
| Tracy Blumstein        | Consumer    | 4737.49     | 9            | -1603.05     |
| Giulietta Baptist      | Consumer    | 4716.29     | 5            | 1135.84      |
| Rick Bensley           | Home Office | 4715.47     | 12           | 640.55       |
| Erin Smith             | Corporate   | 4657.92     | 9            | 246.67       |
| Deborah Brumfield      | Home Office | 4655.9      | 8            | 841.83       |
| Kean Thornton          | Consumer    | 4642.09     | 10           | 194.07       |
| Sample Company A       | Home Office | 4624.57     | 9            | 1011.74      |
| Eugene Moren           | Home Office | 4588.44     | 6            | 1319.37      |
| Dave Brooks            | Consumer    | 4531.65     | 7            | 473.03       |
| Anthony Rawles         | Corporate   | 4523.34     | 8            | 494.84       |
| Arthur Gainer          | Consumer    | 4510.8      | 10           | 343.68       |
| Anthony Johnson        | Corporate   | 4501.39     | 7            | 1158.71      |
| Linda Cazamias         | Corporate   | 4492.95     | 8            | 288.27       |
| Stewart Carmichael     | Corporate   | 4492.66     | 7            | -671.19      |
| Theone Pippenger       | Consumer    | 4454.06     | 9            | 1129.13      |
| Mark Cousins           | Corporate   | 4432.14     | 5            | 1802.39      |
| Jamie Kunitz           | Consumer    | 4427.14     | 5            | 1219.98      |
| Katrina Willman        | Consumer    | 4416.52     | 5            | 1756.14      |
| Bradley Drucker        | Consumer    | 4411.24     | 6            | 1142.12      |
| Arianne Irving         | Consumer    | 4375.79     | 10           | 867.73       |
| Scot Coram             | Corporate   | 4371.96     | 4            | 440.14       |
| Ellis Ballard          | Corporate   | 4358.13     | 5            | 656.2        |
| Gary Zandusky          | Consumer    | 4355.15     | 9            | 1087.75      |
| Steven Roelle          | Home Office | 4345.89     | 8            | 1990.42      |
| Natalie DeCherney      | Consumer    | 4326.14     | 9            | 353.65       |
| Matt Abelman           | Home Office | 4299.16     | 11           | 1240.23      |
| Sung Pak               | Corporate   | 4282.94     | 10           | 566.72       |
| Dana Kaydos            | Consumer    | 4282.18     | 5            | 937.65       |
| Rick Duston            | Consumer    | 4272.93     | 8            | 480.59       |
| Toby Carlisle          | Consumer    | 4266.81     | 8            | 606.37       |
| Alan Schoenberger      | Corporate   | 4260.78     | 5            | 719.78       |
| Frank Hawley           | Corporate   | 4256.27     | 10           | 1073.27      |
| Claudia Bergmann       | Corporate   | 4246.46     | 8            | 1049.56      |
| Tracy Hopkins          | Home Office | 4234.1      | 7            | -571.97      |
| Bill Eplett            | Home Office | 4204.68     | 5            | 1487.77      |
| Jill Fjeld             | Consumer    | 4198.33     | 8            | 1073.21      |
| Gary Hwang             | Consumer    | 4172.85     | 4            | 1176.42      |
| Roland Schwarz         | Corporate   | 4159.77     | 8            | 1206.39      |
| Muhammed Yedwab        | Corporate   | 4152.7      | 11           | -371.71      |
| Peter McVee            | Home Office | 4115.66     | 4            | 526.75       |
| Stewart Visinsky       | Consumer    | 4105.31     | 9            | 485.03       |
| Denise Monton          | Corporate   | 4074.47     | 8            | 1319.06      |
| Frank Preis            | Consumer    | 4046.75     | 8            | 406.45       |
| Susan Pistek           | Consumer    | 3990.69     | 6            | 14.69        |
| Craig Molinari         | Corporate   | 3984.45     | 4            | 176.31       |
| Michael Paige          | Corporate   | 3983.64     | 9            | 638.16       |
| Sean Christensen       | Consumer    | 3979.06     | 7            | 229.16       |
| Sanjit Jacobs          | Home Office | 3949.66     | 12           | 144.12       |
| Luke Foster            | Consumer    | 3930.51     | 7            | -3583.98     |
| Pierre Wener           | Consumer    | 3922.41     | 7            | 1290.35      |
| George Ashbrook        | Consumer    | 3919.78     | 8            | 840.9        |
| Ken Heidel             | Corporate   | 3918.97     | 9            | 727.38       |
| Chris Cortes           | Consumer    | 3913.42     | 12           | 393.96       |
| Dorothy Badders        | Corporate   | 3908.8      | 7            | 109.33       |
| Nora Paige             | Consumer    | 3908.4      | 5            | 514.6        |
| Kelly Collister        | Consumer    | 3908.26     | 4            | 709.42       |
| Fred Chung             | Corporate   | 3889.37     | 7            | 714.29       |
| Bill Stewart           | Corporate   | 3887.83     | 5            | -17.53       |
| John Stevenson         | Consumer    | 3868.02     | 5            | 564.98       |
| Ruben Ausman           | Corporate   | 3832.31     | 7            | 1292.87      |
| Annie Thurman          | Consumer    | 3831.86     | 10           | 974.11       |
| Olvera Toch            | Consumer    | 3818.62     | 5            | -925.12      |
| Rose O'Brian           | Consumer    | 3815.48     | 7            | -1262.57     |
| Michael Chen           | Consumer    | 3805.71     | 7            | 698.42       |
| Michael Moore          | Consumer    | 3794.08     | 11           | 82.13        |
| Carol Adams            | Corporate   | 3789.72     | 6            | 1143.38      |
| Matthew Grinstein      | Home Office | 3785.28     | 7            | 341.9        |
| Maribeth Dona          | Consumer    | 3766.38     | 7            | -241.95      |
| Jim Karlsson           | Consumer    | 3760.03     | 7            | 750.95       |
| Juliana Krohn          | Consumer    | 3747.67     | 3            | 586.66       |
| Frank Merwin           | Home Office | 3736.2      | 9            | 198.11       |
| Scott Cohen            | Corporate   | 3729.79     | 8            | 671.0        |
| Hunter Glantz          | Consumer    | 3690.28     | 7            | 804.61       |
| Ben Peterman           | Corporate   | 3675.86     | 9            | 363.6        |
| Liz Preis              | Consumer    | 3653.4      | 7            | 338.45       |
| Christopher Schild     | Home Office | 3651.86     | 9            | -342.8       |
| Ed Braxton             | Corporate   | 3644.98     | 9            | 13.62        |
| Jeremy Pistek          | Consumer    | 3635.59     | 7            | 757.18       |
| Sam Zeldin             | Home Office | 3625.33     | 11           | 366.43       |
| Rick Hansen            | Consumer    | 3621.38     | 5            | 563.79       |
| Thomas Boland          | Corporate   | 3589.3      | 4            | 829.16       |
| Gary McGarr            | Consumer    | 3582.82     | 7            | 347.27       |
| Dionis Lloyd           | Corporate   | 3539.32     | 8            | -52.79       |
| Erica Smith            | Consumer    | 3510.46     | 5            | 1003.29      |
| Robert Waldorf         | Consumer    | 3495.65     | 5            | 707.55       |
| Anna Gayman            | Consumer    | 3489.04     | 7            | -246.43      |
| Emily Ducich           | Home Office | 3484.92     | 8            | 670.44       |
| Pauline Webber         | Corporate   | 3454.92     | 10           | 803.82       |
| Sarah Foster           | Consumer    | 3422.79     | 9            | 286.9        |
| Frank Carlisle         | Home Office | 3418.74     | 7            | 1217.17      |
| Sally Hughsby          | Corporate   | 3406.84     | 13           | 558.47       |
| Sandra Glassco         | Consumer    | 3406.58     | 3            | 570.44       |
| Trudy Schmidt          | Consumer    | 3368.09     | 5            | 220.92       |
| Sam Craven             | Consumer    | 3362.96     | 5            | -317.05      |
| Victoria Pisteka       | Corporate   | 3360.53     | 7            | -1018.78     |
| Doug Jacobs            | Consumer    | 3356.4      | 3            | 731.56       |
| Dianna Vittorini       | Consumer    | 3341.59     | 6            | 353.21       |
| Sylvia Foulston        | Corporate   | 3336.54     | 9            | 539.94       |
| Dan Campbell           | Consumer    | 3336.17     | 9            | -1441.63     |
| Arthur Prichep         | Consumer    | 3323.56     | 10           | 579.31       |
| Dennis Kane            | Consumer    | 3318.49     | 8            | 377.08       |
| Katharine Harms        | Corporate   | 3312.86     | 8            | 454.79       |
| Randy Ferguson         | Corporate   | 3309.15     | 8            | 633.71       |
| Rick Reed              | Corporate   | 3302.26     | 6            | 721.68       |
| Brian Dahlen           | Consumer    | 3288.47     | 7            | 634.85       |
| Brian Stugart          | Consumer    | 3288.11     | 3            | 238.74       |
| Rob Williams           | Corporate   | 3279.75     | 9            | 698.83       |
| Daniel Lacy            | Consumer    | 3272.2      | 6            | 4.21         |
| Damala Kotsonis        | Corporate   | 3256.48     | 12           | 881.12       |
| Adam Shillingsburg     | Consumer    | 3255.31     | 9            | 64.54        |
| Jack O'Briant          | Corporate   | 3254.95     | 9            | 581.4        |
| Adam Hart              | Corporate   | 3250.34     | 10           | 281.19       |
| Henry Goldwyn          | Corporate   | 3247.64     | 12           | -2797.96     |
| Lindsay Castell        | Home Office | 3246.63     | 4            | 299.48       |
| Carol Triggs           | Consumer    | 3241.9      | 8            | 161.23       |
| Edward Becker          | Corporate   | 3236.31     | 10           | -80.29       |
| Sharelle Roach         | Home Office | 3233.48     | 5            | -3333.91     |
| Lindsay Williams       | Corporate   | 3230.31     | 6            | 662.83       |
| Ricardo Sperren        | Corporate   | 3221.29     | 5            | 633.45       |
| Alejandro Savely       | Corporate   | 3214.24     | 6            | 354.63       |
| Mark Packer            | Home Office | 3206.13     | 7            | 600.29       |
| Christine Sundaresam   | Consumer    | 3202.16     | 11           | 831.94       |
| Brian Thompson         | Consumer    | 3196.75     | 7            | 447.75       |
| Deirdre Greer          | Corporate   | 3195.82     | 5            | 562.78       |
| Jeremy Lonsdale        | Consumer    | 3173.87     | 6            | 591.72       |
| Greg Matthias          | Consumer    | 3163.63     | 6            | 35.49        |
| Janet Martin           | Consumer    | 3159.12     | 6            | 19.82        |
| Chloris Kastensmidt    | Consumer    | 3154.86     | 13           | 141.28       |
| Karen Bern             | Corporate   | 3152.62     | 7            | 763.91       |
| Maxwell Schwartz       | Consumer    | 3144.68     | 9            | 280.86       |
| Ruben Dartt            | Consumer    | 3133.92     | 9            | 455.53       |
| Tanja Norvell          | Home Office | 3130.22     | 7            | -692.05      |
| Steve Nguyen           | Home Office | 3127.96     | 7            | 481.75       |
| Speros Goranitis       | Consumer    | 3124.83     | 6            | 463.27       |
| Katherine Hughes       | Consumer    | 3100.61     | 6            | 528.21       |
| Patrick Gardner        | Consumer    | 3086.91     | 13           | 137.46       |
| Eugene Hildebrand      | Home Office | 3082.65     | 10           | 96.27        |
| Gary Mitchum           | Home Office | 3078.62     | 6            | 793.28       |
| Eugene Barchas         | Consumer    | 3071.13     | 6            | 184.77       |
| Mike Gockenbach        | Consumer    | 3061.54     | 4            | -93.6        |
| Toby Gnade             | Consumer    | 3058.37     | 5            | 682.17       |
| Kean Takahito          | Consumer    | 3057.1      | 7            | 254.0        |
| Shahid Shariari        | Consumer    | 3056.81     | 6            | -1010.97     |
| Sara Luxemburg         | Home Office | 3053.01     | 7            | 527.97       |
| Aaron Smayling         | Corporate   | 3050.69     | 7            | -253.57      |
| Cynthia Arntzen        | Consumer    | 3041.57     | 7            | 204.49       |
| Carlos Soltero         | Consumer    | 3036.55     | 11           | -126.42      |
| Lindsay Shagiari       | Home Office | 2988.67     | 9            | 262.64       |
| Michelle Huthwaite     | Consumer    | 2984.95     | 5            | 476.9        |
| Frank Atkinson         | Corporate   | 2984.05     | 7            | 520.52       |
| David Bremer           | Corporate   | 2973.09     | 7            | -1421.77     |
| Noel Staavos           | Corporate   | 2964.82     | 13           | -234.77      |
| Tamara Manning         | Consumer    | 2955.23     | 8            | 573.3        |
| Christine Kargatis     | Home Office | 2945.32     | 5            | 261.22       |
| Thea Hudgings          | Corporate   | 2942.77     | 4            | -252.55      |
| Liz Thompson           | Consumer    | 2936.25     | 8            | 320.97       |
| Becky Castell          | Home Office | 2933.68     | 9            | 251.6        |
| Julie Kriz             | Home Office | 2932.48     | 10           | 122.66       |
| Shaun Weien            | Consumer    | 2921.54     | 7            | 793.65       |
| Maris LaWare           | Consumer    | 2921.5      | 6            | -76.18       |
| Rob Dowd               | Consumer    | 2912.89     | 10           | 734.52       |
| Craig Yedwab           | Corporate   | 2900.03     | 8            | 60.65        |
| Neil Ducich            | Corporate   | 2893.46     | 6            | 443.34       |
| Meg Tillman            | Consumer    | 2890.14     | 6            | 509.01       |
| Barry Französisch      | Corporate   | 2888.51     | 8            | 302.02       |
| David Smith            | Corporate   | 2881.81     | 9            | 163.7        |
| Paul Van Hugh          | Home Office | 2876.05     | 5            | 434.53       |
| Ionia McGrath          | Consumer    | 2872.63     | 3            | 975.77       |
| Chuck Clark            | Home Office | 2870.05     | 10           | 424.66       |
| Craig Carroll          | Consumer    | 2854.12     | 4            | 850.16       |
| Arthur Wiediger        | Home Office | 2852.97     | 7            | -104.55      |
| Erin Ashbrook          | Corporate   | 2846.71     | 13           | -52.74       |
| Linda Southworth       | Corporate   | 2845.27     | 6            | -318.77      |
| Darren Budd            | Corporate   | 2839.23     | 5            | 213.0        |
| Justin MacKendrick     | Consumer    | 2833.93     | 10           | 754.11       |
| Christina VanderZanden | Consumer    | 2830.63     | 5            | 493.09       |
| Troy Staebel           | Consumer    | 2820.42     | 7            | -294.7       |
| Gary Hansen            | Home Office | 2819.47     | 9            | -576.83      |
| Barry Gonzalez         | Consumer    | 2798.95     | 8            | -711.43      |
| Trudy Brown            | Consumer    | 2797.67     | 9            | 379.88       |
| Robert Dilbeck         | Home Office | 2786.63     | 5            | 835.77       |
| John Castell           | Consumer    | 2772.06     | 9            | 279.57       |
| Philip Fox             | Consumer    | 2770.0      | 6            | 196.87       |
| Emily Burns            | Consumer    | 2767.22     | 10           | 261.53       |
| Chris Selesnick        | Corporate   | 2754.22     | 12           | 738.36       |
| Michelle Moray         | Consumer    | 2749.88     | 8            | -520.34      |
| Ken Black              | Corporate   | 2744.74     | 12           | 579.36       |
| Lauren Leatherbury     | Consumer    | 2741.2      | 6            | 560.01       |
| Marc Crier             | Consumer    | 2725.98     | 8            | 461.0        |
| John Lucas             | Consumer    | 2725.26     | 6            | 779.9        |
| Marina Lichtenstein    | Corporate   | 2722.84     | 9            | 684.92       |
| Jay Kimmel             | Consumer    | 2709.63     | 8            | 330.28       |
| Justin Ellison         | Corporate   | 2697.25     | 3            | 789.65       |
| Bradley Talbott        | Home Office | 2684.49     | 5            | 409.5        |
| Bill Overfelt          | Corporate   | 2682.73     | 5            | 278.78       |
| Frank Olsen            | Consumer    | 2678.44     | 10           | 215.6        |
| Nicole Hansen          | Corporate   | 2673.29     | 7            | 760.17       |
| Richard Bierner        | Consumer    | 2663.09     | 8            | 477.24       |
| Eva Jacobs             | Consumer    | 2656.69     | 5            | 451.88       |
| Dave Kipp              | Consumer    | 2650.56     | 7            | 536.39       |
| Christina Anderson     | Consumer    | 2648.29     | 9            | 279.62       |
| Logan Currie           | Consumer    | 2633.58     | 9            | 231.13       |
| Ralph Arnett           | Consumer    | 2617.91     | 9            | 546.09       |
| Katherine Nockton      | Corporate   | 2617.27     | 9            | -151.15      |
| Sean O'Donnell         | Consumer    | 2602.58     | 6            | -81.09       |
| Stephanie Ulpright     | Home Office | 2595.36     | 7            | 763.47       |
| Helen Andreada         | Consumer    | 2584.16     | 8            | 99.14        |
| Alejandro Grove        | Consumer    | 2582.9      | 5            | 732.74       |
| Lena Cacioppo          | Consumer    | 2580.7      | 8            | -188.25      |
| Steve Chapman          | Corporate   | 2576.41     | 10           | 611.83       |
| Neola Schneider        | Consumer    | 2575.86     | 4            | -12.3        |
| Beth Thompson          | Home Office | 2567.66     | 5            | 417.59       |
| Eleni McCrary          | Corporate   | 2567.01     | 5            | -133.83      |
| Mary Zewe              | Corporate   | 2564.91     | 6            | 787.75       |
| Bruce Stewart          | Consumer    | 2562.38     | 7            | -113.3       |
| Deanra Eno             | Home Office | 2550.87     | 5            | 464.47       |
| Corey Catlett          | Corporate   | 2540.63     | 7            | 331.43       |
| Ann Chong              | Corporate   | 2537.69     | 5            | 298.83       |
| Charles McCrossin      | Consumer    | 2533.31     | 6            | -394.37      |
| Herbert Flentye        | Consumer    | 2533.16     | 7            | -13.88       |
| Fred McMath            | Consumer    | 2523.27     | 9            | 191.49       |
| Julia Barnett          | Home Office | 2518.11     | 5            | 201.52       |
| Joy Smith              | Consumer    | 2516.49     | 6            | -311.26      |
| Don Jones              | Corporate   | 2501.69     | 8            | 345.25       |
| Amy Hunt               | Consumer    | 2495.39     | 5            | -196.12      |
| Patrick O'Donnell      | Consumer    | 2493.21     | 7            | 437.85       |
| Nick Zandusky          | Home Office | 2488.31     | 9            | 402.42       |
| Michael Nguyen         | Consumer    | 2477.95     | 6            | 290.82       |
| Beth Paige             | Consumer    | 2475.16     | 7            | -319.06      |
| Charles Crestani       | Consumer    | 2471.65     | 7            | 392.28       |
| Nat Carroll            | Consumer    | 2461.4      | 5            | 580.31       |
| Filia McAdams          | Corporate   | 2456.64     | 10           | 249.68       |
| Mark Hamilton          | Consumer    | 2456.18     | 8            | 484.77       |
| Brendan Sweed          | Corporate   | 2454.93     | 6            | 381.78       |
| Valerie Mitchum        | Home Office | 2454.87     | 7            | 513.53       |
| George Zrebassa        | Corporate   | 2454.62     | 4            | 828.66       |
| Michelle Arnett        | Home Office | 2453.28     | 6            | 280.78       |
| Bart Pistole           | Corporate   | 2442.04     | 12           | 433.98       |
| Matt Collister         | Corporate   | 2426.07     | 6            | 288.98       |
| Thea Hendricks         | Consumer    | 2422.82     | 5            | -135.21      |
| Marc Harrigan          | Home Office | 2394.02     | 6            | 28.76        |
| David Flashing         | Consumer    | 2390.53     | 3            | -259.31      |
| Xylona Preis           | Consumer    | 2374.66     | 11           | 621.23       |
| Clytie Kelty           | Consumer    | 2372.75     | 11           | 497.71       |
| Jennifer Ferguson      | Consumer    | 2371.45     | 6            | 635.64       |
| Cynthia Voltz          | Corporate   | 2370.31     | 9            | 99.0         |
| Nick Radford           | Consumer    | 2367.28     | 5            | -25.15       |
| Jack Garza             | Consumer    | 2358.68     | 3            | 684.19       |
| Andrew Gjertsen        | Corporate   | 2356.86     | 8            | 295.67       |
| Craig Leslie           | Home Office | 2353.59     | 5            | 229.01       |
| Maureen Gastineau      | Home Office | 2350.19     | 4            | 25.89        |
| Roland Fjeld           | Consumer    | 2341.3      | 7            | 711.62       |
| Elizabeth Moffitt      | Corporate   | 2339.6      | 8            | 682.55       |
| Dean Braden            | Consumer    | 2332.58     | 10           | 169.97       |
| Chris McAfee           | Consumer    | 2305.71     | 5            | 365.04       |
| Michael Kennedy        | Corporate   | 2302.37     | 8            | -405.36      |
| Lena Hernandez         | Consumer    | 2295.33     | 9            | 526.07       |
| Kristina Nunn          | Home Office | 2280.58     | 8            | 329.76       |
| Jamie Frazer           | Consumer    | 2279.59     | 7            | 575.13       |
| Fred Harton            | Consumer    | 2271.28     | 4            | 706.29       |
| Craig Carreira         | Consumer    | 2269.7      | 7            | 187.84       |
| Bobby Elias            | Consumer    | 2261.44     | 5            | 755.92       |
| Kalyca Meade           | Corporate   | 2260.96     | 6            | 635.11       |
| Matt Connell           | Corporate   | 2258.19     | 8            | 195.45       |
| Justin Hirsh           | Consumer    | 2256.39     | 4            | -96.95       |
| Maribeth Yedwab        | Corporate   | 2254.28     | 7            | 319.12       |
| Ken Dana               | Corporate   | 2243.51     | 5            | 539.72       |
| Tony Sayre             | Consumer    | 2243.27     | 6            | 11.38        |
| Jason Gross            | Corporate   | 2240.58     | 6            | 3.8          |
| Laurel Workman         | Corporate   | 2238.06     | 5            | 32.58        |
| Allen Rosenblatt       | Corporate   | 2236.13     | 5            | -98.76       |
| Greg Guthrie           | Corporate   | 2224.0      | 9            | 12.7         |
| Nathan Cano            | Consumer    | 2218.99     | 6            | -2204.81     |
| Mick Crebagga          | Consumer    | 2218.98     | 10           | -64.17       |
| Dave Poirier           | Corporate   | 2215.0      | 8            | 563.18       |
| Phillip Flathmann      | Consumer    | 2206.13     | 5            | 591.31       |
| Maya Herman            | Corporate   | 2203.78     | 7            | 238.56       |
| Janet Lee              | Consumer    | 2203.7      | 5            | 54.52        |
| Justin Ritter          | Corporate   | 2201.69     | 5            | 452.37       |
| Edward Nazzal          | Consumer    | 2199.37     | 4            | 496.11       |
| Toby Braunhardt        | Consumer    | 2198.45     | 6            | 490.96       |
| Giulietta Weimer       | Consumer    | 2189.02     | 7            | -268.54      |
| Bill Tyler             | Corporate   | 2186.61     | 6            | 257.92       |
| Pamela Stobb           | Consumer    | 2181.48     | 6            | -134.44      |
| Shahid Hopkins         | Consumer    | 2180.72     | 10           | -144.52      |
| Kean Nguyen            | Corporate   | 2171.96     | 5            | 114.31       |
| Daniel Byrd            | Home Office | 2171.6      | 8            | 431.37       |
| Roy Phan               | Corporate   | 2170.72     | 8            | 594.59       |
| Theresa Swint          | Corporate   | 2163.62     | 6            | 260.87       |
| Helen Abelman          | Consumer    | 2163.3      | 7            | 270.86       |
| Ed Jacobs              | Consumer    | 2162.17     | 4            | 387.02       |
| Neoma Murray           | Consumer    | 2161.98     | 10           | 788.95       |
| John Dryer             | Consumer    | 2152.35     | 5            | -266.55      |
| Clay Rozendal          | Home Office | 2148.85     | 4            | 74.4         |
| Duane Noonan           | Consumer    | 2139.79     | 7            | 540.54       |
| Karen Carlisle         | Corporate   | 2120.95     | 6            | 846.12       |
| Stefanie Holloman      | Corporate   | 2096.39     | 2            | 260.63       |
| Liz Carlisle           | Consumer    | 2095.06     | 5            | 86.78        |
| Rob Haberlin           | Consumer    | 2085.74     | 3            | 172.63       |
| Trudy Glocke           | Consumer    | 2074.66     | 4            | 365.72       |
| Max Ludwig             | Home Office | 2071.91     | 7            | 409.51       |
| Roger Barcio           | Home Office | 2067.45     | 4            | 243.08       |
| Tom Stivers            | Corporate   | 2054.14     | 5            | 48.7         |
| Art Ferguson           | Consumer    | 2052.91     | 7            | 317.97       |
| Carlos Daly            | Consumer    | 2033.97     | 5            | 426.66       |
| Nicole Fjeld           | Home Office | 2031.47     | 7            | 388.21       |
| Denny Joy              | Corporate   | 2012.52     | 4            | 483.04       |
| Victoria Brennan       | Corporate   | 2005.6      | 6            | 371.24       |
| Harold Pawlan          | Home Office | 1990.31     | 7            | 373.86       |
| Doug Bickford          | Consumer    | 1989.05     | 7            | 438.8        |
| Paul Gonzalez          | Consumer    | 1987.16     | 9            | 334.52       |
| Nona Balk              | Corporate   | 1972.6      | 9            | 117.64       |
| Scott Williamson       | Consumer    | 1966.65     | 6            | 332.87       |
| Lisa DeCherney         | Consumer    | 1961.93     | 4            | 557.17       |
| Christy Brittain       | Consumer    | 1949.2      | 8            | 272.39       |
| Tracy Poddar           | Corporate   | 1936.64     | 4            | 139.23       |
| Jas O'Carroll          | Consumer    | 1934.27     | 6            | 202.14       |
| Jay Fein               | Consumer    | 1911.84     | 6            | 330.2        |
| Max Engle              | Consumer    | 1908.45     | 8            | 77.81        |
| Susan Vittorini        | Consumer    | 1903.49     | 8            | 106.89       |
| Katherine Ducich       | Consumer    | 1888.96     | 6            | 328.59       |
| Giulietta Dortch       | Corporate   | 1888.07     | 4            | 230.94       |
| Sheri Gordon           | Consumer    | 1884.8      | 8            | -119.01      |
| Lisa Ryan              | Corporate   | 1879.31     | 5            | -382.81      |
| Shaun Chance           | Corporate   | 1875.0      | 7            | 379.56       |
| Brooke Gillingham      | Corporate   | 1874.17     | 6            | 107.57       |
| Stephanie Phelps       | Corporate   | 1872.44     | 9            | 268.48       |
| Nat Gilpin             | Corporate   | 1869.58     | 5            | 313.63       |
| Cynthia Delaney        | Home Office | 1860.73     | 5            | 403.84       |
| Skye Norling           | Home Office | 1860.42     | 6            | -716.86      |
| Patrick Ryan           | Consumer    | 1840.18     | 5            | 247.62       |
| Ashley Jarboe          | Consumer    | 1839.24     | 7            | 521.14       |
| Pamela Coakley         | Corporate   | 1832.06     | 4            | 272.69       |
| Emily Grady            | Consumer    | 1832.02     | 5            | 104.27       |
| Pauline Johnson        | Consumer    | 1824.23     | 7            | 683.0        |
| Noah Childs            | Corporate   | 1821.74     | 5            | -359.02      |
| Janet Molinari         | Corporate   | 1804.15     | 5            | 502.61       |
| Jennifer Braxton       | Corporate   | 1791.61     | 10           | 156.05       |
| Andrew Allen           | Consumer    | 1790.51     | 4            | 435.83       |
| Chad Cunningham        | Home Office | 1770.95     | 6            | 208.59       |
| Darrin Sayre           | Home Office | 1762.21     | 4            | 193.33       |
| Monica Federle         | Corporate   | 1758.3      | 5            | 456.86       |
| Aaron Hawkins          | Corporate   | 1744.7      | 7            | 365.22       |
| Logan Haushalter       | Consumer    | 1739.69     | 9            | 316.52       |
| Ben Wallace            | Consumer    | 1738.41     | 6            | 247.0        |
| Valerie Takahito       | Home Office | 1736.6      | 2            | -224.09      |
| Adrian Hane            | Home Office | 1735.51     | 7            | -2.31        |
| Mike Vittorini         | Consumer    | 1734.57     | 7            | 273.86       |
| Jessica Myrick         | Consumer    | 1733.44     | 7            | 356.54       |
| Brad Eason             | Home Office | 1727.65     | 6            | 139.2        |
| Denny Blanton          | Consumer    | 1711.69     | 4            | 438.91       |
| Julie Prescott         | Home Office | 1707.71     | 9            | 309.71       |
| Tracy Zic              | Consumer    | 1707.29     | 4            | 224.89       |
| Becky Pak              | Consumer    | 1697.86     | 6            | 647.38       |
| Darren Koutras         | Consumer    | 1687.04     | 5            | -107.35      |
| Meg O'Connel           | Home Office | 1687.03     | 8            | 169.34       |
| Ryan Akin              | Consumer    | 1686.92     | 5            | -445.7       |
| Katrina Edelman        | Corporate   | 1686.73     | 8            | 397.88       |
| Cathy Armstrong        | Home Office | 1679.72     | 5            | 211.26       |
| Candace McMahon        | Corporate   | 1673.89     | 6            | 214.46       |
| Jennifer Patt          | Corporate   | 1669.14     | 7            | 429.75       |
| Chad McGuire           | Consumer    | 1661.61     | 4            | 409.07       |
| Cindy Chapman          | Consumer    | 1659.44     | 9            | 154.85       |
| Erica Bern             | Corporate   | 1643.26     | 4            | 162.88       |
| Anne Pryor             | Home Office | 1638.55     | 8            | 285.79       |
| Annie Zypern           | Consumer    | 1622.02     | 6            | 154.95       |
| Maurice Satty          | Consumer    | 1613.4      | 6            | 247.43       |
| Tim Brockman           | Consumer    | 1602.38     | 7            | 260.62       |
| Craig Reiter           | Consumer    | 1600.55     | 4            | 306.92       |
| Alan Haines            | Corporate   | 1587.45     | 4            | -378.55      |
| Benjamin Farhat        | Home Office | 1585.16     | 4            | 523.21       |
| Cyma Kinney            | Corporate   | 1582.11     | 9            | -338.43      |
| Mike Caudle            | Corporate   | 1582.0      | 5            | 121.76       |
| James Lanier           | Home Office | 1571.52     | 5            | 209.28       |
| Karl Braun             | Consumer    | 1569.46     | 9            | 49.72        |
| George Bell            | Corporate   | 1568.44     | 11           | 7.84         |
| Odella Nelson          | Corporate   | 1567.52     | 9            | -5.89        |
| Mark Van Huff          | Consumer    | 1560.05     | 9            | 189.03       |
| Maria Bertelson        | Consumer    | 1548.7      | 10           | 212.43       |
| Brian DeCherney        | Consumer    | 1538.11     | 6            | 206.76       |
| Cathy Hwang            | Home Office | 1537.24     | 3            | 195.15       |
| Bruce Degenhardt       | Consumer    | 1526.5      | 6            | 333.98       |
| Benjamin Venier        | Corporate   | 1523.27     | 5            | 315.22       |
| Kelly Andreada         | Consumer    | 1519.51     | 7            | 234.92       |
| Ann Blume              | Corporate   | 1515.86     | 4            | -274.96      |
| John Grady             | Corporate   | 1507.02     | 6            | 206.1        |
| Dan Lawera             | Consumer    | 1503.11     | 8            | 322.24       |
| Zuschuss Donatelli     | Consumer    | 1493.94     | 5            | 249.13       |
| Charlotte Melton       | Consumer    | 1475.14     | 6            | 91.2         |
| Laurel Elliston        | Consumer    | 1469.45     | 6            | 161.76       |
| Ted Butterfield        | Consumer    | 1467.88     | 5            | 390.21       |
| Parhena Norris         | Home Office | 1467.15     | 8            | 192.04       |
| Ralph Kennedy          | Consumer    | 1460.19     | 3            | 269.69       |
| Bradley Nguyen         | Consumer    | 1459.34     | 5            | 340.71       |
| Delfina Latchford      | Consumer    | 1458.26     | 8            | 288.87       |
| Philip Brown           | Consumer    | 1456.95     | 8            | 280.66       |
| Andy Gerbode           | Corporate   | 1455.04     | 4            | -152.76      |
| Raymond Messe          | Consumer    | 1453.47     | 6            | 392.15       |
| Paul Knutson           | Home Office | 1441.15     | 2            | -798.71      |
| Tamara Dahlen          | Consumer    | 1434.55     | 9            | 88.19        |
| Julia West             | Consumer    | 1428.73     | 4            | 154.06       |
| Mick Brown             | Consumer    | 1428.23     | 7            | 117.81       |
| Thomas Thornton        | Consumer    | 1427.04     | 8            | 278.74       |
| Christine Abelman      | Corporate   | 1421.95     | 4            | 246.02       |
| Roger Demir            | Consumer    | 1419.74     | 10           | 207.33       |
| Nancy Lomonaco         | Home Office | 1418.09     | 4            | 343.64       |
| Jill Stevenson         | Corporate   | 1417.65     | 4            | -175.55      |
| Paul MacIntyre         | Consumer    | 1405.4      | 3            | 157.88       |
| Guy Armstrong          | Consumer    | 1398.38     | 11           | 136.71       |
| Cyra Reiten            | Home Office | 1397.87     | 3            | 83.27        |
| Nathan Gelder          | Consumer    | 1395.94     | 5            | 217.09       |
| Jeremy Ellison         | Consumer    | 1388.68     | 6            | 276.22       |
| Troy Blackwell         | Consumer    | 1387.56     | 5            | -136.41      |
| Frank Gastineau        | Home Office | 1383.14     | 7            | 394.74       |
| Don Miller             | Corporate   | 1376.79     | 3            | 199.77       |
| Gene Hale              | Corporate   | 1361.24     | 2            | -95.45       |
| Sarah Bern             | Consumer    | 1348.02     | 3            | 157.67       |
| Liz MacKendrick        | Consumer    | 1346.77     | 5            | -44.88       |
| Maureen Gnade          | Consumer    | 1342.28     | 3            | -398.79      |
| Sarah Jordon           | Consumer    | 1341.04     | 6            | -23.51       |
| Bryan Mills            | Consumer    | 1338.84     | 10           | 137.74       |
| Barry Franz            | Home Office | 1333.88     | 4            | -291.38      |
| Saphhira Shifley       | Corporate   | 1324.03     | 8            | 332.35       |
| Dario Medina           | Corporate   | 1322.03     | 7            | 108.76       |
| Michelle Tran          | Home Office | 1319.45     | 4            | -23.68       |
| Shirley Jackson        | Consumer    | 1318.78     | 5            | 68.1         |
| Magdelene Morse        | Consumer    | 1314.02     | 4            | 178.4        |
| Sibella Parks          | Corporate   | 1306.09     | 6            | -118.78      |
| Matt Collins           | Consumer    | 1303.89     | 8            | 210.75       |
| Eileen Kiefer          | Home Office | 1303.48     | 4            | 97.11        |
| Corey-Lock             | Consumer    | 1300.08     | 5            | 205.63       |
| Denny Ordway           | Consumer    | 1300.03     | 9            | -38.91       |
| Hallie Redmond         | Home Office | 1299.29     | 5            | 185.58       |
| Georgia Rosenberg      | Corporate   | 1284.38     | 2            | 359.83       |
| Cari Sayre             | Corporate   | 1278.95     | 5            | 185.38       |
| Paul Stevenson         | Home Office | 1278.64     | 8            | 198.51       |
| Stuart Van             | Corporate   | 1271.09     | 4            | 199.65       |
| Doug O'Connell         | Consumer    | 1267.32     | 7            | 294.07       |
| Carl Ludwig            | Consumer    | 1262.01     | 4            | 328.08       |
| Liz Willingham         | Consumer    | 1259.04     | 3            | 192.63       |
| Michelle Ellison       | Corporate   | 1256.94     | 4            | 107.36       |
| Gene McClure           | Consumer    | 1255.68     | 10           | 441.32       |
| Steve Carroll          | Home Office | 1254.64     | 6            | 370.16       |
| Matt Hagelstein        | Corporate   | 1252.8      | 4            | 122.36       |
| Elpida Rittenbach      | Corporate   | 1245.79     | 3            | -295.74      |
| Tony Chapman           | Home Office | 1244.98     | 9            | 119.1        |
| Joni Wasserman         | Consumer    | 1244.09     | 7            | -29.58       |
| Michael Grace          | Home Office | 1242.83     | 5            | -470.77      |
| Nora Pelletier         | Home Office | 1228.7      | 6            | 514.5        |
| Patrick Jones          | Corporate   | 1220.09     | 8            | 442.14       |
| Erica Hernandez        | Home Office | 1219.53     | 7            | -94.14       |
| Jack Lebron            | Consumer    | 1214.96     | 6            | -207.8       |
| Christina DeMoss       | Consumer    | 1205.58     | 2            | 233.03       |
| Michael Dominguez      | Corporate   | 1204.91     | 5            | -4.04        |
| Dorothy Wardle         | Corporate   | 1204.85     | 7            | -266.9       |
| Evan Bailliet          | Consumer    | 1186.33     | 6            | 282.17       |
| Benjamin Patterson     | Consumer    | 1181.49     | 5            | -197.27      |
| Debra Catini           | Consumer    | 1174.62     | 5            | 132.07       |
| Alyssa Tate            | Home Office | 1171.81     | 6            | 100.88       |
| Jim Radford            | Consumer    | 1156.66     | 2            | -785.16      |
| Duane Benoit           | Consumer    | 1155.2      | 7            | 177.67       |
| Claire Gute            | Consumer    | 1148.78     | 3            | 169.93       |
| Kimberly Carter        | Corporate   | 1146.05     | 4            | 156.78       |
| Ross DeVincentis       | Home Office | 1137.62     | 8            | 318.46       |
| Carl Weiss             | Home Office | 1136.59     | 6            | 370.83       |
| Jim Sink               | Corporate   | 1131.06     | 4            | -54.87       |
| Darrin Van Huff        | Corporate   | 1119.48     | 5            | -427.18      |
| Alan Barnes            | Consumer    | 1113.84     | 8            | 220.81       |
| Tony Molinari          | Consumer    | 1094.68     | 3            | 292.52       |
| Jesus Ocampo           | Home Office | 1090.84     | 5            | 167.67       |
| Scot Wooten            | Consumer    | 1085.08     | 7            | -19.61       |
| Jeremy Farry           | Consumer    | 1082.92     | 11           | -18.07       |
| Dennis Bolton          | Home Office | 1081.47     | 5            | 291.01       |
| David Wiener           | Corporate   | 1080.75     | 6            | -86.87       |
| Cindy Schnelling       | Corporate   | 1077.23     | 4            | -302.88      |
| Pauline Chand          | Home Office | 1061.49     | 2            | -184.34      |
| David Philippe         | Consumer    | 1058.62     | 2            | -40.94       |
| Jenna Caffey           | Consumer    | 1058.11     | 1            | 502.92       |
| Phillina Ober          | Home Office | 1056.86     | 5            | -49.7        |
| Allen Armold           | Consumer    | 1056.39     | 9            | 277.38       |
| Vivek Sundaresam       | Consumer    | 1055.98     | 4            | -262.81      |
| Alex Russell           | Corporate   | 1055.69     | 4            | -221.05      |
| Darren Powers          | Consumer    | 1050.64     | 9            | 241.45       |
| Duane Huffman          | Home Office | 1043.1      | 4            | 116.67       |
| Susan MacKendrick      | Consumer    | 1043.04     | 1            | -237.29      |
| Eudokia Martin         | Corporate   | 1041.04     | 4            | 240.24       |
| Theresa Coyne          | Corporate   | 1038.26     | 1            | 265.53       |
| Mike Kennedy           | Consumer    | 1031.6      | 4            | 227.83       |
| Tiffany House          | Corporate   | 1022.2      | 8            | 92.73        |
| Sean Wendt             | Home Office | 1019.04     | 3            | 95.84        |
| Luke Schmidt           | Corporate   | 1010.26     | 6            | 244.2        |
| Randy Bradley          | Consumer    | 1008.2      | 2            | -164.41      |
| Lynn Smith             | Consumer    | 1008.14     | 6            | 348.36       |
| Bruce Geld             | Consumer    | 1006.36     | 6            | 119.35       |
| Victor Preis           | Home Office | 993.9       | 3            | 205.39       |
| Ken Brennan            | Corporate   | 983.92      | 7            | 293.55       |
| Barry Pond             | Corporate   | 983.42      | 5            | 209.78       |
| Toby Swindell          | Consumer    | 974.78      | 5            | -184.98      |
| Russell D'Ascenzo      | Consumer    | 970.94      | 4            | 35.06        |
| Aimee Bixby            | Consumer    | 966.71      | 5            | 313.66       |
| Roy Collins            | Consumer    | 966.41      | 6            | 63.99        |
| Sung Shariari          | Consumer    | 964.64      | 5            | -75.59       |
| Jonathan Howell        | Consumer    | 959.48      | 7            | -13.55       |
| Jason Fortune-         | Consumer    | 955.12      | 5            | 97.29        |
| Rachel Payne           | Corporate   | 954.65      | 4            | 59.54        |
| Bryan Spruell          | Home Office | 949.43      | 2            | 194.05       |
| Roy Französisch        | Consumer    | 945.22      | 8            | 280.03       |
| Eric Barreto           | Consumer    | 944.6       | 5            | 0.6          |
| Maureen Fritzler       | Corporate   | 937.04      | 5            | -341.53      |
| Eric Murdock           | Consumer    | 933.7       | 5            | 102.3        |
| Alyssa Crouse          | Corporate   | 925.8       | 3            | -62.13       |
| Evan Henry             | Consumer    | 923.88      | 6            | 242.11       |
| Mary O'Rourke          | Consumer    | 922.49      | 4            | 59.36        |
| Alejandro Ballentine   | Home Office | 914.53      | 9            | 264.57       |
| Katrina Bavinger       | Home Office | 908.82      | 3            | 274.3        |
| Catherine Glotzbach    | Home Office | 904.47      | 6            | 86.51        |
| Sonia Cooley           | Consumer    | 902.73      | 5            | 100.23       |
| Joni Blumstein         | Consumer    | 900.55      | 3            | -286.98      |
| Henia Zydlo            | Consumer    | 886.52      | 5            | -130.39      |
| Aaron Bergman          | Consumer    | 886.16      | 3            | 129.35       |
| Ryan Crowe             | Consumer    | 885.75      | 6            | 10.56        |
| Chad Sievert           | Consumer    | 884.64      | 4            | 143.83       |
| Harold Engle           | Corporate   | 883.53      | 4            | 274.4        |
| Sally Knutson          | Consumer    | 883.41      | 3            | 168.79       |
| Richard Eichhorn       | Consumer    | 876.7       | 5            | 209.23       |
| Jim Mitchum            | Corporate   | 864.95      | 5            | 117.2        |
| Jocasta Rupert         | Consumer    | 863.88      | 1            | 107.99       |
| Art Foster             | Consumer    | 861.57      | 4            | -163.12      |
| Julie Creighton        | Corporate   | 858.58      | 5            | 201.6        |
| Michael Stewart        | Corporate   | 855.12      | 6            | 55.23        |
| Vicky Freymann         | Home Office | 847.94      | 5            | -96.28       |
| Vivek Gonzalez         | Consumer    | 846.01      | 6            | 143.63       |
| Charles Sheldon        | Corporate   | 844.46      | 5            | 113.14       |
| Todd Boyes             | Corporate   | 834.33      | 5            | 268.97       |
| Ann Steele             | Home Office | 833.4       | 7            | 136.49       |
| Erica Hackney          | Consumer    | 825.95      | 6            | 150.38       |
| Thomas Brumley         | Home Office | 816.17      | 4            | 179.0        |
| Alice McCarthy         | Corporate   | 814.01      | 5            | 194.99       |
| Brendan Murry          | Corporate   | 808.16      | 6            | 95.58        |
| David Kendrick         | Corporate   | 797.83      | 2            | 249.94       |
| Matthew Clasen         | Corporate   | 795.15      | 4            | -247.94      |
| Beth Fritzler          | Corporate   | 791.99      | 3            | 25.87        |
| Harry Greene           | Consumer    | 785.63      | 5            | 147.0        |
| Michael Granlund       | Home Office | 776.38      | 9            | 171.74       |
| Muhammed MacIntyre     | Corporate   | 775.41      | 9            | 58.89        |
| Sandra Flanagan        | Consumer    | 763.55      | 7            | 228.16       |
| Steven Ward            | Corporate   | 758.7       | 2            | 68.24        |
| Liz Pelletier          | Consumer    | 756.61      | 4            | 110.78       |
| Dorris liebe           | Corporate   | 755.6       | 5            | 175.24       |
| Ivan Gibson            | Consumer    | 744.57      | 4            | 320.5        |
| Barry Blumstein        | Corporate   | 744.34      | 5            | 11.58        |
| Tracy Collins          | Home Office | 742.56      | 7            | 217.93       |
| Michelle Lonsdale      | Corporate   | 742.08      | 3            | 138.72       |
| Ritsa Hightower        | Consumer    | 740.38      | 2            | 0.31         |
| Patrick Bzostek        | Home Office | 740.36      | 3            | 229.23       |
| Angele Hood            | Consumer    | 738.5       | 4            | 83.96        |
| Henry MacAllister      | Consumer    | 736.28      | 4            | 117.28       |
| Patricia Hirasaki      | Home Office | 729.65      | 1            | 47.89        |
| Pete Armstrong         | Home Office | 729.41      | 6            | 225.86       |
| Jennifer Jackson       | Consumer    | 709.18      | 5            | 200.56       |
| Julia Dunbar           | Consumer    | 695.44      | 3            | 111.11       |
| Peter Bühler           | Consumer    | 688.32      | 4            | 218.16       |
| Eric Hoffmann          | Consumer    | 684.17      | 8            | 53.54        |
| Toby Ritter            | Consumer    | 675.94      | 5            | 220.36       |
| Alex Grayson           | Consumer    | 660.97      | 5            | -5.14        |
| Berenike Kampe         | Consumer    | 659.14      | 6            | -63.76       |
| Bryan Davis            | Consumer    | 658.47      | 6            | 141.26       |
| Anna Chung             | Consumer    | 657.32      | 5            | -28.7        |
| Anthony Witt           | Consumer    | 649.38      | 4            | 65.77        |
| Lori Olson             | Corporate   | 644.35      | 5            | 150.17       |
| Joy Bell-              | Consumer    | 644.12      | 7            | 126.76       |
| Carol Darley           | Consumer    | 639.77      | 3            | -206.72      |
| Mathew Reese           | Home Office | 639.18      | 4            | 162.94       |
| Astrea Jones           | Consumer    | 629.25      | 3            | 60.43        |
| Ralph Ritter           | Consumer    | 615.93      | 2            | -73.83       |
| Shirley Schmidt        | Home Office | 613.4       | 3            | 199.93       |
| Bobby Trafton          | Consumer    | 603.88      | 4            | -77.53       |
| Barbara Fisher         | Corporate   | 599.8       | 7            | 227.44       |
| Maria Zettner          | Home Office | 593.61      | 4            | 85.02        |
| Denise Leinenbach      | Consumer    | 585.02      | 4            | 222.68       |
| Alan Shonely           | Consumer    | 584.61      | 7            | 33.72        |
| Brian Derr             | Consumer    | 582.65      | 3            | 141.53       |
| Neil Knudson           | Home Office | 572.05      | 7            | 121.22       |
| Carlos Meador          | Consumer    | 565.39      | 2            | -43.73       |
| Chuck Sachs            | Consumer    | 550.64      | 2            | 156.26       |
| Cari Schnelling        | Consumer    | 537.63      | 6            | 105.83       |
| John Huston            | Consumer    | 528.91      | 6            | 26.08        |
| Rob Beeghly            | Consumer    | 528.55      | 5            | 76.89        |
| Andy Yotov             | Corporate   | 497.01      | 4            | 103.35       |
| Corey Roper            | Home Office | 475.9       | 3            | 144.76       |
| MaryBeth Skach         | Consumer    | 475.66      | 4            | 84.03        |
| Joni Sundaresam        | Home Office | 469.17      | 5            | -327.93      |
| Erin Creighton         | Consumer    | 461.91      | 5            | 96.43        |
| Khloe Miller           | Consumer    | 453.54      | 5            | 91.14        |
| Kelly Williams         | Consumer    | 449.1       | 4            | 107.93       |
| Tim Taslimi            | Corporate   | 439.5       | 3            | 93.92        |
| Shui Tom               | Consumer    | 433.34      | 7            | 84.44        |
| Vivek Grady            | Corporate   | 427.37      | 5            | -52.33       |
| Sonia Sunley           | Consumer    | 418.49      | 6            | 135.54       |
| Brad Thomas            | Home Office | 415.2       | 2            | 126.87       |
| Mark Haberlin          | Corporate   | 400.02      | 4            | 61.43        |
| Barry Weirich          | Consumer    | 385.52      | 3            | -58.29       |
| Joy Daniels            | Consumer    | 385.43      | 6            | 26.76        |
| Jason Klamczynski      | Corporate   | 383.81      | 3            | 55.33        |
| Vivian Mathis          | Consumer    | 380.69      | 5            | 116.64       |
| Neil Französisch       | Home Office | 377.16      | 4            | 85.93        |
| Melanie Seite          | Consumer    | 370.35      | 4            | 19.43        |
| Lycoris Saunders       | Consumer    | 368.88      | 3            | 39.2         |
| Aleksandra Gannaway    | Corporate   | 367.55      | 4            | 59.29        |
| Evan Minnotte          | Home Office | 366.82      | 3            | 21.77        |
| Heather Jas            | Home Office | 358.1       | 5            | 98.65        |
| Don Weiss              | Consumer    | 344.08      | 5            | 69.67        |
| Larry Tron             | Consumer    | 329.88      | 3            | 59.04        |
| Brendan Dodson         | Home Office | 320.54      | 2            | 116.71       |
| Lisa Hazard            | Consumer    | 318.24      | 4            | -242.74      |
| Jennifer Halladay      | Consumer    | 309.28      | 4            | -24.08       |
| Jill Matthias          | Consumer    | 303.95      | 5            | 113.12       |
| Chuck Magee            | Consumer    | 287.99      | 3            | 64.43        |
| Larry Hughes           | Consumer    | 287.43      | 3            | 12.63        |
| Sung Chung             | Consumer    | 280.63      | 2            | 31.18        |
| Stuart Calhoun         | Consumer    | 279.26      | 4            | 51.83        |
| Nicole Brennan         | Corporate   | 273.87      | 2            | 24.79        |
| Bart Folk              | Consumer    | 272.95      | 3            | 110.93       |
| Dorothy Dickinson      | Consumer    | 269.54      | 6            | 36.43        |
| Brad Norvell           | Corporate   | 265.3       | 4            | 36.61        |
| Andrew Roberts         | Consumer    | 264.86      | 5            | 43.67        |
| Harold Dahlen          | Home Office | 251.36      | 3            | -135.88      |
| Sally Matthias         | Consumer    | 244.49      | 4            | -26.59       |
| Paul Lucas             | Home Office | 239.48      | 5            | -0.75        |
| Guy Phonely            | Corporate   | 236.53      | 2            | 31.84        |
| Erin Mull              | Consumer    | 228.99      | 4            | 40.15        |
| Guy Thornton           | Consumer    | 226.44      | 4            | -6.14        |
| Robert Barroso         | Corporate   | 221.08      | 5            | 72.68        |
| Hilary Holden          | Corporate   | 218.67      | 2            | 86.73        |
| Allen Goldenen         | Consumer    | 200.95      | 5            | 69.28        |
| Joel Jenkins           | Home Office | 195.0       | 2            | 34.45        |
| Anthony Garverick      | Home Office | 170.58      | 4            | -8.43        |
| Muhammed Lee           | Consumer    | 162.23      | 2            | 42.66        |
| Anthony O'Donnell      | Corporate   | 161.28      | 1            | 12.1         |
| Pete Takahito          | Consumer    | 160.57      | 4            | -20.05       |
| Dianna Arnett          | Home Office | 156.76      | 4            | 56.79        |
| Michael Oakman         | Consumer    | 154.29      | 2            | -82.01       |
| Greg Hansen            | Consumer    | 146.94      | 2            | -5.81        |
| Phillip Breyer         | Corporate   | 132.74      | 2            | 21.9         |
| Bobby Odegard          | Consumer    | 130.83      | 2            | 59.45        |
| Ed Ludwig              | Home Office | 124.28      | 2            | 27.12        |
| Clay Cheatham          | Consumer    | 113.83      | 3            | 33.87        |
| Roland Murray          | Consumer    | 98.35       | 1            | 28.69        |
| Karen Seio             | Corporate   | 88.47       | 3            | 0.11         |
| Anemone Ratner         | Consumer    | 88.15       | 1            | 32.63        |
| Fred Wasserman         | Corporate   | 79.75       | 3            | 23.49        |
| Jasper Cacioppo        | Consumer    | 71.26       | 4            | -0.36        |
| Adrian Shami           | Home Office | 58.82       | 2            | 21.85        |
| Larry Blacks           | Consumer    | 50.19       | 3            | 18.65        |
| Ricardo Emerson        | Consumer    | 48.36       | 1            | 6.05         |
| Susan Gilcrest         | Corporate   | 47.95       | 3            | -3.71        |
| Roy Skaria             | Home Office | 22.33       | 2            | 9.58         |
| Mitch Gastineau        | Corporate   | 16.74       | 1            | -1.25        |
| Carl Jackson           | Corporate   | 16.52       | 1            | 1.65         |
| Lela Donovan           | Corporate   | 5.3         | 1            | 0.46         |
| Thais Sissman          | Consumer    | 4.83        | 2            | -3.32        |

### Query 12: Query 4: Customers who placed only a single order

```sql
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
ORDER BY c.customer_name
```

**Rows returned: 12**

| customer_name     | segment     | order_count |
|-------------------|-------------|-------------|
| Anemone Ratner    | Consumer    | 1           |
| Anthony O'Donnell | Corporate   | 1           |
| Carl Jackson      | Corporate   | 1           |
| Jenna Caffey      | Consumer    | 1           |
| Jocasta Rupert    | Consumer    | 1           |
| Lela Donovan      | Corporate   | 1           |
| Mitch Gastineau   | Corporate   | 1           |
| Patricia Hirasaki | Home Office | 1           |
| Ricardo Emerson   | Consumer    | 1           |
| Roland Murray     | Consumer    | 1           |
| Susan MacKendrick | Consumer    | 1           |
| Theresa Coyne     | Corporate   | 1           |


## Section 3 — Window Functions

### Query 13
```sql
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
ORDER BY region, row_num
```

**Rows returned: 20**

| region  | customer_name        | order_id       | sales    | row_num |
|---------|----------------------|----------------|----------|---------|
| Central | Tamara Chand         | CA-2016-118689 | 17499.95 | 1       |
| Central | Adrian Barton        | CA-2016-117121 | 9892.74  | 2       |
| Central | Sanjit Chand         | CA-2014-116904 | 9449.95  | 3       |
| Central | Becky Martin         | CA-2014-139892 | 8159.95  | 4       |
| Central | Andy Reiter          | CA-2017-138289 | 5443.96  | 5       |
| East    | Tom Ashbrook         | CA-2017-127180 | 11199.97 | 1       |
| East    | Hunter Lopez         | CA-2017-166709 | 10499.97 | 2       |
| East    | Bill Shonely         | US-2016-107440 | 9099.93  | 3       |
| East    | Christopher Conant   | CA-2016-143714 | 8399.98  | 4       |
| East    | Tom Boeckenhauer     | CA-2014-145541 | 6999.96  | 5       |
| South   | Sean Miller          | CA-2014-145317 | 22638.48 | 1       |
| South   | Sanjit Engle         | CA-2016-158841 | 8749.95  | 2       |
| South   | Grant Thornton       | US-2017-168116 | 7999.98  | 3       |
| South   | Christopher Martinez | CA-2015-145352 | 6354.95  | 4       |
| South   | Patrick O'Brill      | CA-2017-129021 | 4367.9   | 5       |
| West    | Raymond Buch         | CA-2017-140151 | 13999.96 | 1       |
| West    | Ken Lonsdale         | CA-2014-143917 | 8187.65  | 2       |
| West    | Jane Waco            | CA-2017-135909 | 5083.96  | 3       |
| West    | Edward Hooks         | CA-2016-136301 | 4912.59  | 4       |
| West    | Nick Crebassa        | CA-2017-149881 | 4799.98  | 5       |

### Query 14: Query 6: RANK — customers ranked by total sales (with ties handled)

```sql
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
LIMIT 20
```

**Rows returned: 20**

| sales_rank | dense_rank | customer_name      | segment     | total_sales |
|------------|------------|--------------------|-------------|-------------|
| 1          | 1          | Sean Miller        | Home Office | 25043.05    |
| 2          | 2          | Tamara Chand       | Corporate   | 19052.22    |
| 3          | 3          | Raymond Buch       | Consumer    | 15117.34    |
| 4          | 4          | Tom Ashbrook       | Home Office | 14595.62    |
| 5          | 5          | Adrian Barton      | Consumer    | 14473.57    |
| 6          | 6          | Ken Lonsdale       | Consumer    | 14175.23    |
| 7          | 7          | Sanjit Chand       | Consumer    | 14142.33    |
| 8          | 8          | Hunter Lopez       | Consumer    | 12873.3     |
| 9          | 9          | Sanjit Engle       | Consumer    | 12209.44    |
| 10         | 10         | Christopher Conant | Consumer    | 12129.07    |
| 11         | 11         | Todd Sumrall       | Corporate   | 11891.75    |
| 12         | 12         | Greg Tran          | Consumer    | 11820.12    |
| 13         | 13         | Becky Martin       | Consumer    | 11789.63    |
| 14         | 14         | Seth Vernon        | Consumer    | 11470.95    |
| 15         | 15         | Caroline Jumper    | Consumer    | 11164.97    |
| 16         | 16         | Clay Ludtke        | Consumer    | 10880.55    |
| 17         | 17         | Maria Etezadi      | Home Office | 10663.73    |
| 18         | 18         | Karen Ferguson     | Home Office | 10604.27    |
| 19         | 19         | Bill Shonely       | Corporate   | 10501.65    |
| 20         | 20         | Edward Hooks       | Corporate   | 10310.88    |

### Query 15: Query 7: Running total of sales per customer ordered by order date

```sql
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
LIMIT 30
```

**Rows returned: 30**

| customer_name   | order_date | order_id       | sale_amount | running_total |
|-----------------|------------|----------------|-------------|---------------|
| Aaron Bergman   | 2014-02-18 | CA-2014-152905 | 12.62       | 12.62         |
| Aaron Bergman   | 2014-03-07 | CA-2014-156587 | 17.94       | 79.27         |
| Aaron Bergman   | 2014-03-07 | CA-2014-156587 | 242.94      | 322.21        |
| Aaron Bergman   | 2014-03-07 | CA-2014-156587 | 48.71       | 61.33         |
| Aaron Bergman   | 2016-11-10 | CA-2016-140935 | 341.96      | 886.15        |
| Aaron Bergman   | 2016-11-10 | CA-2016-140935 | 221.98      | 544.19        |
| Aaron Hawkins   | 2014-04-22 | CA-2014-122070 | 247.84      | 257.75        |
| Aaron Hawkins   | 2014-04-22 | CA-2014-122070 | 9.91        | 9.91          |
| Aaron Hawkins   | 2014-05-13 | CA-2014-113768 | 279.46      | 545.21        |
| Aaron Hawkins   | 2014-05-13 | CA-2014-113768 | 8.0         | 265.75        |
| Aaron Hawkins   | 2014-10-25 | US-2014-158400 | 49.41       | 594.62        |
| Aaron Hawkins   | 2014-12-31 | CA-2014-157644 | 18.9        | 613.52        |
| Aaron Hawkins   | 2014-12-31 | CA-2014-157644 | 34.77       | 648.29        |
| Aaron Hawkins   | 2015-12-27 | CA-2015-130113 | 668.16      | 1316.45       |
| Aaron Hawkins   | 2015-12-27 | CA-2015-130113 | 323.1       | 1639.55       |
| Aaron Hawkins   | 2016-03-20 | CA-2016-162747 | 86.45       | 1726.0        |
| Aaron Hawkins   | 2017-12-18 | CA-2017-164000 | 18.7        | 1744.7        |
| Aaron Smayling  | 2014-07-27 | US-2014-150126 | 65.78       | 65.78         |
| Aaron Smayling  | 2016-03-28 | CA-2016-162901 | 31.4        | 97.18         |
| Aaron Smayling  | 2016-09-25 | CA-2016-148747 | 477.67      | 574.85        |
| Aaron Smayling  | 2017-01-02 | CA-2017-113481 | 695.7       | 1270.55       |
| Aaron Smayling  | 2017-01-02 | CA-2017-113481 | 15.66       | 1286.21       |
| Aaron Smayling  | 2017-01-02 | CA-2017-113481 | 28.85       | 1315.06       |
| Aaron Smayling  | 2017-08-01 | CA-2017-162691 | 36.29       | 1351.35       |
| Aaron Smayling  | 2017-08-01 | CA-2017-162691 | 1439.98     | 2791.33       |
| Aaron Smayling  | 2017-09-04 | US-2017-147655 | 88.07       | 2879.4        |
| Aaron Smayling  | 2017-10-03 | CA-2017-101749 | 171.29      | 3050.69       |
| Adam Bellavance | 2015-09-18 | CA-2015-150511 | 18.54       | 18.54         |
| Adam Bellavance | 2016-03-13 | US-2016-108637 | 160.32      | 178.86        |
| Adam Bellavance | 2016-03-13 | US-2016-108637 | 127.88      | 306.74        |


## Section 4 — Business Queries

### Query 16
```sql
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
LIMIT 10
```

**Rows returned: 10**

| customer_name      | segment     | total_sales | total_profit | total_orders |
|--------------------|-------------|-------------|--------------|--------------|
| Sean Miller        | Home Office | 25043.05    | -1980.74     | 5            |
| Tamara Chand       | Corporate   | 19052.22    | 8981.32      | 5            |
| Raymond Buch       | Consumer    | 15117.34    | 6976.1       | 6            |
| Tom Ashbrook       | Home Office | 14595.62    | 4703.79      | 4            |
| Adrian Barton      | Consumer    | 14473.57    | 5444.81      | 10           |
| Ken Lonsdale       | Consumer    | 14175.23    | 806.86       | 12           |
| Sanjit Chand       | Consumer    | 14142.33    | 5757.41      | 9            |
| Hunter Lopez       | Consumer    | 12873.3     | 5622.43      | 6            |
| Sanjit Engle       | Consumer    | 12209.44    | 2650.68      | 11           |
| Christopher Conant | Consumer    | 12129.07    | 2177.05      | 5            |

### Query 17: Query 9: Bottom 10 customers by total sales

```sql
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
LIMIT 10
```

**Rows returned: 10**

| customer_name   | segment     | total_sales |
|-----------------|-------------|-------------|
| Thais Sissman   | Consumer    | 4.83        |
| Lela Donovan    | Corporate   | 5.3         |
| Carl Jackson    | Corporate   | 16.52       |
| Mitch Gastineau | Corporate   | 16.74       |
| Roy Skaria      | Home Office | 22.33       |
| Susan Gilcrest  | Corporate   | 47.95       |
| Ricardo Emerson | Consumer    | 48.36       |
| Larry Blacks    | Consumer    | 50.19       |
| Adrian Shami    | Home Office | 58.82       |
| Jasper Cacioppo | Consumer    | 71.26       |

### Query 18: Query 10: Customers with above-average total sales (CTE + subquery combo)

```sql
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
ORDER BY cs.total_sales DESC
```

**Rows returned: 294**

| customer_name        | segment     | total_sales | average_across_all_customers |
|----------------------|-------------|-------------|------------------------------|
| Sean Miller          | Home Office | 25043.05    | 2896.85                      |
| Tamara Chand         | Corporate   | 19052.22    | 2896.85                      |
| Raymond Buch         | Consumer    | 15117.34    | 2896.85                      |
| Tom Ashbrook         | Home Office | 14595.62    | 2896.85                      |
| Adrian Barton        | Consumer    | 14473.57    | 2896.85                      |
| Ken Lonsdale         | Consumer    | 14175.23    | 2896.85                      |
| Sanjit Chand         | Consumer    | 14142.33    | 2896.85                      |
| Hunter Lopez         | Consumer    | 12873.3     | 2896.85                      |
| Sanjit Engle         | Consumer    | 12209.44    | 2896.85                      |
| Christopher Conant   | Consumer    | 12129.07    | 2896.85                      |
| Todd Sumrall         | Corporate   | 11891.75    | 2896.85                      |
| Greg Tran            | Consumer    | 11820.12    | 2896.85                      |
| Becky Martin         | Consumer    | 11789.63    | 2896.85                      |
| Seth Vernon          | Consumer    | 11470.95    | 2896.85                      |
| Caroline Jumper      | Consumer    | 11164.97    | 2896.85                      |
| Clay Ludtke          | Consumer    | 10880.55    | 2896.85                      |
| Maria Etezadi        | Home Office | 10663.73    | 2896.85                      |
| Karen Ferguson       | Home Office | 10604.27    | 2896.85                      |
| Bill Shonely         | Corporate   | 10501.65    | 2896.85                      |
| Edward Hooks         | Corporate   | 10310.88    | 2896.85                      |
| John Lee             | Consumer    | 9799.92     | 2896.85                      |
| Grant Thornton       | Corporate   | 9351.21     | 2896.85                      |
| Helen Wasserman      | Corporate   | 9300.25     | 2896.85                      |
| Tom Boeckenhauer     | Consumer    | 9133.99     | 2896.85                      |
| Peter Fuller         | Consumer    | 9062.86     | 2896.85                      |
| Christopher Martinez | Consumer    | 8954.02     | 2896.85                      |
| Justin Deggeller     | Corporate   | 8828.03     | 2896.85                      |
| Joe Elijah           | Consumer    | 8697.84     | 2896.85                      |
| Laura Armstrong      | Corporate   | 8673.22     | 2896.85                      |
| Pete Kriz            | Consumer    | 8646.93     | 2896.85                      |
| Daniel Raglin        | Home Office | 8350.87     | 2896.85                      |
| Natalie Fritzler     | Consumer    | 8322.83     | 2896.85                      |
| Karen Daniels        | Consumer    | 8282.36     | 2896.85                      |
| Nick Crebassa        | Corporate   | 8241.74     | 2896.85                      |
| Harry Marie          | Corporate   | 8236.76     | 2896.85                      |
| Keith Dawkins        | Corporate   | 8181.26     | 2896.85                      |
| Sean Braxton         | Corporate   | 8057.89     | 2896.85                      |
| Zuschuss Carroll     | Consumer    | 8025.71     | 2896.85                      |
| Joseph Holt          | Consumer    | 7955.0      | 2896.85                      |
| Nora Preis           | Consumer    | 7903.18     | 2896.85                      |
| Anna Häberlin        | Corporate   | 7888.29     | 2896.85                      |
| Adam Bellavance      | Home Office | 7755.62     | 2896.85                      |
| Jim Epp              | Corporate   | 7754.98     | 2896.85                      |
| Jane Waco            | Corporate   | 7721.71     | 2896.85                      |
| Lena Creighton       | Consumer    | 7663.13     | 2896.85                      |
| John Murray          | Consumer    | 7625.08     | 2896.85                      |
| Jonathan Doherty     | Corporate   | 7610.86     | 2896.85                      |
| Patrick O'Brill      | Consumer    | 7473.83     | 2896.85                      |
| Maribeth Schnelling  | Consumer    | 7443.69     | 2896.85                      |
| Rick Wilson          | Corporate   | 7397.4      | 2896.85                      |
| Brian Moss           | Corporate   | 7294.19     | 2896.85                      |
| Paul Prost           | Home Office | 7252.61     | 2896.85                      |
| Natalie Webber       | Consumer    | 7234.01     | 2896.85                      |
| Dean percer          | Home Office | 7198.76     | 2896.85                      |
| Fred Hopkins         | Corporate   | 6987.2      | 2896.85                      |
| Rick Huthwaite       | Home Office | 6979.18     | 2896.85                      |
| Penelope Sewall      | Home Office | 6843.63     | 2896.85                      |
| Brenda Bowman        | Corporate   | 6765.73     | 2896.85                      |
| Joel Eaton           | Consumer    | 6760.81     | 2896.85                      |
| Yana Sorensen        | Corporate   | 6720.44     | 2896.85                      |
| Andy Reiter          | Consumer    | 6608.45     | 2896.85                      |
| Dan Reichenbach      | Corporate   | 6528.03     | 2896.85                      |
| Grace Kelly          | Corporate   | 6497.27     | 2896.85                      |
| Joseph Airdo         | Consumer    | 6491.03     | 2896.85                      |
| Nathan Mautz         | Home Office | 6459.34     | 2896.85                      |
| Valerie Dominguez    | Consumer    | 6442.25     | 2896.85                      |
| Sarah Brown          | Consumer    | 6411.0      | 2896.85                      |
| James Galang         | Consumer    | 6366.39     | 2896.85                      |
| Darrin Martin        | Consumer    | 6345.1      | 2896.85                      |
| Corinna Mitchell     | Home Office | 6339.56     | 2896.85                      |
| Max Jones            | Consumer    | 6320.75     | 2896.85                      |
| Brosina Hoffman      | Consumer    | 6255.35     | 2896.85                      |
| Rob Lucas            | Consumer    | 6234.91     | 2896.85                      |
| William Brown        | Consumer    | 6160.1      | 2896.85                      |
| Victoria Wilson      | Corporate   | 6134.04     | 2896.85                      |
| Shirley Daniels      | Home Office | 6121.11     | 2896.85                      |
| Quincy Jones         | Corporate   | 6108.34     | 2896.85                      |
| Alan Dominguez       | Home Office | 6106.88     | 2896.85                      |
| Cassandra Brandow    | Consumer    | 6076.14     | 2896.85                      |
| Greg Maxwell         | Corporate   | 6049.97     | 2896.85                      |
| Shahid Collister     | Consumer    | 5992.54     | 2896.85                      |
| Kristen Hastings     | Corporate   | 5990.8      | 2896.85                      |
| Robert Marley        | Home Office | 5979.1      | 2896.85                      |
| Keith Herrera        | Consumer    | 5952.86     | 2896.85                      |
| Ben Ferrer           | Home Office | 5907.97     | 2896.85                      |
| Christine Phan       | Corporate   | 5888.28     | 2896.85                      |
| Bill Donatelli       | Consumer    | 5718.52     | 2896.85                      |
| Cindy Stewart        | Consumer    | 5690.05     | 2896.85                      |
| Anne McFarland       | Consumer    | 5664.02     | 2896.85                      |
| Ross Baird           | Home Office | 5633.32     | 2896.85                      |
| Katherine Murray     | Home Office | 5620.19     | 2896.85                      |
| Alex Avila           | Consumer    | 5563.56     | 2896.85                      |
| Suzanne McNair       | Corporate   | 5563.39     | 2896.85                      |
| Naresj Patel         | Consumer    | 5529.62     | 2896.85                      |
| Amy Cox              | Consumer    | 5527.85     | 2896.85                      |
| Mick Hernandez       | Home Office | 5503.09     | 2896.85                      |
| Dennis Pardue        | Home Office | 5480.72     | 2896.85                      |
| Emily Phan           | Consumer    | 5478.06     | 2896.85                      |
| Yoseph Carroll       | Corporate   | 5454.35     | 2896.85                      |
| Stefania Perrino     | Corporate   | 5440.32     | 2896.85                      |
| Luke Weiss           | Consumer    | 5420.51     | 2896.85                      |
| Cathy Prescott       | Corporate   | 5402.25     | 2896.85                      |
| Thomas Seio          | Corporate   | 5371.09     | 2896.85                      |
| Tonja Turnell        | Home Office | 5364.81     | 2896.85                      |
| Mitch Webber         | Consumer    | 5341.9      | 2896.85                      |
| Tom Prescott         | Consumer    | 5329.0      | 2896.85                      |
| Tamara Willingham    | Home Office | 5278.83     | 2896.85                      |
| Dianna Wilson        | Home Office | 5271.63     | 2896.85                      |
| Mitch Willingham     | Corporate   | 5253.88     | 2896.85                      |
| Harold Ryan          | Corporate   | 5248.79     | 2896.85                      |
| Steven Cartwright    | Consumer    | 5226.21     | 2896.85                      |
| Resi Pölking         | Consumer    | 5153.08     | 2896.85                      |
| Lena Radford         | Consumer    | 5142.89     | 2896.85                      |
| Mike Pelletier       | Home Office | 5087.92     | 2896.85                      |
| Anna Andreadi        | Consumer    | 5086.94     | 2896.85                      |
| Ivan Liston          | Consumer    | 5040.74     | 2896.85                      |
| Kelly Lampkin        | Corporate   | 5016.49     | 2896.85                      |
| Laurel Beltran       | Home Office | 4985.68     | 2896.85                      |
| Dave Hallsten        | Corporate   | 4932.87     | 2896.85                      |
| Irene Maddox         | Consumer    | 4930.47     | 2896.85                      |
| Ted Trevino          | Consumer    | 4915.6      | 2896.85                      |
| Kunst Miller         | Consumer    | 4909.47     | 2896.85                      |
| Philisse Overcash    | Home Office | 4893.04     | 2896.85                      |
| Heather Kirkland     | Corporate   | 4877.78     | 2896.85                      |
| Anthony Jacobs       | Corporate   | 4867.34     | 2896.85                      |
| Joe Kamberova        | Consumer    | 4867.2      | 2896.85                      |
| Alan Hwang           | Consumer    | 4805.34     | 2896.85                      |
| Dean Katz            | Corporate   | 4802.39     | 2896.85                      |
| Russell Applegate    | Consumer    | 4793.54     | 2896.85                      |
| Sue Ann Reed         | Consumer    | 4767.34     | 2896.85                      |
| Jim Kriz             | Home Office | 4760.43     | 2896.85                      |
| Bart Watters         | Corporate   | 4750.36     | 2896.85                      |
| Tracy Blumstein      | Consumer    | 4737.49     | 2896.85                      |
| Giulietta Baptist    | Consumer    | 4716.29     | 2896.85                      |
| Rick Bensley         | Home Office | 4715.47     | 2896.85                      |
| Erin Smith           | Corporate   | 4657.92     | 2896.85                      |
| Deborah Brumfield    | Home Office | 4655.9      | 2896.85                      |
| Kean Thornton        | Consumer    | 4642.09     | 2896.85                      |
| Sample Company A     | Home Office | 4624.57     | 2896.85                      |
| Eugene Moren         | Home Office | 4588.44     | 2896.85                      |
| Dave Brooks          | Consumer    | 4531.65     | 2896.85                      |
| Anthony Rawles       | Corporate   | 4523.34     | 2896.85                      |
| Arthur Gainer        | Consumer    | 4510.8      | 2896.85                      |
| Anthony Johnson      | Corporate   | 4501.39     | 2896.85                      |
| Linda Cazamias       | Corporate   | 4492.95     | 2896.85                      |
| Stewart Carmichael   | Corporate   | 4492.66     | 2896.85                      |
| Theone Pippenger     | Consumer    | 4454.06     | 2896.85                      |
| Mark Cousins         | Corporate   | 4432.14     | 2896.85                      |
| Jamie Kunitz         | Consumer    | 4427.14     | 2896.85                      |
| Katrina Willman      | Consumer    | 4416.52     | 2896.85                      |
| Bradley Drucker      | Consumer    | 4411.24     | 2896.85                      |
| Arianne Irving       | Consumer    | 4375.79     | 2896.85                      |
| Scot Coram           | Corporate   | 4371.96     | 2896.85                      |
| Ellis Ballard        | Corporate   | 4358.13     | 2896.85                      |
| Gary Zandusky        | Consumer    | 4355.15     | 2896.85                      |
| Steven Roelle        | Home Office | 4345.89     | 2896.85                      |
| Natalie DeCherney    | Consumer    | 4326.14     | 2896.85                      |
| Matt Abelman         | Home Office | 4299.16     | 2896.85                      |
| Sung Pak             | Corporate   | 4282.94     | 2896.85                      |
| Dana Kaydos          | Consumer    | 4282.18     | 2896.85                      |
| Rick Duston          | Consumer    | 4272.93     | 2896.85                      |
| Toby Carlisle        | Consumer    | 4266.81     | 2896.85                      |
| Alan Schoenberger    | Corporate   | 4260.78     | 2896.85                      |
| Frank Hawley         | Corporate   | 4256.27     | 2896.85                      |
| Claudia Bergmann     | Corporate   | 4246.46     | 2896.85                      |
| Tracy Hopkins        | Home Office | 4234.1      | 2896.85                      |
| Bill Eplett          | Home Office | 4204.68     | 2896.85                      |
| Jill Fjeld           | Consumer    | 4198.33     | 2896.85                      |
| Gary Hwang           | Consumer    | 4172.85     | 2896.85                      |
| Roland Schwarz       | Corporate   | 4159.77     | 2896.85                      |
| Muhammed Yedwab      | Corporate   | 4152.7      | 2896.85                      |
| Peter McVee          | Home Office | 4115.66     | 2896.85                      |
| Stewart Visinsky     | Consumer    | 4105.31     | 2896.85                      |
| Denise Monton        | Corporate   | 4074.47     | 2896.85                      |
| Frank Preis          | Consumer    | 4046.75     | 2896.85                      |
| Susan Pistek         | Consumer    | 3990.69     | 2896.85                      |
| Craig Molinari       | Corporate   | 3984.45     | 2896.85                      |
| Michael Paige        | Corporate   | 3983.64     | 2896.85                      |
| Sean Christensen     | Consumer    | 3979.06     | 2896.85                      |
| Sanjit Jacobs        | Home Office | 3949.66     | 2896.85                      |
| Luke Foster          | Consumer    | 3930.51     | 2896.85                      |
| Pierre Wener         | Consumer    | 3922.41     | 2896.85                      |
| George Ashbrook      | Consumer    | 3919.78     | 2896.85                      |
| Ken Heidel           | Corporate   | 3918.97     | 2896.85                      |
| Chris Cortes         | Consumer    | 3913.42     | 2896.85                      |
| Dorothy Badders      | Corporate   | 3908.8      | 2896.85                      |
| Nora Paige           | Consumer    | 3908.4      | 2896.85                      |
| Kelly Collister      | Consumer    | 3908.26     | 2896.85                      |
| Fred Chung           | Corporate   | 3889.37     | 2896.85                      |
| Bill Stewart         | Corporate   | 3887.83     | 2896.85                      |
| John Stevenson       | Consumer    | 3868.02     | 2896.85                      |
| Ruben Ausman         | Corporate   | 3832.31     | 2896.85                      |
| Annie Thurman        | Consumer    | 3831.86     | 2896.85                      |
| Olvera Toch          | Consumer    | 3818.62     | 2896.85                      |
| Rose O'Brian         | Consumer    | 3815.48     | 2896.85                      |
| Michael Chen         | Consumer    | 3805.71     | 2896.85                      |
| Michael Moore        | Consumer    | 3794.08     | 2896.85                      |
| Carol Adams          | Corporate   | 3789.72     | 2896.85                      |
| Matthew Grinstein    | Home Office | 3785.28     | 2896.85                      |
| Maribeth Dona        | Consumer    | 3766.38     | 2896.85                      |
| Jim Karlsson         | Consumer    | 3760.03     | 2896.85                      |
| Juliana Krohn        | Consumer    | 3747.67     | 2896.85                      |
| Frank Merwin         | Home Office | 3736.2      | 2896.85                      |
| Scott Cohen          | Corporate   | 3729.79     | 2896.85                      |
| Hunter Glantz        | Consumer    | 3690.28     | 2896.85                      |
| Ben Peterman         | Corporate   | 3675.86     | 2896.85                      |
| Liz Preis            | Consumer    | 3653.4      | 2896.85                      |
| Christopher Schild   | Home Office | 3651.86     | 2896.85                      |
| Ed Braxton           | Corporate   | 3644.98     | 2896.85                      |
| Jeremy Pistek        | Consumer    | 3635.59     | 2896.85                      |
| Sam Zeldin           | Home Office | 3625.33     | 2896.85                      |
| Rick Hansen          | Consumer    | 3621.38     | 2896.85                      |
| Thomas Boland        | Corporate   | 3589.3      | 2896.85                      |
| Gary McGarr          | Consumer    | 3582.82     | 2896.85                      |
| Dionis Lloyd         | Corporate   | 3539.32     | 2896.85                      |
| Erica Smith          | Consumer    | 3510.46     | 2896.85                      |
| Robert Waldorf       | Consumer    | 3495.65     | 2896.85                      |
| Anna Gayman          | Consumer    | 3489.04     | 2896.85                      |
| Emily Ducich         | Home Office | 3484.92     | 2896.85                      |
| Pauline Webber       | Corporate   | 3454.92     | 2896.85                      |
| Sarah Foster         | Consumer    | 3422.79     | 2896.85                      |
| Frank Carlisle       | Home Office | 3418.74     | 2896.85                      |
| Sally Hughsby        | Corporate   | 3406.84     | 2896.85                      |
| Sandra Glassco       | Consumer    | 3406.58     | 2896.85                      |
| Trudy Schmidt        | Consumer    | 3368.09     | 2896.85                      |
| Sam Craven           | Consumer    | 3362.96     | 2896.85                      |
| Victoria Pisteka     | Corporate   | 3360.53     | 2896.85                      |
| Doug Jacobs          | Consumer    | 3356.4      | 2896.85                      |
| Dianna Vittorini     | Consumer    | 3341.59     | 2896.85                      |
| Sylvia Foulston      | Corporate   | 3336.54     | 2896.85                      |
| Dan Campbell         | Consumer    | 3336.17     | 2896.85                      |
| Arthur Prichep       | Consumer    | 3323.56     | 2896.85                      |
| Dennis Kane          | Consumer    | 3318.49     | 2896.85                      |
| Katharine Harms      | Corporate   | 3312.86     | 2896.85                      |
| Randy Ferguson       | Corporate   | 3309.15     | 2896.85                      |
| Rick Reed            | Corporate   | 3302.26     | 2896.85                      |
| Brian Dahlen         | Consumer    | 3288.47     | 2896.85                      |
| Brian Stugart        | Consumer    | 3288.11     | 2896.85                      |
| Rob Williams         | Corporate   | 3279.75     | 2896.85                      |
| Daniel Lacy          | Consumer    | 3272.2      | 2896.85                      |
| Damala Kotsonis      | Corporate   | 3256.48     | 2896.85                      |
| Adam Shillingsburg   | Consumer    | 3255.31     | 2896.85                      |
| Jack O'Briant        | Corporate   | 3254.95     | 2896.85                      |
| Adam Hart            | Corporate   | 3250.34     | 2896.85                      |
| Henry Goldwyn        | Corporate   | 3247.64     | 2896.85                      |
| Lindsay Castell      | Home Office | 3246.63     | 2896.85                      |
| Carol Triggs         | Consumer    | 3241.9      | 2896.85                      |
| Edward Becker        | Corporate   | 3236.31     | 2896.85                      |
| Sharelle Roach       | Home Office | 3233.48     | 2896.85                      |
| Lindsay Williams     | Corporate   | 3230.31     | 2896.85                      |
| Ricardo Sperren      | Corporate   | 3221.29     | 2896.85                      |
| Alejandro Savely     | Corporate   | 3214.24     | 2896.85                      |
| Mark Packer          | Home Office | 3206.13     | 2896.85                      |
| Christine Sundaresam | Consumer    | 3202.16     | 2896.85                      |
| Brian Thompson       | Consumer    | 3196.75     | 2896.85                      |
| Deirdre Greer        | Corporate   | 3195.82     | 2896.85                      |
| Jeremy Lonsdale      | Consumer    | 3173.87     | 2896.85                      |
| Greg Matthias        | Consumer    | 3163.63     | 2896.85                      |
| Janet Martin         | Consumer    | 3159.12     | 2896.85                      |
| Chloris Kastensmidt  | Consumer    | 3154.86     | 2896.85                      |
| Karen Bern           | Corporate   | 3152.62     | 2896.85                      |
| Maxwell Schwartz     | Consumer    | 3144.68     | 2896.85                      |
| Ruben Dartt          | Consumer    | 3133.92     | 2896.85                      |
| Tanja Norvell        | Home Office | 3130.22     | 2896.85                      |
| Steve Nguyen         | Home Office | 3127.96     | 2896.85                      |
| Speros Goranitis     | Consumer    | 3124.83     | 2896.85                      |
| Katherine Hughes     | Consumer    | 3100.61     | 2896.85                      |
| Patrick Gardner      | Consumer    | 3086.91     | 2896.85                      |
| Eugene Hildebrand    | Home Office | 3082.65     | 2896.85                      |
| Gary Mitchum         | Home Office | 3078.62     | 2896.85                      |
| Eugene Barchas       | Consumer    | 3071.13     | 2896.85                      |
| Mike Gockenbach      | Consumer    | 3061.54     | 2896.85                      |
| Toby Gnade           | Consumer    | 3058.37     | 2896.85                      |
| Kean Takahito        | Consumer    | 3057.1      | 2896.85                      |
| Shahid Shariari      | Consumer    | 3056.81     | 2896.85                      |
| Sara Luxemburg       | Home Office | 3053.01     | 2896.85                      |
| Aaron Smayling       | Corporate   | 3050.69     | 2896.85                      |
| Cynthia Arntzen      | Consumer    | 3041.57     | 2896.85                      |
| Carlos Soltero       | Consumer    | 3036.55     | 2896.85                      |
| Lindsay Shagiari     | Home Office | 2988.67     | 2896.85                      |
| Michelle Huthwaite   | Consumer    | 2984.95     | 2896.85                      |
| Frank Atkinson       | Corporate   | 2984.05     | 2896.85                      |
| David Bremer         | Corporate   | 2973.09     | 2896.85                      |
| Noel Staavos         | Corporate   | 2964.82     | 2896.85                      |
| Tamara Manning       | Consumer    | 2955.23     | 2896.85                      |
| Christine Kargatis   | Home Office | 2945.32     | 2896.85                      |
| Thea Hudgings        | Corporate   | 2942.77     | 2896.85                      |
| Liz Thompson         | Consumer    | 2936.25     | 2896.85                      |
| Becky Castell        | Home Office | 2933.68     | 2896.85                      |
| Julie Kriz           | Home Office | 2932.48     | 2896.85                      |
| Shaun Weien          | Consumer    | 2921.54     | 2896.85                      |
| Maris LaWare         | Consumer    | 2921.5      | 2896.85                      |
| Rob Dowd             | Consumer    | 2912.89     | 2896.85                      |
| Craig Yedwab         | Corporate   | 2900.03     | 2896.85                      |

### Query 19: Query 11: Sales performance by category and region

```sql
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
ORDER BY o.region, total_sales DESC
```

**Rows returned: 12**

| region  | category        | total_sales | total_profit | avg_discount_pct | num_orders |
|---------|-----------------|-------------|--------------|------------------|------------|
| Central | Technology      | 177265.23   | 35264.09     | 13.2             | 356        |
| Central | Office Supplies | 171672.2    | 8407.84      | 25.2             | 880        |
| Central | Furniture       | 164908.0    | -3051.92     | 29.9             | 403        |
| East    | Technology      | 279341.27   | 48099.72     | 14.6             | 443        |
| East    | Furniture       | 218985.03   | 3759.31      | 15.1             | 488        |
| East    | Office Supplies | 209629.39   | 42104.76     | 14.2             | 1074       |
| South   | Technology      | 154972.35   | 20810.75     | 10.8             | 255        |
| South   | Office Supplies | 128212.14   | 20754.12     | 16.8             | 619        |
| South   | Furniture       | 119349.73   | 7041.38      | 12.1             | 278        |
| West    | Technology      | 282054.43   | 49241.14     | 13.4             | 490        |
| West    | Furniture       | 261041.89   | 12350.11     | 12.9             | 595        |
| West    | Office Supplies | 227234.87   | 54846.62     | 9.3              | 1169       |


## Final Query — Customer Name + Total Sales + Rank

### Query 20
```sql
WITH customer_sales AS (
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
ORDER BY rank
```

**Rows returned: 793**

| rank | dense_rank | customer_name          | segment     | total_sales | total_orders | total_profit | avg_discount_pct | sales_tier    |
|------|------------|------------------------|-------------|-------------|--------------|--------------|------------------|---------------|
| 1    | 1          | Sean Miller            | Home Office | 25043.05    | 5            | -1980.74     | 24.7             | Top 25%       |
| 2    | 2          | Tamara Chand           | Corporate   | 19052.22    | 5            | 8981.32      | 11.7             | Top 25%       |
| 3    | 3          | Raymond Buch           | Consumer    | 15117.34    | 6            | 6976.1       | 9.4              | Top 25%       |
| 4    | 4          | Tom Ashbrook           | Home Office | 14595.62    | 4            | 4703.79      | 8.0              | Top 25%       |
| 5    | 5          | Adrian Barton          | Consumer    | 14473.57    | 10           | 5444.81      | 24.0             | Top 25%       |
| 6    | 6          | Ken Lonsdale           | Consumer    | 14175.23    | 12           | 806.86       | 20.0             | Top 25%       |
| 7    | 7          | Sanjit Chand           | Consumer    | 14142.33    | 9            | 5757.41      | 6.4              | Top 25%       |
| 8    | 8          | Hunter Lopez           | Consumer    | 12873.3     | 6            | 5622.43      | 1.8              | Top 25%       |
| 9    | 9          | Sanjit Engle           | Consumer    | 12209.44    | 11           | 2650.68      | 11.1             | Top 25%       |
| 10   | 10         | Christopher Conant     | Consumer    | 12129.07    | 5            | 2177.05      | 28.2             | Top 25%       |
| 11   | 11         | Todd Sumrall           | Corporate   | 11891.75    | 6            | 2371.71      | 11.7             | Top 25%       |
| 12   | 12         | Greg Tran              | Consumer    | 11820.12    | 11           | 2163.43      | 10.0             | Top 25%       |
| 13   | 13         | Becky Martin           | Consumer    | 11789.63    | 4            | -1659.96     | 16.9             | Top 25%       |
| 14   | 14         | Seth Vernon            | Consumer    | 11470.95    | 10           | 1199.42      | 15.6             | Top 25%       |
| 15   | 15         | Caroline Jumper        | Consumer    | 11164.97    | 8            | 858.74       | 18.9             | Top 25%       |
| 16   | 16         | Clay Ludtke            | Consumer    | 10880.55    | 12           | 1933.78      | 11.4             | Top 25%       |
| 17   | 17         | Maria Etezadi          | Home Office | 10663.73    | 10           | 1859.47      | 13.2             | Top 25%       |
| 18   | 18         | Karen Ferguson         | Home Office | 10604.27    | 7            | 1660.14      | 3.3              | Top 25%       |
| 19   | 19         | Bill Shonely           | Corporate   | 10501.65    | 5            | 2616.06      | 1.1              | Top 25%       |
| 20   | 20         | Edward Hooks           | Corporate   | 10310.88    | 12           | 1393.52      | 7.2              | Top 25%       |
| 21   | 21         | John Lee               | Consumer    | 9799.92     | 11           | 228.91       | 8.8              | Top 25%       |
| 22   | 22         | Grant Thornton         | Corporate   | 9351.21     | 3            | -4108.66     | 25.0             | Top 25%       |
| 23   | 23         | Helen Wasserman        | Corporate   | 9300.25     | 8            | 2164.16      | 4.5              | Top 25%       |
| 24   | 24         | Tom Boeckenhauer       | Consumer    | 9133.99     | 7            | 2798.37      | 7.1              | Top 25%       |
| 25   | 25         | Peter Fuller           | Consumer    | 9062.86     | 4            | -614.29      | 12.1             | Top 25%       |
| 26   | 26         | Christopher Martinez   | Consumer    | 8954.02     | 4            | 3899.89      | 12.0             | Top 25%       |
| 27   | 27         | Justin Deggeller       | Corporate   | 8828.03     | 8            | 1619.52      | 5.6              | Top 25%       |
| 28   | 28         | Joe Elijah             | Consumer    | 8697.84     | 10           | 1262.29      | 32.3             | Top 25%       |
| 29   | 29         | Laura Armstrong        | Corporate   | 8673.22     | 11           | 2059.12      | 11.5             | Top 25%       |
| 30   | 30         | Pete Kriz              | Consumer    | 8646.93     | 12           | 2038.27      | 7.6              | Top 25%       |
| 31   | 31         | Daniel Raglin          | Home Office | 8350.87     | 8            | 2869.08      | 15.4             | Top 25%       |
| 32   | 32         | Natalie Fritzler       | Consumer    | 8322.83     | 7            | -1695.97     | 25.0             | Top 25%       |
| 33   | 33         | Karen Daniels          | Consumer    | 8282.36     | 5            | 1107.7       | 18.8             | Top 25%       |
| 34   | 34         | Nick Crebassa          | Corporate   | 8241.74     | 7            | 1314.76      | 13.7             | Top 25%       |
| 35   | 35         | Harry Marie            | Corporate   | 8236.76     | 10           | 2437.98      | 23.1             | Top 25%       |
| 36   | 36         | Keith Dawkins          | Corporate   | 8181.26     | 12           | 3038.63      | 8.8              | Top 25%       |
| 37   | 37         | Sean Braxton           | Corporate   | 8057.89     | 7            | -2082.75     | 24.1             | Top 25%       |
| 38   | 38         | Zuschuss Carroll       | Consumer    | 8025.71     | 13           | -1032.15     | 25.5             | Top 25%       |
| 39   | 39         | Joseph Holt            | Consumer    | 7955.0      | 6            | -644.7       | 8.6              | Top 25%       |
| 40   | 40         | Nora Preis             | Consumer    | 7903.18     | 7            | 631.23       | 19.6             | Top 25%       |
| 41   | 41         | Anna Häberlin          | Corporate   | 7888.29     | 12           | 1298.02      | 21.7             | Top 25%       |
| 42   | 42         | Adam Bellavance        | Home Office | 7755.62     | 8            | 2054.59      | 4.4              | Top 25%       |
| 43   | 43         | Jim Epp                | Corporate   | 7754.98     | 7            | 1623.4       | 16.0             | Top 25%       |
| 44   | 44         | Jane Waco              | Corporate   | 7721.71     | 6            | 2173.71      | 7.1              | Top 25%       |
| 45   | 45         | Lena Creighton         | Consumer    | 7663.13     | 12           | 1288.35      | 15.7             | Top 25%       |
| 46   | 46         | John Murray            | Consumer    | 7625.08     | 7            | 1574.62      | 18.5             | Top 25%       |
| 47   | 47         | Jonathan Doherty       | Corporate   | 7610.86     | 11           | 1050.27      | 7.5              | Top 25%       |
| 48   | 48         | Patrick O'Brill        | Consumer    | 7473.83     | 11           | 38.48        | 21.0             | Top 25%       |
| 49   | 49         | Maribeth Schnelling    | Consumer    | 7443.69     | 10           | 844.94       | 16.0             | Top 25%       |
| 50   | 50         | Rick Wilson            | Corporate   | 7397.4      | 7            | 1586.63      | 13.5             | Top 25%       |
| 51   | 51         | Brian Moss             | Corporate   | 7294.19     | 11           | 2199.28      | 8.4              | Top 25%       |
| 52   | 52         | Paul Prost             | Home Office | 7252.61     | 10           | 1495.09      | 10.9             | Top 25%       |
| 53   | 53         | Natalie Webber         | Consumer    | 7234.01     | 7            | 1023.12      | 21.4             | Top 25%       |
| 54   | 54         | Dean percer            | Home Office | 7198.76     | 11           | 333.36       | 18.6             | Top 25%       |
| 55   | 55         | Fred Hopkins           | Corporate   | 6987.2      | 8            | 2050.28      | 13.8             | Top 25%       |
| 56   | 56         | Rick Huthwaite         | Home Office | 6979.18     | 6            | 1289.45      | 3.3              | Top 25%       |
| 57   | 57         | Penelope Sewall        | Home Office | 6843.63     | 7            | 1742.73      | 8.5              | Top 25%       |
| 58   | 58         | Brenda Bowman          | Corporate   | 6765.73     | 9            | 1015.08      | 19.5             | Top 25%       |
| 59   | 59         | Joel Eaton             | Consumer    | 6760.81     | 13           | 221.8        | 14.6             | Top 25%       |
| 60   | 60         | Yana Sorensen          | Corporate   | 6720.44     | 8            | 1778.29      | 5.0              | Top 25%       |
| 61   | 61         | Andy Reiter            | Consumer    | 6608.45     | 6            | 2884.62      | 6.7              | Top 25%       |
| 62   | 62         | Dan Reichenbach        | Corporate   | 6528.03     | 9            | 1641.86      | 13.3             | Top 25%       |
| 63   | 63         | Grace Kelly            | Corporate   | 6497.27     | 9            | 1448.55      | 15.7             | Top 25%       |
| 64   | 64         | Joseph Airdo           | Consumer    | 6491.03     | 8            | -819.42      | 21.3             | Top 25%       |
| 65   | 65         | Nathan Mautz           | Home Office | 6459.34     | 7            | 2751.68      | 4.3              | Top 25%       |
| 66   | 66         | Valerie Dominguez      | Consumer    | 6442.25     | 6            | 1617.79      | 7.5              | Top 25%       |
| 67   | 67         | Sarah Brown            | Consumer    | 6411.0      | 6            | 885.46       | 14.2             | Top 25%       |
| 68   | 68         | James Galang           | Consumer    | 6366.39     | 11           | 1415.67      | 11.1             | Top 25%       |
| 69   | 69         | Darrin Martin          | Consumer    | 6345.1      | 7            | 1677.39      | 23.0             | Top 25%       |
| 70   | 70         | Corinna Mitchell       | Home Office | 6339.56     | 6            | 1572.46      | 7.2              | Top 25%       |
| 71   | 71         | Max Jones              | Consumer    | 6320.75     | 7            | 1054.55      | 21.3             | Top 25%       |
| 72   | 72         | Brosina Hoffman        | Consumer    | 6255.35     | 8            | 802.79       | 18.3             | Top 25%       |
| 73   | 73         | Rob Lucas              | Consumer    | 6234.91     | 8            | 488.15       | 21.9             | Top 25%       |
| 74   | 74         | William Brown          | Consumer    | 6160.1      | 11           | 714.33       | 20.5             | Top 25%       |
| 75   | 75         | Victoria Wilson        | Corporate   | 6134.04     | 10           | -874.66      | 16.1             | Top 25%       |
| 76   | 76         | Shirley Daniels        | Home Office | 6121.11     | 9            | 1985.17      | 10.5             | Top 25%       |
| 77   | 77         | Quincy Jones           | Corporate   | 6108.34     | 9            | 1203.68      | 12.3             | Top 25%       |
| 78   | 78         | Alan Dominguez         | Home Office | 6106.88     | 8            | 1869.93      | 5.8              | Top 25%       |
| 79   | 79         | Cassandra Brandow      | Consumer    | 6076.14     | 10           | 150.21       | 16.3             | Top 25%       |
| 80   | 80         | Greg Maxwell           | Corporate   | 6049.97     | 3            | 188.72       | 5.5              | Top 25%       |
| 81   | 81         | Shahid Collister       | Consumer    | 5992.54     | 9            | 236.66       | 19.0             | Top 25%       |
| 82   | 82         | Kristen Hastings       | Corporate   | 5990.8      | 7            | 1227.51      | 12.7             | Top 25%       |
| 83   | 83         | Robert Marley          | Home Office | 5979.1      | 5            | 1902.54      | 4.5              | Top 25%       |
| 84   | 84         | Keith Herrera          | Consumer    | 5952.86     | 7            | 656.12       | 10.9             | Top 25%       |
| 85   | 85         | Ben Ferrer             | Home Office | 5907.97     | 11           | 1538.21      | 12.2             | Top 25%       |
| 86   | 86         | Christine Phan         | Corporate   | 5888.28     | 8            | -1850.3      | 21.3             | Top 25%       |
| 87   | 87         | Bill Donatelli         | Consumer    | 5718.52     | 12           | 1094.5       | 7.9              | Top 25%       |
| 88   | 88         | Cindy Stewart          | Consumer    | 5690.05     | 6            | -6626.39     | 20.0             | Top 25%       |
| 89   | 89         | Anne McFarland         | Consumer    | 5664.02     | 8            | 1085.73      | 6.4              | Top 25%       |
| 90   | 90         | Ross Baird             | Home Office | 5633.32     | 8            | -461.73      | 25.0             | Top 25%       |
| 91   | 91         | Katherine Murray       | Home Office | 5620.19     | 8            | 973.79       | 14.0             | Top 25%       |
| 92   | 92         | Alex Avila             | Consumer    | 5563.56     | 5            | -362.88      | 9.1              | Top 25%       |
| 93   | 93         | Suzanne McNair         | Corporate   | 5563.39     | 12           | 581.57       | 12.7             | Top 25%       |
| 94   | 94         | Naresj Patel           | Consumer    | 5529.62     | 6            | 1208.89      | 5.7              | Top 25%       |
| 95   | 95         | Amy Cox                | Consumer    | 5527.85     | 7            | 1366.01      | 18.9             | Top 25%       |
| 96   | 96         | Mick Hernandez         | Home Office | 5503.09     | 9            | 170.97       | 16.8             | Top 25%       |
| 97   | 97         | Dennis Pardue          | Home Office | 5480.72     | 9            | 1571.83      | 18.6             | Top 25%       |
| 98   | 98         | Emily Phan             | Consumer    | 5478.06     | 17           | 144.96       | 19.7             | Top 25%       |
| 99   | 99         | Yoseph Carroll         | Corporate   | 5454.35     | 5            | 1305.63      | 7.5              | Top 25%       |
| 100  | 100        | Stefania Perrino       | Corporate   | 5440.32     | 9            | -270.43      | 25.0             | Top 25%       |
| 101  | 101        | Luke Weiss             | Consumer    | 5420.51     | 7            | 837.24       | 16.7             | Top 25%       |
| 102  | 102        | Cathy Prescott         | Corporate   | 5402.25     | 8            | 427.03       | 14.3             | Top 25%       |
| 103  | 103        | Thomas Seio            | Corporate   | 5371.09     | 7            | 862.89       | 15.8             | Top 25%       |
| 104  | 104        | Tonja Turnell          | Home Office | 5364.81     | 7            | 1124.5       | 12.9             | Top 25%       |
| 105  | 105        | Mitch Webber           | Consumer    | 5341.9      | 7            | 1238.42      | 7.9              | Top 25%       |
| 106  | 106        | Tom Prescott           | Consumer    | 5329.0      | 5            | -1087.39     | 46.2             | Top 25%       |
| 107  | 107        | Tamara Willingham      | Home Office | 5278.83     | 7            | 737.39       | 10.0             | Top 25%       |
| 108  | 108        | Dianna Wilson          | Home Office | 5271.63     | 5            | 1348.76      | 3.6              | Top 25%       |
| 109  | 109        | Mitch Willingham       | Corporate   | 5253.88     | 2            | 1665.52      | 6.7              | Top 25%       |
| 110  | 110        | Harold Ryan            | Corporate   | 5248.79     | 7            | 1196.95      | 10.0             | Top 25%       |
| 111  | 111        | Steven Cartwright      | Consumer    | 5226.21     | 11           | 1276.65      | 15.0             | Top 25%       |
| 112  | 112        | Resi Pölking           | Consumer    | 5153.08     | 12           | 465.25       | 14.8             | Top 25%       |
| 113  | 113        | Lena Radford           | Consumer    | 5142.89     | 6            | 535.48       | 17.5             | Top 25%       |
| 114  | 114        | Mike Pelletier         | Home Office | 5087.92     | 9            | 226.45       | 15.5             | Top 25%       |
| 115  | 115        | Anna Andreadi          | Consumer    | 5086.94     | 6            | 857.8        | 6.4              | Top 25%       |
| 116  | 116        | Ivan Liston            | Consumer    | 5040.74     | 7            | 1121.94      | 7.1              | Top 25%       |
| 117  | 117        | Kelly Lampkin          | Corporate   | 5016.49     | 8            | -182.78      | 29.5             | Top 25%       |
| 118  | 118        | Laurel Beltran         | Home Office | 4985.68     | 8            | -52.19       | 23.8             | Top 25%       |
| 119  | 119        | Dave Hallsten          | Corporate   | 4932.87     | 6            | 1193.74      | 7.8              | Top 25%       |
| 120  | 120        | Irene Maddox           | Consumer    | 4930.47     | 7            | 514.65       | 16.7             | Top 25%       |
| 121  | 121        | Ted Trevino            | Consumer    | 4915.6      | 7            | 751.96       | 11.4             | Top 25%       |
| 122  | 122        | Kunst Miller           | Consumer    | 4909.47     | 8            | 745.77       | 8.9              | Top 25%       |
| 123  | 123        | Philisse Overcash      | Home Office | 4893.04     | 9            | 1155.43      | 10.6             | Top 25%       |
| 124  | 124        | Heather Kirkland       | Corporate   | 4877.78     | 8            | 956.95       | 21.3             | Top 25%       |
| 125  | 125        | Anthony Jacobs         | Corporate   | 4867.34     | 7            | 150.71       | 8.7              | Top 25%       |
| 126  | 126        | Joe Kamberova          | Consumer    | 4867.2      | 10           | 55.05        | 33.2             | Top 25%       |
| 127  | 127        | Alan Hwang             | Consumer    | 4805.34     | 9            | 1308.55      | 9.2              | Top 25%       |
| 128  | 128        | Dean Katz              | Corporate   | 4802.39     | 9            | 209.9        | 19.5             | Top 25%       |
| 129  | 129        | Russell Applegate      | Consumer    | 4793.54     | 9            | 304.87       | 28.0             | Top 25%       |
| 130  | 130        | Sue Ann Reed           | Consumer    | 4767.34     | 10           | 610.15       | 19.3             | Top 25%       |
| 131  | 131        | Jim Kriz               | Home Office | 4760.43     | 9            | 1172.53      | 10.0             | Top 25%       |
| 132  | 132        | Bart Watters           | Corporate   | 4750.36     | 8            | 921.26       | 14.1             | Top 25%       |
| 133  | 133        | Tracy Blumstein        | Consumer    | 4737.49     | 9            | -1603.05     | 26.5             | Top 25%       |
| 134  | 134        | Giulietta Baptist      | Consumer    | 4716.29     | 5            | 1135.84      | 3.8              | Top 25%       |
| 135  | 135        | Rick Bensley           | Home Office | 4715.47     | 12           | 640.55       | 13.5             | Top 25%       |
| 136  | 136        | Erin Smith             | Corporate   | 4657.92     | 9            | 246.67       | 26.0             | Top 25%       |
| 137  | 137        | Deborah Brumfield      | Home Office | 4655.9      | 8            | 841.83       | 20.8             | Top 25%       |
| 138  | 138        | Kean Thornton          | Consumer    | 4642.09     | 10           | 194.07       | 14.8             | Top 25%       |
| 139  | 139        | Sample Company A       | Home Office | 4624.57     | 9            | 1011.74      | 18.7             | Top 25%       |
| 140  | 140        | Eugene Moren           | Home Office | 4588.44     | 6            | 1319.37      | 6.7              | Top 25%       |
| 141  | 141        | Dave Brooks            | Consumer    | 4531.65     | 7            | 473.03       | 18.5             | Top 25%       |
| 142  | 142        | Anthony Rawles         | Corporate   | 4523.34     | 8            | 494.84       | 7.7              | Top 25%       |
| 143  | 143        | Arthur Gainer          | Consumer    | 4510.8      | 10           | 343.68       | 16.7             | Top 25%       |
| 144  | 144        | Anthony Johnson        | Corporate   | 4501.39     | 7            | 1158.71      | 8.3              | Top 25%       |
| 145  | 145        | Linda Cazamias         | Corporate   | 4492.95     | 8            | 288.27       | 17.1             | Top 25%       |
| 146  | 146        | Stewart Carmichael     | Corporate   | 4492.66     | 7            | -671.19      | 30.5             | Top 25%       |
| 147  | 147        | Theone Pippenger       | Consumer    | 4454.06     | 9            | 1129.13      | 8.8              | Top 25%       |
| 148  | 148        | Mark Cousins           | Corporate   | 4432.14     | 5            | 1802.39      | 12.0             | Top 25%       |
| 149  | 149        | Jamie Kunitz           | Consumer    | 4427.14     | 5            | 1219.98      | 13.1             | Top 25%       |
| 150  | 150        | Katrina Willman        | Consumer    | 4416.52     | 5            | 1756.14      | 11.0             | Top 25%       |
| 151  | 151        | Bradley Drucker        | Consumer    | 4411.24     | 6            | 1142.12      | 13.5             | Top 25%       |
| 152  | 152        | Arianne Irving         | Consumer    | 4375.79     | 10           | 867.73       | 7.2              | Top 25%       |
| 153  | 153        | Scot Coram             | Corporate   | 4371.96     | 4            | 440.14       | 10.9             | Top 25%       |
| 154  | 154        | Ellis Ballard          | Corporate   | 4358.13     | 5            | 656.2        | 12.5             | Top 25%       |
| 155  | 155        | Gary Zandusky          | Consumer    | 4355.15     | 9            | 1087.75      | 7.9              | Top 25%       |
| 156  | 156        | Steven Roelle          | Home Office | 4345.89     | 8            | 1990.42      | 3.3              | Top 25%       |
| 157  | 157        | Natalie DeCherney      | Consumer    | 4326.14     | 9            | 353.65       | 21.1             | Top 25%       |
| 158  | 158        | Matt Abelman           | Home Office | 4299.16     | 11           | 1240.23      | 9.4              | Top 25%       |
| 159  | 159        | Sung Pak               | Corporate   | 4282.94     | 10           | 566.72       | 20.8             | Top 25%       |
| 160  | 160        | Dana Kaydos            | Consumer    | 4282.18     | 5            | 937.65       | 8.0              | Top 25%       |
| 161  | 161        | Rick Duston            | Consumer    | 4272.93     | 8            | 480.59       | 10.7             | Top 25%       |
| 162  | 162        | Toby Carlisle          | Consumer    | 4266.81     | 8            | 606.37       | 13.1             | Top 25%       |
| 163  | 163        | Alan Schoenberger      | Corporate   | 4260.78     | 5            | 719.78       | 6.2              | Top 25%       |
| 164  | 164        | Frank Hawley           | Corporate   | 4256.27     | 10           | 1073.27      | 12.9             | Top 25%       |
| 165  | 165        | Claudia Bergmann       | Corporate   | 4246.46     | 8            | 1049.56      | 5.0              | Top 25%       |
| 166  | 166        | Tracy Hopkins          | Home Office | 4234.1      | 7            | -571.97      | 6.9              | Top 25%       |
| 167  | 167        | Bill Eplett            | Home Office | 4204.68     | 5            | 1487.77      | 2.2              | Top 25%       |
| 168  | 168        | Jill Fjeld             | Consumer    | 4198.33     | 8            | 1073.21      | 17.5             | Top 25%       |
| 169  | 169        | Gary Hwang             | Consumer    | 4172.85     | 4            | 1176.42      | 19.0             | Top 25%       |
| 170  | 170        | Roland Schwarz         | Corporate   | 4159.77     | 8            | 1206.39      | 11.4             | Top 25%       |
| 171  | 171        | Muhammed Yedwab        | Corporate   | 4152.7      | 11           | -371.71      | 24.4             | Top 25%       |
| 172  | 172        | Peter McVee            | Home Office | 4115.66     | 4            | 526.75       | 12.9             | Top 25%       |
| 173  | 173        | Stewart Visinsky       | Consumer    | 4105.31     | 9            | 485.03       | 18.4             | Top 25%       |
| 174  | 174        | Denise Monton          | Corporate   | 4074.47     | 8            | 1319.06      | 10.0             | Top 25%       |
| 175  | 175        | Frank Preis            | Consumer    | 4046.75     | 8            | 406.45       | 13.6             | Top 25%       |
| 176  | 176        | Susan Pistek           | Consumer    | 3990.69     | 6            | 14.69        | 27.1             | Top 25%       |
| 177  | 177        | Craig Molinari         | Corporate   | 3984.45     | 4            | 176.31       | 30.9             | Top 25%       |
| 178  | 178        | Michael Paige          | Corporate   | 3983.64     | 9            | 638.16       | 25.5             | Top 25%       |
| 179  | 179        | Sean Christensen       | Consumer    | 3979.06     | 7            | 229.16       | 21.7             | Top 25%       |
| 180  | 180        | Sanjit Jacobs          | Home Office | 3949.66     | 12           | 144.12       | 23.3             | Top 25%       |
| 181  | 181        | Luke Foster            | Consumer    | 3930.51     | 7            | -3583.98     | 31.9             | Top 25%       |
| 182  | 182        | Pierre Wener           | Consumer    | 3922.41     | 7            | 1290.35      | 17.1             | Top 25%       |
| 183  | 183        | George Ashbrook        | Consumer    | 3919.78     | 8            | 840.9        | 6.4              | Top 25%       |
| 184  | 184        | Ken Heidel             | Corporate   | 3918.97     | 9            | 727.38       | 10.6             | Top 25%       |
| 185  | 185        | Chris Cortes           | Consumer    | 3913.42     | 12           | 393.96       | 11.8             | Top 25%       |
| 186  | 186        | Dorothy Badders        | Corporate   | 3908.8      | 7            | 109.33       | 15.1             | Top 25%       |
| 187  | 187        | Nora Paige             | Consumer    | 3908.4      | 5            | 514.6        | 2.0              | Top 25%       |
| 188  | 188        | Kelly Collister        | Consumer    | 3908.26     | 4            | 709.42       | 20.0             | Top 25%       |
| 189  | 189        | Fred Chung             | Corporate   | 3889.37     | 7            | 714.29       | 16.0             | Top 25%       |
| 190  | 190        | Bill Stewart           | Corporate   | 3887.83     | 5            | -17.53       | 27.7             | Top 25%       |
| 191  | 191        | John Stevenson         | Consumer    | 3868.02     | 5            | 564.98       | 14.7             | Top 25%       |
| 192  | 192        | Ruben Ausman           | Corporate   | 3832.31     | 7            | 1292.87      | 4.0              | Top 25%       |
| 193  | 193        | Annie Thurman          | Consumer    | 3831.86     | 10           | 974.11       | 8.8              | Top 25%       |
| 194  | 194        | Olvera Toch            | Consumer    | 3818.62     | 5            | -925.12      | 16.0             | Top 25%       |
| 195  | 195        | Rose O'Brian           | Consumer    | 3815.48     | 7            | -1262.57     | 29.2             | Top 25%       |
| 196  | 196        | Michael Chen           | Consumer    | 3805.71     | 7            | 698.42       | 10.0             | Top 25%       |
| 197  | 197        | Michael Moore          | Consumer    | 3794.08     | 11           | 82.13        | 18.1             | Top 25%       |
| 198  | 198        | Carol Adams            | Corporate   | 3789.72     | 6            | 1143.38      | 11.2             | Top 25%       |
| 199  | 199        | Matthew Grinstein      | Home Office | 3785.28     | 7            | 341.9        | 12.9             | Top 25%       |
| 200  | 200        | Maribeth Dona          | Consumer    | 3766.38     | 7            | -241.95      | 32.9             | Upper-Mid 25% |
| 201  | 201        | Jim Karlsson           | Consumer    | 3760.03     | 7            | 750.95       | 11.7             | Upper-Mid 25% |
| 202  | 202        | Juliana Krohn          | Consumer    | 3747.67     | 3            | 586.66       | 20.0             | Upper-Mid 25% |
| 203  | 203        | Frank Merwin           | Home Office | 3736.2      | 9            | 198.11       | 18.0             | Upper-Mid 25% |
| 204  | 204        | Scott Cohen            | Corporate   | 3729.79     | 8            | 671.0        | 19.7             | Upper-Mid 25% |
| 205  | 205        | Hunter Glantz          | Consumer    | 3690.28     | 7            | 804.61       | 17.3             | Upper-Mid 25% |
| 206  | 206        | Ben Peterman           | Corporate   | 3675.86     | 9            | 363.6        | 19.4             | Upper-Mid 25% |
| 207  | 207        | Liz Preis              | Consumer    | 3653.4      | 7            | 338.45       | 18.7             | Upper-Mid 25% |
| 208  | 208        | Christopher Schild     | Home Office | 3651.86     | 9            | -342.8       | 21.4             | Upper-Mid 25% |
| 209  | 209        | Ed Braxton             | Corporate   | 3644.98     | 9            | 13.62        | 25.8             | Upper-Mid 25% |
| 210  | 210        | Jeremy Pistek          | Consumer    | 3635.59     | 7            | 757.18       | 5.9              | Upper-Mid 25% |
| 211  | 211        | Sam Zeldin             | Home Office | 3625.33     | 11           | 366.43       | 22.0             | Upper-Mid 25% |
| 212  | 212        | Rick Hansen            | Consumer    | 3621.38     | 5            | 563.79       | 10.0             | Upper-Mid 25% |
| 213  | 213        | Thomas Boland          | Corporate   | 3589.3      | 4            | 829.16       | 9.1              | Upper-Mid 25% |
| 214  | 214        | Gary McGarr            | Consumer    | 3582.82     | 7            | 347.27       | 11.8             | Upper-Mid 25% |
| 215  | 215        | Dionis Lloyd           | Corporate   | 3539.32     | 8            | -52.79       | 5.0              | Upper-Mid 25% |
| 216  | 216        | Erica Smith            | Consumer    | 3510.46     | 5            | 1003.29      | 12.5             | Upper-Mid 25% |
| 217  | 217        | Robert Waldorf         | Consumer    | 3495.65     | 5            | 707.55       | 7.3              | Upper-Mid 25% |
| 218  | 218        | Anna Gayman            | Consumer    | 3489.04     | 7            | -246.43      | 16.1             | Upper-Mid 25% |
| 219  | 219        | Emily Ducich           | Home Office | 3484.92     | 8            | 670.44       | 21.4             | Upper-Mid 25% |
| 220  | 220        | Pauline Webber         | Corporate   | 3454.92     | 10           | 803.82       | 3.8              | Upper-Mid 25% |
| 221  | 221        | Sarah Foster           | Consumer    | 3422.79     | 9            | 286.9        | 12.7             | Upper-Mid 25% |
| 222  | 222        | Frank Carlisle         | Home Office | 3418.74     | 7            | 1217.17      | 13.6             | Upper-Mid 25% |
| 223  | 223        | Sally Hughsby          | Corporate   | 3406.84     | 13           | 558.47       | 13.6             | Upper-Mid 25% |
| 224  | 224        | Sandra Glassco         | Consumer    | 3406.58     | 3            | 570.44       | 6.8              | Upper-Mid 25% |
| 225  | 225        | Trudy Schmidt          | Consumer    | 3368.09     | 5            | 220.92       | 19.3             | Upper-Mid 25% |
| 226  | 226        | Sam Craven             | Consumer    | 3362.96     | 5            | -317.05      | 21.9             | Upper-Mid 25% |
| 227  | 227        | Victoria Pisteka       | Corporate   | 3360.53     | 7            | -1018.78     | 17.1             | Upper-Mid 25% |
| 228  | 228        | Doug Jacobs            | Consumer    | 3356.4      | 3            | 731.56       | 6.3              | Upper-Mid 25% |
| 229  | 229        | Dianna Vittorini       | Consumer    | 3341.59     | 6            | 353.21       | 11.3             | Upper-Mid 25% |
| 230  | 230        | Sylvia Foulston        | Corporate   | 3336.54     | 9            | 539.94       | 27.1             | Upper-Mid 25% |
| 231  | 231        | Dan Campbell           | Consumer    | 3336.17     | 9            | -1441.63     | 21.1             | Upper-Mid 25% |
| 232  | 232        | Arthur Prichep         | Consumer    | 3323.56     | 10           | 579.31       | 9.4              | Upper-Mid 25% |
| 233  | 233        | Dennis Kane            | Consumer    | 3318.49     | 8            | 377.08       | 10.9             | Upper-Mid 25% |
| 234  | 234        | Katharine Harms        | Corporate   | 3312.86     | 8            | 454.79       | 13.9             | Upper-Mid 25% |
| 235  | 235        | Randy Ferguson         | Corporate   | 3309.15     | 8            | 633.71       | 13.8             | Upper-Mid 25% |
| 236  | 236        | Rick Reed              | Corporate   | 3302.26     | 6            | 721.68       | 6.0              | Upper-Mid 25% |
| 237  | 237        | Brian Dahlen           | Consumer    | 3288.47     | 7            | 634.85       | 7.2              | Upper-Mid 25% |
| 238  | 238        | Brian Stugart          | Consumer    | 3288.11     | 3            | 238.74       | 18.2             | Upper-Mid 25% |
| 239  | 239        | Rob Williams           | Corporate   | 3279.75     | 9            | 698.83       | 13.8             | Upper-Mid 25% |
| 240  | 240        | Daniel Lacy            | Consumer    | 3272.2      | 6            | 4.21         | 3.6              | Upper-Mid 25% |
| 241  | 241        | Damala Kotsonis        | Corporate   | 3256.48     | 12           | 881.12       | 17.8             | Upper-Mid 25% |
| 242  | 242        | Adam Shillingsburg     | Consumer    | 3255.31     | 9            | 64.54        | 18.0             | Upper-Mid 25% |
| 243  | 243        | Jack O'Briant          | Corporate   | 3254.95     | 9            | 581.4        | 7.3              | Upper-Mid 25% |
| 244  | 244        | Adam Hart              | Corporate   | 3250.34     | 10           | 281.19       | 13.5             | Upper-Mid 25% |
| 245  | 245        | Henry Goldwyn          | Corporate   | 3247.64     | 12           | -2797.96     | 17.1             | Upper-Mid 25% |
| 246  | 246        | Lindsay Castell        | Home Office | 3246.63     | 4            | 299.48       | 28.6             | Upper-Mid 25% |
| 247  | 247        | Carol Triggs           | Consumer    | 3241.9      | 8            | 161.23       | 16.1             | Upper-Mid 25% |
| 248  | 248        | Edward Becker          | Corporate   | 3236.31     | 10           | -80.29       | 14.5             | Upper-Mid 25% |
| 249  | 249        | Sharelle Roach         | Home Office | 3233.48     | 5            | -3333.91     | 36.7             | Upper-Mid 25% |
| 250  | 250        | Lindsay Williams       | Corporate   | 3230.31     | 6            | 662.83       | 10.9             | Upper-Mid 25% |
| 251  | 251        | Ricardo Sperren        | Corporate   | 3221.29     | 5            | 633.45       | 0.0              | Upper-Mid 25% |
| 252  | 252        | Alejandro Savely       | Corporate   | 3214.24     | 6            | 354.63       | 22.5             | Upper-Mid 25% |
| 253  | 253        | Mark Packer            | Home Office | 3206.13     | 7            | 600.29       | 12.1             | Upper-Mid 25% |
| 254  | 254        | Christine Sundaresam   | Consumer    | 3202.16     | 11           | 831.94       | 8.2              | Upper-Mid 25% |
| 255  | 255        | Brian Thompson         | Consumer    | 3196.75     | 7            | 447.75       | 7.0              | Upper-Mid 25% |
| 256  | 256        | Deirdre Greer          | Corporate   | 3195.82     | 5            | 562.78       | 10.0             | Upper-Mid 25% |
| 257  | 257        | Jeremy Lonsdale        | Consumer    | 3173.87     | 6            | 591.72       | 7.1              | Upper-Mid 25% |
| 258  | 258        | Greg Matthias          | Consumer    | 3163.63     | 6            | 35.49        | 14.5             | Upper-Mid 25% |
| 259  | 259        | Janet Martin           | Consumer    | 3159.12     | 6            | 19.82        | 28.9             | Upper-Mid 25% |
| 260  | 260        | Chloris Kastensmidt    | Consumer    | 3154.86     | 13           | 141.28       | 23.4             | Upper-Mid 25% |
| 261  | 261        | Karen Bern             | Corporate   | 3152.62     | 7            | 763.91       | 15.0             | Upper-Mid 25% |
| 262  | 262        | Maxwell Schwartz       | Consumer    | 3144.68     | 9            | 280.86       | 10.0             | Upper-Mid 25% |
| 263  | 263        | Ruben Dartt            | Consumer    | 3133.92     | 9            | 455.53       | 5.7              | Upper-Mid 25% |
| 264  | 264        | Tanja Norvell          | Home Office | 3130.22     | 7            | -692.05      | 20.0             | Upper-Mid 25% |
| 265  | 265        | Steve Nguyen           | Home Office | 3127.96     | 7            | 481.75       | 11.7             | Upper-Mid 25% |
| 266  | 266        | Speros Goranitis       | Consumer    | 3124.83     | 6            | 463.27       | 9.2              | Upper-Mid 25% |
| 267  | 267        | Katherine Hughes       | Consumer    | 3100.61     | 6            | 528.21       | 15.0             | Upper-Mid 25% |
| 268  | 268        | Patrick Gardner        | Consumer    | 3086.91     | 13           | 137.46       | 16.9             | Upper-Mid 25% |
| 269  | 269        | Eugene Hildebrand      | Home Office | 3082.65     | 10           | 96.27        | 20.6             | Upper-Mid 25% |
| 270  | 270        | Gary Mitchum           | Home Office | 3078.62     | 6            | 793.28       | 16.7             | Upper-Mid 25% |
| 271  | 271        | Eugene Barchas         | Consumer    | 3071.13     | 6            | 184.77       | 20.9             | Upper-Mid 25% |
| 272  | 272        | Mike Gockenbach        | Consumer    | 3061.54     | 4            | -93.6        | 18.8             | Upper-Mid 25% |
| 273  | 273        | Toby Gnade             | Consumer    | 3058.37     | 5            | 682.17       | 21.1             | Upper-Mid 25% |
| 274  | 274        | Kean Takahito          | Consumer    | 3057.1      | 7            | 254.0        | 22.9             | Upper-Mid 25% |
| 275  | 275        | Shahid Shariari        | Consumer    | 3056.81     | 6            | -1010.97     | 25.8             | Upper-Mid 25% |
| 276  | 276        | Sara Luxemburg         | Home Office | 3053.01     | 7            | 527.97       | 17.8             | Upper-Mid 25% |
| 277  | 277        | Aaron Smayling         | Corporate   | 3050.69     | 7            | -253.57      | 35.5             | Upper-Mid 25% |
| 278  | 278        | Cynthia Arntzen        | Consumer    | 3041.57     | 7            | 204.49       | 18.8             | Upper-Mid 25% |
| 279  | 279        | Carlos Soltero         | Consumer    | 3036.55     | 11           | -126.42      | 26.4             | Upper-Mid 25% |
| 280  | 280        | Lindsay Shagiari       | Home Office | 2988.67     | 9            | 262.64       | 28.2             | Upper-Mid 25% |
| 281  | 281        | Michelle Huthwaite     | Consumer    | 2984.95     | 5            | 476.9        | 13.0             | Upper-Mid 25% |
| 282  | 282        | Frank Atkinson         | Corporate   | 2984.05     | 7            | 520.52       | 25.9             | Upper-Mid 25% |
| 283  | 283        | David Bremer           | Corporate   | 2973.09     | 7            | -1421.77     | 14.3             | Upper-Mid 25% |
| 284  | 284        | Noel Staavos           | Corporate   | 2964.82     | 13           | -234.77      | 21.5             | Upper-Mid 25% |
| 285  | 285        | Tamara Manning         | Consumer    | 2955.23     | 8            | 573.3        | 5.3              | Upper-Mid 25% |
| 286  | 286        | Christine Kargatis     | Home Office | 2945.32     | 5            | 261.22       | 18.3             | Upper-Mid 25% |
| 287  | 287        | Thea Hudgings          | Corporate   | 2942.77     | 4            | -252.55      | 23.3             | Upper-Mid 25% |
| 288  | 288        | Liz Thompson           | Consumer    | 2936.25     | 8            | 320.97       | 24.6             | Upper-Mid 25% |
| 289  | 289        | Becky Castell          | Home Office | 2933.68     | 9            | 251.6        | 11.1             | Upper-Mid 25% |
| 290  | 290        | Julie Kriz             | Home Office | 2932.48     | 10           | 122.66       | 20.6             | Upper-Mid 25% |
| 291  | 291        | Shaun Weien            | Consumer    | 2921.54     | 7            | 793.65       | 11.1             | Upper-Mid 25% |
| 292  | 292        | Maris LaWare           | Consumer    | 2921.5      | 6            | -76.18       | 16.7             | Upper-Mid 25% |
| 293  | 293        | Rob Dowd               | Consumer    | 2912.89     | 10           | 734.52       | 3.2              | Upper-Mid 25% |
| 294  | 294        | Craig Yedwab           | Corporate   | 2900.03     | 8            | 60.65        | 20.0             | Upper-Mid 25% |
| 295  | 295        | Neil Ducich            | Corporate   | 2893.46     | 6            | 443.34       | 8.8              | Upper-Mid 25% |
| 296  | 296        | Meg Tillman            | Consumer    | 2890.14     | 6            | 509.01       | 13.0             | Upper-Mid 25% |
| 297  | 297        | Barry Französisch      | Corporate   | 2888.51     | 8            | 302.02       | 25.7             | Upper-Mid 25% |
| 298  | 298        | David Smith            | Corporate   | 2881.81     | 9            | 163.7        | 15.4             | Upper-Mid 25% |
| 299  | 299        | Paul Van Hugh          | Home Office | 2876.05     | 5            | 434.53       | 8.5              | Upper-Mid 25% |
| 300  | 300        | Ionia McGrath          | Consumer    | 2872.63     | 3            | 975.77       | 10.0             | Upper-Mid 25% |
| 301  | 301        | Chuck Clark            | Home Office | 2870.05     | 10           | 424.66       | 5.8              | Upper-Mid 25% |
| 302  | 302        | Craig Carroll          | Consumer    | 2854.12     | 4            | 850.16       | 25.0             | Upper-Mid 25% |
| 303  | 303        | Arthur Wiediger        | Home Office | 2852.97     | 7            | -104.55      | 30.6             | Upper-Mid 25% |
| 304  | 304        | Erin Ashbrook          | Corporate   | 2846.71     | 13           | -52.74       | 30.0             | Upper-Mid 25% |
| 305  | 305        | Linda Southworth       | Corporate   | 2845.27     | 6            | -318.77      | 30.7             | Upper-Mid 25% |
| 306  | 306        | Darren Budd            | Corporate   | 2839.23     | 5            | 213.0        | 16.6             | Upper-Mid 25% |
| 307  | 307        | Justin MacKendrick     | Consumer    | 2833.93     | 10           | 754.11       | 6.3              | Upper-Mid 25% |
| 308  | 308        | Christina VanderZanden | Consumer    | 2830.63     | 5            | 493.09       | 7.7              | Upper-Mid 25% |
| 309  | 309        | Troy Staebel           | Consumer    | 2820.42     | 7            | -294.7       | 37.3             | Upper-Mid 25% |
| 310  | 310        | Gary Hansen            | Home Office | 2819.47     | 9            | -576.83      | 27.1             | Upper-Mid 25% |
| 311  | 311        | Barry Gonzalez         | Consumer    | 2798.95     | 8            | -711.43      | 19.2             | Upper-Mid 25% |
| 312  | 312        | Trudy Brown            | Consumer    | 2797.67     | 9            | 379.88       | 14.0             | Upper-Mid 25% |
| 313  | 313        | Robert Dilbeck         | Home Office | 2786.63     | 5            | 835.77       | 8.0              | Upper-Mid 25% |
| 314  | 314        | John Castell           | Consumer    | 2772.06     | 9            | 279.57       | 12.2             | Upper-Mid 25% |
| 315  | 315        | Philip Fox             | Consumer    | 2770.0      | 6            | 196.87       | 5.0              | Upper-Mid 25% |
| 316  | 316        | Emily Burns            | Consumer    | 2767.22     | 10           | 261.53       | 29.1             | Upper-Mid 25% |
| 317  | 317        | Chris Selesnick        | Corporate   | 2754.22     | 12           | 738.36       | 5.7              | Upper-Mid 25% |
| 318  | 318        | Michelle Moray         | Consumer    | 2749.88     | 8            | -520.34      | 21.1             | Upper-Mid 25% |
| 319  | 319        | Ken Black              | Corporate   | 2744.74     | 12           | 579.36       | 10.9             | Upper-Mid 25% |
| 320  | 320        | Lauren Leatherbury     | Consumer    | 2741.2      | 6            | 560.01       | 1.7              | Upper-Mid 25% |
| 321  | 321        | Marc Crier             | Consumer    | 2725.98     | 8            | 461.0        | 13.1             | Upper-Mid 25% |
| 322  | 322        | John Lucas             | Consumer    | 2725.26     | 6            | 779.9        | 23.6             | Upper-Mid 25% |
| 323  | 323        | Marina Lichtenstein    | Corporate   | 2722.84     | 9            | 684.92       | 17.3             | Upper-Mid 25% |
| 324  | 324        | Jay Kimmel             | Consumer    | 2709.63     | 8            | 330.28       | 12.4             | Upper-Mid 25% |
| 325  | 325        | Justin Ellison         | Corporate   | 2697.25     | 3            | 789.65       | 2.9              | Upper-Mid 25% |
| 326  | 326        | Bradley Talbott        | Home Office | 2684.49     | 5            | 409.5        | 10.0             | Upper-Mid 25% |
| 327  | 327        | Bill Overfelt          | Corporate   | 2682.73     | 5            | 278.78       | 23.3             | Upper-Mid 25% |
| 328  | 328        | Frank Olsen            | Consumer    | 2678.44     | 10           | 215.6        | 22.0             | Upper-Mid 25% |
| 329  | 329        | Nicole Hansen          | Corporate   | 2673.29     | 7            | 760.17       | 5.5              | Upper-Mid 25% |
| 330  | 330        | Richard Bierner        | Consumer    | 2663.09     | 8            | 477.24       | 16.2             | Upper-Mid 25% |
| 331  | 331        | Eva Jacobs             | Consumer    | 2656.69     | 5            | 451.88       | 6.3              | Upper-Mid 25% |
| 332  | 332        | Dave Kipp              | Consumer    | 2650.56     | 7            | 536.39       | 13.8             | Upper-Mid 25% |
| 333  | 333        | Christina Anderson     | Consumer    | 2648.29     | 9            | 279.62       | 18.9             | Upper-Mid 25% |
| 334  | 334        | Logan Currie           | Consumer    | 2633.58     | 9            | 231.13       | 18.4             | Upper-Mid 25% |
| 335  | 335        | Ralph Arnett           | Consumer    | 2617.91     | 9            | 546.09       | 16.5             | Upper-Mid 25% |
| 336  | 336        | Katherine Nockton      | Corporate   | 2617.27     | 9            | -151.15      | 21.8             | Upper-Mid 25% |
| 337  | 337        | Sean O'Donnell         | Consumer    | 2602.58     | 6            | -81.09       | 13.7             | Upper-Mid 25% |
| 338  | 338        | Stephanie Ulpright     | Home Office | 2595.36     | 7            | 763.47       | 13.3             | Upper-Mid 25% |
| 339  | 339        | Helen Andreada         | Consumer    | 2584.16     | 8            | 99.14        | 20.0             | Upper-Mid 25% |
| 340  | 340        | Alejandro Grove        | Consumer    | 2582.9      | 5            | 732.74       | 1.4              | Upper-Mid 25% |
| 341  | 341        | Lena Cacioppo          | Consumer    | 2580.7      | 8            | -188.25      | 24.0             | Upper-Mid 25% |
| 342  | 342        | Steve Chapman          | Corporate   | 2576.41     | 10           | 611.83       | 15.7             | Upper-Mid 25% |
| 343  | 343        | Neola Schneider        | Consumer    | 2575.86     | 4            | -12.3        | 20.7             | Upper-Mid 25% |
| 344  | 344        | Beth Thompson          | Home Office | 2567.66     | 5            | 417.59       | 4.4              | Upper-Mid 25% |
| 345  | 345        | Eleni McCrary          | Corporate   | 2567.01     | 5            | -133.83      | 14.3             | Upper-Mid 25% |
| 346  | 346        | Mary Zewe              | Corporate   | 2564.91     | 6            | 787.75       | 28.0             | Upper-Mid 25% |
| 347  | 347        | Bruce Stewart          | Consumer    | 2562.38     | 7            | -113.3       | 13.2             | Upper-Mid 25% |
| 348  | 348        | Deanra Eno             | Home Office | 2550.87     | 5            | 464.47       | 11.1             | Upper-Mid 25% |
| 349  | 349        | Corey Catlett          | Corporate   | 2540.63     | 7            | 331.43       | 27.5             | Upper-Mid 25% |
| 350  | 350        | Ann Chong              | Corporate   | 2537.69     | 5            | 298.83       | 11.1             | Upper-Mid 25% |
| 351  | 351        | Charles McCrossin      | Consumer    | 2533.31     | 6            | -394.37      | 24.3             | Upper-Mid 25% |
| 352  | 352        | Herbert Flentye        | Consumer    | 2533.16     | 7            | -13.88       | 13.2             | Upper-Mid 25% |
| 353  | 353        | Fred McMath            | Consumer    | 2523.27     | 9            | 191.49       | 15.7             | Upper-Mid 25% |
| 354  | 354        | Julia Barnett          | Home Office | 2518.11     | 5            | 201.52       | 18.9             | Upper-Mid 25% |
| 355  | 355        | Joy Smith              | Consumer    | 2516.49     | 6            | -311.26      | 18.3             | Upper-Mid 25% |
| 356  | 356        | Don Jones              | Corporate   | 2501.69     | 8            | 345.25       | 6.9              | Upper-Mid 25% |
| 357  | 357        | Amy Hunt               | Consumer    | 2495.39     | 5            | -196.12      | 14.0             | Upper-Mid 25% |
| 358  | 358        | Patrick O'Donnell      | Consumer    | 2493.21     | 7            | 437.85       | 4.6              | Upper-Mid 25% |
| 359  | 359        | Nick Zandusky          | Home Office | 2488.31     | 9            | 402.42       | 17.5             | Upper-Mid 25% |
| 360  | 360        | Michael Nguyen         | Consumer    | 2477.95     | 6            | 290.82       | 26.0             | Upper-Mid 25% |
| 361  | 361        | Beth Paige             | Consumer    | 2475.16     | 7            | -319.06      | 30.0             | Upper-Mid 25% |
| 362  | 362        | Charles Crestani       | Consumer    | 2471.65     | 7            | 392.28       | 8.2              | Upper-Mid 25% |
| 363  | 363        | Nat Carroll            | Consumer    | 2461.4      | 5            | 580.31       | 4.1              | Upper-Mid 25% |
| 364  | 364        | Filia McAdams          | Corporate   | 2456.64     | 10           | 249.68       | 9.3              | Upper-Mid 25% |
| 365  | 365        | Mark Hamilton          | Consumer    | 2456.18     | 8            | 484.77       | 16.4             | Upper-Mid 25% |
| 366  | 366        | Brendan Sweed          | Corporate   | 2454.93     | 6            | 381.78       | 30.0             | Upper-Mid 25% |
| 367  | 367        | Valerie Mitchum        | Home Office | 2454.87     | 7            | 513.53       | 10.0             | Upper-Mid 25% |
| 368  | 368        | George Zrebassa        | Corporate   | 2454.62     | 4            | 828.66       | 4.0              | Upper-Mid 25% |
| 369  | 369        | Michelle Arnett        | Home Office | 2453.28     | 6            | 280.78       | 4.2              | Upper-Mid 25% |
| 370  | 370        | Bart Pistole           | Corporate   | 2442.04     | 12           | 433.98       | 16.5             | Upper-Mid 25% |
| 371  | 371        | Matt Collister         | Corporate   | 2426.07     | 6            | 288.98       | 17.1             | Upper-Mid 25% |
| 372  | 372        | Thea Hendricks         | Consumer    | 2422.82     | 5            | -135.21      | 17.1             | Upper-Mid 25% |
| 373  | 373        | Marc Harrigan          | Home Office | 2394.02     | 6            | 28.76        | 18.8             | Upper-Mid 25% |
| 374  | 374        | David Flashing         | Consumer    | 2390.53     | 3            | -259.31      | 28.3             | Upper-Mid 25% |
| 375  | 375        | Xylona Preis           | Consumer    | 2374.66     | 11           | 621.23       | 4.6              | Upper-Mid 25% |
| 376  | 376        | Clytie Kelty           | Consumer    | 2372.75     | 11           | 497.71       | 18.4             | Upper-Mid 25% |
| 377  | 377        | Jennifer Ferguson      | Consumer    | 2371.45     | 6            | 635.64       | 7.1              | Upper-Mid 25% |
| 378  | 378        | Cynthia Voltz          | Corporate   | 2370.31     | 9            | 99.0         | 24.3             | Upper-Mid 25% |
| 379  | 379        | Nick Radford           | Consumer    | 2367.28     | 5            | -25.15       | 22.3             | Upper-Mid 25% |
| 380  | 380        | Jack Garza             | Consumer    | 2358.68     | 3            | 684.19       | 24.3             | Upper-Mid 25% |
| 381  | 381        | Andrew Gjertsen        | Corporate   | 2356.86     | 8            | 295.67       | 20.5             | Upper-Mid 25% |
| 382  | 382        | Craig Leslie           | Home Office | 2353.59     | 5            | 229.01       | 18.8             | Upper-Mid 25% |
| 383  | 383        | Maureen Gastineau      | Home Office | 2350.19     | 4            | 25.89        | 22.5             | Upper-Mid 25% |
| 384  | 384        | Roland Fjeld           | Consumer    | 2341.3      | 7            | 711.62       | 1.4              | Upper-Mid 25% |
| 385  | 385        | Elizabeth Moffitt      | Corporate   | 2339.6      | 8            | 682.55       | 6.3              | Upper-Mid 25% |
| 386  | 386        | Dean Braden            | Consumer    | 2332.58     | 10           | 169.97       | 18.6             | Upper-Mid 25% |
| 387  | 387        | Chris McAfee           | Consumer    | 2305.71     | 5            | 365.04       | 7.5              | Upper-Mid 25% |
| 388  | 388        | Michael Kennedy        | Corporate   | 2302.37     | 8            | -405.36      | 30.0             | Upper-Mid 25% |
| 389  | 389        | Lena Hernandez         | Consumer    | 2295.33     | 9            | 526.07       | 12.7             | Upper-Mid 25% |
| 390  | 390        | Kristina Nunn          | Home Office | 2280.58     | 8            | 329.76       | 12.0             | Upper-Mid 25% |
| 391  | 391        | Jamie Frazer           | Consumer    | 2279.59     | 7            | 575.13       | 12.1             | Upper-Mid 25% |
| 392  | 392        | Fred Harton            | Consumer    | 2271.28     | 4            | 706.29       | 10.7             | Upper-Mid 25% |
| 393  | 393        | Craig Carreira         | Consumer    | 2269.7      | 7            | 187.84       | 16.8             | Upper-Mid 25% |
| 394  | 394        | Bobby Elias            | Consumer    | 2261.44     | 5            | 755.92       | 16.0             | Upper-Mid 25% |
| 395  | 395        | Kalyca Meade           | Corporate   | 2260.96     | 6            | 635.11       | 2.1              | Upper-Mid 25% |
| 396  | 396        | Matt Connell           | Corporate   | 2258.19     | 8            | 195.45       | 22.2             | Upper-Mid 25% |
| 397  | 397        | Justin Hirsh           | Consumer    | 2256.39     | 4            | -96.95       | 22.0             | Upper-Mid 25% |
| 398  | 398        | Maribeth Yedwab        | Corporate   | 2254.28     | 7            | 319.12       | 30.8             | Lower-Mid 25% |
| 399  | 399        | Ken Dana               | Corporate   | 2243.51     | 5            | 539.72       | 10.8             | Lower-Mid 25% |
| 400  | 400        | Tony Sayre             | Consumer    | 2243.27     | 6            | 11.38        | 19.3             | Lower-Mid 25% |
| 401  | 401        | Jason Gross            | Corporate   | 2240.58     | 6            | 3.8          | 25.5             | Lower-Mid 25% |
| 402  | 402        | Laurel Workman         | Corporate   | 2238.06     | 5            | 32.58        | 20.7             | Lower-Mid 25% |
| 403  | 403        | Allen Rosenblatt       | Corporate   | 2236.13     | 5            | -98.76       | 10.0             | Lower-Mid 25% |
| 404  | 404        | Greg Guthrie           | Corporate   | 2224.0      | 9            | 12.7         | 15.0             | Lower-Mid 25% |
| 405  | 405        | Nathan Cano            | Consumer    | 2218.99     | 6            | -2204.81     | 26.4             | Lower-Mid 25% |
| 406  | 406        | Mick Crebagga          | Consumer    | 2218.98     | 10           | -64.17       | 26.8             | Lower-Mid 25% |
| 407  | 407        | Dave Poirier           | Corporate   | 2215.0      | 8            | 563.18       | 11.4             | Lower-Mid 25% |
| 408  | 408        | Phillip Flathmann      | Consumer    | 2206.13     | 5            | 591.31       | 6.0              | Lower-Mid 25% |
| 409  | 409        | Maya Herman            | Corporate   | 2203.78     | 7            | 238.56       | 7.3              | Lower-Mid 25% |
| 410  | 410        | Janet Lee              | Consumer    | 2203.7      | 5            | 54.52        | 22.0             | Lower-Mid 25% |
| 411  | 411        | Justin Ritter          | Corporate   | 2201.69     | 5            | 452.37       | 22.0             | Lower-Mid 25% |
| 412  | 412        | Edward Nazzal          | Consumer    | 2199.37     | 4            | 496.11       | 4.4              | Lower-Mid 25% |
| 413  | 413        | Toby Braunhardt        | Consumer    | 2198.45     | 6            | 490.96       | 10.0             | Lower-Mid 25% |
| 414  | 414        | Giulietta Weimer       | Consumer    | 2189.02     | 7            | -268.54      | 15.6             | Lower-Mid 25% |
| 415  | 415        | Bill Tyler             | Corporate   | 2186.61     | 6            | 257.92       | 15.0             | Lower-Mid 25% |
| 416  | 416        | Pamela Stobb           | Consumer    | 2181.48     | 6            | -134.44      | 22.4             | Lower-Mid 25% |
| 417  | 417        | Shahid Hopkins         | Consumer    | 2180.72     | 10           | -144.52      | 23.3             | Lower-Mid 25% |
| 418  | 418        | Kean Nguyen            | Corporate   | 2171.96     | 5            | 114.31       | 28.1             | Lower-Mid 25% |
| 419  | 419        | Daniel Byrd            | Home Office | 2171.6      | 8            | 431.37       | 15.4             | Lower-Mid 25% |
| 420  | 420        | Roy Phan               | Corporate   | 2170.72     | 8            | 594.59       | 13.3             | Lower-Mid 25% |
| 421  | 421        | Theresa Swint          | Corporate   | 2163.62     | 6            | 260.87       | 22.4             | Lower-Mid 25% |
| 422  | 422        | Helen Abelman          | Consumer    | 2163.3      | 7            | 270.86       | 23.0             | Lower-Mid 25% |
| 423  | 423        | Ed Jacobs              | Consumer    | 2162.17     | 4            | 387.02       | 17.5             | Lower-Mid 25% |
| 424  | 424        | Neoma Murray           | Consumer    | 2161.98     | 10           | 788.95       | 26.0             | Lower-Mid 25% |
| 425  | 425        | John Dryer             | Consumer    | 2152.35     | 5            | -266.55      | 17.1             | Lower-Mid 25% |
| 426  | 426        | Clay Rozendal          | Home Office | 2148.85     | 4            | 74.4         | 13.3             | Lower-Mid 25% |
| 427  | 427        | Duane Noonan           | Consumer    | 2139.79     | 7            | 540.54       | 1.8              | Lower-Mid 25% |
| 428  | 428        | Karen Carlisle         | Corporate   | 2120.95     | 6            | 846.12       | 2.0              | Lower-Mid 25% |
| 429  | 429        | Stefanie Holloman      | Corporate   | 2096.39     | 2            | 260.63       | 20.0             | Lower-Mid 25% |
| 430  | 430        | Liz Carlisle           | Consumer    | 2095.06     | 5            | 86.78        | 27.2             | Lower-Mid 25% |
| 431  | 431        | Rob Haberlin           | Consumer    | 2085.74     | 3            | 172.63       | 10.9             | Lower-Mid 25% |
| 432  | 432        | Trudy Glocke           | Consumer    | 2074.66     | 4            | 365.72       | 13.0             | Lower-Mid 25% |
| 433  | 433        | Max Ludwig             | Home Office | 2071.91     | 7            | 409.51       | 10.8             | Lower-Mid 25% |
| 434  | 434        | Roger Barcio           | Home Office | 2067.45     | 4            | 243.08       | 15.7             | Lower-Mid 25% |
| 435  | 435        | Tom Stivers            | Corporate   | 2054.14     | 5            | 48.7         | 15.7             | Lower-Mid 25% |
| 436  | 436        | Art Ferguson           | Consumer    | 2052.91     | 7            | 317.97       | 20.0             | Lower-Mid 25% |
| 437  | 437        | Carlos Daly            | Consumer    | 2033.97     | 5            | 426.66       | 4.4              | Lower-Mid 25% |
| 438  | 438        | Nicole Fjeld           | Home Office | 2031.47     | 7            | 388.21       | 11.7             | Lower-Mid 25% |
| 439  | 439        | Denny Joy              | Corporate   | 2012.52     | 4            | 483.04       | 0.0              | Lower-Mid 25% |
| 440  | 440        | Victoria Brennan       | Corporate   | 2005.6      | 6            | 371.24       | 17.0             | Lower-Mid 25% |
| 441  | 441        | Harold Pawlan          | Home Office | 1990.31     | 7            | 373.86       | 30.0             | Lower-Mid 25% |
| 442  | 442        | Doug Bickford          | Consumer    | 1989.05     | 7            | 438.8        | 14.5             | Lower-Mid 25% |
| 443  | 443        | Paul Gonzalez          | Consumer    | 1987.16     | 9            | 334.52       | 9.4              | Lower-Mid 25% |
| 444  | 444        | Nona Balk              | Corporate   | 1972.6      | 9            | 117.64       | 17.4             | Lower-Mid 25% |
| 445  | 445        | Scott Williamson       | Consumer    | 1966.65     | 6            | 332.87       | 2.9              | Lower-Mid 25% |
| 446  | 446        | Lisa DeCherney         | Consumer    | 1961.93     | 4            | 557.17       | 2.9              | Lower-Mid 25% |
| 447  | 447        | Christy Brittain       | Consumer    | 1949.2      | 8            | 272.39       | 33.3             | Lower-Mid 25% |
| 448  | 448        | Tracy Poddar           | Corporate   | 1936.64     | 4            | 139.23       | 24.0             | Lower-Mid 25% |
| 449  | 449        | Jas O'Carroll          | Consumer    | 1934.27     | 6            | 202.14       | 17.3             | Lower-Mid 25% |
| 450  | 450        | Jay Fein               | Consumer    | 1911.84     | 6            | 330.2        | 7.5              | Lower-Mid 25% |
| 451  | 451        | Max Engle              | Consumer    | 1908.45     | 8            | 77.81        | 22.5             | Lower-Mid 25% |
| 452  | 452        | Susan Vittorini        | Consumer    | 1903.49     | 8            | 106.89       | 23.1             | Lower-Mid 25% |
| 453  | 453        | Katherine Ducich       | Consumer    | 1888.96     | 6            | 328.59       | 13.0             | Lower-Mid 25% |
| 454  | 454        | Giulietta Dortch       | Corporate   | 1888.07     | 4            | 230.94       | 13.3             | Lower-Mid 25% |
| 455  | 455        | Sheri Gordon           | Consumer    | 1884.8      | 8            | -119.01      | 15.0             | Lower-Mid 25% |
| 456  | 456        | Lisa Ryan              | Corporate   | 1879.31     | 5            | -382.81      | 27.5             | Lower-Mid 25% |
| 457  | 457        | Shaun Chance           | Corporate   | 1875.0      | 7            | 379.56       | 28.0             | Lower-Mid 25% |
| 458  | 458        | Brooke Gillingham      | Corporate   | 1874.17     | 6            | 107.57       | 13.8             | Lower-Mid 25% |
| 459  | 459        | Stephanie Phelps       | Corporate   | 1872.44     | 9            | 268.48       | 15.3             | Lower-Mid 25% |
| 460  | 460        | Nat Gilpin             | Corporate   | 1869.58     | 5            | 313.63       | 8.8              | Lower-Mid 25% |
| 461  | 461        | Cynthia Delaney        | Home Office | 1860.73     | 5            | 403.84       | 2.7              | Lower-Mid 25% |
| 462  | 462        | Skye Norling           | Home Office | 1860.42     | 6            | -716.86      | 17.3             | Lower-Mid 25% |
| 463  | 463        | Patrick Ryan           | Consumer    | 1840.18     | 5            | 247.62       | 11.7             | Lower-Mid 25% |
| 464  | 464        | Ashley Jarboe          | Consumer    | 1839.24     | 7            | 521.14       | 4.0              | Lower-Mid 25% |
| 465  | 465        | Pamela Coakley         | Corporate   | 1832.06     | 4            | 272.69       | 22.0             | Lower-Mid 25% |
| 466  | 466        | Emily Grady            | Consumer    | 1832.02     | 5            | 104.27       | 20.0             | Lower-Mid 25% |
| 467  | 467        | Pauline Johnson        | Consumer    | 1824.23     | 7            | 683.0        | 8.0              | Lower-Mid 25% |
| 468  | 468        | Noah Childs            | Corporate   | 1821.74     | 5            | -359.02      | 24.4             | Lower-Mid 25% |
| 469  | 469        | Janet Molinari         | Corporate   | 1804.15     | 5            | 502.61       | 13.8             | Lower-Mid 25% |
| 470  | 470        | Jennifer Braxton       | Corporate   | 1791.61     | 10           | 156.05       | 20.6             | Lower-Mid 25% |
| 471  | 471        | Andrew Allen           | Consumer    | 1790.51     | 4            | 435.83       | 1.7              | Lower-Mid 25% |
| 472  | 472        | Chad Cunningham        | Home Office | 1770.95     | 6            | 208.59       | 21.5             | Lower-Mid 25% |
| 473  | 473        | Darrin Sayre           | Home Office | 1762.21     | 4            | 193.33       | 13.9             | Lower-Mid 25% |
| 474  | 474        | Monica Federle         | Corporate   | 1758.3      | 5            | 456.86       | 6.7              | Lower-Mid 25% |
| 475  | 475        | Aaron Hawkins          | Corporate   | 1744.7      | 7            | 365.22       | 9.1              | Lower-Mid 25% |
| 476  | 476        | Logan Haushalter       | Consumer    | 1739.69     | 9            | 316.52       | 7.9              | Lower-Mid 25% |
| 477  | 477        | Ben Wallace            | Consumer    | 1738.41     | 6            | 247.0        | 15.0             | Lower-Mid 25% |
| 478  | 478        | Valerie Takahito       | Home Office | 1736.6      | 2            | -224.09      | 33.3             | Lower-Mid 25% |
| 479  | 479        | Adrian Hane            | Home Office | 1735.51     | 7            | -2.31        | 23.8             | Lower-Mid 25% |
| 480  | 480        | Mike Vittorini         | Consumer    | 1734.57     | 7            | 273.86       | 8.6              | Lower-Mid 25% |
| 481  | 481        | Jessica Myrick         | Consumer    | 1733.44     | 7            | 356.54       | 9.0              | Lower-Mid 25% |
| 482  | 482        | Brad Eason             | Home Office | 1727.65     | 6            | 139.2        | 14.6             | Lower-Mid 25% |
| 483  | 483        | Denny Blanton          | Consumer    | 1711.69     | 4            | 438.91       | 2.9              | Lower-Mid 25% |
| 484  | 484        | Julie Prescott         | Home Office | 1707.71     | 9            | 309.71       | 15.4             | Lower-Mid 25% |
| 485  | 485        | Tracy Zic              | Consumer    | 1707.29     | 4            | 224.89       | 8.9              | Lower-Mid 25% |
| 486  | 486        | Becky Pak              | Consumer    | 1697.86     | 6            | 647.38       | 8.2              | Lower-Mid 25% |
| 487  | 487        | Darren Koutras         | Consumer    | 1687.04     | 5            | -107.35      | 16.3             | Lower-Mid 25% |
| 488  | 488        | Meg O'Connel           | Home Office | 1687.03     | 8            | 169.34       | 16.4             | Lower-Mid 25% |
| 489  | 489        | Ryan Akin              | Consumer    | 1686.92     | 5            | -445.7       | 31.7             | Lower-Mid 25% |
| 490  | 490        | Katrina Edelman        | Corporate   | 1686.73     | 8            | 397.88       | 21.5             | Lower-Mid 25% |
| 491  | 491        | Cathy Armstrong        | Home Office | 1679.72     | 5            | 211.26       | 30.0             | Lower-Mid 25% |
| 492  | 492        | Candace McMahon        | Corporate   | 1673.89     | 6            | 214.46       | 12.0             | Lower-Mid 25% |
| 493  | 493        | Jennifer Patt          | Corporate   | 1669.14     | 7            | 429.75       | 14.0             | Lower-Mid 25% |
| 494  | 494        | Chad McGuire           | Consumer    | 1661.61     | 4            | 409.07       | 2.9              | Lower-Mid 25% |
| 495  | 495        | Cindy Chapman          | Consumer    | 1659.44     | 9            | 154.85       | 16.2             | Lower-Mid 25% |
| 496  | 496        | Erica Bern             | Corporate   | 1643.26     | 4            | 162.88       | 28.3             | Lower-Mid 25% |
| 497  | 497        | Anne Pryor             | Home Office | 1638.55     | 8            | 285.79       | 16.3             | Lower-Mid 25% |
| 498  | 498        | Annie Zypern           | Consumer    | 1622.02     | 6            | 154.95       | 12.5             | Lower-Mid 25% |
| 499  | 499        | Maurice Satty          | Consumer    | 1613.4      | 6            | 247.43       | 22.0             | Lower-Mid 25% |
| 500  | 500        | Tim Brockman           | Consumer    | 1602.38     | 7            | 260.62       | 24.7             | Lower-Mid 25% |
| 501  | 501        | Craig Reiter           | Consumer    | 1600.55     | 4            | 306.92       | 26.7             | Lower-Mid 25% |
| 502  | 502        | Alan Haines            | Corporate   | 1587.45     | 4            | -378.55      | 35.0             | Lower-Mid 25% |
| 503  | 503        | Benjamin Farhat        | Home Office | 1585.16     | 4            | 523.21       | 5.0              | Lower-Mid 25% |
| 504  | 504        | Cyma Kinney            | Corporate   | 1582.11     | 9            | -338.43      | 15.0             | Lower-Mid 25% |
| 505  | 505        | Mike Caudle            | Corporate   | 1582.0      | 5            | 121.76       | 5.5              | Lower-Mid 25% |
| 506  | 506        | James Lanier           | Home Office | 1571.52     | 5            | 209.28       | 21.4             | Lower-Mid 25% |
| 507  | 507        | Karl Braun             | Consumer    | 1569.46     | 9            | 49.72        | 19.5             | Lower-Mid 25% |
| 508  | 508        | George Bell            | Corporate   | 1568.44     | 11           | 7.84         | 17.0             | Lower-Mid 25% |
| 509  | 509        | Odella Nelson          | Corporate   | 1567.52     | 9            | -5.89        | 16.0             | Lower-Mid 25% |
| 510  | 510        | Mark Van Huff          | Consumer    | 1560.05     | 9            | 189.03       | 24.0             | Lower-Mid 25% |
| 511  | 511        | Maria Bertelson        | Consumer    | 1548.7      | 10           | 212.43       | 17.4             | Lower-Mid 25% |
| 512  | 512        | Brian DeCherney        | Consumer    | 1538.11     | 6            | 206.76       | 17.5             | Lower-Mid 25% |
| 513  | 513        | Cathy Hwang            | Home Office | 1537.24     | 3            | 195.15       | 15.0             | Lower-Mid 25% |
| 514  | 514        | Bruce Degenhardt       | Consumer    | 1526.5      | 6            | 333.98       | 2.0              | Lower-Mid 25% |
| 515  | 515        | Benjamin Venier        | Corporate   | 1523.27     | 5            | 315.22       | 9.3              | Lower-Mid 25% |
| 516  | 516        | Kelly Andreada         | Consumer    | 1519.51     | 7            | 234.92       | 5.5              | Lower-Mid 25% |
| 517  | 517        | Ann Blume              | Corporate   | 1515.86     | 4            | -274.96      | 37.5             | Lower-Mid 25% |
| 518  | 518        | John Grady             | Corporate   | 1507.02     | 6            | 206.1        | 6.7              | Lower-Mid 25% |
| 519  | 519        | Dan Lawera             | Consumer    | 1503.11     | 8            | 322.24       | 15.0             | Lower-Mid 25% |
| 520  | 520        | Zuschuss Donatelli     | Consumer    | 1493.94     | 5            | 249.13       | 11.1             | Lower-Mid 25% |
| 521  | 521        | Charlotte Melton       | Consumer    | 1475.14     | 6            | 91.2         | 7.1              | Lower-Mid 25% |
| 522  | 522        | Laurel Elliston        | Consumer    | 1469.45     | 6            | 161.76       | 25.6             | Lower-Mid 25% |
| 523  | 523        | Ted Butterfield        | Consumer    | 1467.88     | 5            | 390.21       | 5.6              | Lower-Mid 25% |
| 524  | 524        | Parhena Norris         | Home Office | 1467.15     | 8            | 192.04       | 12.3             | Lower-Mid 25% |
| 525  | 525        | Ralph Kennedy          | Consumer    | 1460.19     | 3            | 269.69       | 7.5              | Lower-Mid 25% |
| 526  | 526        | Bradley Nguyen         | Consumer    | 1459.34     | 5            | 340.71       | 2.4              | Lower-Mid 25% |
| 527  | 527        | Delfina Latchford      | Consumer    | 1458.26     | 8            | 288.87       | 18.2             | Lower-Mid 25% |
| 528  | 528        | Philip Brown           | Consumer    | 1456.95     | 8            | 280.66       | 12.7             | Lower-Mid 25% |
| 529  | 529        | Andy Gerbode           | Corporate   | 1455.04     | 4            | -152.76      | 15.6             | Lower-Mid 25% |
| 530  | 530        | Raymond Messe          | Consumer    | 1453.47     | 6            | 392.15       | 4.4              | Lower-Mid 25% |
| 531  | 531        | Paul Knutson           | Home Office | 1441.15     | 2            | -798.71      | 36.7             | Lower-Mid 25% |
| 532  | 532        | Tamara Dahlen          | Consumer    | 1434.55     | 9            | 88.19        | 24.4             | Lower-Mid 25% |
| 533  | 533        | Julia West             | Consumer    | 1428.73     | 4            | 154.06       | 32.9             | Lower-Mid 25% |
| 534  | 534        | Mick Brown             | Consumer    | 1428.23     | 7            | 117.81       | 20.0             | Lower-Mid 25% |
| 535  | 535        | Thomas Thornton        | Consumer    | 1427.04     | 8            | 278.74       | 21.3             | Lower-Mid 25% |
| 536  | 536        | Christine Abelman      | Corporate   | 1421.95     | 4            | 246.02       | 11.8             | Lower-Mid 25% |
| 537  | 537        | Roger Demir            | Consumer    | 1419.74     | 10           | 207.33       | 15.7             | Lower-Mid 25% |
| 538  | 538        | Nancy Lomonaco         | Home Office | 1418.09     | 4            | 343.64       | 6.0              | Lower-Mid 25% |
| 539  | 539        | Jill Stevenson         | Corporate   | 1417.65     | 4            | -175.55      | 31.3             | Lower-Mid 25% |
| 540  | 540        | Paul MacIntyre         | Consumer    | 1405.4      | 3            | 157.88       | 15.0             | Lower-Mid 25% |
| 541  | 541        | Guy Armstrong          | Consumer    | 1398.38     | 11           | 136.71       | 18.0             | Lower-Mid 25% |
| 542  | 542        | Cyra Reiten            | Home Office | 1397.87     | 3            | 83.27        | 13.1             | Lower-Mid 25% |
| 543  | 543        | Nathan Gelder          | Consumer    | 1395.94     | 5            | 217.09       | 11.1             | Lower-Mid 25% |
| 544  | 544        | Jeremy Ellison         | Consumer    | 1388.68     | 6            | 276.22       | 18.5             | Lower-Mid 25% |
| 545  | 545        | Troy Blackwell         | Consumer    | 1387.56     | 5            | -136.41      | 27.1             | Lower-Mid 25% |
| 546  | 546        | Frank Gastineau        | Home Office | 1383.14     | 7            | 394.74       | 11.8             | Lower-Mid 25% |
| 547  | 547        | Don Miller             | Corporate   | 1376.79     | 3            | 199.77       | 17.0             | Lower-Mid 25% |
| 548  | 548        | Gene Hale              | Corporate   | 1361.24     | 2            | -95.45       | 46.7             | Lower-Mid 25% |
| 549  | 549        | Sarah Bern             | Consumer    | 1348.02     | 3            | 157.67       | 18.6             | Lower-Mid 25% |
| 550  | 550        | Liz MacKendrick        | Consumer    | 1346.77     | 5            | -44.88       | 5.7              | Lower-Mid 25% |
| 551  | 551        | Maureen Gnade          | Consumer    | 1342.28     | 3            | -398.79      | 25.7             | Lower-Mid 25% |
| 552  | 552        | Sarah Jordon           | Consumer    | 1341.04     | 6            | -23.51       | 37.0             | Lower-Mid 25% |
| 553  | 553        | Bryan Mills            | Consumer    | 1338.84     | 10           | 137.74       | 25.0             | Lower-Mid 25% |
| 554  | 554        | Barry Franz            | Home Office | 1333.88     | 4            | -291.38      | 18.0             | Lower-Mid 25% |
| 555  | 555        | Saphhira Shifley       | Corporate   | 1324.03     | 8            | 332.35       | 11.4             | Lower-Mid 25% |
| 556  | 556        | Dario Medina           | Corporate   | 1322.03     | 7            | 108.76       | 16.7             | Lower-Mid 25% |
| 557  | 557        | Michelle Tran          | Home Office | 1319.45     | 4            | -23.68       | 24.3             | Lower-Mid 25% |
| 558  | 558        | Shirley Jackson        | Consumer    | 1318.78     | 5            | 68.1         | 14.3             | Lower-Mid 25% |
| 559  | 559        | Magdelene Morse        | Consumer    | 1314.02     | 4            | 178.4        | 13.3             | Lower-Mid 25% |
| 560  | 560        | Sibella Parks          | Corporate   | 1306.09     | 6            | -118.78      | 26.0             | Lower-Mid 25% |
| 561  | 561        | Matt Collins           | Consumer    | 1303.89     | 8            | 210.75       | 29.1             | Lower-Mid 25% |
| 562  | 562        | Eileen Kiefer          | Home Office | 1303.48     | 4            | 97.11        | 8.8              | Lower-Mid 25% |
| 563  | 563        | Corey-Lock             | Consumer    | 1300.08     | 5            | 205.63       | 17.5             | Lower-Mid 25% |
| 564  | 564        | Denny Ordway           | Consumer    | 1300.03     | 9            | -38.91       | 15.8             | Lower-Mid 25% |
| 565  | 565        | Hallie Redmond         | Home Office | 1299.29     | 5            | 185.58       | 4.6              | Lower-Mid 25% |
| 566  | 566        | Georgia Rosenberg      | Corporate   | 1284.38     | 2            | 359.83       | 0.0              | Lower-Mid 25% |
| 567  | 567        | Cari Sayre             | Corporate   | 1278.95     | 5            | 185.38       | 27.5             | Lower-Mid 25% |
| 568  | 568        | Paul Stevenson         | Home Office | 1278.64     | 8            | 198.51       | 5.4              | Lower-Mid 25% |
| 569  | 569        | Stuart Van             | Corporate   | 1271.09     | 4            | 199.65       | 20.0             | Lower-Mid 25% |
| 570  | 570        | Doug O'Connell         | Consumer    | 1267.32     | 7            | 294.07       | 9.1              | Lower-Mid 25% |
| 571  | 571        | Carl Ludwig            | Consumer    | 1262.01     | 4            | 328.08       | 5.7              | Lower-Mid 25% |
| 572  | 572        | Liz Willingham         | Consumer    | 1259.04     | 3            | 192.63       | 0.0              | Lower-Mid 25% |
| 573  | 573        | Michelle Ellison       | Corporate   | 1256.94     | 4            | 107.36       | 16.7             | Lower-Mid 25% |
| 574  | 574        | Gene McClure           | Consumer    | 1255.68     | 10           | 441.32       | 11.5             | Lower-Mid 25% |
| 575  | 575        | Steve Carroll          | Home Office | 1254.64     | 6            | 370.16       | 0.0              | Lower-Mid 25% |
| 576  | 576        | Matt Hagelstein        | Corporate   | 1252.8      | 4            | 122.36       | 23.3             | Lower-Mid 25% |
| 577  | 577        | Elpida Rittenbach      | Corporate   | 1245.79     | 3            | -295.74      | 20.0             | Lower-Mid 25% |
| 578  | 578        | Tony Chapman           | Home Office | 1244.98     | 9            | 119.1        | 26.4             | Lower-Mid 25% |
| 579  | 579        | Joni Wasserman         | Consumer    | 1244.09     | 7            | -29.58       | 8.2              | Lower-Mid 25% |
| 580  | 580        | Michael Grace          | Home Office | 1242.83     | 5            | -470.77      | 24.3             | Lower-Mid 25% |
| 581  | 581        | Nora Pelletier         | Home Office | 1228.7      | 6            | 514.5        | 18.6             | Lower-Mid 25% |
| 582  | 582        | Patrick Jones          | Corporate   | 1220.09     | 8            | 442.14       | 7.7              | Lower-Mid 25% |
| 583  | 583        | Erica Hernandez        | Home Office | 1219.53     | 7            | -94.14       | 17.3             | Lower-Mid 25% |
| 584  | 584        | Jack Lebron            | Consumer    | 1214.96     | 6            | -207.8       | 26.7             | Lower-Mid 25% |
| 585  | 585        | Christina DeMoss       | Consumer    | 1205.58     | 2            | 233.03       | 8.5              | Lower-Mid 25% |
| 586  | 586        | Michael Dominguez      | Corporate   | 1204.91     | 5            | -4.04        | 28.7             | Lower-Mid 25% |
| 587  | 587        | Dorothy Wardle         | Corporate   | 1204.85     | 7            | -266.9       | 17.0             | Lower-Mid 25% |
| 588  | 588        | Evan Bailliet          | Consumer    | 1186.33     | 6            | 282.17       | 22.9             | Lower-Mid 25% |
| 589  | 589        | Benjamin Patterson     | Consumer    | 1181.49     | 5            | -197.27      | 6.7              | Lower-Mid 25% |
| 590  | 590        | Debra Catini           | Consumer    | 1174.62     | 5            | 132.07       | 7.9              | Lower-Mid 25% |
| 591  | 591        | Alyssa Tate            | Home Office | 1171.81     | 6            | 100.88       | 20.0             | Lower-Mid 25% |
| 592  | 592        | Jim Radford            | Consumer    | 1156.66     | 2            | -785.16      | 30.0             | Lower-Mid 25% |
| 593  | 593        | Duane Benoit           | Consumer    | 1155.2      | 7            | 177.67       | 16.0             | Lower-Mid 25% |
| 594  | 594        | Claire Gute            | Consumer    | 1148.78     | 3            | 169.93       | 20.0             | Lower-Mid 25% |
| 595  | 595        | Kimberly Carter        | Corporate   | 1146.05     | 4            | 156.78       | 8.6              | Lower-Mid 25% |
| 596  | 596        | Ross DeVincentis       | Home Office | 1137.62     | 8            | 318.46       | 18.8             | Bottom 25%    |
| 597  | 597        | Carl Weiss             | Home Office | 1136.59     | 6            | 370.83       | 9.1              | Bottom 25%    |
| 598  | 598        | Jim Sink               | Corporate   | 1131.06     | 4            | -54.87       | 20.9             | Bottom 25%    |
| 599  | 599        | Darrin Van Huff        | Corporate   | 1119.48     | 5            | -427.18      | 17.2             | Bottom 25%    |
| 600  | 600        | Alan Barnes            | Consumer    | 1113.84     | 8            | 220.81       | 13.6             | Bottom 25%    |
| 601  | 601        | Tony Molinari          | Consumer    | 1094.68     | 3            | 292.52       | 5.0              | Bottom 25%    |
| 602  | 602        | Jesus Ocampo           | Home Office | 1090.84     | 5            | 167.67       | 23.6             | Bottom 25%    |
| 603  | 603        | Scot Wooten            | Consumer    | 1085.08     | 7            | -19.61       | 26.0             | Bottom 25%    |
| 604  | 604        | Jeremy Farry           | Consumer    | 1082.92     | 11           | -18.07       | 14.7             | Bottom 25%    |
| 605  | 605        | Dennis Bolton          | Home Office | 1081.47     | 5            | 291.01       | 8.3              | Bottom 25%    |
| 606  | 606        | David Wiener           | Corporate   | 1080.75     | 6            | -86.87       | 24.4             | Bottom 25%    |
| 607  | 607        | Cindy Schnelling       | Corporate   | 1077.23     | 4            | -302.88      | 25.0             | Bottom 25%    |
| 608  | 608        | Pauline Chand          | Home Office | 1061.49     | 2            | -184.34      | 13.3             | Bottom 25%    |
| 609  | 609        | David Philippe         | Consumer    | 1058.62     | 2            | -40.94       | 15.0             | Bottom 25%    |
| 610  | 610        | Jenna Caffey           | Consumer    | 1058.11     | 1            | 502.92       | 5.0              | Bottom 25%    |
| 611  | 611        | Phillina Ober          | Home Office | 1056.86     | 5            | -49.7        | 19.0             | Bottom 25%    |
| 612  | 612        | Allen Armold           | Consumer    | 1056.39     | 9            | 277.38       | 8.0              | Bottom 25%    |
| 613  | 613        | Vivek Sundaresam       | Consumer    | 1055.98     | 4            | -262.81      | 47.5             | Bottom 25%    |
| 614  | 614        | Alex Russell           | Corporate   | 1055.69     | 4            | -221.05      | 26.0             | Bottom 25%    |
| 615  | 615        | Darren Powers          | Consumer    | 1050.64     | 9            | 241.45       | 21.2             | Bottom 25%    |
| 616  | 616        | Duane Huffman          | Home Office | 1043.1      | 4            | 116.67       | 12.3             | Bottom 25%    |
| 617  | 617        | Susan MacKendrick      | Consumer    | 1043.04     | 1            | -237.29      | 28.3             | Bottom 25%    |
| 618  | 618        | Eudokia Martin         | Corporate   | 1041.04     | 4            | 240.24       | 10.0             | Bottom 25%    |
| 619  | 619        | Theresa Coyne          | Corporate   | 1038.26     | 1            | 265.53       | 0.0              | Bottom 25%    |
| 620  | 620        | Mike Kennedy           | Consumer    | 1031.6      | 4            | 227.83       | 8.2              | Bottom 25%    |
| 621  | 621        | Tiffany House          | Corporate   | 1022.2      | 8            | 92.73        | 20.8             | Bottom 25%    |
| 622  | 622        | Sean Wendt             | Home Office | 1019.04     | 3            | 95.84        | 21.7             | Bottom 25%    |
| 623  | 623        | Luke Schmidt           | Corporate   | 1010.26     | 6            | 244.2        | 20.0             | Bottom 25%    |
| 624  | 624        | Randy Bradley          | Consumer    | 1008.2      | 2            | -164.41      | 31.7             | Bottom 25%    |
| 625  | 625        | Lynn Smith             | Consumer    | 1008.14     | 6            | 348.36       | 8.3              | Bottom 25%    |
| 626  | 626        | Bruce Geld             | Consumer    | 1006.36     | 6            | 119.35       | 14.3             | Bottom 25%    |
| 627  | 627        | Victor Preis           | Home Office | 993.9       | 3            | 205.39       | 4.0              | Bottom 25%    |
| 628  | 628        | Ken Brennan            | Corporate   | 983.92      | 7            | 293.55       | 26.7             | Bottom 25%    |
| 629  | 629        | Barry Pond             | Corporate   | 983.42      | 5            | 209.78       | 14.3             | Bottom 25%    |
| 630  | 630        | Toby Swindell          | Consumer    | 974.78      | 5            | -184.98      | 28.3             | Bottom 25%    |
| 631  | 631        | Russell D'Ascenzo      | Consumer    | 970.94      | 4            | 35.06        | 31.0             | Bottom 25%    |
| 632  | 632        | Aimee Bixby            | Consumer    | 966.71      | 5            | 313.66       | 13.3             | Bottom 25%    |
| 633  | 633        | Roy Collins            | Consumer    | 966.41      | 6            | 63.99        | 11.0             | Bottom 25%    |
| 634  | 634        | Sung Shariari          | Consumer    | 964.64      | 5            | -75.59       | 24.0             | Bottom 25%    |
| 635  | 635        | Jonathan Howell        | Consumer    | 959.48      | 7            | -13.55       | 14.4             | Bottom 25%    |
| 636  | 636        | Jason Fortune-         | Consumer    | 955.12      | 5            | 97.29        | 11.4             | Bottom 25%    |
| 637  | 637        | Rachel Payne           | Corporate   | 954.65      | 4            | 59.54        | 19.3             | Bottom 25%    |
| 638  | 638        | Bryan Spruell          | Home Office | 949.43      | 2            | 194.05       | 0.0              | Bottom 25%    |
| 639  | 639        | Roy Französisch        | Consumer    | 945.22      | 8            | 280.03       | 8.2              | Bottom 25%    |
| 640  | 640        | Eric Barreto           | Consumer    | 944.6       | 5            | 0.6          | 17.1             | Bottom 25%    |
| 641  | 641        | Maureen Fritzler       | Corporate   | 937.04      | 5            | -341.53      | 13.7             | Bottom 25%    |
| 642  | 642        | Eric Murdock           | Consumer    | 933.7       | 5            | 102.3        | 23.3             | Bottom 25%    |
| 643  | 643        | Alyssa Crouse          | Corporate   | 925.8       | 3            | -62.13       | 32.0             | Bottom 25%    |
| 644  | 644        | Evan Henry             | Consumer    | 923.88      | 6            | 242.11       | 28.7             | Bottom 25%    |
| 645  | 645        | Mary O'Rourke          | Consumer    | 922.49      | 4            | 59.36        | 22.0             | Bottom 25%    |
| 646  | 646        | Alejandro Ballentine   | Home Office | 914.53      | 9            | 264.57       | 10.0             | Bottom 25%    |
| 647  | 647        | Katrina Bavinger       | Home Office | 908.82      | 3            | 274.3        | 4.4              | Bottom 25%    |
| 648  | 648        | Catherine Glotzbach    | Home Office | 904.47      | 6            | 86.51        | 18.9             | Bottom 25%    |
| 649  | 649        | Sonia Cooley           | Consumer    | 902.73      | 5            | 100.23       | 34.3             | Bottom 25%    |
| 650  | 650        | Joni Blumstein         | Consumer    | 900.55      | 3            | -286.98      | 30.0             | Bottom 25%    |
| 651  | 651        | Henia Zydlo            | Consumer    | 886.52      | 5            | -130.39      | 20.0             | Bottom 25%    |
| 652  | 652        | Aaron Bergman          | Consumer    | 886.16      | 3            | 129.35       | 6.7              | Bottom 25%    |
| 653  | 653        | Ryan Crowe             | Consumer    | 885.75      | 6            | 10.56        | 17.3             | Bottom 25%    |
| 654  | 654        | Chad Sievert           | Consumer    | 884.64      | 4            | 143.83       | 11.4             | Bottom 25%    |
| 655  | 655        | Harold Engle           | Corporate   | 883.53      | 4            | 274.4        | 1.8              | Bottom 25%    |
| 656  | 656        | Sally Knutson          | Consumer    | 883.41      | 3            | 168.79       | 22.0             | Bottom 25%    |
| 657  | 657        | Richard Eichhorn       | Consumer    | 876.7       | 5            | 209.23       | 13.3             | Bottom 25%    |
| 658  | 658        | Jim Mitchum            | Corporate   | 864.95      | 5            | 117.2        | 15.8             | Bottom 25%    |
| 659  | 659        | Jocasta Rupert         | Consumer    | 863.88      | 1            | 107.99       | 20.0             | Bottom 25%    |
| 660  | 660        | Art Foster             | Consumer    | 861.57      | 4            | -163.12      | 25.7             | Bottom 25%    |
| 661  | 661        | Julie Creighton        | Corporate   | 858.58      | 5            | 201.6        | 4.4              | Bottom 25%    |
| 662  | 662        | Michael Stewart        | Corporate   | 855.12      | 6            | 55.23        | 17.3             | Bottom 25%    |
| 663  | 663        | Vicky Freymann         | Home Office | 847.94      | 5            | -96.28       | 6.4              | Bottom 25%    |
| 664  | 664        | Vivek Gonzalez         | Consumer    | 846.01      | 6            | 143.63       | 7.5              | Bottom 25%    |
| 665  | 665        | Charles Sheldon        | Corporate   | 844.46      | 5            | 113.14       | 16.3             | Bottom 25%    |
| 666  | 666        | Todd Boyes             | Corporate   | 834.33      | 5            | 268.97       | 6.2              | Bottom 25%    |
| 667  | 667        | Ann Steele             | Home Office | 833.4       | 7            | 136.49       | 18.3             | Bottom 25%    |
| 668  | 668        | Erica Hackney          | Consumer    | 825.95      | 6            | 150.38       | 6.3              | Bottom 25%    |
| 669  | 669        | Thomas Brumley         | Home Office | 816.17      | 4            | 179.0        | 2.5              | Bottom 25%    |
| 670  | 670        | Alice McCarthy         | Corporate   | 814.01      | 5            | 194.99       | 12.5             | Bottom 25%    |
| 671  | 671        | Brendan Murry          | Corporate   | 808.16      | 6            | 95.58        | 18.0             | Bottom 25%    |
| 672  | 672        | David Kendrick         | Corporate   | 797.83      | 2            | 249.94       | 12.0             | Bottom 25%    |
| 673  | 673        | Matthew Clasen         | Corporate   | 795.15      | 4            | -247.94      | 17.5             | Bottom 25%    |
| 674  | 674        | Beth Fritzler          | Corporate   | 791.99      | 3            | 25.87        | 15.0             | Bottom 25%    |
| 675  | 675        | Harry Greene           | Consumer    | 785.63      | 5            | 147.0        | 19.0             | Bottom 25%    |
| 676  | 676        | Michael Granlund       | Home Office | 776.38      | 9            | 171.74       | 11.9             | Bottom 25%    |
| 677  | 677        | Muhammed MacIntyre     | Corporate   | 775.41      | 9            | 58.89        | 14.2             | Bottom 25%    |
| 678  | 678        | Sandra Flanagan        | Consumer    | 763.55      | 7            | 228.16       | 10.0             | Bottom 25%    |
| 679  | 679        | Steven Ward            | Corporate   | 758.7       | 2            | 68.24        | 10.0             | Bottom 25%    |
| 680  | 680        | Liz Pelletier          | Consumer    | 756.61      | 4            | 110.78       | 11.1             | Bottom 25%    |
| 681  | 681        | Dorris liebe           | Corporate   | 755.6       | 5            | 175.24       | 21.7             | Bottom 25%    |
| 682  | 682        | Ivan Gibson            | Consumer    | 744.57      | 4            | 320.5        | 2.9              | Bottom 25%    |
| 683  | 683        | Barry Blumstein        | Corporate   | 744.34      | 5            | 11.58        | 20.0             | Bottom 25%    |
| 684  | 684        | Tracy Collins          | Home Office | 742.56      | 7            | 217.93       | 11.0             | Bottom 25%    |
| 685  | 685        | Michelle Lonsdale      | Corporate   | 742.08      | 3            | 138.72       | 25.0             | Bottom 25%    |
| 686  | 686        | Ritsa Hightower        | Consumer    | 740.38      | 2            | 0.31         | 53.3             | Bottom 25%    |
| 687  | 687        | Patrick Bzostek        | Home Office | 740.36      | 3            | 229.23       | 12.0             | Bottom 25%    |
| 688  | 688        | Angele Hood            | Consumer    | 738.5       | 4            | 83.96        | 12.0             | Bottom 25%    |
| 689  | 689        | Henry MacAllister      | Consumer    | 736.28      | 4            | 117.28       | 17.1             | Bottom 25%    |
| 690  | 690        | Patricia Hirasaki      | Home Office | 729.65      | 1            | 47.89        | 20.0             | Bottom 25%    |
| 691  | 691        | Pete Armstrong         | Home Office | 729.41      | 6            | 225.86       | 18.6             | Bottom 25%    |
| 692  | 692        | Jennifer Jackson       | Consumer    | 709.18      | 5            | 200.56       | 6.7              | Bottom 25%    |
| 693  | 693        | Julia Dunbar           | Consumer    | 695.44      | 3            | 111.11       | 5.0              | Bottom 25%    |
| 694  | 694        | Peter Bühler           | Consumer    | 688.32      | 4            | 218.16       | 12.0             | Bottom 25%    |
| 695  | 695        | Eric Hoffmann          | Consumer    | 684.17      | 8            | 53.54        | 29.4             | Bottom 25%    |
| 696  | 696        | Toby Ritter            | Consumer    | 675.94      | 5            | 220.36       | 2.9              | Bottom 25%    |
| 697  | 697        | Alex Grayson           | Consumer    | 660.97      | 5            | -5.14        | 23.3             | Bottom 25%    |
| 698  | 698        | Berenike Kampe         | Consumer    | 659.14      | 6            | -63.76       | 20.6             | Bottom 25%    |
| 699  | 699        | Bryan Davis            | Consumer    | 658.47      | 6            | 141.26       | 12.0             | Bottom 25%    |
| 700  | 700        | Anna Chung             | Consumer    | 657.32      | 5            | -28.7        | 18.3             | Bottom 25%    |
| 701  | 701        | Anthony Witt           | Consumer    | 649.38      | 4            | 65.77        | 20.0             | Bottom 25%    |
| 702  | 702        | Lori Olson             | Corporate   | 644.35      | 5            | 150.17       | 25.6             | Bottom 25%    |
| 703  | 703        | Joy Bell-              | Consumer    | 644.12      | 7            | 126.76       | 7.4              | Bottom 25%    |
| 704  | 704        | Carol Darley           | Consumer    | 639.77      | 3            | -206.72      | 43.3             | Bottom 25%    |
| 705  | 705        | Mathew Reese           | Home Office | 639.18      | 4            | 162.94       | 20.0             | Bottom 25%    |
| 706  | 706        | Astrea Jones           | Consumer    | 629.25      | 3            | 60.43        | 4.0              | Bottom 25%    |
| 707  | 707        | Ralph Ritter           | Consumer    | 615.93      | 2            | -73.83       | 27.5             | Bottom 25%    |
| 708  | 708        | Shirley Schmidt        | Home Office | 613.4       | 3            | 199.93       | 0.0              | Bottom 25%    |
| 709  | 709        | Bobby Trafton          | Consumer    | 603.88      | 4            | -77.53       | 15.7             | Bottom 25%    |
| 710  | 710        | Barbara Fisher         | Corporate   | 599.8       | 7            | 227.44       | 14.6             | Bottom 25%    |
| 711  | 711        | Maria Zettner          | Home Office | 593.61      | 4            | 85.02        | 6.7              | Bottom 25%    |
| 712  | 712        | Denise Leinenbach      | Consumer    | 585.02      | 4            | 222.68       | 5.0              | Bottom 25%    |
| 713  | 713        | Alan Shonely           | Consumer    | 584.61      | 7            | 33.72        | 26.9             | Bottom 25%    |
| 714  | 714        | Brian Derr             | Consumer    | 582.65      | 3            | 141.53       | 10.0             | Bottom 25%    |
| 715  | 715        | Neil Knudson           | Home Office | 572.05      | 7            | 121.22       | 12.7             | Bottom 25%    |
| 716  | 716        | Carlos Meador          | Consumer    | 565.39      | 2            | -43.73       | 20.0             | Bottom 25%    |
| 717  | 717        | Chuck Sachs            | Consumer    | 550.64      | 2            | 156.26       | 6.7              | Bottom 25%    |
| 718  | 718        | Cari Schnelling        | Consumer    | 537.63      | 6            | 105.83       | 22.9             | Bottom 25%    |
| 719  | 719        | John Huston            | Consumer    | 528.91      | 6            | 26.08        | 15.0             | Bottom 25%    |
| 720  | 720        | Rob Beeghly            | Consumer    | 528.55      | 5            | 76.89        | 16.7             | Bottom 25%    |
| 721  | 721        | Andy Yotov             | Corporate   | 497.01      | 4            | 103.35       | 10.0             | Bottom 25%    |
| 722  | 722        | Corey Roper            | Home Office | 475.9       | 3            | 144.76       | 0.0              | Bottom 25%    |
| 723  | 723        | MaryBeth Skach         | Consumer    | 475.66      | 4            | 84.03        | 15.7             | Bottom 25%    |
| 724  | 724        | Joni Sundaresam        | Home Office | 469.17      | 5            | -327.93      | 33.8             | Bottom 25%    |
| 725  | 725        | Erin Creighton         | Consumer    | 461.91      | 5            | 96.43        | 10.0             | Bottom 25%    |
| 726  | 726        | Khloe Miller           | Consumer    | 453.54      | 5            | 91.14        | 4.4              | Bottom 25%    |
| 727  | 727        | Kelly Williams         | Consumer    | 449.1       | 4            | 107.93       | 4.0              | Bottom 25%    |
| 728  | 728        | Tim Taslimi            | Corporate   | 439.5       | 3            | 93.92        | 0.0              | Bottom 25%    |
| 729  | 729        | Shui Tom               | Consumer    | 433.34      | 7            | 84.44        | 20.0             | Bottom 25%    |
| 730  | 730        | Vivek Grady            | Corporate   | 427.37      | 5            | -52.33       | 10.0             | Bottom 25%    |
| 731  | 731        | Sonia Sunley           | Consumer    | 418.49      | 6            | 135.54       | 0.0              | Bottom 25%    |
| 732  | 732        | Brad Thomas            | Home Office | 415.2       | 2            | 126.87       | 6.7              | Bottom 25%    |
| 733  | 733        | Mark Haberlin          | Corporate   | 400.02      | 4            | 61.43        | 7.8              | Bottom 25%    |
| 734  | 734        | Barry Weirich          | Consumer    | 385.52      | 3            | -58.29       | 13.3             | Bottom 25%    |
| 735  | 735        | Joy Daniels            | Consumer    | 385.43      | 6            | 26.76        | 30.9             | Bottom 25%    |
| 736  | 736        | Jason Klamczynski      | Corporate   | 383.81      | 3            | 55.33        | 10.0             | Bottom 25%    |
| 737  | 737        | Vivian Mathis          | Consumer    | 380.69      | 5            | 116.64       | 11.2             | Bottom 25%    |
| 738  | 738        | Neil Französisch       | Home Office | 377.16      | 4            | 85.93        | 25.0             | Bottom 25%    |
| 739  | 739        | Melanie Seite          | Consumer    | 370.35      | 4            | 19.43        | 18.0             | Bottom 25%    |
| 740  | 740        | Lycoris Saunders       | Consumer    | 368.88      | 3            | 39.2         | 11.7             | Bottom 25%    |
| 741  | 741        | Aleksandra Gannaway    | Corporate   | 367.55      | 4            | 59.29        | 8.0              | Bottom 25%    |
| 742  | 742        | Evan Minnotte          | Home Office | 366.82      | 3            | 21.77        | 12.5             | Bottom 25%    |
| 743  | 743        | Heather Jas            | Home Office | 358.1       | 5            | 98.65        | 10.0             | Bottom 25%    |
| 744  | 744        | Don Weiss              | Consumer    | 344.08      | 5            | 69.67        | 17.8             | Bottom 25%    |
| 745  | 745        | Larry Tron             | Consumer    | 329.88      | 3            | 59.04        | 13.3             | Bottom 25%    |
| 746  | 746        | Brendan Dodson         | Home Office | 320.54      | 2            | 116.71       | 0.0              | Bottom 25%    |
| 747  | 747        | Lisa Hazard            | Consumer    | 318.24      | 4            | -242.74      | 46.7             | Bottom 25%    |
| 748  | 748        | Jennifer Halladay      | Consumer    | 309.28      | 4            | -24.08       | 31.4             | Bottom 25%    |
| 749  | 749        | Jill Matthias          | Consumer    | 303.95      | 5            | 113.12       | 11.4             | Bottom 25%    |
| 750  | 750        | Chuck Magee            | Consumer    | 287.99      | 3            | 64.43        | 7.8              | Bottom 25%    |
| 751  | 751        | Larry Hughes           | Consumer    | 287.43      | 3            | 12.63        | 36.7             | Bottom 25%    |
| 752  | 752        | Sung Chung             | Consumer    | 280.63      | 2            | 31.18        | 20.0             | Bottom 25%    |
| 753  | 753        | Stuart Calhoun         | Consumer    | 279.26      | 4            | 51.83        | 12.0             | Bottom 25%    |
| 754  | 754        | Nicole Brennan         | Corporate   | 273.87      | 2            | 24.79        | 10.0             | Bottom 25%    |
| 755  | 755        | Bart Folk              | Consumer    | 272.95      | 3            | 110.93       | 0.0              | Bottom 25%    |
| 756  | 756        | Dorothy Dickinson      | Consumer    | 269.54      | 6            | 36.43        | 24.4             | Bottom 25%    |
| 757  | 757        | Brad Norvell           | Corporate   | 265.3       | 4            | 36.61        | 16.7             | Bottom 25%    |
| 758  | 758        | Andrew Roberts         | Consumer    | 264.86      | 5            | 43.67        | 21.4             | Bottom 25%    |
| 759  | 759        | Harold Dahlen          | Home Office | 251.36      | 3            | -135.88      | 30.0             | Bottom 25%    |
| 760  | 760        | Sally Matthias         | Consumer    | 244.49      | 4            | -26.59       | 26.7             | Bottom 25%    |
| 761  | 761        | Paul Lucas             | Home Office | 239.48      | 5            | -0.75        | 25.0             | Bottom 25%    |
| 762  | 762        | Guy Phonely            | Corporate   | 236.53      | 2            | 31.84        | 14.0             | Bottom 25%    |
| 763  | 763        | Erin Mull              | Consumer    | 228.99      | 4            | 40.15        | 25.0             | Bottom 25%    |
| 764  | 764        | Guy Thornton           | Consumer    | 226.44      | 4            | -6.14        | 20.0             | Bottom 25%    |
| 765  | 765        | Robert Barroso         | Corporate   | 221.08      | 5            | 72.68        | 14.3             | Bottom 25%    |
| 766  | 766        | Hilary Holden          | Corporate   | 218.67      | 2            | 86.73        | 3.3              | Bottom 25%    |
| 767  | 767        | Allen Goldenen         | Consumer    | 200.95      | 5            | 69.28        | 22.5             | Bottom 25%    |
| 768  | 768        | Joel Jenkins           | Home Office | 195.0       | 2            | 34.45        | 6.7              | Bottom 25%    |
| 769  | 769        | Anthony Garverick      | Home Office | 170.58      | 4            | -8.43        | 46.0             | Bottom 25%    |
| 770  | 770        | Muhammed Lee           | Consumer    | 162.23      | 2            | 42.66        | 6.7              | Bottom 25%    |
| 771  | 771        | Anthony O'Donnell      | Corporate   | 161.28      | 1            | 12.1         | 20.0             | Bottom 25%    |
| 772  | 772        | Pete Takahito          | Consumer    | 160.57      | 4            | -20.05       | 37.1             | Bottom 25%    |
| 773  | 773        | Dianna Arnett          | Home Office | 156.76      | 4            | 56.79        | 12.5             | Bottom 25%    |
| 774  | 774        | Michael Oakman         | Consumer    | 154.29      | 2            | -82.01       | 35.0             | Bottom 25%    |
| 775  | 775        | Greg Hansen            | Consumer    | 146.94      | 2            | -5.81        | 24.0             | Bottom 25%    |
| 776  | 776        | Phillip Breyer         | Corporate   | 132.74      | 2            | 21.9         | 10.0             | Bottom 25%    |
| 777  | 777        | Bobby Odegard          | Consumer    | 130.83      | 2            | 59.45        | 0.0              | Bottom 25%    |
| 778  | 778        | Ed Ludwig              | Home Office | 124.28      | 2            | 27.12        | 0.0              | Bottom 25%    |
| 779  | 779        | Clay Cheatham          | Consumer    | 113.83      | 3            | 33.87        | 15.0             | Bottom 25%    |
| 780  | 780        | Roland Murray          | Consumer    | 98.35       | 1            | 28.69        | 0.0              | Bottom 25%    |
| 781  | 781        | Karen Seio             | Corporate   | 88.47       | 3            | 0.11         | 27.5             | Bottom 25%    |
| 782  | 782        | Anemone Ratner         | Consumer    | 88.15       | 1            | 32.63        | 0.0              | Bottom 25%    |
| 783  | 783        | Fred Wasserman         | Corporate   | 79.75       | 3            | 23.49        | 0.0              | Bottom 25%    |
| 784  | 784        | Jasper Cacioppo        | Consumer    | 71.26       | 4            | -0.36        | 22.5             | Bottom 25%    |
| 785  | 785        | Adrian Shami           | Home Office | 58.82       | 2            | 21.85        | 6.7              | Bottom 25%    |
| 786  | 786        | Larry Blacks           | Consumer    | 50.19       | 3            | 18.65        | 26.7             | Bottom 25%    |
| 787  | 787        | Ricardo Emerson        | Consumer    | 48.36       | 1            | 6.05         | 20.0             | Bottom 25%    |
| 788  | 788        | Susan Gilcrest         | Corporate   | 47.95       | 3            | -3.71        | 40.0             | Bottom 25%    |
| 789  | 789        | Roy Skaria             | Home Office | 22.33       | 2            | 9.58         | 6.7              | Bottom 25%    |
| 790  | 790        | Mitch Gastineau        | Corporate   | 16.74       | 1            | -1.25        | 45.0             | Bottom 25%    |
| 791  | 791        | Carl Jackson           | Corporate   | 16.52       | 1            | 1.65         | 20.0             | Bottom 25%    |
| 792  | 792        | Lela Donovan           | Corporate   | 5.3         | 1            | 0.46         | 20.0             | Bottom 25%    |
| 793  | 793        | Thais Sissman          | Consumer    | 4.83        | 2            | -3.32        | 70.0             | Bottom 25%    |
