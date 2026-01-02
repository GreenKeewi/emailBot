# Email Outreach Bot 🤖

A sophisticated, stateful CLI-driven email outreach system that systematically discovers, contacts, and tracks businesses across entire provinces without duplicates.

## 🧠 Core Concept

This bot behaves like a **crawler with memory**:
- ✅ Remembers what it has already scraped
- ✅ Remembers what it has already emailed
- ✅ Automatically moves to new cities and locations
- ✅ Detects when an entire province is completed
- ✅ Never repeats work unless explicitly reset

## 🌟 Features

- **Province-Wide Coverage**: Systematically covers all major cities and towns
- **Smart Grid Search**: Breaks down large cities into overlapping search grids
- **Persistent State**: SQLite database tracks all progress
- **Email Extraction**: Automatically finds contact emails from business websites
- **Website Analysis**: Identifies UX and design improvement opportunities
- **AI-Powered Emails**: Uses Google Gemini to generate personalized outreach
- **Rate Limiting**: Built-in throttling (20-30 emails/hour)
- **Restart Safe**: Can stop and resume without duplicates
- **Progress Tracking**: Real-time CLI output and status commands

## 📋 Prerequisites

- Python 3.8+
- Google Maps API key (with Places API enabled)
- Google Gemini API key
- Gmail account with App Password enabled

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/GreenKeewi/emailBot.git
cd emailBot
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
# Google Maps API
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail SMTP
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password

# Email Settings
FROM_NAME=Your Company Name
REPLY_TO_EMAIL=your_email@gmail.com

# Rate Limiting
EMAILS_PER_HOUR=25

# Search Settings
SEARCH_RADIUS_METERS=5000
MAX_RESULTS_PER_SEARCH=60
```

### 🔑 Getting API Keys

**Google Maps API**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "Places API" and "Maps JavaScript API"
4. Create credentials → API Key
5. Restrict key (optional but recommended)

**Gemini API**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key

**Gmail App Password**:
1. Enable 2-Factor Authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use the 16-character password (no spaces)

## 📖 Usage

### Run the Bot

```bash
python run.py --province=Ontario --category=plumber
```

**Options**:
- `--province`: Province name (Ontario, Quebec, British Columbia, Alberta)
- `--category`: Business category (plumber, electrician, dentist, restaurant, etc.)
- `--limit`: Optional limit on emails to send (e.g., `--limit=50`)
- `--test`: Test connections without running

**Example**:
```bash
python run.py --province=Ontario --category=electrician --limit=100
```

### Check Status

```bash
python status.py --province=Ontario --category=plumber
```

Shows:
- Province completion status
- Total businesses found
- Emails sent
- Search areas completed/pending
- Progress percentage

### Reset Data

```bash
python reset.py --province=Ontario --category=plumber --confirm
```

Deletes all data for the specified province and category, allowing you to start fresh.

## 🎯 CLI Output Example

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
   [2/45] Quick Fix Plumbing - No email found
   [3/45] Metro Plumbers - Generating email...
   ✓ Email sent (2 total)
   ...
⏳ Search status: COMPLETE

============================================================
📊 RUN SUMMARY
============================================================
Cities processed: 1
Businesses discovered: 45
Emails sent: 17
Errors: 0
============================================================
```

## 🏗️ Architecture

```
emailBot/
├── history_store.py      # SQLite database management
├── location_manager.py   # Province/city data and grid generation
├── scraper.py           # Google Maps API and email extraction
├── site_analyzer.py     # Website analysis and UX assessment
├── ai_writer.py         # Gemini AI email generation
├── mailer.py           # Gmail SMTP with rate limiting
├── orchestrator.py     # Main coordination logic
├── run.py             # Main CLI entry point
├── status.py          # Status checking CLI
├── reset.py           # Data reset CLI
├── requirements.txt   # Python dependencies
├── .env.example      # Environment template
└── README.md         # This file
```

