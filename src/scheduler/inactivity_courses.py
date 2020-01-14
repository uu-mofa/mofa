# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Handle the inactivity for a course."""
import datetime as dt

import lib.ll_event_parsers
import assistants.learning_locker as ll_api
import assistants.moodle as moodle_api
from lib.moodle_get_parsers import parse_enrolled_students, parse_course_info


def create_job(course_id, time_not_active):
    """
    Call all the methods that are needs to check the inactivity.

    :param course_id: Id of the course the inactivity needs to be checked for
    :param time_not_active: Time interval the inactivity needs to be checked for
    :return: Sends a message to the students who have been inactive
    """
    time = calculate_date(dt.date.today(), time_not_active)
    viewed_courses = ll_api.get_viewed_courses(time, course_id)
    list_viewed = lib.ll_event_parsers.parse_viewed_courses(viewed_courses)
    enrolled_students = parse_enrolled_students(moodle_api.get_enrolled_users(course_id))
    course_name = parse_course_info(moodle_api.get_course_by_id_field(course_id))
    students = students_not_viewed(enrolled_students, list_viewed)
    message = get_message(course_name, time_not_active)
    send_message(students, message)


def calculate_date(date_today, time_not_active):
    """
    Calculate the date since when the inactivity needs to be checked for.

    :param date_today:
    :param time_not_active: Integer
    :return: a date
    """
    return date_today - dt.timedelta(days=time_not_active)


def students_not_viewed(students, list_viewed):
    """
    Determine which students need to be send a message.

    :param students: List of the enrolled students
    :param list_viewed: List of the students who have viewed a course
    :return: A list of student ids
    """
    return list(set(students) - set(list_viewed))


def get_message(course_name, time_not_active):
    """
    Format the message that needs to be send.

    :param course_name: A string
    :param time_not_active: An integer
    :return: message to be send to users
    """
    return "You have not viewed the course {} in {} day(s). We advise you to check it.".format(
        course_name,
        time_not_active)


def send_message(students, message):
    """
    Loop over all the list of student ids an student a message to every student in the list.

    :param students: List of student ids
    :param message: String of the message
    :return: Sends a message to Moodle
    """
    students = set(students)
    moodle_api.send_bulk_messages(students, message)
