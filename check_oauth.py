"""Check OAuth configuration and provide fix instructions."""
import os
import json

def check_oauth_setup():
    """Check OAuth setup and provide instructions."""
    print("OAuth Configuration Check")
    print("=" * 40)
    
    # Check credentials file
    if os.path.exists("credentials.json"):
        print("SUCCESS: credentials.json found")
        
        # Try to read and show the client info
        try:
            with open("credentials.json", "r") as f:
                creds = json.load(f)
            
            if "web" in creds:
                client_id = creds["web"].get("client_id", "Not found")
                print(f"Client ID: {client_id[:20]}...")
            else:
                print("WARNING: credentials.json format unexpected")
                
        except Exception as e:
            print(f"ERROR reading credentials.json: {e}")
    else:
        print("ERROR: credentials.json not found")
        print("Download it from Google Cloud Console > APIs & Services > Credentials")
        return False
    
    # Check token file
    if os.path.exists("token.json"):
        print("SUCCESS: token.json found")
    else:
        print("INFO: token.json not found (will be created on first run)")
    
    print("\nOAuth Consent Screen Configuration:")
    print("=" * 40)
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Select your project")
    print("3. Navigate to: APIs & Services > OAuth consent screen")
    print("4. Click 'Edit App'")
    print("5. Scroll to 'Scopes' section")
    print("6. Click 'Add or Remove Scopes'")
    print("7. Search for 'Gmail API'")
    print("8. Select: 'Send email on behalf of the user'")
    print("9. Click 'Update'")
    print("10. Save the OAuth consent screen")
    
    print("\nRequired Scope:")
    print("https://www.googleapis.com/auth/gmail.send")
    
    print("\nAfter updating scopes:")
    print("1. Delete token.json: del token.json")
    print("2. Run agent: python main.py")
    print("3. Authenticate when prompted")
    
    return True

if __name__ == "__main__":
    check_oauth_setup()
