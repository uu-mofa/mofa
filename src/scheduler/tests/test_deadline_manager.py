# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
from unittest.mock import patch

from django.test import TestCase
import scheduler.deadline_manager as deadline_manager
from . import test_data


class DeadlineManagerTest(TestCase):

    @patch('assistants.moodle.get_assignments', return_value=test_data.test_get_assignments_data)
    def test_get_assignments(self, a):
        json_result = deadline_manager.get_assignments(2)

        self.assertEqual(json_result, test_data.test_get_assignments_check)

    @patch('assistants.moodle.get_assignments', return_value=test_data.test_get_assignments_data)
    def test_get_deadlines_between(self, a):
        json_result = deadline_manager.get_assignments(2)

        passed_deadlines = deadline_manager.get_deadlines_between(json_result, 1573776059, 1573776061)
        test_dict = {6: ('Learning basic loops', 1573776060), 9: ('Learning booleans', 1573776060)}
        self.assertEqual(passed_deadlines, test_dict)

        empty_deadlines = deadline_manager.get_deadlines_between(json_result, 0, 1)
        self.assertEqual(empty_deadlines, {})

    @patch('assistants.moodle.get_assignment_status', return_value=test_data.test_assignment_completion_check)
    def test_check_assignment_completion(self, a):
        self.assertEqual(deadline_manager.check_assignment_completion(4, 6, 2), True)
        self.assertEqual(deadline_manager.check_assignment_completion(4, 9, 2), False)

    @patch('assistants.moodle.get_enrolled_users', return_value=test_data.test_get_enrolled_users)
    def test_get_users(self, a):
        self.assertEqual(deadline_manager.get_users(2), ['4'])

    @patch('time.time')
    def test_convert_time(self, a):
        a.return_value = 5000
        due_time1 = deadline_manager.convert_time(5060)
        a.return_value = 6000
        due_time2 = deadline_manager.convert_time(10000)
        self.assertEqual(due_time1, (0, 1))
        self.assertEqual(due_time2, (1, 6))

    def test_prep_late_warning(self):
        message = deadline_manager.prep_late_warning('test_assignment')
        self.assertEqual(message, 'The deadline for test_assignment has passed.')

    def test_prep_early_warning(self):
        message = deadline_manager.prep_early_warning(1, 30, "test_assignment")
        self.assertEqual(message, 'The deadline for test_assignment is in 1 hours and 30 minutes.')

    @patch('assistants.moodle.send_bulk_different_messages')
    @patch('time.time', return_value=0)
    def test_send_warnings(self, a, b):
        deadline_manager.send_warnings([(2, "test message"), (3, "testing message")])
        b.assert_called_with([(2, 'test message'), (3, 'testing message')])

    @patch('assistants.moodle.get_enrolled_users', return_value=test_data.test_get_enrolled_users)
    @patch('assistants.moodle.get_assignment_status', return_value=test_data.test_assignment_completion_check)
    @patch('assistants.moodle.get_assignments', return_value=test_data.test_get_assignments_data)
    @patch('scheduler.deadline_manager.send_warnings')
    @patch('time.time', return_value=1573777061)
    def test_notify_about_passed_deadlines(self, a, b, c, d, e):
        deadline_manager.notify_about_passed_deadlines(2)

        b.assert_called_with([('4', 'The deadline for Learning booleans has passed.')])
        b.assert_called_once()

    @patch('assistants.moodle.get_enrolled_users', return_value=test_data.test_get_enrolled_users)
    @patch('assistants.moodle.get_assignment_status', return_value=test_data.test_assignment_completion_check)
    @patch('assistants.moodle.get_assignments', return_value=test_data.test_get_assignments_data)
    @patch('scheduler.deadline_manager.send_warnings')
    @patch('time.time', return_value=1573775000)
    def test_notify_about_upcoming_deadlines(self, a, b, c, d, e):
        deadline_manager.notify_about_upcoming_deadlines(86400, 2)

        b.assert_called_with([('4', 'The deadline for Learning booleans is in 0 hours and 17 minutes.')])
        b.assert_called_once()
