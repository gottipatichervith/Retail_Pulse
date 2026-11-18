
import sqlite3
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

    print("EXISTING DATABASE INDEXES")
    indexes = connection.execute("""
        SELECT name, tbl_name
        FROM sqlite_master
        WHERE type = 'index'
        AND sql IS NOT NULL
    """).fetchall()

    for index in indexes:
        print(index)

    print("\nQUERY EXECUTION PLANS")

    for name, query in QUERIES.items():
        print(f"\n{name}")

        plan = connection.execute(
            "EXPLAIN QUERY PLAN " + query
        ).fetchall()

        for row in plan:
            print(row)

    connection.close()


if __name__ == "__main__":
    main()
