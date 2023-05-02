import os
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from settings import SCOPES


load_dotenv()


class GoogleCalendar:

    SCOPES = SCOPES
    private_key = os.getenv('private_key')

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename=self.private_key, scopes=self.SCOPES)
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


def search_people_who_have_birthday_today(birthdays):
    today_month_day = str(datetime.today().date())[5:]
    peoples_who_have_birthday_today = {i_people: i_date for i_people, i_date in birthdays.items()
                                       if i_date[5:] == today_month_day}
    return peoples_who_have_birthday_today


def calculate_age_of_peoples(peoples):
    pass


obj = GoogleCalendar()
events = obj.get_events()

birthdays_of_all_peoples = {event.get('summary'): event.get('start').get('date') for event in events.get('items')}

peoples_who_today_birthday = search_people_who_have_birthday_today(birthdays_of_all_peoples)
