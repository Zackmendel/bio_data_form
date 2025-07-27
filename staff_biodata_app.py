import streamlit as st
import pandas as pd
from datetime import datetime
import os
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
import json

# Google Sheets API setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Configuration from Streamlit secrets
SERVICE_ACCOUNT_FILE = st.secrets.get('SERVICE_ACCOUNT_FILE', 'service_account_key.json')
SPREADSHEET_ID = st.secrets.get('SPREADSHEET_ID', 'your_spreadsheet_id_here')
WORKSHEET_NAME = 'Staff Biodata'

def get_google_sheets_client():
    """Initialize and return Google Sheets client"""
    try:
        # Check if service account credentials are in secrets
        if 'SERVICE_ACCOUNT_CREDENTIALS' in st.secrets:
            # Use credentials from secrets
            credentials_dict = st.secrets['SERVICE_ACCOUNT_CREDENTIALS']
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict, scopes=SCOPES
            )
        else:
            # Fall back to file-based authentication
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                st.error(f"❌ Service account key file '{SERVICE_ACCOUNT_FILE}' not found!")
                st.info("Please create a Google Cloud service account and download the JSON key file.")
                return None
            
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
        
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
        return None

def save_to_google_sheets(data_dict):
    """Save data to Google Sheets"""
    client = get_google_sheets_client()
    if not client:
        return False
    
    try:
        # Open the spreadsheet
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        # Try to get the worksheet, create if it doesn't exist
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
            # Add headers
            headers = list(data_dict.keys())
            worksheet.append_row(headers)
        
        # Prepare data row
        data_row = list(data_dict.values())
        
        # Append the new row
        worksheet.append_row(data_row)
        
        return True
    except Exception as e:
        st.error(f"❌ Error saving to Google Sheets: {str(e)}")
        return False

def get_all_data_from_sheets():
    """Retrieve all data from Google Sheets"""
    client = get_google_sheets_client()
    if not client:
        return None
    
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        # Get all values
        all_values = worksheet.get_all_values()
        
        if len(all_values) <= 1:  # Only headers or empty
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(all_values[1:], columns=all_values[0])
        return df
    except Exception as e:
        st.error(f"❌ Error reading from Google Sheets: {str(e)}")
        return None

st.title("EduRepublic Staff Biodata Collection")

# Check if Google Sheets is properly configured
if not os.path.exists(SERVICE_ACCOUNT_FILE) and 'SERVICE_ACCOUNT_CREDENTIALS' not in st.secrets:
    st.warning("⚠️ Google Sheets not configured")
    st.info("""
    To use Google Sheets integration:
    1. Create a Google Cloud project
    2. Enable Google Sheets API
    3. Create a service account
    4. For deployment: Add SERVICE_ACCOUNT_CREDENTIALS and SPREADSHEET_ID to Streamlit secrets
    5. For local development: Download the JSON key file as 'service_account_key.json'
    6. Share your Google Sheet with the service account email
    """)

# --- Biodata Form ---
with st.form("biodata_form"):
    st.subheader("Enter Staff Information")

    full_name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    address = st.text_area("Home Address")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    department = st.text_input("Department / Role")
    date_joined = st.date_input("Date Joined")

    st.markdown("---")
    st.subheader("Emergency Contact Details")

    emergency_name = st.text_input("Emergency Contact Name")
    emergency_phone = st.text_input("Emergency Contact Phone")
    emergency_relation = st.text_input("Relationship to Staff")

    submitted = st.form_submit_button("Submit Biodata")

# --- On Form Submission ---
if submitted:
    # Prepare data dictionary
    data_dict = {
        "Full Name": full_name,
        "Phone Number": phone,
        "Email": email,
        "Address": address,
        "Date of Birth": str(dob),
        "Gender": gender,
        "Department/Role": department,
        "Date Joined": str(date_joined),
        "Emergency Contact Name": emergency_name,
        "Emergency Contact Phone": emergency_phone,
        "Emergency Relationship": emergency_relation,
        "Submission Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to Google Sheets
    if save_to_google_sheets(data_dict):
        st.success("✅ Biodata saved successfully to Google Sheets!")
    else:
        st.error("❌ Failed to save biodata. Please check your Google Sheets configuration.")

# --- Display Data ---
st.markdown("## 📄 Submitted Biodata")
df = get_all_data_from_sheets()

if df is not None and not df.empty:
    st.dataframe(df)
    
    # Download button for backup
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV (Backup)", csv, "staff_biodata_backup.csv", "text/csv")
else:
    st.info("No data available or Google Sheets not configured.")
