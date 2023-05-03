import unittest

import settings
from happy_birthday import search_people_who_have_birthday_today, calculate_age_of_peoples, \
    determine_the_end_of_the_age, congratulation_peoples_who_have_birthday_today, nearest_peoples_who_have_birthday, \
    convert_date_to_readable_form, congratulation_peoples_who_nearest_birthday
from freezegun import freeze_time


class TestHappyBirthday(unittest.TestCase):

    def setUp(self):
        self.today = '2023-05-03'
        self.birthdays = {'Иван Иванов': '1990-12-01', 'Петр Петров': '1988-05-03', 'Федор Федоров': '1993-03-09'}
        self.birthdays_today = {'Иван Иванов': '1990-05-03', 'Петр Петров': '1988-05-03'}
        self.nearest_birthday = {'Иван Иванов': '1990-05-09'}
        self.my_name = settings.my_name

    def test_search_people_who_have_birthday_today(self):

        with freeze_time(self.today):
            people_who_have_birthday_today = search_people_who_have_birthday_today(self.birthdays)
            self.assertEqual({'Петр Петров': '1988-05-03'}, people_who_have_birthday_today)

    def test_calculate_age_of_peoples(self):
        with freeze_time(self.today):
            age_of_peoples = calculate_age_of_peoples(self.birthdays_today)
            self.assertEqual({'Иван Иванов': 33, 'Петр Петров': 35}, age_of_peoples)

    def test_determine_the_end_of_the_age(self):
        ages = ['21 год', '22 года', '25 лет']
        for i_age in ages:
            with self.subTest(i_age):
                age = determine_the_end_of_the_age(int(i_age[:2]))
                self.assertEqual(age, i_age)

    def test_congratulation_peoples_who_have_birthday_today(self):
        people_1 = 'Иван Иванов, 33 года'
        people_2 = 'Иван Иванов, 33 года! Петр Петров, 35 лет'
        peoples_hwo_have_today_birthday = {'Иван Иванов': 33, 'Петр Петров': 35}
        output_phrase_1 = congratulation_peoples_who_have_birthday_today({'Иван Иванов': 33})
        self.assertTrue(people_1 in output_phrase_1)

        output_phrase_2 = congratulation_peoples_who_have_birthday_today(peoples_hwo_have_today_birthday)
        self.assertTrue(people_2 in output_phrase_2)

    def test_nearest_peoples_who_have_birthday(self):
        with freeze_time(self.today):
            nearest_birthday = nearest_peoples_who_have_birthday(self.birthdays)
            self.assertEqual({'Петр Петров': '1988-05-03'}, nearest_birthday)

    def test_convert_date_to_readable_form(self):
        date_of_birth = convert_date_to_readable_form('05-02')
        self.assertEqual(date_of_birth, '2 мая')

    def test_congratulation_peoples_who_nearest_birthday(self):
        people = 'Иван Иванов! 9 мая исполнится 33 года'
        with freeze_time(self.today):
            congratulation_phrase = congratulation_peoples_who_nearest_birthday(self.nearest_birthday)
            self.assertTrue(people in congratulation_phrase)


if __name__ == '__main__':
    unittest.main()
