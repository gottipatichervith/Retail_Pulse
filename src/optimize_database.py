
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "database" / "retailpulse_pipeline_test.db"


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_order_items_product
            ON order_items(product_id)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_orders_store
            ON orders(store_id)
        """)

        connection.commit()

        connection.execute("ANALYZE")
        connection.commit()

        print("Database optimization completed!")
        print("Created or verified these indexes:")
        print("- idx_order_items_product")
        print("- idx_orders_store")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
