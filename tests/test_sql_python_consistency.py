import sqlite3

import pandas as pd


def create_test_sales_data():
    """Create a small dataset for SQL/Python consistency testing."""
    return pd.DataFrame(
        {
            "order_id": ["TEST001", "TEST002", "TEST003"],
            "quantity": [2, 3, 1],
            "unit_price": [100, 50, 200],
            "discount": [10, 5, 20],
            "status": ["Completed", "Completed", "Cancelled"],
        }
    )


def create_test_database():
    """Create an in-memory SQLite database with test sales data."""
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE order_items (
            order_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            gross_amount REAL,
            net_amount REAL
        )
        """
    )

    sales_data = create_test_sales_data()

    sales_data["gross_amount"] = (
        sales_data["quantity"] * sales_data["unit_price"]
    )

    sales_data["net_amount"] = (
        sales_data["gross_amount"] - sales_data["discount"]
    )

    sales_data[
        [
            "order_id",
            "quantity",
            "unit_price",
            "discount",
            "gross_amount",
            "net_amount",
        ]
    ].to_sql(
        "order_items",
        connection,
        if_exists="append",
        index=False,
    )

    return connection


def test_sql_and_python_total_net_sales_match():
    """Check that SQL and Python calculate the same total net sales."""
    sales_data = create_test_sales_data()

    # Independent Python calculation
    sales_data["gross_amount"] = (
        sales_data["quantity"] * sales_data["unit_price"]
    )

    sales_data["net_amount"] = (
        sales_data["gross_amount"] - sales_data["discount"]
    )

    python_total = sales_data["net_amount"].sum()

    # SQL calculation
    connection = create_test_database()

    cursor = connection.execute(
        """
        SELECT SUM(net_amount)
        FROM order_items
        """
    )

    sql_total = cursor.fetchone()[0]

    connection.close()

    assert python_total == sql_total


def test_sql_and_python_completed_sales_match():
    """Check that SQL and Python calculate completed sales consistently."""
    sales_data = create_test_sales_data()

    # Independent Python calculation
    completed_sales = sales_data[
        sales_data["status"] == "Completed"
    ].copy()

    completed_sales["gross_amount"] = (
        completed_sales["quantity"]
        * completed_sales["unit_price"]
    )

    completed_sales["net_amount"] = (
        completed_sales["gross_amount"]
        - completed_sales["discount"]
    )

    python_total = completed_sales["net_amount"].sum()

    # Create database including status
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE order_items (
            order_id TEXT,
            quantity INTEGER,
            unit_price REAL,
            discount REAL,
            status TEXT,
            gross_amount REAL,
            net_amount REAL
        )
        """
    )

    database_data = create_test_sales_data()

    database_data["gross_amount"] = (
        database_data["quantity"]
        * database_data["unit_price"]
    )

    database_data["net_amount"] = (
        database_data["gross_amount"]
        - database_data["discount"]
    )

    database_data.to_sql(
        "order_items",
        connection,
        if_exists="append",
        index=False,
    )

    cursor = connection.execute(
        """
        SELECT SUM(net_amount)
        FROM order_items
        WHERE status = 'Completed'
        """
    )

    sql_total = cursor.fetchone()[0]

    connection.close()

    assert python_total == sql_total