
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"

INPUT_FILE = DATA_DIR / "demand_forecasts.csv"

METRICS_FILE = DATA_DIR / "forecast_metrics.csv"
COMPARISON_FILE = DATA_DIR / "forecast_actual_comparison.csv"


def evaluate_forecasts():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Forecast file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("Forecast dataset is empty.")

    results = []

    for model_name, group in df.groupby("model"):

        actual = group["actual_quantity"]
        predicted = group["predicted_quantity"]

        mae = mean_absolute_error(actual, predicted)

        rmse = np.sqrt(mean_squared_error(actual, predicted))

        # MAPE is calculated only where actual demand is greater than zero.
        non_zero = actual > 0

        if non_zero.any():
            mape = (
                np.abs(
                    (actual[non_zero] - predicted[non_zero])
                    / actual[non_zero]
                ).mean()
                * 100
            )
        else:
            mape = np.nan

        results.append({
            "model": model_name,
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "MAPE_percent": round(mape, 2),
            "test_records": len(group),
            "zero_actual_records": int((actual == 0).sum())
        })

    metrics_df = pd.DataFrame(results)

    metrics_df = metrics_df.sort_values(
        by="MAE"
    ).reset_index(drop=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    metrics_df.to_csv(METRICS_FILE, index=False)

    # Save actual vs predicted comparison
    comparison_df = df.copy()

    comparison_df["prediction_error"] = (
        comparison_df["actual_quantity"]
        - comparison_df["predicted_quantity"]
    )

    comparison_df.to_csv(COMPARISON_FILE, index=False)

    print("=" * 60)
    print("RETAILPULSE - FORECAST EVALUATION")
    print("=" * 60)

    print("\nModel performance:")
    print(metrics_df.to_string(index=False))

    print("\nBest model based on MAE:")
    print(metrics_df.iloc[0]["model"])

    print("\nEvaluation files created:")
    print(METRICS_FILE)
    print(COMPARISON_FILE)

    print("\nForecast evaluation completed successfully!")


if __name__ == "__main__":
    evaluate_forecasts()
