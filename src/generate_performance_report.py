
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"

BASELINE_FILE = REPORT_DIR / "performance_baseline.txt"
OUTPUT_FILE = REPORT_DIR / "performance_benchmark.md"


def main():
    baseline = BASELINE_FILE.read_text(encoding="utf-8")

    report = f"""# RetailPulse - Performance Benchmark Report

**Date:** {datetime.now().strftime("%Y-%m-%d")}

## 1. Objective

Test RetailPulse ingestion and SQL query performance
using 100,000 synthetic sales records.

## 2. Dataset

- File: large_sales_100k.csv
- Records: 100,000
- Columns: 11
- Missing values: 0
- Batch size: 200

## 3. Ingestion Performance

{baseline}

## 4. SQL Query Performance

| Query | Before Index Testing | After Index Testing |
|---|---:|---:|
| Total sales | 0.0207 sec | 0.0248 sec |
| Sales by product | 0.0726 sec | 0.1402 sec |
| Sales by store | 0.1491 sec | 0.3058 sec |
| Monthly sales | 0.1839 sec | 0.3569 sec |

## 5. Performance Findings

- Ingestion processed the 100,000-record input successfully.
- Total sales query was the fastest.
- Monthly sales query was the slowest in both tests.
- Additional indexes were tested on product_id and store_id.
- SQLite used the additional indexes for product-wise and
  store-wise queries.
- However, measured query execution times became slower.
- The additional indexes were removed after testing.
- Original database indexes were preserved.

## 6. Identified Optimization Opportunities

- Investigate repeated database lookups during ingestion.
- Evaluate batch size changes through controlled testing.
- Review SQL JOIN and GROUP BY operations.
- Measure peak memory accurately.
- Repeat query benchmarks to reduce timing variation.

## 7. Conclusion

RetailPulse successfully processed a dataset containing
100,000 synthetic records.

The baseline ingestion time was 49.14 seconds.
Additional indexes did not improve measured SQL performance.

Further testing is required before claiming performance
optimization or production scalability.

---
Generated automatically by RetailPulse.
"""

    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print("Performance report generated successfully!")
    print(f"Report: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
