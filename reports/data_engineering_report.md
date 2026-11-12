# RetailPulse — Reliable Data Engineering & Pipeline Orchestration

## 1. Project Overview

This phase focuses on building a reliable data pipeline that can process
CSV files in batches, validate records, load data into SQLite, recover
from failures, maintain audit logs, and reconcile source and database data.

Input file: `data/processed/cleaned_sales.csv`

Test database: `database/retailpulse_pipeline_test.db`

The original database was kept separate during pipeline testing.

## 2. Batch Processing

Implemented batch processing with a configurable batch size.

Features:
- Reads CSV files in smaller batches.
- Validates records before loading.
- Separates rejected records.
- Supports processing multiple CSV files.

Test results using batch size 20:

| Batch | Records |
|---|---:|
| 1 | 20 |
| 2 | 20 |
| 3 | 20 |
| 4 | 8 |
| Total | 68 |

## 3. Incremental Loading

The pipeline uses UPSERT logic to handle records.

- New records are inserted.
- Changed records are updated.
- Unchanged records are skipped.
- Unique constraints prevent duplicate order items.

## 4. Failure Handling and Recovery

A simulated failure was introduced after batch 2.

Results:
- Batches 1 and 2 were committed.
- The pipeline stopped after the simulated failure.
- The checkpoint recorded batch 2 as completed.
- On restart, completed batches were skipped.
- Processing resumed from batch 3.
- Batches 3 and 4 completed successfully.

Database transactions protect each batch from partial commits.

## 5. Audit Logging

Two audit tables were created:

- `pipeline_file_audit`
- `pipeline_batch_audit`

Successful file audit results:

| Metric | Result |
|---|---:|
| Total records | 68 |
| Valid records | 68 |
| Rejected records | 0 |
| Inserted records | 0 |
| Updated records | 0 |
| Skipped records | 68 |
| Status | SUCCESS |

All four batch audit entries also recorded SUCCESS.

## 6. Data Reconciliation

The reconciliation script compared the source CSV with the database.

Initial investigation found:
- A duplicate `ORD1041` / `P001` row in the CSV.
- An extra test order `ORD9999` / `P006` in the test database.

The extra test order was removed from the test database only.

Final reconciliation:

| Check | Result |
|---|---:|
| CSV rows | 68 |
| Database order-item rows | 67 |
| Distinct matching keys | 67 |
| Duplicate-key rows in CSV | 2 |
| Duplicate-key rows in database | 0 |
| Missing records | 0 |
| Extra records | 0 |
| Value mismatches | 0 |

The CSV duplicate was correctly accounted for because the database
stores only one row for each order-product key.

### Reconciled Totals

| Metric | CSV after duplicate adjustment | Database |
|---|---:|---:|
| Records | 67 | 67 |
| Quantity | 90 | 90 |
| Unit-price total | 61,450 | 61,450 |
| Discount | 1,650 | 1,650 |
| Gross sales | 73,800 | 73,800 |
| Net sales | 72,150 | 72,150 |

## 7. Idempotency Verification

The same CSV was processed again after successful completion.

| Metric | Result |
|---|---:|
| Records read | 68 |
| Batches completed | 4 |
| Inserted items | 0 |
| Updated items | 0 |
| Skipped items | 68 |
| Rejected records | 0 |
| Status | SUCCESS |

Database totals after rerunning:

| Metric | Value |
|---|---:|
| Quantity | 90 |
| Gross sales | 73,800 |
| Net sales | 72,150 |

The totals remained unchanged, demonstrating idempotent behavior
for the tested file.

## 8. Important Project Files

| File | Purpose |
|---|---|
| `src/ingestion_pipeline.py` | Main ingestion pipeline |
| `src/batch_processor.py` | Batch processing and validation |
| `src/recovery_handler.py` | Checkpoint and recovery handling |
| `src/reconcile_data.py` | Source-to-database reconciliation |
| `sql/incremental_upsert.sql` | Incremental SQL operations |
| `sql/pipeline_audit_schema.sql` | Audit table creation |
| `tests/test_pipeline_recovery.py` | Recovery test |
| `reports/data_engineering_report.md` | This report |

## 9. Conclusion

The RetailPulse pipeline successfully processed the cleaned sales file
in batches, recovered from a simulated failure, recorded audit information,
and reconciled source and database records.

The rerun test confirmed that the pipeline did not insert duplicate
order items or change the verified sales totals.

Testing scope:
- Used the existing 68-row cleaned sales file.
- Simulated a failure after batch 2.
- Verified recovery and a successful rerun.
- The optional 1,000-record challenge was not performed.
- The final order count was not re-queried after the last rerun.
