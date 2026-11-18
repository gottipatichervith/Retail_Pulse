
from pathlib import Path
from datetime import datetime

from src.logger import get_logger

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "known_issues_and_technical_debt.md"

logger = get_logger("RetailPulseTechnicalDebt")


def generate_report():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = [
        "# RetailPulse - Known Issues and Technical Debt",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 1. Known Limitations",
        "",
        "- Forecasting results are preliminary because the available "
        "historical sales data is limited.",
        "- Forecast accuracy should be reviewed when more historical "
        "sales data becomes available.",
        "- Performance benchmark results are based on the tested "
        "100,000-record dataset and current environment.",
        "- Peak memory usage and performance under larger workloads "
        "require further measurement.",
        "",
        "## 2. Technical Debt",
        "",
        "- Automated test coverage should be expanded across all "
        "pipeline components.",
        "- Retry handling currently focuses on temporary database "
        "lock and busy errors.",
        "- Monitoring should be extended with automated alerts.",
        "- Database query performance should be reviewed as data volume grows.",
        "- Configuration and deployment procedures should be reviewed "
        "before production deployment.",
        "",
        "## 3. Future Improvements",
        "",
        "- Add more automated integration and failure-recovery tests.",
        "- Introduce automated notifications for pipeline failures.",
        "- Perform larger-scale performance and memory testing.",
        "- Improve forecasting using a larger historical dataset.",
        "- Review database indexes using controlled benchmarks.",
        "- Add centralized monitoring and operational dashboards.",
        "",
        "## 4. Production Considerations",
        "",
        "- Protect production database files and credentials.",
        "- Verify backup and recovery procedures.",
        "- Test duplicate-file and interrupted-run scenarios.",
        "- Review logs and monitoring reports regularly.",
        "- Complete final validation before production release.",
        "",
        "## 5. Review Status",
        "",
        "This report records known limitations and recommended improvements.",
        "Items should be verified against the current implementation "
        "before being treated as confirmed defects.",
        "",
    ]

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    logger.info("Technical debt report generated: %s", REPORT_FILE)

    print("Technical debt report generated successfully.")
    print(f"Report location: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
