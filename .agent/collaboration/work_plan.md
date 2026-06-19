# work_plan.md -- WOT-2026-011a

## Metadata

- **ID:** WOT-2026-011a
- **Contract ID:** T-011A-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Hacer que `--session-close` falle cerrado en el mismo cierre que deja un
`archive_rename_uncommitted`, con remediacion auditable y sin auto-commit del
archivador. El ticket debe mover la deteccion desde el ticket siguiente al
punto real de mutacion del closeout.

## Non-goals

- No introducir auto-commit silencioso en `archive_collaboration_artifacts.py`.
- No redisenar la politica general de archivado ni el bus.
- No "resolver" el problema solo con un `dirty tree` generico sin reason estable.
- No borrar artefactos archivados ni reescribir historia para aparentar limpieza.

## Premisas verificadas antes de Builder

- `scripts/delivery_hygiene_check.py:check_archive_rename_complete()` ya
  detecta `archive_rename_uncommitted` con origen/destino y remediacion exacta.
- `scripts/pre_handoff_guard.py` ya reutiliza esa barrera, pero demasiado tarde:
  la contaminacion aparece en el ticket siguiente.
- `scripts/closeout_steps/archival.py:step_archive_collaboration()` hoy devuelve
  `PASS` si `archive_collaboration_artifacts.py` sale `0`, sin verificar la
  post-condicion del rename.
- `WOT-2026-011d` confirmo otra vez el patron en produccion: el cierre previo
  dejo rename pendiente y la falsa salud solo se corrigio con reconcile manual
  en `repo_destino`.

## Decision Arquitectonica

La solucion v1 es fail-closed en closeout, no auto-commit. El ticket debe
reutilizar la barrera canonica ya existente para detectar
`archive_rename_uncommitted` inmediatamente despues del paso de archivado y
convertir ese hallazgo en `FAIL` bloqueante con remediacion self-service. El
contrato prohibe desplazar otra vez la deteccion al siguiente ticket o
introducir una segunda fuente de verdad del diagnostico.

## Files Likely Touched

### repo_motor

- `scripts/closeout_steps/archival.py`
- `scripts/session_closeout.py`
- `scripts/delivery_hygiene_check.py`
- `tests/test_session_closeout.py`
- `tests/unit/test_delivery_hygiene_check.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/archive_collaboration_artifacts.py`
- `tests/test_pre_handoff_guard.py`
- `tests/unit/test_archive_collaboration_artifacts.py`
- `.agent/runtime/memory/observations.jsonl`
- `CHANGELOG.md`

## Forbidden Surfaces

- Auto-commit dentro de `archive_collaboration_artifacts.py`.
- Borrado destructivo de artefactos archivados.
- Mutaciones manuales del bus/runtime para aparentar cierre limpio.
- Redisenar la politica de closeout fuera del hueco declarado.

## Criterios binarios

- `--session-close` o la ruta real de `step_archive_collaboration()` devuelve
  `FAIL` bloqueante si el archivado deja `archive_rename_uncommitted`.
- El diagnostico conserva la razon estable y nombra origen, destino y comando
  exacto de reconcile.
- El ticket no introduce auto-commit del archivador ni borrado destructivo.
- Existe al menos una prueba de regresion que falla sin el fix y pasa con el
  fix reproduciendo la mutacion real del closeout.
- El caso limpio sigue cerrando en `PASS`.
- `uv run ruff check`, tests focales,
  `python scripts/run_pytest_safe.py --project-root <repo_destino>` y
  `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  quedan verdes.

## STOP conditions

- Parar si la unica forma de cerrar el gap es auto-commit silencioso.
- Parar si la deteccion solo puede expresarse como `dirty tree` generico y no
  como `archive_rename_uncommitted`.
- Parar si el test no puede reproducir la mutacion real del closeout sin mocks
  vacios.

## CONTRACT_GAP

Emitir `CG-WOT-2026-011a.md` y parar si la unica solucion segura exige
auto-commit del archivador, cambiar el contrato del archivado mas alla del
closeout declarado o tocar politica de bus/controller fuera del scope.
