# Setup Guide - Email Outreach Bot

Complete step-by-step guide to get the bot running.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [API Key Setup](#api-key-setup)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [First Run](#first-run)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Internet Connection**: Required for API calls
- **Disk Space**: ~100MB for installation, varies with database size

### Check Python Version
```bash
python --version
# or
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GreenKeewi/emailBot.git
cd emailBot
```

### 2. Create Virtual Environment (Recommended)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `python-dotenv` - Environment variable management
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `googlemaps` - Google Maps API client
- `google-generativeai` - Gemini API client
- `click` - CLI framework
- `rich` - Terminal formatting
- `validators` - URL/email validation
- Other utilities

### 4. Verify Installation

```bash
python validate.py
```

You should see all imports passing. Environment check will fail until you configure `.env`.

---

## API Key Setup

You'll need three API keys and one Gmail configuration.

### 1. Google Maps API Key

**Steps:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
   - Click "Select a project" → "New Project"
   - Name it (e.g., "EmailBot")
   - Click "Create"

3. Enable required APIs:
   - Go to "APIs & Services" → "Library"
   - Search for "Places API" → Enable
   - Search for "Maps JavaScript API" → Enable
   - Search for "Geocoding API" → Enable

4. Create API Key:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the key immediately

5. (Optional) Restrict the key:
   - Click on the key name
   - Under "API restrictions" → "Restrict key"
   - Select: Places API, Maps JavaScript API, Geocoding API
   - Save

**Cost**: Google provides $200/month free credit. Each Places API call costs ~$0.032.
Approximate cost for 1000 businesses: $30-50

### 2. Google Gemini API Key

**Steps:**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Select a project or create new
5. Copy the API key

**Cost**: Gemini has a generous free tier:
- 60 requests per minute
- 1,500 requests per day
- Free for moderate use

### 3. Gmail App Password

**Requirements:**
- Gmail account
- 2-Factor Authentication enabled

**Steps:**

1. Enable 2FA on your Google Account:
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Under "Signing in to Google" → "2-Step Verification"
   - Follow the setup wizard

2. Generate App Password:
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Enter name: "Email Outreach Bot"
   - Click "Generate"
   - Copy the 16-character password (no spaces)

**Important**: This is NOT your regular Gmail password. It's a special app-specific password.

---

## Configuration

### 1. Create .env File

```bash
cp .env.example .env
```

### 2. Edit .env File

Open `.env` in your favorite editor and fill in your values:

```bash
# Google Maps API
GOOGLE_MAPS_API_KEY=AIzaSyC_your_actual_key_here

# Gemini API  
GEMINI_API_KEY=AIzaSyD_your_actual_key_here

# Gmail SMTP
GMAIL_ADDRESS=your.email@gmail.com
GMAIL_APP_PASSWORD=abcdefghijklmnop

# Email Settings
FROM_NAME=Your Company Name
REPLY_TO_EMAIL=your.email@gmail.com

# Rate Limiting (emails per hour)
EMAILS_PER_HOUR=25

# Search Settings
SEARCH_RADIUS_METERS=5000
MAX_RESULTS_PER_SEARCH=60
```

**Configuration Options Explained:**

- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key
- `GEMINI_API_KEY`: Your Gemini API key  
- `GMAIL_ADDRESS`: The Gmail address to send FROM
- `GMAIL_APP_PASSWORD`: 16-char app password (NO SPACES)
- `FROM_NAME`: How you want to appear in emails
- `REPLY_TO_EMAIL`: Where replies should go
- `EMAILS_PER_HOUR`: Rate limit (recommended: 25-30)
- `SEARCH_RADIUS_METERS`: Search area radius (5000 = 5km)
- `MAX_RESULTS_PER_SEARCH`: Max businesses per search (max: 60)

### 3. Secure Your .env File

**CRITICAL**: Never commit `.env` to git!

The `.gitignore` file already excludes it, but verify:

```bash
cat .gitignore | grep .env
```

Should show: `.env`

---

## Testing

### 1. Run Validation

```bash
python validate.py
```

Expected output:
```
✓ PASS: Imports
✓ PASS: HistoryStore
✓ PASS: LocationManager
✓ PASS: Environment
```

### 2. Test API Connections

```bash
python run.py --province=Ontario --category=test --test
```

This tests:
- Gmail SMTP connection
- API key validity

Expected output:
```
Testing connections...

✓ Gmail SMTP connection successful
```

If this fails, double-check your credentials.

---

## First Run

### Start Small

For your first run, use a limit to avoid excessive API calls:

```bash
python run.py --province=Ontario --category=plumber --limit=5
```

This will:
1. Initialize search locations for Ontario plumbers
2. Search for businesses in the first city
3. Send up to 5 emails
4. Stop

### Monitor Output

You'll see:
```
============================================================
📍 Province: Ontario
🔍 Category: plumber
============================================================

🏙️  City: Toronto
📍 Location: (43.6532, -79.3832), Radius: 5000m
🔍 Searching for plumber businesses...
   Found 45 businesses
   [1/45] Joe's Plumbing - Generating email...
   ✓ Email sent (1 total)
   ...
```

### Check Status

```bash
python status.py --province=Ontario --category=plumber
```

Shows progress and statistics.

### View Database

The bot creates `outreach_bot.db` (SQLite database).

View with any SQLite browser:
```bash
sqlite3 outreach_bot.db
.tables
SELECT * FROM businesses LIMIT 5;
.quit
```

---

## Troubleshooting

### "Authentication error" when sending emails

**Cause**: Invalid Gmail credentials

**Solutions**:
1. Verify Gmail address is correct
2. Verify App Password is exactly 16 characters, no spaces
3. Ensure 2FA is enabled on Google account
4. Try generating a new App Password
5. Check if "Less secure app access" is NOT enabled (shouldn't be needed with App Password)

### "No module named..." errors

**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### "API key not valid" errors

**Cause**: Invalid or restricted API key

**Solutions**:
1. Verify API key is copied correctly (no extra spaces)
2. Check that APIs are enabled in Google Cloud Console
3. If key is restricted, ensure correct APIs are allowed
4. Try creating a new unrestricted key for testing

### "Rate limit reached"

**Cause**: Hit email sending limit

**Solution**:
This is normal! The bot will automatically wait. Or:
- Adjust `EMAILS_PER_HOUR` in `.env`
- Wait for the next hour
- Use `--limit` to control sends per run

### "No businesses found"

**Cause**: Search returned no results

**Solutions**:
1. Try a different category (more common one)
2. Try a different province/city
3. Check if Google Maps API quota is exceeded
4. Verify Places API is enabled

### Database locked

**Cause**: Multiple instances running or database viewer open

**Solutions**:
1. Ensure only one instance of the bot is running
2. Close any database browsers/viewers
3. Restart the bot

### Import errors after installation

**Cause**: Virtual environment not activated

**Solution**:
```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### "Permission denied" errors

**Cause**: Insufficient file permissions

**Solution**:
```bash
# Linux/macOS
chmod +x run.py status.py reset.py validate.py

# Windows - run as administrator if needed
```

---

## Next Steps

Once setup is complete:

1. **Start with a small run**: `--limit=10`
2. **Monitor the output**: Watch for errors
3. **Check your Gmail**: Verify emails are sending correctly
4. **Review emails sent**: Make sure they look good
5. **Gradually increase**: Remove `--limit` for full automation
6. **Use status command**: Track progress regularly
7. **Let it run**: Bot is restart-safe, stop and resume anytime

---

## Safety Tips

1. **Start slow**: Test with small limits first
2. **Monitor responses**: Check if you get replies
3. **Respect opt-outs**: Stop immediately if requested
4. **Stay compliant**: Follow CAN-SPAM, CASL, GDPR
5. **Watch quotas**: Monitor API usage in Google Cloud Console
6. **Keep backups**: Database is in `outreach_bot.db`
7. **Update regularly**: Keep dependencies updated

---

## Getting Help

If you encounter issues:

1. Check this guide first
2. Review error messages carefully
3. Check API quotas in Google Cloud Console
4. Verify all credentials in `.env`
5. Run `python validate.py` to check setup
6. Review logs and database for clues

---

## Success Checklist

- [ ] Python 3.8+ installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud project created
- [ ] Places API enabled
- [ ] Google Maps API key obtained
- [ ] Gemini API key obtained
- [ ] Gmail 2FA enabled
- [ ] Gmail App Password generated
- [ ] `.env` file created and configured
- [ ] `python validate.py` passes all tests
- [ ] `python run.py --test` succeeds
- [ ] First test run completed successfully

Once all items are checked, you're ready for production use! 🚀

---

**Last Updated**: 2026-01-02
