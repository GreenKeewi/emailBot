"""
Business discovery using Google Maps/Places API.
Extracts business information and emails from websites.
"""

import os
import time
import re
import requests
from typing import List, Dict, Optional
from urllib.parse import urlparse
import googlemaps
from bs4 import BeautifulSoup
import validators


class Scraper:
    """Scrapes business data from Google Maps and websites."""
    
    def __init__(self, api_key: str):
        """
        Initialize scraper with Google Maps API key.
        
        Args:
            api_key: Google Maps API key
        """
        self.gmaps = googlemaps.Client(key=api_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_businesses(self, latitude: float, longitude: float, radius: int, 
                         category: str, max_results: int = 60) -> List[Dict]:
        """
        Search for businesses using Google Places API.
        
        Args:
            latitude: Search center latitude
            longitude: Search center longitude
            radius: Search radius in meters
            category: Business category (e.g., 'plumber', 'restaurant')
            max_results: Maximum number of results to return
            
        Returns:
            List of business dictionaries
        """
        businesses = []
        seen_place_ids = set()
        
        try:
            # Use places_nearby for location-based search
            location = (latitude, longitude)
            
            # Initial search
            results = self.gmaps.places_nearby(
                location=location,
                radius=radius,
                keyword=category,
                rank_by=None
            )
            
            # Process initial results
            for place in results.get('results', []):
                if place['place_id'] not in seen_place_ids:
                    seen_place_ids.add(place['place_id'])
                    business = self._extract_business_info(place)
                    if business:
                        businesses.append(business)
            
            # Handle pagination
            page_token = results.get('next_page_token')
            while page_token and len(businesses) < max_results:
                time.sleep(2)  # Required delay for next_page_token
                
                try:
                    results = self.gmaps.places_nearby(
                        location=location,
                        radius=radius,
                        page_token=page_token
                    )
                    
                    for place in results.get('results', []):
                        if place['place_id'] not in seen_place_ids:
                            seen_place_ids.add(place['place_id'])
                            business = self._extract_business_info(place)
                            if business:
                                businesses.append(business)
                    
                    page_token = results.get('next_page_token')
                except Exception as e:
                    print(f"Pagination error: {e}")
                    break
            
        except Exception as e:
            print(f"Search error: {e}")
        
        return businesses[:max_results]
    
    def _extract_business_info(self, place: Dict) -> Optional[Dict]:
        """
        Extract relevant business information from a place result.
        
        Args:
            place: Place result from Google Maps API
            
        Returns:
            Business dictionary or None
        """
        try:
            place_id = place.get('place_id')
            
            # Get detailed place information
            details = self.gmaps.place(place_id, fields=[
                'name', 'website', 'formatted_address', 'formatted_phone_number',
                'geometry', 'types'
            ])
            
            result = details.get('result', {})
            
            business = {
                'name': result.get('name', ''),
                'website': result.get('website'),
                'address': result.get('formatted_address', ''),
                'phone': result.get('formatted_phone_number'),
                'latitude': result.get('geometry', {}).get('location', {}).get('lat'),
                'longitude': result.get('geometry', {}).get('location', {}).get('lng'),
                'types': result.get('types', [])
            }
            
            # Extract email from website if available
            if business['website']:
                business['email'] = self.extract_email_from_website(business['website'])
            
            return business
            
        except Exception as e:
            print(f"Error extracting business info: {e}")
            return None
    
    def extract_email_from_website(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        Extract email address from a website.
        
        Args:
            url: Website URL
            timeout: Request timeout in seconds
            
        Returns:
            Email address or None
        """
        if not url or not validators.url(url):
            return None
        
        try:
            # Try to fetch the homepage
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for email in common places
            emails = set()
            
            # Method 1: Look for mailto: links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('mailto:'):
                    email = href.replace('mailto:', '').split('?')[0]
                    emails.add(email.lower())
            
            # Method 2: Look for email patterns in text
            text = soup.get_text()
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, text)
            
            for email in found_emails:
                # Filter out common false positives
                if not any(x in email.lower() for x in ['example.com', 'domain.com', 'email.com', 'sentry.io', 'wixpress.com']):
                    emails.add(email.lower())
            
            # Try contact page
            if not emails:
                contact_links = soup.find_all('a', href=True)
                for link in contact_links:
                    href = link['href'].lower()
                    if any(word in href for word in ['contact', 'about', 'reach']):
                        try:
                            contact_url = self._build_absolute_url(url, link['href'])
                            if contact_url and contact_url != url:
                                contact_email = self._extract_from_page(contact_url, timeout)
                                if contact_email:
                                    emails.add(contact_email)
                                    break
                        except:
                            continue
            
            # Return the first reasonable email found
            for email in sorted(emails):
                if self._is_valid_email(email):
                    return email
            
            return None
            
        except Exception as e:
            print(f"Error extracting email from {url}: {e}")
            return None
    
    def _extract_from_page(self, url: str, timeout: int) -> Optional[str]:
        """Extract email from a specific page."""
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for mailto links
            for link in soup.find_all('a', href=True):
                if link['href'].startswith('mailto:'):
                    email = link['href'].replace('mailto:', '').split('?')[0]
                    if self._is_valid_email(email):
                        return email.lower()
            
            # Look for email patterns
            text = soup.get_text()
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, text)
            
            for email in found_emails:
                if self._is_valid_email(email):
                    return email.lower()
            
        except:
            pass
        
        return None
    
    def _build_absolute_url(self, base_url: str, relative_url: str) -> Optional[str]:
        """Build absolute URL from base and relative URLs."""
        try:
            parsed_base = urlparse(base_url)
            
            if relative_url.startswith('http'):
                return relative_url
            elif relative_url.startswith('//'):
                return f"{parsed_base.scheme}:{relative_url}"
            elif relative_url.startswith('/'):
                return f"{parsed_base.scheme}://{parsed_base.netloc}{relative_url}"
            else:
                return f"{parsed_base.scheme}://{parsed_base.netloc}/{relative_url}"
        except:
            return None
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email address."""
        if not email or '@' not in email:
            return False
        
        # Filter out obvious invalid patterns
        invalid_patterns = [
            'example.com', 'domain.com', 'email.com', 'test.com',
            'yoursite.com', 'yourdomain.com', 'sentry.io', 'wixpress.com',
            '.png', '.jpg', '.gif', '.css', '.js'
        ]
        
        email_lower = email.lower()
        
        for pattern in invalid_patterns:
            if pattern in email_lower:
                return False
        
        # Basic email validation
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return bool(re.match(pattern, email))
