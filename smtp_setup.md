# SMTP Setup Guide (No OAuth Required)

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Security > 2-Step Verification
3. Enable 2FA if not already enabled

## Step 2: Generate App Password
1. Go to Google Account settings
2. Security > 2-Step Verification > App passwords
3. Select "Mail" as the app
4. Generate the password
5. Copy the 16-character password

## Step 3: Configure Environment
1. Copy `env_example.txt` to `.env`
2. Add your credentials:
   ```
   GMAIL_EMAIL=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-16-character-app-password
   ```

## Step 4: Test Setup
1. Run: `python setup_email.py`
2. If SMTP is ready, run: `python main_smtp.py`

## Advantages of SMTP:
- ✅ No OAuth setup required
- ✅ No "unverified app" warnings
- ✅ Simpler configuration
- ✅ Works immediately

## Disadvantages:
- ❌ Less secure than OAuth
- ❌ Requires 2FA enabled
- ❌ Uses app password instead of token

## Usage:
- **OAuth method**: `python main.py`
- **SMTP method**: `python main_smtp.py`
