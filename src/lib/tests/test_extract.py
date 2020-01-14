# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

import unittest

import lib.ll_event_parsers
import lib.moodle_get_parsers
import lib.ll_get_parsers
from . import test_data


class TestParseViewedCourses(unittest.TestCase):

    def test_parse_viewed_courses(self):
        self.assertEqual(lib.ll_event_parsers.parse_viewed_courses(test_data.test_parse_viewed_courses),
                         ['2', '5', '3', '4'])

    def test_parse_course_info(self):
        json_data = test_data.test_get_courses_by_id
        self.assertEqual(lib.moodle_get_parsers.parse_course_info(json_data), "BeginningCourse")

    def test_no_statements(self):
        self.assertEqual(lib.ll_event_parsers.parse_viewed_courses(test_data.test_parse_viewed_courses_no_statements),
                         [])


class TestParseNewActivityCreated(unittest.TestCase):
    def test_parse_new_activity_created(self):
        self.assertEqual(
            lib.ll_event_parsers.parse_new_activity_created(test_data.test_parse_new_activity_created_data),
            {'courseId': 1, 'course_name': 'Test_Course', 'activity_name': 'Test_Activity', 'activity_type': 'quiz'})


class TestParseEnrolledStudents(unittest.TestCase):
    def test_parse_students(self):
        parsed_data = lib.moodle_get_parsers.parse_enrolled_students(test_data.test_parse_enrolled_users)
        self.assertEqual(parsed_data, ['2', '3', '4', '5'])


class TestParseModules(unittest.TestCase):
    def test_parse_course_content(self):
        self.maxDiff = None
        self.assertEqual(
            lib.moodle_get_parsers.parse_get_course_contents(test_data.test_parse_get_course_contents, 1),
            test_data.test_parse_get_course_contents_result
        )


class TestParseCourses(unittest.TestCase):
    def test_parse_courses(self):
        self.assertEqual(lib.moodle_get_parsers.parse_courses(test_data.test_parse_get_courses),
                         [{'courseId': 2, 'name': 'Testing Course'}, {'courseId': 3, 'name': 'Inactivity Test Course'},
                          {'courseId': 4, 'name': 'Deadline Test Course'}])


class TestSyncAgentParse(unittest.TestCase):
    def test_sync_agent_parse(self):
        self.assertEqual(lib.ll_event_parsers.parse_module_sync_agent_data(test_data.sync_agent_test_data),
                         {'courseId': 2, 'verb': 'created', 'target': 'http://MOODLE_BASE_URL/mod/book/view.php?id=13',
                          'type': 'book', 'name': 'Advanced Python', 'external_id': 13, 'actor_id': 2}
                         )

    def test_sync_agent_chapter_parse(self):
        self.assertEqual(lib.ll_event_parsers.parse_module_sync_agent_data(test_data.sync_agent_test_data_chapter),
                         {'courseId': 2, 'verb': 'created',
                          'target': 'http://MOODLE_BASE_URL/mod/book/view.php?id=13&chapterid=2',
                          'type': 'chapter', 'name': 'Advanced lambda statements', 'external_id': 2, 'actor_id': 2
                          })

    def test_course_sync_agent_parse(self):
        self.assertEqual(lib.ll_event_parsers.parse_course_sync_agent_data(test_data.test_course_sync_agent_parser),
                         {'courseId': '16', 'course_name': 'Ruby tutorial', 'platform': 'moodle', 'verb': 'created',
                          'actor_id': 2})

    def test_sync_agent_type_check(self):
        self.assertFalse(lib.ll_event_parsers.check_sync_agent_type(test_data.sync_agent_test_data))


class TestParseQuizQuestions(unittest.TestCase):
    def test_parse_quiz_question(self):
        self.assertEqual(lib.ll_get_parsers.parse_quiz_questions(test_data.test_parse_quiz_question),
                         test_data.test_parse_quiz_question_data)

    def test_parse_quiz_question_no_questions(self):
        self.assertEqual(lib.ll_get_parsers.parse_quiz_questions(test_data.test_no_questions_quiz_question_data),
                         {27: []})
