# work_plan.md -- WOT-2026-013c
## Metadata
- **ID:** WOT-2026-013c
- **Contract ID:** T-013C-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Volver parallel-safe `test_upgrade_path_suggestion`, `test_scan_current_project` y `test_no_inline_ticket_regex` sin tocar runner, CI ni la politica xdist/default. El entregable es aislamiento de tests y fixtures, no un cambio de politica del runner.
## Non-goals
- No tocar `scripts/run_pytest_safe.py` ni la semantica de `--level all`.
- No tocar `quality-gates.yml`, CI ni workflows.
- No tocar `.agent/agent_controller.py`, `runtime/`, `bus/` ni codigo de producto.
- No reabrir `011i` ni `013b` como deuda de runner.
## Premisas verificadas antes de Builder
- `011e` COMPLETED y `010m` COMPLETED: xdist opt-in local + piloto CI non-blocking ya son la solucion vigente.
- `011i` y `013b` cerraron honestamente como `not-pursued` / `absorbed`: la politica de runner quedo refutada y NO pertenece a este ticket.
- Los 3 tests persistentes nombrados en el contrato (`test_upgrade_path_suggestion`, `test_scan_current_project`, `test_no_inline_ticket_regex`) son la deuda real global-state-bound a aislar.
- `validate --json --project-root <repo_destino>` verde antes del arranque.
## Decision Arquitectonica
`013c` cambia de capa respecto a `011i`: deja quieta la politica del runner y trabaja solo sobre higiene de tests. Si el rojo deja de pertenecer a estos 3 tests, el ticket para via `CONTRACT_GAP` en vez de ensanchar scope.
## Files Likely Touched
### repo_motor
- tests/unit/test_detect_version.py
- tests/unit/test_project_scanner.py
- tests/unit/test_no_inline_ticket_regex.py
- tests/conftest.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- scripts/run_pytest_safe.py
- tests/unit/test_run_pytest_safe.py
- docs/test_performance/test_performance_baseline_WOT-2026-010j.md
- docs/test_performance/test_performance_followup_WOT-2026-010k.md
- docs/test_performance/test_performance_variance_WOT-2026-010p.md
- .agent/collaboration/_archive/backlog_done.md
- .agent/runtime/pytest-safe/last-run.json
## Forbidden Surfaces
- scripts/run_pytest_safe.py
- quality-gates.yml
- .github/workflows/*
- .agent/agent_controller.py
- runtime/
- bus/
- pre_handoff_guard.py
- cualquier cambio del default xdist o de la semantica de `--level all`
- codigo de producto fuera de tests/fixtures
## Criterios binarios
- Los 3 tests citados pasan serialmente y tambien verdes juntos bajo `python -m pytest <triple> -q -n 8 --dist load`.
- El diff productivo queda acotado a superficies de test/fixture declaradas; no toca runner, CI ni codigo de producto.
- Existe al menos una barrera FAIL-sin/PASS-con contra el rojo real de estado compartido / concurrencia.
- La correccion preserva el sentido de cada test: no sustituye aserciones reales por mocks o floors triviales.
- `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q`, `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q -n 8 --dist load`, `ruff check tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `uv run ruff format --check tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica via verde toca `scripts/run_pytest_safe.py`, `quality-gates.yml` o `runtime/`.
- Parar si la reproduccion deja de centrarse en estos tres tests.
- Parar si el rojo restante tras el fix pertenece ya a otra familia y exige ticket nuevo en vez de ensanchar `013c`.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013c.md` si volver verdes los 3 tests exige tocar runner, CI, politica xdist/default o codigo de producto; si el rojo dominante migra a otra familia distinta al corregir estos tres; o si el fix requiere ampliar superficie mas alla de tests/fixtures declarados.