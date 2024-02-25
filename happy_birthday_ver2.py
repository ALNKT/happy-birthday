import json
import os
from datetime import datetime
from dotenv import load_dotenv
from google.auth._service_account_info import from_dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
import settings


load_dotenv()


class CustomCredential(service_account.Credentials):

    @staticmethod
    def from_filename(filename, require=None, use_rsa_signer=True):
        data = json.loads(filename)
        return data, from_dict(data, require=require, use_rsa_signer=use_rsa_signer)

    @classmethod
    def from_service_account_file(cls, filename, **kwargs):
        info, signer = cls.from_filename(
            filename, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)


class GoogleCalendar:
    SCOPES = settings.SCOPES
    private_key = os.getenv('private_key')
    calendar_id = os.getenv('calendar_id')

    def __init__(self):
        credentials = CustomCredential.from_service_account_file(filename=self.private_key, scopes=self.SCOPES)
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self):
        calendar_list_entry = {
            'id': self.calendar_id
        }
        return self.service.calendarList().insert(body=calendar_list_entry).execute()

    def get_events(self):
        events = self.service.events().list(calendarId=self.calendar_id).execute()
        events_fmt = {event.get('summary'): datetime.strptime(event.get('start').get('date'), '%Y-%m-%d')
                      for event in events.get('items')}
        return events_fmt


class Event:
    def __init__(self, people, birthday, age=None):
        self.__people = people
        self.__birthday = birthday
        self.__age = age

    def get_people(self):
        return self.__people

    def get_date_of_birthday(self):
        return self.__birthday

    def get_date_of_birthday_fmt(self):
        date_of_birthday = datetime.strftime(self.get_date_of_birthday(), '%d-%m').split('-')
        months = {
            '01': 'января',
            '02': 'февраля',
            '03': 'марта',
            '04': 'апреля',
            '05': 'мая',
            '06': 'июня',
            '07': 'июля',
            '08': 'августа',
            '09': 'сентября',
            '10': 'октября',
            '11': 'ноября',
            '12': 'декабря'}
        month = months.get(date_of_birthday[1])
        date_of_birthday = f'{date_of_birthday[0]} {month}'
        if date_of_birthday[0] == '0':
            date_of_birthday = date_of_birthday.replace('0', '')
        return date_of_birthday

    def get_month_and_day_of_birthday(self):
        return datetime.strftime(self.__birthday, '%m-%d')

    def get_age(self):
        return self.__age

    def check_event_today(self):
        today_month_and_day = str(datetime.today().date())[5:]
        if today_month_and_day == self.__birthday.strftime('%m-%d'):
            return True
        return False

    def calculate_age(self):
        age = datetime.today().year - self.__birthday.year
        if 10 <= age <= 20 or str(age % 10) in '056789':
            age = str(age) + ' лет'
        elif age % 10 == 1:
            age = str(age) + ' год'
        elif str(age % 10) in '234':
            age = str(age) + ' года'
        self.__age = age


def search_nearest_event(events):
    today = datetime.today()
    future_events = [event for event in events if event.get_date_of_birthday().month >= today.month]

    for index, event in enumerate(future_events):
        date_of_event = event.get_date_of_birthday()
        if date_of_event.month == today.month:
            if date_of_event.day < today.day:
                future_events.pop(index)

    future_events = list(sorted(future_events, key=lambda x: (x.get_date_of_birthday().month,
                                                              x.get_date_of_birthday().day)))
    nearest_birthday = future_events[0].get_month_and_day_of_birthday()
    events = [event for event in events if event.get_month_and_day_of_birthday() == nearest_birthday]
    return events


def get_all_events_from_calendar(calendar):
    events_from_calendar = calendar.get_events()
    events = [Event(people=people, birthday=birthday) for people, birthday in events_from_calendar.items()]
    return events


def generate_congratulation(events):
    events_today = [event for event in events if event.check_event_today()]
    if events_today:
        phrase = 'Сегодня свой день рождения {word} '.format(
            word='празднует' if len(events_today) == 1 else 'празднуют')
        for event in events_today:
            event.calculate_age()
            phrase += f'{event.get_people()}, {event.get_age()}! '
        phrase += f'{settings.my_name}, не забудьте поздравить!'
        return phrase

    nearest_events = search_nearest_event(events)
    date_of_birthday = nearest_events[0].get_date_of_birthday_fmt()
    phrase = ('Сегодня ваши друзья ничего не празднуют! Ближайший день рождения: {date_of_birthday}, {word} праздновать: '.
              format(date_of_birthday=date_of_birthday, word='будет' if len(nearest_events) == 1 else 'будут'))
    for event in nearest_events:
        event.calculate_age()
        phrase += '{people} - исполнится {age}! '.format(people=event.get_people(), age=event.get_age())
    phrase += f'{settings.my_name}, не забудьте поздравить!'
    print(phrase)
    return phrase


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    text = generate_congratulation(all_events_from_calendar)

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'true'
        },
    }


google_calendar = GoogleCalendar()

all_events_from_calendar = get_all_events_from_calendar(google_calendar)

generate_congratulation(all_events_from_calendar)
