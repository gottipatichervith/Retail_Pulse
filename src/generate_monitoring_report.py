
import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import DATABASE_FILE
from src.logger import get_logger

logger = get_logger("RetailPulseMonitoring")

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "pipeline_monitoring_report.md"


def generate_report():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        cursor = connection.cursor()

        # Latest pipeline execution
        cursor.execute("""
            SELECT
                run_id, filename, started_at, completed_at,
                status, total_records, valid_records,
                rejected_records, inserted_records,
                updated_records, skipped_records, error_message
            FROM pipeline_file_audit
            ORDER BY started_at DESC
            LIMIT 1
        """)

        latest_run = cursor.fetchone()

        # Total failed batches
        cursor.execute("""
            SELECT COUNT(*)
            FROM pipeline_batch_audit
            WHERE status = 'FAILED'
        """)

        failed_batches = cursor.fetchone()[0]

        # Total batches
        cursor.execute("""
            SELECT COUNT(*)
            FROM pipeline_batch_audit
        """)

        total_batches = cursor.fetchone()[0]

        # Negative quantities
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items
            WHERE quantity < 0
        """)

        negative_quantities = cursor.fetchone()[0]

        # Negative prices
        cursor.execute("""
            SELECT COUNT(*)
            FROM order_items
            WHERE unit_price < 0
        """)

        negative_prices = cursor.fetchone()[0]

        # Foreign-key violations
        cursor.execute("PRAGMA foreign_key_check")
        foreign_key_violations = len(cursor.fetchall())

        # Database record counts
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM order_items")
        total_order_items = cursor.fetchone()[0]

        # Build report
        report = []

        report.append("# RetailPulse Pipeline Monitoring Report")
        report.append("")
        report.append(
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report.append("")

        report.append("## 1. Latest Pipeline Execution")
        report.append("")

        if latest_run:

            (
                run_id, filename, started_at, completed_at,
                status, total_records, valid_records,
                rejected_records, inserted_records,
                updated_records, skipped_records, error_message
            ) = latest_run

            report.extend([
                f"- Run ID: {run_id}",
                f"- File: {filename}",
                f"- Started: {started_at}",
                f"- Completed: {completed_at}",
                f"- Status: {status}",
                f"- Records read: {total_records}",
                f"- Valid records: {valid_records}",
                f"- Rejected records: {rejected_records}",
                f"- Inserted records: {inserted_records}",
                f"- Updated records: {updated_records}",
                f"- Skipped records: {skipped_records}",
                f"- Error: {error_message or 'None'}"
            ])

        else:
            report.append("No pipeline execution records found.")

        report.append("")
        report.append("## 2. Batch Monitoring")
        report.append("")
        report.append(f"- Total batches recorded: {total_batches}")
        report.append(f"- Failed batches: {failed_batches}")

        report.append("")
        report.append("## 3. Data Quality Checks")
        report.append("")
        report.append(f"- Negative quantities: {negative_quantities}")
        report.append(f"- Negative unit prices: {negative_prices}")
        report.append(
            f"- Foreign-key violations: {foreign_key_violations}"
        )

        report.append("")
        report.append("## 4. Database Summary")
        report.append("")
        report.append(f"- Total orders: {total_orders}")
        report.append(f"- Total order items: {total_order_items}")

        report.append("")
        report.append("## 5. Investigation Conditions")
        report.append("")

        if latest_run and latest_run[4] != "SUCCESS":
            report.append("- WARNING: Latest pipeline run did not succeed.")

        if failed_batches > 0:
            report.append("- WARNING: Failed batches require investigation.")

        if negative_quantities > 0:
            report.append("- WARNING: Negative quantities were found.")

        if negative_prices > 0:
            report.append("- WARNING: Negative prices were found.")

        if foreign_key_violations > 0:
            report.append("- WARNING: Foreign-key violations were found.")

        if (
            latest_run
            and latest_run[4] == "SUCCESS"
            and failed_batches == 0
            and negative_quantities == 0
            and negative_prices == 0
            and foreign_key_violations == 0
        ):
            report.append(
                "- No issues were detected by these monitoring checks."
            )

        report.append("")

        REPORT_FILE.write_text(
            "\n".join(report),
            encoding="utf-8"
        )

        logger.info("Monitoring report generated: %s", REPORT_FILE)

        print("Monitoring report generated successfully.")
        print(f"Report location: {REPORT_FILE}")

    finally:
        connection.close()


if __name__ == "__main__":
    generate_report()
