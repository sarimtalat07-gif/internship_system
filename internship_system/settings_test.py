"""Settings for running the test-suite without Oracle:
    python manage.py test --settings=internship_system.settings_test
"""
from .settings import *  # noqa

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
