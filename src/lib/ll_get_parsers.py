# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""This file contains all parsers that parse information gotten from LearningLocker API calls."""
import re
from assistants import logger


def parse_statement_forwarder_id(json):
    """
    Extract the statement forwarder id from the post response.

    :param json: JSON text to parse
    :type json
    :return: Return the statement forwarder id
    :rtype: str
    """
    return json['_id']


def parse_quiz_questions(json):
    """Extract the quiz questions from LL get request."""
    try:
        json_statement = json['statements'][0]
    except IndexError:
        logger.log_text(text="The quiz edit page was not viewed for one of the quizzes.")
        return {}
    else:
        quiz_questions = json_statement['context']['extensions']['http://activitystrea.ms/schema/1.0/question']
        quiz_id = re.search("(?<=cmid=).*", json_statement['object']['id'])
        if quiz_id is None:
            raise Exception("No quiz id found in the quiz questions")
        else:
            return {int(quiz_id.group()): quiz_questions}


def parse_sync_agent_forwarder_id(json):
    """
    Extract the sync agent forwarder id from the get response.

    :param json: JSON text to parse
    :return: the statement forwarder id
    """
    return json['edges'][0]['node']['_id'] if len(json['edges']) > 0 else 0


def parse_questions_answered(json):
    """
    Parse Json to extract answers and questions.

    :param json: json file
    :return:
    """
    edges = json['edges']
    question_id = {}
    for question in edges:
        temp_link = question['node']['statement']['object']['id']
        question_id[(temp_link.split('id=')[2])] = question['node']['statement']['result']['success']
    return question_id
