# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Test the methods of the inactivity_courses.py file."""
import datetime as dt
import unittest
from unittest.mock import patch

from scheduler import inactivity_courses as ic
from . import test_data


class TestCalculateDate(unittest.TestCase):
    def test_calculate_date(self):
        self.assertEqual(ic.calculate_date(dt.date(2019, 11, 4), 7), dt.date(2019, 10, 28))

    def test_students_not_viewed(self):
        self.assertEqual(set(ic.students_not_viewed(['2', '3', '4', '5'], ['2', '3'])), {'4', '5'})

    def test_get_message(self):
        self.assertEqual(ic.get_message("BeginningCourse", 7),
                         "You have not viewed the course BeginningCourse in 7 day(s). We advise you to check it.")

    def test_send_message(self):
        with patch('assistants.moodle.send_bulk_messages') as m:
            ic.send_message(['3', '2'], "test")
            self.assertEqual(m.call_count, 1)
        m.assert_called_with({'3', '2'}, 'test')

    def test_create_job(self):
        with patch('assistants.moodle.get_enrolled_users') as moodle_api1:
            with patch('assistants.moodle.get_course_by_id_field') as moodle_api2:
                with patch('assistants.moodle.send_bulk_messages') as moodle_api3:
                    with patch('assistants.learning_locker.get_viewed_courses') as ll_api:
                        jsn = test_data.test_learning_locker_viewed_course
                        json_enrolled = test_data.test_inactivity_get_enrolled_users
                        json_course = test_data.test_get_courses_by_id
                        ll_api.return_value = jsn
                        moodle_api1.return_value = json_enrolled
                        moodle_api2.return_value = json_course
                        message = "You have not viewed the course BeginningCourse in 7 day(s). " \
                                  "We advise you to check it."
                        ic.create_job(1, 7)
                        self.assertEqual(moodle_api3.call_count, 1)
                        moodle_api3.assert_called_with({'5', '3', '4'}, message)
