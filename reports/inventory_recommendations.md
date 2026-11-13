# RetailPulse — Inventory Recommendations Report

## 1. Objective

The objective was to combine forecasted demand, current stock and supplier lead time to identify reorder requirements, stockout risks and potential overstock situations.

## 2. Methodology

The selected Moving Average forecast was combined with current inventory information.

Planning assumptions:

- Safety stock: one additional day of forecast demand.
- Future coverage: seven days.
- Lead-time demand: daily forecast multiplied by supplier lead time.
- Reorder point: lead-time demand plus safety stock.
- Target stock: forecast demand for lead time, future coverage and safety-stock period.
- Recommended order quantity: target stock minus current stock, with a minimum of zero.

## 3. Inventory Results

| Result | Count |
|---|---:|
| Product-store combinations | 21 |
| Forecast-based reorder recommendations | 2 |
| Critical stockout risks | 2 |
| High stockout risks | 0 |
| Potential overstock cases | 10 |
| Overstock not assessable | 8 |

## 4. Critical Stockout Risks

| Product | Store | Current Stock | Recommended Order |
|---|---|---:|---:|
| P006 | ST01 | 0 | 2 |
| P007 | ST02 | 0 | 2 |

## 5. Comparison with Existing Inventory Rules

- Existing Use Case 5 reorder rule: 13 combinations.
- Forecast-based reorder recommendation: 2 combinations.

The difference occurs because the selected forecasting model produces small demand estimates for many combinations.

The existing reorder-level rule should remain an important reference rather than being replaced by the forecast-based calculation alone.

## 6. Business Insights

- 2 product-store combinations currently have zero stock and critical stockout risk.
- Forecast-based recommendations identify 2 combinations for replenishment.
- 10 combinations are flagged as potential overstock under the project's stock-coverage assumption.
- Overstock could not be assessed for 8 combinations because their forecast demand was zero.
- Forecast-based order quantities are preliminary and should be reviewed with existing inventory rules.

## 7. Limitations and Assumptions

- Historical sales cover only 39 days.
- Many product-store combinations have intermittent demand.
- A zero forecast does not guarantee zero future demand.
- Safety stock is based on a one-day demand assumption.
- Future coverage is assumed to be seven days.
- Supplier delays and changing demand were not simulated.
- Inventory recommendations use the available test database snapshot.

## 8. Recommendations

1. Investigate critical zero-stock combinations first.
2. Continue monitoring existing reorder levels.
3. Collect more historical sales data.
4. Re-evaluate forecasts as new sales data arrives.
5. Avoid relying on preliminary forecasts alone for major purchasing decisions.

## 9. Conclusion

The forecasting and inventory analysis demonstrates how predicted demand can support inventory planning. However, limited historical data and intermittent sales reduce forecast reliability. Combining forecast-based recommendations with existing inventory rules is a safer approach at this stage.
