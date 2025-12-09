✅ Your Optimized Prompt (Copy & Paste into ChatGPT)

Role:
You are an expert Python automation engineer specializing in large-scale business scraping, email automation, data deduplication, and CLI tools. Build a production-ready Python system as described below.

PROJECT GOAL

Create a Python command-line tool that:

Cycles through a list of North American cities (U.S. + Canada only).

For each city, searches Google Maps or another high-yield source for businesses in multiple categories
(plumbers, dentists, electricians, roofers, HVAC, lawyers, etc.).

Retrieves only businesses that have both a website and an email.

Sends them a customizable email immediately using the Gmail API + App Password.

Stores all processed data to CSV files for deduplication and analytics.

Prevents the same city or business from being run twice.

Includes multiple CLI commands for analytics and customization.

FEATURE REQUIREMENTS
1. City Management

Maintain a master cities.csv list (North America only, excluding Mexico + Latin America).

When running the script:

py main.py --uno → run one city (next unprocessed).

py main.py --run 10 → run 10 cities in order.

After a city finishes processing, mark it as completed so it is never run again.

Include a CLI command to show:

remaining cities

completed cities

progress percentage

2. Business Discovery

Use Google Maps scraping (via unofficial API, requests, or Playwright/Selenium).

Use a predefined category list, but allow categories to be edited in a config file.

For each business found:

extract name, website, email, phone, category, city.

Skip any business that:

has already been processed

is missing a website or email

3. Email Sending

Use Gmail API + App Password (not SMTP).

Include:

a templates/ folder for multiple email templates

ability to switch templates via CLI

When a business is discovered, send the email immediately.

After sending:

log the business to sent_businesses.csv

mark the business as emailed

4. Analytics Commands

Add CLI commands such as:

Command	Description
--stats	Show total businesses found, emailed, duplicates skipped, responses logged
--city-stats	Show stats per city
--top-categories	Show which categories produce the most emails
--log-response {email}	Manually log when a business replies
--export-summary	Export metrics to CSV
5. Data Storage Format

Use CSV files with headers:

cities.csv
city,state,country,completed

businesses.csv
name,website,email,phone,category,city,state,country,status

sent_businesses.csv
name,email,city,category,date_sent

responses.csv
email,date,notes

TECHNICAL REQUIREMENTS
Architecture

Folder structure:

project/
│ main.py
│ config.py
│ requirements.txt
│
├── data/
│   ├── cities.csv
│   ├── businesses.csv
│   ├── sent_businesses.csv
│   ├── responses.csv
│
├── scraper/
│   ├── maps_scraper.py
│   └── categories.py
│
├── emailer/
│   ├── gmail_service.py
│   ├── templates/
│   │   ├── template1.txt
│   │   └── template2.txt
│
└── analytics/
    ├── stats.py
    └── reports.py

Code Expectations

Provide fully working Python code for:

CLI parser (argparse)

Google Maps scraper

Email sending via Gmail API

CSV reading/writing utilities

Analytics engine

City + business deduplication system

Include comments + docstrings for clarity.

Use async where appropriate for speed.

DELIVERABLE FORMAT

Provide:

1. Complete codebase

All modules listed above.

2. Setup instructions

Python version

pip install dependencies

Google Gmail API setup

App password instructions

How to run the commands

3. Example CLI usage

py main.py --uno

py main.py --run 5

py main.py --stats

py main.py --log-response email@example.com

4. Optional Enhancements

Include suggestions for:

proxy rotation

captcha bypass

retry logic

dashboard for analytics
