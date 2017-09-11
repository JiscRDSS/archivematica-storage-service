"""Production settings and globals."""
from __future__ import absolute_import

from os import environ

from .base import *  # noqa: F401, F403

# ######## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['*']
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
