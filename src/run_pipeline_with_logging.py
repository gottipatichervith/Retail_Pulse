
from src.ingestion_pipeline import (
    INCOMING_DIR,
    process_file_in_batches
)
from src.retry_handler import process_file_with_retry
from src.logger import get_logger

logger = get_logger("RetailPulsePipeline")


def main():
    logger.info("RetailPulse pipeline started.")

    csv_files = sorted(INCOMING_DIR.glob("*.csv"))

    if not csv_files:
        logger.warning("No CSV files found in incoming folder.")
        return

    for file_path in csv_files:

        logger.info("Starting file: %s", file_path.name)

        result = process_file_with_retry(
            process_file_in_batches,
            file_path
        )

        if result and result.get("status") == "SUCCESS":
            logger.info("File completed: %s", file_path.name)
        else:
            logger.error("File failed: %s", file_path.name)

    logger.info("RetailPulse pipeline execution finished.")


if __name__ == "__main__":
    main()
