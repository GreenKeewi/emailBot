#!/usr/bin/env python3
"""
Example usage script for auditBot.
Demonstrates how to use the various components programmatically.
"""
import asyncio
from pathlib import Path

# Import auditBot components
import config
from scraper.categories import get_categories, add_category
from emailer.gmail_service import GmailService
from analytics.stats import StatsCalculator
from analytics.reports import ReportGenerator

def example_1_view_configuration():
    """Example 1: View current configuration."""
    print("\n" + "="*60)
    print("EXAMPLE 1: View Configuration")
    print("="*60)
    
    print(f"\nData Directory: {config.DATA_DIR}")
    print(f"Cities File: {config.CITIES_CSV}")
    print(f"Businesses File: {config.BUSINESSES_CSV}")
    print(f"\nDefault Template: {config.DEFAULT_TEMPLATE}")
    print(f"Scraper Delay: {config.SCRAPER_DELAY} seconds")
    print(f"Max Businesses Per City: {config.MAX_BUSINESSES_PER_CITY}")
    
    print(f"\nBusiness Categories ({len(config.BUSINESS_CATEGORIES)}):")
    for i, category in enumerate(config.BUSINESS_CATEGORIES[:5], 1):
        print(f"  {i}. {category}")
    print(f"  ... and {len(config.BUSINESS_CATEGORIES) - 5} more")

def example_2_manage_categories():
    """Example 2: Manage business categories."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Manage Categories")
    print("="*60)
    
    categories = get_categories()
    print(f"\nCurrent categories: {len(categories)}")
    
    # Add a new category
    new_category = "yoga studios"
    if add_category(new_category):
        print(f"✓ Added new category: {new_category}")
    else:
        print(f"ℹ Category already exists: {new_category}")
    
    print(f"\nUpdated count: {len(get_categories())} categories")

def example_3_view_statistics():
    """Example 3: View statistics programmatically."""
    print("\n" + "="*60)
    print("EXAMPLE 3: View Statistics")
    print("="*60)
    
    stats_calc = StatsCalculator()
    
    # Get city statistics
    city_stats = stats_calc.get_city_stats()
    print("\nCity Statistics:")
    print(f"  Total Cities: {city_stats['total']}")
    print(f"  Completed: {city_stats['completed']}")
    print(f"  Remaining: {city_stats['remaining']}")
    print(f"  Progress: {city_stats['percentage']:.1f}%")
    
    # Get business statistics
    business_stats = stats_calc.get_business_stats()
    print("\nBusiness Statistics:")
    print(f"  Total Found: {business_stats['total_found']}")
    print(f"  Emails Sent: {business_stats['total_emailed']}")
    print(f"  Duplicates Skipped: {business_stats['duplicates_skipped']}")
    print(f"  Responses: {business_stats['responses']}")
    
    # Get top categories
    top_categories = stats_calc.get_top_categories(5)
    if top_categories:
        print("\nTop 5 Categories:")
        for i, (category, count) in enumerate(top_categories, 1):
            print(f"  {i}. {category}: {count} emails")

def example_4_generate_reports():
    """Example 4: Generate reports programmatically."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generate Reports")
    print("="*60)
    
    report_gen = ReportGenerator()
    
    # Export summary
    print("\nExporting summary report...")
    if report_gen.export_summary():
        print("✓ Summary report exported successfully")
    
    # Log a response
    print("\nLogging a test response...")
    if report_gen.log_response("demo@example.com", "Demo response for testing"):
        print("✓ Response logged successfully")

def example_5_email_template_info():
    """Example 5: Display email template information."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Email Templates")
    print("="*60)
    
    templates_dir = config.TEMPLATES_DIR
    print(f"\nTemplates Directory: {templates_dir}")
    
    if templates_dir.exists():
        templates = list(templates_dir.glob("*.txt"))
        print(f"\nAvailable Templates ({len(templates)}):")
        for template in templates:
            print(f"  - {template.name}")
            
            # Show first few lines
            with open(template, 'r') as f:
                lines = f.readlines()[:3]
            print(f"    Preview: {lines[0].strip()}")
    else:
        print("\n⚠ Templates directory not found")

def example_6_data_file_status():
    """Example 6: Check data file status."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Data File Status")
    print("="*60)
    
    files = {
        'Cities': config.CITIES_CSV,
        'Businesses': config.BUSINESSES_CSV,
        'Sent Emails': config.SENT_BUSINESSES_CSV,
        'Responses': config.RESPONSES_CSV,
    }
    
    print("\nData Files Status:")
    for name, filepath in files.items():
        if filepath.exists():
            # Count lines (excluding header)
            with open(filepath, 'r') as f:
                line_count = len(f.readlines()) - 1
            print(f"  ✓ {name}: {line_count} records")
        else:
            print(f"  ✗ {name}: Not found")

def example_7_email_service_info():
    """Example 7: Gmail service information."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Gmail API Configuration")
    print("="*60)
    
    print(f"\nCredentials File: {config.CREDENTIALS_FILE}")
    print(f"Token File: {config.TOKEN_FILE}")
    
    if config.CREDENTIALS_FILE.exists():
        print("✓ Credentials file found")
    else:
        print("✗ Credentials file not found")
        print("  → Run Gmail API setup (see SETUP.md)")
    
    if config.TOKEN_FILE.exists():
        print("✓ Token file found (already authenticated)")
    else:
        print("ℹ Token file not found (authentication required on first run)")
    
    print(f"\nGmail API Scopes:")
    for scope in config.GMAIL_SCOPES:
        print(f"  - {scope}")

def run_all_examples():
    """Run all examples."""
    print("\n" + "="*70)
    print(" "*20 + "AUDITBOT EXAMPLES")
    print("="*70)
    print("\nThis script demonstrates the various capabilities of auditBot.")
    print("No actual scraping or email sending will occur.")
    
    try:
        example_1_view_configuration()
        example_2_manage_categories()
        example_3_view_statistics()
        example_4_generate_reports()
        example_5_email_template_info()
        example_6_data_file_status()
        example_7_email_service_info()
        
        print("\n" + "="*70)
        print("All examples completed successfully!")
        print("="*70)
        
        print("\n📚 Next Steps:")
        print("  1. Complete Gmail API setup (if not done)")
        print("  2. Customize business categories")
        print("  3. Add/edit email templates")
        print("  4. Run: python main.py --uno")
        print("\n💡 For help: python main.py --help")
        print("📖 Documentation: README.md and SETUP.md")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Some features may not be available yet.")

if __name__ == '__main__':
    run_all_examples()
