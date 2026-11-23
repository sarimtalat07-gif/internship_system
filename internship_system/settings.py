"""
Django settings for Student Internship & Career Management System.

IMPORTANT: scroll to DATABASES and put your Oracle XE password in PASSWORD.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Secrets come from environment variables (never commit real passwords).
# The fallback key below is for local development ONLY.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 'django-insecure-dev-only-key-change-me')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',  # our app (all models, views, pages live here)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'internship_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # our HTML files live here
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'internship_system.wsgi.application'

# ---------------------------------------------------------------
# ORACLE DATABASE - configured through environment variables
#   ORACLE_USER      (required)
#   ORACLE_PASSWORD  (required)
#   ORACLE_DSN       (default 127.0.0.1:1521/XE)
#   ORACLE_THICK=1   (needed for older Oracle versions, e.g. XE 11g; requires
#                     Oracle Instant Client. Better: use Oracle XE 21c.)
# Windows cmd example:  set ORACLE_USER=Sarim  &  set ORACLE_PASSWORD=...
# ---------------------------------------------------------------
_db_options = {}
if os.environ.get('ORACLE_THICK') == '1':
    _db_options['use_thick_mode'] = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': os.environ.get('ORACLE_DSN', '127.0.0.1:1521/XE'),
        'USER': os.environ.get('ORACLE_USER', ''),
        'PASSWORD': os.environ.get('ORACLE_PASSWORD', ''),
        'OPTIONS': _db_options,
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_TZ = False  # keep simple for a first project (no timezone math)

STATIC_URL = 'static/'

# where uploaded resume files are stored on disk
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Bootstrap uses "danger" where Django uses "error"
from django.contrib.messages import constants as message_constants  # noqa: E402
MESSAGE_TAGS = {message_constants.ERROR: 'danger'}
