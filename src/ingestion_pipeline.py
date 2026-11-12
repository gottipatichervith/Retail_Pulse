
from pathlib import Path
import sqlite3
from datetime import datetime
from uuid import uuid4

from src.batch_processor import process_csv_in_batches
from src.recovery_handler import (
    save_checkpoint,
    get_checkpoint,
    get_checkpoint_status
)


# ============================================================
# PROJECT PATHS AND SETTINGS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INCOMING_DIR = BASE_DIR / "data" / "incoming"
CLEANED_FILE = BASE_DIR / "data" / "processed" / "cleaned_sales.csv"

# Use the test database, not the original database.
DATABASE_FILE = BASE_DIR / "database" / "retailpulse_pipeline_test.db"

BATCH_SIZE = 200


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    if not DATABASE_FILE.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_FILE}"
        )

    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ============================================================
# REFERENCE DATA CHECKS
# ============================================================

def reference_exists(connection, table_name, column_name, value):

    allowed_tables = {
        "customers": "customer_id",
        "stores": "store_id",
        "products": "product_id"
    }

    if allowed_tables.get(table_name) != column_name:
        raise ValueError("Invalid reference table or column.")

    query = f"""
        SELECT 1
        FROM {table_name}
        WHERE {column_name} = ?
    """

    return connection.execute(
        query, (value,)
    ).fetchone() is not None


# ============================================================
# GET EXISTING RECORDS
# ============================================================

