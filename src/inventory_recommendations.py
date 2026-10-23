import pandas as pd
import sqlite3
import math
inventory = pd.read_csv("data/inventory_snapshot.csv")
print("Inventory data:")
print(inventory)
print("\nShape:")
print(inventory.shape)
print("\nMissing values:")
print(inventory.isna().sum())
print("\nDuplicate rows:")
print(inventory.duplicated().sum())
print("\nUnique products:")
print(inventory["product_id"].nunique())
print("\nUnique stores:")
print(inventory["store_id"].nunique())

valid_products = {"P001", "P002", "P003", "P004","P005", "P006", "P007"}
invalid_products = inventory[~inventory["product_id"].isin(valid_products)]
print("\nInvalid product IDs:")
print(invalid_products)
valid_stores = {"ST01", "ST02", "ST03"}
invalid_stores = inventory[~inventory["store_id"].isin(valid_stores)]
print("\nInvalid store IDs:")
print(invalid_stores)

out_of_stock = inventory[inventory["current_stock"] == 0]
below_reorder_level = inventory[inventory["current_stock"] < inventory["reorder_level"]]
print("\nOut-of-stock products:")
print(out_of_stock)
print("\nProducts below reorder level:")
print(below_reorder_level)

connection = sqlite3.connect("database/retailpulse.db")
print("\nDatabase connected successfully!") 
sales_query = """
SELECT
    o.store_id,
    oi.product_id,
    SUM(oi.quantity) AS units_sold,
    COUNT(DISTINCT o.order_date) AS selling_days
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY
    o.store_id,
    oi.product_id
"""
sales = pd.read_sql_query(sales_query, connection)
print("\nSales demand data:")
print(sales)
sales["average_daily_demand"] = (sales["units_sold"] / sales["selling_days"])
print("\nSales demand with average daily demand:")
print(sales)
inventory_analysis = inventory.merge(sales,on=["store_id", "product_id"], how="left")
print("\nInventory analysis:")
print(inventory_analysis)
inventory_analysis["days_of_stock_remaining"] = ( inventory_analysis["current_stock"]/ inventory_analysis["average_daily_demand"])
print("\nInventory analysis with days of stock remaining:")
print(inventory_analysis)
def get_inventory_status(row):
    if row["current_stock"] == 0:
        return "OUT OF STOCK"

    elif row["days_of_stock_remaining"] < row["lead_time_days"]:
        return "HIGH RISK"

    elif row["current_stock"] < row["reorder_level"]:
        return "REORDER"

    else:
        return "SUFFICIENT"


inventory_analysis["inventory_status"] = inventory_analysis.apply(
    get_inventory_status,
    axis=1
)

print("\nInventory status:")
print(
    inventory_analysis[
        [
            "store_id",
            "product_id",
            "current_stock",
            "lead_time_days",
            "days_of_stock_remaining",
            "inventory_status"
        ]
    ]
)
# Calculate suggested reorder quantity
def calculate_reorder_quantity(row):
    lead_time_demand = (
        row["average_daily_demand"]
        * row["lead_time_days"]
    )

    target_stock = max(
        row["reorder_level"],
        lead_time_demand * 1.20
    )

    reorder_quantity = max(
        0,
        math.ceil(target_stock - row["current_stock"])
    )

    return reorder_quantity


inventory_analysis["suggested_reorder_quantity"] = inventory_analysis.apply(
    calculate_reorder_quantity,
    axis=1
)

print("\nReorder recommendations:")
print(
    inventory_analysis[
        [
            "store_id",
            "product_id",
            "inventory_status",
            "suggested_reorder_quantity"
        ]
    ]
)


# Generate inventory report
report_path = "reports/inventory_report.md"

