
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"

METRICS_FILE = DATA_DIR / "forecast_metrics.csv"
INVENTORY_FILE = DATA_DIR / "inventory_recommendations.csv"

FORECAST_REPORT = REPORT_DIR / "forecast_performance_report.md"
INVENTORY_REPORT = REPORT_DIR / "inventory_recommendations.md"


def generate_forecast_report():

    if not METRICS_FILE.exists():
        raise FileNotFoundError(f"Metrics file not found: {METRICS_FILE}")

    metrics = pd.read_csv(METRICS_FILE)

    required = {
        "model", "MAE", "RMSE", "MAPE_percent",
        "test_records", "zero_actual_records"
    }

    if not required.issubset(metrics.columns):
        raise ValueError("Forecast metrics file is missing required columns.")

    metrics = metrics.sort_values("MAE").reset_index(drop=True)

    best_model = metrics.iloc[0]

    # Build model comparison table
    table = [
        "| Model | MAE | RMSE | MAPE (%) | Test Records |",
        "|---|---:|---:|---:|---:|"
    ]

    for _, row in metrics.iterrows():
        mape = (
            "N/A"
            if pd.isna(row["MAPE_percent"])
            else f'{row["MAPE_percent"]:.2f}'
        )

        table.append(
            f'| {row["model"]} | {row["MAE"]:.4f} | '
            f'{row["RMSE"]:.4f} | {mape} | '
            f'{int(row["test_records"])} |'
        )

    zero_records = int(metrics["zero_actual_records"].max())
    total_records = int(metrics["test_records"].max())

    report = f"""# RetailPulse — Forecast Performance Report

## 1. Objective

The objective was to forecast daily product demand for each store and compare different forecasting methods.

## 2. Dataset Preparation

- Historical period: 2026-01-03 to 2026-02-10
- Historical duration: 39 days
- Product-store combinations: 21
- Prepared records: 819
- Zero-sales records: 752
- Total units sold: 90
- Training records: 672
- Testing records: 147
- Training period: 2026-01-03 to 2026-02-03
- Testing period: 2026-02-04 to 2026-02-10

Missing product-store dates were filled with zero sales. Data was split chronologically to avoid future data leakage.

## 3. Forecasting Models

Four forecasting methods were evaluated:

1. Historical Average
2. Naive Forecast
3. Moving Average using the last 7 training days
4. Exponential Smoothing with alpha = 0.3

Each model generated a static forecast for the seven-day test period using training data only.

## 4. Model Performance

{chr(10).join(table)}

## 5. Selected Model

The selected model was **{best_model["model"]}**, with an MAE of **{best_model["MAE"]:.4f}**.

It achieved the lowest Mean Absolute Error among the evaluated models.

## 6. Evaluation Observations

- Test records evaluated: {total_records}
- Records with zero actual demand: {zero_records}
- Moving Average achieved the lowest MAE.
- Forecast errors were influenced by intermittent demand and many zero-sales days.
- MAPE was calculated only for records with non-zero actual demand to avoid division by zero.

MAPE therefore does not represent all test records and should be interpreted carefully.

## 7. Limitations

- Only 39 days of historical data were available.
- The history is too short to establish reliable seasonal patterns.
- Sales were intermittent across several product-store combinations.
- Forecasts remained static during the seven-day test period.
- The selected model is not guaranteed to be the best model for every product and store.

## 8. Conclusion

The {best_model["model"]} model achieved the lowest MAE in this evaluation. It provides a basic forecasting baseline for RetailPulse. More historical data and further testing are needed before relying on these forecasts for major purchasing decisions.
"""

    FORECAST_REPORT.write_text(report, encoding="utf-8")
    print("Created:", FORECAST_REPORT)


def generate_inventory_report():

    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(
            f"Inventory recommendations file not found: {INVENTORY_FILE}"
        )

    inventory = pd.read_csv(INVENTORY_FILE)

    required = {
        "product_id",
        "store_id",
        "current_stock",
        "daily_forecast",
        "lead_time_days",
        "lead_time_demand",
        "safety_stock",
        "reorder_point",
        "target_stock",
        "recommended_order_quantity",
        "stockout_risk",
        "overstock_risk",
        "recommendation",
        "existing_reorder_level",
        "existing_rule"
    }

    if not required.issubset(inventory.columns):
        raise ValueError(
            "Inventory recommendations file is missing required columns."
        )

    total = len(inventory)

    reorder_count = int(
        (inventory["recommendation"] == "REORDER").sum()
    )

    critical_count = int(
        (inventory["stockout_risk"] == "CRITICAL").sum()
    )

    high_count = int(
        (inventory["stockout_risk"] == "HIGH").sum()
    )

    potential_overstock = int(
        (inventory["overstock_risk"] == "POTENTIAL").sum()
    )

    not_assessable = int(
        (inventory["overstock_risk"] == "NOT ASSESSABLE").sum()
    )

    existing_reorders = int(
        (inventory["existing_rule"] == "REORDER").sum()
    )

    critical_items = inventory[
        inventory["stockout_risk"] == "CRITICAL"
    ]

    critical_table = [
        "| Product | Store | Current Stock | Recommended Order |",
        "|---|---|---:|---:|"
    ]

    if critical_items.empty:
        critical_table.append("| None | - | - | - |")
    else:
        for _, row in critical_items.iterrows():
            critical_table.append(
                f'| {row["product_id"]} | {row["store_id"]} | '
                f'{int(row["current_stock"])} | '
                f'{int(row["recommended_order_quantity"])} |'
            )

    report = f"""# RetailPulse — Inventory Recommendations Report

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
| Product-store combinations | {total} |
| Forecast-based reorder recommendations | {reorder_count} |
| Critical stockout risks | {critical_count} |
| High stockout risks | {high_count} |
| Potential overstock cases | {potential_overstock} |
| Overstock not assessable | {not_assessable} |

## 4. Critical Stockout Risks

{chr(10).join(critical_table)}

## 5. Comparison with Existing Inventory Rules

- Existing Use Case 5 reorder rule: {existing_reorders} combinations.
- Forecast-based reorder recommendation: {reorder_count} combinations.

The difference occurs because the selected forecasting model produces small demand estimates for many combinations.

The existing reorder-level rule should remain an important reference rather than being replaced by the forecast-based calculation alone.

## 6. Business Insights

- {critical_count} product-store combinations currently have zero stock and critical stockout risk.
- Forecast-based recommendations identify {reorder_count} combinations for replenishment.
- {potential_overstock} combinations are flagged as potential overstock under the project's stock-coverage assumption.
- Overstock could not be assessed for {not_assessable} combinations because their forecast demand was zero.
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
"""

    INVENTORY_REPORT.write_text(report, encoding="utf-8")
    print("Created:", INVENTORY_REPORT)


def main():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    generate_forecast_report()
    generate_inventory_report()

    print("\nBoth forecasting reports generated successfully!")


if __name__ == "__main__":
    main()
