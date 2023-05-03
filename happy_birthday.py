import os
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import settings


load_dotenv()


class GoogleCalendar:

    SCOPES = settings.SCOPES
    private_key = os.getenv('private_key')
    calendar_id = os.getenv('calendar_id')

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(filename=self.private_key, scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self):
        calendar_list_entry = {
            'id': self.calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def get_events(self):

        return self.service.events().list(calendarId=self.calendar_id).execute()


def search_people_who_have_birthday_today(birthdays):
    today_month_day = str(datetime.today().date())[5:]
    peoples_who_have_birthday_today = {i_people: i_date for i_people, i_date in birthdays.items()
                                       if i_date[5:] == today_month_day}
    return peoples_who_have_birthday_today


def calculate_age_of_peoples(peoples):
    today_year = datetime.today().year
    age_of_peoples = {i_people: today_year - datetime.strptime(i_date, '%Y-%m-%d').year for i_people, i_date in peoples.items()}
    return age_of_peoples


def determine_the_end_of_the_age(age):
    while age >= 365:
        age = age // 365
    if 10 <= age <= 20 or str(age % 10) in '056789':
        age = str(age) + ' лет'
    elif age % 10 == 1:
        age = str(age) + ' год'
    elif str(age % 10) in '234':
        age = str(age) + ' года'
    return age


def output_peoples_who_have_birthday_today(peoples):
    celebration_word = 'празднует' if len(peoples) <= 1 else 'празднуют'
    congratulation_phrase = f'Сегодня {celebration_word} свой день рождения '

    for i_people, i_date in peoples.items():
        i_date = determine_the_end_of_the_age(i_date)
        congratulation_phrase += f'{i_people} - {i_date}! '

    congratulation_phrase += f'{settings.my_name}, не забудьте поздравить!'
    return congratulation_phrase


if __name__ == '__main__':

    calendar = GoogleCalendar()

    events = calendar.get_events()
    birthdays_of_all_peoples = {event.get('summary'): event.get('start').get('date') for event in events.get('items')}

    peoples_who_today_birthday = search_people_who_have_birthday_today(birthdays_of_all_peoples)

    age_of_peoples_who_today_birthday = calculate_age_of_peoples(peoples_who_today_birthday)

    print(output_peoples_who_have_birthday_today(age_of_peoples_who_today_birthday))
