# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""deadlineManager file."""
import time
import assistants.moodle as moodle_api
from lib import moodle_get_parsers as parser


def get_deadlines_between(assignment_list, start_time, end_time):
    """
    Get the assignments that have deadlines that passed between start_time and end_time.

    :param assignment_list: list containing all assignments from moodle
    :param start_time: lower border of time in which a deadline should be
    :param end_time: upper border of time in which a deadline should be
    :return: dictionary of assignment id and the assignment name
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

    :param course_id: id of the course that is checked
    :return: list of assignments in json
    """
    json = moodle_api.get_assignments([course_id])
    return parser.parse_assignment_list(json)


def check_assignment_completion(user_id, assignment_id, course_id):
    """Check whether the assignment is completed by a user.

    :param user_id: the user id to check
    :param assignment_id: the assignment id to check
    :param course_id: id of the course that is checked
    :return: true if the assignment has been completed, false if the assignment has not been completed
    """
    json = moodle_api.get_assignment_status(course_id, user_id)['statuses']
    assignment_list = [a for a in json if a['cmid'] == assignment_id]
    if len(assignment_list) > 0:
        return assignment_list[0]['state'] != 0


def get_users(course_id):
    """
    Get all users enrolled in a course.

    :param course_id: id of the course that is checked
    :return: list of user ids
    """
    users = moodle_api.get_enrolled_users(course_id)
    return parser.parse_enrolled_students(users)


def convert_time(due_date):
    """
    Convert time to the due_date (in seconds) to hours and minutes.

    :param due_date: the due_date in seconds from the beginning of computers
    :return: hours and seconds until due date
    """
    remaining_secs = due_date - time.time()
    hours = remaining_secs / 3600
    minutes = (remaining_secs % 3600) / 60
    return int(hours), int(minutes)


def prep_late_warning(assignment_name):
    """
    Create a late warning message.

    :param assignment_name: name of the assignment
    :return: a late warning message (string)
    """
    return "The deadline for " + assignment_name + " has passed."


def prep_early_warning(hours, minutes, assignment_name):
    """
    Create a early warning message.

    :param hours: hours until the deadline +
    :param minutes: minutes until the deadline
    :param assignment_name: name of the assignment that approaches its deadline
    :return: a early warning message (string)
    """
    return f'The deadline for {assignment_name} is in {hours} hours and {minutes} minutes.'


def notify_about_passed_deadlines(course_id):
    """
    Send a message to users that have not completed an assigment of which the deadline has passed.

    :param course_id: the id of the to be checked course
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

    :param course_id: the id of the checked course
    :param time_to_deadline: time in seconds the user should be warned in advance
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

    :param message_list: list of tuples (user_id, message)
    """
    moodle_api.send_bulk_different_messages(message_list)
