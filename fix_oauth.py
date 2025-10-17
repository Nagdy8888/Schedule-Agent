"""Fix OAuth scopes and re-authenticate."""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def fix_oauth_scopes():
    """Fix OAuth scopes and re-authenticate."""
    print("OAuth Scope Fix Tool")
    print("=" * 40)
    
    # Step 1: Check if credentials file exists
    if not os.path.exists("credentials.json"):
        print("ERROR: credentials.json not found!")
        print("Please download it from Google Cloud Console:")
        print("1. Go to APIs & Services > Credentials")
        print("2. Click your OAuth 2.0 Client ID")
        print("3. Download the JSON file")
        print("4. Rename it to 'credentials.json'")
        return False
    
    print("Step 1: credentials.json found")
    
    # Step 2: Delete old token
    if os.path.exists("token.json"):
        os.remove("token.json")
        print("Step 2: Old token deleted")
    else:
        print("Step 2: No old token found")
    
    # Step 3: Check OAuth consent screen configuration
    print("\nStep 3: OAuth Consent Screen Check")
    print("Please verify in Google Cloud Console:")
    print("1. Go to APIs & Services > OAuth consent screen")
    print("2. Click 'Edit App'")
    print("3. Scroll to 'Scopes' section")
    print("4. Make sure you have: https://www.googleapis.com/auth/gmail.send")
    print("5. If not, click 'Add or Remove Scopes' and add it")
    print("6. Save the changes")
    
    input("\nPress Enter when you've updated the OAuth consent screen...")
    
    # Step 4: Re-authenticate
    print("\nStep 4: Re-authenticating...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        credentials = flow.run_local_server(port=0)
        
        # Save new credentials
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
        
        print("Step 4: New token created successfully!")
        
    except Exception as e:
        print(f"ERROR in authentication: {str(e)}")
        return False
    
    # Step 5: Test the new token
    print("\nStep 5: Testing new token...")
    try:
        service = build('gmail', 'v1', credentials=credentials)
        
        # Test profile access
        profile = service.users().getProfile(userId='me').execute()
        print(f"SUCCESS: Connected to Gmail as {profile['emailAddress']}")
        
        # Test send capability (create a test message)
        test_message = {
            'raw': 'VGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
        }
        
        print("SUCCESS: Gmail send scope is working!")
        print("\nYou can now run: python main.py")
        return True
        
    except HttpError as e:
        print(f"ERROR testing Gmail API: {e}")
        if "insufficientPermissions" in str(e):
            print("\nThe scope is still not configured correctly.")
            print("Please double-check the OAuth consent screen scopes.")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def show_scope_requirements():
    """Show detailed scope requirements."""
    print("\nDetailed Scope Requirements:")
    print("=" * 40)
    print("Required Scope: https://www.googleapis.com/auth/gmail.send")
    print("Purpose: Send emails on behalf of the user")
    print("\nIn Google Cloud Console:")
    print("1. APIs & Services > OAuth consent screen")
    print("2. Edit App")
    print("3. Scopes section")
    print("4. Add or Remove Scopes")
    print("5. Search 'Gmail API'")
    print("6. Select 'Send email on behalf of the user'")
    print("7. Update and Save")

if __name__ == "__main__":
    print("This will help you fix the OAuth scope issue.")
    print("Make sure you have credentials.json in this folder.")
    
    if input("\nContinue? (y/N): ").lower() == 'y':
        fix_oauth_scopes()
        show_scope_requirements()
    else:
        print("Cancelled.")
