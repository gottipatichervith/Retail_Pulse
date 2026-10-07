import sqlite3
from pathlib import Path

# Create the database folder if it doesn't exist
Path("database").mkdir(exist_ok=True)

# Connect to SQLite database
connection = sqlite3.connect("database/retailpulse.db")
connection.execute("PRAGMA foreign_keys = ON")


cursor = connection.cursor()

sql_files = [
    "sql/customers.sql",
    "sql/products.sql",
    "sql/stores.sql",
    "sql/orders.sql",
    "sql/order_items.sql"
]
    


for file in sql_files:
    print(f"Executing: {file}")

    with open(file, "r") as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)

connection.commit()


connection.close()

print("Database created successfully!")