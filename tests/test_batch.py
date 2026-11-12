import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.batch_processor import process_csv_in_batches

file_path = PROJECT_ROOT / "data" / "incoming" / "batch_test.csv"

for batch_number, valid_df, rejected_df in process_csv_in_batches(
    file_path,
    batch_size=2
):
    print("\nValid records:")
    print(valid_df)

    print("\nRejected records:")
    print(rejected_df)

    print("Valid count:", len(valid_df))
    print("Rejected count:", len(rejected_df))