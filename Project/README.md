# Real-Time Credit Card Fraud Risk Scoring Pipeline

A real-time fraud detection pipeline built on **Databricks**, **PySpark**, and **Delta Lake** following the **Medallion Architecture** (Bronze -> Silver -> Gold).

## Architecture

```
transaction.csv (landing zone)
        |
        v
+------------------+    Auto Loader     +-------------------------------+
|   LANDING ZONE   | --- (streaming) -> |  BRONZE: bronze_transactions  |
|   (CSV files)    |                    |  Raw data + ingestion metadata |
+------------------+                    +---------------+---------------+
                                                        |
customer_profile.csv                                    | readStream
        |                                               v
        +-----(static join)-----------> +-------------------------------+
                                        |  SILVER: silver_transactions  |
                                        |  Cleaned, typed, enriched     |
                                        |  + fraud detection features   |
                                        +---------------+---------------+
                                                        |
                                                        | batch read
                                                        v
                                        +-------------------------------+
                                        |  GOLD: gold_fraud_alerts      |
                                        |  risk_score + fraud_label     |
                                        |  HIGH / MEDIUM / LOW          |
                                        +---------------+---------------+
                                                        |
                                           +------------+------------+
                                           |  Dashboards / Alerts   |
                                           +------------------------+
```

## Project Structure

```
Project/
├── data/
│   ├── transaction.csv               # Raw transaction data (1000+ records)
│   └── customer_profile.csv          # Customer baseline profiles (10 customers)
├── Databricks_Output/
│   ├── Cell Run.webp                 # Screenshot: all notebook cells executed successfully
│   ├── Volumes.webp                  # Screenshot: Unity Catalog Volumes (fraud_data & fraud_checkpoints)
│   └── Workspace.webp                # Screenshot: imported notebooks in Databricks Workspace
├── 01_bronze_layer.py                # Layer 1: Raw ingestion via Auto Loader
├── 02_silver_layer.py                # Layer 2: Cleaning, enrichment & feature engineering
├── 03_gold_layer.py                  # Layer 3: Fraud scoring & risk labelling
├── 04_orchestration.py               # Master pipeline: runs all 3 layers end-to-end
└── README.md
```

## Databricks Output

### Workspace
Notebooks imported into the Databricks Workspace:

![Workspace](Databricks_Output/Workspace.webp)

### Unity Catalog Volumes
`fraud_data` Volume (CSV landing zone) and `fraud_checkpoints` Volume (Auto Loader state):

![Volumes](Databricks_Output/Volumes.webp)

### Pipeline Execution
All cells in `04_orchestration.py` executed successfully — Bronze, Silver, and Gold layers completed with fraud risk scores generated:

![Cell Run](Databricks_Output/Cell%20Run.webp)

## Data

### transaction.csv
| Column | Type | Description |
|---|---|---|
| transaction_id | String | Unique transaction identifier |
| customer_id | String | Customer reference (links to profile) |
| card_id | String | Card used for the transaction |
| transaction_time | Timestamp | Date and time of transaction |
| amount | Double | Transaction amount (INR) |
| merchant | String | Merchant name |
| merchant_category | String | Category (E-commerce, Luxury, Food, etc.) |
| location | String | City where transaction occurred |

### customer_profile.csv
| Column | Type | Description |
|---|---|---|
| customer_id | String | Links to transaction.csv |
| home_location | String | Customer's registered home city |
| avg_spend_per_day | Double | Average daily spending baseline |
| preferred_category | String | Customer's usual merchant category |

## Medallion Layers

### Bronze Layer (`01_bronze_layer.py`)
- Reads `transaction.csv` using **Auto Loader** (`cloudFiles`) in streaming mode
- Appends ingestion metadata: `ingestion_timestamp`, `ingestion_date`, `source_file`
- Writes raw data as-is to `fraud_pipeline.bronze_transactions` Delta table
- Zero business transformations — full audit trail preserved

