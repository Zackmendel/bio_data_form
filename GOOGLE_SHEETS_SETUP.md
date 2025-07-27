# Google Sheets Setup Guide

Follow these steps to configure Google Sheets integration for the Staff Biodata App:

## 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing (required for API usage)

## 2. Enable Google Sheets API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"

## 3. Create a Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `staff-biodata-app`
   - Description: `Service account for staff biodata collection`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

## 4. Generate Service Account Key

1. In the Credentials page, find your service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Download the JSON file
7. Rename it to `service_account_key.json`
8. Place it in the same directory as your `staff_biodata_app.py` file

## 5. Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "EduRepublic Staff Biodata" (or any name you prefer)
4. Copy the spreadsheet ID from the URL:
   - The URL will look like: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part

## 6. Share the Sheet with Service Account

1. In your Google Sheet, click "Share" (top right)
2. Add the service account email (found in the JSON file under `client_email`)
3. Give it "Editor" permissions
4. Click "Send" (you can uncheck "Notify people")

## 7. Update the Code

1. Open `staff_biodata_app.py`
2. Find this line: `SPREADSHEET_ID = 'your_spreadsheet_id_here'`
3. Replace `'your_spreadsheet_id_here'` with your actual spreadsheet ID

## 8. Install Dependencies

Run this command in your terminal:
```bash
pip install -r requirements.txt
```

## 9. Run the App

```bash
streamlit run staff_biodata_app.py
```

## Security Notes

- Keep your `service_account_key.json` file secure and never commit it to version control
- Add `service_account_key.json` to your `.gitignore` file
- The service account has access to your Google Sheet, so keep the credentials safe

## Troubleshooting

- **"Service account key file not found"**: Make sure `service_account_key.json` is in the same directory as your script
- **"Permission denied"**: Make sure you've shared the Google Sheet with the service account email
- **"Spreadsheet not found"**: Check that the `SPREADSHEET_ID` is correct
- **"API not enabled"**: Make sure Google Sheets API is enabled in your Google Cloud project

## Example service_account_key.json structure

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
}
``` 