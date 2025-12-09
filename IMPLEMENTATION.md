# Implementation Notes

## Project Overview

AuditBot is a complete Python CLI application for automated business discovery and email outreach. The system is designed to be production-ready with proper error handling, data persistence, and analytics.

## Architecture

### Module Structure

```
auditBot/
├── main.py              # Entry point & CLI interface
├── config.py            # Centralized configuration
├── scraper/             # Business discovery
│   ├── maps_scraper.py  # Google Maps scraping
│   └── categories.py    # Category management
├── emailer/             # Email automation
│   ├── gmail_service.py # Gmail API integration
│   └── templates/       # Email templates
└── analytics/           # Data analysis
    ├── stats.py         # Statistics calculation
    └── reports.py       # Report generation
```

### Design Patterns Used

1. **Service Pattern**: `GmailService`, `StatsCalculator`, `ReportGenerator`
2. **Manager Pattern**: `CityManager`, `BusinessManager`
3. **Configuration Centralization**: All settings in `config.py`
4. **CSV-based Persistence**: Simple, portable, human-readable data storage

## Key Features Implemented

### 1. City Management ✓

- Master cities list with 50 North American cities (US + Canada)
- Completion tracking prevents duplicate processing
- Sequential processing with `--uno` and `--run N` commands
- Progress tracking and statistics

**Implementation**: `CityManager` class in `main.py`

### 2. Business Discovery ✓

- Google Maps scraper framework (Playwright-based)
- Configurable category list (20 default categories)
- Email and website validation
- Deduplication system

**Implementation**: `scraper/maps_scraper.py` and `BusinessManager`

**Note**: The actual scraping implementation is simplified as production-grade Google Maps scraping requires:
- Advanced anti-detection measures
- Proxy rotation
- CAPTCHA solving
- Rate limiting

Consider using:
- Google Maps API (official, paid)
- Third-party scraping services (Apify, Bright Data)
- Outscraper API

### 3. Email Automation ✓

- Gmail API integration (OAuth2)
- Multiple email templates
- Template variable substitution
- Immediate sending upon discovery
- Sent email logging

**Implementation**: `emailer/gmail_service.py`

### 4. Analytics & Reporting ✓

- Overall statistics (cities, businesses, responses)
- Per-city breakdowns
- Top categories analysis
- Response rate calculation
- CSV export for external analysis

**Implementation**: `analytics/stats.py` and `analytics/reports.py`

### 5. Data Deduplication ✓

- Email-based duplicate detection
- Cross-file checking (businesses.csv + sent_businesses.csv)
- Status tracking for processed businesses

**Implementation**: `BusinessManager.is_duplicate()`

## Data Model

### cities.csv
```csv
city,state,country,completed
New York,New York,USA,false
```

### businesses.csv
```csv
name,website,email,phone,category,city,state,country,status
ABC Plumbing,http://abc.com,info@abc.com,555-1234,plumbers,New York,New York,USA,new
```

### sent_businesses.csv
```csv
name,email,city,category,date_sent
ABC Plumbing,info@abc.com,New York,plumbers,2024-01-15 10:30:00
```

### responses.csv
```csv
email,date,notes
info@abc.com,2024-01-16 14:20:00,Interested in service
```

## CLI Commands Reference

| Command | Purpose | Status |
|---------|---------|--------|
| `--uno` | Process one city | ✓ Implemented |
| `--run N` | Process N cities | ✓ Implemented |
| `--stats` | Show overall stats | ✓ Implemented |
| `--city-stats` | Per-city stats | ✓ Implemented |
| `--top-categories` | Top categories | ✓ Implemented |
| `--log-response EMAIL` | Log response | ✓ Implemented |
| `--export-summary` | Export to CSV | ✓ Implemented |
| `--template FILE` | Custom template | ✓ Implemented |

## Technical Decisions

### Why CSV instead of Database?

**Pros:**
- Simple, no dependencies
- Human-readable
- Easy to backup/restore
- Portable across systems
- Can be edited manually if needed

**Cons:**
- Not suitable for concurrent access
- Limited query capabilities
- No transactions

**Future**: Could migrate to SQLite or PostgreSQL for production scale

### Why Gmail API instead of SMTP?

**Pros:**
- More reliable delivery
- Better security (OAuth2)
- No App Password needed
- Better rate limits
- Official Google support

**Cons:**
- More complex setup
- Requires OAuth flow
- Web browser needed for first auth

### Why Playwright instead of Requests?

