# Instrucciones de agentes OPDev

<!-- OPDEV-COMMON-AGENT-RULES -->
# Reglas corporativas OPDev para agentes

Estas reglas son obligatorias en todos los repositorios de software e infraestructura OPDev, sin excepción. Complementan las instrucciones locales; si hay contradicción, prevalece esta política, salvo que la regla local sea más estricta.

## Seguridad y cambios

- No incluir secretos, tokens, credenciales, datos de clientes ni `.env` reales en el repositorio o en salidas compartidas.
- No operar sobre producción, clientes o servicios externos sin autorización explícita; nunca debilitar controles de seguridad.
- Preservar cambios preexistentes, comprender el contexto antes de editar, revisar el diff y validar con los controles pertinentes. No declarar completo lo que no se verificó.

## Commits y títulos de PR

- Usar Conventional Commits: `<tipo>(<scope>): <asunto>`. Tipos permitidos: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`, `security`, `brand`, `data`.
- El asunto y título del PR deben ser imperativos, sin punto final y de máximo **90 caracteres**.
- Nunca usar `--no-verify`. Si un hook rechaza el mensaje, leer el error completo y corregir el mensaje; no saltarse el hook.
- Antes de atribuir una falla del linter al asunto, inspeccionar el dato crudo con `git log -1 --format=%s <sha>`.

## Documentos entregables OPDev

- Los documentos oficiales entregables siguen el estándar corporativo: cabecera con favicon y metadata vertical; control de versiones inmediatamente después; cuerpo; footer corporativo completo al final.
- Todo cambio de contenido sube la versión y añade una fila de control con autor. La versión mayor corresponde a reescrituras o cambios de regla; la menor a correcciones o datos. El copyright conserva el año de creación y agrega los años posteriores como rango.
- Aplican a informes, manuales, runbooks, reportes, estándares, ADR, documentos de diseño/release y propuestas; no aplican a AGENTS/CLAUDE/Copilot instructions, CHANGELOG, configuración, contextos ni README de código.
- Estándar canónico: `OPDev/docs/standards/document-format.md` en `devops-managements`.

## Jira y tiempo OPDev

- Para Jira OPDev (`opdev.atlassian.net`), usar REST API con el token configurado para OPDev; nunca usar el MCP Atlassian de CopecFlux.
- Para Jira CopecFlux (`fluxsolar.atlassian.net`), usar el MCP Atlassian con OAuth; no pedir crear ni rotar API tokens.
- Todo ticket OPDev debe llevar estimación original al crearse y worklog antes de cerrarse. Nunca cerrar un ticket sin registrar el tiempo trabajado.
- Registrar el trabajo real en tareas granulares; en tickets paraguas registrar solo el overhead de integración para evitar doble conteo.
- Resolver las transiciones de Jira consultando el estado y las transiciones disponibles; no hardcodear IDs. Al publicar comentarios, usar ASCII simple y evitar `·` y `—`.
<!-- /OPDEV-COMMON-AGENT-RULES -->
