"""
Gmail API service for sending emails.
Uses Gmail API with OAuth2 authentication.
"""
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GmailService:
    """Service for sending emails via Gmail API."""
    
    def __init__(self):
        """Initialize Gmail service."""
        self.service = None
        self.creds = None
    
    def authenticate(self):
        """
        Authenticate with Gmail API using OAuth2.
        
        The file token.json stores the user's access and refresh tokens,
        and is created automatically when the authorization flow completes
        for the first time.
        """
        if config.TOKEN_FILE.exists():
            self.creds = Credentials.from_authorized_user_file(
                str(config.TOKEN_FILE), config.GMAIL_SCOPES
            )
        
        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not config.CREDENTIALS_FILE.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {config.CREDENTIALS_FILE}\n"
                        "Please download credentials.json from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(config.CREDENTIALS_FILE), config.GMAIL_SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(config.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
        
        try:
            self.service = build('gmail', 'v1', credentials=self.creds)
            logger.info("Gmail service authenticated successfully")
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            raise
    
    def create_message(
        self,
        to: str,
        subject: str,
        body: str,
        sender: Optional[str] = None
    ) -> dict:
        """
        Create a message for an email.
        
        Args:
            to: Email address of the receiver
            subject: The subject of the email message
            body: The text of the email message
            sender: Email address of the sender (defaults to 'me')
            
        Returns:
            An object containing a base64url encoded email object
        """
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        
        if sender:
            message['from'] = sender
        
        msg = MIMEText(body)
        message.attach(msg)
        
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        
        return {'raw': raw}
    
    def send_message(self, to: str, subject: str, body: str) -> Optional[dict]:
        """
        Send an email message.
        
        Args:
            to: Email address of receiver
            subject: Subject of the email
            body: Body of the email
            
        Returns:
            Sent Message or None if error
        """
        try:
            message = self.create_message(to, subject, body)
            sent_message = self.service.users().messages().send(
                userId='me', body=message
            ).execute()
            
            logger.info(f"Email sent successfully to {to}. Message ID: {sent_message['id']}")
            return sent_message
            
        except HttpError as error:
            logger.error(f"An error occurred sending email to {to}: {error}")
            return None
    
    def send_from_template(
        self,
        to: str,
        template_name: str,
        replacements: dict = None
    ) -> Optional[dict]:
        """
        Send an email using a template.
        
        Args:
            to: Email address of receiver
            template_name: Name of the template file
            replacements: Dictionary of placeholders to replace in template
            
        Returns:
            Sent Message or None if error
        """
        template_path = config.TEMPLATES_DIR / template_name
        
        if not template_path.exists():
            logger.error(f"Template not found: {template_path}")
            return None
        
        try:
            with open(template_path, 'r') as f:
                content = f.read()
            
            # Split content into subject and body
            lines = content.split('\n', 1)
            subject = lines[0].replace('Subject: ', '').strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            
            # Apply replacements
            if replacements:
                for key, value in replacements.items():
                    placeholder = f"{{{key}}}"
                    subject = subject.replace(placeholder, str(value))
                    body = body.replace(placeholder, str(value))
            
            return self.send_message(to, subject, body)
            
        except Exception as e:
            logger.error(f"Error sending from template: {e}")
            return None


def send_business_email(
    gmail_service: GmailService,
    business_email: str,
    business_name: str,
    template: str = None
) -> bool:
    """
    Send an email to a business.
    
    Args:
        gmail_service: Authenticated Gmail service
        business_email: Business email address
        business_name: Business name
        template: Template file name (defaults to config.DEFAULT_TEMPLATE)
        
    Returns:
        True if sent successfully, False otherwise
    """
    if template is None:
        template = config.DEFAULT_TEMPLATE
    
    replacements = {
        'business_name': business_name,
        'name': business_name,
    }
    
    result = gmail_service.send_from_template(
        business_email,
        template,
        replacements
    )
    
    return result is not None