## 📊 Database Schema

**searches** table:
- Tracks search locations and completion status
- Fields: province, city, category, latitude, longitude, radius, status

**businesses** table:
- Stores discovered businesses
- Fields: name, website, email, city, category, province, email_sent

**runs** table:
- Tracks execution history
- Fields: timestamp, province, category, businesses_discovered, emails_sent

## ✉️ Email Generation

Emails are personalized using Google Gemini AI and include:
- Business name and city reference
- Industry-specific context
- Website observations (if available)
- Arc UI pitch: $99/month for full web service
- Soft call-to-action
- Unsubscribe line

### Example Email

```
Subject: Quick question about Joe's Plumbing's website

Hi Joe's Plumbing team,

I came across your plumbing business in Toronto and wanted to reach out.

I visited your website and noticed a few areas where it could be improved:
• No mobile viewport meta tag - site may not be mobile-friendly
• Limited or unclear calls-to-action (CTAs)

We provide a complete web solution for $99/month that includes:
• Modern, professional website design
• Reliable hosting
• Regular updates and maintenance
• Everything handled for you

Many plumbing businesses in Toronto work with us to strengthen their 
online presence without the hassle of managing it themselves.

Would you be open to a quick conversation about how we could help 
Joe's Plumbing?

Best regards,
Arc UI Team
https://arc-ui.vercel.app/

---
To unsubscribe, reply with 'unsubscribe' in the subject line.
```

## 🔒 Security & Best Practices

- ✅ Uses Gmail App Passwords (never stores main password)
- ✅ Environment variables in `.env` (never committed)
- ✅ Rate limiting to avoid spam flags
- ✅ Unsubscribe option in every email
- ✅ Input validation and error handling
- ✅ Connection testing before execution

## 🛠️ Troubleshooting

**"Authentication error"**:
- Verify Gmail App Password is correct (16 characters, no spaces)
- Ensure 2FA is enabled on Google account

**"No businesses found"**:
- Check Google Maps API key and quota
- Verify Places API is enabled
- Try a different category or city

**"Rate limit reached"**:
- Normal behavior - bot will wait automatically
- Adjust `EMAILS_PER_HOUR` in `.env` if needed

**Database locked**:
- Ensure only one instance is running
- Close any database viewers

## 🔄 Smart Progression

The bot automatically:
1. Loads all cities for a province
2. Generates search grids for each city
3. Processes locations in order
4. Skips already-contacted businesses
5. Marks areas complete when exhausted
6. Moves to next city automatically
7. Detects province completion

## 📈 Supported Provinces

- **Ontario**: 45 cities (Toronto, Ottawa, Mississauga, etc.)
- **Quebec**: 5 major cities (Montreal, Quebec City, etc.)
- **British Columbia**: 5 major cities (Vancouver, Surrey, etc.)
- **Alberta**: 4 major cities (Calgary, Edmonton, etc.)

To add more provinces, edit `location_manager.py` and add city data to `PROVINCE_DATA`.

## 🧪 Testing

Test connections without sending emails:
```bash
python run.py --province=Ontario --category=test --test
```

## 📝 Notes

- First run initializes all search locations (may take a moment)
- Large cities get multiple overlapping search grids
- Duplicate businesses are automatically filtered
- Emails are sent with delays to avoid spam detection
- All progress is saved - safe to stop and resume anytime

## 🤝 Contributing

This is a production-grade automation system. Contributions welcome for:
- Additional provinces/cities
- Enhanced website analysis
- Improved email templates
- Better error handling

## 📄 License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This bot is for legitimate business outreach only. Ensure compliance with:
- CAN-SPAM Act (USA)
- CASL (Canada)
- GDPR (EU)
- Local anti-spam laws

Always include unsubscribe options and honor opt-out requests.

---

**Built with** ❤️ **using Python, Google Maps API, and Gemini AI**
