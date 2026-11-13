
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"
GRAPH_DIR = REPORT_DIR / "graphs"

FORECAST_FILE = DATA_DIR / "demand_forecasts.csv"
METRICS_FILE = DATA_DIR / "forecast_metrics.csv"
INVENTORY_FILE = DATA_DIR / "inventory_recommendations.csv"

SELECTED_MODEL = "moving_average"


def create_actual_vs_predicted_graph():

    if not FORECAST_FILE.exists():
        raise FileNotFoundError(f"File not found: {FORECAST_FILE}")

    df = pd.read_csv(FORECAST_FILE)

    df = df[df["model"] == SELECTED_MODEL].copy()

    if df.empty:
        raise ValueError("No Moving Average predictions found.")

    # Calculate total actual and predicted demand for each date
    daily_comparison = (
        df.groupby("sales_date")
        .agg(
            actual_quantity=("actual_quantity", "sum"),
            predicted_quantity=("predicted_quantity", "sum")
        )
        .reset_index()
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        daily_comparison["sales_date"],
        daily_comparison["actual_quantity"],
        marker="o",
        label="Actual Demand"
    )

    plt.plot(
        daily_comparison["sales_date"],
        daily_comparison["predicted_quantity"],
        marker="o",
        label="Predicted Demand"
    )

    plt.title("Actual vs Predicted Daily Demand - Moving Average")
    plt.xlabel("Sales Date")
    plt.ylabel("Total Quantity")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output = GRAPH_DIR / "actual_vs_predicted.png"
    plt.savefig(output, dpi=300)
    plt.close()

    print("Created:", output)


def create_model_comparison_graph():

    if not METRICS_FILE.exists():
        raise FileNotFoundError(f"File not found: {METRICS_FILE}")

    metrics = pd.read_csv(METRICS_FILE)

    required = {"model", "MAE", "RMSE"}

    if not required.issubset(metrics.columns):
        raise ValueError("Metrics file is missing required columns.")

    metrics = metrics.sort_values("MAE")

    x = range(len(metrics))
    width = 0.35

    plt.figure(figsize=(11, 6))

    plt.bar(
        [i - width / 2 for i in x],
        metrics["MAE"],
        width,
        label="MAE"
    )

    plt.bar(
        [i + width / 2 for i in x],
        metrics["RMSE"],
        width,
        label="RMSE"
    )

    plt.title("Forecast Model Performance Comparison")
    plt.xlabel("Forecasting Model")
    plt.ylabel("Prediction Error")
    plt.xticks(list(x), metrics["model"], rotation=15)
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()

    output = GRAPH_DIR / "model_comparison.png"
    plt.savefig(output, dpi=300)
    plt.close()

    print("Created:", output)


def create_inventory_stock_graph():

    if not INVENTORY_FILE.exists():
        raise FileNotFoundError(f"File not found: {INVENTORY_FILE}")

    inventory = pd.read_csv(INVENTORY_FILE)

    required = {
        "product_id",
        "store_id",
        "current_stock",
        "reorder_point"
    }

    if not required.issubset(inventory.columns):
        raise ValueError("Inventory file is missing required columns.")

    inventory["combination"] = (
        inventory["product_id"] + " / " + inventory["store_id"]
    )

    x = range(len(inventory))
    width = 0.35

    plt.figure(figsize=(15, 7))

    plt.bar(
        [i - width / 2 for i in x],
        inventory["current_stock"],
        width,
        label="Current Stock"
    )

    plt.bar(
        [i + width / 2 for i in x],
        inventory["reorder_point"],
        width,
        label="Reorder Point"
    )

    plt.title("Current Inventory vs Forecast-Based Reorder Point")
    plt.xlabel("Product / Store")
    plt.ylabel("Quantity")
    plt.xticks(
        list(x),
        inventory["combination"],
        rotation=60,
        ha="right"
    )
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()

    output = GRAPH_DIR / "inventory_stock_analysis.png"
    plt.savefig(output, dpi=300)
    plt.close()

    print("Created:", output)


def main():

    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("RETAILPULSE - FORECASTING GRAPHS")
    print("=" * 60)

    create_actual_vs_predicted_graph()
    create_model_comparison_graph()
    create_inventory_stock_graph()

    print("\nAll three graphs generated successfully!")
    print("Graph folder:", GRAPH_DIR)


if __name__ == "__main__":
    main()
