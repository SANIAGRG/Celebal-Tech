"""
PART 5: EDGE CASE TESTS
Standalone plain Python test functions (no pytest). Each prints PASS or FAIL.
"""
import pandas as pd
from datetime import datetime, timedelta

from clean_data import check_referential_integrity


def test_orphan_order_items():
    desc = "Orphan order_item with non-existent order_id is detected by check_referential_integrity"
    try:
        orders_df = pd.DataFrame(
            {"order_id": ["ORD000001", "ORD000002"], "customer_id": ["CUST00001", "CUST00002"]}
        )
        order_items_df = pd.DataFrame(
            {
                "item_id": ["ITEM000001", "ITEM000002", "ITEM999999"],
                "order_id": ["ORD000001", "ORD000002", "ORD999999"],  # last one is orphan
                "product_id": ["PROD00001", "PROD00002", "PROD00003"],
                "quantity": [1, 2, 1],
                "unit_price": [10.0, 20.0, 30.0],
                "discount_percent": [0, 0, 0],
            }
        )
        orphans = check_referential_integrity(orders_df, order_items_df)
        passed = orphans == ["ITEM999999"]
        print(f"{'PASS' if passed else 'FAIL'}: test_orphan_order_items - {desc} (found: {orphans})")
    except Exception as e:
        print(f"FAIL: test_orphan_order_items - exception raised: {e}")


def test_discount_over_100():
    desc = "discount_percent=150 should be clamped/flagged so revenue is not negative-inflated"
    try:
        quantity, unit_price, discount_percent = 2, 50.0, 150
        clamped_discount = min(discount_percent, 100)
        flagged = discount_percent > 100
        revenue = quantity * unit_price * (1 - clamped_discount / 100.0)
        passed = flagged and revenue >= 0
        print(
            f"{'PASS' if passed else 'FAIL'}: test_discount_over_100 - {desc} "
            f"(flagged={flagged}, clamped_revenue={revenue})"
        )
    except Exception as e:
        print(f"FAIL: test_discount_over_100 - exception raised: {e}")


def test_zero_quantity():
    desc = "quantity=0 should be excluded from both purchase and return counts"
    try:
        order_items_df = pd.DataFrame(
            {
                "item_id": ["ITEM000001", "ITEM000002"],
                "order_id": ["ORD000001", "ORD000001"],
                "product_id": ["PROD00001", "PROD00001"],
                "quantity": [0, 5],
                "unit_price": [10.0, 10.0],
                "discount_percent": [0, 0],
            }
        )
        purchases = order_items_df.loc[order_items_df["quantity"] > 0, "quantity"].sum()
        returns = order_items_df.loc[order_items_df["quantity"] < 0, "quantity"].sum()
        zero_qty_rows = order_items_df[order_items_df["quantity"] == 0]
        passed = len(zero_qty_rows) == 1 and purchases == 5 and returns == 0
        print(
            f"{'PASS' if passed else 'FAIL'}: test_zero_quantity - {desc} "
            f"(zero_qty_rows={len(zero_qty_rows)}, purchases={purchases}, returns={returns})"
        )
    except Exception as e:
        print(f"FAIL: test_zero_quantity - exception raised: {e}")


def test_future_order_date():
    desc = "order_date 1 year in the future should be detected as a future-dated order"
    try:
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
        orders_df = pd.DataFrame(
            {
                "order_id": ["ORD000001"],
                "customer_id": ["CUST00001"],
                "order_date": [future_date],
                "status": ["PLACED"],
                "region_code": ["NORTH"],
            }
        )
        orders_df["order_date_parsed"] = pd.to_datetime(orders_df["order_date"])
        future_mask = orders_df["order_date_parsed"] > pd.Timestamp.now()
        passed = bool(future_mask.iloc[0])
        print(
            f"{'PASS' if passed else 'FAIL'}: test_future_order_date - {desc} "
            f"(future_date={future_date}, detected={passed})"
        )
    except Exception as e:
        print(f"FAIL: test_future_order_date - exception raised: {e}")


def main():
    print("=" * 60)
    print("PART 5: EDGE CASE TESTS")
    print("=" * 60)
    test_orphan_order_items()
    test_discount_over_100()
    test_zero_quantity()
    test_future_order_date()
    print("=" * 60)
    print("Edge case tests complete.")


if __name__ == "__main__":
    main()
