"""
Configuration management for the auditBot application.
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "emailer" / "templates"

# Data file paths
CITIES_CSV = DATA_DIR / "cities.csv"
BUSINESSES_CSV = DATA_DIR / "businesses.csv"
SENT_BUSINESSES_CSV = DATA_DIR / "sent_businesses.csv"
RESPONSES_CSV = DATA_DIR / "responses.csv"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Email configuration
EMAIL_SUBJECT = "Business Opportunity"
DEFAULT_TEMPLATE = "template1.txt"

# Scraper configuration
SCRAPER_DELAY = 2  # seconds between requests
MAX_BUSINESSES_PER_CITY = 100  # limit per city to avoid overwhelming

# Gmail API configuration
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

# Categories for business search
BUSINESS_CATEGORIES = [
    "plumbers",
    "dentists",
    "electricians",
    "roofers",
    "HVAC contractors",
    "lawyers",
    "accountants",
    "real estate agents",
    "insurance agents",
    "financial advisors",
    "chiropractors",
    "veterinarians",
    "auto repair shops",
    "landscaping services",
    "cleaning services",
]

def get_env_variable(var_name, default=None):
    """Get environment variable with optional default."""
    return os.getenv(var_name, default)
