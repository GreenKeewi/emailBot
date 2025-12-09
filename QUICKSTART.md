# Quick Start Guide for AuditBot

This guide will help you get started with AuditBot quickly.

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip package manager
- [ ] Google Cloud account (for Gmail API)

## Installation (5 minutes)

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### 2. Set Up Data Files

```bash
# Copy example files to create initial data
cp data/cities.csv.example data/cities.csv
cp data/businesses.csv.example data/businesses.csv
cp data/sent_businesses.csv.example data/sent_businesses.csv
cp data/responses.csv.example data/responses.csv
```

### 3. Configure Gmail API

Follow the detailed instructions in [SETUP.md](SETUP.md) to:
1. Create a Google Cloud project
2. Enable Gmail API
3. Create OAuth credentials
4. Download `credentials.json` to project root

## Quick Test (No Gmail Required)

Test the system with sample data (no email sending):

```bash
# Add test data
python test_setup.py

# View statistics
python main.py --stats

# View per-city breakdown
python main.py --city-stats

# View top categories
python main.py --top-categories

# Log a test response
python main.py --log-response test@example.com --notes "Interested"

# Export summary report
python main.py --export-summary
```

## Basic Usage

### Process Cities

```bash
# Process one city (requires Gmail API setup)
python main.py --uno

# Process 5 cities
python main.py --run 5

# Process with custom email template
python main.py --template template2.txt --run 3
```

### View Analytics

```bash
# Overall statistics
python main.py --stats

# Per-city breakdown
python main.py --city-stats

# Top performing categories
python main.py --top-categories
```

### Manage Responses

```bash
# Log a business response
python main.py --log-response business@example.com --notes "Very interested in service"

# Export all data to CSV
python main.py --export-summary
```

## Customization

### Add/Edit Business Categories

Edit `scraper/categories.py`:

```python
CATEGORIES = [
    "plumbers",
    "dentists",
    # Add your categories here
    "yoga studios",
    "coffee shops",
]
```

### Create Custom Email Templates

Create a new file in `emailer/templates/` (e.g., `my_template.txt`):

```
Subject: Your Custom Subject for {business_name}

Hello {business_name},

Your custom email body here.

Best regards,
Your Name
```

Use it with:
```bash
python main.py --template my_template.txt --uno
```

### Add More Cities

Edit `data/cities.csv`:

```csv
city,state,country,completed
Your City,Your State,USA,false
Another City,Province,Canada,false
```

## Common Workflows

### Workflow 1: Daily Batch Processing

```bash
# Morning: Process 10 cities
python main.py --run 10

# Evening: Check results
python main.py --stats
python main.py --export-summary
```

### Workflow 2: Test Run

```bash
# Process one city to test
python main.py --uno

# Review stats
python main.py --stats

# If satisfied, process more
python main.py --run 5
```

### Workflow 3: Analytics Review

```bash
# View overall performance
python main.py --stats

# Identify top-performing categories
python main.py --top-categories

# Check city-by-city results
python main.py --city-stats

# Export for external analysis
python main.py --export-summary
```

## Troubleshooting

### Error: "Credentials file not found"

**Solution:** Complete Gmail API setup (see SETUP.md)

### Error: "No unprocessed cities remaining"

**Solution:** Edit `data/cities.csv` and set `completed` to `false` for cities you want to process

### Stats showing 0

**Solution:** Run `python test_setup.py` to add sample data for testing

### Browser not installed

**Solution:** Run `playwright install chromium`

## Production Best Practices

1. **Start Small**: Process 1-2 cities first to test
2. **Monitor Results**: Check `--stats` regularly
3. **Backup Data**: Copy CSV files regularly
4. **Respect Limits**: Don't process too many cities at once
5. **Track Responses**: Use `--log-response` when businesses reply
6. **Review Analytics**: Use `--export-summary` for weekly reports

## Next Steps

- [ ] Complete Gmail API setup (if not done)
- [ ] Add/customize business categories
- [ ] Customize email templates
- [ ] Add more cities to your list
- [ ] Process your first city
- [ ] Monitor and optimize based on results

## Support

- Check [README.md](README.md) for detailed documentation
- Review [SETUP.md](SETUP.md) for Gmail API help
- Check code comments for technical details

---

**You're ready to start! 🚀**

Run `python main.py --help` to see all available commands.
