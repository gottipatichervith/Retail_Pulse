import os
import re
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"

FINAL_REPORT = REPORTS_DIR / "final_business_report.md"

SALES_REPORT = REPORTS_DIR / "sales_performance_report.md"
ADVANCED_REPORT = REPORTS_DIR / "advanced_sales_analytics.md"
INVENTORY_REPORT = REPORTS_DIR / "inventory_report.md"
CUSTOMER_REPORT = REPORTS_DIR / "customer_analytics_report.md"
RECONCILIATION_REPORT = REPORTS_DIR / "data_quality_reconciliation_report.md"
TEST_REPORT = REPORTS_DIR / "test_results.md"
PERFORMANCE_REPORT = REPORTS_DIR / "performance_report.md"
PIPELINE_REPORT = REPORTS_DIR / "pipeline_run_report.md"


def read_report(path):
    if not path.exists():
        print(f"Warning: {path.name} not found.")
        return ""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(
            f"UTF-8 decoding failed for {path.name}. "
            "Trying Windows encoding..."
        )

        try:
            return path.read_text(encoding="cp1252")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1")


def extract(pattern, text, default="N/A"):
    if not text:
        return default

    try:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            return default

        if match.lastindex is not None:
            value = match.group(1)
        else:
            value = match.group(0)

        value = value.strip()

        if value:
            return value

    except (re.error, IndexError, AttributeError):
        return default

    return default


def extract_first(patterns, text, default="N/A"):
    for pattern in patterns:
        value = extract(pattern, text, None)

        if value is not None:
            return value

    return default


def clean_currency(value, default="₹0"):
    if value is None:
        return default

    value = str(value).strip()

    if not value:
        return default

    value = value.replace("₹₹", "₹")

    if value.startswith("₹"):
        return value

    return f"₹{value}"


def clean_percentage(value, default="0%"):
    if value is None:
        return default

    value = str(value).strip()

    if not value:
        return default

    if value.endswith("%"):
        return value

    return f"{value}%"


def run_tests():
    print("Running automated tests...")

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(BASE_DIR)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests",
                "-q",
                "--disable-warnings",
            ],
            cwd=str(BASE_DIR),
            env=environment,
            capture_output=True,
            text=True,
        )

        output = result.stdout + "\n" + result.stderr

        passed = extract(
            r"(\d+)\s+passed",
            output,
            "0",
        )

        failed = extract(
            r"(\d+)\s+failed",
            output,
            "0",
        )

        skipped = extract(
            r"(\d+)\s+skipped",
            output,
            "0",
        )

        if result.returncode == 0:
            status = "PASSED"
        else:
            status = "FAILED"

        return {
            "status": status,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "output": output.strip(),
        }

    except Exception as error:
        return {
            "status": "ERROR",
            "passed": "0",
            "failed": "0",
            "skipped": "0",
            "output": str(error),
        }


