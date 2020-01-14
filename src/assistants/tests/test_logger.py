# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

from unittest import TestCase
from unittest.mock import patch

from assistants import logger


class TestLogger(TestCase):

    def test_log_response_all(self):
        url = 'dummy_url'
        status_code = 'dummy_status_code'
        params = 'dummy_p: dummy_p_value'
        headers = 'dummy_h: dummy_h_value'
        json = 'dummy_j: dummy_j_value'
        text = 'dummy_text'

        with patch('logging.warning') as w:
            logger.log_response(url, status_code, params=params, headers=headers, json=json, text=text)

        w.assert_called_with('API error! Status code = dummy_status_code. Data = dummy_url dummy_p: dummy_p_value '
                             'dummy_h: dummy_h_value dummy_j: dummy_j_value dummy_text')

    def test_log_response_none(self):
        url = 'dummy_url'
        status_code = 'dummy_status_code'

        with patch('logging.warning') as w:
            logger.log_response(url, status_code)

        w.assert_called_with('API error! Status code = dummy_status_code. Data = dummy_url')
