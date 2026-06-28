"""
PART 1: DATA GENERATION
Generates orders.csv, order_items.csv, products.csv, customers.csv
using only faker and random.
"""
import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

DATASET_DIR = "dataset"

N_CUSTOMERS = 520
N_ORDERS = 600
N_PRODUCTS = 540
N_ORDER_ITEMS_MIN = 520

REGIONS = ["NORTH", "SOUTH", "EAST", "WEST"]
ORDER_STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
CUSTOMER_TYPES = ["REGULAR", "PREMIUM", "VIP"]
CATEGORIES = {
    "Electronics": ["Phones", "Laptops", "Accessories", "Audio"],
    "Clothing": ["Men", "Women", "Kids", "Footwear"],
    "Home": ["Kitchen", "Furniture", "Decor", "Bedding"],
    "Books": ["Fiction", "NonFiction", "Comics", "Educational"],
}


def random_date_within(days_back=730):
    start = datetime.now() - timedelta(days=days_back)
    delta_seconds = int((datetime.now() - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta_seconds))


def generate_customers():
    customers = []
    for i in range(1, N_CUSTOMERS + 1):
        customer_id = f"CUST{i:05d}"
        name = fake.name()
        if random.random() < 0.02:
            # invalid email: missing @ or missing domain dot
            bad_type = random.choice(["no_at", "no_domain_dot"])
            local = fake.user_name()
            if bad_type == "no_at":
                email = f"{local}example.com"
            else:
                email = f"{local}@examplecom"
        else:
            email = fake.email()
        reg_date = fake.date_between(start_date="-3y", end_date="today")
        customer_type = random.choices(
            CUSTOMER_TYPES, weights=[0.6, 0.3, 0.1]
        )[0]
        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": name,
                "email": email,
                "registration_date": reg_date.strftime("%Y-%m-%d"),
                "customer_type": customer_type,
            }
        )
    return customers


def generate_products():
    products = []
    for i in range(1, N_PRODUCTS + 1):
        product_id = f"PROD{i:05d}"
        category = random.choice(list(CATEGORIES.keys()))
        subcategory = random.choice(CATEGORIES[category])
        base_name = f"{fake.word().capitalize()} {subcategory[:-1] if subcategory.endswith('s') else subcategory}"
        # introduce dirty data: extra spaces / mixed case
        if random.random() < 0.25:
            dirty_choice = random.choice(["spaces", "upper", "lower", "mixed"])
            if dirty_choice == "spaces":
                base_name = f"  {base_name}   "
            elif dirty_choice == "upper":
                base_name = base_name.upper()
            elif dirty_choice == "lower":
                base_name = base_name.lower()
            else:
                base_name = "  " + base_name.swapcase() + " "
        cost_price = round(random.uniform(5, 1500), 2)
        products.append(
            {
                "product_id": product_id,
                "product_name": base_name,
                "category": category,
                "subcategory": subcategory,
                "cost_price": cost_price,
            }
        )
    return products


def generate_orders(customer_ids):
    orders = []
    for i in range(1, N_ORDERS + 1):
        order_id = f"ORD{i:06d}"
        if random.random() < 0.05:
            customer_id = ""  # missing customer id
        else:
            customer_id = random.choice(customer_ids)

        order_dt = random_date_within(730)
        if random.random() < 0.05:
            order_date_str = order_dt.strftime("%d-%m-%Y")  # wrong format
        else:
            order_date_str = order_dt.strftime("%Y-%m-%d %H:%M:%S")

        status = random.choices(
            ORDER_STATUSES, weights=[0.15, 0.2, 0.45, 0.1, 0.1]
        )[0]
        region_code = random.choice(REGIONS)

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date_str,
                "status": status,
                "region_code": region_code,
            }
        )
    return orders


def generate_order_items(order_ids, product_ids):
    items = []
    item_counter = 1
    # ensure every order has at least 1 item
    for order_id in order_ids:
        n_items = random.randint(1, 4)
        for _ in range(n_items):
            item_id = f"ITEM{item_counter:06d}"
            item_counter += 1
            product_id = random.choice(product_ids)
            if random.random() < 0.03:
                quantity = -random.randint(1, 5)  # return
            else:
                quantity = random.randint(1, 10)
            unit_price = round(random.uniform(5, 2000), 2)
            discount_percent = round(random.uniform(0, 100), 2)
            items.append(
                {
                    "item_id": item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_percent": discount_percent,
                }
            )
    # top up to ensure 500+ rows minimum
    while len(items) < N_ORDER_ITEMS_MIN:
        item_id = f"ITEM{item_counter:06d}"
        item_counter += 1
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(5, 2000), 2)
        discount_percent = round(random.uniform(0, 100), 2)
        items.append(
            {
                "item_id": item_id,
                "order_id": order_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount_percent": discount_percent,
            }
        )
    return items


def write_csv(filename, rows, fieldnames):
    os.makedirs(DATASET_DIR, exist_ok=True)
    filename = os.path.join(DATASET_DIR, filename)
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows)} rows -> {filename}")


def main():
    print("=" * 60)
    print("PART 1: DATA GENERATION")
    print("=" * 60)

    customers = generate_customers()
    write_csv(
        "customers.csv",
        customers,
        ["customer_id", "customer_name", "email", "registration_date", "customer_type"],
    )

    products = generate_products()
    write_csv(
        "products.csv",
        products,
        ["product_id", "product_name", "category", "subcategory", "cost_price"],
    )

    customer_ids = [c["customer_id"] for c in customers]
    orders = generate_orders(customer_ids)
    write_csv(
        "orders.csv",
        orders,
        ["order_id", "customer_id", "order_date", "status", "region_code"],
    )

    order_ids = [o["order_id"] for o in orders]
    product_ids = [p["product_id"] for p in products]
    order_items = generate_order_items(order_ids, product_ids)
    write_csv(
        "order_items.csv",
        order_items,
        ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"],
    )

    print("\nData generation complete.")
    print(f"  customers: {len(customers)} rows")
    print(f"  products: {len(products)} rows")
    print(f"  orders: {len(orders)} rows")
    print(f"  order_items: {len(order_items)} rows")


if __name__ == "__main__":
    main()
