import sqlite3
DB_PATH = "database/retailpulse.db"
conn = sqlite3.connect(DB_PATH)
print("Connected to RetailPulse database")

query = """
SELECT
    o.customer_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS units_purchased,
    SUM(oi.net_amount) AS net_spending,
    MIN(o.order_date) AS first_purchase_date,
    MAX(o.order_date) AS most_recent_purchase_date,
    ROUND(
        SUM(oi.net_amount) * 1.0
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
WHERE o.status != 'Cancelled'
GROUP BY o.customer_id
ORDER BY net_spending DESC;
"""

cursor = conn.cursor()
cursor.execute(query)

rows = cursor.fetchall()

print("Number of customers:", len(rows))
print(rows[:5])
import pandas as pd

columns = [
    "customer_id",
    "total_orders",
    "units_purchased",
    "net_spending",
    "first_purchase_date",
    "most_recent_purchase_date",
    "average_order_value"
]

df = pd.DataFrame(rows, columns=columns)

print("\nCustomer Data:")
print(df.head())
analysis_date = pd.Timestamp("2026-02-10")

df["most_recent_purchase_date"] = pd.to_datetime(
    df["most_recent_purchase_date"]
)

df["recency"] = (
    analysis_date - df["most_recent_purchase_date"]
).dt.days

print("\nRFM Data:")
print(
    df[
        [
            "customer_id",
            "most_recent_purchase_date",
            "recency",
            "total_orders",
            "net_spending"
        ]
    ].head()
)
def assign_segment(row):
    if row["net_spending"] >= 625 and row["recency"] <= 29:
        return "High Value"

    elif row["net_spending"] >= 625 and row["recency"] > 29:
        return "At Risk"

    elif row["net_spending"] < 625 and row["recency"] <= 29:
        return "Recent Low Engagement"

    else:
        return "Low Engagement"


df["customer_segment"] = df.apply(assign_segment, axis=1)

print("\nCustomer Segments:")
print(
    df[
        [
            "customer_id",
            "recency",
            "total_orders",
            "net_spending",
            "customer_segment"
        ]
    ].head(10)
)
segment_summary = (
    df.groupby("customer_segment")
      .agg(
          customer_count=("customer_id", "count"),
          segment_revenue=("net_spending", "sum")
      )
      .reset_index()
)

print("\nSegment Summary:")
print(segment_summary)
expected_counts = {
    "High Value": 31,
    "At Risk": 13,
    "Recent Low Engagement": 18,
    "Low Engagement": 5
}

actual_counts = dict(
    zip(
        segment_summary["customer_segment"],
        segment_summary["customer_count"]
    )
)

if actual_counts == expected_counts:
    print("\nValidation passed: Python segmentation matches SQL results.")
else:
    print("\nValidation failed: Python and SQL results do not match.")
    print("Expected:", expected_counts)
    print("Actual:", actual_counts)
customer_query = """
SELECT customer_id
FROM customers
"""

customer_rows = conn.execute(customer_query).fetchall()

all_customers = {row[0] for row in customer_rows}
eligible_customers = set(df["customer_id"])

customers_without_purchases = all_customers - eligible_customers

print("\nCustomers without eligible purchases:")

if customers_without_purchases:
    print(customers_without_purchases)
else:
    print("None")
df["customer_type"] = df["total_orders"].apply(
    lambda orders: "One-time buyer"
    if orders == 1
    else "Repeat buyer"
)

customer_type_summary = (
    df["customer_type"]
    .value_counts()
    .reset_index()
)

customer_type_summary.columns = [
    "customer_type",
    "customer_count"
]

print("\nCustomer Type Summary:")
print(customer_type_summary)
revenue_by_customer_type = (
    df.groupby("customer_type")["net_spending"]
      .sum()
      .reset_index()
)

print("\nRevenue by Customer Type:")
print(revenue_by_customer_type)
top_10_customers = (
    df.nlargest(10, "net_spending")
      [
          [
              "customer_id",
              "net_spending",
              "customer_segment"
          ]
      ]
      .reset_index(drop=True)
)

top_10_customers["customer_rank"] = (
    top_10_customers.index + 1
)

print("\nTop 10 Customers:")
print(top_10_customers)
top_10_sales = top_10_customers["net_spending"].sum()

total_sales = df["net_spending"].sum()

top_10_percentage = (
    top_10_sales / total_sales
) * 100

print("\nTop 10 Revenue Contribution:")
print("Top 10 sales:", top_10_sales)
print("Total sales:", total_sales)
print("Top 10 sales percentage:", round(top_10_percentage, 2), "%")
inactive_customers = df[df["recency"] > 29].copy()

