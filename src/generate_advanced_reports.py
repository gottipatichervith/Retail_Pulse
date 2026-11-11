
from pathlib import Path

# --------------------------------------------------
# 1. Set project folders
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_FOLDER = PROJECT_ROOT / "reports"

# Create reports folder automatically if it does not exist
REPORTS_FOLDER.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Advanced Business Intelligence Report
# --------------------------------------------------

business_report = """
# RetailPulse — Advanced Business Intelligence Report

## 1. Project Overview

The objective of this assignment was to perform advanced SQL analysis
on RetailPulse sales data and provide useful business insights.

The analysis focused on:
- Reusable business KPIs
- Customer cohort and retention analysis
- Customer lifetime value
- Product and store performance

**Tools Used:** SQLite, SQL

**Analysis Period:** January 2026 – February 2026

## 2. Dataset Overview

The analysis used the RetailPulse SQLite database and the reusable
sales view `v_bi_sales_base`.

The base view:
- Includes completed sales.
- Excludes the test order ORD9999.
- Removes exact duplicate order-item records.
- Retains the modified ORD1001 record.

| Metric | Result |
|---|---:|
| Total analyzed orders | 67 |
| Total customers | 67 |
| Total net sales | ₹72,650 |
| Products | 7 |
| Stores | 3 |

## 3. Task 1 — Reusable KPI Layer

Created reusable SQL views to calculate important business KPIs.

The KPIs include:
- Total net sales
- Total orders
- Average Order Value (AOV)
- Unique customers
- Repeat purchase rate

### Overall KPIs

| KPI | Result |
|---|---:|
| Total Net Sales | ₹72,650 |
| Total Orders | 67 |
| Average Order Value | ₹1,084.33 |
| Unique Customers | 67 |
| Repeat Purchase Rate | 0% |

### Monthly Sales

| Month | Net Sales | Orders |
|---|---:|---:|
| January 2026 | ₹55,550 | 48 |
| February 2026 | ₹17,100 | 19 |

### Store Performance

| Store | Net Sales | Orders |
|---|---:|---:|
| ST01 | ₹25,250 | 24 |
| ST02 | ₹25,700 | 21 |
| ST03 | ₹21,700 | 22 |

ST02 generated the highest net sales, while ST01 received
the highest number of orders.

### Product Performance

| Product | Net Sales |
|---|---:|
| P001 | ₹8,500 |
| P002 | ₹12,900 |
| P003 | ₹3,500 |
| P004 | ₹9,350 |
| P005 | ₹19,100 |
| P006 | ₹2,400 |
| P007 | ₹16,900 |

P005 generated the highest net sales.

## 4. Task 2 — Customer Cohort and Retention Analysis

Customers were grouped into cohorts based on the month of their
first purchase.

### Cohort Sizes

| Cohort Month | Customers |
|---|---:|
| January 2026 | 48 |
| February 2026 | 19 |

### Monthly Retention

| Cohort | Activity Month | Active Customers | Retention |
|---|---|---:|---:|
| January | January | 48 | 100% |
| January | February | 0 | 0% |
| February | February | 19 | 100% |

### Key Insights

- 48 customers made their first purchase in January.
- 19 customers made their first purchase in February.
- No January cohort customers purchased again in February.
- January month-one retention was 0%.
- Future retention for February cannot yet be measured.

The 100% retention in the first purchase month represents
the starting cohort size. It does not prove repeat loyalty.

No customers had more than one distinct order during the
analysis period.

## 5. Task 3 — Customer Lifetime Value

Historical customer spending was calculated using total net sales
per customer.

### Top 10 Customers

| Customer | Historical Spending |
|---|---:|
| C024 | ₹3,000 |
| C019 | ₹2,900 |
| C036 | ₹2,900 |
| C016 | ₹2,300 |
| C015 | ₹2,200 |
| C055 | ₹2,200 |
| C062 | ₹2,200 |
| C069 | ₹2,200 |
| C027 | ₹2,100 |
| C010 | ₹2,000 |

### Customer Value Segments

| Segment | Customers | Total Spending |
|---|---:|---:|
| High Value | 17 | ₹35,500 |
| Upper-Middle Value | 17 | ₹21,400 |
| Lower-Middle Value | 17 | ₹11,700 |
| Low Value | 16 | ₹4,050 |

Customers were divided into four spending groups using NTILE(4).

### Customer Value by Store

| Store | Customers | Net Sales | Average Customer Spending |
|---|---:|---:|---:|
| ST01 | 24 | ₹25,250 | ₹1,052.08 |
| ST02 | 21 | ₹25,700 | ₹1,223.81 |
| ST03 | 22 | ₹21,700 | ₹986.36 |

### Key Insights

- C024 had the highest historical spending at ₹3,000.
- The High Value segment contributed ₹35,500.
- ST02 had the highest average customer spending.
- All top 10 customers had only one order.

**Limitation:** This is historical customer value, not a prediction
of future spending. The short analysis period does not provide
enough information to estimate long-term lifetime value reliably.

## 6. Task 4 — Product and Store Performance

Product sales were compared across January and February 2026.

### Month-over-Month Product Sales

| Product | January Sales | February Sales | Change |
|---|---:|---:|---:|
| P001 | ₹7,500 | ₹1,000 | -86.67% |
| P002 | ₹9,300 | ₹3,600 | -61.29% |
| P003 | ₹2,750 | ₹750 | -72.73% |
| P004 | ₹6,950 | ₹2,400 | -65.47% |
| P005 | ₹14,600 | ₹4,500 | -69.18% |
| P006 | ₹1,950 | ₹450 | -76.92% |
| P007 | ₹12,500 | ₹4,400 | -64.80% |

All seven products recorded lower sales in February than in January.

### Product Contribution to Total Sales

| Product | Net Sales | Contribution |
|---|---:|---:|
| P005 | ₹19,100 | 26.29% |
| P007 | ₹16,900 | 23.26% |
| P002 | ₹12,900 | 17.76% |
| P004 | ₹9,350 | 12.87% |
| P001 | ₹8,500 | 11.70% |
| P003 | ₹3,500 | 4.82% |
| P006 | ₹2,400 | 3.30% |

P005 was the highest revenue contributor, while P006 had
the lowest contribution.

### Top Product by Store

| Store | Highest Revenue Product |
|---|---|
| ST01 | P007 |
| ST02 | P005 |
| ST03 | P002 |

Product performance differs across stores. Management can use
these results to review store-level product demand and inventory.

**Limitation:** Only two months of data are available.
The observed decline should not be treated as proof of a
long-term decline or seasonal trend.

## 7. Business Challenge — Customer Re-engagement

The challenge was to identify customers whose purchasing activity
had declined compared with their previous behaviour and prioritize
them by business value.

The analysis found:
- 67 customers were included.
- Every customer had exactly one order.
- No customer had a repeat purchase during the available period.

There is insufficient purchase history to reliably identify
a decline in individual repeat purchasing behaviour.

### Recommendations

- Monitor customer purchase activity as more data becomes available.
- Give attention to customers with high historical spending.
- Collect additional months of sales data.
- Consider targeted offers and customer feedback campaigns.

## 8. Overall Business Recommendations

1. Investigate why sales were lower in February.
2. Review the performance of P005 and P007.
3. Investigate the low sales contribution of P006.
4. Review product demand separately for each store.
5. Track repeat purchases over a longer period.
6. Use customer spending segments to support marketing decisions.

## 9. Conclusion

The Advanced Business Intelligence analysis created a reusable
KPI layer and provided insights into customer retention,
historical customer value, and product and store performance.

ST02 was the highest-revenue store, P005 was the
highest-revenue product, and no repeat purchases were observed
during the available period.

The results are based on January–February 2026 data and
should be reviewed again when additional sales data becomes available.
"""


