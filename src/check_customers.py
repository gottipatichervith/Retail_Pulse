import pandas as pd

df = pd.read_csv("data/processed/cleaned_sales.csv")

customers = df["customer_id"].drop_duplicates().sort_values()

print("Unique customers:", len(customers))
print(customers.to_list())