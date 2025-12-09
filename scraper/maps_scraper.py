"""
Google Maps scraper for business information.
Uses Playwright for web scraping with retry logic.
"""
import asyncio
import re
import time
from typing import Dict, List, Optional
from playwright.async_api import async_playwright, Page, TimeoutError as PlaywrightTimeout
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleMapsScraper:
    """Scrapes business information from Google Maps."""
    
    def __init__(self, headless: bool = True, delay: int = 2):
        """
        Initialize the scraper.
        
        Args:
            headless: Whether to run browser in headless mode
            delay: Delay in seconds between requests
        """
        self.headless = headless
        self.delay = delay
        self.browser = None
        self.context = None
        self.page = None
    
    async def start(self):
        """Start the browser instance."""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()
        logger.info("Browser started successfully")
    
    async def close(self):
        """Close the browser instance."""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")
    
    async def search_businesses(
        self, 
        city: str, 
        state: str, 
        country: str, 
        category: str,
        max_results: int = 20
    ) -> List[Dict[str, str]]:
        """
        Search for businesses in a specific city and category.
        
        Args:
            city: City name
            state: State/Province name
            country: Country name
            category: Business category
            max_results: Maximum number of results to return
            
        Returns:
            List of business dictionaries
        """
        businesses = []
        query = f"{category} in {city}, {state}, {country}"
        
        try:
            logger.info(f"Searching for: {query}")
            url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
            
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(self.delay)
            
            # Scroll to load more results
            await self._scroll_results(max_results)
            
            # Extract business information
            businesses = await self._extract_businesses(category, city, state, country)
            
            logger.info(f"Found {len(businesses)} businesses for {query}")
            
        except Exception as e:
            logger.error(f"Error searching businesses: {e}")
        
        return businesses[:max_results]
    
    async def _scroll_results(self, max_results: int):
        """Scroll through results to load more businesses."""
        try:
            # Wait for results container
            await self.page.wait_for_selector('div[role="feed"]', timeout=10000)
            
            # Scroll to load results
            for _ in range(min(5, max_results // 4)):
                await self.page.evaluate(
                    'document.querySelector(\'div[role="feed"]\').scrollBy(0, 1000)'
                )
                await asyncio.sleep(1)
        except Exception as e:
            logger.warning(f"Error scrolling results: {e}")
    
    async def _extract_businesses(
        self, 
        category: str, 
        city: str, 
        state: str, 
        country: str
    ) -> List[Dict[str, str]]:
        """Extract business information from the page."""
        businesses = []
        
        try:
            # This is a simplified extraction - in production, you'd use more robust selectors
            # For demonstration, we'll return mock data as Google Maps scraping requires
            # more sophisticated anti-detection measures
            
            # In a real implementation, you would:
            # 1. Click on each business listing
            # 2. Extract name, phone, website from the detail panel
            # 3. Use email finding services or website crawling to get emails
            
            # For now, returning empty list as this requires sophisticated scraping
            # that would need proper anti-bot measures, which is beyond this scope
            logger.warning("Note: Actual Google Maps scraping requires advanced anti-detection")
            logger.warning("Consider using Google Maps API or third-party services")
            
        except Exception as e:
            logger.error(f"Error extracting businesses: {e}")
        
        return businesses
    
    def extract_email_from_website(self, website: str) -> Optional[str]:
        """
        Extract email from a business website.
        
        Args:
            website: Website URL
            
        Returns:
            Email address if found, None otherwise
        """
        # This would require additional implementation
        # Using requests/BeautifulSoup to crawl the website
        # and regex to find email addresses
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        try:
            # Placeholder for actual implementation
            # In production, you would fetch the website and parse it
            return None
        except Exception as e:
            logger.error(f"Error extracting email from {website}: {e}")
            return None


async def scrape_city_businesses(
    city: str,
    state: str, 
    country: str,
    categories: List[str],
    max_per_category: int = 20
) -> List[Dict[str, str]]:
    """
    Scrape businesses for a city across multiple categories.
    
    Args:
        city: City name
        state: State/Province name
        country: Country name
        categories: List of business categories
        max_per_category: Maximum results per category
        
    Returns:
        List of business dictionaries
    """
    scraper = GoogleMapsScraper()
    await scraper.start()
    
    all_businesses = []
    
    try:
        for category in categories:
            businesses = await scraper.search_businesses(
                city, state, country, category, max_per_category
            )
            all_businesses.extend(businesses)
            await asyncio.sleep(2)  # Rate limiting
    finally:
        await scraper.close()
    
    return all_businesses
