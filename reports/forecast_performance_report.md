# RetailPulse — Forecast Performance Report

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

| Model | MAE | RMSE | MAPE (%) | Test Records |
|---|---:|---:|---:|---:|
| moving_average | 0.1672 | 0.3022 | 94.51 | 147 |
| exponential_smoothing | 0.1698 | 0.3187 | 97.98 | 147 |
| naive | 0.1837 | 0.4286 | 100.00 | 147 |
| historical_average | 0.1847 | 0.2936 | 89.66 | 147 |

## 5. Selected Model

The selected model was **moving_average**, with an MAE of **0.1672**.

It achieved the lowest Mean Absolute Error among the evaluated models.

## 6. Evaluation Observations

- Test records evaluated: 147
- Records with zero actual demand: 134
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

The moving_average model achieved the lowest MAE in this evaluation. It provides a basic forecasting baseline for RetailPulse. More historical data and further testing are needed before relying on these forecasts for major purchasing decisions.
