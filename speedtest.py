import os
import re
import subprocess
import time
from pathlib import Path


def run_speedtest() -> tuple[str, str, str]:
    response = subprocess.check_output(
        ["speedtest-cli", "--simple"], text=True, stderr=subprocess.STDOUT, timeout=120
    )

    ping = re.findall(r"Ping:\s(.*?)\s", response, re.MULTILINE)
    download = re.findall(r"Download:\s(.*?)\s", response, re.MULTILINE)
    upload = re.findall(r"Upload:\s(.*?)\s", response, re.MULTILINE)
    if not (ping and download and upload):
        raise RuntimeError(f"No se pudieron parsear resultados: {response}")

    return (
        ping[0].replace(",", "."),
        download[0].replace(",", "."),
        upload[0].replace(",", "."),
    )


def main() -> None:
    ping, download, upload = run_speedtest()
    csv_path = Path(os.getenv("CSV_PATH", "/home/pi/speedtest/speedtest.csv"))
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    is_new = not csv_path.exists() or csv_path.stat().st_size == 0
    with csv_path.open("a+", encoding="utf-8") as f:
        if is_new:
            f.write("Date,Time,Ping (ms),Download (Mbit/s),Upload (Mbit/s)\n")
        f.write(
            f"{time.strftime('%m/%d/%y')},{time.strftime('%H:%M')},{ping},{download},{upload}\n"
        )
    print(f"Escrito en {csv_path} ping={ping}ms down={download}Mb/s up={upload}Mb/s")


if __name__ == "__main__":
    main()
