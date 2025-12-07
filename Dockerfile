FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ARG APP_VERSION=0.3.0
ARG APP_USER=appuser
ARG APP_UID=1000
ARG APP_GID=1000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends speedtest-cli ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid "${APP_GID}" "${APP_USER}" \
    && useradd --uid "${APP_UID}" --gid "${APP_GID}" --create-home "${APP_USER}"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
RUN mkdir -p /data && chown -R "${APP_UID}:${APP_GID}" /app /data

# SemVer de la imagen
LABEL org.opencontainers.image.version="${APP_VERSION}"

USER ${APP_UID}

# Por defecto envía métricas a InfluxDB
CMD ["python", "-m", "app.speedtestdb"]
