import sqlite3

# Connect to the database
connection = sqlite3.connect("database/retailpulse.db")

cursor = connection.cursor()

# 1-5. Count records
queries = {
    "Customers": "SELECT COUNT(*) FROM customers",
    "Products": "SELECT COUNT(*) FROM products",
    "Stores": "SELECT COUNT(*) FROM stores",
    "Orders": "SELECT COUNT(*) FROM orders",
    "Order Items": "SELECT COUNT(*) FROM order_items"
}

print("=== Record Counts ===")

for table, query in queries.items():
    cursor.execute(query)
    count = cursor.fetchone()[0]
    print(f"{table}: {count}")

# 6. Invalid customer IDs
cursor.execute("""
    SELECT COUNT(*)
    FROM orders o
    LEFT JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL;
""")

print("Invalid customer references:", cursor.fetchone()[0])

# 7. Invalid product IDs
cursor.execute("""
    SELECT COUNT(*)
    FROM order_items oi
    LEFT JOIN products p
        ON oi.product_id = p.product_id
    WHERE p.product_id IS NULL;
""")

print("Invalid product references:", cursor.fetchone()[0])

# 8. Invalid store IDs
cursor.execute("""
    SELECT COUNT(*)
    FROM orders o
    LEFT JOIN stores s
        ON o.store_id = s.store_id
    WHERE s.store_id IS NULL;
""")

print("Invalid store references:", cursor.fetchone()[0])

# 9. Duplicate order IDs
cursor.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT order_id
        FROM orders
        GROUP BY order_id
        HAVING COUNT(*) > 1
    );
""")

print("Duplicate order IDs:", cursor.fetchone()[0])

# 10. Invalid quantities
cursor.execute("""
    SELECT COUNT(*)
    FROM order_items
    WHERE quantity <= 0;
""")

print("Invalid quantities:", cursor.fetchone()[0])

# 11. Negative prices
cursor.execute("""
    SELECT COUNT(*)
    FROM order_items
    WHERE unit_price < 0;
""")

print("Negative prices:", cursor.fetchone()[0])

import pandas as pd

df = pd.read_csv("data/processed/cleaned_sales.csv")

csv_gross_total = df["gross_amount"].sum()
csv_net_total = df["net_amount"].sum()

cursor.execute("SELECT SUM(gross_amount) FROM order_items")
db_gross_total = cursor.fetchone()[0]

cursor.execute("SELECT SUM(net_amount) FROM order_items")
db_net_total = cursor.fetchone()[0]

print("\n=== CSV vs Database Totals ===")
print("CSV Gross Amount:", csv_gross_total)
print("DB Gross Amount:", db_gross_total)

print("CSV Net Amount:", csv_net_total)
print("DB Net Amount:", db_net_total)

if csv_gross_total == db_gross_total and csv_net_total == db_net_total:
    print("Totals match successfully!")
else:
    print("Totals do not match!")

connection.close()