with open(report_path, "w") as report:
    report.write("# RetailPulse — Inventory Intelligence Report\n\n")

    report.write("## 1. Objective\n")
    report.write(
        "Analyze inventory levels and sales demand to identify "
        "stock risks and recommend products that need replenishment.\n\n"
    )

    report.write("## 2. Data Sources\n")
    report.write(
        "- Sales data: Existing RetailPulse SQLite database\n"
        "- Inventory data: data/inventory_snapshot.csv\n"
        "- Inventory and supplier values are realistic sample values "
        "because actual inventory and supplier data were not available.\n\n"
    )

    report.write("## 3. Assumptions\n")
    report.write(
        "- Demand is calculated using the available sales history.\n"
        "- Supplier lead time is measured in days.\n"
        "- A 20% safety buffer is used for reorder recommendations.\n"
        "- Inventory analysis is performed at product-store level.\n"
        "- Historical sales data is not modified.\n\n"
    )

    report.write("## 4. Validation Results\n")
    report.write(
        f"- Inventory records: {len(inventory_analysis)}\n"
        f"- Duplicate product-store combinations: "
        f"{inventory_analysis.duplicated(subset=['product_id', 'store_id']).sum()}\n"
        f"- Missing values: {inventory_analysis.isna().sum().sum()}\n"
        f"- Negative current stock: "
        f"{(inventory_analysis['current_stock'] < 0).sum()}\n"
        f"- Negative reorder quantities: "
        f"{(inventory_analysis['suggested_reorder_quantity'] < 0).sum()}\n\n"
    )

    report.write("## 5. Reorder Recommendations\n\n")

    report.write(
        "| Priority | Store | Product | Status | Suggested Reorder Quantity |\n"
    )
    report.write(
        "|---:|---|---|---|---:|\n"
    )

    priority_order = {
        "OUT OF STOCK": 1,
        "HIGH RISK": 2,
        "REORDER": 3,
        "SUFFICIENT": 4
    }

    recommendations = inventory_analysis[
        inventory_analysis["inventory_status"] != "SUFFICIENT"
    ].copy()

    recommendations["priority"] = recommendations[
        "inventory_status"
    ].map(priority_order)

    recommendations = recommendations.sort_values(
        ["priority", "store_id", "product_id"]
    )

    for _, row in recommendations.iterrows():
        report.write(
            f"| {int(row['priority'])} | "
            f"{row['store_id']} | "
            f"{row['product_id']} | "
            f"{row['inventory_status']} | "
            f"{int(row['suggested_reorder_quantity'])} |\n"
        )

    report.write("\n")

    report.write("## 6. Business Insights\n\n")

    out_of_stock_count = (
        inventory_analysis["inventory_status"] == "OUT OF STOCK"
    ).sum()

    high_risk_count = (
        inventory_analysis["inventory_status"] == "HIGH RISK"
    ).sum()

    report.write(
        f"- {out_of_stock_count} product-store combinations are out of stock.\n"
        f"- {high_risk_count} product-store combinations are at high risk.\n"
    )

    store_risk = (
        inventory_analysis[
            inventory_analysis["inventory_status"].isin(
                ["OUT OF STOCK", "HIGH RISK"]
            )
        ]
        .groupby("store_id")
        .size()
        .sort_values(ascending=False)
    )

    highest_risk_store = store_risk.index[0]

    report.write(
        f"- {highest_risk_store} has the highest number of risky "
        f"product-store combinations.\n"
    )

    report.write(
        "- Out-of-stock products should be prioritized first.\n"
        "- Products that may run out before supplier delivery should "
        "be monitored closely.\n"
        "- Products with high stock and low demand should be reviewed "
        "before placing additional orders.\n\n"
    )

    report.write("## 7. Reorder Quantity Rule\n\n")
    report.write(
        "Target Stock = MAX(Reorder Level, "
        "Lead-Time Demand × 1.20)\n\n"
        "Suggested Reorder Quantity = "
        "MAX(0, Target Stock - Current Stock)\n\n"
        "The 20% safety buffer is a project assumption because "
        "actual business safety-stock policies were not available.\n"
    )

connection.close()

print(f"\nInventory report generated successfully: {report_path}")