import os
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd

from validators import validate_sales_file


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INCOMING_DIR = BASE_DIR / "data" / "incoming"
REJECTED_DIR = BASE_DIR / "data" / "rejected"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

DATABASE_FILE = BASE_DIR / "database" / "retailpulse.db"

LOG_FILE = LOG_DIR / "pipeline_log.csv"
REPORT_FILE = REPORT_DIR / "pipeline_run_report.md"


# ============================================================
# REQUIRED DATABASE COLUMNS
# ============================================================

ORDER_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "store_id",
    "status"
]

ORDER_ITEM_COLUMNS = [
    "order_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount",
    "gross_amount",
    "net_amount"
]


# ============================================================
# CREATE REQUIRED FOLDERS
# ============================================================

def create_directories():
    """
    Create folders required by the pipeline.
    """

    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    REJECTED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# READ INCOMING CSV
# ============================================================

def read_csv_file(file_path):
    """
    Read one incoming CSV file.

    Returns:
        DataFrame
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Incoming file not found: {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            f"Incoming file is empty: {file_path.name}"
        )

    try:
        df = pd.read_csv(file_path)
    except Exception as error:
        raise ValueError(
            f"Could not read CSV file: {error}"
        )

    if df.empty:
        raise ValueError(
            f"CSV file contains no records: {file_path.name}"
        )

    return df


# ============================================================
# CONNECT TO DATABASE
# ============================================================

def connect_database():
    """
    Connect to the RetailPulse SQLite database.

    Foreign-key checking is enabled.
    """

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_FILE}"
        )

    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


# ============================================================
# CHECK CUSTOMER
# ============================================================

def customer_exists(connection, customer_id):
    """
    Check whether a customer exists in the database.
    """

    cursor = connection.execute(
        """
        SELECT 1
        FROM customers
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    return cursor.fetchone() is not None


# ============================================================
# CHECK STORE
# ============================================================

def store_exists(connection, store_id):
    """
    Check whether a store exists in the database.
    """

    cursor = connection.execute(
        """
        SELECT 1
        FROM stores
        WHERE store_id = ?
        """,
        (store_id,)
    )

    return cursor.fetchone() is not None


# ============================================================
# CHECK PRODUCT
# ============================================================

def product_exists(connection, product_id):
    """
    Check whether a product exists in the database.
    """

    cursor = connection.execute(
        """
        SELECT 1
        FROM products
        WHERE product_id = ?
        """,
        (product_id,)
    )

    return cursor.fetchone() is not None


# ============================================================
# GET EXISTING ORDER
# ============================================================

def get_existing_order(connection, order_id):
    """
    Get an existing order from the database.
    """

    cursor = connection.execute(
        """
        SELECT
            order_id,
            order_date,
            customer_id,
            store_id,
            status
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    )

    return cursor.fetchone()


# ============================================================
# GET EXISTING ORDER ITEM
# ============================================================

def get_existing_order_item(
    connection,
    order_id,
    product_id
):
    """
    Get an existing order item.

    Business key:
        order_id + product_id
    """

    cursor = connection.execute(
        """
        SELECT
            order_id,
            product_id,
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount
        FROM order_items
        WHERE order_id = ?
          AND product_id = ?
        """,
        (order_id, product_id)
    )

    return cursor.fetchone()


# ============================================================
# INSERT ORDER
# ============================================================

def insert_order(connection, row):
    """
    Insert a new order.
    """

    connection.execute(
        """
        INSERT INTO orders (
            order_id,
            order_date,
            customer_id,
            store_id,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            row["order_id"],
            row["order_date"],
            row["customer_id"],
            row["store_id"],
            row["status"]
        )
    )


# ============================================================
# UPDATE ORDER
# ============================================================

def update_order(connection, row):
    """
    Update an existing order when its values changed.
    """

    connection.execute(
        """
        UPDATE orders
        SET
            order_date = ?,
            customer_id = ?,
            store_id = ?,
            status = ?
        WHERE order_id = ?
        """,
        (
            row["order_date"],
            row["customer_id"],
            row["store_id"],
            row["status"],
            row["order_id"]
        )
    )


# ============================================================
# INSERT ORDER ITEM
# ============================================================

