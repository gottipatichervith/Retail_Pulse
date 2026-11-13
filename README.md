# RetailPulse

RetailPulse is a retail data analysis project built using **Python, SQL, pandas, and SQLite**.

The project focuses on cleaning retail data, storing it in a database, analyzing sales, and generating inventory recommendations.

---

## Project Objectives

- Clean and validate retail sales data.
- Store cleaned data in a relational database.
- Analyze sales performance using SQL.
- Perform advanced sales analysis using SQL window functions.
- Analyze inventory and generate reorder recommendations using Python and SQL.

---

## Technologies Used

- Python
- pandas
- SQL
- SQLite
- Git & GitHub

---

## Project Structure

```text
Retail_Pulse/
├── data/
│   ├── raw/
│   ├── processed/
│   └── inventory_snapshot.csv
├── sql/
├── src/
├── reports/
├── docs/
├── database/
├── README.md
└── requirements.txt
```
---

# Use Case 1 — Retail Data Quality & Ingestion

### Objective
Clean and validate the raw retail sales data before using it for further analysis.

### Work Done
- Checked missing values and duplicate records.
- Validated product, store, status, price, quantity, and discount values.
- Separated valid and rejected records.
- Calculated gross and net sales amounts.
- Generated a data quality report.

### Main Outputs

data/processed/cleaned_sales.csv
data/processed/rejected_records.csv
reports/data_quality_report.txt

---

# Use Case 2 — Database Design & Data Loading

### Objective
Store the cleaned sales data in a structured relational database.

### Work Done
- Designed tables for customers, products, stores, orders, and order items.
- Added primary keys and foreign keys.
- Added basic data validation rules.
- Loaded cleaned sales data into SQLite.
- Validated record counts, references, duplicates, and sales totals.

### Main Outputs

database/retailpulse.db
docs/database_design.png
sql/
src/load_data.py
reports/database_validation_report.txt

---

# Use Case 3 — Sales Performance Analysis

### Objective
Analyze sales performance and identify important business results.

### Work Done
- Calculated total orders, units sold, gross sales, discounts, and net sales.
- Compared sales performance across stores.
- Analyzed product sales and units sold.
- Analyzed monthly sales.
- Answered key business questions using SQL.

### Key Result

**ST02** had the highest net sales among the three stores.

### Main Outputs

sql/sales_analysis.sql
reports/sales_performance_report.md

---

# Use Case 4 — Advanced Sales Analytics

### Objective
Use advanced SQL techniques to find deeper sales patterns.

### Work Done
- Ranked products using `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`.
- Found the top products in each store.
- Calculated running sales totals.
- Compared monthly sales using `LAG()`.
- Calculated product contribution to total sales.
- Identified products contributing to the top 80% of sales.

### Main Outputs

sql/advanced_sales_analytics.sql
reports/advanced_sales_report.md

---

# Use Case 5 — Inventory Intelligence & Reorder Recommendations

### Objective
Analyze inventory risk and recommend products that may need replenishment.

### Work Done
- Created and validated inventory data for products and stores.
- Calculated units sold and average daily demand.
- Calculated days of stock remaining.
- Classified inventory as:
  - OUT OF STOCK
  - HIGH RISK
  - REORDER
  - SUFFICIENT
- Calculated suggested reorder quantities using lead time and a 20% safety buffer.
- Generated inventory recommendations and business insights using Python.

### Key Results

- ST01 P006 and ST02 P007 were out of stock.
- ST02 had the highest inventory risk.
- Reorder quantities were calculated for products requiring replenishment.

### Main Outputs

data/inventory_snapshot.csv
sql/inventory_analysis.sql
src/inventory_recommendations.py
reports/inventory_report.md

---

# Use Case 6 — Customer Analytics & Segmentation

### Objective
Analyze customer purchasing behavior and segment customers based on their spending and purchase recency.

### Work Done
- Analyzed customer orders, units purchased, and net spending.
- Calculated first and most recent purchase dates.
- Performed RFM (Recency, Frequency, Monetary) analysis.
- Segmented customers into High Value, At Risk, Recent Low Engagement, and Low Engagement groups.
- Identified top 10 customers by net spending.
- Calculated the revenue contribution of the top 10 customers.
- Compared one-time and repeat customers.
- Identified customers who have not purchased recently.
- Validated Python segmentation results against SQL results.
- Generated a customer analytics report.

### Main Outputs

