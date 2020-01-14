# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

from django.test import TestCase
from unittest.mock import patch
from django.core.exceptions import ObjectDoesNotExist

import assistants.sync_agent as db_update
import assistants.tests.test_data as test_data
from courses.models import Course, Resource, Quiz, Assignment, Choice


class TestDatabaseUpdate(TestCase):

    def setUp(self) -> None:
        """Set up of test."""
        Course.objects.create(name='test-course', courseId=2)

    def test_create_update_delete_content(self):
        with patch('assistants.moodle.send_bulk_messages'):
            db_update.module_update_or_create(test_data.test_database_create_resource)
            self.assertEqual(1, Resource.objects.count())
            db_update.module_update_or_create(test_data.test_database_update_resource)
            self.assertEqual(1, Resource.objects.count())
            self.assertEqual('Advanced', Resource.objects.first().name)
            db_update.module_delete(test_data.test_database_update_resource)
            self.assertEqual(0, Resource.objects.count())

    def test_create_update_delete_assignment(self):
        with patch('assistants.moodle.send_bulk_messages'):
            db_update.module_update_or_create(test_data.test_database_create_assign)
            self.assertEqual(1, Assignment.objects.count())
            db_update.module_update_or_create(test_data.test_database_update_assign)
            self.assertEqual(1, Assignment.objects.count())
            self.assertEqual('For Loops', Assignment.objects.first().name)
            db_update.module_delete(test_data.test_database_update_assign)
            self.assertEqual(0, Assignment.objects.count())

    def test_create_update_delete_quiz(self):
        with patch('assistants.moodle.send_bulk_messages'):
            db_update.module_update_or_create(test_data.test_database_create_quiz)
            self.assertEqual(1, Quiz.objects.count())
            db_update.module_update_or_create(test_data.test_database_update_quiz)
            self.assertEqual(1, Quiz.objects.count())
            self.assertEqual('For', Quiz.objects.first().name)
            db_update.module_delete(test_data.test_database_update_quiz)
            self.assertEqual(0, Quiz.objects.count())

    def test_create_update_delete_choice(self):
        with patch('assistants.moodle.send_bulk_messages'):
            db_update.module_update_or_create(test_data.test_database_create_choice)
            self.assertEqual(1, Choice.objects.count())
            db_update.module_update_or_create(test_data.test_database_update_choice)
            self.assertEqual(1, Choice.objects.count())
            self.assertEqual('F', Choice.objects.first().name)
            db_update.module_delete(test_data.test_database_update_choice)
            self.assertEqual(0, Choice.objects.count())

    def test_create_update_delete_course(self):
        with patch('assistants.moodle.send_bulk_messages'):
            db_update.course_update_or_create(test_data.test_database_create_course)
            self.assertEqual(2, Course.objects.count())
            db_update.course_update_or_create(test_data.test_database_update_course)
            self.assertEqual(2, Course.objects.count())
            self.assertEqual('Python', Course.objects.last().name)
            db_update.course_delete(test_data.test_database_update_course)
            self.assertEqual(1, Course.objects.count())

    def test_create_sync_agent(self):
        with patch('assistants.learning_locker.create_statement_forwarder') as m:
            m.return_value = {'_id': 1}
            db_update.create_sync_agent()
        m.assert_called_with('sync_agent',
                             query='{\n  "$and": [\n    {\n      "$comment": "{\\"criterionLabel\\":\\"A\\",\\"crit'
                                   'eriaPath\\":[\\"statement\\",\\"verb\\"]}",\n      "statement.verb.id": {\n    '
                                   '    "$in": [\n          "http://activitystrea.ms/schema/1.0/create",\n         '
                                   ' "http://activitystrea.ms/schema/1.0/update",\n          "http://activitystrea.'
                                   'ms/schema/1.0/delete"\n        ]\n      },\n      "$comment": "{\\"criterionLabel'
                                   '\\":\\"B\\",\\"criteriaPath\\":[\\"statement\\",\\"object\\",\\"definition\\",\\'
                                   '"type\\"]}",\n      "statement.object.definition.type": {\n        "$in": [\n    '
                                   '      "http://id.tincanapi.com/activitytype/lms/course",\n          "http://id.tin'
                                   'canapi.com/activitytype/lms/module",\n          "http://id.tincanapi.com/activity'
                                   'type/chapter",\n          "http://id.tincanapi.com/activitytype/assign",\n       '
                                   '   "http://id.tincanapi.com/activitytype/quiz",\n          "http://id.tincanapi.'
                                   'com/activitytype/choice",\n          "http://id.tincanapi.com/activitytype/book"'
                                   '\n        ]\n      }\n    }\n  ]\n}')

    def test_build_sync_agent(self):
        with patch('assistants.learning_locker.create_statement_forwarder') as m:
            with patch('assistants.learning_locker.get_sync_agent_forwarder') as m2:
                m.return_value = {'_id': 1}
                m2.return_value = test_data.test_build_sync_agent_get_data_empty
                db_update.build_sync_agent()

        m.assert_called_with('sync_agent',
                             query='{\n  "$and": [\n    {\n      "$comment": "{\\"criterionLabel\\":\\"A\\",\\'
                                   '"criteriaPath\\":[\\"statement\\",\\"verb\\"]}",\n      "statement.verb.id": '
                                   '{\n        "$in": [\n          "http://activitystrea.ms/schema/1.0/create",\n '
                                   '         "http://activitystrea.ms/schema/1.0/update",\n          "http://activity'
                                   'strea.ms/schema/1.0/delete"\n        ]\n      },\n      "$comment": "{\\"criterion'
                                   'Label\\":\\"B\\",\\"criteriaPath\\":[\\"statement\\",\\"object\\",\\"definition'
                                   '\\",\\"type\\"]}",\n      "statement.object.definition.type": {\n        "$in": '
                                   '[\n          "http://id.tincanapi.com/activitytype/lms/course",\n          "http:'
                                   '//id.tincanapi.com/activitytype/lms/module",\n          "http://id.tincanapi.com/'
                                   'activitytype/chapter",\n          "http://id.tincanapi.com/activitytype/assign",'
                                   '\n          "http://id.tincanapi.com/activitytype/quiz",\n          "http://id.tin'
                                   'canapi.com/activitytype/choice",\n          "http://id.tincanapi.com/activitytype'
                                   '/book"\n        ]\n      }\n    }\n  ]\n}')

    def test_dont_build_sync_agent(self):
        with patch('assistants.learning_locker.create_statement_forwarder') as m:
            with patch('assistants.learning_locker.get_sync_agent_forwarder') as m2:
                m.return_value = {'_id': 1}
                m2.return_value = test_data.test_build_sync_agent_get_data
                db_update.build_sync_agent()

        self.assertFalse(m.called)

    def test_no_course_with_course_id(self):
        Course.objects.all().delete()
        with self.assertRaises(ObjectDoesNotExist):
            db_update.module_update_or_create(test_data.test_database_create_assign)
