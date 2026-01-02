# Deployment Guide

Complete guide for deploying the Email Outreach Bot to production.

## Pre-Deployment Checklist

### Required Accounts & Services
- [ ] Google Cloud Account with billing enabled
- [ ] Google Maps API access (Places API enabled)
- [ ] Google AI Studio account (Gemini API)
- [ ] Gmail account with 2FA enabled
- [ ] Gmail App Password generated

### API Quotas & Costs

#### Google Maps Places API
- **Free Tier**: $200/month credit
- **Cost per call**: ~$0.032
- **Estimated usage**: 1000 businesses ≈ $30-50
- **Monitor**: https://console.cloud.google.com/

#### Google Gemini API
- **Free Tier**: 60 requests/min, 1,500/day
- **Cost**: Free for moderate use
- **Monitor**: https://makersuite.google.com/

#### Gmail SMTP
- **Limit**: 500 emails/day for regular accounts
- **Recommended**: 25-30 emails/hour to avoid spam flags
- **Cost**: Free

## Deployment Steps

### 1. Server Setup

**Recommended Specs:**
- OS: Ubuntu 20.04+ / Debian 11+ / Any Linux
- RAM: 1GB minimum (2GB recommended)
- Storage: 5GB minimum
- Python: 3.8+

**Option A: Local Machine**
```bash
# Install Python and required system packages
sudo apt update
sudo apt install python3 python3-pip python3-venv git sqlite3
```

**Option B: VPS (DigitalOcean, Linode, AWS EC2)**
```bash
# Same as above, plus configure firewall
sudo ufw allow ssh
sudo ufw enable
```

**Option C: Docker (Future)**
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```

### 2. Clone and Install

```bash
# Clone repository
git clone https://github.com/GreenKeewi/emailBot.git
cd emailBot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python validate.py
```

### 3. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or vim, or your editor
```

**Required values:**
```env
GOOGLE_MAPS_API_KEY=AIzaSy...
GEMINI_API_KEY=AIzaSy...
GMAIL_ADDRESS=your@email.com
GMAIL_APP_PASSWORD=abcdefghijklmnop
FROM_NAME=Your Company
REPLY_TO_EMAIL=your@email.com
EMAILS_PER_HOUR=25
```

### 4. Test Configuration

```bash
# Validate setup
python validate.py

# Test API connections
python run.py --test

# Test with 1 email
python run.py --province=Ontario --category=plumber --limit=1
```

### 5. Production Run

```bash
# Run in foreground (for testing)
python run.py --province=Ontario --category=plumber

# Run in background (production)
nohup python run.py --province=Ontario --category=plumber > bot.log 2>&1 &

# Monitor
tail -f bot.log

# Check status
python status.py --province=Ontario --category=plumber
```

## Running as a Service

### Option 1: systemd (Recommended for Linux)

Create `/etc/systemd/system/emailbot.service`:

```ini
[Unit]
Description=Email Outreach Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/emailBot
Environment="PATH=/path/to/emailBot/venv/bin"
ExecStart=/path/to/emailBot/venv/bin/python run.py --province=Ontario --category=plumber
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable emailbot
sudo systemctl start emailbot
sudo systemctl status emailbot

# View logs
sudo journalctl -u emailbot -f
```

### Option 2: Cron Job (For scheduled runs)

```bash
# Edit crontab
crontab -e

# Run daily at 9 AM
0 9 * * * cd /path/to/emailBot && /path/to/emailBot/venv/bin/python run.py --province=Ontario --category=plumber --limit=50 >> /path/to/bot.log 2>&1

# Run every 2 hours
0 */2 * * * cd /path/to/emailBot && /path/to/emailBot/venv/bin/python run.py --province=Ontario --category=plumber --limit=25 >> /path/to/bot.log 2>&1
```

### Option 3: Screen/tmux (Simple)

```bash
# Start screen session
screen -S emailbot

# Run bot
cd emailBot
source venv/bin/activate
python run.py --province=Ontario --category=plumber

# Detach: Ctrl+A, then D
# Reattach: screen -r emailbot
```

## Monitoring & Maintenance

### Check Status
```bash
# Progress
python status.py --province=Ontario --category=plumber

# Database stats
sqlite3 outreach_bot.db "SELECT COUNT(*) FROM businesses;"
sqlite3 outreach_bot.db "SELECT COUNT(*) FROM businesses WHERE email_sent = 1;"
```

### Monitor Logs
```bash
# Systemd service
sudo journalctl -u emailbot -f

# Manual run
tail -f bot.log

# Check for errors
grep "error\|Error\|ERROR" bot.log
```

### Database Backup
```bash
# Backup database
cp outreach_bot.db outreach_bot_backup_$(date +%Y%m%d).db

# Scheduled backup (add to crontab)
0 0 * * * cp /path/to/emailBot/outreach_bot.db /path/to/backups/outreach_bot_$(date +\%Y\%m\%d).db
```

