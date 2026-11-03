# RetailPulse — Capstone Integration & Business Presentation

## 1. Project Overview

### Project Name
**RetailPulse — Retail Sales Analytics & Intelligence System**

### Project Objective

RetailPulse is a retail data analytics project designed to transform raw sales data into useful business insights.

The project covers the complete flow:

**Raw Data → Data Cleaning → Database → Analytics → Inventory Intelligence → Customer Analytics → Reconciliation → Incremental Loading → Testing → Business Insights**

The main goal is to help a retail business understand:

- Sales performance
- Product performance
- Store performance
- Inventory risks
- Customer behavior
- Data-quality problems
- Business opportunities

---

# 2. Business Problem

Retail businesses generate sales data from different transactions.

However, raw data may contain:

- Missing values
- Invalid values
- Duplicate records
- Incorrect references
- Changing sales records
- Inventory risks
- Customers who may need re-engagement

If this data is not properly cleaned and validated, business reports can become unreliable.

RetailPulse addresses this problem by creating a structured and validated data pipeline.

---

# 3. End-to-End Architecture

```text
Raw Sales CSV
      |
      v
Use Case 1
Data Cleaning & Validation
      |
      v
Cleaned Sales CSV
      |
      v
Use Case 2
Relational Database
      |
      v
+-----------------------------+
|                             |
v                             v
Sales Analytics          Incremental Loading
|                             |
v                             v
Advanced Analytics       New / Updated Records
|                             |
+-------------+---------------+
              |
              v
      Business Analysis
              |
      +-------+-------+
      |       |       |
      v       v       v
 Inventory  Customer  Reconciliation
 Analytics  Analytics
      |       |       |
      +-------+-------+
              |
              v
       Testing & Validation
              |
              v
       Final Business Report
              |
              v
       Business Recommendations
```

---

# 4. Use Case 1 — Data Cleaning & Validation

The first stage was to clean and validate the raw sales data.

### Main tasks

- Checked missing values
- Checked duplicate records
- Validated quantities
- Validated prices
- Validated discounts
- Validated stores
- Validated products
- Validated order status
- Validated order dates
- Separated valid and rejected records

The cleaned data was then stored in:

```text
data/processed/cleaned_sales.csv
```

Rejected records were stored separately so that invalid data was not silently removed.

### Why this is important

Cleaning the data before loading it into the database helps prevent incorrect information from affecting later analysis.

---

# 5. Use Case 2 — Database Design

Instead of keeping all information in one large table, the project uses a relational database.

### Main tables

- Customers
- Products
- Stores
- Orders
- Order Items

### Relationships

```text
Customer
   |
   | 1-to-many
   v
Orders
   |
   | 1-to-many
   v
Order Items
   |
   | many-to-1
   v
Products

Stores
   |
   | 1-to-many
   v
Orders
```

Primary keys and foreign keys were used to maintain relationships between the tables.

Database constraints were also used to improve data integrity.

---

# 6. Incremental Loading

The project also supports incremental loading.

Instead of loading the same sales data again every time, the pipeline checks whether a record already exists.

The business key used is:

```text
order_id + product_id
```

The pipeline handles records in three ways:

### New record

```text
INSERT
```

### Existing record with changed values

```text
UPDATE
```

### Existing record with no changes

```text
SKIP
```

This prevents duplicate records during repeated pipeline runs.

The pipeline also uses database transactions so that errors can trigger a rollback.

---

# 7. Sales Performance

The final sales analysis produced the following overall results:

| Metric | Result |
|---|---:|
| Orders | 67 |
| Units Sold | 92 |
| Gross Sales | ₹74,800 |
| Discount | ₹1,650 |
| Net Sales | ₹73,150 |
| Average Order Value | ₹1,091.79 |

The overall net sales were:

**₹73,150**

---

# 8. Store Performance

The three stores generated the following net sales:

| Store | Net Sales |
|---|---:|
| ST02 | ₹25,700 |
| ST01 | ₹24,750 |
| ST03 | ₹22,700 |

### Key Insight

**ST02 generated the highest net sales at ₹25,700.**

ST02 also had the highest average order value among the three stores.

This suggests that ST02 is currently the strongest-performing store based on the available dataset.

---

# 9. Product Performance

The highest-performing products by net sales were:

| Product | Net Sales |
|---|---:|
| P005 | ₹19,100 |
| P007 | ₹16,900 |
| P002 | ₹12,900 |
| P004 | ₹9,350 |
| P001 | ₹9,000 |

### Key Insight

**P005 was the highest-selling product by net sales with ₹19,100.**

The top four products contributed approximately **79.62%** of total net sales.

This shows that sales are concentrated among a small number of products.

### Business Action

The business should:

- Maintain sufficient stock for high-performing products.
- Monitor demand for P005, P007, P002 and P004.
- Avoid stockouts for these important products.

---

# 10. Monthly Sales Trend

Sales were divided into January and February.

