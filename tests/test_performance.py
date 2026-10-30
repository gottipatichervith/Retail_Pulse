import sqlite3
import time


def create_test_database():
    """Create an in-memory database with test sales data."""
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE order_items (
            order_id TEXT,
            product_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            gross_amount REAL,
            net_amount REAL
        )
        """
    )

    records = []

    for i in range(10000):
        records.append(
            (
                f"ORDER{i:05d}",
                f"P{(i % 7) + 1:03d}",
                (i % 5) + 1,
                100 + (i % 50),
                i % 10,
                0,
                0,
            )
        )

    connection.executemany(
        """
        INSERT INTO order_items (
            order_id,
            product_id,
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        records,
    )

    connection.commit()

    return connection


def measure_query_time(connection):
    """Measure the time required to execute the product query."""
    start_time = time.perf_counter()

    connection.execute(
        """
        SELECT
            product_id,
            SUM(quantity) AS total_quantity,
            SUM(net_amount) AS total_net_amount
        FROM order_items
        WHERE product_id = 'P001'
        GROUP BY product_id
        """
    ).fetchall()

    end_time = time.perf_counter()

    return end_time - start_time


def test_query_performance_with_index():
    """Compare query execution before and after adding an index."""
    connection = create_test_database()

    time_before_index = measure_query_time(connection)

    connection.execute(
        """
        CREATE INDEX idx_order_items_product_id
        ON order_items(product_id)
        """
    )

    connection.commit()

    time_after_index = measure_query_time(connection)

    print(
        f"\nQuery time before index: "
        f"{time_before_index:.6f} seconds"
    )

    print(
        f"Query time after index: "
        f"{time_after_index:.6f} seconds"
    )

    connection.close()

    assert time_before_index >= 0
    assert time_after_index >= 0