"""
AI-powered email generation using Google Gemini.
Creates personalized outreach emails based on business analysis.
"""

import google.generativeai as genai
from typing import Dict, Optional
import json


class AIWriter:
    """Generates personalized emails using Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize AI writer with Gemini API key.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_email(self, business: Dict, site_analysis: str = None, 
                      from_name: str = "Arc UI Team") -> Dict[str, str]:
        """
        Generate a personalized email for a business.
        
        Args:
            business: Business dictionary with name, city, category, website
            site_analysis: JSON string from site analyzer
            from_name: Sender name
            
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        business_name = business.get('name', 'Business')
        city = business.get('city', '')
        website = business.get('website', '')
        category = business.get('category', 'business')
        
        # Extract key findings from site analysis
        findings = ""
        if site_analysis:
            try:
                analysis = json.loads(site_analysis)
                issues = analysis.get('issues', [])
                observations = analysis.get('observations', [])
                
                if issues:
                    findings += "Website observations:\n"
                    findings += "\n".join([f"- {issue}" for issue in issues[:3]])
                
                if observations and len(observations) > 0:
                    findings += f"\n\nI noticed: {observations[0]}"
            except:
                findings = "I visited your website"
        
        # Create prompt for Gemini
        prompt = f"""
You are writing a personalized business outreach email for Arc UI, a web development service.

Business Details:
- Business Name: {business_name}
- City: {city}
- Industry: {category}
- Website: {website}

{findings if findings else "I visited their website"}

Write a professional, personalized cold email that:
1. Addresses the business by name and mentions their city
2. References what they do (their industry/service)
3. If website observations are provided, briefly mention 1-2 specific observations (keep it subtle and helpful, not critical)
4. Introduces Arc UI (https://arc-ui.vercel.app/) as a full-service web solution
5. Highlights the offer: $99/month for website, hosting, updates, and maintenance - "we handle everything"
6. Keeps a friendly, helpful tone (not salesy)
7. Is concise (under 150 words)
8. Ends with a soft call-to-action
9. Includes an unsubscribe line at the bottom

Format your response as:
SUBJECT: [email subject line]

BODY:
[email body]

Keep the email personalized but professional. Don't be too pushy.
"""
        
        try:
            response = self.model.generate_content(prompt)
            email_text = response.text
            
            # Parse the response
            parts = email_text.split('BODY:', 1)
            
            if len(parts) == 2:
                subject_part = parts[0].replace('SUBJECT:', '').strip()
                body_part = parts[1].strip()
            else:
                # Fallback if format is different
                subject_part = f"Website Solutions for {business_name}"
                body_part = email_text
            
            # Ensure unsubscribe line is present
            if 'unsubscribe' not in body_part.lower():
                body_part += "\n\n---\nIf you'd prefer not to receive emails from us, please reply with 'unsubscribe' in the subject line."
            
            return {
                'subject': subject_part,
                'body': body_part
            }
            
        except Exception as e:
            print(f"Error generating email with AI: {e}")
            # Fallback to template
            return self._generate_template_email(business_name, city, category, website, findings)
    
    def _generate_template_email(self, business_name: str, city: str, 
                                 category: str, website: str, findings: str) -> Dict[str, str]:
        """Generate a template-based email as fallback."""
        
        subject = f"Quick question about {business_name}'s website"
        
        body = f"""Hi {business_name} team,

I came across your {category} business in {city} and wanted to reach out.

{findings if findings else f"I visited {website} and"} thought you might be interested in what we offer at Arc UI.

We provide a complete web solution for $99/month that includes:
• Modern, professional website design
• Reliable hosting
• Regular updates and maintenance
• Everything handled for you

Many {category} businesses in {city} work with us to strengthen their online presence without the hassle of managing it themselves.

Would you be open to a quick conversation about how we could help {business_name}?

Best regards,
Arc UI Team
https://arc-ui.vercel.app/

---
To unsubscribe, reply with 'unsubscribe' in the subject line.
"""
        
        return {
            'subject': subject,
            'body': body
        }
