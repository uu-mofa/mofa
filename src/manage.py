# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software and Game project course

# !/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    if 'test' in sys.argv:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mofa.test_settings')
        os.environ['TESTING'] = '1'
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mofa.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