sql/customer_analysis.sql  
src/customer_segmentation.py  
reports/customer_analytics_report.md

---

# Use Case 7 — Data Anomalies & Reconciliation

### Objective
Detect data anomalies and reconcile sales data between the cleaned CSV and the SQLite database.

### Work Done
- Detected duplicate orders and duplicate order items.
- Checked customer, product, and store references.
- Validated quantities, prices, discounts, and net amounts.
- Investigated unusual high-value transactions.
- Reconciled order counts and sales totals between CSV and database.
- Investigated the difference caused by the duplicate transaction.
- Added critical reconciliation checks.
- Generated an automated data quality and reconciliation report.

### Main Outputs

sql/anomaly_detection.sql  
src/reconciliation.py  
reports/data_quality_reconciliation_report.md

### Execution

Run anomaly detection SQL queries using the RetailPulse SQLite database.
Run the reconciliation script:
python src/reconciliation.py

The script validates the cleaned sales data against the database and automatically generates:
reports/data_quality_reconciliation_report.md

# Use Case 8 — Pipeline Automation & Incremental Loading

### Objective
Automate incoming sales CSV processing and load only new or changed records into the SQLite database while preventing duplicate records.

### Work Done
- Automated reading of incoming sales CSV files.
- Validated required columns, data types, missing values, and business rules.
- Separated valid and rejected records with rejection reasons.
- Implemented incremental loading using the `order_id + product_id` business key.
- Inserted new records into the database.
- Updated existing records when values changed.
- Skipped identical existing records to prevent duplicates.
- Used database transactions for safe processing and rollback.
- Maintained an automated processing log.
- Generated an automated pipeline run report.
- Tested reprocessing to verify duplicate prevention.
- Verified pipeline results using new, updated, and existing records.

### Main Outputs

src/pipeline.py  
src/validators.py  
sql/incremental_load.sql  
logs/pipeline_log.csv  
reports/pipeline_run_report.md

---
### Execution

Place incoming sales CSV files in:

data/incoming/

Run the pipeline:
python src/pipeline.py

The pipeline validates the incoming data, performs incremental loading, and automatically generates:

logs/pipeline_log.csv
reports/pipeline_run_report.md

The pipeline handles new records using `INSERT`, changed records using `UPDATE`, and identical existing records using `SKIP` to prevent duplicate inserts.

# Use Case 9 — Testing & Performance Optimization

### Objective
Test the RetailPulse system for correctness, reliability, data consistency, and performance before production use.

### Work Done
- Created automated tests for data quality validation.
- Tested sales calculation logic.
- Tested incremental loading and duplicate prevention.
- Tested SQL and Python result consistency.
- Added performance testing for SQL queries.
- Tested query performance before and after adding an index.
- Generated automated test results and performance reports.
- Verified 20 automated tests with 20 tests passed.
- Documented test coverage and performance results.
- Documented limitations of test results and performance measurements.

### Main Outputs

tests/test_data_quality.py
tests/test_sales_analytics.py
tests/test_incremental_loading.py
tests/test_sql_python_consistency.py
tests/test_performance.py
src/generate_test_report.py
reports/test_results.md
reports/performance_report.md

---

### Execution

Run the complete test suite:

python -m pytest tests -q

Generate the automated test and performance reports:

python src/generate_test_report.py

The test suite validates data quality, sales calculations, incremental loading, SQL/Python consistency, and performance.

The pipeline automatically generates:

reports/test_results.md  
reports/performance_report.md

The performance test compares query execution before and after creating an index and records the measured improvement.

The latest performance test showed a **32.73% reduction in query execution time** for the tested dataset.

# Use Case 10 — Capstone Integration & Business Presentation

## Objective

Integrate all RetailPulse use cases into one complete and reproducible retail analytics workflow and generate business-focused insights and recommendations.

The final workflow combines data validation, database loading, sales analytics, inventory analysis, customer analytics, anomaly detection, incremental loading, testing, and business reporting.

## Complete Workflow

```text
Raw Sales Data
      ↓
Data Quality Validation
      ↓
Cleaned Sales Data
      ↓
Relational Database
      ↓
Sales Analytics
      ↓
Advanced Sales Analytics
      ↓
Inventory Intelligence
      ↓
Customer Analytics & Segmentation
      ↓
Data Anomaly & Reconciliation
      ↓
Incremental Loading
      ↓
Automated Testing & Performance Testing
      ↓
Final Business Report
      ↓
Capstone Presentation
```

## Work Done

