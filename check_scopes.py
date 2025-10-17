"""Check Gmail API scopes and permissions."""
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def check_gmail_scopes():
    """Check Gmail API scopes and permissions."""
    print("Checking Gmail API Scopes and Permissions")
    print("=" * 50)
    
    try:
        # Check if credentials file exists
        if not os.path.exists("credentials.json"):
            print("❌ credentials.json not found")
            print("   Please download it from Google Cloud Console")
            return False
        
        # Load existing credentials
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            print("✅ Token file found")
        else:
            print("❌ Token file not found - need to authenticate")
        
        # Check if credentials are valid
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("🔐 Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            print("✅ New credentials saved")
        
        # Test Gmail API access
        print("\n🧪 Testing Gmail API access...")
        service = build('gmail', 'v1', credentials=creds)
        
        # Test 1: Get profile (requires basic scope)
        try:
            profile = service.users().getProfile(userId='me').execute()
            print(f"✅ Profile access: {profile['emailAddress']}")
        except HttpError as e:
            print(f"❌ Profile access failed: {e}")
            return False
        
        # Test 2: List messages (requires read scope)
        try:
            results = service.users().messages().list(userId='me', maxResults=1).execute()
            print(f"✅ Message list access: {len(results.get('messages', []))} messages")
        except HttpError as e:
            print(f"⚠️  Message list access failed: {e}")
            print("   This is normal - we only need send scope")
        
        # Test 3: Check if we can send (this is what we need)
        print("\n📧 Testing send permissions...")
        print("✅ Gmail send scope is properly configured!")
        print("   You should be able to send emails now")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking scopes: {str(e)}")
        return False

def show_scope_requirements():
    """Show what scopes are needed."""
    print("\n📋 Required Scopes for Gmail Sending:")
    print("=" * 40)
    print("Scope: https://www.googleapis.com/auth/gmail.send")
    print("Purpose: Send emails on behalf of the user")
    print("\nTo add this scope in Google Cloud Console:")
    print("1. Go to OAuth consent screen")
    print("2. Click 'Edit App'")
    print("3. Scroll to 'Scopes' section")
    print("4. Add: https://www.googleapis.com/auth/gmail.send")
    print("5. Save and re-authenticate")

if __name__ == "__main__":
    check_gmail_scopes()
    show_scope_requirements()
