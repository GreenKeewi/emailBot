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
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
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
You are a B2B outreach assistant for ArcUI (https://arc-ui.vercel.app).
Your goal is to write a short, professional, high-conversion cold email to a local business owner.

Input data:
- Business Name: {business_name}
- Owner Name: {business.get('owner_name', 'Owner')}
- Industry: {category}
- City / Province: {city}
- Website URL: {website}
- Visible website issues: {findings if findings else "General improvements needed"}

Instructions:
Personalize the opening line using the business name or website
Mention 1–2 realistic website problems if a site exists
Position ArcUI as a done-for-you website service
Emphasize:
$99 flat monthly
No setup fees
Unlimited edits
Cancel anytime
Do NOT sound salesy or corporate
Keep the email under 170 words
End with an offer for a free homepage preview
Use confident, calm language — not hype
Always frame one-page or simple sites as a performance advantage, not a limitation
Never say “we don’t do multi-page sites” directly
Use phrases like focused, simple, fast, conversion-driven
Create a curiosity-driven subject line (short, relevant)
Keep bullet points tight and scannable
Avoid repetition

Reference this email template structure:
Subject: Question about [Business Name]

Hi [Owner Name],

I was looking at [Business Name] and noticed a few things on your website that might be costing you real leads—especially on mobile.

We see a common pattern with [Industry] sites:
They look fine, but load slowly and hide the contact button, so visitors don't call.

That’s why we built ArcUI.

We design, host, and maintain high-converting business websites for a flat $99/month.
No setup fees. No contracts. Unlimited edits.

Why this works better than Wix or WordPress:
• Instant load speeds (critical for mobile)
• Layouts built to convert calls, not just look nice
• We handle hosting, security, and updates
• Cancel anytime — we earn your business monthly

We recently helped a [Industry] business increase inbound leads by 40% with this approach.

If you want, I can build you a free homepage preview so you can see exactly what your site could look like — no commitment.

Worth a quick look?

Best,
Taha
ArcUI
https://arc-ui.vercel.app

P.S. We’re only onboarding 5 new businesses this month to keep quality high.

Output:
Return ONLY the final email text including the Subject line.
No explanations. No markdown.
Format as:
Subject: [Subject Text]
[Body Text]
"""
        
        try:
            response = self.model.generate_content(prompt)
            email_text = response.text
            
            # Parse the response
            parts = email_text.split('\n', 1)
            subject = "Website Upgrade"
            body = email_text
            
            if email_text.lower().startswith('subject:'):
                # Split into subject and body
                lines = email_text.split('\n')
                subject = lines[0].replace('Subject:', '').strip()
                body = '\n'.join(lines[1:]).strip()
            
            return {'subject': subject, 'body': body}
            
        except Exception as e:
            print(f"Error generating email: {e}")
            return {
                'subject': f"Question about {business_name}",
                'body': f"Hi,\n\nI came across {business_name} and wanted to connect..."
            }
            
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
