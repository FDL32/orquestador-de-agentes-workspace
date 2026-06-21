# work_plan.md -- WOT-2026-010m
## Metadata
- **ID:** WOT-2026-010m
- **Contract ID:** T-010M-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Anadir un piloto CI xdist estrictamente aditivo en `.github/workflows/quality-gates.yml`, reutilizando el camino opt-in creado por `011e` sin tocar el default del runner ni el cierre canonico `--level all`.
## Non-goals
- No tocar `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `scripts/pre_handoff_guard.py` ni `scripts/run_gates_dispatch.py`.
- No convertir xdist en default implicito, ni local ni en CI, ni cambiar la semantica del cierre canonico `python scripts/run_pytest_safe.py --level all`.
- No mezclar el ticket con `011i` (default futuro), `011h`, otros workflows ni cambios de policy fuera de `quality-gates.yml`.
## Premisas verificadas antes de Builder
- `.github/workflows/quality-gates.yml` sigue ejecutando la ruta serial canonica y aun no consume `--xdist-workers`.
- `scripts/run_pytest_safe.py` ya soporta `--xdist-workers` por `011e`, con fallback auditable y cierre canonico intacto.
- La frontera `011e <-> 010m <-> 011i` ya esta fijada: `011e` = runner local opt-in, `010m` = piloto CI, `011i` = evaluar default despues.
- Si el piloto CI exige tocar el runner o el guard de handoff, el resultado correcto es `CG-WOT-2026-010m.md`.
## Decision Arquitectonica
`010m` se mantiene en la capa de workflow + barrera CI. Consume la capacidad ya expuesta por `011e`, pero no reabre el contrato del runner ni cambia la corrida canonica que sigue gobernando handoff y cierre.
## Files Likely Touched
### repo_motor
- .github/workflows/quality-gates.yml
- tests/unit/test_quality_gates_workflow.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- scripts/run_pytest_safe.py
- tests/unit/test_run_pytest_safe.py
- scripts/pre_handoff_guard.py
- docs/test_performance/test_performance_baseline_WOT-2026-010j.md
- docs/test_performance/test_performance_followup_WOT-2026-010k.md
- .agent/runtime/pytest-safe/last-run.json
- .agent/collaboration/_archive/backlog_done.md
## Forbidden Surfaces
- tocar `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `scripts/pre_handoff_guard.py` o `scripts/run_gates_dispatch.py`
- meter xdist en la corrida canonica `--level all` o convertirlo en default implicito
- tocar otros workflows, CI policy ajena, `privada/`, `.env` o eventos del bus manualmente
- ampliar el ticket a una reescritura del selector/runner para aislar tests paralelos
## Criterios binarios
- `.github/workflows/quality-gates.yml` incorpora un piloto CI xdist estable y acotado, sin eliminar ni alterar la corrida serial canonica existente.
- El piloto usa `scripts/run_pytest_safe.py` con `--xdist-workers <N>` solo sobre la superficie permitida del ticket; la corrida canonica en CI sigue sin xdist.
- `tests/unit/test_quality_gates_workflow.py` aporta una barrera FAIL-sin/PASS-con que falla si desaparece el piloto o si la corrida canonica adopta xdist por accidente.
- `execution_log.md` deja evidencia de la separacion entre piloto CI y cierre canonico, con resultado/medicion auditable del piloto.
- `python -m pytest tests/unit/test_quality_gates_workflow.py -q`, `ruff check tests/unit/test_quality_gates_workflow.py`, `uv run ruff format --check tests/unit/test_quality_gates_workflow.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica implementacion viable toca el runner, el guard de handoff o el dispatcher.
- Parar si el piloto solo puede validarse convirtiendo xdist en default o metiendolo en la corrida canonica `--level all`.
- Parar si los tests no parallel-safe obligan a redisenar el selector/runner en vez de dejar un piloto CI acotado.
## CONTRACT_GAP
Emitir `CG-WOT-2026-010m.md` si el piloto CI no puede definirse sin tocar `scripts/run_pytest_safe.py`, si la unica via verde convierte xdist en default o lo mete en el camino canonico `--level all`, o si el subset seguro exige expansion a nuevas superficies del runner/selector fuera del workflow y la barrera declarada.