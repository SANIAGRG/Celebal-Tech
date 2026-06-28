"""
PART 2: DATA CLEANING
Uses pandas to clean orders.csv, products.csv, customers.csv, order_items.csv
"""
import re
import pandas as pd

DATASET_DIR = "dataset"

DATE_DDMMYYYY_RE = re.compile(r"^\d{2}-\d{2}-\d{4}$")
DATE_YYYYMMDD_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def clean_orders(df):
    issues = []
    df = df.copy()

    def fix_date(value):
        value = str(value).strip()
        if DATE_DDMMYYYY_RE.match(value):
            dt = pd.to_datetime(value, format="%d-%m-%Y")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return value

    bad_format_mask = df["order_date"].astype(str).str.match(DATE_DDMMYYYY_RE)
    n_bad_format = bad_format_mask.sum()
    if n_bad_format:
        issues.append(f"Fixed {n_bad_format} order_date rows in DD-MM-YYYY format")
    df["order_date"] = df["order_date"].apply(fix_date)

    # flag any remaining rows that still don't match expected format
    unparseable_mask = ~df["order_date"].astype(str).str.match(DATE_YYYYMMDD_RE)
    if unparseable_mask.sum():
        issues.append(
            f"{unparseable_mask.sum()} order_date rows still don't match YYYY-MM-DD HH:MM:SS after fix"
        )

    missing_cust_mask = df["customer_id"].isna() | (df["customer_id"].astype(str).str.strip() == "")
    n_missing_cust = missing_cust_mask.sum()
    if n_missing_cust:
        issues.append(f"Replaced {n_missing_cust} NULL/empty customer_id values with 'UNKNOWN'")
    df.loc[missing_cust_mask, "customer_id"] = "UNKNOWN"

    return df, issues


def clean_products(df):
    issues = []
    df = df.copy()

    stripped = df["product_name"].astype(str).str.strip()
    n_whitespace = (stripped != df["product_name"].astype(str)).sum()
    if n_whitespace:
        issues.append(f"Stripped extra whitespace from {n_whitespace} product_name values")

    titled = stripped.str.title()
    n_case_changed = (titled != stripped).sum()
    if n_case_changed:
        issues.append(f"Applied title case to {n_case_changed} product_name values")

    df["product_name"] = titled
    return df, issues


def validate_emails(df):
    invalid_customer_ids = []
    for _, row in df.iterrows():
        email = str(row["email"])
        if "@" not in email:
            invalid_customer_ids.append(row["customer_id"])
            continue
        domain = email.split("@", 1)[1]
        if "." not in domain:
            invalid_customer_ids.append(row["customer_id"])
    return invalid_customer_ids


def check_referential_integrity(orders_df, order_items_df):
    valid_order_ids = set(orders_df["order_id"].astype(str))
    orphan_mask = ~order_items_df["order_id"].astype(str).isin(valid_order_ids)
    orphan_item_ids = order_items_df.loc[orphan_mask, "item_id"].tolist()
    return orphan_item_ids


def main():
    print("=" * 60)
    print("PART 2: DATA CLEANING")
    print("=" * 60)

    all_issues = {}

    orders_df = pd.read_csv(f"{DATASET_DIR}/orders.csv", dtype=str)
    products_df = pd.read_csv(f"{DATASET_DIR}/products.csv")
    customers_df = pd.read_csv(f"{DATASET_DIR}/customers.csv", dtype=str)
    order_items_df = pd.read_csv(f"{DATASET_DIR}/order_items.csv")

    orders_clean, order_issues = clean_orders(orders_df)
    all_issues["orders"] = order_issues

    products_clean, product_issues = clean_products(products_df)
    all_issues["products"] = product_issues

    invalid_emails = validate_emails(customers_df)
    all_issues["customers"] = [
        f"Found {len(invalid_emails)} invalid email(s): {invalid_emails[:10]}"
        + ("..." if len(invalid_emails) > 10 else "")
    ] if invalid_emails else ["No invalid emails found"]

    orphan_items = check_referential_integrity(orders_clean, order_items_df)
    all_issues["order_items"] = [
        f"Found {len(orphan_items)} orphan order_item(s): {orphan_items[:10]}"
        + ("..." if len(orphan_items) > 10 else "")
    ] if orphan_items else ["No orphan order_items found"]

    orders_clean.to_csv(f"{DATASET_DIR}/orders_cleaned.csv", index=False)
    products_clean.to_csv(f"{DATASET_DIR}/products_cleaned.csv", index=False)
    customers_df.to_csv(f"{DATASET_DIR}/customers_cleaned.csv", index=False)
    order_items_df.to_csv(f"{DATASET_DIR}/order_items_cleaned.csv", index=False)

    print("\nSaved cleaned files: orders_cleaned.csv, products_cleaned.csv, "
          "customers_cleaned.csv, order_items_cleaned.csv")

    print("\n--- ISSUES REPORT ---")
    for section, issues in all_issues.items():
        print(f"\n[{section}]")
        for issue in issues:
            print(f"  - {issue}")

    print("\nData cleaning complete.")


if __name__ == "__main__":
    main()
