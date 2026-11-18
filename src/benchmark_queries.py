
import sqlite3
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "database" / "retailpulse_pipeline_test.db"

QUERIES = {
    "Total sales": """
        SELECT SUM(net_amount)
        FROM order_items
    """,
    "Sales by product": """
        SELECT product_id, SUM(net_amount)
        FROM order_items
        GROUP BY product_id
    """,
    "Sales by store": """
        SELECT store_id, SUM(net_amount)
        FROM orders
        JOIN order_items USING(order_id)
        GROUP BY store_id
    """,
    "Monthly sales": """
        SELECT substr(order_date, 1, 7), SUM(net_amount)
        FROM orders
        JOIN order_items USING(order_id)
        GROUP BY substr(order_date, 1, 7)
    """
}


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    print("=" * 50)
    print("RETAILPULSE - SQL PERFORMANCE TEST")
    print("=" * 50)

    for name, query in QUERIES.items():
        start = time.perf_counter()

        result = connection.execute(query).fetchall()

        end = time.perf_counter()

        print(f"{name}: {end - start:.4f} seconds")
        print(f"Rows returned: {len(result)}")
        print("-" * 40)

    connection.close()


if __name__ == "__main__":
    main()
