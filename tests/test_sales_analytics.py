import pandas as pd

from src.validators import calculate_amounts


def create_sales_data():
    """Create a small sales dataset for testing calculations."""
    return pd.DataFrame(
        {
            "order_id": ["TEST001"],
            "order_date": ["2026-01-15"],
            "store_id": ["ST01"],
            "product_id": ["P001"],
            "customer_id": ["C001"],
            "quantity": [2],
            "unit_price": [100],
            "discount": [10],
            "status": ["Completed"],
        }
    )


def test_gross_amount_is_calculated_correctly():
    """Check that gross amount equals quantity multiplied by unit price."""
    df = create_sales_data()

    result = calculate_amounts(df)

    assert result.loc[0, "gross_amount"] == 200


def test_net_amount_is_calculated_correctly():
    """Check that net amount equals gross amount minus discount."""
    df = create_sales_data()

    result = calculate_amounts(df)

    assert result.loc[0, "net_amount"] == 190


def test_multiple_records_are_calculated_correctly():
    """Check that each sales record is calculated independently."""
    df = pd.DataFrame(
        {
            "order_id": ["TEST001", "TEST002"],
            "order_date": ["2026-01-15", "2026-01-16"],
            "store_id": ["ST01", "ST02"],
            "product_id": ["P001", "P002"],
            "customer_id": ["C001", "C002"],
            "quantity": [2, 3],
            "unit_price": [100, 50],
            "discount": [10, 5],
            "status": ["Completed", "Completed"],
        }
    )

    result = calculate_amounts(df)

    assert result.loc[0, "gross_amount"] == 200
    assert result.loc[0, "net_amount"] == 190

    assert result.loc[1, "gross_amount"] == 150
    assert result.loc[1, "net_amount"] == 145