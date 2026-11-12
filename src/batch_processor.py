
from pathlib import Path
import pandas as pd

from src.validators import validate_sales_file


BATCH_SIZE = 200

# Project folders
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"


def process_csv_in_batches(file_path, batch_size=BATCH_SIZE):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.stat().st_size == 0:
        raise ValueError("CSV file is empty.")

    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")

    # Create rejected folder if it does not exist
    REJECTED_DIR.mkdir(parents=True, exist_ok=True)

    # Create a separate rejected file for this input CSV
    rejected_file = REJECTED_DIR / f"{file_path.stem}_rejected.csv"

    # Remove the previous test output so rerunning does not append
    # the same rejected records again
    if rejected_file.exists():
        rejected_file.unlink()

    batch_number = 0

    for batch_number, batch_df in enumerate(
        pd.read_csv(file_path, chunksize=batch_size),
        start=1
    ):
        print(f"\nProcessing Batch {batch_number}")

        # Validate current batch
        valid_df, rejected_df, summary = validate_sales_file(batch_df)

        print("Records read:", summary["records_read"])
        print("Valid records:", summary["valid_records"])
        print("Rejected records:", summary["rejected_records"])
        print("Exact duplicate rows:", summary["exact_duplicate_rows"])

        # Save rejected records
        if not rejected_df.empty:

            if rejected_file.exists():
                rejected_df.to_csv(
                    rejected_file,
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                rejected_df.to_csv(
                    rejected_file,
                    index=False
                )

            print("Rejected records saved:", rejected_file)

        yield batch_number, valid_df, rejected_df

    if batch_number == 0:
        raise ValueError("CSV contains no records.")


def process_multiple_csv_files(
    input_directory,
    batch_size=BATCH_SIZE
):

    input_directory = Path(input_directory)

    if not input_directory.exists():
        raise FileNotFoundError(
            f"Directory not found: {input_directory}"
        )

    csv_files = sorted(input_directory.glob("*.csv"))

    if not csv_files:
        print("No CSV files found.")
        return

    for file_path in csv_files:

        print("\n" + "=" * 50)
        print("Processing file:", file_path.name)
        print("=" * 50)

        for batch_number, valid_df, rejected_df in (
            process_csv_in_batches(file_path, batch_size)
        ):
            print("Batch completed:", batch_number)
            print("Valid records:", len(valid_df))
            print("Rejected records:", len(rejected_df))

    print("\nAll CSV files processed.")
