import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"

TEST_REPORT_PATH = REPORTS_DIR / "test_results.md"
PERFORMANCE_REPORT_PATH = REPORTS_DIR / "performance_report.md"


def run_tests():
    """Run the complete pytest test suite and return the output."""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(PROJECT_ROOT)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
            "-s",
            "--disable-warnings",
        ],
        cwd=str(PROJECT_ROOT),
        env=environment,
        capture_output=True,
        text=True,
    )

    return result


def extract_test_summary(output):
    """Extract the pytest summary from the test output."""
    match = re.search(
        r"(\d+) passed"
        r"(?:,\s*(\d+) failed)?"
        r"(?:,\s*(\d+) skipped)?"
        r"(?:,\s*(\d+) error)?"
        r"\s+in\s+([\d.]+)s",
        output,
    )

    if not match:
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
            "execution_time": 0,
        }

    passed = int(match.group(1))
    failed = int(match.group(2) or 0)
    skipped = int(match.group(3) or 0)
    errors = int(match.group(4) or 0)
    execution_time = float(match.group(5))

    total = passed + failed + skipped + errors

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "execution_time": execution_time,
    }


def extract_performance_metrics(output):
    """Extract before/after index timings from pytest output."""
    before_match = re.search(
        r"Query time before index:\s*([\d.]+)\s*seconds",
        output,
    )

    after_match = re.search(
        r"Query time after index:\s*([\d.]+)\s*seconds",
        output,
    )

    if not before_match or not after_match:
        return None

    before_time = float(before_match.group(1))
    after_time = float(after_match.group(1))

    if before_time > 0:
        improvement = ((before_time - after_time) / before_time) * 100
    else:
        improvement = 0

    return {
        "before_index": before_time,
        "after_index": after_time,
        "improvement": improvement,
    }


def generate_test_report(summary, run_time):
    """Generate the automated test results report."""
    status = "PASSED" if summary["failed"] == 0 and summary["errors"] == 0 else "FAILED"

    report = f"""# RetailPulse — Test Results

## Test Run Summary

- **Run time:** {run_time}
- **Python version:** {sys.version.split()[0]}
- **Operating system:** {os.name}
- **Total tests:** {summary["total"]}
- **Passed:** {summary["passed"]}
- **Failed:** {summary["failed"]}
- **Skipped:** {summary["skipped"]}
- **Collection/runtime errors:** {summary["errors"]}
- **Execution time:** {summary["execution_time"]:.4f} seconds
- **Overall status:** {status}

## Test Coverage

- Data quality validation
- Sales calculations
- Incremental loading
- SQL/Python consistency
- Performance measurement

## Important Notes

Passing tests show that the tested scenarios behaved as expected.

Passing tests do not prove that every possible production scenario is correct.

Test results depend on the test data and scenarios included in the test suite.
"""

    TEST_REPORT_PATH.write_text(report, encoding="utf-8")


def generate_performance_report(metrics, run_time):
    """Generate the automated performance report."""
    if metrics is None:
        report = f"""# RetailPulse — Performance Report

- **Run time:** {run_time}

## Performance Results

Performance metrics were not generated during this test run.
Check whether `tests/test_performance.py` completed successfully.
"""
    else:
        report = f"""# RetailPulse — Performance Report

- **Run time:** {run_time}

## Performance Results

| Metric | Result |
|---|---:|
| Query time before index | {metrics["before_index"]:.6f} seconds |
| Query time after index | {metrics["after_index"]:.6f} seconds |
| Improvement | {metrics["improvement"]:.2f}% |

## Interpretation

The indexed query completed faster than the query without the index in this test run.

The measured improvement was **{metrics["improvement"]:.2f}%**.

This performance result is based on the test dataset and one execution run. Query timings can vary depending on system load, database size, hardware, and other runtime conditions.

Therefore, the measured improvement should be treated as a benchmark for this test scenario rather than a guaranteed production improvement.
"""

    PERFORMANCE_REPORT_PATH.write_text(report, encoding="utf-8")


def main():
    """Run tests and generate both Markdown reports."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Running RetailPulse test suite...")

    result = run_tests()

    combined_output = result.stdout + "\n" + result.stderr

    summary = extract_test_summary(combined_output)
    metrics = extract_performance_metrics(combined_output)

    generate_test_report(summary, run_time)
    generate_performance_report(metrics, run_time)

    print("\nTest suite completed.")

    print(f"Tests passed: {summary['passed']}")
    print(f"Tests failed: {summary['failed']}")
    print(f"Tests skipped: {summary['skipped']}")
    print(f"Execution time: {summary['execution_time']:.4f} seconds")

    if metrics:
        print(
            f"Performance before index: "
            f"{metrics['before_index']:.6f} seconds"
        )
        print(
            f"Performance after index: "
            f"{metrics['after_index']:.6f} seconds"
        )
        print(
            f"Performance improvement: "
            f"{metrics['improvement']:.2f}%"
        )

    print(f"\nTest report: {TEST_REPORT_PATH}")
    print(f"Performance report: {PERFORMANCE_REPORT_PATH}")

    if result.returncode != 0:
        print("\nSome tests failed. Check the test output above.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()