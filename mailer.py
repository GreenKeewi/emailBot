"""
Email delivery using Gmail SMTP with rate limiting and retry logic.
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
from datetime import datetime, timedelta
import os


class Mailer:
    """Handles email delivery with rate limiting."""
    
    def __init__(self, gmail_address: str, gmail_app_password: str, 
                 from_name: str = "Arc UI Team", reply_to: str = None,
                 emails_per_hour: int = 25):
        """
        Initialize mailer.
        
        Args:
            gmail_address: Gmail address
            gmail_app_password: Gmail app password (16 characters)
            from_name: Display name for sender
            reply_to: Reply-to email address
            emails_per_hour: Maximum emails to send per hour
        """
        self.gmail_address = gmail_address
        self.gmail_app_password = gmail_app_password
        self.from_name = from_name
        self.reply_to = reply_to or gmail_address
        self.emails_per_hour = emails_per_hour
        
        # Rate limiting tracking
        self.sent_timestamps = []
        self.delay_between_emails = 3600 / emails_per_hour  # seconds between emails
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   max_retries: int = 3) -> bool:
        """
        Send an email with rate limiting and retry logic.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body
            max_retries: Maximum retry attempts
            
        Returns:
            True if sent successfully, False otherwise
        """
        # Apply rate limiting
        self._wait_for_rate_limit()
        
        # Try sending with retries
        for attempt in range(max_retries):
            try:
                # Create message
                msg = MIMEMultipart('alternative')
                msg['From'] = f"{self.from_name} <{self.gmail_address}>"
                msg['To'] = to_email
                msg['Subject'] = subject
                msg['Reply-To'] = self.reply_to
                
                # Add body
                text_part = MIMEText(body, 'plain', 'utf-8')
                msg.attach(text_part)
                
                # Connect to Gmail SMTP
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(self.gmail_address, self.gmail_app_password)
                    server.send_message(msg)
                
                # Track successful send
                self.sent_timestamps.append(datetime.now())
                print(f"✓ Email sent to {to_email}")
                return True
                
            except smtplib.SMTPAuthenticationError as e:
                print(f"✗ Authentication error: {e}")
                return False  # Don't retry auth errors
                
            except smtplib.SMTPRecipientsRefused as e:
                print(f"✗ Invalid recipient {to_email}: {e}")
                return False  # Don't retry invalid recipients
                
            except Exception as e:
                print(f"✗ Attempt {attempt + 1}/{max_retries} failed: {e}")
                
                if attempt < max_retries - 1:
                    # Wait before retry (exponential backoff)
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    return False
        
        return False
    
    def _wait_for_rate_limit(self):
        """Wait if necessary to comply with rate limits."""
        now = datetime.now()
        
        # Remove timestamps older than 1 hour
        cutoff = now - timedelta(hours=1)
        self.sent_timestamps = [ts for ts in self.sent_timestamps if ts > cutoff]
        
        # Check if we've hit the hourly limit
        if len(self.sent_timestamps) >= self.emails_per_hour:
            # Wait until the oldest email is more than an hour old
            oldest = self.sent_timestamps[0]
            wait_until = oldest + timedelta(hours=1)
            
            if now < wait_until:
                wait_seconds = (wait_until - now).total_seconds()
                print(f"⏳ Rate limit reached. Waiting {wait_seconds:.0f} seconds...")
                time.sleep(wait_seconds)
                
                # Clear old timestamps
                now = datetime.now()
                cutoff = now - timedelta(hours=1)
                self.sent_timestamps = [ts for ts in self.sent_timestamps if ts > cutoff]
        
        # Add a small delay between emails to avoid being flagged as spam
        if self.sent_timestamps:
            last_sent = self.sent_timestamps[-1]
            time_since_last = (now - last_sent).total_seconds()
            
            if time_since_last < self.delay_between_emails:
                wait_time = self.delay_between_emails - time_since_last
                time.sleep(wait_time)
    
    def get_rate_limit_status(self) -> Dict:
        """
        Get current rate limit status.
        
        Returns:
            Dictionary with rate limit information
        """
        now = datetime.now()
        cutoff = now - timedelta(hours=1)
        self.sent_timestamps = [ts for ts in self.sent_timestamps if ts > cutoff]
        
        sent_this_hour = len(self.sent_timestamps)
        remaining = max(0, self.emails_per_hour - sent_this_hour)
        
        return {
            'sent_this_hour': sent_this_hour,
            'remaining_this_hour': remaining,
            'limit': self.emails_per_hour
        }
    
    def test_connection(self) -> bool:
        """
        Test SMTP connection and authentication.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_address, self.gmail_app_password)
            print("✓ Gmail SMTP connection successful")
            return True
        except Exception as e:
            print(f"✗ Gmail SMTP connection failed: {e}")
            return False
