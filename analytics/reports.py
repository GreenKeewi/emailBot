"""
Report generation for auditBot.
"""
import csv
from datetime import datetime
from pathlib import Path
import logging

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate reports and export data."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.cities_file = config.CITIES_CSV
        self.businesses_file = config.BUSINESSES_CSV
        self.sent_file = config.SENT_BUSINESSES_CSV
        self.responses_file = config.RESPONSES_CSV
    
    def export_summary(self, output_file: Path = None) -> bool:
        """
        Export a summary report to CSV.
        
        Args:
            output_file: Path to output file (defaults to summary_YYYYMMDD.csv)
            
        Returns:
            True if successful, False otherwise
        """
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = config.DATA_DIR / f"summary_{timestamp}.csv"
        
        try:
            from analytics.stats import StatsCalculator
            
            stats_calc = StatsCalculator()
            city_stats = stats_calc.get_city_stats()
            business_stats = stats_calc.get_business_stats()
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow(['AuditBot Summary Report'])
                writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                writer.writerow([])
                
                # City statistics
                writer.writerow(['City Statistics'])
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Total Cities', city_stats['total']])
                writer.writerow(['Completed Cities', city_stats['completed']])
                writer.writerow(['Remaining Cities', city_stats['remaining']])
                writer.writerow(['Completion Percentage', f"{city_stats['percentage']:.1f}%"])
                writer.writerow([])
                
                # Business statistics
                writer.writerow(['Business Statistics'])
                writer.writerow(['Metric', 'Value'])
                writer.writerow(['Total Businesses Found', business_stats['total_found']])
                writer.writerow(['Emails Sent', business_stats['total_emailed']])
                writer.writerow(['Duplicates Skipped', business_stats['duplicates_skipped']])
                writer.writerow(['Responses Received', business_stats['responses']])
                
                if business_stats['total_emailed'] > 0:
                    response_rate = (business_stats['responses'] / business_stats['total_emailed']) * 100
                    writer.writerow(['Response Rate', f"{response_rate:.1f}%"])
                
                writer.writerow([])
                
                # Top categories
                writer.writerow(['Top Categories'])
                writer.writerow(['Category', 'Emails Sent'])
                
                top_categories = stats_calc.get_top_categories(10)
                for category, count in top_categories:
                    writer.writerow([category, count])
                
                writer.writerow([])
                
                # Per-city statistics
                writer.writerow(['Statistics by City'])
                writer.writerow(['City', 'Emails Sent', 'Unique Categories'])
                
                city_breakdown = stats_calc.get_stats_by_city()
                for city in city_breakdown:
                    writer.writerow([
                        city['city'],
                        city['emails_sent'],
                        city['unique_categories']
                    ])
            
            logger.info(f"Summary report exported to: {output_file}")
            print(f"\n✓ Summary report exported to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting summary: {e}")
            print(f"\n✗ Error exporting summary: {e}")
            return False
    
    def log_response(self, email: str, notes: str = "") -> bool:
        """
        Log a response from a business.
        
        Args:
            email: Email address of the responding business
            notes: Optional notes about the response
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create responses file if it doesn't exist
            if not self.responses_file.exists():
                with open(self.responses_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['email', 'date', 'notes'])
            
            # Append the response
            with open(self.responses_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([email, date, notes])
            
            logger.info(f"Response logged for {email}")
            print(f"\n✓ Response logged for {email}")
            return True
            
        except Exception as e:
            logger.error(f"Error logging response: {e}")
            print(f"\n✗ Error logging response: {e}")
            return False
