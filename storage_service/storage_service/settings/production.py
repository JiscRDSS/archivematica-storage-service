# flake8: noqa

"""Production settings and globals."""

from __future__ import absolute_import

import dj_database_url

from .base import *


# ######## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {}
if 'SS_DB_URL' in environ:
    DATABASES['default'] = dj_database_url.config(
        env='SS_DB_URL', conn_max_age=600)
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': get_env_variable('SS_DB_NAME'),
        'USER': get_env_variable('SS_DB_USER'),  # Not used with sqlite3.
        'PASSWORD': get_env_variable('SS_DB_PASSWORD'),  # Not used with sqlite3.
        'HOST': get_env_variable('SS_DB_HOST'),  # Set to empty string forr localhost. Not used with sqlite3.
        'PORT': '',  # Set to empty string for default. Not used with sqlite3.
    }
# ######## END DATABASE CONFIGURATION


# ######## HOST CONFIGURATION
# See:
# https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = get_env_variable('DJANGO_ALLOWED_HOSTS').split(',')
# ######## END HOST CONFIGURATION


# ######## EMAIL CONFIGURATION

#
# Which Email backend to use? SMTP is default, others including Amazon SES are
# also supported.  See https://docs.djangoproject.com/en/dev/ref/settings/ and
# https://docs.djangoproject.com/en/dev/topics/email/
#

EMAIL_BACKEND = environ.get('EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend')

# Amazon SES Backend
# See https://github.com/azavea/django-amazon-ses
DJANGO_AMAZON_SES_REGION = environ.get('DJANGO_AMAZON_SES_REGION', 'us-east-1')


# SMTP Backend
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')
EMAIL_PORT = to_int(environ.get('EMAIL_PORT', '587'))
EMAIL_SSL_CERTFILE = environ.get('EMAIL_SSL_CERTFILE')
EMAIL_SSL_KEYFILE = environ.get('EMAIL_SSL_KEYFILE')
EMAIL_USE_SSL = is_true(environ.get('EMAIL_USE_SSL', 'False'))
EMAIL_USE_TLS = is_true(environ.get('EMAIL_USE_TLS', 'True'))

# General
DEFAULT_FROM_EMAIL = environ.get('DEFAULT_FROM_EMAIL', 'webmaster@example.com')
EMAIL_SUBJECT_PREFIX = environ.get('EMAIL_SUBJECT_PREFIX', '[Archivematica Storage Service] ')
EMAIL_TIMEOUT = to_int(environ.get('EMAIL_TIMEOUT'))
SERVER_EMAIL = environ.get('SERVER_EMAIL', EMAIL_HOST_USER)
# ######## END EMAIL CONFIGURATION


# ######## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
# ######## END CACHE CONFIGURATION


# ######## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')
# ######## END SECRET CONFIGURATION
