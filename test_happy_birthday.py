import unittest

import settings
from happy_birthday import search_people_who_have_birthday_today, calculate_age_of_peoples, \
    determine_the_end_of_the_age, output_peoples_who_have_birthday_today
from freezegun import freeze_time


class TestHappyBirthday(unittest.TestCase):

    def setUp(self):
        self.today_month_day = '12-01'
        self.today_year = '2023'
        self.birthdays = {'Иван Иванов': '1990-12-01', 'Петр Петров': '1988-05-03', 'Федор Федоров': '1993-03-09'}
        self.birthdays_today = {'Иван Иванов': '1990-12-01', 'Петр Петров': '1988-12-01'}
        self.my_name = settings.my_name

    def test_search_people_who_have_birthday_today(self):

        with freeze_time(self.today_month_day):
            people_who_have_birthday_today = search_people_who_have_birthday_today(self.birthdays)
            self.assertEqual({'Иван Иванов': '1990-12-01'}, people_who_have_birthday_today)

    def test_calculate_age_of_peoples(self):
        with freeze_time(self.today_year):
            age_of_peoples = calculate_age_of_peoples(self.birthdays_today)
            self.assertEqual({'Иван Иванов': 33, 'Петр Петров': 35}, age_of_peoples)

    def test_determine_the_end_of_the_age(self):
        ages = ['21 год', '22 года', '25 лет']
        for i_age in ages:
            with self.subTest(i_age):
                age = determine_the_end_of_the_age(int(i_age[:2]))
                self.assertEqual(age, i_age)

    def test_output_peoples_who_have_birthday_today(self):
        congratulation_phrase_1 = f'Сегодня празднует свой день рождения Иван Иванов - 33 года! {self.my_name}, ' \
                                  f'не забудьте поздравить!'
        congratulation_phrase_2 = f'Сегодня празднуют свой день рождения Иван Иванов - 33 года! Петр Петров - 35 лет! ' \
                                  f'{self.my_name}, не забудьте поздравить!'
        peoples_hwo_have_today_birthday = {'Иван Иванов': 33, 'Петр Петров': 35}
        output_phrase_1 = output_peoples_who_have_birthday_today({'Иван Иванов': 33})
        self.assertEqual(output_phrase_1, congratulation_phrase_1)

        output_phrase_2 = output_peoples_who_have_birthday_today(peoples_hwo_have_today_birthday)
        self.assertEqual(output_phrase_2, congratulation_phrase_2)


if __name__ == '__main__':
    unittest.main()
