# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

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
        entry = models.Course(name="Test", courseId=2, inactivity=False, deadline=True, hours_before=86400)
        entry2 = models.Course(name="Test", courseId=2, inactivity=False, deadline=False, hours_before=86400)
        entry3 = models.Course(name="Test", courseId=2, inactivity=True, deadline=True, hours_before=86400)
        entry4 = models.Course(name="Test", courseId=2, inactivity=True, deadline=False, hours_before=86400)

        entry.save()
        self.assertEqual(len(main_scheduler.jobs), 2)
        entry.save()
        self.assertEqual(len(main_scheduler.jobs), 2)
        entry.delete()
        self.assertEqual(len(main_scheduler.jobs), 0)
        entry2.save()
        self.assertEqual(len(main_scheduler.jobs), 0)
        entry2.delete()
        entry3.save()
        self.assertEqual(len(main_scheduler.jobs), 3)
        entry3.delete()
        entry4.save()
        self.assertEqual(len(main_scheduler.jobs), 1)
