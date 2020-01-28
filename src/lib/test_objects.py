# This program has been developed by students from the bachelor Computer Science at Utrecht University within the
# Software and Game project course
# ©Copyright Utrecht University Department of Information and Computing Sciences.
"""This file contains all mock objects used when testing."""


class MockResponse:
    """Mock response used for testing."""

    def __init__(self, status_code, json_data=None):
        """Initialize variable for a response."""
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        """
        Get the response json.

        :return: Response json data.
        """
        return self.json_data


def raise_(exception):
    """
    Raise an exception.

    Usefull for testing, since lambda functions can not contain statements.
    """
    raise exception


STATEMENTS = [
    {
        'id': 'dummy-statement-id-1',
        'verb': {
            'id': 'http://dummy-verb'
        },
        'object': {
            'definition': {
                'type': 'http://dummy-type.ms'
            }
        }
    },
    {
        'id': 'dummy-statement-id-2',
        'verb': {
            'id': 'http://id.tincanapi.com/verb/viewed'
        },
        'object': {
            'definition': {
                'type': 'http://activitystrea.ms/schema/1.0/page'
            }
        }
    },
    {
        'id': 'dummy-statement-id-3',
        'verb': {
            'id': 'http://id.tincanapi.com/verb/viewed'
        },
        'object': {
            'definition': {
                'type': 'http://id.tincanapi.com/activitytype/lms/course'
            }
        }
    }]
