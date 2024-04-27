import pandas as pd
from dotenv import load_dotenv
import os.path
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

def credentials_wrapper(SCOPES):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.\
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', 
                SCOPES
                )
            creds = flow.run_local_server(port=0)        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    
    return creds


def pull_sheet_data():
    # grab credentials
    creds = credentials_wrapper(['https://www.googleapis.com/auth/spreadsheets.readonly'])
    try:
        service = build('sheets', 'v4', credentials=creds)
        # call the google sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=os.getenv('SHEET_ID'),
            range=os.getenv('SHEET_RANGE')
            ).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return

        # pull the data
        rows = sheet.values().get(
            spreadsheetId=os.getenv('SHEET_ID'),
            range=os.getenv('SHEET_RANGE')
            ).execute()
        data = rows.get('values')

        # turn that into a pandas dataframe
        df = pd.DataFrame(data[1:], columns=data[0])

        print("COMPLETE: Data copied")
        return df
    
    # error handle with what the api returns
    except HttpError as err:
        print(err)