| Month | Orders | Units | Net Sales |
|---|---:|---:|---:|
| January | 48 | 73 | ₹56,050 |
| February | 19 | 19 | ₹17,100 |

Net sales decreased by:

**₹38,950**

This represents a:

**69.49% decrease**

from January to February.

### Business Insight

The available data shows a significant decrease in sales activity in February.

However, this should not immediately be treated as a long-term business trend because the dataset covers only a limited historical period.

---

# 11. Inventory Intelligence

The inventory analysis examined product-stock levels at store level.

The analysis contained:

- 21 product-store records
- 0 duplicate product-store combinations
- 0 missing values
- 0 negative stock values
- 0 negative reorder quantities

### Critical Inventory Risks

There were:

**2 products out of stock**

and

**4 products at high risk.**

### Out-of-stock products

| Store | Product | Recommendation |
|---|---|---:|
| ST01 | P006 | Reorder 10 |
| ST02 | P007 | Reorder 10 |

### High-risk products

| Store | Product | Recommendation |
|---|---|---:|
| ST01 | P005 | Reorder 6 |
| ST02 | P001 | Reorder 8 |
| ST02 | P003 | Reorder 4 |
| ST03 | P007 | Reorder 5 |

### Business Action

The immediate priority should be:

1. Replenish out-of-stock products.
2. Monitor high-risk products.
3. Pay particular attention to ST02 because it contains multiple inventory risks.
4. Consider lead time when planning replenishment.

---

# 12. Customer Analytics

Customer segmentation was performed using RFM-style analysis.

The segments were:

- High Value
- At Risk
- Recent Low Engagement
- Low Engagement

### Segment Summary

| Segment | Customers | Revenue |
|---|---:|---:|
| High Value | 31 | ₹48,100 |
| At Risk | 13 | ₹17,400 |
| Recent Low Engagement | 18 | ₹5,500 |
| Low Engagement | 5 | ₹2,150 |

### Key Insight

The **High Value** segment generated the largest revenue at:

**₹48,100**

There were also:

**13 At Risk customers**

with ₹17,400 in revenue.

### Business Action

The business can:

- Reward high-value customers.
- Send targeted offers to at-risk customers.
- Use personalized campaigns for customer re-engagement.
- Monitor customers who have not purchased recently.

---

# 13. Customer Concentration

The top 10 customers generated approximately:

**₹24,000**

This represented:

**32.81%**

of eligible net sales of ₹73,150.

This means a relatively small group of customers contributes a significant portion of revenue.

### Business Action

These customers should receive appropriate retention and loyalty strategies because losing high-value customers could have a noticeable revenue impact.

---

# 14. Data Quality & Reconciliation

The reconciliation process compared the cleaned CSV against the database.

### Results

| Metric | CSV | Database | Result |
|---|---:|---:|---|
| Order count | 68 | 67 | Difference |
| Unique orders | 67 | 67 | PASS |
| Quantity | 92 | 92 | PASS |
| Gross Sales | ₹74,800 | ₹74,800 | PASS |
| Discount | ₹1,650 | ₹1,650 | PASS |
| Net Sales | ₹73,150 | ₹73,150 | PASS |

### Important Finding

The order-count difference was caused by a confirmed duplicate record:

```text
ORD1041 + P001
```

This record appeared twice in the cleaned CSV.

The important point is that the duplicate was identified rather than silently ignored.

### Business Impact

If duplicate records are not detected, transaction counts and business reporting can become misleading.

---

# 15. Testing

The project includes an automated testing suite.

The final test result was:

```text
20 passed
0 failed
0 skipped
```

### Tested Areas

- Data quality validation
- Sales calculations
- Incremental loading
- Duplicate prevention
- SQL/Python consistency
- Performance

The tests help confirm that the main project components work together correctly.

---

# 16. Performance Testing

The project also compared query performance before and after adding an index.

Measured result:

```text
Before index: 0.001167 seconds
After index:  0.000785 seconds
Improvement:  32.73%
```

The result shows faster execution for the tested query and dataset.

### Limitation

This was a test on the project dataset and should not be treated as a guaranteed production performance improvement.

---

# 17. Important Business Insights

The major findings from RetailPulse are:

### 1. ST02 is the strongest store

ST02 generated the highest net sales:

**₹25,700**

### 2. P005 is the strongest product

P005 generated:

**₹19,100**

in net sales.

### 3. Sales dropped significantly in February

Net sales decreased by:

**69.49%**

compared with January.

### 4. Inventory requires immediate attention

There are:

- 2 out-of-stock products
- 4 high-risk products

### 5. High-value customers are important

31 high-value customers generated:

**₹48,100**

### 6. Data quality requires monitoring

A duplicate transaction was identified for:

**ORD1041 + P001**

### 7. Automated testing improves reliability

All 20 automated tests passed.

---

# 18. Business Recommendations

Based on the analysis, I recommend:

### Recommendation 1 — Prioritize inventory replenishment

Immediately replenish the two out-of-stock products and monitor high-risk products.

### Recommendation 2 — Protect high-performing products

