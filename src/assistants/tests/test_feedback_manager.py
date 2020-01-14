# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Testing the Feedback Manager."""

from django.test import TestCase
from unittest.mock import patch
from . import test_data
from assistants import feedback_manager
from assistants import models
from courses.models import Course, Resource, Quiz, Subject, Question


class FeedbackMangerTest(TestCase):
    def test_get_questions_feedback(self):
        params = {
            'actor_name': 'test_name',
            'actor_id': 1,
            'quiz_name': 'test_quiz',
            'quiz_id': 1,
            'score': 0.6,
            'course_name': 'test_course',
            'course_id': 1,
            'attempt_id': 1
        }
        with patch('assistants.feedback_manager.get_question_feedback_link') as x:
            x.return_value = '<br></br><a href="site">chapter 1</a>'
            string = feedback_manager.get_questions_feedback(params, True, test_data.test_get_questions)
            test_string = 'Hi test_name,\n You have completed the quiz "test_quiz" for the course' \
                          ' "test_course". Your result was 6.0. For information about the topics of the questions ' \
                          'you answered wrong, please take a look at: <br></br><a href="site">chapter 1</a>'
            self.assertEqual(string, test_string)

    def test_get_question_feedback_link(self):
        course = models.Course.objects.create(name='Course 0', courseId=1, inactivity=False, deadline=False)
        quiz = models.Quiz.objects.create(course_id=1, name="Test_quiz1", external_id=18)
        resource = Resource.objects.create(course=course, name='chapter 1', type='Book', target="site",
                                           external_id=8)
        q = Question.objects.create(course=course, name='test_question', quiz=quiz, external_id=8, subjects=None)
        q.resources.add(resource)
        result = feedback_manager.get_question_feedback_link(test_data.test_get_questions)
        expected = '<p><a href="site">chapter 1</a></p>'
        self.assertEqual(result, expected)

        course1 = models.Course.objects.create(name='Course 1', courseId=2, inactivity=False, deadline=False)
        quiz1 = models.Quiz.objects.create(course_id=2, name="Test_quiz1", external_id=19)
        resource1 = Resource.objects.create(course=course, name='chapter 2', type='Book', target="course1/site1",
                                            external_id=9)
        resource2 = Resource.objects.create(course=course, name='chapter 3', type='Book', target="course2/site1",
                                            external_id=10)
        subject = Subject.objects.create(name="subject", course=course1)
        subject.resources.add(resource1)
        subject.resources.add(resource2)
        Question.objects.create(course=course1, name='test_question', quiz=quiz1, external_id=9, subjects=subject)
        expected = '<p><a href="course1/site1">chapter 2</a></p><p><a href="course2/site1">chapter 3</a></p>'
        result = feedback_manager.get_question_feedback_link(test_data.test_get_questions2)
        self.assertEqual(expected, result)


class BuildQuizCompletedFeedbackTest(TestCase):
    def test_build_completed_quiz_feedback(self):
        message = feedback_manager.build_completed_quiz_feedback('test_actor', 'test_quiz',
                                                                 'test_course', 'test_score', 'test_feedback')
        self.assertEqual(
            'Hi test_actor,\n You have completed the quiz "test_quiz" for the course "test_course". '
            'Your result was test_score, maybe you should look at: test_feedback', message)


class GetQuizCompletedFeedbackTest(TestCase):
    def test_get_quiz_feedback_with_no_resource_and_no_subjects(self):
        Course.objects.create(pk=159, name="Test_course1", courseId=1)
        Quiz.objects.create(course_id=159, name="Test_quiz1", external_id=18)

        self.assertEqual(feedback_manager.get_quiz_feedback_link(18), "the course resource")

    def test_get_quiz_feedback_with_only_resource(self):
        # fill database
        Course.objects.create(pk=159, name="Test_course1", courseId=1)
        quiz = Quiz(course_id=159, name="Test_quiz1", external_id=18)
        resource = Resource(course_id=159, name="Book 1", target="http://localhost:4000/mod/book/view.php?id=12",
                            type="book", external=False, external_id=12)
        quiz.save()
        resource.save()

        # add the link of the many to many relationship between quizzes and resource
        quiz.resources.add(resource)
        message = '<a href="http://localhost:4000/mod/book/view.php?id=12">Book 1</a>'
        self.assertEqual(feedback_manager.get_quiz_feedback_link(18), message)

    def test_get_quiz_feedback_with_only_subjects_and_linked_resource(self):
        # fill database
        course = Course(pk=159, name="Test_course1", courseId=1)
        course.save()

        Quiz.objects.create(course_id=159, name="Test_quiz1", external_id=18, subjects_id=1)
        resource = Resource(course_id=159, name="Book 1", target="http://localhost:4000/mod/book/view.php?id=12",
                            type="book", external=False, external_id=12)
        resource.save()

        subject = Subject(course=course, name="Test_subject1")
        subject.save()

        # add the link between subjects and resources
        subject.resources.add(resource)
        message = '\r\n- <a href="http://localhost:4000/mod/book/view.php?id=12">Book 1</a>'
        self.assertEqual(feedback_manager.get_quiz_feedback_link(18), message)

    def test_get_quiz_feedback_with_only_subjects_and_no_linked_resource(self):
        # fill database
        course = Course(pk=159, name="Test_course1", courseId=1)
        course.save()

        Quiz.objects.create(course_id=159, name="Test_quiz1", external_id=18, subjects_id=1)
        resource = Resource(course_id=159, name="Book 1", target="http://localhost:4000/mod/book/view.php?id=12",
                            type="book", external=False, external_id=12)
        resource.save()

        subject = Subject(course=course, name="Test_subject1")
        subject.save()

        self.assertEqual(feedback_manager.get_quiz_feedback_link(18), "the course resource")
