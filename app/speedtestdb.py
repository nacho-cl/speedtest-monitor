import os
import re
import subprocess  # nosec B404
from typing import Dict, List

from influxdb import InfluxDBClient


def run_speedtest() -> Dict[str, float]:
    """Ejecuta speedtest y parsea resultados, devolviendo ping/download/upload."""
    response = subprocess.check_output(  # nosec
        ["speedtest-cli", "--simple"],
        text=True,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    ping = re.findall(r"Ping:\s(.*?)\s", response, re.MULTILINE)
    download = re.findall(r"Download:\s(.*?)\s", response, re.MULTILINE)
    upload = re.findall(r"Upload:\s(.*?)\s", response, re.MULTILINE)

    if not (ping and download and upload):
        raise RuntimeError(f"No se pudieron parsear resultados: {response}")

    return {
        "ping": float(ping[0].replace(",", ".")),
        "download": float(download[0].replace(",", ".")),
        "upload": float(upload[0].replace(",", ".")),
    }


def write_to_influx(speed: Dict[str, float]) -> None:
    host = os.getenv("INFLUX_HOST", "localhost")
    port = int(os.getenv("INFLUX_PORT", "8086"))
    username = os.getenv("INFLUX_USER", "speedmonitor")
    password = os.getenv("INFLUX_PASSWORD", "speedmonitor")
    database = os.getenv("INFLUX_DB", "internetspeed")
    measurement = os.getenv("INFLUX_MEASUREMENT", "internet_speed")
    host_tag = os.getenv("HOST_TAG", "speedtest-monitor")

    speed_data: List[dict] = [
        {
            "measurement": measurement,
            "tags": {"host": host_tag},
            "fields": speed,
        }
    ]

    client = InfluxDBClient(
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        timeout=int(os.getenv("INFLUX_TIMEOUT", "10")),
    )
    client.create_database(database)
    client.write_points(speed_data)


def main() -> None:
    speed = run_speedtest()
    write_to_influx(speed)
    print(f"OK ping={speed['ping']}ms down={speed['download']}Mb/s up={speed['upload']}Mb/s")


if __name__ == "__main__":
    main()
