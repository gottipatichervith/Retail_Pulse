import pandas as pd

from src.validators import (
    validate_required_columns,
    validate_sales_file,
)


def create_valid_sales_data():
    """Create a small valid sales dataset for testing."""
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


def test_required_columns_are_present():
    """Check that all required sales columns exist."""
    df = create_valid_sales_data()

    missing_columns = validate_required_columns(df)

    assert missing_columns == []


def test_missing_required_column_is_detected():
    """Check that a missing required column is detected."""
    df = create_valid_sales_data()

    df = df.drop(columns=["quantity"])

    missing_columns = validate_required_columns(df)

    assert "quantity" in missing_columns


def test_negative_quantity_is_rejected():
    """Check that negative quantity is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "quantity"] = -2

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_negative_unit_price_is_rejected():
    """Check that negative unit price is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "unit_price"] = -100

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_negative_discount_is_rejected():
    """Check that negative discount is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "discount"] = -10

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_invalid_store_is_rejected():
    """Check that an invalid store ID is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "store_id"] = "INVALID_STORE"

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_invalid_product_is_rejected():
    """Check that an invalid product ID is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "product_id"] = "INVALID_PRODUCT"

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_invalid_status_is_rejected():
    """Check that an invalid order status is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "status"] = "InvalidStatus"

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_invalid_order_date_is_rejected():
    """Check that an invalid order date is rejected."""
    df = create_valid_sales_data()
    df.loc[0, "order_date"] = "not-a-date"

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(rejected_df) == 1
    assert len(valid_df) == 0


def test_valid_record_is_accepted():
    """Check that a valid sales record passes validation."""
    df = create_valid_sales_data()

    valid_df, rejected_df, summary = validate_sales_file(df)

    print("SUMMARY:", summary)

    assert len(valid_df) == 1
    assert len(rejected_df) == 0