"""
Django settings for Student Internship & Career Management System.

IMPORTANT: scroll to DATABASES and put your Oracle XE password in PASSWORD.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret in real life!
SECRET_KEY = 'django-insecure-student-project-demo-key-change-me'

DEBUG = True  # True = shows helpful error pages while developing

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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'internship_system.wsgi.application'

# ---------------------------------------------------------------
# ORACLE DATABASE  <-- EDIT HERE
# ---------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',      # tells Django to talk to Oracle
        'NAME': '127.0.0.1:1521/XE',                # XE = the free Oracle edition's service name
        'USER': 'Sarim',                           # system = the admin user created during install
        'PASSWORD': '123',                      # <--- PUT YOUR ORACLE XE PASSWORD HERE
        'OPTIONS': {},
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
