#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get('LOGNAME') == 'mpetyx':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Anlzer_Project.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
