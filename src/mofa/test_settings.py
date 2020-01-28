# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""These settings will be used when running tests."""
# noinspection PyUnresolvedReferences
from .settings import *

# Moodle
MOODLE_BASE_URL = 'DUMMY_MOODLE_BASE_URL'
MOODLE_BASE_IP = 'DUMMY_MOODLE_BASE_IP'
MOODLE_WEBSERVICE_URL = 'DUMMY_MOODLE_URL'
MOODLE_TOKEN = "DUMMY_MOODLE_TOKEN"

# Learning Locker
LL_URL = "DUMMY_LL_URL/"
LL_AUTH_KEY = "DUMMY_LL_AUTH_KEY"
ORGANISATION = "DUMMY_ORGANISATION"

DJANGO_URL = "DUMMY_DJANGO_URL"
DJANGO_PORT = "1234"
SYNC_AGENT_URLS = {'course': f'{DJANGO_URL}:{DJANGO_PORT}/assistants/api/course_sync_agent/',
                   'user': f'{DJANGO_URL}:{DJANGO_PORT}/assistants/api/user_sync_agent/',
                   'question': f'{DJANGO_URL}:{DJANGO_PORT}/assistants/api/question_sync_agent/'}
