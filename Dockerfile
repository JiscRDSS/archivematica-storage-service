FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
ENV DJANGO_SETTINGS_MODULE storage_service.settings.production
ENV PYTHONUNBUFFERED 1
ENV GUNICORN_CMD_ARGS \
	--user archivematica \
	--group archivematica \
	--bind 0.0.0.0:8000 \
	--workers 4 \
	--timeout 172800 \
	--chdir /src/storage_service \
	--access-logfile - \
	--error-logfile - \
	--log-level info \
	--reload \
	--name archivematica-storage-service

# OS dependencies
RUN set -ex \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends \
		gettext \
		rsync \
		unar \
	&& rm -rf /var/lib/apt/lists/*

ADD requirements/ /src/requirements/
RUN pip install -r /src/requirements/production.txt -r /src/requirements/test.txt
ADD ./ /src/

RUN set -ex \
	&& groupadd -r archivematica \
	&& useradd -r -g archivematica archivematica

RUN set -ex \
	&& internalDirs=' \
		/db \
		/src/storage_service/assets \
		/var/archivematica/storage_service \
	' \
	&& mkdir -p $internalDirs \
	&& chown -R archivematica:archivematica $internalDirs

USER archivematica

RUN env \
	DJANGO_SETTINGS_MODULE=storage_service.settings.local \
	DJANGO_SECRET_KEY=12345 \
	SS_DB_HOST=foobar \
	SS_DB_USER=foobar \
	SS_DB_PASSWORD=foobar \
	SS_DB_NAME=foobar \
		/src/storage_service/manage.py collectstatic --noinput --clear

EXPOSE 8000
ENTRYPOINT /usr/local/bin/gunicorn storage_service.wsgi:application
