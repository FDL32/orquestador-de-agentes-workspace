# Execution Log -- WOT-2026-013g

**Estado:** COMPLETED

## MANAGER - WOT-2026-013g - Bootstrap operativo

Ticket activado para diagnosticar el coste unknown de `test_upgrade_path_suggestion` sin tocar test, runner ni producto.

Packet activo en repo_destino:
- backlog alineado: `013f` sale de la cola viva y pasa a historico; `013g` queda como ultimo ticket accionable
- `OBJ-013G-001` en `repo_charter.md`
- `PLAN-013G-001` en `plan_graph.md`
- `T-013G-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013g.md` y `AUDIT_WOT-2026-013g.md` activos para Builder

Premisa operativa del Builder:
- releer `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_variance.md`, `docs/test_performance/test_suite_audit_WOT-2026-013e.md` y `tests/unit/test_detect_version.py`
- medir en foreground con comandos reproducibles y comparables
- producir solo `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` + evidencia en `execution_log.md`
- si explicar el coste exige tocar el test o producto, parar y emitir `CG-WOT-2026-013g.md`

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `bc658f8`
- repo_destino HEAD = `<pending closeout+bootstrap commit>`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings
- `013f` cerrado canonica y documentalmente; `013g` es ahora el ultimo ticket pendiente accionable

## BUILDER - WOT-2026-013g - Fase 0 (diagnostico read-only)

Preflight bootstrap verificado: STATE.md=WOT-2026-013g/IN_PROGRESS, TURN.md Plan ID=WOT-2026-013g, work_plan.md ID=WOT-2026-013g, bus seq 1318 STATE_CHANGED->IN_PROGRESS para 013g (013f COMPLETED seq 1316). No anclado a ticket anterior.

Lecturas previas (Read/inspect only) completadas:
- docs/test_performance/test_performance_baseline.md (010j: outlier #3 59.22s), test_performance_variance.md (010p: #2 ~68-70s), test_suite_audit_WOT-2026-013e.md (clasificado unknown).
- tests/unit/test_detect_version.py: confirmado que `test_upgrade_path_suggestion` (l.195-210) pertenece a `TestVersionDetection`, cuerpo trivial = instancia `AgentSystemDetector(".")` + 6 llamadas a `suggest_upgrade_path` (op de string pura, sin I/O en el cuerpo).

Seam de coste identificado por lectura (a confirmar con medicion):
- `AgentSystemDetector.__init__` (scripts/detect_version.py l.114-118) construye `ProjectPathsResolver(project_dir)` y llama `get_project_root()` / `get_agent_dir()` / `get_drift_info()`.
- El test pasa `project_dir="."` (repo real), NO un `tmp_path` aislado como los otros 14 tests del archivo.
- `ProjectPathsResolver.resolve_paths()` (agent_system/scripts/project_paths.py l.82+) llama `_find_agent_dirs()` (l.36-47) que hace `os.walk` del ARBOL COMPLETO para detectar drift de multiples `.agent`. Sobre `.` = el repo entero, incluyendo `tests/sandbox/test_runtime/` (cientos de miles de entradas segun 010k).
- HIPOTESIS [I]: el coste de ~60-70s es el `os.walk` del repo real disparado por `project_dir="."`, no el cuerpo del test. Es el mismo subsistema que 013d endurecio (no su bug de crash, sino su coste de travesia).

Comandos de medicion a usar (foreground, reproducibles):
- `python -m pytest tests/unit/test_detect_version.py -q --durations=10` (archivo completo, ver atribucion)
- `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion -q --durations=10` (focal aislado)
- micro-bench directo del seam: instanciar `AgentSystemDetector(".")` vs `suggest_upgrade_path` puro, con `time.perf_counter`, para atribuir el coste al walk y no al cuerpo.

Desviaciones de scope: ninguna. El test usa `.` pero NO se tocara (Forbidden). Procedo a Fase 1 (medir + reporte).

## BUILDER - WOT-2026-013g - Fase 1 (mediciones) + gates + entrega

Mediciones (foreground, reproducibles, HEAD bc658f8):
- M1 focal aislado: `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion -q --durations=10 -p no:cacheprovider` => `53.51s setup`, `0.10s call`, `1 passed in 53.68s`. [V] El coste esta en setup, no en el cuerpo (call=0.10s).
- M2 micro-bench directo (perf_counter): `AgentSystemDetector(".")` __init__ = 0.048s; 6x `suggest_upgrade_path` = 0.0000s. [V] Constructor y cuerpo baratos; hipotesis del os.walk-en-ctor REFUTADA.
- M3 archivo completo: `python -m pytest tests/unit/test_detect_version.py -q --durations=15 -p no:cacheprovider` => `43.90s setup ...::test_detect_v8x_structures` (PRIMER test), `0.07s call ...::test_upgrade_path_suggestion`, `15 passed in 44.17s`. [V] El setup caro se atribuye al primer test ejecutado, no al focal.

Causa raiz [V]: `tests/conftest.py` fixture session-autouse `_project_temp_environment` (l.81-85) llama en sessionstart `_purge_orphan_session_dirs()` (l.57-76, introducido por 013d) que hace `shutil.rmtree` de los `session_<PID>` huerfanos en `tests/sandbox/test_runtime/`. Conteo actual: `ls -d tests/sandbox/test_runtime/session_* | wc -l` => 568 dirs huerfanos. Borrar ese arbol en Windows es el coste ~44-53s, atribuido por pytest al setup del primer test. El "outlier" es artefacto de atribucion de un coste de higiene de sesion unica, variable segun sandbox acumulado.

Conclusion binaria del reporte: SIN OPTIMIZACION SEGURA en este ticket. El test no tiene coste propio (0.07s); el coste real es la purga de sandbox de conftest (Forbidden Surface + barrera de 013d). Recomendacion: si se ataca, abrir ticket de higiene de runner/sandbox aparte; mientras tanto `run_pytest_safe.py --cleanup-only` reduce el outlier sin tocar codigo. Reclasificar el unknown de 013e como coste-de-harness explicado.

Gates (comandos exactos + exit codes):
- pytest focal (M1/M2/M3 arriba): instrumento de analisis, NO cierre canonico.
- Ruff / ruff format: NO APLICA (ticket analysis, no se toco Python).
- Encoding guard: `python scripts/check_encoding_guard.py docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` => exit 0.
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings.
- Diff motor: `git status --porcelain` => unico cambio `?? docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` (165 lineas). No se toco test, producto, runner ni CI.

Desviaciones y justificaciones CEM: ninguna. Procedo a commit + pre-handoff + mark-ready.

Reporte docs/test_performance/test_upgrade_cost_WOT-2026-013g.md creado. Validate: exit code 0, 0 errors, 0 warnings.


Manager approved canonical closeout for WOT-2026-013g