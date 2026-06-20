# work_plan.md -- WOT-2026-011e
## Metadata
- **ID:** WOT-2026-011e
- **Contract ID:** T-011E-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Anadir `pytest-xdist` como opt-in local en `run_pytest_safe.py` para un subset unitario explicito, con medicion auditable y fallback seguro a ejecucion serial cuando el scope no sea apto, sin tocar el default del runner ni la semantica de cierre canonico.
## Non-goals
- No cambiar el default de `python scripts/run_pytest_safe.py` sin flags.
- No paralelizar `--level all`, `--level integration` ni el cierre canonico.
- No tocar CI/workflows ni reabrir `010m`.
- No convertir xdist en politica por defecto; eso pertenece a `011i`.
- No relajar la barrera de state-leak ni la validacion `tested_commit_sha/level/args_mode`.
## Premisas verificadas antes de Builder
- `010m` ya quedo separado como piloto CI y `011i` como follow-up si este opt-in local sale estable.
- `scripts/run_pytest_safe.py` hoy solo distingue `unit|integration|all`, no ofrece flag xdist y el guard de handoff sigue exigiendo `level=all` + `args_mode=default_discovery`.
- `pyproject.toml` no declara aun `pytest-xdist`.
## Decision Arquitectonica
`011e` implementa un camino local y explicito: un flag de paralelizacion que solo se activa sobre subset unitario explicito, registra si xdist se habilito o si se replego a serial, y deja intacto el camino canonico que usa el closeout. La frontera queda asi: `011e` = runner local opt-in medido; `010m` = CI; `011i` = evaluar default futuro.
## Files Likely Touched
### repo_motor
- pyproject.toml
- uv.lock
- scripts/run_pytest_safe.py
- tests/unit/test_run_pytest_safe.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- scripts/pre_handoff_guard.py
- docs/test_performance/test_performance_baseline_WOT-2026-010j.md
- docs/test_performance/test_performance_followup_WOT-2026-010k.md
- .agent/runtime/pytest-safe/last-run.json
- .agent/collaboration/backlog.md
## Forbidden Surfaces
- cambiar la logica de handoff de `scripts/pre_handoff_guard.py`
- tocar `scripts/run_gates_dispatch.py` o workflows de CI
- convertir xdist en default implicito
- aceptar pass-open silencioso cuando el scope no sea seguro
- tocar `privada/`, `.env` o `bus/runtime/events` manualmente
## Criterios binarios
- `pytest-xdist` queda declarado en dependencias dev y reflejado en `uv.lock`.
- `scripts/run_pytest_safe.py` expone un flag opt-in de xdist y mantiene backward-compat total cuando no se usa.
- El flag solo habilita paralelizacion para subset unitario explicito; fuera de ese contrato el runner cae a serial con razon auditable.
- El runner registra en `last-run.json` si xdist fue solicitado, habilitado, con cuantos workers y, si no, el motivo de fallback.
- Existe al menos una prueba FAIL-sin/PASS-con para la ruta xdist y otra para el fallback seguro.
- El Builder deja en `execution_log.md` una medicion comparando el mismo subset unitario en serial vs xdist sobre este host.
- `ruff`, tests focales, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica implementacion viable cambia el default del runner o afecta el camino canonico de closeout.
- Parar si xdist obliga a relajar la barrera de state-leak o rompe cobertura/semantica del subset.
- Parar si el subset seguro no puede definirse sin tocar CI o sin mezclar `010m`/`011i`.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011e.md` si el opt-in local requiere alterar `pre_handoff_guard.py`, si `pytest-xdist` no puede integrarse sin abrir el default del runner, o si el fallback seguro no puede distinguir subset unitario apto de suite canonica.