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