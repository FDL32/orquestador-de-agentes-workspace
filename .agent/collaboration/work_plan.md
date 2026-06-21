# work_plan.md -- WOT-2026-011h
## Metadata
- **ID:** WOT-2026-011h
- **Contract ID:** T-011H-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Hacer que `--mark-ready` falle cerrado cuando su auto-archivado deje `archive_rename_uncommitted`, reutilizando el mismo diagnostico estable cerrado por `011a` para `--session-close`, sin introducir auto-commit del archivador.
## Non-goals
- No reabrir `--session-close` ni el closeout de `011a`.
- No introducir auto-commit dentro del archivador.
- No borrar destructivamente artefactos archivados.
- No tocar workflows/CI, `scripts/run_pytest_safe.py`, ni `scripts/pre_handoff_guard.py` fuera de la barrera estrictamente necesaria.
## Premisas verificadas antes de Builder
- `011a` COMPLETED (commits 4532d1a fail-closed closeout, 28bc7f4 non-zero/timeout) y `011d` COMPLETED (28bbe85), verificado via git log.
- `_auto_archive_closed_artifacts()` mueve PLAN_/AUDIT_/STRATEGY_ con `shutil.move` sin commit; `_handle_mark_ready()` lo invoca DESPUES del pre-handoff guard y ANTES de `_sync_mark_ready_targets` (READY_FOR_REVIEW).
- El detector estable `check_archive_rename_complete` (reason `archive_rename_uncommitted`) ya existe en `scripts/delivery_hygiene_check.py` y lo reusa `pre_handoff_guard`.
- El pre-handoff guard corre ANTES del archivado de mark-ready, por lo que no atrapa el limbo que mark-ready crea.
- `--validate --json` errors=0 warnings=0 antes del arranque.
## Decision Arquitectonica
`011h` cierra el mismo hueco que `011a` resolvio para closeout, pero en el camino de handoff (`--mark-ready`). Reutiliza el detector canonico, no reabre el contrato del archivador ni del closeout, y mantiene el invariante de no-auto-commit.
## Files Likely Touched
### repo_motor
- .agent/agent_controller.py
- tests/test_agent_controller.py
- tests/test_mark_ready_motor_scope.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- scripts/delivery_hygiene_check.py
- scripts/pre_handoff_guard.py
- tests/test_pre_handoff_guard.py
- tests/unit/test_scope_gate.py
- scripts/closeout_steps/archival.py
- scripts/archive_collaboration_artifacts.py
- .agent/runtime/events/events.jsonl
- .agent/collaboration/backlog.md
## Forbidden Surfaces
- reabrir `--session-close`
- auto-commit dentro del archivador
- borrado destructivo de artefactos archivados
- tocar workflows/CI, `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` fuera de la barrera estrictamente necesaria, `privada/`, `.env` o eventos del bus manualmente
## Criterios binarios
- `--mark-ready` bloquea con razon estable `archive_rename_uncommitted` si su auto-archivado deja limbo `D old + ?? new`.
- El diagnostico conserva origen, destino y comando de reconcile exacto, alineado con `011a`.
- El caso limpio de `--mark-ready` sigue alcanzando `READY_FOR_REVIEW` sin falso positivo.
- Existe al menos una barrera FAIL-sin/PASS-con sobre la ruta real de mark-ready, no solo sobre helper aislado.
- El ticket no introduce auto-commit del archivador ni relaja el handoff canonico.
- `python -m pytest tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py -q`, `ruff check`, `uv run ruff format --check`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica forma de cerrar el hueco es auto-commitear el archivador.
- Parar si la deteccion solo puede expresarse como `dirty tree` generico y no como `archive_rename_uncommitted`.
- Parar si reproducir la mutacion real exige tocar `--session-close` en vez de la ruta de handoff.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011h.md` si la unica solucion segura exige auto-commit del archivador, cambiar el contrato del archivado fuera de mark-ready, o tocar politicas de bus/controller fuera del flujo declarado.
