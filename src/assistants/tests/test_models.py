# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
import datetime
from django.test import TestCase

from assistants import models
from scheduler.main_scheduler import main_scheduler


class NewActivityNotificationTest(TestCase):
    def test_build_new_activity_notification(self):
        # Test if the notification is build correctly.
        message = models.build_new_activity_notification('test_course', 'test_activity', 'test_type')
        self.assertEqual(
            'For the course test_course the test_type test_activity is added.', message)


class CourseSaveTest(TestCase):
    def test_save_and_delete(self):
        entry = models.Course(name="Test", courseId=2, inactivity=False, deadline=True, hours_before=86400,
                              version_time=datetime.datetime(2020, 1, 28))
        entry2 = models.Course(name="Test", courseId=2, inactivity=False, deadline=False, hours_before=86400,
                               version_time=datetime.datetime(2020, 1, 28))
        entry3 = models.Course(name="Test", courseId=2, inactivity=True, deadline=True, hours_before=86400,
                               version_time=datetime.datetime(2020, 1, 28))
        entry4 = models.Course(name="Test", courseId=2, inactivity=True, deadline=False, hours_before=86400,
                               version_time=datetime.datetime(2020, 1, 28))

        entry.save()
        self.assertEqual(self.count_entries(self), 2)
        entry.save()
        self.assertEqual(self.count_entries(self), 2)
        entry.delete()
        self.assertEqual(self.count_entries(self), 0)
        entry2.save()
        self.assertEqual(self.count_entries(self), 0)
        entry2.delete()
        entry3.save()
        self.assertEqual(self.count_entries(self), 3)
        entry3.delete()
        entry4.save()
        self.assertEqual(self.count_entries(self), 1)

    @staticmethod
    def count_entries(self):
        # Counts all entries except error ahndling: this is added when running the program
        count = 0
        for job in main_scheduler.jobs:
            if not (job == "error handling"):
                count += 1

        return count
