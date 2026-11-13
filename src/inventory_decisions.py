
from pathlib import Path
import sqlite3
import math
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_FILE = PROJECT_ROOT / "database" / "retailpulse_pipeline_test.db"
FORECAST_FILE = PROJECT_ROOT / "data" / "processed" / "demand_forecasts.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "inventory_recommendations.csv"

SELECTED_MODEL = "moving_average"
SAFETY_STOCK_DAYS = 1
FUTURE_COVERAGE_DAYS = 7


def generate_inventory_recommendations():

    if not DB_FILE.exists():
        raise FileNotFoundError(f"Database not found: {DB_FILE}")

    if not FORECAST_FILE.exists():
        raise FileNotFoundError(f"Forecast file not found: {FORECAST_FILE}")

    forecasts = pd.read_csv(FORECAST_FILE)

    required_columns = {
        "product_id", "store_id", "model", "predicted_quantity"
    }

    if not required_columns.issubset(forecasts.columns):
        raise ValueError("Forecast file is missing required columns.")

    forecasts = forecasts[
        forecasts["model"] == SELECTED_MODEL
    ].copy()

    if forecasts.empty:
        raise ValueError("No forecasts found for the selected model.")

    daily_forecasts = (
        forecasts
        .groupby(["product_id", "store_id"])["predicted_quantity"]
        .first()
        .reset_index()
    )

    connection = sqlite3.connect(DB_FILE)

    try:
        inventory = pd.read_sql_query(
            """
            SELECT product_id, store_id, current_stock,
                   reorder_level, lead_time_days
            FROM inventory
            """,
            connection
        )
    finally:
        connection.close()

    if inventory.empty:
        raise ValueError("No inventory records found.")

    df = inventory.merge(
        daily_forecasts,
        on=["product_id", "store_id"],
        how="left",
        validate="one_to_one"
    )

    if df["predicted_quantity"].isna().any():
        raise ValueError("Some inventory combinations do not have a forecast.")

    results = []

    for _, row in df.iterrows():

        daily_demand = max(0, float(row["predicted_quantity"]))
        current_stock = int(row["current_stock"])
        existing_reorder_level = int(row["reorder_level"])
        lead_time = int(row["lead_time_days"])

        lead_time_demand = math.ceil(daily_demand * lead_time)
        safety_stock = math.ceil(daily_demand * SAFETY_STOCK_DAYS)

        reorder_point = lead_time_demand + safety_stock

        target_stock = math.ceil(
            daily_demand
            * (lead_time + FUTURE_COVERAGE_DAYS + SAFETY_STOCK_DAYS)
        )

        reorder_quantity = max(0, target_stock - current_stock)

        if current_stock == 0:
            stockout_risk = "CRITICAL"
        elif current_stock <= reorder_point:
            stockout_risk = "HIGH"
        elif current_stock <= target_stock:
            stockout_risk = "MEDIUM"
        else:
            stockout_risk = "LOW"

        # Do not label stock as overstock when forecast demand is zero.
        if daily_demand == 0:
            overstock_risk = "NOT ASSESSABLE"
        elif current_stock > target_stock + math.ceil(
            daily_demand * FUTURE_COVERAGE_DAYS
        ):
            overstock_risk = "POTENTIAL"
        else:
            overstock_risk = "NO"

        recommendation = (
            "REORDER" if reorder_quantity > 0 else "NO REORDER"
        )

        existing_rule = (
            "REORDER"
            if current_stock <= existing_reorder_level
            else "NO REORDER"
        )

        results.append({
            "product_id": row["product_id"],
            "store_id": row["store_id"],
            "current_stock": current_stock,
            "daily_forecast": round(daily_demand, 4),
            "lead_time_days": lead_time,
            "lead_time_demand": lead_time_demand,
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "target_stock": target_stock,
            "recommended_order_quantity": reorder_quantity,
            "stockout_risk": stockout_risk,
            "overstock_risk": overstock_risk,
            "recommendation": recommendation,
            "existing_reorder_level": existing_reorder_level,
            "existing_rule": existing_rule
        })

    result_df = pd.DataFrame(results)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUTPUT_FILE, index=False)

    print("=" * 65)
    print("RETAILPULSE - INVENTORY RECOMMENDATIONS")
    print("=" * 65)

    print("\nInventory recommendations:")
    print(result_df.to_string(index=False))

    print("\nSummary:")
    print("Total combinations:", len(result_df))
    print("Items requiring reorder:",
          (result_df["recommendation"] == "REORDER").sum())
    print("Critical stockout risks:",
          (result_df["stockout_risk"] == "CRITICAL").sum())
    print("High stockout risks:",
          (result_df["stockout_risk"] == "HIGH").sum())
    print("Potential overstock cases:",
          (result_df["overstock_risk"] == "POTENTIAL").sum())
    print("Overstock not assessable:",
          (result_df["overstock_risk"] == "NOT ASSESSABLE").sum())

    print("\nOutput file created:")
    print(OUTPUT_FILE)
    print("\nInventory recommendations completed successfully!")


if __name__ == "__main__":
    generate_inventory_recommendations()
