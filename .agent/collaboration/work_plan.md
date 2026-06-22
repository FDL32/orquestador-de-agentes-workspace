# work_plan.md -- WOT-2026-013h
## Metadata
- **ID:** WOT-2026-013h
- **Contract ID:** T-013H-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Eliminar la herencia recurrente de `archive_rename_uncommitted` en la ruta canonica de archivado/cierre, de forma que el siguiente ticket no arranque con renames pendientes del ticket anterior y sin introducir auto-commit opaco de artefactos historicos.
## Non-goals
- No auto-commitear `STRATEGY_` / `AUDIT_` archivados desde el archivador.
- No relajar `archive_rename_uncommitted` ni convertir el closeout en pass-open.
- No tocar `scripts/run_pytest_safe.py`, CI/workflows, xdist ni producto ajeno al closeout.
- No reabrir `013g`; el hallazgo de coste ya esta cerrado y solo actua como evidencia disparadora.
## Premisas verificadas antes de Builder
- `011a` y `011h` ya endurecieron barreras fail-closed, pero la deuda estructural del archivado persiste.
- `013e`, `013f` y `013g` dejaron evidencia de reconcile manual repetido por `archive_rename_uncommitted`.
- El detector canonico del limbo vive en `scripts/delivery_hygiene_check.py`; no hace falta un segundo guard.
- El problema correcto pertenece a `archive_collaboration_artifacts.py` y/o a su closeout caller, no a xdist ni al runner.
## Decision Arquitectonica
`013h` es un ticket `code` de higiene de closeout. El fix debe atacar la ruta real de archivado/cierre con repo git real y mantener una sola fuente de verdad para el limbo (`archive_rename_uncommitted`). `reconcile_ticket.py` sigue siendo recuperacion, no cierre normal.
## Files Likely Touched
### repo_motor
- scripts/archive_collaboration_artifacts.py
- scripts/closeout_steps/archival.py
- scripts/session_closeout.py
- tests/test_archive_collaboration_artifacts.py
- tests/test_session_closeout.py
- tests/test_agent_controller.py
- tests/test_pre_handoff_guard.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- scripts/delivery_hygiene_check.py
- scripts/reconcile_ticket.py
- tests/test_mark_ready_motor_scope.py
- docs/test_performance/test_upgrade_cost_WOT-2026-013g.md
- .agent/runtime/memory/UPSTREAM_LEARNINGS.md
## Forbidden Surfaces
- auto-commit del archivador
- relajacion o renombre del detector `archive_rename_uncommitted`
- scripts/run_pytest_safe.py
- CI/workflows
- tickets cerrados `011e`, `010m`, `011i`, `013d`, `013g`
- privada/
- .env
- eventos del bus escritos manualmente
## Criterios binarios
- La ruta canonica de archivado/cierre deja de heredar `archive_rename_uncommitted` al ticket siguiente, o falla cerrado en el mismo ciclo antes de dejar el limbo persistente.
- Existe al menos una barrera con repo git real que falla sin el fix y pasa con el fix sobre el patron repetido de delete+untracked del archivado.
- `python -m pytest tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py -q` termina verde.
- `ruff check scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py` termina verde.
- `uv run ruff format --check scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py` termina verde.
- `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- No se introduce auto-commit opaco ni se degrada la trazabilidad del historico archivado.
## STOP conditions
- Parar si la unica solucion segura exige auto-commitear historicos.
- Parar si la reproduccion real deja de concentrarse en archivado/cierre y pide ampliar scope a runner, CI o producto.
- Parar si la unica via verde rompe la trazabilidad de `STRATEGY_` / `AUDIT_` archivados.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013h.md` si la unica salida segura exige auto-commit, rediseno mayor del lifecycle de cierre o superficies fuera del archivado/cierre declaradas.
