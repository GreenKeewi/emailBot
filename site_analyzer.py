"""
Website analysis for identifying improvement opportunities.
Analyzes site content, UX, and design.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import json


class SiteAnalyzer:
    """Analyzes websites for UX and design issues."""
    
    def __init__(self):
        """Initialize site analyzer."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_website(self, url: str, business_name: str = "", timeout: int = 10) -> Optional[str]:
        """
        Analyze a website and generate findings.
        
        Args:
            url: Website URL
            business_name: Business name for context
            timeout: Request timeout
            
        Returns:
            JSON string with analysis findings or None
        """
        if not url:
            return None
        
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            analysis = {
                'url': url,
                'business_name': business_name,
                'issues': [],
                'observations': []
            }
            
            # Check for mobile responsiveness meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                analysis['issues'].append("No mobile viewport meta tag - site may not be mobile-friendly")
            
            # Check for clear CTAs
            cta_buttons = soup.find_all(['button', 'a'], class_=lambda x: x and any(
                word in str(x).lower() for word in ['cta', 'call-to-action', 'contact', 'quote', 'book']
            ))
            
            if len(cta_buttons) < 2:
                analysis['issues'].append("Limited or unclear calls-to-action (CTAs)")
            
            # Check page title
            title = soup.find('title')
            if not title or len(title.text.strip()) < 10:
                analysis['issues'].append("Missing or inadequate page title")
            else:
                analysis['observations'].append(f"Page title: {title.text.strip()[:100]}")
            
            # Check for contact information
            text = soup.get_text().lower()
            has_phone = any(word in text for word in ['phone', 'call', 'tel:', '('])
            has_email = '@' in text or 'email' in text
            has_address = any(word in text for word in ['address', 'location', 'visit us'])
            
            contact_methods = sum([has_phone, has_email, has_address])
            if contact_methods < 2:
                analysis['issues'].append("Limited contact information visible")
            
            # Check for images
            images = soup.find_all('img')
            if len(images) < 3:
                analysis['issues'].append("Few images - site may look bare")
            
            # Check for modern design indicators
            has_modern_css = soup.find_all('link', rel='stylesheet')
            if len(has_modern_css) == 0:
                analysis['issues'].append("No external stylesheets detected - may have outdated design")
            
            # Check navigation
            nav = soup.find_all(['nav', 'header'])
            if not nav:
                analysis['issues'].append("No clear navigation structure found")
            
            # Check for SSL
            if not url.startswith('https://'):
                analysis['issues'].append("Site not using HTTPS - security concern")
            
            # Observe what they offer
            headings = soup.find_all(['h1', 'h2', 'h3'])
            if headings:
                main_heading = headings[0].text.strip()[:150]
                analysis['observations'].append(f"Main message: {main_heading}")
            
            # Check for social media links
            social_links = soup.find_all('a', href=lambda x: x and any(
                social in str(x).lower() for social in ['facebook', 'twitter', 'instagram', 'linkedin']
            ))
            
            if len(social_links) > 0:
                analysis['observations'].append(f"Has {len(social_links)} social media links")
            
            # Performance observation
            page_size = len(response.content)
            if page_size > 3000000:  # 3MB
                analysis['issues'].append("Large page size may cause slow loading")
            
            return json.dumps(analysis)
            
        except Exception as e:
            return json.dumps({
                'url': url,
                'business_name': business_name,
                'error': str(e),
                'issues': ['Unable to analyze website'],
                'observations': []
            })
    
    def get_key_findings(self, analysis_json: str) -> str:
        """
        Extract key findings from analysis for email generation.
        
        Args:
            analysis_json: JSON string from analyze_website
            
        Returns:
            Human-readable summary of findings
        """
        try:
            analysis = json.loads(analysis_json)
            
            findings = []
            
            # Prioritize top issues
            issues = analysis.get('issues', [])
            if issues:
                findings.append("I noticed a few areas where your website could be improved:")
                findings.extend([f"• {issue}" for issue in issues[:3]])  # Top 3 issues
            
            # Add observations
            observations = analysis.get('observations', [])
            if observations:
                findings.append("\nI saw that " + observations[0].lower())
            
            return "\n".join(findings) if findings else "I visited your website"
            
        except:
            return "I visited your website"
