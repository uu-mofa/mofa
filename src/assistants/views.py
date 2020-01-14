# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""Views are created here."""
import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

import lib.ll_event_parsers
import lib.moodle_get_parsers
import lib.ll_get_parsers
from assistants.models import DESTINATIONS
from . import models
from assistants import feedback_manager
from assistants import learning_locker
import assistants.sync_agent as sync_agent


@csrf_exempt
def quiz_completed_feedback(request, action_id):
    """Obtain statement forwards from LRS."""
    if request.method == 'POST':
        action = models.QuizCompletedFeedback.objects.get(id=action_id)
        api = DESTINATIONS[action.destination]
        request_json = json.loads(request.body)
        params = parsers[action.event](request_json)
        if action.question_feedback:
            questions_json = learning_locker.get_questions_answered(params['attempt_id'], params['quiz_id'])
            questions = lib.ll_get_parsers.parse_questions_answered(questions_json)
            question_message = feedback_manager.get_questions_feedback(params, action.question_feedback, questions)
            if not question_message == '':
                api.send_message(params['actor_id'], question_message)
        else:
            quiz_message = feedback_manager.get_quiz_feedback(params, action)
            if not quiz_message == '':
                api.send_message(params['actor_id'], quiz_message)
        return HttpResponse('POST request: {0}'.format('Assistant successfully run'))
    return HttpResponseBadRequest('Invalid data')


@csrf_exempt
def new_activity_notification(request, action_id):
    """
    Obtain statement forwards from LRS when "created" is called.

    When created is for a course, do nothing. When it is for a module (activity) send a message about the new
    activity to all the enrolled users of that course.
    """
    if request.method == 'POST':
        action = models.NewActivityCreated.objects.get(id=action_id)
        request_json = json.loads(request.body)
        object_id = request_json['statement']['object']['id']
        # Check if it is an assignment/quiz that is being created. If not do nothing.
        if "quiz" in object_id or "assign" in object_id:
            params = parsers[action.event](request_json)
            message = models.build_new_activity_notification(params['course_name'], params['activity_name'],
                                                             params['activity_type'])
            api = DESTINATIONS[action.destination]
            students_in_JSON = api.get_enrolled_users(params['courseId'])
            student_ids = lib.moodle_get_parsers.parse_enrolled_students(students_in_JSON)
            # Send all students that are enrolled in the course the message about the new activity.
            for student in student_ids:
                api.send_message(student, message)
        return HttpResponse('POST request: {0}'.format('Assistant successfully run'))
    return HttpResponseBadRequest('Invalid data')


@csrf_exempt
def sync_agent_execute(request):
    """
    Execute update of database when a course changes.

    :param request: contains the request information of learning locker
    :return: http response
    """
    if request.method == 'POST':
        request_json = json.loads(request.body)
        is_course = lib.ll_event_parsers.check_sync_agent_type(request_json)
        if is_course:
            parsed_json = lib.ll_event_parsers.parse_course_sync_agent_data(request_json)
            course_database_actions[parsed_json['verb']](parsed_json)
        else:
            parsed_json = lib.ll_event_parsers.parse_module_sync_agent_data(request_json)
            module_database_actions[parsed_json['verb']](parsed_json)

        return HttpResponse('POST request: Database successfully updated}')
    return HttpResponseBadRequest('Invalid data')


parsers = {
    'http://activitystrea.ms/schema/1.0/create': lib.ll_event_parsers.parse_new_activity_created,
    'http://adlnet.gov/expapi/verbs/completed': lib.ll_event_parsers.parse_quiz_completed_feedback,
}

module_database_actions = {
    'created': sync_agent.module_update_or_create,
    'updated': sync_agent.module_update_or_create,
    'deleted': sync_agent.module_delete,
}

course_database_actions = {
    'created': sync_agent.course_update_or_create,
    'updated': sync_agent.course_update_or_create,
    'deleted': sync_agent.course_delete,
}
