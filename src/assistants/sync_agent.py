# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""File contains functions that update the resources and assignments in the database."""

from django.template import loader
from django.core.exceptions import ObjectDoesNotExist

from courses.models import Course
import assistants.learning_locker as ll_api
import assistants.moodle as moodle_api
import lib.ll_get_parsers as ll_get
from assistants.logger import log_assistants


def module_update_or_create(module):
    """
    Create new resource or update resource of a certain course.

    :param module: contains the necessary info of the new resource (dict)
    :param request: the request variable for the admin message
    """
    try:
        course = Course.objects.get(courseId=module['courseId'])
    except ObjectDoesNotExist:
        log_assistants(f'The course object with id: {module["courseId"]} does not exist!', 'Sync Agent')
        raise ObjectDoesNotExist(f'The course object with id: {module["courseId"]} does not exist!')

    object_type = module['type']

    defaults = {'name': module['name'], 'course': course}
    kwargs = {'external_id': module['external_id'], 'defaults': defaults}

    if object_type == 'assign':
        _, created = course.assignment_set.update_or_create(**kwargs)
    elif object_type == 'quiz':
        _, created = course.quiz_set.update_or_create(**kwargs)
    elif object_type == 'choice':
        _, created = course.choice_set.update_or_create(**kwargs)
    else:
        kwargs.update({'target': module['target'], 'type': object_type, 'external': False})
        _, created = course.resource_set.update_or_create(**kwargs)

    if created:
        message = f'{module["name"]} has been created in the Mofa database.'
    else:
        message = f'{module["name"]} has been updated in the Mofa database.'

    send_update_notification(course, message)


def module_delete(module):
    """
    Delete certain resource from a certain course.

    :param module: contains the necessary info of the to be deleted course (dict)
    """
    course = Course.objects.get(courseId=module['courseId'])
    object_type = module['type']
    try:
        kwargs = {'external_id': module['external_id']}
        if object_type == 'assign':
            assignment = course.assignment_set.get(**kwargs)
            name = assignment.name
            assignment.delete()
        elif object_type == 'quiz':
            quiz = course.quiz_set.get(**kwargs)
            name = quiz.name
            for agent in course.quizcompletedfeedback_set.filter(quiz=quiz):
                agent.delete()
            quiz.delete()
        elif object_type == 'choice':
            choice = course.choice_set.get(**kwargs)
            name = choice.name
            choice.delete()
        else:
            kwargs = {'target': module['target']}
            content = course.resource_set.get(**kwargs)
            name = content.name
            content.delete()
    except ObjectDoesNotExist:
        log_assistants('sync agent tried to delete an object not present in the database, is it perhaps asynchronous?',
                       'Sync Agent')
        return

    message = f'{name} has been deleted from the Mofa database. '
    send_update_notification(course, message)


def course_update_or_create(course):
    """
    Create or update a course entry in the database.

    :param course: contains all necessary info for a creation or an update
    """
    defaults = {'name': course['course_name']}
    kwargs = {'courseId': course['courseId'], 'platform': course['platform'], 'defaults': defaults}
    Course.objects.update_or_create(**kwargs)


def course_delete(course):
    """
    Delete a course entry in the database.

    :param course: contains all necessary info for a deletion
    """
    kwargs = {'courseId': course['courseId']}
    Course.objects.filter(**kwargs).delete()


def build_sync_agent():
    """Build a sync_agent based on if it already present in the database or not."""
    forwarder_id = ll_get.parse_sync_agent_forwarder_id(ll_api.get_sync_agent_forwarder())
    if forwarder_id != 0:
        return
    create_sync_agent()


def create_sync_agent():
    """Create a sync agent."""
    context = {
        'create': 'http://activitystrea.ms/schema/1.0/create',
        'update': 'http://activitystrea.ms/schema/1.0/update',
        'delete': 'http://activitystrea.ms/schema/1.0/delete'

    }
    query = loader.render_to_string('assistants/sync_agent_query.json', context)
    ll_api.create_statement_forwarder('sync_agent', query=query)


def send_update_notification(course, message):
    """
    Send a message to all admin users linked to the course.

    :param course: course in which a module has changed
    :param message: the message that has to be sent
    """
    user_list = []
    for user in course.user_set.all():
        user_list.append(user.moodle_id)
    if len(user_list) > 0:
        moodle_api.send_bulk_messages(user_list, message)
