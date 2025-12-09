#!/usr/bin/env python3
"""
AuditBot - Business Scraping and Email Automation Tool

A command-line tool for discovering and contacting businesses across North American cities.
"""
import argparse
import asyncio
import csv
import sys
from datetime import datetime
from pathlib import Path
import logging

import config
from scraper.categories import get_categories
from scraper.maps_scraper import scrape_city_businesses
from emailer.gmail_service import GmailService, send_business_email
from analytics.stats import StatsCalculator
from analytics.reports import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CityManager:
    """Manages city processing and tracking."""
    
    def __init__(self):
        """Initialize city manager."""
        self.cities_file = config.CITIES_CSV
        self._ensure_cities_file()
    
    def _ensure_cities_file(self):
        """Ensure cities.csv exists, create from example if not."""
        if not self.cities_file.exists():
            example_file = config.DATA_DIR / "cities.csv.example"
            if example_file.exists():
                import shutil
                shutil.copy(example_file, self.cities_file)
                logger.info(f"Created cities.csv from example file")
            else:
                # Create empty cities file
                with open(self.cities_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['city', 'state', 'country', 'completed'])
                logger.warning("Created empty cities.csv - please add cities")
    
    def get_next_city(self):
        """
        Get the next unprocessed city.
        
        Returns:
            Dictionary with city info or None if no cities left
        """
        try:
            with open(self.cities_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('completed', '').lower() != 'true':
                        return row
            return None
        except Exception as e:
            logger.error(f"Error reading cities file: {e}")
            return None
    
    def get_cities(self, count: int):
        """
        Get multiple unprocessed cities.
        
        Args:
            count: Number of cities to get
            
        Returns:
            List of city dictionaries
        """
        cities = []
        try:
            with open(self.cities_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('completed', '').lower() != 'true':
                        cities.append(row)
                        if len(cities) >= count:
                            break
            return cities
        except Exception as e:
            logger.error(f"Error reading cities file: {e}")
            return []
    
    def mark_city_completed(self, city_name: str, state: str):
        """
        Mark a city as completed.
        
        Args:
            city_name: Name of the city
            state: State/Province
        """
        try:
            rows = []
            with open(self.cities_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['city'] == city_name and row['state'] == state:
                        row['completed'] = 'true'
                    rows.append(row)
            
            with open(self.cities_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['city', 'state', 'country', 'completed'])
                writer.writeheader()
                writer.writerows(rows)
            
            logger.info(f"Marked {city_name}, {state} as completed")
        except Exception as e:
            logger.error(f"Error marking city completed: {e}")


class BusinessManager:
    """Manages business data and deduplication."""
    
    def __init__(self):
        """Initialize business manager."""
        self.businesses_file = config.BUSINESSES_CSV
        self.sent_file = config.SENT_BUSINESSES_CSV
        self._ensure_files()
    
    def _ensure_files(self):
        """Ensure business CSV files exist."""
        if not self.businesses_file.exists():
            with open(self.businesses_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'website', 'email', 'phone', 'category', 'city', 'state', 'country', 'status'])
        
        if not self.sent_file.exists():
            with open(self.sent_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'email', 'city', 'category', 'date_sent'])
    
    def is_duplicate(self, email: str) -> bool:
        """
        Check if business email already exists.
        
        Args:
            email: Business email address
            
        Returns:
            True if duplicate, False otherwise
        """
        try:
            # Check in businesses file
            if self.businesses_file.exists():
                with open(self.businesses_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('email', '').lower() == email.lower():
                            return True
            
            # Check in sent file
            if self.sent_file.exists():
                with open(self.sent_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('email', '').lower() == email.lower():
                            return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking duplicate: {e}")
            return False
    
    def add_business(self, business: dict):
        """
        Add a business to the database.
        
        Args:
            business: Dictionary with business information
        """
        try:
            with open(self.businesses_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'name', 'website', 'email', 'phone', 'category', 'city', 'state', 'country', 'status'
                ])
                writer.writerow(business)
            logger.info(f"Added business: {business.get('name', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error adding business: {e}")
    
    def log_sent_email(self, business: dict):
        """
        Log a sent email.
        
        Args:
            business: Dictionary with business information
        """
        try:
            with open(self.sent_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'name', 'email', 'city', 'category', 'date_sent'
                ])
                row = {
                    'name': business.get('name', ''),
                    'email': business.get('email', ''),
                    'city': business.get('city', ''),
                    'category': business.get('category', ''),
                    'date_sent': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                writer.writerow(row)
            logger.info(f"Logged sent email to: {business.get('email', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error logging sent email: {e}")


async def process_city(city_info: dict, gmail_service: GmailService, template: str = None):
    """
    Process a single city: scrape businesses and send emails.
    
    Args:
        city_info: Dictionary with city information
        gmail_service: Authenticated Gmail service
        template: Email template to use
    """
    city_name = city_info['city']
    state = city_info['state']
    country = city_info['country']
    
    print(f"\n{'='*60}")
    print(f"Processing: {city_name}, {state}, {country}")
    print(f"{'='*60}\n")
    
    business_manager = BusinessManager()
    categories = get_categories()
    
    # Scrape businesses
    logger.info(f"Scraping businesses for {city_name}...")
    print(f"Searching for businesses in {len(categories)} categories...")
    
    # Note: The actual scraping is simplified here
    # In production, you would use the actual scraper
    businesses = await scrape_city_businesses(
        city_name, state, country, categories, max_per_category=5
    )
    
    print(f"Found {len(businesses)} businesses")
    
    # Process each business
    sent_count = 0
    duplicate_count = 0
    skipped_count = 0
    
    for business in businesses:
        # Skip if missing required fields
        if not business.get('email') or not business.get('website'):
            skipped_count += 1
            continue
        
        # Check for duplicates
        if business_manager.is_duplicate(business['email']):
            duplicate_count += 1
            business['status'] = 'duplicate'
            business_manager.add_business(business)
            continue
        
        # Add to businesses database
        business['status'] = 'new'
        business_manager.add_business(business)
        
        # Send email
        try:
            success = send_business_email(
                gmail_service,
                business['email'],
                business.get('name', 'Business'),
                template
            )
            
            if success:
                business_manager.log_sent_email(business)
                sent_count += 1
                print(f"✓ Sent email to {business.get('name', 'Unknown')} ({business['email']})")
            else:
                print(f"✗ Failed to send email to {business['email']}")
        except Exception as e:
            logger.error(f"Error sending email to {business['email']}: {e}")
            print(f"✗ Error sending email to {business['email']}: {e}")
    
    print(f"\n{'-'*60}")
    print(f"City Summary:")
    print(f"  Businesses found: {len(businesses)}")
    print(f"  Emails sent: {sent_count}")
    print(f"  Duplicates skipped: {duplicate_count}")
    print(f"  Invalid entries skipped: {skipped_count}")
    print(f"{'-'*60}\n")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='AuditBot - Business Scraping and Email Automation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --uno                          Process one city
  python main.py --run 5                        Process 5 cities
  python main.py --stats                        Show overall statistics
  python main.py --city-stats                   Show per-city statistics
  python main.py --top-categories               Show top categories
  python main.py --log-response email@test.com  Log a business response
  python main.py --export-summary               Export summary report
  python main.py --template template2.txt --run 3  Use custom template
        """
    )
    
    # City processing commands
    parser.add_argument('--uno', action='store_true',
                        help='Process one city (next unprocessed)')
    parser.add_argument('--run', type=int, metavar='N',
                        help='Process N cities in order')
    
    # Analytics commands
    parser.add_argument('--stats', action='store_true',
                        help='Show overall statistics')
    parser.add_argument('--city-stats', action='store_true',
                        help='Show statistics by city')
    parser.add_argument('--top-categories', action='store_true',
                        help='Show top categories by emails sent')
    
    # Response logging
    parser.add_argument('--log-response', metavar='EMAIL',
                        help='Log a response from a business')
    parser.add_argument('--notes', metavar='TEXT',
                        help='Notes for the response (use with --log-response)')
    
    # Export
    parser.add_argument('--export-summary', action='store_true',
                        help='Export summary report to CSV')
    
    # Email template
    parser.add_argument('--template', metavar='FILE',
                        help='Email template to use (default: template1.txt)')
    
    args = parser.parse_args()
    
    # Handle analytics commands (don't require Gmail auth)
    if args.stats:
        stats_calc = StatsCalculator()
        stats_calc.display_stats()
        return
    
    if args.city_stats:
        stats_calc = StatsCalculator()
        stats_calc.display_city_stats()
        return
    
    if args.top_categories:
        stats_calc = StatsCalculator()
        stats_calc.display_top_categories()
        return
    
    if args.log_response:
        report_gen = ReportGenerator()
        notes = args.notes or ""
        report_gen.log_response(args.log_response, notes)
        return
    
    if args.export_summary:
        report_gen = ReportGenerator()
        report_gen.export_summary()
        return
    
    # Handle city processing commands (require Gmail auth)
    if args.uno or args.run:
        # Initialize Gmail service
        print("Initializing Gmail service...")
        try:
            gmail_service = GmailService()
            gmail_service.authenticate()
        except FileNotFoundError as e:
            print(f"\n✗ Error: {e}")
            print("\nPlease set up Gmail API credentials:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create a project and enable Gmail API")
            print("3. Create OAuth 2.0 credentials")
            print("4. Download credentials.json to this directory")
            return
        except Exception as e:
            print(f"\n✗ Error authenticating with Gmail: {e}")
            return
        
        city_manager = CityManager()
        template = args.template or config.DEFAULT_TEMPLATE
        
        # Get cities to process
        if args.uno:
            city = city_manager.get_next_city()
            if city:
                cities = [city]
            else:
                print("\n✗ No unprocessed cities remaining.")
                return
        else:
            cities = city_manager.get_cities(args.run)
            if not cities:
                print(f"\n✗ No unprocessed cities remaining.")
                return
            if len(cities) < args.run:
                print(f"\nNote: Only {len(cities)} unprocessed cities available (requested {args.run})")
        
        # Process cities
        print(f"\nProcessing {len(cities)} city/cities...")
        
        for city in cities:
            try:
                asyncio.run(process_city(city, gmail_service, template))
                city_manager.mark_city_completed(city['city'], city['state'])
                print(f"✓ Completed: {city['city']}, {city['state']}")
            except Exception as e:
                logger.error(f"Error processing {city['city']}: {e}")
                print(f"\n✗ Error processing {city['city']}: {e}")
        
        print(f"\n{'='*60}")
        print("Processing complete!")
        print(f"{'='*60}\n")
        
        # Show updated stats
        stats_calc = StatsCalculator()
        stats_calc.display_stats()
        return
    
    # No arguments provided
    parser.print_help()


if __name__ == '__main__':
    main()