def insert_order_item(connection, row):
    """
    Insert a new order item.
    """

    connection.execute(
        """
        INSERT INTO order_items (
            order_id,
            product_id,
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["order_id"],
            row["product_id"],
            row["quantity"],
            row["unit_price"],
            row["discount"],
            row["gross_amount"],
            row["net_amount"]
        )
    )


# ============================================================
# UPDATE ORDER ITEM
# ============================================================

def update_order_item(connection, row):
    """
    Update an existing order item when its values changed.
    """

    connection.execute(
        """
        UPDATE order_items
        SET
            quantity = ?,
            unit_price = ?,
            discount = ?,
            gross_amount = ?,
            net_amount = ?
        WHERE order_id = ?
          AND product_id = ?
        """,
        (
            row["quantity"],
            row["unit_price"],
            row["discount"],
            row["gross_amount"],
            row["net_amount"],
            row["order_id"],
            row["product_id"]
        )
    )


# ============================================================
# COMPARE ORDER
# ============================================================

def order_is_same(existing_order, row):
    """
    Check whether an existing order is identical
    to the incoming order.
    """

    return (
        str(existing_order[1]) == str(row["order_date"])
        and str(existing_order[2]) == str(row["customer_id"])
        and str(existing_order[3]) == str(row["store_id"])
        and str(existing_order[4]) == str(row["status"])
    )


# ============================================================
# COMPARE ORDER ITEM
# ============================================================

def order_item_is_same(existing_item, row):
    """
    Check whether an existing order item is identical
    to the incoming order item.
    """

    return (
        float(existing_item[2]) == float(row["quantity"])
        and float(existing_item[3]) == float(row["unit_price"])
        and float(existing_item[4]) == float(row["discount"])
        and float(existing_item[5]) == float(row["gross_amount"])
        and float(existing_item[6]) == float(row["net_amount"])
    )


# ============================================================
# SAVE REJECTED RECORDS
# ============================================================

def save_rejected_records(
    rejected_df,
    source_file_name
):
    """
    Save rejected records into data/rejected/.
    """

    if rejected_df.empty:
        return None

    output_file = (
        REJECTED_DIR
        / f"{Path(source_file_name).stem}_rejected.csv"
    )

    rejected_df.to_csv(
        output_file,
        index=False
    )

    return output_file


# ============================================================
# PROCESS ONE FILE
# ============================================================

def process_file(file_path):
    """
    Process one incoming CSV file.

    Returns:
        Dictionary containing processing statistics.
    """

    start_time = datetime.now()

    result = {
        "filename": file_path.name,
        "start_time": start_time.isoformat(
            timespec="seconds"
        ),
        "end_time": "",
        "records_read": 0,
        "inserted": 0,
        "updated": 0,
        "rejected": 0,
        "skipped": 0,
        "status": "FAILED",
        "error_message": ""
    }

    connection = None

    try:
        print(
            f"\nProcessing file: {file_path.name}"
        )

        # ----------------------------------------------------
        # Read CSV
        # ----------------------------------------------------

        df = read_csv_file(file_path)

        result["records_read"] = len(df)

        print(
            f"Records read: {len(df)}"
        )

        # ----------------------------------------------------
        # Validate CSV
        # ----------------------------------------------------

        (
            valid_df,
            rejected_df,
            validation_summary
        ) = validate_sales_file(df)

        result["rejected"] = len(rejected_df)

        print(
            f"Valid records: {len(valid_df)}"
        )

        print(
            f"Rejected records: {len(rejected_df)}"
        )

        # ----------------------------------------------------
        # Save rejected records
        # ----------------------------------------------------

        rejected_file = save_rejected_records(
            rejected_df,
            file_path.name
        )

        if rejected_file:
            print(
                f"Rejected records saved to: {rejected_file}"
            )

        # ----------------------------------------------------
        # Connect to database
        # ----------------------------------------------------

        connection = connect_database()

        # ----------------------------------------------------
        # Start transaction
        # ----------------------------------------------------

        connection.execute("BEGIN")

        # ----------------------------------------------------
        # Process valid records
        # ----------------------------------------------------

        for _, row in valid_df.iterrows():

            # ================================================
            # Check reference data
            # ================================================

            if not customer_exists(
                connection,
                row["customer_id"]
            ):
                raise ValueError(
                    f"Customer does not exist: "
                    f"{row['customer_id']}"
                )

            if not store_exists(
                connection,
                row["store_id"]
            ):
                raise ValueError(
                    f"Store does not exist: "
                    f"{row['store_id']}"
                )

            if not product_exists(
                connection,
                row["product_id"]
            ):
                raise ValueError(
                    f"Product does not exist: "
                    f"{row['product_id']}"
                )

            # ================================================
            # Process order
            # ================================================

            existing_order = get_existing_order(
                connection,
                row["order_id"]
            )

            if existing_order is None:

                insert_order(
                    connection,
                    row
                )

            elif not order_is_same(
                existing_order,
                row
            ):

                update_order(
                    connection,
                    row
                )

            # ================================================
            # Process order item
            # ================================================

            existing_item = get_existing_order_item(
                connection,
                row["order_id"],
                row["product_id"]
            )

            if existing_item is None:

                insert_order_item(
                    connection,
                    row
                )

                result["inserted"] += 1

            elif order_item_is_same(
                existing_item,
                row
            ):

                result["skipped"] += 1

            else:

                update_order_item(
                    connection,
                    row
                )

                result["updated"] += 1

        # ----------------------------------------------------
        # Commit transaction
        # ----------------------------------------------------

        connection.commit()

        result["status"] = "SUCCESS"

        print(
            "\nTransaction committed successfully."
        )

    except Exception as error:

        # ----------------------------------------------------
        # Roll back everything if something fails
        # ----------------------------------------------------

        if connection is not None:
            connection.rollback()

        result["inserted"] = 0
        result["updated"] = 0

        result["status"] = "FAILED"
        result["error_message"] = str(error)

        print(
            f"\nPipeline failed: {error}"
        )

        print(
            "Database changes were rolled back."
        )

    finally:

        if connection is not None:
            connection.close()

        end_time = datetime.now()

        result["end_time"] = end_time.isoformat(
            timespec="seconds"
        )

    return result


# ============================================================
# WRITE PIPELINE LOG
# ============================================================

def write_pipeline_log(result):
    """
    Add one processing result to pipeline_log.csv.
    """

    columns = [
        "filename",
        "start_time",
        "end_time",
        "records_read",
        "inserted",
        "updated",
        "rejected",
        "skipped",
        "status",
        "error_message"
    ]

    new_log = pd.DataFrame(
        [result],
        columns=columns
    )

    if LOG_FILE.exists():

        new_log.to_csv(
            LOG_FILE,
            mode="a",
            header=False,
            index=False
        )

    else:

        new_log.to_csv(
            LOG_FILE,
            index=False
        )


# ============================================================
# CREATE PIPELINE REPORT
# ============================================================

def create_pipeline_report(results):
    """
    Create a Markdown report summarizing pipeline runs.
    """

    report_lines = []

    report_lines.append(
        "# RetailPulse Pipeline Run Report"
    )

    report_lines.append("")

    report_lines.append(
        f"Generated: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    report_lines.append("")

    report_lines.append(
        "## Run Summary"
    )

    report_lines.append("")

    report_lines.append(
        "| File | Read | Inserted | Updated | "
        "Rejected | Skipped | Status |"
    )

    report_lines.append(
        "|---|---:|---:|---:|---:|---:|---|"
    )

    total_read = 0
    total_inserted = 0
    total_updated = 0
    total_rejected = 0
    total_skipped = 0

    for result in results:

        report_lines.append(
            f"| {result['filename']} "
            f"| {result['records_read']} "
            f"| {result['inserted']} "
            f"| {result['updated']} "
            f"| {result['rejected']} "
            f"| {result['skipped']} "
            f"| {result['status']} |"
        )

        total_read += result["records_read"]
        total_inserted += result["inserted"]
        total_updated += result["updated"]
        total_rejected += result["rejected"]
        total_skipped += result["skipped"]

    report_lines.append("")

    report_lines.append(
        "## Totals"
    )

    report_lines.append("")

    report_lines.append(
        f"- Records read: {total_read}"
    )

    report_lines.append(
        f"- Records inserted: {total_inserted}"
    )

    report_lines.append(
        f"- Records updated: {total_updated}"
    )

    report_lines.append(
        f"- Records rejected: {total_rejected}"
    )

    report_lines.append(
        f"- Records skipped: {total_skipped}"
    )

    report_lines.append("")

    report_lines.append(
        "## Errors"
    )

    report_lines.append("")

    errors_found = False

    for result in results:

        if result["error_message"]:

            errors_found = True

            report_lines.append(
                f"- **{result['filename']}**: "
                f"{result['error_message']}"
            )

    if not errors_found:

        report_lines.append(
            "No errors were reported."
        )

    report_lines.append("")

    report_lines.append(
        "## Incremental Loading Strategy"
    )

    report_lines.append("")

    report_lines.append(
        "- Business key for order items: "
        "`order_id + product_id`."
    )

    report_lines.append(
        "- New business key: INSERT."
    )

    report_lines.append(
        "- Existing key with changed values: UPDATE."
    )

    report_lines.append(
        "- Existing key with identical values: SKIP."
    )

    report_lines.append(
        "- Database transactions are used so failed "
        "runs can be rolled back safely."
    )

    report_lines.append("")

    REPORT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )


# ============================================================
# PROCESS ALL INCOMING FILES
# ============================================================

def main():
    """
    Main pipeline entry point.
    """

    print("=" * 60)
    print("RetailPulse Incremental Loading Pipeline")
    print("=" * 60)

    create_directories()

    # --------------------------------------------------------
    # Find CSV files
    # --------------------------------------------------------

    csv_files = sorted(
        INCOMING_DIR.glob("*.csv")
    )

    if not csv_files:

        print(
            "\nNo CSV files found in:"
        )

        print(
            INCOMING_DIR
        )

        print(
            "\nAdd an incoming CSV file and run "
            "the pipeline again."
        )

        return

    results = []

    # --------------------------------------------------------
    # Process each CSV
    # --------------------------------------------------------

    for file_path in csv_files:

        result = process_file(
            file_path
        )

        results.append(result)

        write_pipeline_log(
            result
        )

    # --------------------------------------------------------
    # Create report
    # --------------------------------------------------------

    create_pipeline_report(
        results
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Pipeline processing completed.")
    print("=" * 60)

    print(
        f"\nPipeline log:"
        f"\n{LOG_FILE}"
    )

    print(
        f"\nPipeline report:"
        f"\n{REPORT_FILE}"
    )


# ============================================================
# RUN PIPELINE
# ============================================================

if __name__ == "__main__":
    main()