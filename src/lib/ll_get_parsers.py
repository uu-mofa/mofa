# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""This file contains all parsers that parse information gotten from LearningLocker API calls."""
import re
from assistants import logger


def parse_statement_forwarder_id(json):
    """
    Extract the statement forwarder id from the post response.

    :param json: JSON from the post response from LearningLocker.
    :type json: dict(str, dict(str, str))
    :return: The extracted statement forwarder id.
    :rtype: str
    """
    return json['_id']


def parse_batch_parse_statement_forwarder_id_url(json):
    """
    Extract the statement forwarder ids from a batch of statement forwarders.

    :param json: JSON text to parse.
    :type json: list(dict(str, dict(str, str)))
    :return: List of ids from statement forwarders.
    :rtype: list(dict(str, str))
    """
    forwarder_list = []
    for forwarder in json:
        forwarder_list.append({
            'url': forwarder['configuration']['url'],
            'id': forwarder['_id']
        })
    return forwarder_list


def parse_quiz_questions(json):
    """
    Extract the quiz questions from a LearningLocker statement.

    :param json: A LearningLocker statement.
    :type json: dict(str, str)
    :return: A dictionary containing the quiz questions.
    :rtype: dict(int, list(dict(str, str)))
    """
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
    Extract the sync agent forwarder id from the get response of LearningLocker.

    :param json: JSON statement from the get response.
    :type json: dict(str, list(dict(str, str))
    :return: The statement forwarder id from the sync agent.
    :rtype: str
    """
    temp_forwarder_id = 0
    if len(json['edges']) > 0:
        temp_forwarder_id = json['edges'][0]['node']['_id']
    return temp_forwarder_id


def parse_questions_answered(json):
    """
    Parse the statement to extract answered questions.

    :param json: A statement containing answered  questions.
    :type json: dict(str, list)
    :return: The question id of the answered question.
    :rtype: str
    """
    edges = json['edges']
    question_id = {}
    for question in edges:
        temp_link = question['node']['statement']['object']['id']
        question_id[(temp_link.split('id=')[2])] = question['node']['statement']['result']['success']
    return question_id