inactive_customers = inactive_customers[
    [
        "customer_id",
        "recency",
        "net_spending",
        "customer_segment"
    ]
].sort_values("recency", ascending=False)

print("\nCustomers who haven't purchased recently:")
print(inactive_customers)



report_path = "reports/customer_analytics_report.md"

with open(report_path, "w", encoding="utf-8") as report:

    report.write("# RetailPulse - Customer Analytics & Segmentation Report\n\n")

    report.write("## 1. Objective\n\n")
    report.write(
        "The objective of this analysis is to understand customer "
        "purchasing behavior, identify customer segments, and find "
        "customers who may need retention attention.\n\n"
    )

    report.write("## 2. Analysis Date\n\n")
    report.write(
        f"The analysis date is **{analysis_date.strftime('%Y-%m-%d')}**.\n\n"
    )

    report.write("## 3. RFM Methodology\n\n")
    report.write(
        "- **Recency:** Number of days since the customer's most recent purchase.\n"
        "- **Frequency:** Number of distinct orders placed by the customer.\n"
        "- **Monetary:** Total net spending by the customer.\n\n"
    )

    report.write("## 4. Segmentation Rules\n\n")
    report.write(
        "| Segment | Rule |\n"
        "|---|---|\n"
        "| High Value | Spending >= ₹625 and Recency <= 29 days |\n"
        "| At Risk | Spending >= ₹625 and Recency > 29 days |\n"
        "| Recent Low Engagement | Spending < ₹625 and Recency <= 29 days |\n"
        "| Low Engagement | Spending < ₹625 and Recency > 29 days |\n\n"
    )

    report.write("## 5. Segment Summary\n\n")
    report.write(
        "| Segment | Customers | Revenue |\n"
        "|---|---:|---:|\n"
    )

    for _, row in segment_summary.iterrows():
        report.write(
            f"| {row['customer_segment']} | "
            f"{row['customer_count']} | "
            f"₹{row['segment_revenue']:,.2f} |\n"
        )

    report.write("\n")

    report.write("## 6. Repeat vs One-time Customers\n\n")

    for _, row in customer_type_summary.iterrows():
        report.write(
            f"- **{row['customer_type']}:** "
            f"{row['customer_count']} customers\n"
        )

    report.write("\n")

    report.write("## 7. Revenue by Customer Type\n\n")

    for _, row in revenue_by_customer_type.iterrows():
        report.write(
            f"- **{row['customer_type']}:** "
            f"₹{row['net_spending']:,.2f}\n"
        )

    report.write("\n")

    report.write("## 8. Top 10 Customers\n\n")
    report.write(
        "| Rank | Customer | Net Spending | Segment |\n"
        "|---:|---|---:|---|\n"
    )

    for _, row in top_10_customers.iterrows():
        report.write(
            f"| {row['customer_rank']} | "
            f"{row['customer_id']} | "
            f"₹{row['net_spending']:,.2f} | "
            f"{row['customer_segment']} |\n"
        )

    report.write("\n")

    report.write("## 9. Top 10 Revenue Contribution\n\n")
    report.write(
        f"The top 10 customers generated **₹{top_10_sales:,.2f}**, "
        f"representing **{top_10_percentage:.2f}%** of total "
        f"eligible net sales of **₹{total_sales:,.2f}**.\n\n"
    )

    report.write("## 10. Customers Who Have Not Purchased Recently\n\n")
    report.write(
        f"There are **{len(inactive_customers)} customers** "
        f"with more than 29 days since their most recent purchase.\n\n"
    )

    report.write(
        "| Customer | Recency | Net Spending | Segment |\n"
        "|---|---:|---:|---|\n"
    )

    for _, row in inactive_customers.iterrows():
        report.write(
            f"| {row['customer_id']} | "
            f"{row['recency']} days | "
            f"₹{row['net_spending']:,.2f} | "
            f"{row['customer_segment']} |\n"
        )

    report.write("\n")

    report.write("## 11. Business Recommendations\n\n")
    report.write(
        "- Prioritize **At Risk** customers for retention campaigns.\n"
        "- Focus especially on high-spending At Risk customers.\n"
        "- Encourage one-time buyers to make a second purchase.\n"
        "- Use targeted offers for Recent Low Engagement customers.\n"
        "- Monitor customer activity as more historical data becomes available.\n\n"
    )

    report.write("## 12. Limitations\n\n")
    report.write(
        "- The dataset covers a limited historical period.\n"
        "- All customers currently have only one eligible order, so repeat "
        "purchase behavior cannot be measured yet.\n"
        "- At Risk is a recency-based signal and should not be interpreted "
        "as confirmed customer churn.\n"
        "- Segmentation thresholds were derived from the current dataset "
        "and may change as more data becomes available.\n"
    )

print(f"\nReport generated successfully: {report_path}")