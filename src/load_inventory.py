import sqlite3
import pandas as pd

connection = sqlite3.connect("database/retailpulse.db")

connection.execute("PRAGMA foreign_keys = ON")

inventory = pd.read_csv("data/inventory_snapshot.csv")

create_table_sql = """
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT NOT NULL,
    store_id TEXT NOT NULL,
    current_stock INTEGER NOT NULL CHECK (current_stock >= 0),
    reorder_level INTEGER NOT NULL CHECK (reorder_level >= 0),
    lead_time_days INTEGER NOT NULL CHECK (lead_time_days > 0),

    PRIMARY KEY (product_id, store_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
)
"""

connection.execute(create_table_sql)
inventory.to_sql(
    "inventory",
    connection,
    if_exists="append",
    index=False
)

connection.commit()
connection.close()

print("Inventory data loaded successfully!")