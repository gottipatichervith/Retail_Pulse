import sqlite3
import pytest


@pytest.fixture
def test_database():
    """Create a temporary database for incremental loading tests."""
    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE order_items (
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            discount REAL NOT NULL,
            gross_amount REAL NOT NULL,
            net_amount REAL NOT NULL,
            UNIQUE(order_id, product_id)
        )
        """
    )

    yield connection

    connection.close()


def insert_order_item(connection, order_id, product_id, quantity, unit_price, discount):
    """Insert an order item into the test database."""
    gross_amount = quantity * unit_price
    net_amount = gross_amount - discount

    connection.execute(
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
        (
            order_id,
            product_id,
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount,
        ),
    )

    connection.commit()


def test_new_record_is_inserted(test_database):
    """Check that a new order-item record can be inserted."""
    insert_order_item(
        test_database,
        "TEST001",
        "P001",
        2,
        100,
        10,
    )

    cursor = test_database.execute(
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE order_id = ?
          AND product_id = ?
        """,
        ("TEST001", "P001"),
    )

    count = cursor.fetchone()[0]

    assert count == 1


def test_existing_record_can_be_updated(test_database):
    """Check that an existing order-item record can be updated."""
    insert_order_item(
        test_database,
        "TEST001",
        "P001",
        2,
        100,
        10,
    )

    new_quantity = 5
    new_unit_price = 120
    new_discount = 20

    new_gross_amount = new_quantity * new_unit_price
    new_net_amount = new_gross_amount - new_discount

    test_database.execute(
        """
        UPDATE order_items
        SET
            quantity = ?,
            unit_price = ?,
            discount = ?,
            gross_amount = ?,
            net_amount = ?
        WHERE order_id = ?
          AND product_id = ?
        """,
        (
            new_quantity,
            new_unit_price,
            new_discount,
            new_gross_amount,
            new_net_amount,
            "TEST001",
            "P001",
        ),
    )

    test_database.commit()

    cursor = test_database.execute(
        """
        SELECT
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount
        FROM order_items
        WHERE order_id = ?
          AND product_id = ?
        """,
        ("TEST001", "P001"),
    )

    result = cursor.fetchone()

    assert result == (5, 120, 20, 600, 580)


def test_same_record_does_not_create_duplicate(test_database):
    """Check that the same order-item cannot be inserted twice."""
    insert_order_item(
        test_database,
        "TEST001",
        "P001",
        2,
        100,
        10,
    )

    with pytest.raises(sqlite3.IntegrityError):
        insert_order_item(
            test_database,
            "TEST001",
            "P001",
            2,
            100,
            10,
        )


def test_different_product_same_order_is_allowed(test_database):
    """Check that one order can contain multiple products."""
    insert_order_item(
        test_database,
        "TEST001",
        "P001",
        2,
        100,
        10,
    )

    insert_order_item(
        test_database,
        "TEST001",
        "P002",
        3,
        50,
        5,
    )

    cursor = test_database.execute(
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE order_id = ?
        """,
        ("TEST001",),
    )

    count = cursor.fetchone()[0]

    assert count == 2