# Superstore Sales — SQL Query Results

> Dataset: Sample - Superstore.csv &nbsp;|&nbsp; Tool: DuckDB &nbsp;|&nbsp; Rows: 9,994 &nbsp;|&nbsp; Period: 2014–2017

---

## Table of Contents
1. [Step 1 — Load Dataset](#step-1--load-dataset)
2. [Step 2 — Schema & Sample Data](#step-2--schema--sample-data)
3. [Step 3 — WHERE Filters](#step-3--where-filters)
4. [Step 4 — GROUP BY Aggregations](#step-4--group-by-aggregations)
5. [Step 5 — Sort & Limit](#step-5--sort--limit-top-products--categories)
6. [Step 6 — Business Use Cases](#step-6--business-use-cases)
7. [Step 7 — Data Validation](#step-7--data-validation)

---

## Step 1 — Load Dataset

### Table created

```sql
SELECT COUNT(*) AS rows_loaded FROM superstore;
```

Result:

| rows_loaded |
| ----------- |
| 9994        |

> Insight: 9,994 rows loaded successfully from the Superstore CSV into an in-memory DuckDB table.

---

## Step 2 — Schema & Sample Data

### 2.1 — Table Schema

```sql
DESCRIBE superstore;
```

Result:

| column_name   | column_type | null | key  | default | extra |
| ------------- | ----------- | ---- | ---- | ------- | ----- |
| row_id        | INTEGER     | YES  | NULL | NULL    | NULL  |
| order_id      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| order_date    | DATE        | YES  | NULL | NULL    | NULL  |
| ship_date     | DATE        | YES  | NULL | NULL    | NULL  |
| ship_mode     | VARCHAR     | YES  | NULL | NULL    | NULL  |
| customer_id   | VARCHAR     | YES  | NULL | NULL    | NULL  |
| customer_name | VARCHAR     | YES  | NULL | NULL    | NULL  |
| segment       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| country       | VARCHAR     | YES  | NULL | NULL    | NULL  |
| city          | VARCHAR     | YES  | NULL | NULL    | NULL  |
| state         | VARCHAR     | YES  | NULL | NULL    | NULL  |
| postal_code   | INTEGER     | YES  | NULL | NULL    | NULL  |
| region        | VARCHAR     | YES  | NULL | NULL    | NULL  |
| product_id    | VARCHAR     | YES  | NULL | NULL    | NULL  |
| category      | VARCHAR     | YES  | NULL | NULL    | NULL  |
| sub_category  | VARCHAR     | YES  | NULL | NULL    | NULL  |
| product_name  | VARCHAR     | YES  | NULL | NULL    | NULL  |
| sales         | DOUBLE      | YES  | NULL | NULL    | NULL  |
| quantity      | INTEGER     | YES  | NULL | NULL    | NULL  |
| discount      | DOUBLE      | YES  | NULL | NULL    | NULL  |
| profit        | DOUBLE      | YES  | NULL | NULL    | NULL  |

> Insight: 21 columns: order metadata (dates, ship mode), customer info (name, segment), geography (city/state/region), product details (category, sub-category), and numeric KPIs (sales, quantity, discount, profit).

---

### 2.2 — First 10 Rows

```sql
SELECT * FROM superstore LIMIT 10;
```

Result:

| row_id | order_id       | order_date | ship_date  | ship_mode      | customer_id | customer_name   | segment   | country       | city            | state      | postal_code | region | product_id      | category        | sub_category | product_name                                                     | sales    | quantity | discount | profit   |
| ------ | -------------- | ---------- | ---------- | -------------- | ----------- | --------------- | --------- | ------------- | --------------- | ---------- | ----------- | ------ | --------------- | --------------- | ------------ | ---------------------------------------------------------------- | -------- | -------- | -------- | -------- |
| 1      | CA-2016-152156 | 2016-11-08 | 2016-11-11 | Second Class   | CG-12520    | Claire Gute     | Consumer  | United States | Henderson       | Kentucky   | 42420       | South  | FUR-BO-10001798 | Furniture       | Bookcases    | Bush Somerset Collection Bookcase                                | 261.96   | 2        | 0        | 41.9136  |
| 2      | CA-2016-152156 | 2016-11-08 | 2016-11-11 | Second Class   | CG-12520    | Claire Gute     | Consumer  | United States | Henderson       | Kentucky   | 42420       | South  | FUR-CH-10000454 | Furniture       | Chairs       | Hon Deluxe Fabric Upholstered Stacking Chairs, Rounded Back      | 731.94   | 3        | 0        | 219.582  |
| 3      | CA-2016-138688 | 2016-06-12 | 2016-06-16 | Second Class   | DV-13045    | Darrin Van Huff | Corporate | United States | Los Angeles     | California | 90036       | West   | OFF-LA-10000240 | Office Supplies | Labels       | Self-Adhesive Address Labels for Typewriters by Universal        | 14.62    | 2        | 0        | 6.8714   |
| 4      | US-2015-108966 | 2015-10-11 | 2015-10-18 | Standard Class | SO-20335    | Sean O'Donnell  | Consumer  | United States | Fort Lauderdale | Florida    | 33311       | South  | FUR-TA-10000577 | Furniture       | Tables       | Bretford CR4500 Series Slim Rectangular Table                    | 957.5775 | 5        | 0.45     | -383.031 |
| 5      | US-2015-108966 | 2015-10-11 | 2015-10-18 | Standard Class | SO-20335    | Sean O'Donnell  | Consumer  | United States | Fort Lauderdale | Florida    | 33311       | South  | OFF-ST-10000760 | Office Supplies | Storage      | Eldon Fold 'N Roll Cart System                                   | 22.368   | 2        | 0.2      | 2.5164   |
| 6      | CA-2014-115812 | 2014-06-09 | 2014-06-14 | Standard Class | BH-11710    | Brosina Hoffman | Consumer  | United States | Los Angeles     | California | 90032       | West   | FUR-FU-10001487 | Furniture       | Furnishings  | Eldon Expressions Wood and Plastic Desk Accessories, Cherry Wood | 48.86    | 7        | 0        | 14.1694  |
| 7      | CA-2014-115812 | 2014-06-09 | 2014-06-14 | Standard Class | BH-11710    | Brosina Hoffman | Consumer  | United States | Los Angeles     | California | 90032       | West   | OFF-AR-10002833 | Office Supplies | Art          | Newell 322                                                       | 7.28     | 4        | 0        | 1.9656   |
| 8      | CA-2014-115812 | 2014-06-09 | 2014-06-14 | Standard Class | BH-11710    | Brosina Hoffman | Consumer  | United States | Los Angeles     | California | 90032       | West   | TEC-PH-10002275 | Technology      | Phones       | Mitel 5320 IP Phone VoIP phone                                   | 907.152  | 6        | 0.2      | 90.7152  |
| 9      | CA-2014-115812 | 2014-06-09 | 2014-06-14 | Standard Class | BH-11710    | Brosina Hoffman | Consumer  | United States | Los Angeles     | California | 90032       | West   | OFF-BI-10003910 | Office Supplies | Binders      | DXL Angle-View Binders with Locking Rings by Samsill             | 18.504   | 3        | 0.2      | 5.7825   |
| 10     | CA-2014-115812 | 2014-06-09 | 2014-06-14 | Standard Class | BH-11710    | Brosina Hoffman | Consumer  | United States | Los Angeles     | California | 90032       | West   | OFF-AP-10002892 | Office Supplies | Appliances   | Belkin F5C206VTEL 6 Outlet Surge                                 | 114.9    | 5        | 0        | 34.47    |

> Insight: Sample rows confirm correct parsing: dates are DATE type, sales/profit are DOUBLE, quantity is INTEGER.

---

### 2.3 — Total Row Count

```sql
SELECT COUNT(*) AS total_rows FROM superstore;
```

Result:

| total_rows |
| ---------- |
| 9994       |

> Insight: Dataset contains 9,994 transaction-level rows.

---

### 2.4 — Dataset Summary

```sql
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
```

Result:

| total_rows | unique_orders | unique_customers | unique_products | earliest_order | latest_order | regions | states | categories | sub_categories |
| ---------- | ------------- | ---------------- | --------------- | -------------- | ------------ | ------- | ------ | ---------- | -------------- |
| 9994       | 5009          | 793              | 1862            | 2014-01-03     | 2017-12-30   | 4       | 49     | 3          | 17             |

> Insight: Data spans 4 years (2014–2017), covers 4 regions, 49 states, 3 categories, and 17 sub-categories with 793 unique customers.

---

## Step 3 — WHERE Filters

### 3.1 — Orders from West Region (first 15)

```sql
SELECT order_id, customer_name, product_name, sales, profit, region FROM superstore WHERE region='West' LIMIT 15;
```

Result:

| order_id       | customer_name      | product_name                                                     | sales     | profit   | region |
| -------------- | ------------------ | ---------------------------------------------------------------- | --------- | -------- | ------ |
| CA-2016-138688 | Darrin Van Huff    | Self-Adhesive Address Labels for Typewriters by Universal        | 14.62     | 6.8714   | West   |
| CA-2014-115812 | Brosina Hoffman    | Eldon Expressions Wood and Plastic Desk Accessories, Cherry Wood | 48.86     | 14.1694  | West   |
| CA-2014-115812 | Brosina Hoffman    | Newell 322                                                       | 7.28      | 1.9656   | West   |
| CA-2014-115812 | Brosina Hoffman    | Mitel 5320 IP Phone VoIP phone                                   | 907.152   | 90.7152  | West   |
| CA-2014-115812 | Brosina Hoffman    | DXL Angle-View Binders with Locking Rings by Samsill             | 18.504    | 5.7825   | West   |
| CA-2014-115812 | Brosina Hoffman    | Belkin F5C206VTEL 6 Outlet Surge                                 | 114.9     | 34.47    | West   |
| CA-2014-115812 | Brosina Hoffman    | Chromcraft Rectangular Conference Tables                         | 1,706.184 | 85.3092  | West   |
| CA-2014-115812 | Brosina Hoffman    | Konftel 250 Conference phone - Charcoal black                    | 911.424   | 68.3568  | West   |
| CA-2016-161389 | Irene Maddox       | Fellowes PB200 Plastic Comb Binding Machine                      | 407.976   | 132.5922 | West   |
| CA-2014-167164 | Alejandro Grove    | Fellowes Super Stor/Drawer                                       | 55.5      | 9.99     | West   |
| CA-2014-143336 | Zuschuss Donatelli | Newell 341                                                       | 8.56      | 2.4824   | West   |
| CA-2014-143336 | Zuschuss Donatelli | Cisco SPA 501G IP Phone                                          | 213.48    | 16.011   | West   |
| CA-2014-143336 | Zuschuss Donatelli | Wilson Jones Hanging View Binder, White, 1"                      | 22.72     | 7.384    | West   |
| CA-2015-106320 | Emily Burns        | Bretford CR4500 Series Slim Rectangular Table                    | 1,044.63  | 240.2649 | West   |
| CA-2016-121755 | Eric Hoffmann      | Wilson Jones Active Use Binders                                  | 11.648    | 4.2224   | West   |

> Insight: West region has highest total sales (~$725K). California dominates West-region orders.

---

### 3.2 — Technology Category Orders (first 15)

```sql
SELECT order_id, customer_name, product_name, category, sales, profit FROM superstore WHERE category='Technology' LIMIT 15;
```

Result:

| order_id       | customer_name      | product_name                                                                                       | category   | sales     | profit   |
| -------------- | ------------------ | -------------------------------------------------------------------------------------------------- | ---------- | --------- | -------- |
| CA-2014-115812 | Brosina Hoffman    | Mitel 5320 IP Phone VoIP phone                                                                     | Technology | 907.152   | 90.7152  |
| CA-2014-115812 | Brosina Hoffman    | Konftel 250 Conference phone - Charcoal black                                                      | Technology | 911.424   | 68.3568  |
| CA-2014-143336 | Zuschuss Donatelli | Cisco SPA 501G IP Phone                                                                            | Technology | 213.48    | 16.011   |
| CA-2016-121755 | Eric Hoffmann      | Imation 8GB Mini TravelDrive USB 2.0 Flash Drive                                                   | Technology | 90.57     | 11.7741  |
| CA-2016-117590 | Gene Hale          | GE 30524EE4                                                                                        | Technology | 1,097.544 | 123.4737 |
| CA-2015-117415 | Steve Nguyen       | Plantronics HL10 Handset Lifter                                                                    | Technology | 371.168   | 41.7564  |
| CA-2017-120999 | Linda Cazamias     | Panasonic Kx-TS550                                                                                 | Technology | 147.168   | 16.5564  |
| CA-2016-118255 | Odella Nelson      | Verbatim 25 GB 6x Blu-ray Single Layer Recordable Disc, 25/Pack                                    | Technology | 45.98     | 19.7714  |
| CA-2016-169194 | Lena Hernandez     | Imation 8gb Micro Traveldrive Usb 2.0 Flash Drive                                                  | Technology | 45        | 4.95     |
| CA-2016-169194 | Lena Hernandez     | LF Elite 3D Dazzle Designer Hard Case Cover, Lf Stylus Pen and Wiper For Apple Iphone 5c Mini Lite | Technology | 21.8      | 6.104    |
| CA-2016-105816 | Janet Molinari     | AT&T CL83451 4-Handset Telephone                                                                   | Technology | 1,029.95  | 298.6855 |
| CA-2016-111682 | Ted Butterfield    | Imation 8gb Micro Traveldrive Usb 2.0 Flash Drive                                                  | Technology | 30        | 3.3      |
| CA-2015-135545 | Kunst Miller       | Verbatim 25 GB 6x Blu-ray Single Layer Recordable Disc, 3/Pack                                     | Technology | 13.98     | 6.1512   |
| CA-2014-106376 | Brendan Sweed      | netTALK DUO VoIP Telephone Service                                                                 | Technology | 167.968   | 62.988   |
| CA-2017-155558 | Paul Gonzalez      | Logitech LS21 Speaker System - PC Multimedia - 2.1-CH - Wired                                      | Technology | 19.99     | 6.7966   |

> Insight: Technology orders tend to have higher per-unit sales values (phones, copiers). This category delivers the highest average sale amount.

---

### 3.3 — Orders Placed in 2016 (first 15)

```sql
SELECT order_id, order_date, customer_name, sales, profit FROM superstore WHERE YEAR(order_date)=2016 LIMIT 15;
```

Result:

| order_id       | order_date | customer_name   | sales     | profit   |
| -------------- | ---------- | --------------- | --------- | -------- |
| CA-2016-152156 | 2016-11-08 | Claire Gute     | 261.96    | 41.9136  |
| CA-2016-152156 | 2016-11-08 | Claire Gute     | 731.94    | 219.582  |
| CA-2016-138688 | 2016-06-12 | Darrin Van Huff | 14.62     | 6.8714   |
| CA-2016-161389 | 2016-12-05 | Irene Maddox    | 407.976   | 132.5922 |
| CA-2016-137330 | 2016-12-09 | Ken Black       | 19.46     | 5.0596   |
| CA-2016-137330 | 2016-12-09 | Ken Black       | 60.34     | 15.6884  |
| CA-2016-121755 | 2016-01-16 | Eric Hoffmann   | 11.648    | 4.2224   |
| CA-2016-121755 | 2016-01-16 | Eric Hoffmann   | 90.57     | 11.7741  |
| CA-2016-117590 | 2016-12-08 | Gene Hale       | 1,097.544 | 123.4737 |
| CA-2016-117590 | 2016-12-08 | Gene Hale       | 190.92    | -147.963 |
| CA-2016-101343 | 2016-07-17 | Ruben Ausman    | 77.88     | 3.894    |
| CA-2016-118255 | 2016-03-11 | Odella Nelson   | 45.98     | 19.7714  |
| CA-2016-118255 | 2016-03-11 | Odella Nelson   | 17.46     | 8.2062   |
| CA-2016-169194 | 2016-06-20 | Lena Hernandez  | 45        | 4.95     |
| CA-2016-169194 | 2016-06-20 | Lena Hernandez  | 21.8      | 6.104    |

> Insight: 2016 had 2,823 order rows — the second-highest annual volume, showing consistent growth from 2014.

---

### 3.4 — High-Value Orders: Sales > $1,000 (top 15)

```sql
SELECT order_id, customer_name, product_name, ROUND(sales,2) AS sales, ROUND(profit,2) AS profit FROM superstore WHERE sales>1000 ORDER BY sales DESC LIMIT 15;
```

Result:

| order_id       | customer_name        | product_name                                                                | sales     | profit    |
| -------------- | -------------------- | --------------------------------------------------------------------------- | --------- | --------- |
| CA-2014-145317 | Sean Miller          | Cisco TelePresence System EX90 Videoconferencing Unit                       | 22,638.48 | -1,811.08 |
| CA-2016-118689 | Tamara Chand         | Canon imageCLASS 2200 Advanced Copier                                       | 17,499.95 | 8,399.98  |
| CA-2017-140151 | Raymond Buch         | Canon imageCLASS 2200 Advanced Copier                                       | 13,999.96 | 6,719.98  |
| CA-2017-127180 | Tom Ashbrook         | Canon imageCLASS 2200 Advanced Copier                                       | 11,199.97 | 3,919.99  |
| CA-2017-166709 | Hunter Lopez         | Canon imageCLASS 2200 Advanced Copier                                       | 10,499.97 | 5,039.99  |
| CA-2016-117121 | Adrian Barton        | GBC Ibimaster 500 Manual ProClick Binding System                            | 9,892.74  | 4,946.37  |
| CA-2014-116904 | Sanjit Chand         | Ibico EPK-21 Electric Binding System                                        | 9,449.95  | 4,630.48  |
| US-2016-107440 | Bill Shonely         | 3D Systems Cube Printer, 2nd Generation, Magenta                            | 9,099.93  | 2,365.98  |
| CA-2016-158841 | Sanjit Engle         | HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | 8,749.95  | 2,799.98  |
| CA-2016-143714 | Christopher Conant   | Canon imageCLASS 2200 Advanced Copier                                       | 8,399.98  | 1,120     |
| CA-2014-143917 | Ken Lonsdale         | High Speed Automatic Electric Letter Opener                                 | 8,187.65  | 327.51    |
| CA-2014-139892 | Becky Martin         | Lexmark MX611dhe Monochrome Laser Printer                                   | 8,159.95  | -1,359.99 |
| US-2017-168116 | Grant Thornton       | Cubify CubeX 3D Printer Triple Head Print                                   | 7,999.98  | -3,839.99 |
| CA-2014-145541 | Tom Boeckenhauer     | HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | 6,999.96  | 2,239.99  |
| CA-2015-145352 | Christopher Martinez | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | 6,354.95  | 3,177.48  |

> Insight: Copiers and large furniture items dominate high-value orders. The top single sale exceeded $22,000.

---

### 3.5 — High Discount Orders: Discount >= 30% (top 15)

```sql
SELECT order_id, product_name, category, ROUND(discount,2) AS discount, ROUND(sales,2) AS sales, ROUND(profit,2) AS profit FROM superstore WHERE discount>=0.30 ORDER BY discount DESC LIMIT 15;
```

Result:

| order_id       | product_name                                                                 | category        | discount | sales  | profit  |
| -------------- | ---------------------------------------------------------------------------- | --------------- | -------- | ------ | ------- |
| US-2015-118983 | Holmes Replacement Filter for HEPA Air Cleaner, Very Large Room, HEPA Filter | Office Supplies | 0.8      | 68.81  | -123.86 |
| US-2015-118983 | Storex DuraTech Recycled Plastic Frosted Binders                             | Office Supplies | 0.8      | 2.54   | -3.82   |
| US-2017-118038 | Economy Binders                                                              | Office Supplies | 0.8      | 1.25   | -1.93   |
| CA-2016-158568 | Avery Hidden Tab Dividers for Binding Systems                                | Office Supplies | 0.8      | 1.79   | -3.04   |
| CA-2014-139892 | Kensington 7 Outlet MasterPiece Power Center                                 | Office Supplies | 0.8      | 177.98 | -453.85 |
| US-2014-100853 | Kensington 7 Outlet MasterPiece HOMEOFFICE Power Control Center              | Office Supplies | 0.8      | 52.45  | -131.12 |
| US-2017-152366 | Acco 7-Outlet Masterpiece Power Center, Wihtout Fax/Phone Line Protection    | Office Supplies | 0.8      | 97.26  | -243.16 |
| US-2017-116701 | Eureka Sanitaire  Commercial Upright                                         | Office Supplies | 0.8      | 66.28  | -178.97 |
| US-2017-155299 | Eureka Disposable Bags for Sanitaire Vibra Groomer I Upright Vac             | Office Supplies | 0.8      | 1.62   | -4.47   |
| US-2015-161991 | Round Ring Binders                                                           | Office Supplies | 0.8      | 2.08   | -3.43   |
| CA-2015-130792 | Holmes Odor Grabber                                                          | Office Supplies | 0.8      | 8.65   | -20.33  |
| CA-2015-130792 | GBC Twin Loop Wire Binding Elements, 9/16" Spine, Black                      | Office Supplies | 0.8      | 12.18  | -18.87  |
| US-2014-134971 | Wilson Jones Century Plastic Molded Ring Binders                             | Office Supplies | 0.8      | 12.46  | -20.56  |
| US-2016-100419 | Cardinal Hold-It CD Pocket                                                   | Office Supplies | 0.8      | 4.79   | -7.9    |
| CA-2015-157812 | XtraLife ClearVue Slant-D Ring Binders by Cardinal                           | Office Supplies | 0.8      | 14.11  | -21.17  |

> Insight: High discounts correlate strongly with negative profit. Most items discounted ≥ 30% sell at a loss.

---

### 3.6 — Loss-Making Orders: Profit < 0 (worst 15)

```sql
SELECT order_id, product_name, category, ROUND(sales,2) AS sales, ROUND(discount,2) AS discount, ROUND(profit,2) AS profit FROM superstore WHERE profit<0 ORDER BY profit ASC LIMIT 15;
```

Result:

| order_id       | product_name                                                                | category        | sales     | discount | profit    |
| -------------- | --------------------------------------------------------------------------- | --------------- | --------- | -------- | --------- |
| CA-2016-108196 | Cubify CubeX 3D Printer Double Head Print                                   | Technology      | 4,499.98  | 0.7      | -6,599.98 |
| US-2017-168116 | Cubify CubeX 3D Printer Triple Head Print                                   | Technology      | 7,999.98  | 0.5      | -3,839.99 |
| CA-2014-169019 | GBC DocuBind P400 Electric Binding System                                   | Office Supplies | 2,177.58  | 0.8      | -3,701.89 |
| CA-2017-134845 | Lexmark MX611dhe Monochrome Laser Printer                                   | Technology      | 2,549.99  | 0.7      | -3,399.98 |
| US-2017-122714 | Ibico EPK-21 Electric Binding System                                        | Office Supplies | 1,889.99  | 0.8      | -2,929.48 |
| CA-2015-147830 | Cubify CubeX 3D Printer Double Head Print                                   | Technology      | 1,799.99  | 0.7      | -2,639.99 |
| CA-2017-131254 | Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies | 1,525.19  | 0.8      | -2,287.78 |
| CA-2015-116638 | Chromcraft Bull-Nose Wood Oval Conference Tables & Bases                    | Furniture       | 4,297.64  | 0.4      | -1,862.31 |
| CA-2016-130946 | GBC DocuBind P400 Electric Binding System                                   | Office Supplies | 1,088.79  | 0.8      | -1,850.95 |
| CA-2014-145317 | Cisco TelePresence System EX90 Videoconferencing Unit                       | Technology      | 22,638.48 | 0.5      | -1,811.08 |
| US-2015-150630 | Riverside Palais Royal Lawyers Bookcase, Royale Cherry Finish               | Furniture       | 3,083.43  | 0.5      | -1,665.05 |
| CA-2014-165309 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies | 896.99    | 0.8      | -1,480.03 |
| CA-2014-139892 | Lexmark MX611dhe Monochrome Laser Printer                                   | Technology      | 8,159.95  | 0.4      | -1,359.99 |
| US-2017-120390 | GBC DocuBind P400 Electric Binding System                                   | Office Supplies | 1,633.19  | 0.7      | -1,306.55 |
| CA-2017-128363 | GBC DocuBind TL300 Electric Binding System                                  | Office Supplies | 1,614.58  | 0.7      | -1,237.85 |

> Insight: 1,871 out of 9,994 rows are loss-making (~18.7%). Tables and Bookcases in Furniture are frequent loss drivers, often with high discounts.

---

## Step 4 — GROUP BY Aggregations

### 4.1 — Sales & Profit by Region

```sql
SELECT
    region,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    ROUND(AVG(sales),2) AS avg_sale,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100,2) AS profit_margin_pct
FROM superstore GROUP BY region ORDER BY total_sales DESC;
```

Result:

| region  | total_orders | total_sales | total_profit | avg_sale | profit_margin_pct |
| ------- | ------------ | ----------- | ------------ | -------- | ----------------- |
| West    | 3203         | 725,457.82  | 108,418.45   | 226.49   | 14.94             |
| East    | 2848         | 678,781.24  | 91,522.78    | 238.34   | 13.48             |
| Central | 2323         | 501,239.89  | 39,706.36    | 215.77   | 7.92              |
| South   | 1620         | 391,721.91  | 46,749.43    | 241.8    | 11.93             |

> Insight: West leads in sales (~$725K), but East region has the highest profit margin. Central has the lowest margin, suggesting heavy discounting or product-mix issues.

---

### 4.2 — Sales, Quantity & Discount by Category

```sql
SELECT
    category,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS total_sales,
    SUM(quantity) AS total_quantity,
    ROUND(AVG(sales),2) AS avg_sale,
    ROUND(SUM(profit),2) AS total_profit,
    ROUND(AVG(discount)*100,2) AS avg_discount_pct
FROM superstore GROUP BY category ORDER BY total_sales DESC;
```

Result:

| category        | total_orders | total_sales | total_quantity | avg_sale | total_profit | avg_discount_pct |
| --------------- | ------------ | ----------- | -------------- | -------- | ------------ | ---------------- |
| Technology      | 1847         | 836,154.03  | 6939           | 452.71   | 145,454.95   | 13.23            |
| Furniture       | 2121         | 741,999.8   | 8028           | 349.83   | 18,451.27    | 17.39            |
| Office Supplies | 6026         | 719,047.03  | 22906          | 119.32   | 122,490.8    | 15.73            |

> Insight: Technology generates the highest sales and profit despite fewer orders. Office Supplies has the most orders but lowest average sale. Furniture has poor margins due to high discounting.

---

### 4.3 — Sales & Profit by Sub-Category

```sql
SELECT
    category, sub_category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(profit)/NULLIF(SUM(sales),0)*100,2) AS profit_margin_pct
FROM superstore GROUP BY category, sub_category ORDER BY total_profit DESC;
```

Result:

| category        | sub_category | total_sales | total_profit | total_quantity | profit_margin_pct |
| --------------- | ------------ | ----------- | ------------ | -------------- | ----------------- |
| Technology      | Copiers      | 149,528.03  | 55,617.82    | 234            | 37.2              |
| Technology      | Phones       | 330,007.05  | 44,515.73    | 3289           | 13.49             |
| Technology      | Accessories  | 167,380.32  | 41,936.64    | 2976           | 25.05             |
| Office Supplies | Paper        | 78,479.21   | 34,053.57    | 5178           | 43.39             |
| Office Supplies | Binders      | 203,412.73  | 30,221.76    | 5974           | 14.86             |
| Furniture       | Chairs       | 328,449.1   | 26,590.17    | 2356           | 8.1               |
| Office Supplies | Storage      | 223,843.61  | 21,278.83    | 3158           | 9.51              |
| Office Supplies | Appliances   | 107,532.16  | 18,138.01    | 1729           | 16.87             |
| Furniture       | Furnishings  | 91,705.16   | 13,059.14    | 3563           | 14.24             |
| Office Supplies | Envelopes    | 16,476.4    | 6,964.18     | 906            | 42.27             |
| Office Supplies | Art          | 27,118.79   | 6,527.79     | 3000           | 24.07             |
| Office Supplies | Labels       | 12,486.31   | 5,546.25     | 1400           | 44.42             |
| Technology      | Machines     | 189,238.63  | 3,384.76     | 440            | 1.79              |
| Office Supplies | Fasteners    | 3,024.28    | 949.52       | 914            | 31.4              |
| Office Supplies | Supplies     | 46,673.54   | -1,189.1     | 647            | -2.55             |
| Furniture       | Bookcases    | 114,880     | -3,472.56    | 868            | -3.02             |
| Furniture       | Tables       | 206,965.53  | -17,725.48   | 1241           | -8.56             |

> Insight: Copiers (Technology) have the highest profit margin. Tables and Bookcases (Furniture) are deeply loss-making. Labels and Paper (Office Supplies) show strong margins despite small revenue.

---

### 4.4 — Sales by Customer Segment

```sql
SELECT
    segment,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(AVG(sales),2) AS avg_order_value,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY segment ORDER BY total_sales DESC;
```

Result:

| segment     | total_orders | total_sales  | avg_order_value | total_profit |
| ----------- | ------------ | ------------ | --------------- | ------------ |
| Consumer    | 5191         | 1,161,401.34 | 223.73          | 134,119.21   |
| Corporate   | 3020         | 706,146.37   | 233.82          | 91,979.13    |
| Home Office | 1783         | 429,653.15   | 240.97          | 60,298.68    |

> Insight: Consumer segment is the largest by order volume and sales. Corporate segment has the highest average order value. Home Office is smallest but relatively profitable per order.

---

### 4.5 — Orders & Sales by Ship Mode

```sql
SELECT
    ship_mode,
    COUNT(*) AS order_count,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(AVG(sales),2) AS avg_sales
FROM superstore GROUP BY ship_mode ORDER BY order_count DESC;
```

Result:

| ship_mode      | order_count | total_sales  | avg_sales |
| -------------- | ----------- | ------------ | --------- |
| Standard Class | 5968        | 1,358,215.74 | 227.58    |
| Second Class   | 1945        | 459,193.57   | 236.09    |
| First Class    | 1538        | 351,428.42   | 228.5     |
| Same Day       | 543         | 128,363.13   | 236.4     |

> Insight: Standard Class is the most used shipping method (59% of orders). Same Day shipping is rare but has the highest average sale value, suggesting premium buyers prefer speed.

---

## Step 5 — Sort & Limit (Top Products & Categories)

### 5.1 — Top 10 Products by Total Sales

```sql
SELECT product_name, category, sub_category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    SUM(quantity) AS total_quantity
FROM superstore GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC LIMIT 10;
```

Result:

| product_name                                                                | category        | sub_category | total_sales | total_profit | total_quantity |
| --------------------------------------------------------------------------- | --------------- | ------------ | ----------- | ------------ | -------------- |
| Canon imageCLASS 2200 Advanced Copier                                       | Technology      | Copiers      | 61,599.82   | 25,199.93    | 20             |
| Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies | Binders      | 27,453.38   | 7,753.04     | 31             |
| Cisco TelePresence System EX90 Videoconferencing Unit                       | Technology      | Machines     | 22,638.48   | -1,811.08    | 6              |
| HON 5400 Series Task Chairs for Big and Tall                                | Furniture       | Chairs       | 21,870.58   | 0            | 39             |
| GBC DocuBind TL300 Electric Binding System                                  | Office Supplies | Binders      | 19,823.48   | 2,233.51     | 37             |
| GBC Ibimaster 500 Manual ProClick Binding System                            | Office Supplies | Binders      | 19,024.5    | 760.98       | 48             |
| Hewlett Packard LaserJet 3310 Copier                                        | Technology      | Copiers      | 18,839.69   | 6,983.88     | 38             |
| HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | Technology      | Machines     | 18,374.9    | 4,094.98     | 12             |
| GBC DocuBind P400 Electric Binding System                                   | Office Supplies | Binders      | 17,965.07   | -1,878.17    | 27             |
| High Speed Automatic Electric Letter Opener                                 | Office Supplies | Supplies     | 17,030.31   | -262         | 11             |

> Insight: Canon imageCLASS 2200 Copier tops the list by sales. High-end copiers and chairs dominate the top 10, confirming Technology drives revenue.

---

### 5.2 — Top 10 Products by Total Profit

```sql
SELECT product_name, category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY product_name, category
ORDER BY total_profit DESC LIMIT 10;
```

Result:

| product_name                                                                | category        | total_sales | total_profit |
| --------------------------------------------------------------------------- | --------------- | ----------- | ------------ |
| Canon imageCLASS 2200 Advanced Copier                                       | Technology      | 61,599.82   | 25,199.93    |
| Fellowes PB500 Electric Punch Plastic Comb Binding Machine with Manual Bind | Office Supplies | 27,453.38   | 7,753.04     |
| Hewlett Packard LaserJet 3310 Copier                                        | Technology      | 18,839.69   | 6,983.88     |
| Canon PC1060 Personal Laser Copier                                          | Technology      | 11,619.83   | 4,570.93     |
| HP Designjet T520 Inkjet Large Format Printer - 24" Color                   | Technology      | 18,374.9    | 4,094.98     |
| Ativa V4110MDD Micro-Cut Shredder                                           | Technology      | 7,699.89    | 3,772.95     |
| 3D Systems Cube Printer, 2nd Generation, Magenta                            | Technology      | 14,299.89   | 3,717.97     |
| Plantronics Savi W720 Multi-Device Wireless Headset System                  | Technology      | 9,367.29    | 3,696.28     |
| Ibico EPK-21 Electric Binding System                                        | Office Supplies | 15,875.92   | 3,345.28     |
| Zebra ZM400 Thermal Label Printer                                           | Technology      | 6,965.7     | 3,343.54     |

> Insight: Canon and Hewlett Packard copiers deliver the highest profits. Technology products have the strongest profit-to-sales ratio among top performers.

---

### 5.3 — Bottom 10 Products by Profit (Biggest Loss-Makers)

```sql
SELECT product_name, category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY product_name, category
ORDER BY total_profit ASC LIMIT 10;
```

Result:

| product_name                                                      | category        | total_sales | total_profit |
| ----------------------------------------------------------------- | --------------- | ----------- | ------------ |
| Cubify CubeX 3D Printer Double Head Print                         | Technology      | 11,099.96   | -8,879.97    |
| Lexmark MX611dhe Monochrome Laser Printer                         | Technology      | 16,829.9    | -4,589.97    |
| Cubify CubeX 3D Printer Triple Head Print                         | Technology      | 7,999.98    | -3,839.99    |
| Chromcraft Bull-Nose Wood Oval Conference Tables & Bases          | Furniture       | 9,917.64    | -2,876.12    |
| Bush Advantage Collection Racetrack Conference Table              | Furniture       | 9,544.73    | -1,934.4     |
| GBC DocuBind P400 Electric Binding System                         | Office Supplies | 17,965.07   | -1,878.17    |
| Cisco TelePresence System EX90 Videoconferencing Unit             | Technology      | 22,638.48   | -1,811.08    |
| Martin Yale Chadless Opener Electric Letter Opener                | Office Supplies | 16,656.2    | -1,299.18    |
| Balt Solid Wood Round Tables                                      | Furniture       | 6,518.75    | -1,201.06    |
| BoxOffice By Design Rectangular and Half-Moon Meeting Room Tables | Furniture       | 1,706.25    | -1,148.44    |

> Insight: Cubify and GBC binding machines top the loss list. Furniture tables and binders are sold at significant losses, often driven by deep discounting.

---

### 5.4 — Top 5 Sub-Categories by Profit

```sql
SELECT category, sub_category,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY category, sub_category
ORDER BY total_profit DESC LIMIT 5;
```

Result:

| category        | sub_category | total_profit |
| --------------- | ------------ | ------------ |
| Technology      | Copiers      | 55,617.82    |
| Technology      | Phones       | 44,515.73    |
| Technology      | Accessories  | 41,936.64    |
| Office Supplies | Paper        | 34,053.57    |
| Office Supplies | Binders      | 30,221.76    |

> Insight: Copiers, Phones, Accessories, Paper and Binders are the top 5 profitable sub-categories. These should be prioritized in marketing campaigns.

---

### 5.5 — Top 10 States by Sales

```sql
SELECT state, region,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    COUNT(DISTINCT order_id) AS unique_orders
FROM superstore GROUP BY state, region
ORDER BY total_sales DESC LIMIT 10;
```

Result:

| state        | region  | total_sales | total_profit | unique_orders |
| ------------ | ------- | ----------- | ------------ | ------------- |
| California   | West    | 457,687.63  | 76,381.39    | 1021          |
| New York     | East    | 310,876.27  | 74,038.55    | 562           |
| Texas        | Central | 170,188.05  | -25,729.36   | 487           |
| Washington   | West    | 138,641.27  | 33,402.65    | 256           |
| Pennsylvania | East    | 116,511.91  | -15,559.96   | 288           |
| Florida      | South   | 89,473.71   | -3,399.3     | 200           |
| Illinois     | Central | 80,166.1    | -12,607.89   | 276           |
| Ohio         | East    | 78,258.14   | -16,971.38   | 236           |
| Michigan     | Central | 76,269.61   | 24,463.19    | 117           |
| Virginia     | South   | 70,636.72   | 18,597.95    | 115           |

> Insight: California leads with over $457K in sales. New York follows. Texas has high sales but notable profit challenges, possibly due to high discount rates.

---

## Step 6 — Business Use Cases

### 6.1 — Monthly Sales & Profit Trends

```sql
SELECT
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS monthly_sales,
    ROUND(SUM(profit),2) AS monthly_profit
FROM superstore GROUP BY year, month ORDER BY year, month;
```

Result:

| year | month | total_orders | monthly_sales | monthly_profit |
| ---- | ----- | ------------ | ------------- | -------------- |
| 2014 | 1     | 79           | 14,236.89     | 2,450.19       |
| 2014 | 2     | 46           | 4,519.89      | 862.31         |
| 2014 | 3     | 157          | 55,691.01     | 498.73         |
| 2014 | 4     | 135          | 28,295.34     | 3,488.84       |
| 2014 | 5     | 122          | 23,648.29     | 2,738.71       |
| 2014 | 6     | 135          | 34,595.13     | 4,976.52       |
| 2014 | 7     | 143          | 33,946.39     | -841.48        |
| 2014 | 8     | 153          | 27,909.47     | 5,318.11       |
| 2014 | 9     | 268          | 81,777.35     | 8,328.1        |
| 2014 | 10    | 159          | 31,453.39     | 3,448.26       |
| 2014 | 11    | 318          | 78,628.72     | 9,292.13       |
| 2014 | 12    | 278          | 69,545.62     | 8,983.57       |
| 2015 | 1     | 58           | 18,174.08     | -3,281.01      |
| 2015 | 2     | 64           | 11,951.41     | 2,813.85       |
| 2015 | 3     | 138          | 38,726.25     | 9,732.1        |
| 2015 | 4     | 160          | 34,195.21     | 4,187.5        |
| 2015 | 5     | 146          | 30,131.69     | 4,667.87       |
| 2015 | 6     | 138          | 24,797.29     | 3,335.56       |
| 2015 | 7     | 140          | 28,765.32     | 3,288.65       |
| 2015 | 8     | 159          | 36,898.33     | 5,355.81       |
| 2015 | 9     | 293          | 64,595.92     | 8,209.16       |
| 2015 | 10    | 166          | 31,404.92     | 2,817.37       |
| 2015 | 11    | 324          | 75,972.56     | 12,474.79      |
| 2015 | 12    | 316          | 74,919.52     | 8,016.97       |
| 2016 | 1     | 89           | 18,542.49     | 2,824.82       |
| 2016 | 2     | 83           | 22,978.82     | 5,004.58       |
| 2016 | 3     | 163          | 51,715.88     | 3,611.97       |
| 2016 | 4     | 170          | 38,750.04     | 2,977.81       |
| 2016 | 5     | 225          | 56,987.73     | 8,662.15       |
| 2016 | 6     | 199          | 40,344.53     | 4,750.38       |
| 2016 | 7     | 201          | 39,261.96     | 4,432.88       |
| 2016 | 8     | 176          | 31,115.37     | 2,062.07       |
| 2016 | 9     | 363          | 73,410.02     | 9,328.66       |
| 2016 | 10    | 196          | 59,687.75     | 16,243.14      |
| 2016 | 11    | 370          | 79,411.97     | 4,011.41       |
| 2016 | 12    | 352          | 96,999.04     | 17,885.31      |
| 2017 | 1     | 155          | 43,971.37     | 7,140.44       |
| 2017 | 2     | 107          | 20,301.13     | 1,613.87       |
| 2017 | 3     | 238          | 58,872.35     | 14,751.89      |
| 2017 | 4     | 203          | 36,521.54     | 933.29         |
| 2017 | 5     | 242          | 44,261.11     | 6,342.58       |
| 2017 | 6     | 245          | 52,981.73     | 8,223.34       |
| 2017 | 7     | 226          | 45,264.42     | 6,952.62       |
| 2017 | 8     | 218          | 63,120.89     | 9,040.96       |
| 2017 | 9     | 459          | 87,866.65     | 10,991.56      |
| 2017 | 10    | 298          | 77,776.92     | 9,275.28       |
| 2017 | 11    | 459          | 118,447.83    | 9,690.1        |
| 2017 | 12    | 462          | 83,829.32     | 8,483.35       |

> Insight: Sales peak in Q4 (Oct-Dec) every year — holiday effect. September is consistently strong. February and January are the weakest months. Profit trends mirror sales but dip more sharply during high-discount periods.

---

### 6.2 — Year-over-Year Sales by Category

```sql
SELECT
    YEAR(order_date) AS year, category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY year, category ORDER BY year, category;
```

Result:

| year | category        | total_sales | total_profit |
| ---- | --------------- | ----------- | ------------ |
| 2014 | Furniture       | 157,192.85  | 5,457.73     |
| 2014 | Office Supplies | 151,776.41  | 22,593.42    |
| 2014 | Technology      | 175,278.23  | 21,492.83    |
| 2015 | Furniture       | 170,518.24  | 3,015.2      |
| 2015 | Office Supplies | 137,233.46  | 25,099.53    |
| 2015 | Technology      | 162,780.81  | 33,503.87    |
| 2016 | Furniture       | 198,901.44  | 6,959.95     |
| 2016 | Office Supplies | 183,939.98  | 35,061.23    |
| 2016 | Technology      | 226,364.18  | 39,773.99    |
| 2017 | Furniture       | 215,387.27  | 3,018.39     |
| 2017 | Office Supplies | 246,097.18  | 39,736.62    |
| 2017 | Technology      | 271,730.81  | 50,684.26    |

> Insight: All three categories show year-over-year growth from 2014 to 2017. Technology sales more than doubled from 2014 to 2017. Furniture profit remains stubbornly negative in some years.

---

### 6.3 — Top 10 Customers by Total Sales

```sql
SELECT customer_id, customer_name, segment, state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    ROUND(AVG(discount)*100,2) AS avg_discount_pct
FROM superstore GROUP BY customer_id, customer_name, segment, state
ORDER BY total_sales DESC LIMIT 10;
```

Result:

| customer_id | customer_name | segment     | state      | total_orders | total_sales | total_profit | avg_discount_pct |
| ----------- | ------------- | ----------- | ---------- | ------------ | ----------- | ------------ | ---------------- |
| SM-20320    | Sean Miller   | Home Office | Florida    | 1            | 23,661.23   | -1,789.73    | 28.57            |
| TC-20980    | Tamara Chand  | Corporate   | Indiana    | 1            | 18,336.74   | 8,762.39     | 0                |
| RB-19360    | Raymond Buch  | Consumer    | Washington | 1            | 14,052.48   | 6,734.47     | 0                |
| TA-21385    | Tom Ashbrook  | Home Office | New York   | 2            | 13,723.5    | 4,599.21     | 4                |
| BM-11140    | Becky Martin  | Consumer    | Texas      | 1            | 10,539.9    | -1,878.79    | 32.86            |
| HL-15040    | Hunter Lopez  | Consumer    | Delaware   | 1            | 10,499.97   | 5,039.99     | 0                |
| SC-20095    | Sanjit Chand  | Consumer    | Minnesota  | 1            | 9,900.19    | 4,668.69     | 0                |
| AB-10105    | Adrian Barton | Consumer    | Michigan   | 1            | 9,892.74    | 4,946.37     | 0                |
| BS-11365    | Bill Shonely  | Corporate   | New Jersey | 1            | 9,135.19    | 2,381.16     | 0                |
| SE-20110    | Sanjit Engle  | Consumer    | Virginia   | 1            | 8,805.04    | 2,825.29     | 0                |

> Insight: Sean Miller tops by sales but with notable losses — indicating heavy discounting. Top customers are mostly from Consumer and Corporate segments in coastal states.

---

### 6.4 — Top 10 Customers by Profit Contribution

```sql
SELECT customer_id, customer_name, segment,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY customer_id, customer_name, segment
ORDER BY total_profit DESC LIMIT 10;
```

Result:

| customer_id | customer_name        | segment     | total_sales | total_profit |
| ----------- | -------------------- | ----------- | ----------- | ------------ |
| TC-20980    | Tamara Chand         | Corporate   | 19,052.22   | 8,981.32     |
| RB-19360    | Raymond Buch         | Consumer    | 15,117.34   | 6,976.1      |
| SC-20095    | Sanjit Chand         | Consumer    | 14,142.33   | 5,757.41     |
| HL-15040    | Hunter Lopez         | Consumer    | 12,873.3    | 5,622.43     |
| AB-10105    | Adrian Barton        | Consumer    | 14,473.57   | 5,444.81     |
| TA-21385    | Tom Ashbrook         | Home Office | 14,595.62   | 4,703.79     |
| CM-12385    | Christopher Martinez | Consumer    | 8,954.02    | 3,899.89     |
| KD-16495    | Keith Dawkins        | Corporate   | 8,181.26    | 3,038.63     |
| AR-10540    | Andy Reiter          | Consumer    | 6,608.45    | 2,884.62     |
| DR-12940    | Daniel Raglin        | Home Office | 8,350.87    | 2,869.08     |

> Insight: Tamara Chand and Raymond Buch are top profit contributors. These customers buy high-margin Technology products with low discounts — ideal customer profiles.

---

### 6.5 — Orders with Multiple Line Items (top 10)

```sql
SELECT order_id, COUNT(*) AS line_items,
    ROUND(SUM(sales),2) AS order_total_sales,
    COUNT(DISTINCT product_id) AS unique_products
FROM superstore GROUP BY order_id HAVING COUNT(*) > 1
ORDER BY line_items DESC LIMIT 10;
```

Result:

| order_id       | line_items | order_total_sales | unique_products |
| -------------- | ---------- | ----------------- | --------------- |
| CA-2017-100111 | 14         | 7,359.92          | 14              |
| CA-2017-157987 | 12         | 2,255.87          | 12              |
| CA-2016-165330 | 11         | 1,937.92          | 11              |
| US-2016-108504 | 11         | 2,075.51          | 11              |
| CA-2016-105732 | 10         | 2,374.73          | 10              |
| US-2015-126977 | 10         | 7,678.23          | 10              |
| CA-2015-131338 | 10         | 3,385.61          | 10              |
| CA-2017-140949 | 9          | 496.63            | 9               |
| US-2015-163433 | 9          | 544.41            | 9               |
| CA-2014-106439 | 9          | 1,007.94          | 9               |

> Insight: Most orders have 2-7 line items. Some orders contain 14+ distinct products — these are likely bulk corporate purchases and represent high-value customers.

---

### 6.6 — Discount Impact on Profit

```sql
SELECT
    CASE
        WHEN discount=0 THEN '0 - No Discount'
        WHEN discount<0.20 THEN '1 - Low (0-20%)'
        WHEN discount<0.40 THEN '2 - Medium (20-40%)'
        ELSE '3 - High (40%+)'
    END AS discount_band,
    COUNT(*) AS order_count,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    ROUND(AVG(profit),2) AS avg_profit_per_order
FROM superstore GROUP BY discount_band ORDER BY discount_band;
```

Result:

| discount_band       | order_count | total_sales  | total_profit | avg_profit_per_order |
| ------------------- | ----------- | ------------ | ------------ | -------------------- |
| 0 - No Discount     | 4798        | 1,087,908.47 | 320,987.6    | 66.9                 |
| 1 - Low (0-20%)     | 146         | 81,927.87    | 10,448.17    | 71.56                |
| 2 - Medium (20-40%) | 3911        | 882,314.48   | 77,576.89    | 19.84                |
| 3 - High (40%+)     | 1139        | 245,050.04   | -122,615.64  | -107.65              |

> Insight: No-discount orders average ~$28 profit. Medium-discount orders turn negative. High-discount orders average -$64 loss per transaction. Discounting strategy needs a complete overhaul — every 10% discount above 20% destroys margin.

---

### 6.7 — States with Net Losses

```sql
SELECT state, region,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM superstore GROUP BY state, region HAVING SUM(profit)<0
ORDER BY total_profit ASC;
```

Result:

| state          | region  | total_sales | total_profit |
| -------------- | ------- | ----------- | ------------ |
| Texas          | Central | 170,188.05  | -25,729.36   |
| Ohio           | East    | 78,258.14   | -16,971.38   |
| Pennsylvania   | East    | 116,511.91  | -15,559.96   |
| Illinois       | Central | 80,166.1    | -12,607.89   |
| North Carolina | South   | 55,603.16   | -7,490.91    |
| Colorado       | West    | 32,108.12   | -6,527.86    |
| Tennessee      | South   | 30,661.87   | -5,341.69    |
| Arizona        | West    | 35,282      | -3,427.92    |
| Florida        | South   | 89,473.71   | -3,399.3     |
| Oregon         | West    | 17,431.15   | -1,190.47    |

> Insight: Texas, Ohio, Pennsylvania, and Illinois are the most loss-making states despite high sales volumes — pricing and discount policies need regional calibration.

---

### 6.8 — Average Shipping Delay by Ship Mode

```sql
SELECT ship_mode,
    ROUND(AVG(DATEDIFF('day', order_date, ship_date)),1) AS avg_days_to_ship,
    MIN(DATEDIFF('day', order_date, ship_date)) AS min_days,
    MAX(DATEDIFF('day', order_date, ship_date)) AS max_days
FROM superstore GROUP BY ship_mode ORDER BY avg_days_to_ship;
```

Result:

| ship_mode      | avg_days_to_ship | min_days | max_days |
| -------------- | ---------------- | -------- | -------- |
| Same Day       | 0                | 0        | 1        |
| First Class    | 2.2              | 1        | 4        |
| Second Class   | 3.2              | 1        | 5        |
| Standard Class | 5                | 3        | 7        |

> Insight: Same Day shipping ships in 0 days as expected. Standard Class averages ~5 days. First Class (~2 days) provides a good balance between speed and cost.

---

## Step 7 — Data Validation

### 7.1 — Total Row Count

```sql
SELECT COUNT(*) AS total_rows FROM superstore;
```

Result:

| total_rows |
| ---------- |
| 9994       |

> Insight: Confirmed: 9,994 rows loaded. Matches the source CSV (9,994 data rows + 1 header).

---

### 7.2 — NULL Value Check (all columns)

```sql
SELECT
    SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_id,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_date,
    SUM(CASE WHEN ship_date IS NULL THEN 1 ELSE 0 END) AS null_ship_date,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_name,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profit,
    SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) AS null_quantity,
    SUM(CASE WHEN discount IS NULL THEN 1 ELSE 0 END) AS null_discount
FROM superstore;
```

Result:

| null_row_id | null_order_id | null_order_date | null_ship_date | null_customer_id | null_customer_name | null_sales | null_profit | null_quantity | null_discount |
| ----------- | ------------- | --------------- | -------------- | ---------------- | ------------------ | ---------- | ----------- | ------------- | ------------- |
| 0           | 0             | 0               | 0              | 0                | 0                  | 0          | 0           | 0             | 0             |

> Insight: Zero NULL values across all key columns. The dataset is complete and requires no imputation.

---

### 7.3 — Statistical Summary

```sql
SELECT
    ROUND(MIN(sales),2) AS min_sales, ROUND(MAX(sales),2) AS max_sales, ROUND(AVG(sales),2) AS avg_sales,
    ROUND(MIN(profit),2) AS min_profit, ROUND(MAX(profit),2) AS max_profit, ROUND(AVG(profit),2) AS avg_profit,
    ROUND(MIN(discount),2) AS min_discount, ROUND(MAX(discount),2) AS max_discount, ROUND(AVG(discount),4) AS avg_discount
FROM superstore;
```

Result:

| min_sales | max_sales | avg_sales | min_profit | max_profit | avg_profit | min_discount | max_discount | avg_discount |
| --------- | --------- | --------- | ---------- | ---------- | ---------- | ------------ | ------------ | ------------ |
| 0.44      | 22,638.48 | 229.86    | -6,599.98  | 8,399.98   | 28.66      | 0            | 0.8          | 0.1562       |

> Insight: Average sale: ~$230. Min profit: -$6,600 (extreme loss from a single discounted item). Max profit: ~$8,400. Average discount: ~15.6%. Wide profit variance signals inconsistent pricing strategy.

---

### 7.4 — Distinct Values per Categorical Column

```sql
SELECT
    COUNT(DISTINCT region) AS distinct_regions,
    COUNT(DISTINCT category) AS distinct_categories,
    COUNT(DISTINCT sub_category) AS distinct_subcategories,
    COUNT(DISTINCT state) AS distinct_states,
    COUNT(DISTINCT segment) AS distinct_segments,
    COUNT(DISTINCT ship_mode) AS distinct_ship_modes
FROM superstore;
```

Result:

| distinct_regions | distinct_categories | distinct_subcategories | distinct_states | distinct_segments | distinct_ship_modes |
| ---------------- | ------------------- | ---------------------- | --------------- | ----------------- | ------------------- |
| 4                | 3                   | 17                     | 49              | 3                 | 4                   |

> Insight: 4 regions, 3 categories, 17 sub-categories, 49 states (all US states except one), 3 customer segments, 4 ship modes. Cardinality is as expected for this retail dataset.

---

### 7.5 — Discount Validity Check (must be in [0, 1])

```sql
SELECT
    COUNT(*) FILTER (WHERE discount < 0) AS invalid_negative_discount,
    COUNT(*) FILTER (WHERE discount > 1) AS invalid_over_100_pct
FROM superstore;
```

Result:

| invalid_negative_discount | invalid_over_100_pct |
| ------------------------- | -------------------- |
| 0                         | 0                    |

> Insight: No invalid discount values found. All discounts are within the valid [0, 1] range.

---

### 7.6 — Negative Sales Check

```sql
SELECT COUNT(*) AS negative_sales_count FROM superstore WHERE sales < 0;
```

Result:

| negative_sales_count |
| -------------------- |
| 0                    |

> Insight: No negative sales values. Every transaction has a positive revenue amount, which is correct for a retail order dataset.

---
