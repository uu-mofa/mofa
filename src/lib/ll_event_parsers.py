# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""This file contains parsers that parse event data from Learning Locker."""
from urllib.parse import urlparse
from django.conf import settings


def parse_viewed_courses(json):
    """
    Parse the json from Learning Locker by looping over all the statements.

    Get the id of the students in the statement which is equal to ['actor']['account']['name'].
    Add a student to the list if it is not jet in it.
    :param json: A file with all the statements of the course that is viewed since a certain time.
    :return: List of students who have viewed the course.
    """
    student_list = []
    for statement in json['statements']:
        student_id = statement['actor']['account']['name']
        if student_id not in student_list:
            student_list.append(student_id)
    return student_list


def parse_quiz_completed_feedback(json):
    """
    Parse quiz completed statement from Learning Locker and extract the needed information.

    :param json: statement from Learning Locker in json format.
    """
    statement = json['statement']
    temp_id = statement['context']['contextActivities']['grouping'][1]['id']
    temp_quiz_id = statement['object']['id']
    link_with_attempt_id = statement['context']['contextActivities']['other'][0]['id']
    return {
        'actor_name': statement['actor']['name'],
        'actor_id': statement['actor']['account']['name'],
        'quiz_name': statement['object']['definition']['name']['en'],
        'quiz_id': int(temp_quiz_id.split("id=")[1]),
        'score': statement['result']['score']['scaled'],
        'course_name': statement['context']['contextActivities']['grouping'][1]['definition']['name']['en'],
        'course_id': int(temp_id.split("id=")[1]),
        'attempt_id': int(link_with_attempt_id.split("attempt=")[1].split("&")[0])
    }


def parse_new_activity_created(json):
    """
    Parse the incoming JSON.

    Extract the course id, course name and name of the new activity.
    :param json: Incoming JSON.
    :return: Parsed values for course id, course name and activity name.
    """
    statement = json['statement']
    courseid = statement['context']['contextActivities']['grouping'][1]['id']
    object_id = statement['object']['id']
    activity_type = "assignment"
    if "quiz" in object_id:
        activity_type = "quiz"

    return {
        'courseId': int(courseid.split("id=")[1]),
        'course_name': statement['context']['contextActivities']['grouping'][1]['definition']['name']['en'],
        'activity_name': statement['object']['definition']['name']['en'],
        'activity_type': activity_type
    }


def check_sync_agent_type(json):
    """
    Check the type of the object of the incoming statement.

    :param json: Incoming JSON containing the xapi statement
    :return: boolean. True means course, false means module
    """
    statement = json['statement']
    obj_type = statement['object']['definition']['type'].split('/')[-1]

    return obj_type == 'course'


def parse_module_sync_agent_data(json):
    """
    Parse the incoming json for a sync agent event concerning a module.

    :param json: Incoming JSON
    :return: Parsed values: course id, object, ...
    """
    statement = json['statement']
    course_id = int(statement['context']['contextActivities']['grouping'][1]['id'].split('=')[-1])
    actor_id = int(statement['actor']['account']['name'])
    verb = statement['verb']['display']['en']
    object_target = urlparse(statement['object']['id'])._replace(netloc=settings.MOODLE_BASE_URL).geturl()
    object_id = int(object_target.split('=')[-1])
    obj_type = urlparse(object_target).path.split('/')[2]
    object_name = statement['object']['definition']['name']['en']

    if obj_type == 'book':
        object_type = urlparse(statement['object']['definition']['type']).path.split('/')[-1]
        if object_type == 'chapter':
            obj_type = object_type

    return {
        'courseId': course_id,
        'verb': verb,
        'target': object_target,
        'type': obj_type,
        'external_id': object_id,
        'name': object_name,
        'actor_id': actor_id
    }


def parse_course_sync_agent_data(json):
    """
    Parse the incoming json for a sync agent event concerning a course.

    :param json: incoming JSON
    :return: the parsed values needed to perform the database change.
    """
    statement = json['statement']
    course_id = statement['object']['id'].split('=')[-1]
    actor_id = int(statement['actor']['account']['name'])
    platform = statement['context']['contextActivities']['category'][0]['definition']['name']['en'].lower()
    course_name = statement['object']['definition']['name']['en']
    verb = statement['verb']['display']['en']

    return {
        'courseId': course_id,
        'platform': platform,
        'course_name': course_name,
        'verb': verb,
        'actor_id': actor_id
    }
