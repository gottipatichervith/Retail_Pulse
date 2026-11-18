
from src.logger import get_logger

logger = get_logger("RetailPulseTest")

logger.info("RetailPulse application started.")
logger.warning("This is a sample warning.")
logger.error("This is a sample error.")

print("\nLogging test completed.")