- Integrated the complete RetailPulse workflow.
- Organized Python scripts, SQL files, tests, data, logs, and reports.
- Integrated data quality validation before database loading.
- Integrated relational database loading using SQLite.
- Added sales performance and advanced sales analytics.
- Added inventory intelligence and reorder recommendations.
- Added customer analytics and customer segmentation.
- Added data anomaly detection and source-to-database reconciliation.
- Added incremental loading for incoming sales files.
- Added duplicate prevention and safe rerun handling.
- Added automated testing for data quality and business logic.
- Added SQL and Python consistency validation.
- Added performance testing and query optimization.
- Generated a final business report with evidence-based insights.
- Created a capstone presentation for the final project demonstration.

## Business Insights

The final analysis identified several important business findings:

- P005 generated the highest net sales.
- ST02 generated the highest store-level net sales.
- February sales were significantly lower than January.
- Inventory analysis identified out-of-stock and high-risk product-store combinations.
- Customer segmentation identified high-value and at-risk customers.
- Reconciliation identified a duplicate source transaction.
- Automated testing confirmed the main project functionality.

## Business Recommendations

Based on the analysis:

- Investigate the significant decline in February sales.
- Prioritize high-performing products such as P005, P007, and P002.
- Monitor ST02 closely for both sales and inventory performance.
- Replenish out-of-stock and high-risk inventory promptly.
- Use customer segmentation for targeted retention and re-engagement.
- Continue reconciliation checks to identify duplicate or inconsistent data.
- Run automated tests before future production changes.

## Testing

The final project was tested using the automated test suite.

Latest result:

```text
20 passed
0 failed
0 skipped
```

The tests cover:

- Data quality validation
- Sales calculation logic
- Incremental loading
- Duplicate prevention
- SQL/Python consistency
- Performance testing

Run the complete test suite:

```text
python -m pytest tests -q
```

## Incremental Loading

The pipeline processes incoming CSV files and classifies records as:

- Inserted
- Updated
- Skipped
- Rejected

The business key used for order-item processing is:

```text
order_id + product_id
```

The pipeline also supports safe reruns and prevents duplicate database records.

Run the pipeline using:

```text
python src/pipeline.py
```

## Final Reports

The major reports generated during the project include:

```text
reports/sales_performance_report.md
reports/advanced_sales_analytics.md
reports/inventory_report.md
reports/customer_analytics_report.md
reports/data_quality_reconciliation_report.md
reports/pipeline_run_report.md
reports/test_results.md
reports/performance_report.md
reports/final_business_report.md
reports/capstone_presentation.md
```

## Final Project Structure

```text
Retail_Pulse/
├── data/
├── database/
├── docs/
├── logs/
├── reports/
├── sql/
├── src/
├── tests/
├── README.md
└── requirements.txt
```

## Capstone Presentation

The final presentation covers:

1. Business problem and project architecture
2. Data ingestion and data quality
3. Database design and incremental loading
4. Sales, inventory, and customer insights
5. Anomaly detection, reconciliation, and testing
6. Business recommendations and limitations

## Limitations

- The available sales history is limited.
- Customer segmentation thresholds are based on the current project dataset.
- At-risk customers are identified using recency-based signals and do not confirm actual churn.
- Inventory recommendations use project assumptions such as the 20% safety buffer.
- Performance results depend on the current dataset and execution environment.

## Conclusion

Use Case 10 brings all RetailPulse components together into a single reproducible retail analytics solution.

The project demonstrates data validation, relational database management, SQL analytics, Python automation, inventory intelligence, customer segmentation, anomaly detection, incremental processing, automated testing, and business reporting.

The final solution is designed to be understandable, reproducible, and suitable for demonstrating both technical implementation and business-oriented decision making.

## Advanced Phase — Week 1: Advanced SQL & Business Intelligence

### Objective
Performed advanced SQL analysis to generate business insights about sales growth, customer retention, customer lifetime value, and product and store performance.

### Tasks Completed

**1. Reusable KPI Layer**
- Created reusable SQL views for business KPIs.
- Calculated total net sales, order count, Average Order Value (AOV), unique customers, and repeat purchase rate.
- Analyzed KPIs by month, store, and product.

**2. Customer Cohort & Retention Analysis**
- Grouped customers based on their first purchase month.
- Calculated monthly customer retention.
- Identified customer activity and repeat purchase behaviour.

