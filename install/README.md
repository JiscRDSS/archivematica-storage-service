# Storage Service Configuration

## Table of contents

- [Introduction](#introduction)
- [Environment variables](#environment-variables)
  - [Application-specific environment variables](#application-specific-environment-variables)
  - [Gunicorn-specific environment variables](#gunicorn-specific-environment-variables)
- [Logging configuration](#logging-configuration)

## Introduction

The configuration system in Storage Service is based on the following pattern:

1. **Environment variables** - setting a configuration parameter with an
   environment variable will override all other methods.
1. **Application defaults**  - if the parameter is not set in an environment
   variable or the config file, the application default is used.

Logging behaviour is configured differently, and provides two methods:

1. **`logging.json` file** - if a JSON file is present in the default location,
    the contents of the JSON file will control the components logging behaviour.
1. **Application default** - if no JSON file is present, the default logging
   behaviour is to write to standard streams (standard out and standard error).

## Environment variables

The value of an environment variable is a string of characters. The
configuration system coerces the value to the types supported:

- `string` (e.g. `"foobar"`)
- `int` (e.g. `"60"`)
- `float` (e.g. `"1.20"`)
- `boolean` where truth values can be represented as follows (checked in a
  case-insensitive manner):
  - True (enabled):  `"1"`, `"yes"`, `"true"` or `"on"`
  - False (disabled): `"0"`, `"no"`, `"false"` or `"off"`

Certain environment strings are mandatory, i.e. they don't have defaults and
the application will refuse to start if the user does not provide one.

Please be aware that Archivematica supports different types of distributions
(Ubuntu/CentOS packages, Ansible or Docker images) and they may override some
of these settings or provide values to mandatory fields.

### Application-specific environment variables

- **`DJANGO_SETTINGS_MODULE`**:
    - **Description:** the [settings module](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key) used by Django. There are three modules available: [storage_service.settings.production](../storage_service/storage_service/settings/production.py), [storage_service.settings.local](../storage_service/storage_service/settings/local.py) and [storage_service.settings.test](../storage_service/storage_service/settings/test.py). Unless you are a developer you should only use the former.
    - **Type:** `string`
    - :red_circle: **Mandatory!**

- **`DJANGO_ALLOWED_HOSTS`**:
    - **Description:** comma-separated list of hosts or domain names that this Django site can serve. See the [official docs](https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts).
    - **Type:** `string`
    - :red_circle: **Mandatory!**

- **`SECRET_KEY`**:
    - **Description:** a secret key used for cryptographic signing. See [SECRET_KEY](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key) for more details.
    - **Type:** `string`
    - :red_circle: **Mandatory!**

- **`SS_SHIBBOLETH_AUTHENTICATION`**:
    - **Description:** enables the Shibboleth authentication system. Other settings related to Shibboleth cannot be defined via environment variables at the moment, please edit [storage_service.settings.base](../storage_service/storage_service/settings/base.py) manually.
    - **Type:** `boolean`
    - **Default:** `false`

- **`SS_BAG_VALIDATION_NO_PROCESSES`**:
    - **Description:** number of concurrent processes used by BagIt. If Gunicorn is being used to serve the Storage Service and its worker class is set to `gevent`, then BagIt validation must use 1 process. Otherwise, calls to `validate` will hang because of the incompatibility between gevent and multiprocessing (BagIt) concurrency strategies. See [#708](https://github.com/artefactual/archivematica/issues/708).
    - **Type:** `int`
    - **Default:** `1`

- **`SS_GNUPG_HOME_PATH`**:
    - **Description:** path of the GnuPG home directory. If this environment string is not defined Storage Service will use its internal location directory.
    - **Type:** `string`
    - **Default:** `None`

- **`SS_INSECURE_SKIP_VERIFY`**:
    - **Description:** skip the SSL certificate verification process. This setting should not be used in production environments.
    - **Type:** `boolean`
    - **Default:** `false`

There are a limited number of email settings that can be populated via
environment variables - we are hoping to improve this soon (see
[#813](https://github.com/artefactual/archivematica/pull/813)). We have some
settings hard-coded (see [storage_service.settings.production](../storage_service/storage_service/settings/production.py)).
This is the current list of strings supported:

- **`EMAIL_HOST`**
    - **Description:** https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    - **Type:** `string`
    - **Default:** `smtp.gmail.com`

- **`EMAIL_HOST_PASSWORD`**
    - **Description:** https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
    - **Type:** `string`
    - **Default:** (empty string)

- **`EMAIL_HOST_USER`**
    - **Description:** https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
    - **Type:** `string`
    - **Default:** `your_email@example.com`

- **`EMAIL_PORT`**
    - **Description:** https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    - **Type:** `int`
    - **Default:** `587`

### Gunicorn-specific environment variables

- **`SS_GUNICORN_USER`**:
    - **Description:** OS user for gunicorn worker processes to run as. See [USER](http://docs.gunicorn.org/en/stable/settings.html#user).
    - **Type:** `integer` (user id) or `string` (user name)
    - **Default:** `archivematica`

- **`SS_GUNICORN_GROUP`**:
    - **Description:** OS group for gunicorn worker processes to run as. See [GROUP](http://docs.gunicorn.org/en/styable/settings.html#group).
    - **Type:** `integer` (group id) or `string` (group name)
    - **Default:** `archivematica`

- **`SS_GUNICORN_BIND`**:
    - **Description:** the socket for gunicorn to bind to. See [BIND](http://docs.gunicorn.org/en/stable/settings.html#bind).
    - **Type:** `string` (host name or ip with port number)
    - **Default:** `127.0.0.1:8001`

- **`SS_GUNICORN_WORKERS`**:
    - **Description:** number of gunicorn worker processes to run. See [WORKERS](http://docs.gunicorn.org/en/stable/settings.html#workers). If `SS_GUNICORN_WORKER_CLASS` is set to `gevent`, then `SS_BAG_VALIDATION_NO_PROCESSES` **must** be set to `1`. Otherwise reingest will fail at bagit validate. See [#708](https://github.com/artefactual/archivematica/issues/708).
    - **Type:** `integer`
    - **Default:** `1`

- **`SS_GUNICORN_WORKER_CLASS`**:
    - **Description:** the type of worker processes to run. See [WORKER-CLASS](http://docs.gunicorn.org/en/stable/settings.html#worker-class).
    - **Type:** `string`
    - **Default:** `gevent`

- **`SS_GUNICORN_TIMEOUT`**:
    - **Description:** worker process timeout. See [TIMEOUT](http://docs.gunicorn.org/en/stable/settings.html#timeout).
    - **Type:** `integer` (seconds)
    - **Default:** `172800`

- **`SS_GUNICORN_RELOAD`**:
    - **Description:** restart workers when code changes. See [RELOAD](http://docs.gunicorn.org/en/stable/settings.html#reload).
    - **Type:** `boolean`
    - **Default:** `false`

- **`SS_GUNICORN_RELOAD_ENGINE`**:
    - **Description:** method of performing reload. See [RELOAD-ENGINE](http://docs.gunicorn.org/en/stable/settings.html#reload-engine).
    - **Type:** `string`
    - **Default:** `auto`

- **`SS_GUNICORN_CHDIR`**:
    - **Description:** directory to load apps from. See [CHDIR](http://docs.gunicorn.org/en/stable/settings.html#chdir).
    - **Type:** `string`
    - **Default:** `/usr/lib/archivematica/storage-service`

- **`SS_GUNICORN_ACCESSLOG`**:
    - **Description:** location to write access log to. See [ACCESSLOG](http://docs.gunicorn.org/en/stable/settings.html#accesslog).
    - **Type:** `string`
    - **Default:** `/dev/null`

- **`SS_GUNICORN_ERRORLOG`**:
    - **Description:** location to write error log to. See [ERRORLOG](http://docs.gunicorn.org/en/stable/settings.html#errorlog).
    - **Type:** `string`
    - **Default:** `-`

- **`SS_GUNICORN_LOGLEVEL`**:
    - **Description:** the granularity of Error log outputs. See [LOGLEVEL](http://docs.gunicorn.org/en/stable/settings.html#loglevel).
    - **Type:** `string`
    - **Default:** `INFO`

- **`SS_GUNICORN_PROC_NAME`**:
    - **Description:** name for this instance of gunicorn. See [PROC-NAME](http://docs.gunicorn.org/en/stable/settings.html#proc-name).
    - **Type:** `string`
    - **Default:** `archivematica-storage-service`

## Logging configuration

Storage Service 0.10.0 and earlier releases are configured by default to log to
the `/var/log/archivematica/storage-service` directory, such as
`/var/log/archivematica/storage-service/storage_service.log`. Starting with
Storage Service 0.11.0, logging configuration defaults to using stdout and
stderr for all logs. If no changes are made to the new default configuration
logs will be handled by whichever process is managing Archivematica's services.
For example on Ubuntu 16.04 or Centos 7, Archivematica's processes are managed
by systemd. Logs for the Storage Service can be accessed using
`sudo journalctl -u archivematica-storage-service`. On Ubuntu 14.04, upstart is
used instead of systemd, so logs are usually found in `/var/log/upstart`. When
running Archivematica using docker, `docker-compose logs` commands can be used
to access the logs from different containers.

The Storage Service will look in `/etc/archivematica` for a file called
`storageService.logging.json`, and if found, this file will override the default
behaviour described above.

The [`storageService.logging.json`](./storageService.logging.json) file in this
directory provides an example that implements the logging behaviour used in
Storage Service 0.10.0 and earlier.
