
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Read the environment name first
load_dotenv(BASE_DIR / "config" / ".env", override=False)

APP_ENV = os.getenv("APP_ENV", "development")

# Select the correct configuration file
if APP_ENV == "production":
    ENV_FILE = BASE_DIR / "config" / ".env.production"
elif APP_ENV == "development":
    ENV_FILE = BASE_DIR / "config" / ".env"
else:
    raise ValueError("APP_ENV must be development or production.")

# Load selected settings
load_dotenv(ENV_FILE, override=True)

DATABASE_PATH = os.getenv("DATABASE_PATH")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "200"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

if not DATABASE_PATH:
    raise ValueError("DATABASE_PATH is missing.")

DATABASE_FILE = BASE_DIR / DATABASE_PATH

if BATCH_SIZE <= 0:
    raise ValueError("BATCH_SIZE must be greater than zero.")

if MAX_RETRIES < 0:
    raise ValueError("MAX_RETRIES cannot be negative.")
