"""
Statistics calculation for auditBot.
"""
import csv
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime
from collections import Counter
import logging

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatsCalculator:
    """Calculate statistics for the auditBot system."""
    
    def __init__(self):
        """Initialize the stats calculator."""
        self.cities_file = config.CITIES_CSV
        self.businesses_file = config.BUSINESSES_CSV
        self.sent_file = config.SENT_BUSINESSES_CSV
        self.responses_file = config.RESPONSES_CSV
    
    def get_city_stats(self) -> Dict[str, int]:
        """
        Get statistics about cities.
        
        Returns:
            Dictionary with total, completed, and remaining cities
        """
        stats = {
            'total': 0,
            'completed': 0,
            'remaining': 0,
            'percentage': 0.0
        }
        
        if not self.cities_file.exists():
            return stats
        
        try:
            with open(self.cities_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cities = list(reader)
                
                stats['total'] = len(cities)
                stats['completed'] = sum(1 for c in cities if c.get('completed', '').lower() == 'true')
                stats['remaining'] = stats['total'] - stats['completed']
                
                if stats['total'] > 0:
                    stats['percentage'] = (stats['completed'] / stats['total']) * 100
                    
        except Exception as e:
            logger.error(f"Error reading city stats: {e}")
        
        return stats
    
    def get_business_stats(self) -> Dict[str, int]:
        """
        Get statistics about businesses.
        
        Returns:
            Dictionary with business statistics
        """
        stats = {
            'total_found': 0,
            'total_emailed': 0,
            'duplicates_skipped': 0,
            'responses': 0
        }
        
        # Count total businesses found
        if self.businesses_file.exists():
            try:
                with open(self.businesses_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    businesses = list(reader)
                    stats['total_found'] = len(businesses)
                    
                    # Count duplicates (businesses with status 'duplicate')
                    stats['duplicates_skipped'] = sum(
                        1 for b in businesses if b.get('status', '') == 'duplicate'
                    )
            except Exception as e:
                logger.error(f"Error reading business stats: {e}")
        
        # Count total emails sent
        if self.sent_file.exists():
            try:
                with open(self.sent_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    stats['total_emailed'] = len(list(reader))
            except Exception as e:
                logger.error(f"Error reading sent emails: {e}")
        
        # Count responses
        if self.responses_file.exists():
            try:
                with open(self.responses_file, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    stats['responses'] = len(list(reader))
            except Exception as e:
                logger.error(f"Error reading responses: {e}")
        
        return stats
    
    def get_stats_by_city(self) -> List[Dict[str, any]]:
        """
        Get statistics grouped by city.
        
        Returns:
            List of dictionaries with per-city statistics
        """
        city_stats = {}
        
        if not self.sent_file.exists():
            return []
        
        try:
            with open(self.sent_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    city = row.get('city', 'Unknown')
                    if city not in city_stats:
                        city_stats[city] = {
                            'city': city,
                            'emails_sent': 0,
                            'categories': set()
                        }
                    
                    city_stats[city]['emails_sent'] += 1
                    category = row.get('category', '')
                    if category:
                        city_stats[city]['categories'].add(category)
            
            # Convert sets to counts
            result = []
            for city, stats in city_stats.items():
                stats['unique_categories'] = len(stats['categories'])
                del stats['categories']
                result.append(stats)
            
            # Sort by emails sent descending
            result.sort(key=lambda x: x['emails_sent'], reverse=True)
            return result
            
        except Exception as e:
            logger.error(f"Error calculating city stats: {e}")
            return []
    
    def get_top_categories(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Get top categories by number of emails sent.
        
        Args:
            top_n: Number of top categories to return
            
        Returns:
            List of tuples (category, count)
        """
        if not self.sent_file.exists():
            return []
        
        try:
            categories = []
            with open(self.sent_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category = row.get('category', '')
                    if category:
                        categories.append(category)
            
            counter = Counter(categories)
            return counter.most_common(top_n)
            
        except Exception as e:
            logger.error(f"Error calculating top categories: {e}")
            return []
    
    def display_stats(self):
        """Display overall statistics."""
        city_stats = self.get_city_stats()
        business_stats = self.get_business_stats()
        
        print("\n" + "="*60)
        print("AUDITBOT STATISTICS")
        print("="*60)
        
        print("\nCity Progress:")
        print(f"  Total Cities: {city_stats['total']}")
        print(f"  Completed: {city_stats['completed']}")
        print(f"  Remaining: {city_stats['remaining']}")
        print(f"  Progress: {city_stats['percentage']:.1f}%")
        
        print("\nBusiness Statistics:")
        print(f"  Total Businesses Found: {business_stats['total_found']}")
        print(f"  Emails Sent: {business_stats['total_emailed']}")
        print(f"  Duplicates Skipped: {business_stats['duplicates_skipped']}")
        print(f"  Responses Received: {business_stats['responses']}")
        
        if business_stats['total_emailed'] > 0:
            response_rate = (business_stats['responses'] / business_stats['total_emailed']) * 100
            print(f"  Response Rate: {response_rate:.1f}%")
        
        print("="*60 + "\n")
    
    def display_city_stats(self):
        """Display per-city statistics."""
        stats = self.get_stats_by_city()
        
        if not stats:
            print("\nNo city statistics available yet.")
            return
        
        print("\n" + "="*60)
        print("STATISTICS BY CITY")
        print("="*60)
        print(f"\n{'City':<30} {'Emails Sent':<15} {'Categories':<15}")
        print("-"*60)
        
        for city_stat in stats:
            print(f"{city_stat['city']:<30} {city_stat['emails_sent']:<15} {city_stat['unique_categories']:<15}")
        
        print("="*60 + "\n")
    
    def display_top_categories(self, top_n: int = 10):
        """
        Display top categories.
        
        Args:
            top_n: Number of top categories to show
        """
        categories = self.get_top_categories(top_n)
        
        if not categories:
            print("\nNo category statistics available yet.")
            return
        
        print("\n" + "="*60)
        print(f"TOP {top_n} CATEGORIES BY EMAILS SENT")
        print("="*60)
        print(f"\n{'Rank':<8} {'Category':<35} {'Emails Sent':<15}")
        print("-"*60)
        
        for rank, (category, count) in enumerate(categories, 1):
            print(f"{rank:<8} {category:<35} {count:<15}")
        
        print("="*60 + "\n")