Maintain adequate stock for products such as P005, P007 and P002 because they contribute significantly to sales.

### Recommendation 3 — Investigate February's sales decline

The 69.49% decrease in February should be investigated further.

Possible areas for investigation include:

- Customer activity
- Product availability
- Promotions
- Store performance
- Sales volume

### Recommendation 4 — Focus on customer retention

Create targeted campaigns for:

- High-value customers
- At-risk customers
- Recently inactive customers

### Recommendation 5 — Strengthen duplicate detection

Continue detecting duplicate business keys before loading records into the database.

### Recommendation 6 — Continue automated testing

Run the automated test suite whenever important project code is changed.

---

# 19. Assumptions & Limitations

The project has several limitations.

### Limited historical data

The dataset covers a limited period, so long-term trends cannot be confirmed.

### Customer history limitation

The available customer data does not provide enough historical purchase activity to confidently measure repeat purchasing behavior.

### At-risk customers

The At Risk segment is based on recency and spending rules.

It is a signal for potential churn, not confirmed customer churn.

### Inventory assumptions

Inventory recommendations use project assumptions such as:

- Historical demand
- Lead time
- 20% safety buffer

These assumptions may need to be adjusted using real business data.

### Performance measurement

The performance improvement was measured using the project dataset and one test execution.

Production performance may be different.

---

# 20. Project Reproducibility

The project can be executed using the documented project structure.

Important commands include:

```bash
pip install -r requirements.txt
```

Run data cleaning:

```bash
python src/clean_sales.py
```

Run database setup/loading:

```bash
python src/database.py
python src/load_reference_data.py
python src/load_data.py
```

Run inventory analysis:

```bash
python src/inventory_recommendations.py
```

Run customer analysis:

```bash
python src/customer_segmentation.py
```

Run reconciliation:

```bash
python src/reconciliation.py
```

Run incremental pipeline:

```bash
python src/pipeline.py
```

Run tests:

```bash
python -m pytest tests -q
```

The final test suite produced:

```text
20 passed
```

---

# 21. Final Project Outcome

RetailPulse successfully integrates:

```text
Data Quality
      +
Database Management
      +
Sales Analytics
      +
Inventory Intelligence
      +
Customer Analytics
      +
Data Reconciliation
      +
Incremental Loading
      +
Automated Testing
      =
Business Intelligence Solution
```

The project demonstrates how raw retail data can be transformed into reliable information that supports business decisions.

---

# 22. Final Conclusion

RetailPulse provides an end-to-end retail analytics workflow that starts with raw sales data and ends with business recommendations.

The project successfully identifies important business areas such as:

- Best-performing stores
- Best-performing products
- Sales trends
- Inventory risks
- High-value and at-risk customers
- Data-quality issues

The system also includes validation, database constraints, incremental loading, reconciliation, automated testing, and performance measurement.

The most important business priorities identified are:

1. Replenish out-of-stock inventory.
2. Monitor high-risk products.
3. Protect high-value customers.
4. Investigate the February sales decline.
5. Continue monitoring data quality and duplicate transactions.

Overall, the project demonstrates how data engineering, SQL, Python, and analytics can work together to support retail business decisions.

---

# 23. Presentation Flow — 10 to 15 Minutes

### Slide 1 — Introduction
**RetailPulse: Retail Sales Analytics & Intelligence**

Briefly introduce the project and its objective.

### Slide 2 — Business Problem
Explain why raw retail data needs cleaning, validation, storage, and analysis.

### Slide 3 — Architecture
Show:

```text
Raw Data
→ Cleaning
→ Database
→ Analytics
→ Inventory
→ Customers
→ Reconciliation
→ Testing
→ Business Insights
```

### Slide 4 — Data Quality
Explain validation, rejected records, and duplicate detection.

### Slide 5 — Database
Explain Customers, Products, Stores, Orders and Order Items.

### Slide 6 — Incremental Loading
Explain:

```text
New → INSERT
Changed → UPDATE
Same → SKIP
```

### Slide 7 — Sales Insights
Mention:

- ₹73,150 net sales
- ST02 highest store
- P005 highest product
- 69.49% February decline

### Slide 8 — Inventory
Mention:

- 2 out-of-stock products
- 4 high-risk products
- ST02 requires attention

### Slide 9 — Customer Analytics
Mention:

- 31 high-value customers
- ₹48,100 high-value revenue
- 13 at-risk customers

### Slide 10 — Reconciliation & Testing
Mention:

- Duplicate ORD1041 + P001
- 20 tests passed
- SQL/Python consistency checks

### Slide 11 — Recommendations
Present the main business actions.

### Slide 12 — Conclusion
Explain how RetailPulse converts raw retail data into reliable business insights.

---

# 24. Final Statement for Presentation

> "RetailPulse helped me build an end-to-end retail analytics solution starting from data cleaning and validation, followed by relational database design, sales and customer analysis, inventory intelligence, reconciliation, incremental loading, and automated testing. The final system not only produces business insights but also focuses on data reliability and reproducibility."