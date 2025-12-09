# Gmail API Setup Guide

This guide provides detailed instructions for setting up Gmail API credentials for the AuditBot application.

## Overview

AuditBot uses the Gmail API with OAuth 2.0 authentication to send emails. This is more secure and reliable than using SMTP with app passwords.

## Prerequisites

- Google account
- Access to Google Cloud Console
- Project directory set up with AuditBot code

## Step-by-Step Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Enter a project name (e.g., "AuditBot Email Service")
5. Click "Create"
6. Wait for the project to be created (this may take a few seconds)

### Step 2: Enable Gmail API

1. Make sure your new project is selected in the dropdown
2. Navigate to "APIs & Services" > "Library" (use the left sidebar menu)
3. Search for "Gmail API"
4. Click on "Gmail API" in the results
5. Click the "Enable" button
6. Wait for the API to be enabled

### Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" > "OAuth consent screen"
2. Select "External" user type (unless you have a Google Workspace account)
3. Click "Create"

4. Fill in the OAuth consent screen:
   - **App name:** AuditBot Email Service
   - **User support email:** Your email address
   - **Developer contact email:** Your email address
   - Leave other fields as default
5. Click "Save and Continue"

6. On the "Scopes" screen:
   - Click "Add or Remove Scopes"
   - Search for "Gmail API"
   - Select the scope: `https://www.googleapis.com/auth/gmail.send`
   - Click "Update"
   - Click "Save and Continue"

7. On the "Test users" screen:
   - Click "Add Users"
   - Enter your Gmail address (the one you'll use to send emails)
   - Click "Add"
   - Click "Save and Continue"

8. Review the summary and click "Back to Dashboard"

### Step 4: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" at the top
3. Select "OAuth client ID"

4. Configure the OAuth client:
   - **Application type:** Desktop app
   - **Name:** AuditBot Desktop Client
   - Click "Create"

5. A dialog will appear with your credentials
   - Click "Download JSON"
   - This downloads a file named something like `client_secret_XXXXX.json`

### Step 5: Set Up Credentials in AuditBot

1. Rename the downloaded file to `credentials.json`
2. Move it to the root directory of your AuditBot project:
   ```
   auditBot/
   ├── credentials.json  ← Place it here
   ├── main.py
   ├── config.py
   └── ...
   ```

3. Verify the file is in the correct location:
   ```bash
   # On Windows
   dir credentials.json
   
   # On macOS/Linux
   ls -l credentials.json
   ```

### Step 6: First-Time Authentication

1. Run the application for the first time:
   ```bash
   python main.py --uno
   ```

2. The application will:
   - Detect no existing token
   - Open your default web browser
   - Show Google's OAuth consent screen

3. In the browser:
   - Select your Google account
   - You may see a warning "Google hasn't verified this app"
   - Click "Advanced" → "Go to AuditBot Email Service (unsafe)"
   - Review the permissions (ability to send emails)
   - Click "Allow"

4. The browser will show "The authentication flow has completed"
5. Return to your terminal - authentication is complete
6. A `token.json` file is created in your project directory

### Step 7: Verify Setup

1. Check that `token.json` was created:
   ```bash
   # On Windows
   dir token.json
   
   # On macOS/Linux
   ls -l token.json
   ```

2. Test sending (you'll need cities and businesses data):
   ```bash
   python main.py --stats
   ```

3. If you see statistics without errors, setup is complete!

## File Security

⚠️ **IMPORTANT: Keep these files secure and private!**

### Files to Keep Secret

1. **credentials.json** - Contains your OAuth client ID and secret
2. **token.json** - Contains your access and refresh tokens

### Security Best Practices

1. **Never commit credentials to Git**
   - The `.gitignore` file already excludes these
   - Verify with: `git status` (shouldn't show credentials.json or token.json)

2. **Never share these files**
   - Don't upload to public repositories
   - Don't share in emails or chat
   - Don't include in screenshots

3. **Protect the files**
   ```bash
   # On macOS/Linux, restrict permissions
   chmod 600 credentials.json
   chmod 600 token.json
   ```

4. **If compromised**
   - Go to Google Cloud Console
   - Delete the OAuth client
   - Create new credentials
   - Remove and re-authorize

## Token Refresh

The OAuth token automatically refreshes when needed. If you encounter authentication errors:

1. Delete `token.json`
2. Run the application again
3. Complete the browser authentication flow

## Common Issues and Solutions

### Issue: "Credentials file not found"

**Solution:**
- Verify `credentials.json` is in the project root
- Check the filename is exactly `credentials.json`
- Ensure it's a valid JSON file (open in text editor to verify)

### Issue: "Access blocked: This app's request is invalid"

**Solution:**
- Ensure you've enabled the Gmail API
- Verify the OAuth consent screen is configured
- Check that the redirect URI matches

### Issue: "The caller does not have permission"

**Solution:**
- Add yourself as a test user in the OAuth consent screen
- Verify the Gmail API scope is added
- Re-authenticate by deleting `token.json`

### Issue: "invalid_grant" error

**Solution:**
- Delete `token.json`
- Run the app again to re-authenticate
- If persists, create new OAuth credentials

### Issue: Browser doesn't open automatically

**Solution:**
- Copy the URL from the terminal
- Paste it into your browser manually
- Complete the authentication
- Return to the terminal

## Publishing Your App (Optional)

If you want to use this app without the "unverified app" warning:

1. Complete the OAuth consent screen verification process
2. Provide privacy policy and terms of service
3. Submit for Google verification
4. Wait for approval (can take several days)

**Note:** This is only necessary if distributing to others. For personal use, the "unsafe" warning is normal and okay to bypass.

## Alternative: Service Account (Advanced)

For automated environments without browser access, consider using a Service Account:

1. Create a Service Account in Google Cloud Console
2. Enable Domain-Wide Delegation
3. Grant necessary scopes in Google Workspace Admin
4. Use service account credentials instead of OAuth

**Note:** This requires Google Workspace and administrative access.

## API Quotas and Limits

Gmail API has usage quotas:

- **Free tier:** 1,000,000,000 quota units per day
- **Sending emails:** 100 units per email
- **Effective limit:** ~10,000,000 emails per day

To check your usage:
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" > "Dashboard"
3. Click on "Gmail API"
4. View "Quotas" tab

## Support

If you encounter issues:

1. Check the [Google Gmail API documentation](https://developers.google.com/gmail/api)
2. Review [OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2)
3. Visit [Google Cloud Console Help](https://cloud.google.com/support)

## Summary Checklist

- [ ] Created Google Cloud project
- [ ] Enabled Gmail API
- [ ] Configured OAuth consent screen
- [ ] Added test users
- [ ] Created OAuth 2.0 credentials
- [ ] Downloaded and renamed to `credentials.json`
- [ ] Placed `credentials.json` in project root
- [ ] Completed first-time authentication
- [ ] Verified `token.json` was created
- [ ] Tested with `--stats` command
- [ ] Verified files are in `.gitignore`

---

**You're all set! Your Gmail API is configured and ready to use. 🎉**
