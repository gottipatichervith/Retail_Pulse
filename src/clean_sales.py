import os
import pandas as pd


# ============================================================
# FILE PATHS
# ============================================================

INPUT_FILE = "data/raw/retailpulse_usecase1_raw_sales.csv"

CLEANED_FILE = "data/processed/cleaned_sales.csv"

REJECTED_FILE = "data/processed/rejected_records.csv"

REPORT_FILE = "reports/data_quality_report.txt"


# ============================================================
# VALID VALUES FROM PROJECT REQUIREMENTS
# ============================================================

VALID_STORES = [
    "ST01",
    "ST02",
    "ST03"
]

VALID_PRODUCTS = [
    "P001",
    "P002",
    "P003",
    "P004",
    "P005",
    "P006",
    "P007"
]

VALID_STATUSES = [
    "Completed",
    "Cancelled",
    "Pending"
]


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    df = pd.read_csv(INPUT_FILE)

    print("Data loaded successfully.")
    print("Total records:", len(df))

    return df


# ============================================================
# CHECK AND VALIDATE DATA
# ============================================================

def validate_data(df):

    # Create gross amount for validation
    df["gross_amount"] = (
        df["quantity"] * df["unit_price"]
    )

    # Convert order date to datetime
    df["order_date_check"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Start with quantity not missing
    df["is_valid"] = df["quantity"].notna()

    # Quantity must be greater than zero
    df["is_valid"] = (
        df["is_valid"]
        & (df["quantity"] > 0)
    )

    # Unit price cannot be negative
    df["is_valid"] = (
        df["is_valid"]
        & (df["unit_price"] >= 0)
    )

    # Discount cannot be negative
    df["is_valid"] = (
        df["is_valid"]
        & (df["discount"] >= 0)
    )

    # Discount cannot be greater than gross amount
    df["is_valid"] = (
        df["is_valid"]
        & (df["discount"] <= df["gross_amount"])
    )

    # Store ID validation
    df["is_valid"] = (
        df["is_valid"]
        & df["store_id"].isin(VALID_STORES)
    )

    # Product ID validation
    df["is_valid"] = (
        df["is_valid"]
        & df["product_id"].isin(VALID_PRODUCTS)
    )

    # Status validation
    df["is_valid"] = (
        df["is_valid"]
        & df["status"].isin(VALID_STATUSES)
    )

    # Order date validation
    df["is_valid"] = (
        df["is_valid"]
        & df["order_date_check"].notna()
    )

    return df


# ============================================================
# CREATE REJECTION REASONS
# ============================================================

def create_rejection_reasons(rejected_df):

    rejected_df["rejection_reason"] = ""

    # Missing quantity
    rejected_df.loc[
        rejected_df["quantity"].isna(),
        "rejection_reason"
    ] = "Missing quantity"

    # Invalid quantity
    rejected_df.loc[
        rejected_df["quantity"] <= 0,
        "rejection_reason"
    ] = "Invalid quantity"

    # Invalid unit price
    rejected_df.loc[
        rejected_df["unit_price"] < 0,
        "rejection_reason"
    ] = "Invalid unit price"

    # Invalid discount
    rejected_df.loc[
        rejected_df["discount"] < 0,
        "rejection_reason"
    ] = "Invalid discount"

    # Discount greater than gross amount
    rejected_df.loc[
        rejected_df["discount"] > rejected_df["gross_amount"],
        "rejection_reason"
    ] = "Discount greater than gross amount"

    # Invalid store ID
    rejected_df.loc[
        ~rejected_df["store_id"].isin(VALID_STORES),
        "rejection_reason"
    ] = "Invalid store ID"

    # Invalid product ID
    rejected_df.loc[
        ~rejected_df["product_id"].isin(VALID_PRODUCTS),
        "rejection_reason"
    ] = "Invalid product ID"

    # Invalid status
    rejected_df.loc[
        ~rejected_df["status"].isin(VALID_STATUSES),
        "rejection_reason"
    ] = "Invalid status"

    # Invalid order date
    rejected_df.loc[
        rejected_df["order_date_check"].isna(),
        "rejection_reason"
    ] = "Invalid order date"

    return rejected_df


# ============================================================
# CALCULATE AMOUNTS FOR CLEANED DATA
# ============================================================

def calculate_amounts(cleaned_df):

    # Gross amount
    cleaned_df["gross_amount"] = (
        cleaned_df["quantity"]
        * cleaned_df["unit_price"]
    )

    # Net amount
    cleaned_df["net_amount"] = (
        cleaned_df["gross_amount"]
        - cleaned_df["discount"]
    )

    return cleaned_df


# ============================================================
# REMOVE HELPER COLUMNS
# ============================================================

def remove_helper_columns(cleaned_df, rejected_df):

    cleaned_df = cleaned_df.drop(
        columns=[
            "is_valid",
            "order_date_check"
        ]
    )

    rejected_df = rejected_df.drop(
        columns=[
            "is_valid",
            "order_date_check"
        ]
    )

    return cleaned_df, rejected_df


# ============================================================
# CREATE DATA QUALITY REPORT
# ============================================================

def create_report(
    df,
    cleaned_df,
    rejected_df
):

    total_records = len(df)

    duplicate_count = df.duplicated().sum()

    valid_records = len(cleaned_df)

    rejected_records = len(rejected_df)

    missing_quantity = (
        df["quantity"].isna().sum()
    )

    invalid_quantity = (
        df["quantity"] <= 0
    ).sum()

    invalid_unit_price = (
        df["unit_price"] < 0
    ).sum()

    invalid_discount = (
        df["discount"] < 0
    ).sum()

    discount_too_high = (
        df["discount"] > df["gross_amount"]
    ).sum()

    invalid_store_id = (
        ~df["store_id"].isin(VALID_STORES)
    ).sum()

    invalid_product_id = (
        ~df["product_id"].isin(VALID_PRODUCTS)
    ).sum()

    invalid_status = (
        ~df["status"].isin(VALID_STATUSES)
    ).sum()

    invalid_dates = (
        df["order_date_check"].isna()
    ).sum()

    report = f"""
RetailPulse - Data Quality Report
=================================

Total raw records: {total_records}
Exact duplicates: {duplicate_count}

Valid records: {valid_records}
Rejected records: {rejected_records}

Data Quality Issues
-------------------

Missing quantity: {missing_quantity}
Invalid quantity: {invalid_quantity}
Invalid unit price: {invalid_unit_price}
Invalid discount: {invalid_discount}
Discount greater than gross amount: {discount_too_high}

Invalid store ID: {invalid_store_id}
Invalid product ID: {invalid_product_id}
Invalid status: {invalid_status}
Invalid order date: {invalid_dates}
"""

    return report


# ============================================================
# SAVE OUTPUT FILES
# ============================================================

def save_outputs(cleaned_df, rejected_df, report):

    # Create output folders if they don't exist
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    # Save cleaned data
    cleaned_df.to_csv(
        CLEANED_FILE,
        index=False
    )

    # Save rejected records
    rejected_df.to_csv(
        REJECTED_FILE,
        index=False
    )

    # Save quality report
    with open(
        REPORT_FILE,
        "w"
    ) as file:

        file.write(report)

    print("\nOutput files created successfully.")
    print("Cleaned file:", CLEANED_FILE)
    print("Rejected file:", REJECTED_FILE)
    print("Report file:", REPORT_FILE)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("========================================")
    print("RetailPulse Data Cleaning Started")
    print("========================================")

    # Step 1: Load data
    df = load_data()

    # Step 2: Validate data
    df = validate_data(df)

    # Step 3: Separate valid and rejected records
    cleaned_df = df[
        df["is_valid"]
    ].copy()

    rejected_df = df[
        ~df["is_valid"]
    ].copy()

    print("\nValidation Summary")
    print("------------------")
    print("Valid records:", len(cleaned_df))
    print("Rejected records:", len(rejected_df))

    # Step 4: Create rejection reasons
    rejected_df = create_rejection_reasons(
        rejected_df
    )

    # Step 5: Calculate amounts
    cleaned_df = calculate_amounts(
        cleaned_df
    )

    # Step 6: Create report
    report = create_report(
        df,
        cleaned_df,
        rejected_df
    )

    # Step 7: Remove helper columns
    cleaned_df, rejected_df = remove_helper_columns(
        cleaned_df,
        rejected_df
    )

    # Step 8: Save outputs
    save_outputs(
        cleaned_df,
        rejected_df,
        report
    )

    print("\n========================================")
    print("RetailPulse Data Cleaning Completed")
    print("========================================")


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()