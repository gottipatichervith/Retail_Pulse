
import random
from pathlib import Path
import pandas as pd


# Project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Output file
OUTPUT_FILE = BASE_DIR / "data" / "incoming" / "large_sales_100k.csv"

# Dataset size
TOTAL_RECORDS = 100_000

# Valid reference IDs from the test database
CUSTOMERS = [f"C{i:03d}" for i in range(1, 6)]

STORES = ["ST01", "ST02", "ST03"]

PRODUCT_PRICES = {
    "P001": 500,
    "P002": 1200,
    "P003": 250,
    "P004": 800,
    "P005": 1500,
    "P006": 150,
    "P007": 2200,
}

random.seed(42)


def generate_sales_data():
    records = []

    product_ids = list(PRODUCT_PRICES.keys())

    for i in range(1, TOTAL_RECORDS + 1):

        order_id = f"PERF{i:06d}"

        product_id = random.choice(product_ids)
        store_id = random.choice(STORES)
        customer_id = random.choice(CUSTOMERS)

        quantity = random.randint(1, 5)
        unit_price = PRODUCT_PRICES[product_id]

        gross_amount = quantity * unit_price

        discount = random.randint(
            0,
            min(100, int(gross_amount * 0.10))
        )

        net_amount = gross_amount - discount

        order_date = (
            pd.Timestamp("2026-03-01")
            + pd.Timedelta(days=random.randint(0, 364))
        ).strftime("%Y-%m-%d")

        records.append({
            "order_id": order_id,
            "order_date": order_date,
            "store_id": store_id,
            "product_id": product_id,
            "customer_id": customer_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "status": "Completed",
            "gross_amount": gross_amount,
            "net_amount": net_amount,
        })

    return pd.DataFrame(records)


def main():
    print("Generating synthetic RetailPulse sales data...")

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = generate_sales_data()

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nDataset generated successfully!")
    print(f"Total records: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nSample records:")
    print(df.head())

    print("\nDataset information:")
    print(df.info())

    print("\nMissing values:")
    print(df.isnull().sum().sum())


if __name__ == "__main__":
    main()