**3. Customer Lifetime Value**
- Analyzed historical customer spending and purchase frequency.
- Identified the top 10 customers.
- Divided customers into four value segments.
- Compared customer value across stores.

**4. Product & Store Performance**
- Analyzed monthly product sales and month-over-month changes.
- Identified declining product sales.
- Calculated product contribution to total revenue.
- Compared product performance across stores.

**5. Query Optimization**
- Analyzed SQL execution plans using `EXPLAIN QUERY PLAN`.
- Created indexes to improve database lookups.
- Examined index usage and query execution times.
- Documented optimization findings and measurement limitations.

### Technologies Used
- SQLite
- SQL
- Python
- SQL Views and CTEs
- Window Functions
- Database Indexing

### Deliverables
- `sql/advanced_kpi_layer.sql`
- `sql/customer_cohort_analysis.sql`
- `sql/customer_lifetime_value.sql`
- `sql/product_store_performance.sql`
- `sql/query_optimization.sql`
- `src/generate_advanced_reports.py`
- `reports/advanced_business_intelligence_report.md`
- `reports/query_performance_comparison.md`

### Key Business Insights
- Total analyzed net sales: ₹72,650.
- ST02 generated the highest store revenue.
- P005 was the highest revenue-generating product.
- No repeat purchases were observed during the analysis period.
- All seven products recorded lower sales in February than in January.

### Outcome
Completed Advanced Phase Week 1 by building reusable SQL KPI views, performing customer and product analytics, analyzing store performance, and exploring SQL query optimization.

# Advanced Phase – Week 2: Reliable Data Engineering & Pipeline Orchestration

## Overview
Developed a reliable data pipeline for RetailPulse to process sales CSV files in batches, validate records, load data into SQLite, recover from failures, and maintain audit logs.

## Technologies Used
- Python
- Pandas
- SQLite
- SQL
- Pytest

## Key Implementations
- **Batch Processing:** Processed CSV files in configurable batches.
- **Incremental Loading:** Implemented UPSERT logic to insert new records, update changed records, and skip unchanged records.
- **Failure Recovery:** Used checkpoints and database transactions to resume processing after failures.
- **Audit Logging:** Created file-level and batch-level audit tables.
- **Reconciliation:** Compared CSV records and sales totals with database records.
- **Idempotency:** Verified that rerunning the same file does not create duplicate records or change existing totals.

## Testing Results

| Metric | Result |
|---|---:|
| CSV records processed | 68 |
| Batches completed | 4 |
| Valid records | 68 |
| Rejected records | 0 |
| Inserted items on rerun | 0 |
| Updated items on rerun | 0 |
| Skipped items on rerun | 68 |
| Reconciliation mismatches | 0 |

A simulated failure after batch 2 was successfully recovered by resuming from batch 3.

## Key Files

- `src/ingestion_pipeline.py`
- `src/batch_processor.py`
- `src/recovery_handler.py`
- `src/re

## Advanced Phase – Week 3: Demand Forecasting & Inventory Decisions

### Overview
Built a demand forecasting system to predict product demand and generate inventory recommendations for RetailPulse.

### Technologies Used
- Python
- Pandas and NumPy
- Matplotlib
- Scikit-learn
- SQLite
- SQL

### Key Implementations
- Prepared daily product-store sales data.
- Created time-based training and testing datasets.
- Compared four forecasting models.
- Evaluated models using MAE, RMSE and MAPE.
- Selected Moving Average based on the lowest MAE.
- Calculated lead-time demand, safety stock and reorder quantities.
- Identified stockout and potential overstock risks.
- Compared forecast-based recommendations with existing inventory rules.
- Generated reports and visualizations automatically.

### Key Results
- Historical data: 39 days
- Product-store combinations: 21
- Forecasting models compared: 4
- Best model: Moving Average
- Best MAE: 0.1672
- Critical stockout risks: 2
- Forecast-based reorder recommendations: 2

### Main Deliverables
- `sql/forecasting_dataset.sql`
- `src/data_preparation.py`
- `src/demand_forecasting.py`
- `src/forecast_evaluation.py`
- `src/inventory_decisions.py`
- `src/generate_forecasting_reports.py`
- `src/generate_forecasting_graphs.py`
- `reports/forecast_performance_report.md`
- `reports/inventory_recommendations.md`
- `reports/graphs/`

### Conclusion
Implemented a basic demand forecasting and inventory recommendation system. The results demonstrate how forecasting can support inventory planning. More historical data is needed to improve forecast reliability.      