### Update Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
python validate.py
```

## Scaling & Optimization

### Multiple Categories
```bash
# Run different categories sequentially
python run.py --province=Ontario --category=plumber --limit=50
python run.py --province=Ontario --category=electrician --limit=50
python run.py --province=Ontario --category=dentist --limit=50
```

### Multiple Provinces
```bash
# Ontario first
python run.py --province=Ontario --category=plumber

# Then Quebec
python run.py --province=Quebec --category=plumber

# Then BC
python run.py --province="British Columbia" --category=plumber
```

### Increase Rate Limit (Carefully)
```env
# In .env
EMAILS_PER_HOUR=30  # Increase slowly, monitor for spam flags
```

### Multiple Gmail Accounts
Edit code to rotate between accounts (future enhancement).

## Security Best Practices

### 1. Secure .env file
```bash
chmod 600 .env
# Never commit to git (already in .gitignore)
```

### 2. Restrict API Keys
In Google Cloud Console:
- Set API restrictions
- Set application restrictions
- Set daily quotas

### 3. Monitor Access
- Check Gmail sent folder regularly
- Review API usage in consoles
- Watch for unusual activity

### 4. Regular Updates
```bash
# Weekly check
pip list --outdated
pip install -r requirements.txt --upgrade
```

## Troubleshooting Production Issues

### Bot Stops Unexpectedly
```bash
# Check logs
sudo journalctl -u emailbot -n 100

# Check system resources
free -h
df -h

# Restart service
sudo systemctl restart emailbot
```

### API Rate Limits Hit
```bash
# Check Google Cloud quota
# https://console.cloud.google.com/apis/dashboard

# Reduce send rate in .env
EMAILS_PER_HOUR=20
```

### Database Lock
```bash
# Find processes using database
lsof outreach_bot.db

# Kill if necessary
kill <PID>
```

### Gmail Blocks
```bash
# Reduce send rate
EMAILS_PER_HOUR=15

# Check Gmail account security
# https://myaccount.google.com/security

# Regenerate App Password if needed
```

## Performance Optimization

### Database Optimization
```bash
# Vacuum database periodically
sqlite3 outreach_bot.db "VACUUM;"

# Analyze tables
sqlite3 outreach_bot.db "ANALYZE;"
```

### Monitor Resource Usage
```bash
# CPU and Memory
top
htop

# Disk space
df -h

# Database size
ls -lh outreach_bot.db
```

## Rollback & Recovery

### Restore from Backup
```bash
# Stop bot
sudo systemctl stop emailbot

# Restore database
cp outreach_bot_backup_20260102.db outreach_bot.db

# Restart bot
sudo systemctl start emailbot
```

### Reset Category
```bash
# If something goes wrong
python reset.py --province=Ontario --category=plumber --confirm
```

## Production Monitoring Checklist

Daily:
- [ ] Check bot is running
- [ ] Review recent emails sent
- [ ] Check for error messages
- [ ] Monitor API quota usage

Weekly:
- [ ] Review database size
- [ ] Check backup exists
- [ ] Update dependencies
- [ ] Review response rate

Monthly:
- [ ] Analyze performance metrics
- [ ] Review and optimize prompts
- [ ] Check compliance with regulations
- [ ] Review API costs

## Support & Maintenance

### Log Rotation
```bash
# Add to logrotate
sudo nano /etc/logrotate.d/emailbot

/path/to/emailBot/bot.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Health Check Script
```bash
#!/bin/bash
# health_check.sh
if ! systemctl is-active --quiet emailbot; then
    echo "Bot is down, restarting..."
    sudo systemctl restart emailbot
fi
```

### Alerts (Optional)
Set up email/SMS alerts for:
- Service failures
- API quota warnings
- Database size limits
- Error rate thresholds

## Compliance & Legal

Before production:
- [ ] Review CAN-SPAM Act requirements
- [ ] Review CASL (Canada) requirements
- [ ] Review GDPR (if EU recipients)
- [ ] Ensure unsubscribe works
- [ ] Have opt-out process
- [ ] Keep records of consent
- [ ] Maintain suppression list

## Performance Metrics

Track these metrics:
- **Emails sent per day**
- **Response rate**
- **Unsubscribe rate**
- **Error rate**
- **API costs**
- **Database size**
- **Processing time per city**

## Disaster Recovery

1. **Database Corruption**
   - Restore from backup
   - May lose recent progress

2. **API Key Compromise**
   - Regenerate immediately
   - Update .env
   - Restart bot

3. **Gmail Account Issue**
   - Generate new App Password
   - Update .env
   - Test connection

4. **Server Failure**
   - Deploy to new server
   - Restore database backup
   - Continue from last state

---

**Production Readiness Checklist:**
- [ ] All API keys configured
- [ ] Services tested successfully
- [ ] Backups configured
- [ ] Monitoring in place
- [ ] Logs rotating properly
- [ ] Security measures active
- [ ] Compliance understood
- [ ] Recovery plan documented

**You're ready for production! 🚀**
