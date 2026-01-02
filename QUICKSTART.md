# Quick Reference Guide

Fast reference for common commands and workflows.

## Installation (One-Time Setup)

```bash
git clone https://github.com/GreenKeewi/emailBot.git
cd emailBot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python validate.py
```

## Daily Usage

### Start the Bot

```bash
# Full province run
python run.py --province=Ontario --category=plumber

# Limited run (for testing)
python run.py --province=Ontario --category=plumber --limit=10

# Different province
python run.py --province=Quebec --category=electrician
```

### Check Progress

```bash
python status.py --province=Ontario --category=plumber
```

### Reset Data

```bash
python reset.py --province=Ontario --category=plumber --confirm
```

## Supported Provinces & Categories

### Provinces
- `Ontario` (45 cities)
- `Quebec` (5 cities)
- `British Columbia` (5 cities)
- `Alberta` (4 cities)

### Example Categories
- `plumber`
- `electrician`
- `dentist`
- `restaurant`
- `lawyer`
- `accountant`
- `contractor`
- `landscaper`
- `mechanic`
- `realtor`

Any valid Google Maps category works!

## CLI Options

### run.py
```bash
--province PROVINCE   # Required: Province name
--category CATEGORY   # Required: Business category
--limit NUMBER       # Optional: Max emails to send
--test              # Optional: Test connections only
```

### status.py
```bash
--province PROVINCE   # Required: Province name
--category CATEGORY   # Optional: Category filter
```

### reset.py
```bash
--province PROVINCE   # Required: Province name
--category CATEGORY   # Required: Category to reset
--confirm            # Optional: Skip confirmation prompt
```

## Environment Variables (.env)

```bash
GOOGLE_MAPS_API_KEY=your_key       # Required
GEMINI_API_KEY=your_key            # Required
GMAIL_ADDRESS=your@email.com       # Required
GMAIL_APP_PASSWORD=16chars         # Required
FROM_NAME=Your Company             # Required
REPLY_TO_EMAIL=your@email.com     # Required
EMAILS_PER_HOUR=25                # Optional (default: 25)
SEARCH_RADIUS_METERS=5000         # Optional (default: 5000)
MAX_RESULTS_PER_SEARCH=60         # Optional (default: 60)
```

## Common Workflows

### First Time Setup
1. Get API keys (see SETUP.md)
2. Configure .env
3. Run `python validate.py`
4. Test: `python run.py --province=Ontario --category=test --limit=1`

### Regular Operation
1. Start: `python run.py --province=Ontario --category=plumber`
2. Monitor: Watch console output
3. Check progress: `python status.py --province=Ontario --category=plumber`
4. Stop: Ctrl+C (safe to interrupt)
5. Resume: Run same command again

### Troubleshooting
```bash
# Test connections
python run.py --test

# Verify setup
python validate.py

# Check database
sqlite3 outreach_bot.db
.tables
SELECT COUNT(*) FROM businesses;
.quit

# View recent businesses
sqlite3 outreach_bot.db "SELECT name, email, email_sent FROM businesses LIMIT 10;"
```

## File Locations

- **Database**: `outreach_bot.db` (created on first run)
- **Config**: `.env` (you create from .env.example)
- **Logs**: Console output only (no log files)

## Quick Commands

```bash
# Activate environment
source venv/bin/activate

# Run bot
python run.py --province=Ontario --category=plumber

# Check status
python status.py --province=Ontario --category=plumber

# Test connection
python run.py --test

# Validate setup
python validate.py

# Update dependencies
pip install -r requirements.txt --upgrade

# Deactivate environment
deactivate
```

## Database Queries

```sql
-- Count total businesses
SELECT COUNT(*) FROM businesses;

-- Count by province
SELECT province, COUNT(*) FROM businesses GROUP BY province;

-- Count emails sent
SELECT COUNT(*) FROM businesses WHERE email_sent = 1;

-- View recent businesses
SELECT name, city, email, email_sent FROM businesses ORDER BY created_at DESC LIMIT 10;

-- Check search progress
SELECT city, status, COUNT(*) FROM searches GROUP BY city, status;

-- View run history
SELECT * FROM runs ORDER BY run_timestamp DESC LIMIT 5;
```

## Rate Limits

- **Gmail**: 25 emails/hour (default, adjustable in .env)
- **Google Maps**: Check your quota in Cloud Console
- **Gemini**: 60 requests/minute (free tier)

Bot automatically handles rate limiting and will wait when needed.

## Tips

1. **Start Small**: Use `--limit=10` for first runs
2. **Monitor Closely**: Watch for errors in console
3. **Check Status Often**: Use status.py to track progress
4. **Safe to Stop**: Ctrl+C anytime, resume later
5. **Multiple Categories**: Run different categories sequentially
6. **Backup Database**: Copy `outreach_bot.db` periodically
7. **Watch Quotas**: Monitor API usage in Google Cloud Console
8. **Test Emails**: Check your sent folder to see actual emails

## Error Messages

| Error | Solution |
|-------|----------|
| "Authentication error" | Check Gmail App Password in .env |
| "No module named..." | Run `pip install -r requirements.txt` |
| "API key not valid" | Verify API keys in .env |
| "Rate limit reached" | Normal - bot will wait automatically |
| "No businesses found" | Try different category or check API quota |
| "Database locked" | Close other instances or DB viewers |

## Support

- Read SETUP.md for detailed installation
- Read ARCHITECTURE.md for system design
- Read EXAMPLES.md for email samples
- Check validate.py output for issues

## Quick Test

```bash
# After setup, test everything:
python validate.py
python run.py --test
python run.py --province=Ontario --category=plumber --limit=1
python status.py --province=Ontario --category=plumber
```

If all commands succeed, you're ready!

---

**Remember**: This bot sends real emails. Always:
- Start with small limits
- Monitor the output
- Check sent emails
- Respect opt-outs
- Follow compliance laws
