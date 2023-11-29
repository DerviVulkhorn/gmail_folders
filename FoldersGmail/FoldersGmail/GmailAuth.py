import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from main_page.models import Users



SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_auth():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "FoldersGmail/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_users():
    profile = gmail_auth().users().getProfile(userId='me').execute()
    email = profile['emailAddress']
    try:
        existing_record = Users.objects.get(login=email)
        print(f"Пользователь {existing_record} найден")
        return existing_record
    except:
        save_usr = Users.objects.create(login=f'{email}')
        print(f"Пользователь {save_usr} добавлен")
        return save_usr