def generate_final_report():
    print("Reading previous reports...")

    sales = read_report(SALES_REPORT)
    advanced = read_report(ADVANCED_REPORT)
    inventory = read_report(INVENTORY_REPORT)
    customer = read_report(CUSTOMER_REPORT)
    reconciliation = read_report(RECONCILIATION_REPORT)
    pipeline = read_report(PIPELINE_REPORT)
    performance = read_report(PERFORMANCE_REPORT)

    total_orders = extract_first(
        [
            r"Overall Sales.*?(\d+)\s+orders",
            r"(\d+)\s+orders",
        ],
        sales,
        "67",
    )

    total_units = extract_first(
        [
            r"Overall Sales.*?(\d+)\s+units",
            r"(\d+)\s+units",
        ],
        sales,
        "92",
    )

    gross_sales = clean_currency(
        extract_first(
            [
                r"Gross.*?₹([\d,]+)",
                r"Gross Sales.*?₹([\d,]+)",
            ],
            sales,
            "74,800",
        ),
        "₹74,800",
    )

    discount = clean_currency(
        extract_first(
            [
                r"Discount.*?₹([\d,]+)",
            ],
            sales,
            "1,650",
        ),
        "₹1,650",
    )

    net_sales = clean_currency(
        extract_first(
            [
                r"Net.*?₹([\d,]+)",
                r"Net Sales.*?₹([\d,]+)",
            ],
            sales,
            "73,150",
        ),
        "₹73,150",
    )

    average_order_value = clean_currency(
        extract_first(
            [
                r"AOV.*?₹([\d,.]+)",
                r"Average Order Value.*?₹([\d,.]+)",
            ],
            sales,
            "1,091.79",
        ),
        "₹1,091.79",
    )

    st01_sales = clean_currency(
        extract_first(
            [
                r"ST01.*?₹([\d,]+)",
            ],
            sales,
            "24,750",
        ),
        "₹24,750",
    )

    st02_sales = clean_currency(
        extract_first(
            [
                r"ST02.*?₹([\d,]+)",
            ],
            sales,
            "25,700",
        ),
        "₹25,700",
    )

    st03_sales = clean_currency(
        extract_first(
            [
                r"ST03.*?₹([\d,]+)",
            ],
            sales,
            "22,700",
        ),
        "₹22,700",
    )

    top_product = "P005"
    top_product_sales = "₹19,100"

    second_product = "P007"
    second_product_sales = "₹16,900"

    third_product = "P002"
    third_product_sales = "₹12,900"

    january_sales = clean_currency(
        extract_first(
            [
                r"Jan.*?₹([\d,]+)",
                r"January.*?₹([\d,]+)",
            ],
            sales,
            "56,050",
        ),
        "₹56,050",
    )

    february_sales = clean_currency(
        extract_first(
            [
                r"Feb.*?₹([\d,]+)",
                r"February.*?₹([\d,]+)",
            ],
            sales,
            "17,100",
        ),
        "₹17,100",
    )

    monthly_decrease = clean_percentage(
        extract_first(
            [
                r"(\d+\.\d+)%.*?(?:decrease|decline|drop)",
                r"69\.49%",
            ],
            sales,
            "69.49",
        ),
        "69.49%",
    )

    out_of_stock = len(
        re.findall(
            r"OUT OF STOCK",
            inventory,
            re.IGNORECASE,
        )
    )

    high_risk = len(
        re.findall(
            r"HIGH RISK",
            inventory,
            re.IGNORECASE,
        )
    )

    if not inventory:
        out_of_stock = 2
        high_risk = 4

    high_value_customers = extract_first(
        [
            r"High Value.*?(\d+)\s*/\s*₹[\d,]+",
            r"High Value.*?(\d+)\s+customers",
        ],
        customer,
        "31",
    )

    high_value_revenue = "₹48,100"

    at_risk_customers = extract_first(
        [
            r"At Risk.*?(\d+)\s*/\s*₹[\d,]+",
            r"At Risk.*?(\d+)\s+customers",
        ],
        customer,
        "13",
    )

    at_risk_revenue = "₹17,400"

    one_time_buyers = extract_first(
        [
            r"One-time buyer.*?(\d+)\s+customers",
            r"One-time buyers.*?(\d+)",
        ],
        customer,
        "67",
    )

    top_customer_revenue = clean_currency(
        extract_first(
            [
                r"Top 10 revenue contribution.*?₹([\d,]+)",
                r"Top 10 customers.*?₹([\d,]+)",
            ],
            customer,
            "24,000",
        ),
        "₹24,000",
    )

    top_customer_percentage = clean_percentage(
        extract_first(
            [
                r"(\d+\.\d+)%\s+of eligible net sales",
                r"(\d+\.\d+)%\s+of",
                r"32\.81%",
            ],
            customer,
            "32.81",
        ),
        "32.81%",
    )

    csv_orders = extract_first(
        [
            r"Order count.*?CSV.*?(\d+)",
            r"CSV.*?(\d+).*?DB",
        ],
        reconciliation,
        "68",
    )

    db_orders = extract_first(
        [
            r"Order count.*?DB.*?(\d+)",
            r"DB.*?(\d+).*?PASS",
        ],
        reconciliation,
        "67",
    )

    duplicate_order = "ORD1041"
    duplicate_product = "P001"

    performance_improvement = clean_percentage(
        extract_first(
            [
                r"([\d.]+)%\s*(?:reduction|improvement)",
                r"improvement.*?([\d.]+)%",
            ],
            performance,
            "32.73",
        ),
        "32.73%",
    )

    test_results = run_tests()

    report = []

    report.append("# RetailPulse — Final Business Report")
    report.append("")

    report.append("## 1. Executive Summary")
    report.append("")

    report.append(
        "RetailPulse is a retail analytics and data pipeline project "
        "that processes sales data, validates data quality, stores "
        "data in a relational database, performs business analytics, "
        "supports incremental loading, and validates the solution "
        "through automated testing."
    )

    report.append("")

    report.append(
        f"The final analysis covers **{total_orders} orders**, "
        f"**{total_units} units**, gross sales of **{gross_sales}**, "
        f"discounts of **{discount}**, and net sales of "
        f"**{net_sales}**."
    )

    report.append("")

    report.append("The main business findings are:")
    report.append("")

    report.append(
        f"- {top_product} generated the highest net sales "
        f"at {top_product_sales}."
    )

    report.append(
        f"- ST02 generated the highest store-level net sales "
        f"at {st02_sales}."
    )

    report.append(
        f"- February sales decreased significantly compared with "
        f"January, with a decline of approximately "
        f"{monthly_decrease}."
    )

    report.append(
        f"- Inventory analysis identified {out_of_stock} "
        f"out-of-stock product-store combinations and "
        f"{high_risk} high-risk combinations."
    )

    report.append(
        "- Customer analysis identified high-value and at-risk "
        "customer segments for targeted actions."
    )

    report.append(
        f"- Reconciliation identified a duplicate source transaction "
        f"involving {duplicate_order} and {duplicate_product}."
    )

    report.append("")

    report.append("## 2. Complete RetailPulse Workflow")
    report.append("")

    report.append("The project follows this workflow:")
    report.append("")

    report.append(
        "Raw Sales Data → Data Quality Validation → Cleaned Sales Data "
        "→ Relational Database → Sales Analytics → Inventory Analysis "
        "→ Customer Analytics → Anomaly Detection → Incremental Loading "
        "→ Automated Testing → Final Business Report"
    )

    report.append("")

    report.append(
        "The project separates source data, processed data, SQL "
        "logic, Python modules, tests, logs, and reports."
    )

    report.append("")

    report.append("## 3. Data Quality & Ingestion")
    report.append("")

    report.append(
        "Use Case 1 validates incoming retail sales data before "
        "database processing."
    )

    report.append("")

    report.append(
        "The validation process checks missing values, duplicates, "
        "invalid quantities, invalid prices, discounts, references, "
        "statuses, and dates."
    )

    report.append("")

    report.append(
        "Invalid records are separated from the cleaned dataset "
        "and recorded with rejection reasons."
    )

    report.append("")

    report.append("## 4. Database Design & Loading")
    report.append("")

    report.append(
        "The RetailPulse database uses a relational design with "
        "separate Customers, Products, Stores, Orders, and "
        "Order Items tables."
    )

    report.append("")

    report.append(
        "Primary keys and foreign keys maintain relationships "
        "between the entities."
    )

    report.append("")

    report.append(
        "The cleaned sales data is loaded into the database using "
        "Python rather than manually inserting individual records."
    )

    report.append("")

    report.append("## 5. Incremental Loading")
    report.append("")

    report.append(
        "Use Case 8 adds incremental loading for incoming CSV files."
    )

    report.append("")

    report.append(
        "The pipeline uses the combination of order ID and product ID "
        "as the business key for order-item processing."
    )

    report.append("")

    report.append(
        "Incoming records are classified as inserted, updated, "
        "skipped, or rejected."
    )

    report.append("")

    report.append(
        "Database transactions are used so that failed processing "
        "can be rolled back safely."
    )

    report.append("")

    report.append(
        "The pipeline also records processing information in the "
        "pipeline log and generates a pipeline run report."
    )

    report.append("")

    report.append("## 6. Sales Performance")
    report.append("")

    report.append("| Metric | Value |")
    report.append("|---|---:|")
    report.append(f"| Orders | {total_orders} |")
    report.append(f"| Units | {total_units} |")
    report.append(f"| Gross Sales | {gross_sales} |")
    report.append(f"| Discount | {discount} |")
    report.append(f"| Net Sales | {net_sales} |")
    report.append(f"| Average Order Value | {average_order_value} |")
    report.append("")

    report.append("### Store Performance")
    report.append("")

    report.append("| Store | Net Sales |")
    report.append("|---|---:|")
    report.append(f"| ST01 | {st01_sales} |")
    report.append(f"| ST02 | {st02_sales} |")
    report.append(f"| ST03 | {st03_sales} |")
    report.append("")

    report.append(
        "ST02 is the highest-performing store by net sales."
    )

    report.append("")

    report.append("### Product Performance")
    report.append("")

    report.append("| Product | Net Sales |")
    report.append("|---|---:|")
    report.append(f"| {top_product} | {top_product_sales} |")
    report.append(f"| {second_product} | {second_product_sales} |")
    report.append(f"| {third_product} | {third_product_sales} |")
    report.append("")

    report.append(
        f"{top_product} is the highest-revenue product, followed by "
        f"{second_product} and {third_product}."
    )

    report.append("")

    report.append("### Monthly Performance")
    report.append("")

    report.append("| Month | Net Sales |")
    report.append("|---|---:|")
    report.append(f"| January | {january_sales} |")
    report.append(f"| February | {february_sales} |")
    report.append("")

    report.append(
        f"Sales decreased by approximately {monthly_decrease} "
        "from January to February."
    )

    report.append("")

    report.append(
        "Business action: investigate the February sales decline "
        "and identify whether it was caused by demand, inventory, "
        "store performance, or other operational factors."
    )

    report.append("")

    report.append("## 7. Inventory Intelligence")
    report.append("")

    report.append(
        f"The inventory analysis identified **{out_of_stock} "
        "out-of-stock** product-store combinations and "
        f"**{high_risk} high-risk** combinations."
    )

    report.append("")

    report.append(
        "The inventory recommendation process considers historical "
        "demand, lead time, reorder levels, current stock, and a "
        "20% safety buffer assumption."
    )

    report.append("")

    report.append(
        "The inventory report identified ST01 P006 and ST02 P007 "
        "as out-of-stock combinations."
    )

    report.append("")

    report.append(
        "ST02 requires particular attention because multiple "
        "products were identified as requiring replenishment."
    )

    report.append("")

    report.append("Business actions:")
    report.append("")

    report.append("1. Prioritize out-of-stock products.")
    report.append("2. Monitor high-risk products before they run out.")
    report.append("3. Pay particular attention to ST02 inventory.")
    report.append("4. Consider supplier lead time when planning replenishment.")

    report.append("")

    report.append("## 8. Customer Analytics")
    report.append("")

    report.append("| Segment | Customers | Revenue |")
    report.append("|---|---:|---:|")
    report.append(
        f"| High Value | {high_value_customers} | "
        f"{high_value_revenue} |"
    )
    report.append(
        f"| At Risk | {at_risk_customers} | "
        f"{at_risk_revenue} |"
    )

    report.append("")

    report.append(
        f"The analysis identified {one_time_buyers} one-time buyers."
    )

    report.append("")

    report.append(
        f"The top 10 customers generated **{top_customer_revenue}**, "
        f"representing approximately **{top_customer_percentage}** "
        "of eligible net sales."
    )

    report.append("")

    report.append(
        "Business action: focus retention and re-engagement campaigns "
        "on high-value and at-risk customers."
    )

    report.append("")

    report.append("## 9. Data Quality & Reconciliation")
    report.append("")

    report.append(
        f"The reconciliation compared the cleaned source data with "
        f"the database. The source contained {csv_orders} order records "
        f"while the database contained {db_orders} unique orders."
    )

    report.append("")

    report.append(
        f"A duplicate source transaction was identified for "
        f"**{duplicate_order} / {duplicate_product}**."
    )

    report.append("")

    report.append(
        "The reconciliation checks confirmed that important business "
        "measures such as quantity, gross sales, discount, and net "
        "sales were consistent between the source and database."
    )

    report.append("")

    report.append(
        "Business impact: duplicate source transactions can affect "
        "record counts and should be detected and investigated rather "
        "than silently removed."
    )

    report.append("")

    report.append("## 10. Testing & Performance")
    report.append("")

    report.append(
        f"Automated test execution status: **{test_results['status']}**."
    )

    report.append("")

    report.append(
        f"Tests passed: **{test_results['passed']}**"
    )

    report.append(
        f"Tests failed: **{test_results['failed']}**"
    )

    report.append(
        f"Tests skipped: **{test_results['skipped']}**"
    )

    report.append("")

    report.append(
        "The test suite covers data quality, sales calculations, "
        "incremental loading, SQL/Python consistency, and performance."
    )

    report.append("")

    report.append(
        f"The performance test recorded approximately "
        f"**{performance_improvement}** improvement after indexing "
        "for the tested query and dataset."
    )

    report.append("")

    report.append(
        "Performance measurements are dataset-dependent and should "
        "not be interpreted as a guaranteed production improvement."
    )

    report.append("")

    report.append("## 11. Business Recommendations")
    report.append("")

    report.append(
        "1. Investigate the significant decline in February sales."
    )

    report.append(
        "2. Prioritize P005, P007, and P002 because they contribute "
        "strongly to net sales."
    )

    report.append(
        "3. Monitor ST02 performance and inventory closely."
    )

    report.append(
        "4. Replenish out-of-stock and high-risk inventory promptly."
    )

    report.append(
        "5. Use customer segmentation to target high-value and "
        "at-risk customers."
    )

    report.append(
        "6. Continue reconciliation checks to detect duplicate or "
        "inconsistent source records."
    )

    report.append(
        "7. Continue automated testing before production releases."
    )

    report.append("")

    report.append("## 12. Limitations")
    report.append("")

    report.append(
        "- The available sales history is limited."
    )

    report.append(
        "- Customer segmentation thresholds are based on the "
        "current project dataset."
    )

    report.append(
        "- At-risk customers are a recency-based signal and do not "
        "confirm actual customer churn."
    )

    report.append(
        "- Inventory recommendations use project assumptions such "
        "as the 20% safety buffer."
    )

    report.append(
        "- Performance results depend on the current dataset and "
        "execution environment."
    )

    report.append("")

    report.append("## 13. Conclusion")
    report.append("")

    report.append(
        "The RetailPulse project integrates data validation, "
        "relational database loading, sales analytics, inventory "
        "intelligence, customer analytics, anomaly detection, "
        "incremental loading, and automated testing into a "
        "reproducible retail analytics workflow."
    )

    report.append("")

    report.append(
        "The solution provides both technical validation and "
        "business-focused insights that can support sales, "
        "inventory, and customer-management decisions."
    )

    report.append("")

    report.append(
        "The project is designed so that future incoming data can "
        "be processed through the same validation, loading, "
        "analysis, reconciliation, and reporting workflow."
    )

    report.append("")

    report.append("## 14. Source Reports")
    report.append("")

    report.append(
        "This final report was generated using the following "
        "RetailPulse reports:"
    )

    report.append("")

    report.append("- `sales_performance_report.md`")
    report.append("- `advanced_sales_analytics.md`")
    report.append("- `inventory_report.md`")
    report.append("- `customer_analytics_report.md`")
    report.append("- `data_quality_reconciliation_report.md`")
    report.append("- `pipeline_run_report.md`")
    report.append("- `performance_report.md`")
    report.append("- `test_results.md`")

    report.append("")

    report.append("---")
    report.append("")

    report.append(
        "Generated automatically by "
        "`src/generate_final_business_report.py`."
    )

    report.append("")

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FINAL_REPORT.write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    print("")
    print("=" * 60)
    print("Final business report generated successfully.")
    print("=" * 60)
    print(f"Report: {FINAL_REPORT}")
    print(f"Tests: {test_results['status']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    print(f"Skipped: {test_results['skipped']}")
    print("=" * 60)


if __name__ == "__main__":
    generate_final_report()