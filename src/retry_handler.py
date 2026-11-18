
import sqlite3
import time

from src.config import MAX_RETRIES
from src.logger import get_logger

logger = get_logger("RetailPulseRetry")


def execute_with_retry(operation):
    """
    Retry an operation when SQLite is temporarily busy or locked.
    """

    for attempt in range(MAX_RETRIES + 1):

        try:
            return operation()

        except sqlite3.OperationalError as error:

            error_message = str(error).lower()

            temporary_error = (
                "locked" in error_message
                or "busy" in error_message
            )

            if not temporary_error:
                raise

            if attempt >= MAX_RETRIES:
                logger.exception(
                    "Operation failed after %s retries.",
                    MAX_RETRIES
                )
                raise

            wait_time = 2 ** attempt

            logger.warning(
                "Database temporarily busy. Retry %s of %s "
                "after %s seconds.",
                attempt + 1,
                MAX_RETRIES,
                wait_time
            )

            time.sleep(wait_time)
