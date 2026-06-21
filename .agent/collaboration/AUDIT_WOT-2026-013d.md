# AUDIT_WOT-2026-013d

## Preguntas binarias
- [ ] El diff productivo toca solo las superficies declaradas (`project_scanner`, `project_paths`, tests/fixtures asociados) y no invade runner/CI/default xdist.
- [ ] Los 3 sitios `rglob` verificados quedaron cubiertos por el fix, incluido `scan_project()`.
- [ ] La limpieza de `tests/sandbox/test_runtime` se expresa via `tests/conftest.py` o harness equivalente dentro de FLT, no por manipulacion manual del arbol sandbox.
- [ ] Existe evidencia FAIL-sin/PASS-con que demuestra que la robustez viene del fix y no solo de limpiar ruido residual.
- [ ] El triple xdist (`test_upgrade_path_suggestion`, `test_scan_current_project`, `test_no_inline_ticket_regex`) queda verde en 3 corridas consecutivas sobre el mismo host.
- [ ] `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes al cierre.

## Rechazar si aparece cualquiera de estos hallazgos
- Se toca `scripts/run_pytest_safe.py`, CI o la politica xdist/default.
- Se mueve el sandbox fuera del arbol del repo para forzar el verde.
- El fix cubre `_collect_local_modules()` pero deja vivo el rojo en `scan_project()` o `project_paths.resolve_paths()`.
- Se usan mocks, `skip`, `xfail` o floors para maquillar el rojo xdist.
- El triple verde solo ocurre una vez y no se demuestra estabilidad por 3 corridas.
