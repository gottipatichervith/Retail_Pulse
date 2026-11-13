
from pathlib import Path
import pandas as pd

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "forecasting_dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

# Create output folder if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def prepare_forecasting_data():

    print("=" * 55)
    print("RETAILPULSE - FORECASTING DATA PREPARATION")
    print("=" * 55)

    # 1. Read CSV
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Forecasting dataset is empty.")

    print(f"\nRecords loaded: {len(df)}")

    # 2. Check required columns
    required_columns = [
        "sales_date",
        "product_id",
        "store_id",
        "daily_quantity"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    # 3. Convert data types
    df["sales_date"] = pd.to_datetime(
        df["sales_date"], errors="coerce"
    )

    df["daily_quantity"] = pd.to_numeric(
        df["daily_quantity"], errors="coerce"
    )

    # 4. Check missing values
    print("\nMissing values before cleaning:")
    print(df[required_columns].isnull().sum())

    # Remove records with missing required values
    df = df.dropna(subset=required_columns)

    # 5. Check invalid quantities
    invalid_rows = df[df["daily_quantity"] < 0]

    if not invalid_rows.empty:
        raise ValueError(
            f"Found {len(invalid_rows)} records with negative quantities."
        )

    # 6. Remove duplicate product-store-date records
    duplicate_count = df.duplicated(
        subset=["sales_date", "product_id", "store_id"]
    ).sum()

    print(f"\nDuplicate records found: {duplicate_count}")

    if duplicate_count > 0:
        raise ValueError(
            "Duplicate product-store-date records found. "
            "Please investigate before continuing."
        )

    # 7. Sort records chronologically
    df = df.sort_values(
        ["sales_date", "store_id", "product_id"]
    ).reset_index(drop=True)

    # 8. Check dataset information
    print("\nDataset summary:")
    print(f"Total records: {len(df)}")
    print(f"Date range: {df['sales_date'].min().date()} "
          f"to {df['sales_date'].max().date()}")
    print(f"Products: {df['product_id'].nunique()}")
    print(f"Stores: {df['store_id'].nunique()}")
    print(f"Total units sold: {df['daily_quantity'].sum()}")

    # 9. Split using dates, not random sampling
    unique_dates = sorted(df["sales_date"].unique())

    if len(unique_dates) <= 7:
        raise ValueError(
            "At least 8 dates are needed for a 7-day test period."
        )

    test_dates = unique_dates[-7:]
    first_test_date = test_dates[0]

    train_df = df[df["sales_date"] < first_test_date].copy()
    test_df = df[df["sales_date"].isin(test_dates)].copy()

    # 10. Save output files
    prepared_file = OUTPUT_DIR / "prepared_forecasting_data.csv"
    train_file = OUTPUT_DIR / "forecast_train.csv"
    test_file = OUTPUT_DIR / "forecast_test.csv"

    df.to_csv(prepared_file, index=False)

    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)

    print("\nTime-based split:")
    print(f"Training records: {len(train_df)}")
    print(f"Testing records: {len(test_df)}")
    print(f"Training ends: {train_df['sales_date'].max().date()}")
    print(f"Testing starts: {test_df['sales_date'].min().date()}")

    print("\nFiles created:")
    print(prepared_file)
    print(train_file)
    print(test_file)

    print("\nData preparation completed successfully!")


if __name__ == "__main__":
    prepare_forecasting_data()
