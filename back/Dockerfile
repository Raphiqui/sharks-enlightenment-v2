FROM python:3.12-slim-bookworm

RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

# Copy Django source from back/
COPY --chown=wagtail:wagtail back/ .

USER wagtail

CMD set -xe; python manage.py migrate --noinput; gunicorn back.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
