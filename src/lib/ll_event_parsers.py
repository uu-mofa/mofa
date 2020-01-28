# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""This file contains parsers that parse event data from Learning Locker."""
from urllib.parse import urlparse
from django.conf import settings


def parse_viewed_courses(json):
    """
    Parse course viewed statements.

    Extract the students that have viewed the course from the course viewed statements.
    Return a list of those students.

    :param json: All the course viewed statements since a certain time.
    :type json: dict(str, str)
    :return: List of students who have viewed the course.
    :rtype: list(str)
    """
    student_list = []
    for statement in json['statements']:
        student_id = statement['actor']['account']['name']
        if student_id not in student_list:
            student_list.append(student_id)

    return student_list


def parse_quiz_completed_feedback(json):
    """
    Parse quiz completed statements.

    Receives a quiz completed statement.
    Extract from that statement the actor, quiz and course names and ids. Also extract the score and attempt id.

    :param json: A quiz completed statement.
    :type json: dict(str, NoneType)
    :return: A dictionary containing the score and attempt id as well as actor, quiz and course names and ids.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    temp_id = statement['context']['contextActivities']['grouping'][1]['id']
    temp_quiz_id = statement['object']['id']
    link_with_attempt_id = statement['context']['contextActivities']['other'][0]['id']
    statement_quiz_completed = {
        'statement_id': statement['id'],
        'actor_name': statement['actor']['name'],
        'actor_id': statement['actor']['account']['name'],
        'quiz_name': statement['object']['definition']['name']['en'],
        'quiz_id': int(temp_quiz_id.split("id=")[1]),
        'score': statement['result']['score']['scaled'],
        'course_name': statement['context']['contextActivities']['grouping'][1]['definition']['name']['en'],
        'course_id': int(temp_id.split("id=")[1]),
        'attempt_id': int(link_with_attempt_id.split("attempt=")[1].split("&")[0])
    }
    return statement_quiz_completed


def parse_new_activity_created(json):
    """
    Parse a module created statement.

    Receives a statement of module created.
    Extract from that statement the course id, course name and name and type of the new activity.

    :param json: A module created statement.
    :type json: dict(str, dict(str, str))
    :return: A dictionary containing the course id and name, and module name and type.
    :rtype: dict(str, int)
    """
    statement = json['statement']
    temp_course_id = statement['context']['contextActivities']['grouping'][1]['id']
    temp_object_id = statement['object']['id']
    activity_type = "assignment"
    if "quiz" in temp_object_id:
        activity_type = "quiz"

    statement_new_activity = {
        'statement_id': statement['id'],
        'courseId': int(temp_course_id.split("id=")[1]),
        'course_name': statement['context']['contextActivities']['grouping'][1]['definition']['name']['en'],
        'activity_name': statement['object']['definition']['name']['en'],
        'activity_type': activity_type
    }
    return statement_new_activity


def check_course_sync_agent_type(json):
    """
    Check if the type of the incoming statement is course.

    :param json: A statement, possibly with type course.
    :type json: union(dict(str, NoneType), dict(str, dict(str, str)))
    :return: A boolean, true if the type of the incoming statement is a course, false otherwise.
    :rtype: bool
    """
    obj_type = json['statement']['object']['definition']['type'].split("/")[-1]
    check_course = (obj_type == "course")
    return check_course


def check_user_sync_agent_type(json):
    """
    Check type of incoming user statement.

    :param json: A user statement.
    :type json: dict(str, NoneType)
    :return: The type of the verb of the statement.
    :rtype: str
    """
    obj_type = json['statement']['verb']['display']['en']
    return obj_type


def check_question_update_data(json):
    """
    Check if there is data about questions present in the statement.

    :param json: A quiz edit page viewed statement.
    :type json: dict(str, NoneType)
    :return: A boolean, true if there is data about questions, false otherwise.
    :rtype: bool
    """
    statement = json['statement']['context']['extensions']['http://activitystrea.ms/schema/1.0/question']
    check_question_data = (len(statement) != 0)
    return check_question_data


def parse_module_sync_agent_data(json):
    """
    Parse the statement of a module that has to be synced.

    :param json: A statement of a module that has to be synced.
    :type json: union(dict(str, NoneType), dict(str, dict(str, str)))
    :return: A dictionary containing the course id, verb, target, type, external id, name of the object and actor id.
    :rtype: dict(str, int)
    """
    statement = json['statement']
    course_id = int(statement['context']['contextActivities']['grouping'][1]['id'].split("=")[-1])
    actor_id = int(statement['actor']['account']['name'])
    verb = statement['verb']['display']['en']
    object_target = \
        urlparse(statement['object']['id'])._replace(netloc=urlparse(settings.MOODLE_BASE_URL).netloc).geturl()
    object_id = int(object_target.split("=")[-1])
    obj_type = urlparse(object_target).path.split("/")[2]
    object_name = statement['object']['definition']['name']['en']

    if obj_type == "book":
        object_type = urlparse(statement['object']['definition']['type']).path.split("/")[-1]
        if object_type == "chapter":
            obj_type = object_type

    sync_module_data = {
        'courseId': course_id,
        'verb': verb,
        'target': object_target,
        'type': obj_type,
        'external_id': object_id,
        'name': object_name,
        'actor_id': actor_id
    }
    return sync_module_data


def parse_course_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a course.

    :param json: A statement concerning a course that needs to be synced.
    :type json: dict(str, NoneType)
    :return: A dictionary containing the course id, platform, course name, verb and actor id of the statement.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    course_id = statement['object']['id'].split("=")[-1]
    actor_id = int(statement['actor']['account']['name'])
    platform = statement['context']['contextActivities']['category'][0]['definition']['name']['en']
    course_name = statement['object']['definition']['name']['en']
    verb = statement['verb']['display']['en']
    sync_course_data = {
        'courseId': course_id,
        'platform': platform,
        'course_name': course_name,
        'verb': verb,
        'actor_id': actor_id
    }
    return sync_course_data


def parse_user_assign_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a user role assignment.

    :param json: A statement concerning a user role assignment that needs to be synced.
    :type json: dict(str, NoneType)
    :return: A dictionary containing all user information, a course id, and its role for that course.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    role = statement['object']['definition']['name']['en']
    course_id = statement['object']['id'].split("=")[-1]
    user_info = statement['context']['extensions']['http://id.tincanapi.com/activitytype/role']
    sync_user_role_data = {
        'role': role,
        'course_id': course_id,
    }
    sync_user_role_data.update(user_info)
    return sync_user_role_data


def parse_user_unassign_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a user role unassignment.

    :param json: A statement concerning a user role unassignment that needs to be synced.
    :type json: union(dict(str, NoneType), dict(str, dict(str, str)))
    :return: A dictionary containing a user id, a course id, and the unassigned role for that course.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    role = statement['object']['definition']['name']['en']
    course_id = statement['object']['id'].split("=")[-1]
    user_id = statement['actor']['account']['name']
    sync_unassign_role_data = {
        'role': role,
        'course_id': course_id,
        'user_id': user_id,
    }
    return sync_unassign_role_data


def parse_user_delete_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a user deletion.

    :param json: A statement concerning a user deletion.
    :type json: dict(str, NoneType)
    :return: A dictionary containing the user id of the deleted user.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    user_id = statement['object']['id'].split("=")[-1]
    sync_user_delete_data = {
        'user_id': user_id,
    }
    return sync_user_delete_data


def parse_user_update_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a user update.

    :param json: A statement concerning a user update that needs to be synced.
    :type json: dict(str, NoneType)
    :return: A dictionary containing all user information of the updated user.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    user_info = statement['context']['extensions']['http://id.tincanapi.com/activitytype/update']
    return user_info


def parse_question_update_sync_agent_data(json):
    """
    Parse the incoming statement for a sync agent event concerning a question update.

    :param json: A statement concerning a question update.
    :type json: dict(str, NoneType)
    :return: A dictionary containing a course id, quiz id and all question information.
    :rtype: dict(str, str)
    """
    statement = json['statement']
    questions_info = statement['context']['extensions']['http://activitystrea.ms/schema/1.0/question']
    course_id = statement['context']['contextActivities']['grouping'][1]['id'].split("=")[-1]
    quiz_id = statement['object']['id'].split("=")[-1]
    question_update_data = {
        'course_id': course_id,
        'quiz_id': quiz_id,
        'questions': questions_info
    }
    return question_update_data
