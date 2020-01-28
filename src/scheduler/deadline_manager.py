# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""Handle deadline related feedback."""
import time
import assistants.moodle as moodle_api
from lib import moodle_get_parsers as parser


def get_deadlines_between(assignment_list, start_time, end_time):
    """
    Filter the passed deadlines from the given assignment list.

    :param assignment_list: List of assignments that need to be checked.
    :type assignment_list: list(dict(str,int))
    :param start_time: Time that the deadline needs to have passed.
    :type start_time: int
    :param end_time: Time that the deadline must not have passed yet.
    :type end_time: int
    :return: Dictionary of all the assignments with its passed deadlines.
    :rtype: dict(int, (str, int))
    """
    passed_deadlines = {}
    for assignment in assignment_list:
        assignment_id, due_date, name = parser.parse_single_assignment(assignment)
        if start_time < due_date < end_time:
            passed_deadlines[assignment_id] = (name, due_date)
    return passed_deadlines


def get_assignments(course_id):
    """
    Get all assignments in the course.

    :param course_id: Id of the course that is checked.
    :type course_id: int
    :return: List of assignments.
    :rtype: list(dict(assignment, assignment_content))
    """
    json = moodle_api.get_assignments([course_id])
    return parser.parse_assignment_list(json)


def check_assignment_completion(user_id, assignment_id, course_id):
    """
    Check whether the assignment is completed by a user.

    :param user_id: The user id to check.
    :type user_id: int
    :param assignment_id: The assignment id to check.
    :type assignment_id: int
    :param course_id: Id of the course that is checked.
    :type course_id: int
    :return: Whether the user has completed the assignment or not.
    :rtype: bool
    """
    json = moodle_api.get_assignment_status(course_id, user_id)['statuses']
    assignment_list = [a for a in json if a['cmid'] == assignment_id]
    if len(assignment_list) > 0:
        return assignment_list[0]['state'] != 0


def get_users(course_id):
    """
    Get all users enrolled in a course.

    :param course_id: Id of the course that is checked.
    :type course_id: int
    :return: List of user ids.
    :rtype: list(int)
    """
    users = moodle_api.get_enrolled_users(course_id)
    return parser.parse_enrolled_students(users)


def convert_time(due_date):
    """
    Convert time to the due_date (in seconds) to hours and minutes.

    :param due_date: The due_date in seconds from the beginning of computers (unix-time).
    :type due_date: int
    :return: Hours and seconds until due date.
    :rtype: tuple(int, int)
    """
    remaining_secs = due_date - time.time()
    hours = remaining_secs / 3600
    minutes = (remaining_secs % 3600) / 60
    return int(hours), int(minutes)


def prep_late_warning(assignment_name):
    """
    Create a late warning message.

    :param assignment_name: Name of the assignment.
    :type assignment_name: str
    :return: A late warning message.
    :rtype: str
    """
    return "The deadline for " + assignment_name + " has passed."


def prep_early_warning(hours, minutes, assignment_name):
    """
    Create a early warning message.

    :param hours: Hours until the deadline.
    :type hours: int
    :param minutes: Minutes until the deadline.
    :type minutes: int
    :param assignment_name: Name of the assignment that approaches its deadline.
    :type assignment_name: str
    :return: An early warning message.
    :rtype: str
    """
    return f'The deadline for {assignment_name} is in {hours} hours and {minutes} minutes.'


def notify_about_passed_deadlines(course_id):
    """
    Send a message to users that have not completed an assigment of which the deadline has passed.

    :param course_id: The id of the to be checked course.
    :type course_id: int
    """
    assignment_list = get_assignments(course_id)
    passed_deadlines = get_deadlines_between(assignment_list, time.time() - 86400, time.time())

    if len(passed_deadlines) == 0:
        return

    user_id_list = get_users(course_id)
    notify_list = []
    for user_id in user_id_list:
        for assignment_id, (assignment_name, due_date) in passed_deadlines.items():
            status = check_assignment_completion(user_id, assignment_id, course_id)
            if not status:
                message = prep_late_warning(assignment_name)
                notify_list.append((user_id, message))
    send_warnings(notify_list)


def notify_about_upcoming_deadlines(time_to_deadline, course_id):
    """
    Send a message to users that have not completed an assignment that has a deadline passing soon.

    :param course_id: The id of the checked course.
    :type course_id: int
    :param time_to_deadline: Time in seconds the user should be warned in advance.
    """
    assignment_list = get_assignments(course_id)
    upcoming_deadlines = get_deadlines_between(assignment_list, time.time() + time_to_deadline - 86400,
                                               time.time() + time_to_deadline)
    if len(upcoming_deadlines) == 0:
        return

    user_id_list = get_users(course_id)
    notify_list = []
    for user_id in user_id_list:
        for assignment_id, (assignment_name, due_date) in upcoming_deadlines.items():
            status = check_assignment_completion(user_id, assignment_id, course_id)
            if not status:
                hours, minutes = convert_time(due_date)
                message = prep_early_warning(hours, minutes, assignment_name)
                notify_list.append((user_id, message))
    send_warnings(notify_list)


def send_warnings(message_list):
    """
    Send all users a deadline message.

    :param message_list: List of messages.
    :type message_list: list(tuple(int, str))
    """
    moodle_api.send_bulk_different_messages(message_list)
