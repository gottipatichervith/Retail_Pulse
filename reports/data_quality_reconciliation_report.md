
# RetailPulse — Data Quality & Reconciliation Report

## 1. Overview

This report documents the data quality checks and reconciliation performed
between the cleaned sales CSV file and the RetailPulse SQLite database.

### Source Files

- Cleaned sales data: `data/processed/cleaned_sales.csv`
- Database: `database/retailpulse.db`

## 2. Reconciliation Results

| Check | CSV | Database | Difference | Result |
|---|---:|---:|---:|---|
| Order count | 68 | 67 | 1 | FAIL |
| Unique orders | 67 | 67 | 0 | PASS |
| Quantity | 92.0 | 92 | 0.0 | PASS |
| Gross sales | ₹74,800.00 | ₹74,800.00 | ₹0.00 | PASS |
| Discount | ₹1,650.00 | ₹1,650.00 | ₹0.00 | PASS |
| Net sales | ₹73,150.00 | ₹73,150.00 | ₹0.00 | PASS |

## 3. Confirmed Data Quality Issue

### Duplicate Transaction

The cleaned CSV contains 68 rows but only 67 unique order IDs.

The affected transaction is:

- Order ID: ORD1041
- Product ID: P001
- Occurrences: 2

The duplicate transaction explains the difference between the CSV row count
and the number of unique orders in the database.

### Root Cause

The duplicate transaction is already present in the cleaned CSV.

### Business Impact

The duplicate can cause transaction-level counts to be overstated if the
CSV is analyzed without duplicate detection.

### Recommended Action

- Detect exact duplicate transactions before database loading.
- Flag confirmed duplicates.
- Preserve the original source data.
- Do not silently delete records.

## 4. Reference Validation

| Validation Check | Result |
|---|---|
| Customer references | PASS |
| Store references | PASS |
| Product references | PASS |
| Quantity values | PASS |
| Unit prices | PASS |
| Discounts | PASS |
| Discount <= Gross Amount | PASS |
| Net amount calculation | PASS |
| Product price consistency | PASS |

## 5. High-Value Transaction Investigation

High-value transactions were reviewed individually.

The identified transactions were valid purchases with valid product prices,
quantities, discounts, and order information.

Therefore, they were classified as legitimate high-value transactions
rather than confirmed data-quality anomalies.

## 6. Corrective Actions

1. Add duplicate detection to the data-cleaning pipeline.
2. Flag exact duplicate transactions before database loading.
3. Preserve the original source data.
4. Continue using database constraints.
5. Run reconciliation checks after every data load.

## 7. Limitations

- The sales data covers a limited historical period.
- High-value detection uses a statistical threshold.
- Inventory movement data was not available for this reconciliation.
- The duplicate should be addressed in the cleaning pipeline.

## 8. Conclusion

Quantity, gross sales, discount, and net sales totals agree between the
cleaned CSV and database.

The only reconciliation difference is the raw row count, which is explained
by the confirmed duplicate transaction for ORD1041.

No invalid customer, product, or store references were found.
