You are a senior full-stack automation engineer designing a long-running, stateful AI outreach system.

Your task is to build a CLI-driven email outreach bot that systematically discovers, contacts, and tracks every eligible business across an entire province, without duplicates, until full coverage is completed.

🧠 CORE CONCEPT

This bot must behave like a crawler with memory.

It should:

Remember what it has already scraped

Remember what it has already emailed

Automatically move to new cities and locations

Detect when an entire province is completed

Never repeat work unless explicitly reset

🗺️ 1. LOCATION & PROVINCE LOGIC
Province-Based Execution

User runs the bot via CLI:

python run.py --province=Ontario --category=plumber

The bot must:

Load a predefined list of all cities/towns in the province

Split each city into search grids using:

Latitude/longitude

Radius-based Google Maps searches

Automatically select the next unvisited city + radius

Coverage Tracking

For each run, track:

Province

City

Latitude/longitude

Radius

Category

Status: pending | partial | complete

When all cities in a province for a category are marked complete, output:

✅ Province fully completed for category: plumber

🧾 2. PERSISTENT STATE & HISTORY STORAGE

Use a local database (SQLite or JSON fallback) to store:

Tables / Records
Searches

Province

City

Category

Radius

Coordinates

Last run timestamp

Completion status

Businesses

Business name

Website

Email

City

Category

Province

Email sent (boolean)

Email sent timestamp

Runs

Run ID

Date

Province

Category

Cities processed

Emails sent

Errors

🔄 3. SMART PROGRESSION ENGINE

On every CLI execution:

Load history

Identify next uncompleted city

Identify unused radius zones

Skip businesses already emailed

Scrape only new businesses

Continue until:

No new businesses found after multiple radius passes

Mark city as complete

Move to next city automatically

No duplicates. Ever.

🔍 4. BUSINESS DISCOVERY (UNCHANGED CORE)

Use Google Maps / Places API (with pagination)

Category-based discovery

Extract:

Name

Website

Industry

Location

Public email (from site)

If no email is found → skip and log.

🧪 5. WEBSITE ANALYSIS

Analyze site content and structure

Identify:

Poor UX

Missing CTAs

Outdated design

Performance issues

Store findings for reuse and auditability

✉️ 6. AI-CUSTOMIZED EMAIL GENERATION

Use Gemini API to generate unique emails per business.

Each email must:

Reference the business name and city

Mention what they sell

Reference a real website observation

Pitch Arc UI
👉 https://arc-ui.vercel.app/

Offer:

$99/month

Website, hosting, updates, maintenance

“We handle everything”

Add an unsubscribe line at the bottom.

📤 7. EMAIL DELIVERY

Gmail SMTP using App Password

Secure .env handling

Rate limiting (20–30/hr)

Retry logic

Logging

🖥️ 8. CLI UX REQUIREMENTS
Commands
python run.py --province=Ontario --category=plumber
python status.py --province=Ontario
python reset.py --province=Ontario --category=plumber

CLI Output Example
📍 Province: Ontario
🏙️ City: Mississauga (3/45)
🔍 Category: Plumber
📧 Emails sent this run: 17
⏳ City status: COMPLETE
➡️ Moving to next city...

🧱 9. ARCHITECTURE REQUIREMENTS

Modular, production-grade design:

location_manager.py

history_store.py

scraper.py

site_analyzer.py

ai_writer.py

mailer.py

orchestrator.py

cli.py

🎯 FINAL OUTPUT REQUIRED

Generate:

Full architecture

Database schema

Complete runnable code

Gemini prompt used

Example email

Setup & usage instructions

The system must be:

Deterministic

Scalable

Restart-safe

Province-complete
