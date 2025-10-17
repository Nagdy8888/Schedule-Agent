# Quick Gmail Setup (Avoid Unverified App Warning)

## Method 1: Add Test Users (Easiest)

1. **Go to Google Cloud Console**
   - Navigate to your project
   - Go to "APIs & Services" > "OAuth consent screen"

2. **Add Test Users**
   - Scroll down to "Test users" section
   - Click "Add users"
   - Add your Gmail address
   - Click "Save"

3. **Keep App in Testing Mode**
   - Don't publish the app
   - Keep it in "Testing" status
   - This allows your test users to use it without verification

## Method 2: Use App Passwords (Alternative)

If you don't want to deal with OAuth, you can use App Passwords:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate password for "Mail"
3. **Use SMTP instead of Gmail API** (I can modify the code for this)

## Method 3: Request Verification (For Production)

1. **Complete OAuth Consent Screen**:
   - Add app name, logo, privacy policy
   - Add all required scopes
   - Add authorized domains

2. **Submit for Verification**:
   - Go to "OAuth consent screen"
   - Click "Publish app"
   - Submit for verification (takes 1-2 weeks)

## Recommended: Use Method 1 for Development

For learning and development, Method 1 is the easiest and fastest.
