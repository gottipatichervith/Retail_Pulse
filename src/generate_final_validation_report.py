
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from src.config import DATABASE_FILE
from src.logger import get_logger

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "final_validation_report.md"

logger = get_logger("RetailPulseFinalValidation")


def run_tests():

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/",
            "-v",
            "--ignore=tests/test_batch.py"
        ],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    output = result.stdout + "\n" + result.stderr

    passed = 0
    failed = 0
    errors = 0

    for line in output.splitlines():
        if " passed" in line and ("failed" in line or "error" in line):
            pass

    import re

    match = re.search(
        r"(\d+) passed(?:, (\d+) failed)?(?:, (\d+) error)?",
        output
    )

    if match:
        passed = int(match.group(1))
        failed = int(match.group(2) or 0)
        errors = int(match.group(3) or 0)

    return result.returncode, passed, failed, errors


def generate_report():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        # Database counts
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM order_items")
        total_order_items = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM stores")
        total_stores = cursor.fetchone()[0]

        # Data quality
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items
            WHERE quantity < 0 OR unit_price < 0
        """)
        invalid_records = cursor.fetchone()[0]

        cursor.execute("PRAGMA foreign_key_check")
        foreign_key_violations = len(cursor.fetchall())

        # Duplicate order-item combinations
        cursor.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT order_id, product_id
                FROM order_items
                GROUP BY order_id, product_id
                HAVING COUNT(*) > 1
            )
        """)
        duplicate_items = cursor.fetchone()[0]

    finally:
        connection.close()

    # Automated tests
    test_code, passed, failed, errors = run_tests()

    test_status = "PASSED" if test_code == 0 else "FAILED"

    # Report
    report = [
        "# RetailPulse - Final System Validation Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Database:** `{DATABASE_FILE.name}`",
        "",
        "## 1. Automated Test Results",
        "",
        f"- Test status: {test_status}",
        f"- Tests passed: {passed}",
        f"- Tests failed: {failed}",
        f"- Collection/runtime errors: {errors}",
        "- Batch test excluded because its required CSV is unavailable.",
        "",
        "## 2. Database Validation",
        "",
        f"- Customers: {total_customers}",
        f"- Products: {total_products}",
        f"- Stores: {total_stores}",
        f"- Orders: {total_orders}",
        f"- Order items: {total_order_items}",
        "",
        "## 3. Data Quality Checks",
        "",
        f"- Negative quantities/prices: {invalid_records}",
        f"- Foreign-key violations: {foreign_key_violations}",
        f"- Duplicate order/product combinations: {duplicate_items}",
        "",
        "## 4. Validation Summary",
        "",
    ]

    if (
        test_code == 0
        and invalid_records == 0
        and foreign_key_violations == 0
        and duplicate_items == 0
    ):
        report.append(
            "Automated tests and the selected database checks passed."
        )
    else:
        report.append(
            "One or more checks require investigation before release."
        )

    report.extend([
        "",
        "## 5. Remaining Validation",
        "",
        "- Verify duplicate-file and late-arriving-record handling.",
        "- Verify simulated database failure and restart recovery.",
        "- Review forecast and inventory outputs.",
        "- Complete final production configuration review.",
        "- Create the release tag after all required checks are complete.",
        "",
        "This report covers the checks executed by this script. "
        "It does not claim that unexecuted production scenarios have passed.",
        ""
    ])

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    logger.info("Final validation report generated: %s", REPORT_FILE)

    print("Final validation report generated.")
    print(f"Location: {REPORT_FILE}")
    print(f"Tests passed: {passed}")
    print(f"Tests failed: {failed}")


if __name__ == "__main__":
    generate_report()
