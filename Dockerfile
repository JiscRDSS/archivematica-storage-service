FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
ENV DJANGO_SETTINGS_MODULE storage_service.settings.production
ENV PYTHONUNBUFFERED 1
ENV GUNICORN_CMD_ARGS \
	--user archivematica \
	--group archivematica \
	--bind 0.0.0.0:8000 \
	--workers 4 \
	--worker-class gevent \
	--timeout 172800 \
	--chdir /src/storage_service \
	--access-logfile - \
	--error-logfile - \
	--log-level info \
	--reload \
        # We can't combine gevent + inotify, see https://github.com/benoitc/gunicorn/issues/1494 \
	--reload-engine poll \
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
	&& groupadd --gid 333 --system archivematica \
	&& useradd --uid 333 --gid 333 --system archivematica

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
	DJANGO_ALLOWED_HOSTS=127.0.0.1 \
	SS_DB_URL=mysql://ne:ver@min/d \
		/src/storage_service/manage.py collectstatic --noinput --clear

EXPOSE 8000
ENTRYPOINT /usr/local/bin/gunicorn storage_service.wsgi:application
