# work_plan.md -- WOT-2026-013i
## Metadata
- **ID:** WOT-2026-013i
- **Contract ID:** T-013I-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Reducir o acotar la latencia operacional del purge de sandboxes huerfanos en `tests/conftest.py`, manteniendo la limpieza defensiva introducida por `013d` y sin reabrir producto, runner, CI ni la politica xdist/default.
## Non-goals
- No tocar `scripts/project_scanner.py` ni `agent_system/scripts/project_paths.py`.
- No tocar `tests/unit/test_detect_version.py` ni `tests/unit/test_no_inline_ticket_regex.py`; esas barreras se revalidan, no se editan.
- No tocar `scripts/run_pytest_safe.py`, `pytest.ini`, CI/workflows ni la politica `011e` / `010m` / `011i`.
- No convertir la higiene en una limpieza manual o externa al harness de tests.
## Premisas verificadas antes de Builder
- `013g` verifico que >99% del coste observado viene del purge de `tests/conftest.py`, no del cuerpo del test ni del producto.
- `013d` necesita mantener la higiene del sandbox para evitar residuos que amplifican latencia y superficie de race.
- La frontera correcta de este ticket es harness/tests: `tests/conftest.py` y sus barreras de no-regresion.
- Si la unica mejora segura exige tocar producto, runner o xdist, el ticket debe bloquear por `CG-WOT-2026-013i.md`.
## Decision Arquitectonica
`013i` es un ticket `code` de higiene de runtime de tests. El cambio permitido vive en `tests/conftest.py` y en barreras asociadas del propio harness. La cura de producto de `013d` y la politica del runner permanecen congeladas; este ticket solo puede reducir o acotar el coste del purge sin relajar la limpieza defensiva.
## Files Likely Touched
### repo_motor
- tests/conftest.py
- tests/unit/test_project_scanner.py
- tests/unit/test_windows_safe_temp_runtime.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- docs/test_performance/test_upgrade_cost_WOT-2026-013g.md
- docs/test_performance/test_suite_audit_WOT-2026-013e.md
- docs/test_performance/test_performance_variance.md
- tests/unit/test_detect_version.py
- tests/unit/test_no_inline_ticket_regex.py
- scripts/project_scanner.py
- agent_system/scripts/project_paths.py
- scripts/run_pytest_safe.py
## Forbidden Surfaces
- scripts/project_scanner.py
- agent_system/scripts/project_paths.py
- tests/unit/test_detect_version.py
- tests/unit/test_no_inline_ticket_regex.py
- scripts/run_pytest_safe.py
- pytest.ini
- pyproject.toml
- uv.lock
- CI/workflows
- politica xdist/default (`011e`, `010m`, `011i`)
- privada/
- .env
- eventos del bus escritos manualmente
## Criterios binarios
- `execution_log.md` registra una medicion before/after comparable en el mismo host con comandos exactos que aislen el coste de setup/purge o lo acoten con evidencia.
- El cambio reduce o acota la latencia del setup ligada al purge de sandboxes huerfanos sin reintroducir residuos bajo `tests/sandbox/test_runtime/`.
- Existe al menos una barrera de regresion sobre `tests/conftest.py` que protege explicitamente la nueva semantica de purge/higiene.
- `python -m pytest tests/unit/test_project_scanner.py tests/unit/test_windows_safe_temp_runtime.py -q -p no:cacheprovider` termina verde.
- `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` termina verde en 3 corridas consecutivas.
- `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- No se toca producto, runner, CI ni la politica xdist/default.
## STOP conditions
- Parar si la mejora segura solo existe tocando producto, runner, CI o politica xdist/default.
- Parar si la medicion no puede aislar razonablemente el coste del purge en el mismo host.
- Parar si la unica via verde debilita la limpieza defensiva o deja residuos operativos peores.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013i.md` si la unica salida segura exige reabrir `013d` como ticket de producto, tocar el runner/politica xdist o aceptar residuos/flake potencial en el sandbox.

