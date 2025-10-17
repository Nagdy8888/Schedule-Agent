"""SMTP service for sending emails (no OAuth required)."""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from config import GMAIL_CREDENTIALS_FILE

class SMTPService:
    """SMTP service for sending emails via Gmail SMTP."""
    
    def __init__(self):
        """Initialize SMTP service."""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email = None
        self.password = None
        self.load_credentials()
    
    def load_credentials(self):
        """Load email credentials from environment or config."""
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        # Try to get from environment variables
        self.email = os.getenv("GMAIL_EMAIL")
        self.password = os.getenv("GMAIL_APP_PASSWORD")  # App password, not regular password
        
        if not self.email or not self.password:
            print("❌ Gmail credentials not found. Please set GMAIL_EMAIL and GMAIL_APP_PASSWORD in .env")
            print("   GMAIL_EMAIL=your-email@gmail.com")
            print("   GMAIL_APP_PASSWORD=your-app-password")
    
    def send_email(self, to: str, subject: str, body: str, from_email: str = None) -> bool:
        """Send email via SMTP."""
        try:
            if not self.email or not self.password:
                print("❌ SMTP credentials not configured")
                return False
            
            if not from_email:
                from_email = self.email
            
            print(f"📧 Sending email via SMTP to: {to}")
            print(f"📝 Subject: {subject}")
            
            # Create message
            message = MIMEMultipart()
            message["From"] = from_email
            message["To"] = to
            message["Subject"] = subject
            
            # Add body
            message.attach(MIMEText(body, "plain"))
            
            # Create secure connection
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.email, self.password)
                server.sendmail(from_email, to, message.as_string())
            
            print("✅ Email sent successfully via SMTP!")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email via SMTP: {str(e)}")
            return False
    
    def is_available(self) -> bool:
        """Check if SMTP service is available."""
        return self.email is not None and self.password is not None


# Global SMTP service instance
smtp_service = None

def get_smtp_service() -> SMTPService:
    """Get or create SMTP service instance."""
    global smtp_service
    if smtp_service is None:
        smtp_service = SMTPService()
    return smtp_service
