"""
Orchestrator for the email outreach bot.
Coordinates all components and manages the execution flow.
"""

from typing import Dict, Optional, Tuple
import os
from dotenv import load_dotenv

from history_store import HistoryStore
from location_manager import LocationManager
from scraper import Scraper
from site_analyzer import SiteAnalyzer
from ai_writer import AIWriter
from mailer import Mailer


class Orchestrator:
    """Coordinates the entire outreach process."""
    
    def __init__(self):
        """Initialize orchestrator and load configuration."""
        load_dotenv()
        
        # Initialize components
        self.history = HistoryStore()
        self.location_manager = LocationManager(
            default_radius=int(os.getenv('SEARCH_RADIUS_METERS', 5000))
        )
        
        # Initialize API-dependent components
        google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        gmail_address = os.getenv('GMAIL_ADDRESS')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not all([google_maps_key, gemini_key, gmail_address, gmail_password]):
            raise ValueError("Missing required environment variables. Check .env file.")
        
        self.scraper = Scraper(google_maps_key)
        self.analyzer = SiteAnalyzer()
        self.writer = AIWriter(gemini_key)
        self.mailer = Mailer(
            gmail_address=gmail_address,
            gmail_app_password=gmail_password,
            from_name=os.getenv('FROM_NAME', 'Arc UI Team'),
            reply_to=os.getenv('REPLY_TO_EMAIL', gmail_address),
            emails_per_hour=int(os.getenv('EMAILS_PER_HOUR', 25))
        )
        
        self.max_results_per_search = int(os.getenv('MAX_RESULTS_PER_SEARCH', 60))
    
    def run(self, province: str, category: str, limit: Optional[int] = None) -> Dict:
        """
        Run the outreach bot for a province and category.
        
        Args:
            province: Province name
            category: Business category
            limit: Optional limit on number of emails to send
            
        Returns:
            Dictionary with run statistics
        """
        print(f"\n{'='*60}")
        print(f"📍 Province: {province}")
        print(f"🔍 Category: {category}")
        print(f"{'='*60}\n")
        
        # Create run record
        run_id = self.history.create_run(province, category)
        
        stats = {
            'cities_processed': 0,
            'businesses_discovered': 0,
            'emails_sent': 0,
            'errors': 0
        }
        
        try:
            # Ensure all search locations are initialized
            self._initialize_search_locations(province, category)
            
            # Process searches until complete or limit reached
            while True:
                # Get next uncompleted search
                search = self.history.get_next_search(province, category)
                
                if not search:
                    print("\n✅ Province fully completed for category:", category)
                    self.history.update_run(run_id, status='completed', **stats)
                    break
                
                # Process this search location
                city_stats = self._process_search(search, category, limit, stats['emails_sent'])
                
                stats['cities_processed'] += 1
                stats['businesses_discovered'] += city_stats['businesses_found']
                stats['emails_sent'] += city_stats['emails_sent']
                stats['errors'] += city_stats['errors']
                
                # Update run
                run_update_params = {
                    'cities_processed': 1,
                    'businesses_discovered': city_stats['businesses_found'],
                    'emails_sent': city_stats['emails_sent'],
                    'errors': city_stats['errors']
                }
                self.history.update_run(run_id, **run_update_params)
                
                # Check if we've hit the email limit
                if limit and stats['emails_sent'] >= limit:
                    print(f"\n⏹️  Reached email limit of {limit}")
                    self.history.update_run(run_id, status='paused', **stats)
                    break
            
        except KeyboardInterrupt:
            print("\n\n⏸️  Run interrupted by user")
            self.history.update_run(run_id, status='interrupted', **stats)
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            self.history.update_run(run_id, status='failed', error_log=str(e), **stats)
            stats['errors'] += 1
        
        print(f"\n{'='*60}")
        print(f"📊 RUN SUMMARY")
        print(f"{'='*60}")
        print(f"Cities processed: {stats['cities_processed']}")
        print(f"Businesses discovered: {stats['businesses_discovered']}")
        print(f"Emails sent: {stats['emails_sent']}")
        print(f"Errors: {stats['errors']}")
        print(f"{'='*60}\n")
        
        return stats
    
    def _initialize_search_locations(self, province: str, category: str):
        """Initialize all search locations for a province."""
        all_locations = self.location_manager.get_all_search_locations(province, category)
        
        for location in all_locations:
            self.history.add_search(
                province=location['province'],
                city=location['city'],
                category=location['category'],
                latitude=location['latitude'],
                longitude=location['longitude'],
                radius=location['radius']
            )
    
    def _process_search(self, search: Dict, category: str, email_limit: Optional[int], 
                       emails_sent_so_far: int) -> Dict:
        """Process a single search location."""
        city = search['city']
        latitude = search['latitude']
        longitude = search['longitude']
        radius = search['radius']
        search_id = search['id']
        
        print(f"\n🏙️  City: {city}")
        print(f"📍 Location: ({latitude:.4f}, {longitude:.4f}), Radius: {radius}m")
        
        stats = {
            'businesses_found': 0,
            'emails_sent': 0,
            'errors': 0,
            'cities_processed': 0,
            'businesses_discovered': 0
        }
        
        try:
            # Search for businesses
            print(f"🔍 Searching for {category} businesses...")
            businesses = self.scraper.search_businesses(
                latitude, longitude, radius, category, self.max_results_per_search
            )
            
            print(f"   Found {len(businesses)} businesses")
            stats['businesses_found'] = len(businesses)
            
            # Process each business
            for i, business in enumerate(businesses, 1):
                try:
                    # Check email limit
                    if email_limit and emails_sent_so_far + stats['emails_sent'] >= email_limit:
                        break
                    
                    # Add business to database
                    site_analysis = None
                    if business.get('website'):
                        site_analysis = self.analyzer.analyze_website(
                            business['website'], 
                            business['name']
                        )
                    
                    business_id = self.history.add_business(
                        name=business['name'],
                        city=city,
                        province=search['province'],
                        category=category,
                        website=business.get('website'),
                        email=business.get('email'),
                        address=business.get('address'),
                        phone=business.get('phone'),
                        latitude=business.get('latitude'),
                        longitude=business.get('longitude'),
                        site_analysis=site_analysis
                    )
                    
                    # Skip if duplicate or no email
                    if not business_id:
                        continue
                    
                    if not business.get('email'):
                        print(f"   [{i}/{len(businesses)}] {business['name']} - No email found")
                        continue
                    
                    # Generate and send email
                    print(f"   [{i}/{len(businesses)}] {business['name']} - Generating email...")
                    
                    email_content = self.writer.generate_email(
                        {**business, 'city': city, 'category': category},
                        site_analysis
                    )
                    
                    success = self.mailer.send_email(
                        to_email=business['email'],
                        subject=email_content['subject'],
                        body=email_content['body']
                    )
                    
                    if success:
                        self.history.mark_email_sent(business_id)
                        stats['emails_sent'] += 1
                        print(f"   ✓ Email sent ({stats['emails_sent']} total)")
                    else:
                        stats['errors'] += 1
                        print(f"   ✗ Email failed")
                    
                except Exception as e:
                    print(f"   ✗ Error processing business: {e}")
                    stats['errors'] += 1
                    continue
            
            # Mark search as complete
            self.history.update_search(search_id, 'complete', stats['businesses_found'])
            print(f"⏳ Search status: COMPLETE\n")
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            self.history.update_search(search_id, 'partial', stats['businesses_found'])
            stats['errors'] += 1
        
        return stats
    
    def get_status(self, province: str, category: Optional[str] = None) -> Dict:
        """
        Get status for a province.
        
        Args:
            province: Province name
            category: Optional category filter
            
        Returns:
            Status dictionary
        """
        if category:
            status = self.history.get_province_status(province, category)
            is_complete = self.history.is_province_complete(province, category)
            
            return {
                'province': province,
                'category': category,
                'complete': is_complete,
                **status
            }
        else:
            return {'province': province, 'message': 'Specify category for detailed status'}
    
    def reset(self, province: str, category: str):
        """
        Reset all data for a province and category.
        
        Args:
            province: Province name
            category: Business category
        """
        self.history.reset_province(province, category)
        print(f"✓ Reset complete for {province} - {category}")
    
    def generate_preview(self, province: str, category: str) -> Optional[str]:
        """
        Generate a preview email for the first business found.
        
        Args:
            province: Province name
            category: Business category
            
        Returns:
            Generated email text or None if no business found
        """
        print(f"Generating preview for {category} in {province}...")
        
        # Get a search location
        locations = self.location_manager.get_all_search_locations(province, category)
        if not locations:
            print("No search locations found.")
            return None
            
        location = locations[0]
        
        # Search for businesses
        print(f"Searching in {location['city']}...")
        businesses = self.scraper.search_businesses(
            location['latitude'], 
            location['longitude'], 
            location['radius'], 
            category, 
            max_results=5 # Just get a few
        )
        
        if not businesses:
            print("No businesses found.")
            return None
            
        business = businesses[0]
        print(f"Found business: {business['name']}")
        
        # Analyze website if available
        site_analysis = None
        if business.get('website'):
            print(f"Analyzing website: {business['website']}")
            site_analysis = self.analyzer.analyze_website(
                business['website'], 
                business['name']
            )
            
        # Generate email
        print("Generating email...")
        email_content = self.writer.generate_email(
            {**business, 'city': location['city'], 'category': category},
            site_analysis
        )
        
        return f"Subject: {email_content['subject']}\n\n{email_content['body']}"

    def test_connection(self) -> bool:
        """Test all connections."""
        print("Testing connections...\n")
        
        # Test Gmail
        gmail_ok = self.mailer.test_connection()
        
        # Could add more tests here
        
        return gmail_ok
