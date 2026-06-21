# work_plan.md -- WOT-2026-013d
## Metadata
- **ID:** WOT-2026-013d
- **Contract ID:** T-013D-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Endurecer el escaneo de proyecto ante borrados concurrentes en las 3 travesias verificadas de PRODUCTO (`scripts/project_scanner.py` en `_collect_local_modules()` y `scan_project()`, `agent_system/scripts/project_paths.py` en `resolve_paths()`), de modo que el triple xdist historico quede estable sin tocar runner, CI ni la politica xdist/default.
## Non-goals
- No tocar `scripts/run_pytest_safe.py` ni la semantica de `--level all`.
- No tocar `quality-gates.yml`, CI ni workflows.
- No tocar `.agent/agent_controller.py`, `runtime/project_root.py`, `bus/` ni controller/supervisor.
- No mover el sandbox fuera del arbol del repo como atajo para obtener verde.
- No reabrir `011e`, `010m`, `011i` ni `013c` como deuda de runner/politica.
## Premisas verificadas antes de Builder
- `013c` cerro `BLOCKED-FINAL`: la causa raiz ya no es tests-only, sino 3 recorridos `rglob` de PRODUCTO que descienden a `tests/sandbox/test_runtime/session_*` mientras otros workers borran subarboles.
- Los 3 sitios reales verificados son: `scripts/project_scanner.py` (`_collect_local_modules()` y `scan_project()`), `agent_system/scripts/project_paths.py` (`resolve_paths()`).
- Baseline recapturado para el follow-up: `tests/sandbox/test_runtime` contiene `session_dirs=566`.
- El triple sintomatico sigue definido por `test_upgrade_path_suggestion`, `test_scan_current_project` y `test_no_inline_ticket_regex`; la estabilidad exigida es xdist verde en 3 corridas consecutivas.
- `validate --json --project-root <repo_destino>` verde antes del arranque.
## Decision Arquitectonica
`013d` absorbe el hallazgo honesto de `013c` sin reabrir la politica del runner. La limpieza del sandbox debe expresarse via fixture/harness en `tests/conftest.py`; `tests/sandbox/test_runtime` puede verse afectado como efecto colateral controlado, pero no es superficie de edicion manual del ticket.
## Files Likely Touched
### repo_motor
- scripts/project_scanner.py
- agent_system/scripts/project_paths.py
- tests/unit/test_project_scanner.py
- tests/test_project_paths.py
- tests/unit/test_detect_version.py
- tests/unit/test_no_inline_ticket_regex.py
- tests/conftest.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- CG-WOT-2026-013c.md
- prompts/audit_agent_output.md
- tests/README.md
- tests/ARCHITECTURE.md
- docs/test_performance/test_performance_followup_WOT-2026-010k.md
- tests/unit/test_windows_safe_temp_runtime.py
- .agent/runtime/pytest-safe/last-run.json
## Forbidden Surfaces
- scripts/run_pytest_safe.py
- quality-gates.yml
- .github/workflows/*
- .agent/agent_controller.py
- runtime/project_root.py
- bus/
- controller/supervisor
- cualquier cambio del default xdist o de la semantica de `--level all`
- mover el sandbox fuera del arbol del repo como salida rapida
- borrado manual de historico o runtime fuera de `tests/sandbox/test_runtime`
## Criterios binarios
- Los 3 puntos de escaneo verificados quedan robustos frente a borrados concurrentes y el fix cubre tambien el recorrido de `scan_project()` (no solo `_collect_local_modules()`).
- Existe limpieza determinista del ruido en `tests/sandbox/test_runtime`, gestionada via fixture/harness en `tests/conftest.py`, y `execution_log.md` registra baseline + reconciliacion usada para la verificacion final.
- `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` queda verde en 3 corridas consecutivas sobre el mismo host.
- El diff productivo queda acotado a escaneo de producto + tests/fixtures declarados; no toca runner, CI ni codigo de producto ajeno.
- La correccion preserva el sentido de los tests: no sustituye aserciones reales por mocks, floors, `xfail` o `skip` cosmeticos.
- `python -m pytest tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py -q`, `ruff check scripts/project_scanner.py agent_system/scripts/project_paths.py tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `uv run ruff format --check scripts/project_scanner.py agent_system/scripts/project_paths.py tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica via verde toca `scripts/run_pytest_safe.py`, `quality-gates.yml`, CI o la politica xdist/default.
- Parar si la unica salida verde mueve el sandbox fuera del arbol o rompe la invariante de `tests/unit/test_windows_safe_temp_runtime.py`.
- Parar si el rojo dominante deja de ser reproducible con el triple acordado y exige ticket nuevo en vez de ensanchar `013d`.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013d.md` si volver verde el triple xdist exige tocar runner, CI, politica xdist/default o reconciliar la invariante sandbox-dentro-vs-fuera fuera de las superficies declaradas; o si el fix exige ampliar superficie mas alla de producto/tests declarados.
