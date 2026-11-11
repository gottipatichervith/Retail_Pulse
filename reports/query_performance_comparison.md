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
