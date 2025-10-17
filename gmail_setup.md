# Gmail Setup Guide

## Prerequisites
1. Google account with Gmail access
2. Google Cloud Console access

## Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

## Step 2: Create Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop application"
4. Download the JSON file
5. Rename it to `credentials.json` and place in project root

## Step 3: Set Up Environment
1. Copy `env_example.txt` to `.env`
2. Add your settings:
   ```
   GMAIL_CREDENTIALS_FILE=credentials.json
   GMAIL_TOKEN_FILE=token.json
   ```

## Step 4: First Run
1. Run the agent: `python main.py`
2. When prompted, authenticate with Google
3. Grant permissions for Gmail access
4. The `token.json` file will be created automatically

## Step 5: Test Gmail
Try sending a message with email keywords:
- "Send me an email"
- "Email this to someone"
- "Gmail this message"

## Troubleshooting
- **Credentials not found**: Make sure `credentials.json` is in project root
- **Authentication failed**: Delete `token.json` and try again
- **Permission denied**: Check Gmail API is enabled in Google Cloud Console
- **Email not sent**: Check recipient email address is valid

## Security Notes
- Never commit `credentials.json` or `token.json` to version control
- These files are already in `.gitignore`
- Keep your credentials secure