# --------------------------------------------------
# 3. Query Performance Comparison Report
# --------------------------------------------------

performance_report = """
# RetailPulse — Query Performance Comparison Report

## 1. Objective

The objective was to examine SQL query execution plans,
identify optimization opportunities, and evaluate database indexes.

**Database:** SQLite

**Tool Used:** SQLite Terminal

## 2. Queries Selected

Five queries were selected for performance analysis:

1. Monthly sales analysis
2. Store-wise sales analysis
3. Customer spending analysis
4. Product performance analysis
5. Product performance by store

The SQLite `EXPLAIN QUERY PLAN` command was used to inspect
how the database executes these queries.

## 3. Indexes Created

| Index | Table | Indexed Columns |
|---|---|---|
| idx_orders_status_date | orders | status, order_date |
| idx_orders_customer_status | orders | customer_id, status |
| idx_orders_store_status | orders | store_id, status |
| idx_order_items_order_product | order_items | order_id, product_id |
| idx_order_items_product | order_items | product_id |

The `ANALYZE` command was also executed to update
SQLite query-planner statistics.

## 4. Query Plan Observations

| Operation | Meaning |
|---|---|
| SCAN | Reads through a table or intermediate result |
| SEARCH | Looks for matching records |
| USING INDEX | Uses an available index |
| TEMP B-TREE | Creates a temporary structure for sorting, grouping, or distinct operations |
| CO-ROUTINE | Processes an intermediate query result |

After index creation, the store-wise and customer-spending
query plans showed use of the relevant custom indexes.

Some queries continued to scan intermediate results and use
temporary B-trees because of grouping, sorting, distinct counts,
and duplicate-removal logic in the reusable sales view.

## 5. Execution Time After Indexing

The following execution times were recorded in SQLite Terminal.

| Query | Execution Time |
|---|---:|
| Monthly sales | 0.001 seconds |
| Store-wise sales | 0.013 seconds |
| Customer spending | 0.020 seconds |
| Product performance | 0.007 seconds |
| Product performance by store | 0.013 seconds |

## 6. Before-Indexing Measurement

The custom indexes were temporarily removed to measure query
performance without them.

Only the monthly sales query was measured before indexing.

| Query | Before Indexing | After Indexing |
|---|---:|---:|
| Monthly sales | 0.000 seconds | 0.001 seconds |
| Store-wise sales | Not measured | 0.013 seconds |
| Customer spending | Not measured | 0.020 seconds |
| Product performance | Not measured | 0.007 seconds |
| Product performance by store | Not measured | 0.013 seconds |

A complete before-and-after comparison was not performed
for all five queries.

No overall performance improvement percentage is claimed.

## 7. Optimization Findings

- Indexes were created on frequently used filtering and joining columns.
- SQLite used the store and customer indexes in relevant query plans.
- Some operations still required scans and temporary structures.
- Window functions and duplicate-removal logic add processing work.
- Indexes do not guarantee faster execution for every query.

## 8. Limitations

1. The database contains a relatively small amount of sales data.
2. Execution times were very small and may be affected by timer resolution.
3. All five queries were not measured both before and after indexing.
4. Query execution time can vary depending on database state and system load.

For a more reliable comparison, all five queries should be executed
multiple times under identical conditions on a larger dataset.

## 9. Conclusion

The optimization task demonstrated how SQLite indexes and
EXPLAIN QUERY PLAN can be used to inspect database query execution.

The query plans confirmed that SQLite used some of the created indexes.
However, the available measurements are insufficient to claim
a general performance improvement.

The exercise provided practical experience in understanding
query plans, creating indexes, and evaluating SQL performance.
"""


# --------------------------------------------------
# 4. Generate both report files
# --------------------------------------------------

business_report_path = (
    REPORTS_FOLDER / "advanced_business_intelligence_report.md"
)

performance_report_path = (
    REPORTS_FOLDER / "query_performance_comparison.md"
)

business_report_path.write_text(
    business_report.strip() + "\n",
    encoding="utf-8"
)

performance_report_path.write_text(
    performance_report.strip() + "\n",
    encoding="utf-8"
)


# --------------------------------------------------
# 5. Display completion message
# --------------------------------------------------

print("\nAdvanced Phase reports generated successfully!")

print(f"\n1. {business_report_path}")
print(f"2. {performance_report_path}")

print("\nBoth report files are saved in the reports folder.")
