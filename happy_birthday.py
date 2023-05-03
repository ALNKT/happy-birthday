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
        return self.service.events().list(calendarId=self.calendar_id).execute()


def search_people_who_have_birthday_today(birthdays):
    today_month_day = str(datetime.today().date())[5:]
    peoples_who_have_birthday_today = {i_people: i_date for i_people, i_date in birthdays.items()
                                       if i_date[5:] == today_month_day}
    return peoples_who_have_birthday_today


def calculate_age_of_peoples(peoples):
    today_year = datetime.today().year
    age_of_peoples = {i_people: today_year - datetime.strptime(i_date, '%Y-%m-%d').year for i_people, i_date in
                      peoples.items()}
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


def congratulation_peoples_who_have_birthday_today(peoples):
    celebration_word = 'празднует' if len(peoples) <= 1 else 'празднуют'
    congratulation_phrase = f'Сегодня {celebration_word} свой день рождения '

    for i_people, i_date in peoples.items():
        i_date = determine_the_end_of_the_age(i_date)
        congratulation_phrase += f'{i_people}, {i_date}! '

    congratulation_phrase += f'{settings.my_name}, не забудьте поздравить!'
    return congratulation_phrase


def nearest_peoples_who_have_birthday(peoples):
    today = datetime.today().month
    nearest_birthdays = {i_people: i_date for i_people, i_date in peoples.items()
                         if datetime.strptime(i_date, '%Y-%m-%d').month >= today}
    sorted_nearest_birthdays = dict(sorted(nearest_birthdays.items(), key=lambda item: item[1][5:], reverse=True))
    nearest_birthday_of_people = sorted_nearest_birthdays.popitem()
    nearest_birthday_of_people = {nearest_birthday_of_people[0]: nearest_birthday_of_people[1]}
    return nearest_birthday_of_people


def convert_date_to_readable_form(date_of_birth: str):
    months = {
        '1': 'января',
        '2': 'февраля',
        '3': 'марта',
        '4': 'апреля',
        '5': 'мая',
        '6': 'июня',
        '7': 'июля',
        '8': 'августа',
        '9': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря'}
    date_of_birth = date_of_birth.replace('0', '').split('-')
    month = months.get(date_of_birth[0])
    date_of_birth = f'{date_of_birth[1]} {month}'
    return date_of_birth


def congratulation_peoples_who_nearest_birthday(nearest_birthday_of_people):
    age_of_people_who_nearest_birthday = calculate_age_of_peoples(nearest_birthday_of_people)
    people, age = age_of_people_who_nearest_birthday.popitem()
    age = determine_the_end_of_the_age(age)
    date_of_birthday = nearest_birthday_of_people.popitem()[1][5:]
    date_of_birthday = convert_date_to_readable_form(date_of_birthday)

    congratulation_phrase = f'Сегодня ваши друзья ничего не празднуют! ' \
                            f'Ближайший день рождения будет праздновать {people}! ' \
                            f'{date_of_birthday} исполнится {age}! Не забудьте поздравить!'
    return congratulation_phrase


def birthdays_of_all_people_from_calendar(calendar):
    events = calendar.get_events()
    return {event.get('summary'): event.get('start').get('date') for event in events.get('items')}


def congratulation_phrase_with_data(birthdays):
    peoples_who_today_birthday = search_people_who_have_birthday_today(birthdays)

    if peoples_who_today_birthday:
        age_of_peoples_who_today_birthday = calculate_age_of_peoples(peoples_who_today_birthday)
        return congratulation_peoples_who_have_birthday_today(age_of_peoples_who_today_birthday)

    nearest_birthday = nearest_peoples_who_have_birthday(birthdays)
    return congratulation_peoples_who_nearest_birthday(nearest_birthday)


def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    text = congratulation_phrase_with_data(birthdays_of_all_peoples)

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'end_session': 'true'
        },
    }


google_calendar = GoogleCalendar()

birthdays_of_all_peoples = birthdays_of_all_people_from_calendar(google_calendar)
