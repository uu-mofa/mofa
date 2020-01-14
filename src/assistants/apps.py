# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

"""TODO."""
from django.apps import AppConfig
from django.conf import settings
import os
import requests


class AssistantsConfig(AppConfig):
    """Perform sync_agent presence check on starting the app."""

    name = 'assistants'

    def ready(self):
        """Perform sync agent checks, updates and creations when the server is started."""
        if os.environ.get('RUN_MAIN'):
            from assistants import sync_agent
            try:
                sync_agent.build_sync_agent()
            except requests.ConnectionError:
                print(f'Connection to Learning Locker was refused! Is it running on {settings.LL_URL} and reachable?')
                quit()
