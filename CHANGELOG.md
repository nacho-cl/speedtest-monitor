# Changelog
# Changelog
Todos los cambios notables de este proyecto se documentarán en este archivo.

## [0.2.0] - 2025-12-06
- Se agregan Dockerfile, docker-compose.yml, .dockerignore y .gitignore para ejecución contenedorizada.
- Se parametriza configuración vía variables de entorno (12-factor) en `speedtest.py` y `speedtestdb.py`.
- Se añaden configuraciones de Ruff/Black/Pytest/Coverage en `pyproject.toml` y archivos de requisitos con pip-tools (`requirements.in`, `requirements-dev.in`).

## [0.2.1] - 2025-12-06
- Se añade InfluxDB 1.8 y Chronograf al `docker-compose.yml` con volúmenes persistentes y credenciales desde `INFLUX_*`.
- README actualizado con descripción del stack Docker y uso de Chronograf.

## [0.2.2] - 2025-12-06
- Se elimina el servicio opcional de Chronograf del `docker-compose.yml` y su volumen asociado.
- README ajustado para reflejar el stack sin Chronograf.

## [0.2.3] - 2025-12-06
- La imagen Docker instala `speedtest-cli` de sistema (apt) además del paquete Python para garantizar el binario en Linux.
- README actualizado para reflejar la inclusión de speedtest-cli nativo en el contenedor.

## [0.2.4] - 2025-12-06
- Se crea una red interna en `docker-compose.yml` para aislar InfluxDB (sin exponer puerto).
- Se agrega servicio opcional de Grafana (puerto configurable, por defecto 3100) para visualizar métricas.
- `.env` y `.env.example` incluyen credenciales y puerto de Grafana; README actualizado.

## [0.3.0] - 2025-12-06
- `speedtest` ahora corre en bucle cada `INTERVAL_SECONDS` (por defecto 300s) para enviar resultados a InfluxDB.
- Grafana se provisiona automáticamente con datasource a InfluxDB y dashboard inicial (`grafana/dashboards/speedtest.json`).
- Compose monta las carpetas de provisioning/dashboards de Grafana y añade variable `INTERVAL_SECONDS` en `.env` y `.env.example`.

## [0.1.0] - 2025-12-06
- Se agregan guías de desarrollo, seguridad y operabilidad en `README.md`.
- Se documentan comandos para formato, lint, pruebas y seguridad (Ruff, Black, Pytest, Gitleaks, Trivy, pip-tools).
- Se establece control de dependencias con `requirements.txt` y lineamientos de versionado semántico.
