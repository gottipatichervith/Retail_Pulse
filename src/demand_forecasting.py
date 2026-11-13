
from pathlib import Path

import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

TRAIN_FILE = DATA_DIR / "forecast_train.csv"
TEST_FILE = DATA_DIR / "forecast_test.csv"

OUTPUT_FILE = DATA_DIR / "demand_forecasts.csv"

# Model settings
MOVING_AVERAGE_WINDOW = 7
SMOOTHING_ALPHA = 0.3


def load_data():
    """Load training and testing datasets."""

    if not TRAIN_FILE.exists():
        raise FileNotFoundError(f"Training file not found: {TRAIN_FILE}")

    if not TEST_FILE.exists():
        raise FileNotFoundError(f"Testing file not found: {TEST_FILE}")

    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)

    for df in [train_df, test_df]:
        df["sales_date"] = pd.to_datetime(df["sales_date"])
        df["daily_quantity"] = pd.to_numeric(
            df["daily_quantity"], errors="raise"
        )

    if train_df.empty or test_df.empty:
        raise ValueError("Training or testing dataset is empty.")

    return train_df, test_df


def historical_average(series):
    """Predict using average historical daily demand."""

    return series.mean()


def naive_forecast(series):
    """Predict using the latest observed demand."""

    return series.iloc[-1]


def moving_average_forecast(series):
    """Predict using the average of the latest 7 days."""

    recent_values = series.tail(MOVING_AVERAGE_WINDOW)

    return recent_values.mean()


def exponential_smoothing_forecast(series):
    """
    Simple exponential smoothing.

    Recent observations receive more importance.
    """

    forecast = float(series.iloc[0])

    for actual_value in series.iloc[1:]:
        forecast = (
            SMOOTHING_ALPHA * float(actual_value)
            + (1 - SMOOTHING_ALPHA) * forecast
        )

    return forecast


def generate_forecasts(train_df, test_df):
    """Generate forecasts for every product-store combination."""

    results = []

    combinations = train_df[
        ["product_id", "store_id"]
    ].drop_duplicates()

    for _, combination in combinations.iterrows():

        product_id = combination["product_id"]
        store_id = combination["store_id"]

        train_group = train_df[
            (train_df["product_id"] == product_id)
            & (train_df["store_id"] == store_id)
        ].sort_values("sales_date")

        test_group = test_df[
            (test_df["product_id"] == product_id)
            & (test_df["store_id"] == store_id)
        ].sort_values("sales_date")

        if train_group.empty or test_group.empty:
            continue

        history = train_group["daily_quantity"]

        # Calculate forecasts using training data only
        predictions = {
            "historical_average": historical_average(history),
            "naive": naive_forecast(history),
            "moving_average": moving_average_forecast(history),
            "exponential_smoothing": exponential_smoothing_forecast(
                history
            )
        }

        # Compare predictions against actual test values
        for _, test_row in test_group.iterrows():

            for model_name, prediction in predictions.items():

                results.append({
                    "sales_date": test_row["sales_date"],
                    "product_id": product_id,
                    "store_id": store_id,
                    "actual_quantity": test_row["daily_quantity"],
                    "model": model_name,
                    "predicted_quantity": max(0, prediction)
                })

    return pd.DataFrame(results)


def main():

    print("=" * 60)
    print("RETAILPULSE - DEMAND FORECASTING")
    print("=" * 60)

    # Load datasets
    train_df, test_df = load_data()

    print(f"\nTraining records: {len(train_df)}")
    print(f"Testing records: {len(test_df)}")

    print(
        f"Training period: {train_df['sales_date'].min().date()} "
        f"to {train_df['sales_date'].max().date()}"
    )

    print(
        f"Testing period: {test_df['sales_date'].min().date()} "
        f"to {test_df['sales_date'].max().date()}"
    )

    # Generate predictions
    forecast_df = generate_forecasts(train_df, test_df)

    if forecast_df.empty:
        raise ValueError("No forecasts were generated.")

    # Save predictions
    forecast_df.to_csv(OUTPUT_FILE, index=False)

    print("\nForecast generation completed!")

    print(f"Forecast records: {len(forecast_df)}")
    print(f"Products: {forecast_df['product_id'].nunique()}")
    print(f"Stores: {forecast_df['store_id'].nunique()}")
    print(f"Models: {forecast_df['model'].nunique()}")

    print("\nModel record counts:")
    print(forecast_df["model"].value_counts())

    print(f"\nForecast file saved: {OUTPUT_FILE}")

    print("\nSample predictions:")
    print(forecast_df.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
