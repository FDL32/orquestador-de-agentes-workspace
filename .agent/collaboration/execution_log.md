# Execution Log -- WOT-2026-013d

**Estado:** IN_PROGRESS

## MANAGER - WOT-2026-013d - Bootstrap operativo

Ticket abierto como sucesor correcto de `013c`: la familia xdist/default ya quedo cerrada y la deuda real vive en producto (`project_scanner` / `project_paths`) con ruido concurrente de `tests/sandbox/test_runtime`.

Packet congelado y actualizado en repo_destino:
- backlog vivo + ficha `013d`
- `T-013D-001` en `ticket_contracts.md`
- `PLAN-013D-001` en `plan_graph.md`
- aclaracion explicita: la limpieza del sandbox se expresa via fixture/harness en `tests/conftest.py`, no por edicion manual del arbol

Premisa operativa del Builder:
- recapturar baseline de `tests/sandbox/test_runtime` antes del fix
- reproducir el triple xdist (`test_upgrade_path_suggestion`, `test_scan_current_project`, `test_no_inline_ticket_regex`) con `-n 8 --dist load`
- cubrir los 3 sitios `rglob` verificados, incluido `scan_project()`
- demostrar triple xdist verde en 3 corridas consecutivas
- cualquier necesidad de tocar runner/CI/default xdist o mover el sandbox fuera del arbol dispara STOP + `CG-WOT-2026-013d.md`

## BUILDER - WOT-2026-013d - Escaneo robusto ante borrados concurrentes

### Fase 0 - Baseline
- 3 sitios rglob confirmados: project_scanner._collect_local_modules (l.344), scan_project (l.615), project_paths.resolve_paths (l.59). Baseline ~566 session_dirs huerfanos.
- Triple xdist reproducido rojo: FileNotFoundError en pathlib durante rglob (set no determinista 1-3 failed).

### Fase 1 - Fix de producto (3 sitios)
- scripts/project_scanner.py: nuevo _safe_walk() (os.walk con onerror + poda de EXCLUDE_DIRS y tests/sandbox/test_runtime ANTES de descender via _is_excluded_dir). Usado en _collect_local_modules y scan_project. scan_project ademas tolera FileNotFoundError/PermissionError/OSError en path.stat() post-listado. sorted() preserva determinismo.
- agent_system/scripts/project_paths.py: nuevo _find_agent_dirs() (os.walk robusto + poda) reemplaza rglob(".agent") en resolve_paths().
- tests/unit/test_no_inline_ticket_regex.py: su propio rglob (no es producto, esta en FLT) robustecido via _safe_scan_py() con misma poda/tolerancia.

### Fase 2 - Higiene + barreras
- tests/conftest.py: _purge_orphan_session_dirs() (session-scoped, autouse) limpia session_<PID> muertos al inicio. Higiene determinista del sandbox via fixture (no edicion manual del arbol).
- 5 barreras FAIL-sin/PASS-con: test_project_scanner.py::TestConcurrentDeleteRobustness (prune sandbox + tolerate vanished) y test_project_paths.py::TestFindAgentDirsRobustness (nested + prune + tolerate vanished). Cubren scan_project, _safe_walk y _find_agent_dirs.

### Fase 3 - Verificacion fuerte
- Triple xdist verde en 3 corridas consecutivas: 3/3/3 passed (-n 8 --dist load). Antes: 1-3 failed.
- Focal (4 archivos DoD): 70 passed. 5 barreras: 5 passed.
- ruff check: All checks passed (tras eliminar dead code _safe_iter_dirs y un test no-determinista). ruff format --check: ok. encoding: exit 0.
- Suite canonica --level all: 3091 passed, 20 skipped, 0 failed (exit 0, 7m26s).

### Calidad (auto-auditada)
- Eliminado _safe_iter_dirs (dead code) y un test "baseline unsafe" no-determinista, anti-patrones que el propio prompt de auditoria marca.
- Diff acotado a 6 superficies del FLT: project_scanner.py, project_paths.py, conftest.py, test_project_scanner.py, test_project_paths.py, test_no_inline_ticket_regex.py.
