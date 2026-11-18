
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "database" / "retailpulse_pipeline_test.db"


def main():
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        connection.execute(
            "DROP INDEX IF EXISTS idx_order_items_product"
        )

        connection.execute(
            "DROP INDEX IF EXISTS idx_orders_store"
        )

        connection.commit()

        print("Additional test indexes removed successfully.")
        print("Original database indexes are preserved.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