**Pros:**
- Handles JavaScript rendering
- Better for modern web apps
- Built-in anti-detection features
- Can handle CAPTCHAs manually

**Cons:**
- Slower than requests
- More resource-intensive
- Browser download required

## Security Considerations

### Implemented

1. **Credentials isolation**: `credentials.json` and `token.json` in `.gitignore`
2. **OAuth2 authentication**: Secure, token-based
3. **No hardcoded secrets**: All sensitive data externalized
4. **Input validation**: Email format validation

### To Consider

1. **Encryption at rest**: Encrypt CSV files with sensitive data
2. **API key rotation**: Regular rotation of OAuth tokens
3. **Rate limiting**: Prevent abuse
4. **Logging**: Sanitize logs to remove PII

## Performance Optimization

### Current Approach

- Synchronous processing (one business at a time)
- Sequential city processing
- Fixed delays between requests

### Future Optimizations

1. **Async/Await**: Use `asyncio` for concurrent scraping
2. **Batch Processing**: Process multiple businesses in parallel
3. **Caching**: Cache scraped data to avoid re-scraping
4. **Queue System**: Use Celery/RQ for background processing

## Known Limitations

1. **Google Maps Scraping**: Simplified implementation, not production-ready
2. **Email Finding**: No automatic email extraction from websites
3. **Concurrent Access**: CSV files don't support concurrent writes
4. **Error Recovery**: Limited retry logic for failed operations
5. **Scale**: Not optimized for millions of businesses

## Future Enhancements

### High Priority

1. **Robust Scraping**: Implement production-grade Google Maps scraping
2. **Email Discovery**: Add website crawling to find emails
3. **Retry Logic**: Add exponential backoff for failed requests
4. **Progress Persistence**: Resume from failures

### Medium Priority

1. **Web Dashboard**: Flask/FastAPI dashboard for monitoring
2. **API Integration**: Hunter.io, Clearbit for email finding
3. **Proxy Support**: Rotating proxies for scraping
4. **Database Migration**: Move from CSV to SQLite/PostgreSQL

### Low Priority

1. **CAPTCHA Solving**: Integration with 2Captcha, Anti-Captcha
2. **Multi-User Support**: User authentication and isolation
3. **Scheduled Runs**: Cron/scheduler for automated processing
4. **Webhooks**: Real-time notifications for responses

## Testing

### Manual Testing Completed

- ✓ All CLI commands
- ✓ Data persistence
- ✓ Statistics calculation
- ✓ Report generation
- ✓ Response logging

### Recommended Tests

1. **Unit Tests**: Test each module independently
2. **Integration Tests**: Test end-to-end workflows
3. **Load Tests**: Test with large datasets
4. **Error Tests**: Test error handling

### Test Data

Use `test_setup.py` to create sample data for testing without requiring actual scraping or email sending.

## Maintenance

### Regular Tasks

1. **Backup CSV files**: Daily backup recommended
2. **Monitor Gmail quotas**: Check API usage
3. **Update cities list**: Add new cities as needed
4. **Review categories**: Update based on performance

### Monitoring

Monitor:
- Response rates by category
- City completion progress
- Failed email sends
- API quota usage

## Dependencies

All dependencies are specified in `requirements.txt`:

- `google-*`: Gmail API integration
- `playwright`: Web scraping
- `beautifulsoup4`: HTML parsing
- `pandas`: Data manipulation
- `aiohttp`: Async HTTP requests

## License & Legal

### Compliance

Ensure compliance with:
- CAN-SPAM Act (US)
- GDPR (EU)
- CASL (Canada)
- Google Terms of Service
- Website scraping legality

### Best Practices

1. Honor robots.txt
2. Include unsubscribe links in emails
3. Respect opt-out requests
4. Rate limit requests
5. Identify your scraper in User-Agent

## Support & Documentation

- **README.md**: User-facing documentation
- **SETUP.md**: Gmail API setup guide
- **QUICKSTART.md**: Quick start guide
- **This file**: Developer notes

## Contributing

When contributing:

1. Follow existing code style
2. Add docstrings to all functions
3. Update documentation
4. Test thoroughly
5. Consider security implications

## Version History

- **v1.0.0** (2024-12): Initial implementation
  - Complete CLI interface
  - Gmail API integration
  - Analytics and reporting
  - 50 North American cities
  - 20 business categories
  - Comprehensive documentation

---

**Status**: Production-ready framework, scraping implementation needs enhancement for real-world use.
