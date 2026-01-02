# Email Outreach Bot - Architecture Documentation

## System Overview

The Email Outreach Bot is a stateful, deterministic system designed for large-scale business outreach across provinces. It combines web scraping, AI content generation, and email automation in a modular, production-ready architecture.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  run.py  │    │status.py │    │ reset.py │              │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘              │
│       └──────────────┬─────────────────┘                    │
└──────────────────────┼──────────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────────┐
│                      ▼                                       │
│              ┌───────────────┐        Orchestration Layer   │
│              │ orchestrator  │                              │
│              │     .py       │                              │
│              └───────┬───────┘                              │
│                      │                                       │
│      ┌───────┬───────┼───────┬───────┬────────┐           │
└──────┼───────┼───────┼───────┼───────┼────────┼───────────┘
       │       │       │       │       │        │
┌──────▼───────▼───────▼───────▼───────▼────────▼────────────┐
│                   Component Layer                            │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ history_ │  │location_ │  │ scraper  │  │   site_  │   │
│  │  store   │  │ manager  │  │   .py    │  │ analyzer │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────┐  ┌──────────┐                                │
│  │   ai_    │  │  mailer  │                                │
│  │  writer  │  │   .py    │                                │
│  └──────────┘  └──────────┘                                │
└──────┬────────────────┬────────────────┬─────────┬─────────┘
       │                │                │         │
┌──────▼────────────────▼────────────────▼─────────▼─────────┐
│                  External Services                          │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  SQLite  │  │  Google  │  │  Gemini  │  │  Gmail   │   │
│  │    DB    │  │ Maps API │  │   API    │  │   SMTP   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. CLI Layer

#### run.py
- **Purpose**: Main entry point for bot execution
- **Responsibilities**:
  - Parse command-line arguments
  - Initialize orchestrator
  - Handle execution flow
  - Display results
- **Key Functions**:
  - `main()`: Entry point with argument parsing

#### status.py
- **Purpose**: Display progress and statistics
- **Responsibilities**:
  - Query database for status
  - Format and display metrics
  - Show completion percentage
- **Key Functions**:
  - `main()`: Status display logic

#### reset.py
- **Purpose**: Reset data for a province/category
- **Responsibilities**:
  - Confirm user intent
  - Delete specified data
  - Provide feedback
- **Key Functions**:
  - `main()`: Reset with confirmation

### 2. Orchestration Layer

#### orchestrator.py
- **Purpose**: Coordinate all components
- **Responsibilities**:
  - Initialize all components
  - Manage execution flow
  - Track run statistics
  - Handle errors and interruptions
  - Coordinate smart progression
- **Key Classes**:
  - `Orchestrator`: Main coordination class
- **Key Methods**:
  - `run()`: Execute outreach for province/category
  - `_initialize_search_locations()`: Set up search grid
  - `_process_search()`: Handle single search location
  - `get_status()`: Query current status
  - `reset()`: Reset province data

### 3. Component Layer

#### history_store.py
- **Purpose**: Persistent state management
- **Responsibilities**:
  - Database initialization and schema
  - CRUD operations for searches, businesses, runs
  - Query methods for progression logic
  - Status tracking and reporting
- **Key Classes**:
  - `HistoryStore`: Database interface
- **Database Tables**:
  - `searches`: Search locations and status
  - `businesses`: Discovered business data
  - `runs`: Execution history
- **Key Methods**:
  - `add_search()`: Register search location
  - `update_search()`: Update search status
  - `add_business()`: Store discovered business
  - `mark_email_sent()`: Track sent emails
  - `get_next_search()`: Get uncompleted search
  - `is_province_complete()`: Check completion

#### location_manager.py
- **Purpose**: Geographic data and grid generation
- **Responsibilities**:
  - Store province/city coordinates
  - Generate search grids for cities
  - Calculate distances
  - Prevent duplicate locations
- **Key Classes**:
  - `LocationManager`: Location coordination
- **Data Structure**:
  - `PROVINCE_DATA`: Dictionary of provinces and cities
- **Key Methods**:
  - `get_province_cities()`: Get all cities
  - `generate_search_grids()`: Create search points
  - `get_all_search_locations()`: Full province grid
  - `calculate_distance()`: Haversine distance
  - `is_duplicate_location()`: Duplicate detection

#### scraper.py
- **Purpose**: Business discovery via Google Maps
- **Responsibilities**:
  - Query Google Places API
  - Handle pagination
  - Extract business details
  - Scrape emails from websites
  - Parse HTML content
- **Key Classes**:
  - `Scraper`: Web scraping interface
- **Key Methods**:
  - `search_businesses()`: Query Places API
  - `_extract_business_info()`: Parse place data
  - `extract_email_from_website()`: Find email addresses
  - `_is_valid_email()`: Validate email format

#### site_analyzer.py
- **Purpose**: Website analysis for insights
- **Responsibilities**:
  - Fetch and parse websites
  - Identify UX issues
  - Detect design problems
  - Generate findings
- **Key Classes**:
  - `SiteAnalyzer`: Website analysis
- **Analysis Categories**:
  - Mobile responsiveness
  - Call-to-action presence
  - Contact information
  - Navigation structure
  - SSL/HTTPS
  - Performance issues
