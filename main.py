import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


load_dotenv()


class GoogleCalendar:

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    FILE_PATH = os.getenv('FILE_PATH')

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename=self.FILE_PATH, scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendarId):
        calendar_list_entry = {
            'id': calendarId
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def get_events(self):
        calendarId = os.getenv('calendar_id')
        return self.service.events().list(calendarId=calendarId).execute()


obj = GoogleCalendar()
