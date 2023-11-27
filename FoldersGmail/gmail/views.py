import os.path

from google.auth.transport.requests import Request
from django.shortcuts import render
from google.oauth2 import service_account
from google.auth import jwt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
def get_emails(request):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "FoldersGmail/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get("messages", [])
        users = service.users().getProfile
        content_list = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'],format='full').execute()
            content_list.append(msg)

        return render(request, 'email_list.html', {'emails': content_list})

    except HttpError as error:
        print(f"An error occurred: {error}")
