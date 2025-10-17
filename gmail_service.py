"""Gmail service for sending emails."""
import os
import json
from typing import Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    """Service class for Gmail API interactions."""
    
    def __init__(self):
        """Initialize Gmail service."""
        self.service = None
        self.credentials = None
        self.setup_gmail_service()
    
    def setup_gmail_service(self):
        """Set up Gmail API service."""
        try:
            # Load credentials
            self.credentials = self.load_credentials()
            
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    self.credentials = self.authenticate()
                
                # Save credentials
                self.save_credentials()
            
            # Build Gmail service
            self.service = build('gmail', 'v1', credentials=self.credentials)
            print("✅ Gmail service initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up Gmail service: {str(e)}")
            self.service = None
    
    def load_credentials(self) -> Optional[Credentials]:
        """Load existing credentials from token file."""
        try:
            if os.path.exists(GMAIL_TOKEN_FILE):
                return Credentials.from_authorized_user_file(GMAIL_TOKEN_FILE, SCOPES)
        except Exception as e:
            print(f"❌ Error loading credentials: {str(e)}")
        return None
    
    def save_credentials(self):
        """Save credentials to token file."""
        try:
            with open(GMAIL_TOKEN_FILE, 'w') as token:
                token.write(self.credentials.to_json())
            print("💾 Credentials saved to token file")
        except Exception as e:
            print(f"❌ Error saving credentials: {str(e)}")
    
    def authenticate(self) -> Credentials:
        """Authenticate with Google OAuth2."""
        if not os.path.exists(GMAIL_CREDENTIALS_FILE):
            raise FileNotFoundError(f"Credentials file not found: {GMAIL_CREDENTIALS_FILE}")
        
        flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        return credentials
    
    def create_message(self, to: str, subject: str, body: str, from_email: str = None) -> Dict[str, str]:
        """Create a Gmail message."""
        if not from_email:
            # Get the authenticated user's email
            profile = self.service.users().getProfile(userId='me').execute()
            from_email = profile['emailAddress']
        
        message = f"""To: {to}
From: {from_email}
Subject: {subject}

{body}"""
        
        # Encode message
        import base64
        message_bytes = message.encode('utf-8')
        message_b64 = base64.urlsafe_b64encode(message_bytes).decode('utf-8')
        
        return {
            'raw': message_b64
        }
    
    def send_email(self, to: str, subject: str, body: str, from_email: str = None) -> bool:
        """Send an email via Gmail API."""
        try:
            if not self.service:
                print("❌ Gmail service not initialized")
                return False
            
            print(f"📧 Preparing to send email to: {to}")
            print(f"📝 Subject: {subject}")
            
            # Create message
            message = self.create_message(to, subject, body, from_email)
            
            # Send message
            result = self.service.users().messages().send(
                userId='me',
                body=message
            ).execute()
            
            print(f"✅ Email sent successfully! Message ID: {result['id']}")
            return True
            
        except HttpError as error:
            print(f"❌ Gmail API error: {error}")
            return False
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def is_available(self) -> bool:
        """Check if Gmail service is available."""
        return self.service is not None


# Global Gmail service instance
gmail_service = None

def get_gmail_service() -> GmailService:
    """Get or create Gmail service instance."""
    global gmail_service
    if gmail_service is None:
        gmail_service = GmailService()
    return gmail_service
