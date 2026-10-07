import sqlite3

connection = sqlite3.connect("database/retailpulse.db")

cursor = connection.cursor()

sql_files = [
    "sql/customers_data.sql",
    "sql/products_data.sql",
    "sql/stores_data.sql"
]

for file in sql_files:
    print(f"Loading: {file}")

    with open(file, "r") as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)

connection.commit()

connection.close()

print("Reference data loaded successfully!")