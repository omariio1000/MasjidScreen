"""
Created on Thu Feb 6 23:16 2025

@author: Omar Nassar
"""

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def create_email_template(name, date, code):
    name = ' '.join([part.capitalize() for part in name.split()])
    """Create an email body with a dynamic name, date, and code."""

    email_body = f"Assalamu Alaikum {name},\n\nCongratulations on winning trivia on {date}!\nHere is your amazon gift card code: {code}.\n\nJazakum Allahu Khairan,\nICCH Trivia Team\n\nThis is an automated email, please don't reply."
    return email_body

def authenticate_gmail():
    """Authenticate using OAuth 2.0 and return a Gmail API service instance."""

    # If modifying the scope, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    # The token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('../resources/token.json'):
        creds = Credentials.from_authorized_user_file('../resources/token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None  # Force re-authentication
        
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('../resources/email_credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the new credentials
        with open('../resources/token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

def hide_email(email):
    # Split the email at the '@' symbol
    local, domain = email.split('@', 1)
    
    # Mask everything after the first three characters of the local part
    masked_local = local[:3] + '*' * (len(local) - 3)
    
    # Return the masked email with the domain intact
    return masked_local + '@' + domain

def send_email(name, receiving_address, code, date):
    """Send an email using the Gmail API."""
    name = ' '.join([part.capitalize() for part in name.split()])
    try:
        # Create the email message
        message = MIMEMultipart()
        message['to'] = receiving_address
        message['subject'] = "Congratulations on Winning ICCH Trivia!"
        msg = MIMEText(create_email_template(name, date, code))
        message.attach(msg)
        
        # Encode the email message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email using the Gmail API
        message = authenticate_gmail().users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f"Message sent to {name} ({hide_email(receiving_address)}) with Message ID: {message['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

def test_email(name, receiving_address):
    """Send a test email using the Gmail API."""

    try:
        # Create the email message
        message = MIMEMultipart()
        message['to'] = receiving_address
        message['subject'] = "Test Email"
        msg = MIMEText(f"Test Email sent on {datetime.now().strftime("%B %d, %Y at %H:%M:%S")}")
        message.attach(msg)
        
        # Encode the email message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email using the Gmail API
        message = authenticate_gmail().users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f"Message sent to {name}")
        return True
    except Exception as error:
        print(f"An error occurred: {error}")
        return False

def main():
    """Test send email"""

    if test_email("Omar Nassar", "omariio1000@gmail.com"):
        print("Account verified and test email sent.")

if __name__ == '__main__':
    main()
