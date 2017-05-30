FROM python:2.7

ENV DEBIAN_FRONTEND noninteractive
ENV DJANGO_SETTINGS_MODULE storage_service.settings.production
ENV PYTHONUNBUFFERED 1
ENV GUNICORN_BIND 0.0.0.0:8000
ENV GUNICORN_CHDIR /src/storage_service
ENV GUNICORN_ACCESSLOG -
ENV GUNICORN_ERRORLOG -
ENV FORWARDED_ALLOW_IPS *

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
ADD ./install/storage-service.gunicorn-config.py /etc/archivematica/storage-service.gunicorn-config.py

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
ENTRYPOINT /usr/local/bin/gunicorn --config=/etc/archivematica/storage-service.gunicorn-config.py storage_service.wsgi:application
