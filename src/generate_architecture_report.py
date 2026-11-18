
from pathlib import Path
from datetime import datetime

from src.logger import get_logger

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "architecture_documentation.md"

logger = get_logger("RetailPulseArchitecture")


def get_project_structure():

    excluded = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        ".idea"
    }

    lines = []

    for path in sorted(BASE_DIR.rglob("*")):

        if any(part in excluded for part in path.relative_to(BASE_DIR).parts):
            continue

        relative_path = path.relative_to(BASE_DIR)

        if path.is_dir():
            lines.append(f"- `{relative_path}/`")
        elif path.is_file():
            lines.append(f"- `{relative_path}`")

    return lines


def get_python_files():

    python_files = []

    for path in sorted((BASE_DIR / "src").glob("*.py")):

        if path.is_file():
            python_files.append(path.name)

    return python_files


def generate_report():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    structure = get_project_structure()
    python_files = get_python_files()

    report = [
        "# RetailPulse Architecture Documentation",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 1. Project Overview",
        "",
        "RetailPulse is a retail sales and inventory intelligence system.",
        "It supports data cleaning, database loading, batch ingestion,",
        "data quality monitoring, sales analysis, demand forecasting,",
        "and inventory recommendations.",
        "",
        "## 2. Project Structure",
        "",
        "The following structure was collected automatically from the project:",
        "",
        *structure,
        "",
        "## 3. Python Source Files",
        "",
        "The following Python files were found in the src folder:",
        "",
    ]

    if python_files:
        report.extend([f"- `{name}`" for name in python_files])
    else:
        report.append("- No Python files found.")

    report.extend([
        "",
        "## 4. Main System Components",
        "",
        "| Component | Responsibility |",
        "|---|---|",
        "| Configuration | Stores environment-specific settings |",
        "| Data ingestion | Reads and processes incoming sales files |",
        "| Database | Stores retail sales information |",
        "| Logging | Records pipeline activities and errors |",
        "| Monitoring | Tracks pipeline execution and data quality |",
        "| Reporting | Generates performance and monitoring reports |",
        "| Forecasting | Estimates future product demand |",
        "| Inventory | Supports stock recommendations |",
        "",
        "## 5. Data Flow",
        "",
        "1. Incoming CSV files are received.",
        "2. Data is validated and processed.",
        "3. Valid records are loaded into the database.",
        "4. Audit information and checkpoints are maintained.",
        "5. Monitoring and reports summarize pipeline activity.",
        "6. Analytical and forecasting components use stored data.",
        "",
        "## 6. Configuration and Security",
        "",
        "- Development and production settings are separated.",
        "- Environment settings are loaded from configuration files.",
        "- Database paths and batch settings are configurable.",
        "- Sensitive credentials should not be committed to Git.",
        "- Local environment files should be protected using `.gitignore`.",
        "",
        "## 7. Reliability",
        "",
        "- Batch processing supports large input files.",
        "- Checkpoints support restarting interrupted processing.",
        "- Logging records important pipeline events.",
        "- Retry handling supports temporary database lock errors.",
        "",
        "## 8. Architecture Review Notes",
        "",
        "This report describes the detected project structure and the",
        "intended responsibilities of its main components.",
        "A source-code review is still required to confirm implementation",
        "details, identify duplicated logic, and verify all dependencies.",
        "",
    ])

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    logger.info("Architecture report generated: %s", REPORT_FILE)

    print("Architecture documentation generated successfully.")
    print(f"Report location: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
