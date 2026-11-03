# RetailPulse — Inventory Intelligence Report

## 1. Objective
Analyze inventory levels and sales demand to identify stock risks and recommend products that need replenishment.

## 2. Data Sources
- Sales data: Existing RetailPulse SQLite database
- Inventory data: data/inventory_snapshot.csv
- Inventory and supplier values are realistic sample values because actual inventory and supplier data were not available.

## 3. Assumptions
- Demand is calculated using the available sales history.
- Supplier lead time is measured in days.
- A 20% safety buffer is used for reorder recommendations.
- Inventory analysis is performed at product-store level.
- Historical sales data is not modified.

## 4. Validation Results
- Inventory records: 21
- Duplicate product-store combinations: 0
- Missing values: 0
- Negative current stock: 0
- Negative reorder quantities: 0

## 5. Reorder Recommendations

| Priority | Store | Product | Status | Suggested Reorder Quantity |
|---:|---|---|---|---:|
| 1 | ST01 | P006 | OUT OF STOCK | 10 |
| 1 | ST02 | P007 | OUT OF STOCK | 10 |
| 2 | ST01 | P005 | HIGH RISK | 6 |
| 2 | ST02 | P001 | HIGH RISK | 8 |
| 2 | ST02 | P003 | HIGH RISK | 4 |
| 2 | ST03 | P007 | HIGH RISK | 5 |
| 3 | ST01 | P001 | REORDER | 7 |
| 3 | ST01 | P003 | REORDER | 5 |
| 3 | ST02 | P004 | REORDER | 5 |
| 3 | ST02 | P005 | REORDER | 5 |
| 3 | ST02 | P006 | REORDER | 1 |
| 3 | ST03 | P002 | REORDER | 3 |
| 3 | ST03 | P004 | REORDER | 6 |

## 6. Business Insights

- 2 product-store combinations are out of stock.
- 4 product-store combinations are at high risk.
- ST02 has the highest number of risky product-store combinations.
- Out-of-stock products should be prioritized first.
- Products that may run out before supplier delivery should be monitored closely.
- Products with high stock and low demand should be reviewed before placing additional orders.

## 7. Reorder Quantity Rule

Target Stock = MAX(Reorder Level, Lead-Time Demand × 1.20)

Suggested Reorder Quantity = MAX(0, Target Stock - Current Stock)

The 20% safety buffer is a project assumption because actual business safety-stock policies were not available.
