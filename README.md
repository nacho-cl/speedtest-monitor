# Speedtest Monitor
Scripts to collect internet speed metrics using `speedtest-cli`, store them locally in CSV, or push them to InfluxDB for dashboards.

## Instalación y entorno
- Requisitos: Python 3.13+, PowerShell/Bash, acceso a internet para dependencias.
- Crear venv: `python -m venv .venv` y activarlo (`.\.venv\Scripts\activate` en Windows, `source .venv/bin/activate` en Linux/macOS).
- Instalar dependencias de runtime: `pip install -r requirements.txt`.
- Gestión robusta de deps con `pip-tools`: `pip install pip-tools` y para actualizar `pip-compile --generate-hashes`; luego `pip-sync`.

## Uso rápido
- CSV local: `python speedtest.py` (genera/append en `/home/pi/speedtest/speedtest.csv`, ajusta ruta si usas otro OS).
- Enviar a InfluxDB: configura las variables de entorno `INFLUX_HOST`, `INFLUX_PORT`, `INFLUX_USER`, `INFLUX_PASSWORD`, `INFLUX_DB` (o ajusta en el script) y ejecuta `python speedtestdb.py`.
- Ejecución periódica: programa con `cron`/Task Scheduler según tu plataforma.
- Con Docker: `docker compose build` y `docker compose up -d` (usa variables de entorno o un `.env` para InfluxDB y `CSV_PATH`). Imagen por defecto ejecuta `speedtestdb.py`; puedes sobrescribir `command` a `python speedtest.py` para CSV.
- Stack en Docker Compose:
  - `influxdb` (v1.8) con DB y credenciales de `INFLUX_*`, solo accesible dentro de la red interna del compose.
  - `speedtest` (este proyecto) que envía datos a InfluxDB.
  - `grafana` (opcional) expuesto en el puerto `GRAFANA_PORT` (por defecto 3100) para visualizar métricas; conecta a InfluxDB por la red interna.
- La imagen instala `speedtest-cli` nativo (Debian/apt) y el paquete Python `speedtest-cli` para asegurar el binario en Linux.
- El contenedor de `speedtest` ejecuta `speedtest-cli` cada `INTERVAL_SECONDS` (default 300s) y guarda resultados en InfluxDB.
- Grafana se provisiona con datasource a InfluxDB y dashboard básico en `/var/lib/grafana/dashboards/speedtest.json` (volúmenes montados desde `./grafana/...`).

## Estilo, calidad y pruebas
- Formato y lint: `ruff check .` y `black .` (aplica primero `black`, luego `ruff --fix` si quieres autofix).
- Pruebas unitarias: `pytest` y cobertura con `pytest --cov`. Agrega tests para cualquier nueva lógica.
- Versionado: Semantic Versioning (MAJOR.MINOR.PATCH) para cambios de API/CLI/scripts.

## Seguridad y cumplimiento
- OWASP Top 10 e ISO 27001:2022: sin secretos en repositorio, usa variables de entorno/secret manager; valida entradas y maneja errores sin exponer datos sensibles; aplica principios de mínimo privilegio al conectar con InfluxDB.
- Gitleaks: `gitleaks detect` antes de hacer commit para asegurar que no haya credenciales.
- Trivy: `trivy fs .` para escanear vulnerabilidades en dependencias y sistema de archivos.

## Arquitectura y principios
- Enfoque hexagonal: separar lógica de dominio (medición) de puertos/adaptadores (CLI, CSV, InfluxDB). Refactoriza nuevas funcionalidades siguiendo esta separación.
- 12 Factors: configuración por entorno, dependencias explícitas, logs stdout/archivos estructurados, procesos sin estado.
- CUPID: preferir código centrado en claridad, con interfaces pequeñas, acoplado por contrato y con pruebas que describan el comportamiento.

## Operabilidad
- Observabilidad: exporta métricas a InfluxDB y registra errores con contexto mínimo.
- Resiliencia: añade timeouts/reintentos a integraciones externas (p.ej. cliente de InfluxDB) y maneja fallos de red sin perder el proceso.

## Comandos útiles
- `pip-compile --generate-hashes` para fijar versiones.
- `pip-sync` para alinear el entorno con los requisitos.
- `ruff check .` y `black .` para calidad de código.
- `pytest --cov` para ejecutar pruebas con cobertura.
- `gitleaks detect` y `trivy fs .` para seguridad.

## Próximos pasos sugeridos
- Refactorizar los scripts hacia adaptadores para CSV e InfluxDB con puertos claros.
- Añadir tests de unidad/integración simulando respuestas de `speedtest-cli`.
- Agregar manejo de configuración por variables de entorno en ambos scripts y logging estructurado.
