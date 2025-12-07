FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends speedtest-cli \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY speedtest.py speedtestdb.py ./

# Variables de entorno configurables (12-factor)
ENV INFLUX_HOST=localhost \
    INFLUX_PORT=8086 \
    INFLUX_USER=speedmonitor \
    INFLUX_PASSWORD=speedmonitor \
    INFLUX_DB=internetspeed \
    INFLUX_MEASUREMENT=internet_speed \
    HOST_TAG=speedtest-monitor \
    CSV_PATH=/data/speedtest.csv

# Por defecto envía métricas a InfluxDB
CMD ["python", "speedtestdb.py"]