- **Key Methods**:
  - `analyze_website()`: Perform full analysis
  - `get_key_findings()`: Extract highlights

#### ai_writer.py
- **Purpose**: AI-powered email generation
- **Responsibilities**:
  - Interface with Gemini API
  - Generate personalized content
  - Create email subjects and bodies
  - Include business-specific context
  - Fallback to templates if API fails
- **Key Classes**:
  - `AIWriter`: Email generation
- **Key Methods**:
  - `generate_email()`: Create personalized email
  - `_generate_template_email()`: Fallback template

#### mailer.py
- **Purpose**: Email delivery via Gmail
- **Responsibilities**:
  - SMTP connection management
  - Rate limiting enforcement
  - Retry logic
  - Email formatting
  - Status tracking
- **Key Classes**:
  - `Mailer`: Email sender
- **Features**:
  - Automatic rate limiting
  - Exponential backoff retry
  - Send tracking
  - Connection testing
- **Key Methods**:
  - `send_email()`: Send with retry
  - `_wait_for_rate_limit()`: Enforce limits
  - `get_rate_limit_status()`: Check quota
  - `test_connection()`: Verify setup

## Data Flow

### Typical Execution Flow

1. **Initialization**:
   ```
   CLI → Orchestrator → Initialize Components → Load .env
   ```

2. **Search Location Setup**:
   ```
   Orchestrator → LocationManager → Generate Grids → HistoryStore
   ```

3. **Business Discovery**:
   ```
   Orchestrator → Get Next Search → Scraper → Places API
   → Extract Business Info → Find Email → HistoryStore
   ```

4. **Website Analysis**:
   ```
   Orchestrator → SiteAnalyzer → Fetch Website → Parse HTML
   → Generate Findings → HistoryStore
   ```

5. **Email Generation**:
   ```
   Orchestrator → AIWriter → Gemini API → Generate Content
   → Return Subject + Body
   ```

6. **Email Delivery**:
   ```
   Orchestrator → Mailer → Check Rate Limit → SMTP Send
   → Update HistoryStore
   ```

7. **Progression**:
   ```
   Orchestrator → Mark Search Complete → Get Next Search
   → Repeat or Complete
   ```

## State Management

### Search States
- `pending`: Not yet processed
- `partial`: Started but incomplete
- `complete`: Fully processed

### Business States
- `email_sent = 0`: Not contacted
- `email_sent = 1`: Email sent

### Run States
- `running`: Currently executing
- `paused`: Stopped at limit
- `completed`: Finished all searches
- `interrupted`: User stopped
- `failed`: Error occurred

## Determinism & Restart Safety

The system ensures deterministic behavior through:

1. **Unique Constraints**: Database prevents duplicates
2. **Sequential Processing**: Searches processed in order
3. **State Persistence**: All progress saved immediately
4. **Idempotent Operations**: Safe to re-run searches
5. **Transaction Safety**: Database commits after each step

## Scalability Considerations

### Current Limitations
- Single-threaded execution
- Rate-limited by Gmail (25/hour)
- Sequential city processing

### Future Enhancements
- Multi-threaded scraping
- Multiple email accounts (round-robin)
- Distributed city processing
- Background job queue
- Web dashboard interface

## Error Handling

### Graceful Degradation
- API failures → Continue with next business
- Email failures → Retry with backoff
- Connection errors → Log and skip
- Keyboard interrupt → Save state and exit

### Logging Strategy
- Console output for user feedback
- Database error logs for tracking
- Run statistics for analysis

## Security Measures

1. **Credential Protection**:
   - Environment variables only
   - `.env` never committed
   - App passwords (not main password)

2. **Input Validation**:
   - Email format validation
   - URL validation
   - Province/category sanitization

3. **Rate Limiting**:
   - Per-hour limits
   - Delay between sends
   - Timestamp tracking

4. **Compliance**:
   - Unsubscribe in every email
   - Opt-out handling
   - Anti-spam compliance

## Configuration

### Environment Variables
All configuration via `.env`:
- API keys (Google Maps, Gemini)
- Email credentials (Gmail)
- Rate limits
- Search parameters

### Tuneable Parameters
- `SEARCH_RADIUS_METERS`: Search area size
- `MAX_RESULTS_PER_SEARCH`: Businesses per search
- `EMAILS_PER_HOUR`: Send rate
- Grid generation (in code)

## Testing Strategy

### Unit Testing (Future)
- Each component independently testable
- Mock external APIs
- Test database operations
- Validate email generation

### Integration Testing
- Test with `--test` flag
- Verify API connections
- Check database initialization
- Validate environment setup

### Manual Testing
- Small test runs (`--limit=5`)
- Status command verification
- Reset functionality
- Error handling scenarios

## Deployment

### Requirements
- Python 3.8+
- Internet connection
- Valid API keys
- Gmail account

### Installation Steps
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Configure `.env`
5. Test connections
6. Run bot

### Monitoring
- Watch CLI output
- Check `status.py` regularly
- Monitor database size
- Track API quotas

## Maintenance

### Regular Tasks
- Monitor API quotas
- Review error logs
- Update city data
- Refresh email templates
- Check compliance

### Updates
- Keep dependencies updated
- Review API changes
- Adjust rate limits as needed
- Add new provinces/cities

---

**Last Updated**: 2026-01-02
**Version**: 1.0.0
