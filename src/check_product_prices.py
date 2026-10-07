import pandas as pd
df = pd.read_csv("data/processed/cleaned_sales.csv")
product_prices = df[["product_id", "unit_price"]].drop_duplicates()
print(product_prices.sort_values("product_id"))