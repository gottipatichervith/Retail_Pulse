# RetailPulse — Final Business Report

## 1. Executive Summary

RetailPulse is a retail analytics and data pipeline project that processes sales data, validates data quality, stores data in a relational database, performs business analytics, supports incremental loading, and validates the solution through automated testing.

The final analysis covers **67 orders**, **92 units**, gross sales of **₹74,800**, discounts of **₹1,650**, and net sales of **₹73,150**.

The main business findings are:

- P005 generated the highest net sales at ₹19,100.
- ST02 generated the highest store-level net sales at ₹25,700.
- February sales decreased significantly compared with January, with a decline of approximately 69.49%.
- Inventory analysis identified 3 out-of-stock product-store combinations and 5 high-risk combinations.
- Customer analysis identified high-value and at-risk customer segments for targeted actions.
- Reconciliation identified a duplicate source transaction involving ORD1041 and P001.

## 2. Complete RetailPulse Workflow

The project follows this workflow:

Raw Sales Data → Data Quality Validation → Cleaned Sales Data → Relational Database → Sales Analytics → Inventory Analysis → Customer Analytics → Anomaly Detection → Incremental Loading → Automated Testing → Final Business Report

The project separates source data, processed data, SQL logic, Python modules, tests, logs, and reports.

## 3. Data Quality & Ingestion

Use Case 1 validates incoming retail sales data before database processing.

The validation process checks missing values, duplicates, invalid quantities, invalid prices, discounts, references, statuses, and dates.

Invalid records are separated from the cleaned dataset and recorded with rejection reasons.

## 4. Database Design & Loading

The RetailPulse database uses a relational design with separate Customers, Products, Stores, Orders, and Order Items tables.

Primary keys and foreign keys maintain relationships between the entities.

The cleaned sales data is loaded into the database using Python rather than manually inserting individual records.

## 5. Incremental Loading

Use Case 8 adds incremental loading for incoming CSV files.

The pipeline uses the combination of order ID and product ID as the business key for order-item processing.

Incoming records are classified as inserted, updated, skipped, or rejected.

Database transactions are used so that failed processing can be rolled back safely.

The pipeline also records processing information in the pipeline log and generates a pipeline run report.

## 6. Sales Performance

| Metric | Value |
|---|---:|
| Orders | 67 |
| Units | 92 |
| Gross Sales | ₹74,800 |
| Discount | ₹1,650 |
| Net Sales | ₹73,150 |
| Average Order Value | ₹1,091.79 |

### Store Performance

| Store | Net Sales |
|---|---:|
| ST01 | ₹24,750 |
| ST02 | ₹25,700 |
| ST03 | ₹22,700 |

ST02 is the highest-performing store by net sales.

### Product Performance

| Product | Net Sales |
|---|---:|
| P005 | ₹19,100 |
| P007 | ₹16,900 |
| P002 | ₹12,900 |

P005 is the highest-revenue product, followed by P007 and P002.

### Monthly Performance

| Month | Net Sales |
|---|---:|
| January | ₹56,050 |
| February | ₹17,100 |

Sales decreased by approximately 69.49% from January to February.

Business action: investigate the February sales decline and identify whether it was caused by demand, inventory, store performance, or other operational factors.

## 7. Inventory Intelligence

The inventory analysis identified **3 out-of-stock** product-store combinations and **5 high-risk** combinations.

The inventory recommendation process considers historical demand, lead time, reorder levels, current stock, and a 20% safety buffer assumption.

The inventory report identified ST01 P006 and ST02 P007 as out-of-stock combinations.

ST02 requires particular attention because multiple products were identified as requiring replenishment.

Business actions:

1. Prioritize out-of-stock products.
2. Monitor high-risk products before they run out.
3. Pay particular attention to ST02 inventory.
4. Consider supplier lead time when planning replenishment.

## 8. Customer Analytics

| Segment | Customers | Revenue |
|---|---:|---:|
| High Value | 66 | ₹48,100 |
| At Risk | 66 | ₹17,400 |

The analysis identified 66 one-time buyers.

The top 10 customers generated **₹24,000**, representing approximately **32.81%** of eligible net sales.

Business action: focus retention and re-engagement campaigns on high-value and at-risk customers.

## 9. Data Quality & Reconciliation

The reconciliation compared the cleaned source data with the database. The source contained 68 order records while the database contained 2 unique orders.

A duplicate source transaction was identified for **ORD1041 / P001**.

The reconciliation checks confirmed that important business measures such as quantity, gross sales, discount, and net sales were consistent between the source and database.

Business impact: duplicate source transactions can affect record counts and should be detected and investigated rather than silently removed.

## 10. Testing & Performance

Automated test execution status: **PASSED**.

Tests passed: **20**
Tests failed: **0**
Tests skipped: **0**

The test suite covers data quality, sales calculations, incremental loading, SQL/Python consistency, and performance.

The performance test recorded approximately **32.73%** improvement after indexing for the tested query and dataset.

Performance measurements are dataset-dependent and should not be interpreted as a guaranteed production improvement.

## 11. Business Recommendations

1. Investigate the significant decline in February sales.
2. Prioritize P005, P007, and P002 because they contribute strongly to net sales.
3. Monitor ST02 performance and inventory closely.
4. Replenish out-of-stock and high-risk inventory promptly.
5. Use customer segmentation to target high-value and at-risk customers.
6. Continue reconciliation checks to detect duplicate or inconsistent source records.
7. Continue automated testing before production releases.

## 12. Limitations

- The available sales history is limited.
- Customer segmentation thresholds are based on the current project dataset.
- At-risk customers are a recency-based signal and do not confirm actual customer churn.
- Inventory recommendations use project assumptions such as the 20% safety buffer.
- Performance results depend on the current dataset and execution environment.

## 13. Conclusion

The RetailPulse project integrates data validation, relational database loading, sales analytics, inventory intelligence, customer analytics, anomaly detection, incremental loading, and automated testing into a reproducible retail analytics workflow.

The solution provides both technical validation and business-focused insights that can support sales, inventory, and customer-management decisions.

The project is designed so that future incoming data can be processed through the same validation, loading, analysis, reconciliation, and reporting workflow.

## 14. Source Reports

This final report was generated using the following RetailPulse reports:

- `sales_performance_report.md`
- `advanced_sales_analytics.md`
- `inventory_report.md`
- `customer_analytics_report.md`
- `data_quality_reconciliation_report.md`
- `pipeline_run_report.md`
- `performance_report.md`
- `test_results.md`

---

Generated automatically by `src/generate_final_business_report.py`.