def get_existing_order(connection, order_id):

    return connection.execute(
        """
        SELECT order_id, order_date, customer_id, store_id, status
        FROM orders
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchone()


def get_existing_order_item(connection, order_id, product_id):

    return connection.execute(
        """
        SELECT order_id, product_id, quantity, unit_price,
               discount, gross_amount, net_amount
        FROM order_items
        WHERE order_id = ? AND product_id = ?
        """,
        (order_id, product_id)
    ).fetchone()


# ============================================================
# COMPARE RECORDS
# ============================================================

def order_is_same(existing, row):

    return (
        str(existing[1]) == str(row["order_date"])
        and str(existing[2]) == str(row["customer_id"])
        and str(existing[3]) == str(row["store_id"])
        and str(existing[4]) == str(row["status"])
    )


def order_item_is_same(existing, row):

    return (
        float(existing[2]) == float(row["quantity"])
        and float(existing[3]) == float(row["unit_price"])
        and float(existing[4]) == float(row["discount"])
        and float(existing[5]) == float(row["gross_amount"])
        and float(existing[6]) == float(row["net_amount"])
    )


# ============================================================
# INSERT OR UPDATE ORDER
# ============================================================

def save_order(connection, row, counts):

    existing = get_existing_order(
        connection, row["order_id"]
    )

    values = (
        row["order_date"],
        row["customer_id"],
        row["store_id"],
        row["status"]
    )

    connection.execute(
        """
        INSERT INTO orders (
            order_id, order_date, customer_id, store_id, status
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(order_id)
        DO UPDATE SET
            order_date = excluded.order_date,
            customer_id = excluded.customer_id,
            store_id = excluded.store_id,
            status = excluded.status
        WHERE
            orders.order_date IS NOT excluded.order_date
            OR orders.customer_id IS NOT excluded.customer_id
            OR orders.store_id IS NOT excluded.store_id
            OR orders.status IS NOT excluded.status
        """,
        (row["order_id"], *values)
    )

    if existing is None:
        counts["orders_inserted"] += 1

    elif not order_is_same(existing, row):
        counts["orders_updated"] += 1


# ============================================================
# INSERT OR UPDATE ORDER ITEM
# ============================================================

def save_order_item(connection, row, counts):

    existing = get_existing_order_item(
        connection,
        row["order_id"],
        row["product_id"]
    )

    values = (
        row["order_id"],
        row["product_id"],
        row["quantity"],
        row["unit_price"],
        row["discount"],
        row["gross_amount"],
        row["net_amount"]
    )

    connection.execute(
        """
        INSERT INTO order_items (
            order_id, product_id, quantity, unit_price,
            discount, gross_amount, net_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(order_id, product_id)
        DO UPDATE SET
            quantity = excluded.quantity,
            unit_price = excluded.unit_price,
            discount = excluded.discount,
            gross_amount = excluded.gross_amount,
            net_amount = excluded.net_amount
        WHERE
            order_items.quantity IS NOT excluded.quantity
            OR order_items.unit_price IS NOT excluded.unit_price
            OR order_items.discount IS NOT excluded.discount
            OR order_items.gross_amount IS NOT excluded.gross_amount
            OR order_items.net_amount IS NOT excluded.net_amount
        """,
        values
    )

    if existing is None:
        counts["inserted"] += 1

    elif order_item_is_same(existing, row):
        counts["skipped"] += 1

    else:
        counts["updated"] += 1


# ============================================================
# PROCESS ONE BATCH AND SAVE CHECKPOINT
# ============================================================

def process_one_batch(connection, valid_df, filename, batch_number):

    counts = {
        "orders_inserted": 0,
        "orders_updated": 0,
        "inserted": 0,
        "updated": 0,
        "skipped": 0
    }

    connection.execute("BEGIN")

    try:

        for _, row in valid_df.iterrows():

            if not reference_exists(
                connection, "customers", "customer_id",
                row["customer_id"]
            ):
                raise ValueError(
                    f"Customer does not exist: {row['customer_id']}"
                )

            if not reference_exists(
                connection, "stores", "store_id",
                row["store_id"]
            ):
                raise ValueError(
                    f"Store does not exist: {row['store_id']}"
                )

            if not reference_exists(
                connection, "products", "product_id",
                row["product_id"]
            ):
                raise ValueError(
                    f"Product does not exist: {row['product_id']}"
                )

            save_order(connection, row, counts)
            save_order_item(connection, row, counts)

        # Save checkpoint in the same transaction.
        save_checkpoint(
            connection,
            filename,
            batch_number,
            status="IN_PROGRESS"
        )

        connection.commit()

        print(f"Checkpoint saved: Batch {batch_number}")

        return counts

    except Exception:
        connection.rollback()
        raise


# ============================================================
# MARK FILE AS COMPLETED
# ============================================================

def mark_file_completed(connection, filename, last_batch):

    connection.execute("BEGIN")

    try:

        save_checkpoint(
            connection,
            filename,
            last_batch,
            status="COMPLETED"
        )

        connection.commit()

    except Exception:
        connection.rollback()
        raise


# ============================================================
# DATA LINEAGE AND AUDIT LOGGING
# ============================================================

def create_file_audit(connection, run_id, filename, started_at):
    """Create an audit record for a file-processing run."""

    connection.execute(
        """
        INSERT INTO pipeline_file_audit (
            run_id,
            filename,
            started_at,
            status
        )
        VALUES (?, ?, ?, 'IN_PROGRESS')
        """,
        (run_id, filename, started_at)
    )

    connection.commit()


def save_batch_audit(
    connection,
    run_id,
    filename,
    batch_number,
    started_at,
    completed_at,
    status,
    records_read,
    valid_records,
    rejected_records,
    inserted_records=0,
    updated_records=0,
    skipped_records=0,
    error_message=None
):
    """Save processing details for an individual batch."""

    connection.execute(
        """
        INSERT INTO pipeline_batch_audit (
            run_id,
            filename,
            batch_number,
            started_at,
            completed_at,
            status,
            records_read,
            valid_records,
            rejected_records,
            inserted_records,
            updated_records,
            skipped_records,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_id,
            filename,
            batch_number,
            started_at,
            completed_at,
            status,
            records_read,
            valid_records,
            rejected_records,
            inserted_records,
            updated_records,
            skipped_records,
            error_message
        )
    )

    connection.commit()


def finish_file_audit(connection, run_id, result):
    """Update the final result of a file-processing run."""

    connection.execute(
        """
        UPDATE pipeline_file_audit
        SET
            completed_at = ?,
            status = ?,
            total_records = ?,
            valid_records = ?,
            rejected_records = ?,
            inserted_records = ?,
            updated_records = ?,
            skipped_records = ?,
            error_message = ?
        WHERE run_id = ?
        """,
        (
            result["end_time"],
            result["status"],
            result["records_read"],
            result["valid"],
            result["rejected"],
            result["inserted"],
            result["updated"],
            result["skipped"],
            result["error"] or None,
            run_id
        )
    )

    connection.commit()


# ============================================================
# PROCESS ONE CSV FILE WITH RECOVERY AND AUDIT LOGGING
# ============================================================

def process_file_in_batches(
    file_path,
    batch_size=BATCH_SIZE,
    simulate_failure_after_batch=None
):

    file_path = Path(file_path)
    filename = file_path.name
    run_id = str(uuid4())

    if batch_size <= 0:
        raise ValueError("Batch size must be greater than zero.")

    if (
        simulate_failure_after_batch is not None
        and simulate_failure_after_batch <= 0
    ):
        raise ValueError(
            "Failure simulation batch must be greater than zero."
        )

    result = {
        "filename": filename,
        "start_time": datetime.now().isoformat(timespec="seconds"),
        "end_time": "",
        "records_read": 0,
        "valid": 0,
        "rejected": 0,
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
        "orders_inserted": 0,
        "orders_updated": 0,
        "completed_batches": 0,
        "failed_batch": None,
        "status": "FAILED",
        "error": ""
    }

    connection = None
    last_completed_batch = 0
    audit_created = False

    try:

        print("\n" + "=" * 55)
        print(f"Processing file: {filename}")
        print(f"Run ID: {run_id}")
        print(f"Batch size: {batch_size}")

        if simulate_failure_after_batch is not None:
            print(
                "Failure simulation enabled after batch: "
                f"{simulate_failure_after_batch}"
            )

        print("=" * 55)

        connection = connect_database()

        # Create file-level audit record.
        create_file_audit(
            connection,
            run_id,
            filename,
            result["start_time"]
        )

        audit_created = True

        # Check previous checkpoint.
        last_completed_batch = get_checkpoint(
            connection, filename
        )

        previous_status = get_checkpoint_status(
            connection, filename
        )

        if previous_status == "COMPLETED":

            print("File was completed previously.")
            print("Starting a fresh run from Batch 1.")

            connection.execute("BEGIN")

            try:

                save_checkpoint(
                    connection,
                    filename,
                    0,
                    status="IN_PROGRESS"
                )

                connection.commit()

            except Exception:
                connection.rollback()
                raise

            last_completed_batch = 0

        elif previous_status == "IN_PROGRESS":

            print(
                f"Previous checkpoint found: Batch "
                f"{last_completed_batch}"
            )

            print(
                f"Resuming from Batch {last_completed_batch + 1}"
            )

        else:

            print("No previous checkpoint found.")
            print("Starting from Batch 1.")

            connection.execute("BEGIN")

            try:

                save_checkpoint(
                    connection,
                    filename,
                    0,
                    status="IN_PROGRESS"
                )

                connection.commit()

            except Exception:
                connection.rollback()
                raise

        # Read and process batches.
        for batch_number, valid_df, rejected_df in (
            process_csv_in_batches(file_path, batch_size)
        ):

            # Skip previously committed batches.
            if batch_number <= last_completed_batch:

                print(
                    f"Batch {batch_number} already completed. Skipping."
                )

                continue

            print(f"\nLoading batch {batch_number}")

            batch_started_at = datetime.now().isoformat(
                timespec="seconds"
            )

            records_in_batch = len(valid_df) + len(rejected_df)

            result["records_read"] += records_in_batch
            result["valid"] += len(valid_df)
            result["rejected"] += len(rejected_df)

            try:

                # Load the batch into the database.
                batch_counts = process_one_batch(
                    connection,
                    valid_df,
                    filename,
                    batch_number
                )

                # Save successful batch audit.
                save_batch_audit(
                    connection=connection,
                    run_id=run_id,
                    filename=filename,
                    batch_number=batch_number,
                    started_at=batch_started_at,
                    completed_at=datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    status="SUCCESS",
                    records_read=records_in_batch,
                    valid_records=len(valid_df),
                    rejected_records=len(rejected_df),
                    inserted_records=batch_counts["inserted"],
                    updated_records=batch_counts["updated"],
                    skipped_records=batch_counts["skipped"]
                )

            except Exception as batch_error:

                result["failed_batch"] = batch_number

                if connection.in_transaction:
                    connection.rollback()

                # Save failed batch details.
                save_batch_audit(
                    connection=connection,
                    run_id=run_id,
                    filename=filename,
                    batch_number=batch_number,
                    started_at=batch_started_at,
                    completed_at=datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    status="FAILED",
                    records_read=records_in_batch,
                    valid_records=len(valid_df),
                    rejected_records=len(rejected_df),
                    error_message=str(batch_error)
                )

                raise

            # Update summary only after successful processing.
            for key, value in batch_counts.items():
                result[key] += value

            result["completed_batches"] += 1

            print("Batch committed successfully.")
            print(f"Valid records: {len(valid_df)}")
            print(f"Rejected records: {len(rejected_df)}")
            print(f"Inserted items: {batch_counts['inserted']}")
            print(f"Updated items: {batch_counts['updated']}")
            print(f"Skipped items: {batch_counts['skipped']}")

            # Optional failure simulation.
            if batch_number == simulate_failure_after_batch:

                result["failed_batch"] = batch_number + 1

                raise RuntimeError(
                    "SIMULATED PIPELINE FAILURE after committed "
                    f"Batch {batch_number}"
                )

        # Mark the file as completed.
        mark_file_completed(
            connection,
            filename,
            last_batch=get_checkpoint(connection, filename)
        )

        result["status"] = "SUCCESS"

        print("\nAll batches completed successfully.")

    except Exception as error:

        result["error"] = str(error)

        print(f"\nPipeline failed: {error}")

        print(
            "Any active transaction was rolled back. "
            "Previously committed batches remain saved."
        )

    finally:

        result["end_time"] = datetime.now().isoformat(
            timespec="seconds"
        )

        if connection is not None:

            # Update file-level audit record.
            if audit_created:

                try:

                    finish_file_audit(
                        connection,
                        run_id,
                        result
                    )

                except Exception as audit_error:

                    print(
                        f"Could not update file audit: {audit_error}"
                    )

            connection.close()

    # Display final summary.
    print("\n========== FILE SUMMARY ==========")
    print(f"Run ID: {run_id}")
    print(f"Records read: {result['records_read']}")
    print(f"Completed batches this run: {result['completed_batches']}")
    print(f"Inserted items: {result['inserted']}")
    print(f"Updated items: {result['updated']}")
    print(f"Skipped items: {result['skipped']}")
    print(f"Rejected records: {result['rejected']}")
    print(f"Status: {result['status']}")

    if result["error"]:
        print(f"Error: {result['error']}")

    return result


# ============================================================
# MAIN FUNCTION
# ============================================================

def main():

    INCOMING_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(INCOMING_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/incoming.")
        return

    for file_path in csv_files:
        process_file_in_batches(file_path)


if __name__ == "__main__":
    main()
