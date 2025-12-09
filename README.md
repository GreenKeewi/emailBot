# AuditBot - Business Scraping and Email Automation Tool

A production-ready Python command-line tool for discovering and contacting businesses across North American cities. The system scrapes Google Maps for businesses in various categories, validates their contact information, and sends customizable emails via Gmail API.

## Features

✅ **City Management**
- Process cities one at a time or in batches
- Automatic tracking of completed cities
- Progress monitoring and analytics

✅ **Business Discovery**
- Multi-category business search
- Email and website validation
- Automatic deduplication

✅ **Email Automation**
- Gmail API integration (OAuth2)
- Multiple customizable templates
- Immediate sending upon discovery

✅ **Analytics & Reporting**
- Overall statistics
- Per-city breakdowns
- Top-performing categories
- Response tracking
- CSV export capabilities

## Table of Contents

- [Installation](#installation)
- [Gmail API Setup](#gmail-api-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [CLI Commands](#cli-commands)
- [Project Structure](#project-structure)
- [Data Files](#data-files)
- [Optional Enhancements](#optional-enhancements)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Cloud account (for Gmail API)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/GreenKeewi/auditBot.git
   cd auditBot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

5. **Set up data files**
   ```bash
   # Copy example files to create initial data files
   cp data/cities.csv.example data/cities.csv
   cp data/businesses.csv.example data/businesses.csv
   cp data/sent_businesses.csv.example data/sent_businesses.csv
   cp data/responses.csv.example data/responses.csv
   ```

6. **Configure Gmail API** (See [Gmail API Setup](#gmail-api-setup) section)

## Gmail API Setup

Detailed instructions can be found in [SETUP.md](SETUP.md). Quick overview:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Save it as `credentials.json` in the project root directory
7. On first run, the application will open a browser for authentication
8. Authorize the application - this creates `token.json` for future use

**Note:** Never commit `credentials.json` or `token.json` to version control!

## Configuration

### Edit Business Categories

Edit `scraper/categories.py` to customize the business categories:

```python
CATEGORIES = [
    "plumbers",
    "dentists",
    "electricians",
    # Add your categories here
]
```

### Edit Email Templates

Templates are located in `emailer/templates/`:
- `template1.txt` - Default business opportunity template
- `template2.txt` - Marketing offer template

Create new templates by adding `.txt` files to this directory. Format:

```
Subject: Your Subject Line Here

Email body goes here.
Use {business_name} for personalization.
```

### Modify Configuration

Edit `config.py` to adjust:
- `SCRAPER_DELAY` - Delay between requests (seconds)
- `MAX_BUSINESSES_PER_CITY` - Maximum businesses per city
- `EMAIL_SUBJECT` - Default email subject
- `DEFAULT_TEMPLATE` - Default template file

## Usage

### Basic Commands

```bash
# Process one city
python main.py --uno

# Process 5 cities
python main.py --run 5

# Process with custom template
python main.py --template template2.txt --run 3

# Show overall statistics
python main.py --stats

# Show per-city statistics
python main.py --city-stats

# Show top categories
python main.py --top-categories

# Log a business response
python main.py --log-response business@example.com --notes "Interested in service"

# Export summary report
python main.py --export-summary
```

## CLI Commands

### City Processing

| Command | Description | Example |
|---------|-------------|---------|
| `--uno` | Process one unprocessed city | `python main.py --uno` |
| `--run N` | Process N cities in order | `python main.py --run 10` |
| `--template FILE` | Use custom email template | `python main.py --template template2.txt --uno` |

### Analytics

| Command | Description | Example |
|---------|-------------|---------|
| `--stats` | Show overall statistics | `python main.py --stats` |
| `--city-stats` | Show per-city breakdown | `python main.py --city-stats` |
| `--top-categories` | Show top categories by emails sent | `python main.py --top-categories` |

### Response Management

| Command | Description | Example |
|---------|-------------|---------|
| `--log-response EMAIL` | Log a business response | `python main.py --log-response email@test.com` |
| `--notes TEXT` | Add notes to response | `python main.py --log-response email@test.com --notes "Very interested"` |

### Reporting

| Command | Description | Example |
|---------|-------------|---------|
| `--export-summary` | Export metrics to CSV | `python main.py --export-summary` |

## Project Structure

```
auditBot/
│
├── main.py                      # Main CLI application
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── SETUP.md                     # Detailed Gmail setup guide
├── .gitignore                   # Git ignore rules
│
├── data/                        # Data storage (excluded from git)
│   ├── cities.csv              # Master cities list
│   ├── businesses.csv          # All discovered businesses
│   ├── sent_businesses.csv     # Sent email log
│   ├── responses.csv           # Business responses log
│   └── *.csv.example           # Example/template files
│
├── scraper/                     # Web scraping module
│   ├── maps_scraper.py         # Google Maps scraper
│   └── categories.py           # Business categories
│
├── emailer/                     # Email module
│   ├── gmail_service.py        # Gmail API integration
│   └── templates/              # Email templates
│       ├── template1.txt       # Default template
│       └── template2.txt       # Alternative template
│
└── analytics/                   # Analytics module
    ├── stats.py                # Statistics calculator
    └── reports.py              # Report generator
```

## Data Files

### cities.csv
Tracks all cities and their processing status.

```csv
city,state,country,completed
New York,New York,USA,false
Los Angeles,California,USA,true
```

### businesses.csv
Stores all discovered businesses.

```csv
name,website,email,phone,category,city,state,country,status
ABC Plumbing,http://abc.com,info@abc.com,555-1234,plumbers,New York,New York,USA,new
```

### sent_businesses.csv
Logs all sent emails.

```csv
name,email,city,category,date_sent
ABC Plumbing,info@abc.com,New York,plumbers,2024-01-15 10:30:00
```

### responses.csv
Tracks business responses.

```csv
email,date,notes
info@abc.com,2024-01-16 14:20:00,Interested in service
```

## Optional Enhancements

### 1. Proxy Rotation

To avoid IP blocking, implement proxy rotation:

```python
# In scraper/maps_scraper.py
PROXIES = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
]

# Use with Playwright
self.browser = await playwright.chromium.launch(
    proxy={'server': random.choice(PROXIES)}
)
```

### 2. CAPTCHA Bypass

Consider using services like:
- 2Captcha
- Anti-Captcha
- Death By Captcha

### 3. Retry Logic

Implement exponential backoff for failed requests:

```python
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
```

### 4. Dashboard

Create a web dashboard using:
- **Flask/FastAPI** for backend
- **Chart.js** or **Plotly** for visualizations
- **Bootstrap** for UI

Example structure:
```python
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Load data
    df = pd.read_csv('data/sent_businesses.csv')
    # Generate statistics
    stats = calculate_stats(df)
    return render_template('dashboard.html', stats=stats)
```

### 5. Advanced Email Finding

Integrate with:
- Hunter.io API
- Clearbit API
- Custom website crawling with BeautifulSoup

### 6. Rate Limiting

Implement rate limiting to avoid triggering anti-bot measures:

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def search_business():
    # Your scraping code
    pass
```

## Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Ensure `credentials.json` is in the project root
   - Verify you've completed Gmail API setup

2. **"Browser not installed"**
   - Run: `playwright install chromium`

3. **"No unprocessed cities remaining"**
   - Check `data/cities.csv` and reset `completed` column to `false`
   - Add more cities to the file

4. **Email sending fails**
   - Verify Gmail API is enabled
   - Check internet connection
   - Ensure OAuth token is valid

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and commercial purposes.

## Disclaimer

⚠️ **Important:**
- Respect website Terms of Service when scraping
- Comply with anti-spam laws (CAN-SPAM, GDPR, CASL)
- Use responsibly and ethically
- Ensure proper authentication and authorization
- Be aware of rate limits and API usage restrictions

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review the code comments and docstrings

---

**Happy Automating! 🚀**
