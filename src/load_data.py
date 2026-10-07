import sqlite3
import pandas as pd

# Read cleaned sales data
df = pd.read_csv("data/processed/cleaned_sales.csv")

print("Rows in cleaned CSV:", len(df))

# Connect to SQLite database
connection = sqlite3.connect("database/retailpulse.db")

cursor = connection.cursor()

print("Database connected successfully!")

# Get unique orders
orders = df[
    ["order_id", "order_date", "customer_id", "store_id", "status"]
].drop_duplicates()

print("Unique orders:", len(orders))

# Insert orders
for _, row in orders.iterrows():
    cursor.execute("""
        INSERT INTO orders (
            order_id,
            order_date,
            customer_id,
            store_id,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        row["order_id"],
        row["order_date"],
        row["customer_id"],
        row["store_id"],
        row["status"]
    ))

print("Orders loaded successfully!")

# Insert order items
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO order_items (
            order_id,
            product_id,
            quantity,
            unit_price,
            discount,
            gross_amount,
            net_amount
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        row["order_id"],
        row["product_id"],
        row["quantity"],
        row["unit_price"],
        row["discount"],
        row["gross_amount"],
        row["net_amount"]
    ))

# Save changes
connection.commit()

print("Order items loaded successfully!")

connection.close()