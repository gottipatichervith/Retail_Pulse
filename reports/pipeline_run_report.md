# RetailPulse Pipeline Run Report

Generated: 2026-10-28 16:06:38

## Run Summary

| File | Read | Inserted | Updated | Rejected | Skipped | Status |
|---|---:|---:|---:|---:|---:|---|
| first_test_file.csv | 68 | 0 | 1 | 0 | 67 | SUCCESS |
| second_test_file.csv | 69 | 0 | 1 | 0 | 68 | SUCCESS |

## Totals

- Records read: 137
- Records inserted: 0
- Records updated: 2
- Records rejected: 0
- Records skipped: 135

## Errors

No errors were reported.

## Incremental Loading Strategy

- Business key for order items: `order_id + product_id`.
- New business key: INSERT.
- Existing key with changed values: UPDATE.
- Existing key with identical values: SKIP.
- Database transactions are used so failed runs can be rolled back safely.
