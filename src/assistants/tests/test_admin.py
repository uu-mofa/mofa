# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

from unittest.mock import MagicMock, patch

from django.test import TestCase

from assistants.admin import AssistantAdmin


class TestAssistantAdmin(TestCase):

    def test_has_error_with_object(self):
        m = MagicMock()
        m.forwarder_id = "1"
        with patch('assistants.learning_locker.check_statement_forwarder') as p:
            p.return_value = True
            self.assertEqual(AssistantAdmin.has_error(m), False)

    def test_has_error_with_object_false(self):
        m = MagicMock()
        m.forwarder_id = "1"
        with patch('assistants.learning_locker.check_statement_forwarder') as p:
            p.return_value = False
            self.assertEqual(AssistantAdmin.has_error(m), True)

    def test_has_error_with_none_object(self):
        m = None
        self.assertEqual(AssistantAdmin.has_error(m), False)
