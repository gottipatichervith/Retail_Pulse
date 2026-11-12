from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "data" / "processed" / "cleaned_sales.csv"
DATABASE_FILE = PROJECT_ROOT / "database" / "retailpulse_pipeline_test.db"

KEY_COLUMNS = ["order_id", "product_id"]

VALUE_COLUMNS = [
    "quantity",
    "unit_price",
    "discount",
    "gross_amount",
    "net_amount"
]


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(f"Database not found: {DATABASE_FILE}")

    # Read source CSV
    source_df = pd.read_csv(CSV_FILE)

    # Read destination database
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        database_df = pd.read_sql_query("""
            SELECT
                oi.order_id,
                oi.product_id,
                oi.quantity,
                oi.unit_price,
                oi.discount,
                oi.gross_amount,
                oi.net_amount
            FROM order_items oi
        """, connection)
    finally:
        connection.close()

    print("\n========== RECONCILIATION REPORT ==========")

    print("\n1. Record counts")
    print("CSV records:", len(source_df))
    print("Database records:", len(database_df))

    print("\n2. Source CSV totals")
    print(source_df[VALUE_COLUMNS].sum())

    print("\n3. Database totals")
    print(database_df[VALUE_COLUMNS].sum())

    # Check duplicate keys
    source_duplicates = source_df[
        source_df.duplicated(subset=KEY_COLUMNS, keep=False)
    ]

    database_duplicates = database_df[
        database_df.duplicated(subset=KEY_COLUMNS, keep=False)
    ]

    print("\n4. Duplicate key checks")
    print("CSV duplicate-key rows:", len(source_duplicates))
    print("Database duplicate-key rows:", len(database_duplicates))

    if not source_duplicates.empty:
        print("\nDuplicate keys in CSV:")
        print(source_duplicates[KEY_COLUMNS + VALUE_COLUMNS])

    if not database_duplicates.empty:
        print("\nDuplicate keys in database:")
        print(database_duplicates[KEY_COLUMNS + VALUE_COLUMNS])

    # Compare unique order-product keys
    source_unique = source_df.drop_duplicates(
        subset=KEY_COLUMNS,
        keep="first"
    )

    database_unique = database_df.drop_duplicates(
        subset=KEY_COLUMNS,
        keep="first"
    )

    comparison = source_unique.merge(
        database_unique,
        on=KEY_COLUMNS,
        how="outer",
        suffixes=("_csv", "_db"),
        indicator=True
    )

    print("\n5. Missing and extra records")

    missing = comparison[comparison["_merge"] == "left_only"]
    extra = comparison[comparison["_merge"] == "right_only"]

    print("Records missing from database:", len(missing))
    print("Extra records in database:", len(extra))

    if not missing.empty:
        print("\nMissing from database:")
        print(missing[KEY_COLUMNS])

    if not extra.empty:
        print("\nExtra in database:")
        print(extra[KEY_COLUMNS])

    # Compare values for matching keys
    matching = comparison[comparison["_merge"] == "both"].copy()

    mismatch_count = 0

    for column in VALUE_COLUMNS:
        csv_column = f"{column}_csv"
        db_column = f"{column}_db"

        different = (
            pd.to_numeric(matching[csv_column], errors="coerce")
            - pd.to_numeric(matching[db_column], errors="coerce")
        ).abs() > 0.001

        mismatches = matching[different]

        if not mismatches.empty:
            mismatch_count += len(mismatches)

            print(f"\nDifferences in {column}:")
            print(
                mismatches[
                    KEY_COLUMNS + [csv_column, db_column]
                ].to_string(index=False)
            )

    print("\n6. Final comparison")
    print("Matching keys:", len(matching))
    print("Value mismatch count:", mismatch_count)

    print("\n========== RECONCILIATION COMPLETED ==========")


if __name__ == "__main__":
    main()