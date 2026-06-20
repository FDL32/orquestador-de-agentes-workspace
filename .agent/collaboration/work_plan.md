# work_plan.md -- WOT-2026-011b
## Metadata
- **ID:** WOT-2026-011b
- **Contract ID:** T-011B-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Volver determinista la familia de tests de relaunch que ejerce verificacion temporal, reutilizando la costura existente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` para evitar waits dependientes del host, sin cambiar la semantica productiva del relaunch ni su timeout default.
## Non-goals
- No cambiar la semantica productiva de `builder_started_verified`, `builder_launch_unverified` ni `timeout`.
- No tocar `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py`, CI/workflows ni la politica de handoff.
- No convertir el timeout productivo en un parametro exclusivo de test ni abrir la puerta a sleeps wall-clock fragiles.
## Premisas verificadas antes de Builder
- `bus/builder_relaunch.py` ya declara `BUILDER_START_VERIFY_TIMEOUT_SECONDS` y `_BUILDER_START_VERIFY_TIMEOUT_DEFAULT = 20.0`.
- La familia de relaunch en `tests/test_supervisor.py` ya cubre `builder_started_verified`, `timeout` y `builder_launch_unverified`.
- La deuda abierta por `011b` es de determinismo de test, no de funcionalidad de producto ni de topologia.
## Decision Arquitectonica
`011b` debe resolver la robustez de las pruebas alrededor de la costura ya existente, no inventar otra. El seam de timeout vive en `bus/builder_relaunch.py`; el Builder puede endurecer el helper o las pruebas, pero el resultado debe preservar la semantica productiva y dejar evidencia explicita de que la ruta temporizada ya no depende del timeout default del host.
## Files Likely Touched
### repo_motor
- bus/builder_relaunch.py
- tests/test_supervisor.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- bus/supervisor.py
- tests/test_relaunch_evidence_capsule.py
- .agent/runtime/pytest-safe/last-run.json
- .agent/collaboration/backlog.md
## Forbidden Surfaces
- cambiar la semantica productiva del relaunch
- tocar scripts/run_pytest_safe.py, scripts/pre_handoff_guard.py o CI/workflows
- relajar el cierre canonico por `--level all`
- escribir eventos del bus manualmente
## Criterios binarios
- Las pruebas temporizadas de relaunch fijan explicitamente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` o una costura equivalente determinista.
- `_BUILDER_START_VERIFY_TIMEOUT_DEFAULT = 20.0` y el env var canonico se conservan salvo refactor semantico neutro.
- Existe al menos una barrera FAIL-sin/PASS-con que demuestra que la ruta temporizada deja de depender del timeout default del host.
- Las rutas `builder_started_verified` y `builder_launch_unverified` siguen cubiertas sin cambiar su semantica observable.
- `pytest` focal, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica implementacion viable cambia la semantica productiva del relaunch o su default runtime.
- Parar si la costura real del timeout cae fuera de `bus/builder_relaunch.py` / `tests/test_supervisor.py`.
- Parar si para probar la ruta temporizada hace falta depender de sleeps wall-clock o procesos reales no acotables.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011b.md` si la deuda real resulta estar fuera de las superficies declaradas, si el fix exige tocar runner/handoff/CI, o si el determinismo no puede lograrse sin modificar la semantica productiva del relaunch.
