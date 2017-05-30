# Documentation: http://docs.gunicorn.org/en/stable/configure.html
# Example: https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py

import os

# http://docs.gunicorn.org/en/stable/settings.html#user
user = os.environ.get('SS_GUNICORN_USER', 'archivematica')

# http://docs.gunicorn.org/en/stable/settings.html#group
group = os.environ.get('SS_GUNICORN_GROUP', 'archivematica')

# http://docs.gunicorn.org/en/stable/settings.html#bind
bind = os.environ.get('SS_GUNICORN_BIND', '127.0.0.1:8001')

# http://docs.gunicorn.org/en/stable/settings.html#workers
workers = os.environ.get('SS_GUNICORN_WORKERS', '4')

# http://docs.gunicorn.org/en/stable/settings.html#worker-class
worker_class = os.environ.get('SS_GUNICORN_WORKER_CLASS', 'gevent')

# http://docs.gunicorn.org/en/stable/settings.html#timeout
timeout = os.environ.get('SS_GUNICORN_TIMEOUT', '172800')

# http://docs.gunicorn.org/en/stable/settings.html#reload
reload = os.environ.get('SS_GUNICORN_RELOAD', 'false')

# http://docs.gunicorn.org/en/stable/settings.html#reload-engine
reload_engine = os.environ.get('SS_GUNICORN_RELOAD_ENGINE', 'auto')

# http://docs.gunicorn.org/en/stable/settings.html#chdir
chdir = os.environ.get('SS_GUNICORN_CHDIR', '/usr/lib/archivematica/storage-service')

# http://docs.gunicorn.org/en/stable/settings.html#raw-env
envs = (
    ("EMAIL_HOST_PASSWORD", ""),
    ("SS_DB_NAME", "/var/archivematica/storage-service/storage.db"),
    ("SS_DB_PASSWORD", ""),
    ("SS_DB_USER", ""),
    ("SS_DB_HOST", ""),
    ("DJANGO_SETTINGS_MODULE", "storage_service.settings.production"),
    ("EMAIL_PORT", "25"),
    ("DJANGO_SECRET_KEY", "<replace-with-key>"),
    ("EMAIL_HOST_USER", ""),
    ("EMAIL_HOST", "localhost"),
)
raw_env = []
for e in envs:
    if e[0] in os.environ:
        continue
    raw_env.append('='.join(e))

# http://docs.gunicorn.org/en/stable/settings.html#accesslog
accesslog = os.environ.get('SS_GUNICORN_ACCESSLOG', '/var/log/archivematica/storage-service/gunicorn.access_log')

# http://docs.gunicorn.org/en/stable/settings.html#errorlog
errorlog = os.environ.get('SS_GUNICORN_ERRORLOG', '/var/log/archivematica/storage-service/gunicorn.error_log')

# http://docs.gunicorn.org/en/stable/settings.html#loglevel
loglevel = os.environ.get('SS_GUNICORN_LOGLEVEL', 'info')

# http://docs.gunicorn.org/en/stable/settings.html#proc-name
proc_name = os.environ.get('SS_GUNICORN_PROC_NAME', 'archivematica-storage-service')

# http://docs.gunicorn.org/en/stable/settings.html#pythonpath
pythonpath = os.environ.get('SS_GUNICORN_PYTHONPATH', '')

# http://docs.gunicorn.org/en/stable/settings.html#sendfile
sendfile = os.environ.get('SS_GUNICORN_SENDFILE', 'false')
