# ── Stage 1: Build Vite frontend ────────────────────────────────────────────
FROM node:20-slim AS frontend

WORKDIR /front
COPY front/package*.json ./
RUN npm ci
COPY front/ ./
RUN npm run build
# Outputs to /front/../back/static/dist via vite.config.js outDir,
# but since we're in a container we need to redirect output.
# Override outDir at build time to a known location.

# ── Stage 2: Django application ──────────────────────────────────────────────
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

RUN pip install "gunicorn==20.0.4"

COPY back/requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

# Copy Django source from back/
COPY --chown=wagtail:wagtail back/ .

# Copy Vite build output into static/dist/
COPY --chown=wagtail:wagtail --from=frontend ../back/static/dist/ ./static/dist/

USER wagtail

RUN mkdir -p /app/media /app/static

RUN python manage.py collectstatic --noinput --clear

CMD set -xe; python manage.py migrate --noinput; gunicorn back.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - --log-level debug
