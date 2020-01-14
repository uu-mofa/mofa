# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

import json
from unittest.mock import patch, call
from django.test import TestCase

from . import test_data
from assistants import models as assistant_models
from courses import models as courses_models
from lib.tests import test_data as lib_test_data


class QuizCompletedFeedbackViewTest(TestCase):
    def test_quiz_completed_feedback(self):
        course = assistant_models.Course.objects.create(name='Course 1', courseId=1, inactivity=False, deadline=False)
        quiz = assistant_models.Quiz.objects.create(course_id=1, name="Test_quiz1", external_id=18)
        with patch('assistants.learning_locker.create_statement_forwarder') as ll:
            ll.return_value = {'_id': 1}
            with patch('assistants.learning_locker.get_questions_answered') as answered:
                answered.return_value = test_data.test_get_questions
                assistant_models.QuizCompletedFeedback.objects.create(course=course, quiz=quiz, forwarder_id=1,
                                                                      threshold=5.00, question_feedback=False)
                with patch('assistants.feedback_manager.get_questions_feedback') as get_q:
                    get_q.return_value = ''
                    with patch('assistants.moodle.send_message') as m:
                        response = self.client.post('/assistants/api/quiz_completed_feedback/1/',
                                                    json.dumps(test_data.test_parse_quiz_completed_feedback),
                                                    content_type="application/json")
                    self.assertEqual(200, response.status_code)
                    m.assert_called_with('3', 'Hi Will Smith,\n '
                                              'You have completed the quiz "Testquiz1" '
                                              'for the course "BeginningCourse". '
                                              'Your result was 0, maybe you should look at: the course resource')


class NewActivityNotificationTest(TestCase):
    def test_new_activity_notification(self):
        # Mock the course.
        course = courses_models.Course.objects.create(name='Test_Course', courseId=1, inactivity=False, deadline=False)
        # Mock learning locker.
        with patch('assistants.learning_locker.create_statement_forwarder') as ll:
            ll.return_value = {'_id': 1}
            assistant_models.NewActivityCreated.objects.create(course=course, forwarder_id=1)
            # Mock the get_enrolled_users XML.
            with patch('assistants.moodle.get_enrolled_users') as g:
                # Mock the send message to Moodle.
                with patch('assistants.moodle.send_message') as m:
                    g.return_value = lib_test_data.test_parse_enrolled_users
                    response = self.client.post('/assistants/api/new_activity_notification/1/',
                                                json.dumps(lib_test_data.test_parse_new_activity_created_data),
                                                content_type="application/json")
            # Check the status code of the response.
            self.assertEqual(200, response.status_code)
            # Check if the get enrolled users is called for the correct course ID.
            g.assert_called_with(1)
            # Check how many times enrolled users is called.
            self.assertEqual(g.call_count, 1)
            # Check how many times send message is called.
            self.assertEqual(m.call_count, 4)
            # Check if the message is send to all the enrolled students of the course.
            messagetext = "For the course Test_Course the quiz Test_Activity is added."
            m.assert_has_calls([call.send_message("2", messagetext), call.send_message("3", messagetext),
                                call.send_message("4", messagetext), call.send_message("5", messagetext)]
                               )

    def test_new_activity_notification_get(self):
        resp = self.client.get('/assistants/api/new_activity_notification/1/')
        self.assertEqual(400, resp.status_code)


class SyncAgentTest(TestCase):
    def test_sync_agent(self):
        with patch('assistants.moodle.send_bulk_messages'):
            courses_models.Course.objects.create(name='Test_Course', courseId=2, inactivity=False, deadline=False)
            self.client.post('/assistants/api/sync_agent/', json.dumps(lib_test_data.sync_agent_test_data),
                             content_type='application/json')
            self.assertEqual(courses_models.Resource.objects.count(), 1)
            self.client.post('/assistants/api/sync_agent/', json.dumps(lib_test_data.sync_agent_test_data_chapter),
                             content_type='application/json')
            self.assertEqual(courses_models.Resource.objects.count(), 2)

    def test_sync_agent_get(self):
        resp = self.client.get('/assistants/api/sync_agent/')
        self.assertEqual(400, resp.status_code)