### Silver Layer (`02_silver_layer.py`)
- Reads Bronze table as a stream
- **Cleans**: casts `transaction_time` to Timestamp, `amount` to Double, drops nulls and zero-amount rows
- **Enriches**: stream-static join with `customer_profile.csv` on `customer_id`
- **Feature engineering**:

| Feature | Description |
|---|---|
| `hour_of_day` | Hour extracted from transaction time |
| `is_weekend` | True if Saturday or Sunday |
| `is_odd_hours` | True if transaction between 00:00-05:59 or 23:00+ |
| `spend_ratio` | amount / avg_spend_per_day |
| `location_mismatch` | True if transaction city != home city |
| `category_mismatch` | True if merchant category != preferred category |

### Gold Layer (`03_gold_layer.py`)
Applies 5 fraud detection rules and computes a cumulative `risk_score`:

| Rule | Condition | Score |
|---|---|---|
| High Amount | spend_ratio > 3x baseline | +40 |
| Location Mismatch | Transaction city != home city | +20 |
| Odd Hours | Transaction at 00:00-05:59 or 23:00+ | +20 |
| Category Mismatch | Merchant category != preferred category | +15 |
| Velocity | More than 1 transaction from same customer in 10 minutes | +30 |

**Risk Labels:**
- `HIGH` - risk_score >= 70 (immediate alert)
- `MEDIUM` - risk_score 40-69 (review required)
- `LOW` - risk_score < 40 (normal)

Writes to `fraud_pipeline.gold_fraud_alerts` Delta table.

## Paths & Storage (Unity Catalog Volumes)

The pipeline uses **Unity Catalog Volumes** for all file storage and checkpoints:

| Purpose | Path |
|---|---|
| Transaction CSV landing zone | `/Volumes/workspace/default/fraud_data/transactions/` |
| Customer profile CSV | `/Volumes/workspace/default/fraud_data/customer_profile.csv` |
| Bronze checkpoint | `/Volumes/workspace/default/fraud_checkpoints/bronze` |
| Silver checkpoint | `/Volumes/workspace/default/fraud_checkpoints/silver` |
| Auto Loader schema location | `/Volumes/workspace/default/fraud_checkpoints/schema/bronze` |

> Checkpoints are kept in a **separate Volume** (`fraud_checkpoints`) from the data (`fraud_data`) to avoid Auto Loader storage-overlap errors.

## How to Run on Databricks

### Setup
1. Create two Unity Catalog Volumes in your Databricks workspace:
   ```
   /Volumes/workspace/default/fraud_data/
   /Volumes/workspace/default/fraud_checkpoints/
   ```

2. Upload the data files into the `fraud_data` Volume:
   ```
   /Volumes/workspace/default/fraud_data/transactions/transaction.csv
   /Volumes/workspace/default/fraud_data/customer_profile.csv
   ```

3. Import the four `.py` notebooks into your Databricks workspace.

4. If your catalog/schema names differ from `workspace.default`, update the paths in the **Global Configuration** cell of `04_orchestration.py`.

### Run Order
Run notebooks individually in this exact order:
```
01_bronze_layer.py   ->   02_silver_layer.py   ->   03_gold_layer.py
```

Or run the master orchestration notebook which executes all three layers automatically:
```
04_orchestration.py
```

### Schedule as a Job
To achieve near real-time fraud detection, schedule `04_orchestration.py` as a Databricks Job with a recurring trigger (e.g., every 5 minutes). Auto Loader will automatically detect and process any new CSV files dropped into the landing zone Volume.

## Tech Stack

| Component | Technology |
|---|---|
| Processing Engine | Apache Spark (PySpark) |
| Storage Format | Delta Lake |
| File Storage | Unity Catalog Volumes |
| Streaming Ingestion | Databricks Auto Loader (`cloudFiles`) |
| Source File Tracking | `_metadata.file_path` (Volumes-compatible) |
| Cluster | Databricks Runtime 13.0+ |
| Architecture | Medallion (Bronze / Silver / Gold) |
