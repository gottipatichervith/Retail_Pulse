import pandas as pd


# ============================================================
# VALID VALUES FROM RETAILPULSE PROJECT
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
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "store_id",
    "product_id",
    "customer_id",
    "quantity",
    "unit_price",
    "discount",
    "status"
]


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

def validate_required_columns(df):
    """
    Check whether the incoming CSV contains all required columns.

    Returns:
        missing_columns: list of missing columns
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns


# ============================================================
# VALIDATE DATA
# ============================================================

def validate_data(df):
    """
    Validate incoming sales records using the same business
    rules used in RetailPulse Use Case 1.

    Returns:
        validated_df: DataFrame containing validation results
    """

    df = df.copy()

    # --------------------------------------------------------
    # Create gross amount for validation
    # --------------------------------------------------------

    df["gross_amount"] = (
        df["quantity"] * df["unit_price"]
    )

    # --------------------------------------------------------
    # Convert order date to datetime for validation
    # --------------------------------------------------------

    df["order_date_check"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Start with quantity not missing
    # --------------------------------------------------------

    df["is_valid"] = df["quantity"].notna()

    # --------------------------------------------------------
    # Quantity must be greater than zero
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & (df["quantity"] > 0)
    )

    # --------------------------------------------------------
    # Unit price cannot be negative
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & (df["unit_price"] >= 0)
    )

    # --------------------------------------------------------
    # Discount cannot be negative
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & (df["discount"] >= 0)
    )

    # --------------------------------------------------------
    # Discount cannot be greater than gross amount
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & (df["discount"] <= df["gross_amount"])
    )

    # --------------------------------------------------------
    # Store ID validation
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & df["store_id"].isin(VALID_STORES)
    )

    # --------------------------------------------------------
    # Product ID validation
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & df["product_id"].isin(VALID_PRODUCTS)
    )

    # --------------------------------------------------------
    # Status validation
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & df["status"].isin(VALID_STATUSES)
    )

    # --------------------------------------------------------
    # Order date validation
    # --------------------------------------------------------

    df["is_valid"] = (
        df["is_valid"]
        & df["order_date_check"].notna()
    )

    return df


# ============================================================
# CREATE REJECTION REASONS
# ============================================================

def create_rejection_reasons(rejected_df):
    """
    Add a rejection_reason column to invalid records.

    The first matching validation reason is kept.
    """

    rejected_df = rejected_df.copy()

    rejected_df["rejection_reason"] = ""

    # --------------------------------------------------------
    # Missing quantity
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["quantity"].isna()
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Missing quantity"

    # --------------------------------------------------------
    # Invalid quantity
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["quantity"].notna()
        & (rejected_df["quantity"] <= 0)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid quantity"

    # --------------------------------------------------------
    # Invalid unit price
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["unit_price"].notna()
        & (rejected_df["unit_price"] < 0)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid unit price"

    # --------------------------------------------------------
    # Invalid discount
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["discount"].notna()
        & (rejected_df["discount"] < 0)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid discount"

    # --------------------------------------------------------
    # Discount greater than gross amount
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["discount"].notna()
        & rejected_df["gross_amount"].notna()
        & (
            rejected_df["discount"]
            > rejected_df["gross_amount"]
        )
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Discount greater than gross amount"

    # --------------------------------------------------------
    # Invalid store ID
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & ~rejected_df["store_id"].isin(VALID_STORES)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid store ID"

    # --------------------------------------------------------
    # Invalid product ID
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & ~rejected_df["product_id"].isin(VALID_PRODUCTS)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid product ID"

    # --------------------------------------------------------
    # Invalid status
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & ~rejected_df["status"].isin(VALID_STATUSES)
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid status"

    # --------------------------------------------------------
    # Invalid order date
    # --------------------------------------------------------

    mask = (
        rejected_df["rejection_reason"].eq("")
        & rejected_df["order_date_check"].isna()
    )

    rejected_df.loc[
        mask,
        "rejection_reason"
    ] = "Invalid order date"

    return rejected_df


# ============================================================
# CALCULATE AMOUNTS
# ============================================================

def calculate_amounts(df):
    """
    Calculate gross_amount and net_amount for valid records.
    """

    df = df.copy()

    df["gross_amount"] = (
        df["quantity"]
        * df["unit_price"]
    )

    df["net_amount"] = (
        df["gross_amount"]
        - df["discount"]
    )

    return df


# ============================================================
# CHECK EXACT DUPLICATES
# ============================================================

def find_exact_duplicates(df):
    """
    Find exact duplicate rows.

    This does NOT treat repeated order_id values as duplicates,
    because one order may contain multiple products.

    Returns:
        DataFrame containing exact duplicate rows.
    """

    duplicate_mask = df.duplicated(
        keep=False
    )

    duplicates = df[
        duplicate_mask
    ].copy()

    return duplicates


# ============================================================
# SEPARATE VALID AND REJECTED RECORDS
# ============================================================

def separate_valid_and_rejected(df):
    """
    Separate records into valid and rejected DataFrames.

    Returns:
        valid_df
        rejected_df
    """

    valid_df = df[
        df["is_valid"]
    ].copy()

    rejected_df = df[
        ~df["is_valid"]
    ].copy()

    return valid_df, rejected_df


# ============================================================
# REMOVE HELPER COLUMNS
# ============================================================

def remove_helper_columns(df):
    """
    Remove temporary validation columns before saving data.
    """

    helper_columns = [
        "is_valid",
        "order_date_check"
    ]

    existing_columns = [
        column
        for column in helper_columns
        if column in df.columns
    ]

    return df.drop(
        columns=existing_columns
    )


# ============================================================
# COMPLETE VALIDATION FUNCTION
# ============================================================

def validate_sales_file(df):
    """
    Run the complete validation process for an incoming
    RetailPulse sales CSV.

    Returns:
        valid_df
        rejected_df
        validation_summary
    """

    # --------------------------------------------------------
    # Check required columns first
    # --------------------------------------------------------

    missing_columns = validate_required_columns(df)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # --------------------------------------------------------
    # Validate records
    # --------------------------------------------------------

    validated_df = validate_data(df)

    # --------------------------------------------------------
    # Separate valid and rejected records
    # --------------------------------------------------------

    valid_df, rejected_df = (
        separate_valid_and_rejected(
            validated_df
        )
    )

    # --------------------------------------------------------
    # Create rejection reasons
    # --------------------------------------------------------

    rejected_df = create_rejection_reasons(
        rejected_df
    )

    # --------------------------------------------------------
    # Calculate final amounts for valid records
    # --------------------------------------------------------

    valid_df = calculate_amounts(
        valid_df
    )

    # --------------------------------------------------------
    # Find exact duplicates
    # --------------------------------------------------------

    duplicate_df = find_exact_duplicates(
        df
    )

    # --------------------------------------------------------
    # Remove helper columns
    # --------------------------------------------------------

    valid_df = remove_helper_columns(
        valid_df
    )

    rejected_df = remove_helper_columns(
        rejected_df
    )

    # --------------------------------------------------------
    # Create validation summary
    # --------------------------------------------------------

    validation_summary = {
        "records_read": len(df),
        "valid_records": len(valid_df),
        "rejected_records": len(rejected_df),
        "exact_duplicate_rows": len(duplicate_df)
    }

    return (
        valid_df,
        rejected_df,
        validation_summary
    )