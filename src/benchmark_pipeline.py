
import time
import psutil
from pathlib import Path

from src.ingestion_pipeline import (
    process_file_in_batches,
    connect_database,
    INCOMING_DIR,
    BATCH_SIZE,
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = INCOMING_DIR / "large_sales_100k.csv"
REPORT_FILE = REPORT_DIR / "performance_baseline.txt"


def main():
    process = psutil.Process()

    if not CSV_FILE.exists():
        print(f"CSV file not found: {CSV_FILE}")
        return

    print("=" * 55)
    print("RETAILPULSE - PERFORMANCE BENCHMARK")
    print("=" * 55)

    # Measure starting memory
    memory_before = process.memory_info().rss / (1024 * 1024)

    # Start timer
    start_time = time.perf_counter()

    # Run the existing ingestion pipeline
    process_file_in_batches(CSV_FILE)

    # Stop timer
    end_time = time.perf_counter()

    # Measure ending memory
    memory_after = process.memory_info().rss / (1024 * 1024)

    execution_time = end_time - start_time

    # Check database record counts
    connection = connect_database()

    order_count = connection.execute(
        "SELECT COUNT(*) FROM orders"
    ).fetchone()[0]

    item_count = connection.execute(
        "SELECT COUNT(*) FROM order_items"
    ).fetchone()[0]

    connection.close()

    # Prepare results
    report = f"""
=======================================================
RETAILPULSE - PERFORMANCE BASELINE REPORT
=======================================================

Input file: {CSV_FILE.name}
Expected CSV records: 100000
Batch size: {BATCH_SIZE}

Execution time: {execution_time:.2f} seconds
Memory before: {memory_before:.2f} MB
Memory after: {memory_after:.2f} MB
Memory difference: {memory_after - memory_before:.2f} MB

Database totals after processing:
Orders: {order_count}
Order items: {item_count}

=======================================================
"""

    print(report)

    REPORT_FILE.write_text(report, encoding="utf-8")

    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
