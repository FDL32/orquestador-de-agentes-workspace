# plan_graph.md -- Plan WOT-2026-008

## PLAN-001 -- Inventario y contrato de migracion

- objetivo: producir el manifiesto verificable de taxonomia y compatibilidad que
  enlaza OBJ-001, OBJ-002 y OBJ-003.
- tickets: [WOT-2026-008a]
- depends_on: [WOT-2026-007d]
- superficies_archivo:
  - repo_destino/.agent/docs/taxonomy_migration_WOT-2026-008a.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - prompts/*.md y su contrato source_prompt/Skill canonica
  - skills/*/SKILL.md, name, triggers y contract_id
  - scripts/discover_skills.py y scripts/check_skill_collisions.py (read-only)
- shared_dependencies:
  - MANIFEST.distribute y MANIFEST.workspace (read-only)
  - AGENTS.md, PROJECT.md, QUICKSTART.md, llms*.txt y tests (read-only)

## PLAN-010D-001 -- Lifecycle canonico de pausa/reanudacion

- objetivo: producir la capacidad minima de `pause/resume` canonicos para tickets
  activos del motor sin stash opaco y con recuperacion fail-closed.
- tickets: [WOT-2026-010d]
- depends_on: [WOT-2026-010c]
- superficies_archivo:
  - repo_motor/.agent/agent_controller.py
  - repo_motor/.agent/state_validation.py
  - repo_motor/bus/state_machine.py
  - repo_motor/bus/supervisor.py
  - repo_motor/bus/builder_locks.py
  - repo_motor/scripts/pre_handoff_guard.py
  - repo_motor/runtime/ui_state_projector.py
  - repo_motor/tests/unit/test_pause_ticket.py
  - repo_motor/tests/unit/test_resume_ticket.py
  - repo_motor/tests/test_pre_handoff_guard.py
  - repo_motor/tests/unit/test_state_projection_probe.py
  - repo_destino/.agent/collaboration/paused/<ticket>.json (artefacto runtime producido por la feature)
- interfaces:
  - CLI `agent_controller.py --pause-ticket|--resume-ticket|--abort-paused-ticket`
  - event bus `TICKET_PAUSED`, `TICKET_RESUMED`, `STATE_CHANGED`
  - proyecciones `TURN.md`, `STATE.md`, `execution_log.md`
- shared_dependencies:
  - EventBus y secuencias cross-ticket
  - runtime multi-root (`repo_motor` + `repo_destino`)
  - `pre_handoff_guard.py` y `--mark-ready`
  - `run_pytest_safe.py` / `validate --json` como gates de cierre


## PLAN-012B-001 -- Gate backlog fail-closed sobre cola viva

- objetivo: convertir el contrato de cola viva fijado por `012a` en una barrera
  automatica fail-closed ejecutable desde `repo_motor`, leyendo
  `repo_destino/.agent/collaboration/backlog.md` solo via `--project-root` o
  `AGENT_PROJECT_ROOT`.
- tickets: [WOT-2026-012b]
- depends_on: [WOT-2026-012a]
- superficies_archivo:
  - repo_motor/scripts/check_backlog_contract.py
  - repo_motor/tests/unit/test_check_backlog_contract.py
  - repo_motor/scripts/run_gates_dispatch.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - CLI `scripts/check_backlog_contract.py --project-root <repo_destino>`
  - dispatcher `scripts/run_gates_dispatch.py`
  - tabla activa de `repo_destino/.agent/collaboration/backlog.md`
- shared_dependencies:
  - resolucion topologica `--project-root` / `AGENT_PROJECT_ROOT`
  - `scripts/check_deliverables_exist.py` y `scripts/validate_ticket_prose.py` (read-only)
  - contrato de estados/`Reactivation` fijado por `012a`
  - `validate --json --project-root <repo_destino>` como gate de cierre



## PLAN-013A-001 -- Robustez del test approved_pending sin drift de topologia

- objetivo: reparar el rojo aislado de `test_approved_pending_returns_builder_implement` endureciendo solo el fixture/driver de `tests/test_controller_integration.py`, sin tocar codigo productivo del controller ni introducir features nuevas de topologia.
- tickets: [WOT-2026-013a]
- depends_on: []
- superficies_archivo:
  - repo_motor/tests/test_controller_integration.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `python -m pytest tests/test_controller_integration.py -k approved_pending -q`
  - fixture `sandbox()` y helper `_run()` en `tests/test_controller_integration.py`
- shared_dependencies:
  - `.agent/agent_controller.py` (read-only; no feature nueva en este ticket)
  - `runtime/` y `bus/` copiados por el fixture (read-only)
  - cierre canonico `python scripts/run_pytest_safe.py --level all`

## PLAN-011B-001 -- Determinismo del timeout de relaunch en tests

- objetivo: hacer determinista la familia de pruebas de relaunch que ejerce verificaciones temporizadas, reutilizando la costura existente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` sin cambiar la semantica productiva ni el timeout default del runtime.
- tickets: [WOT-2026-011b]
- depends_on: []
- superficies_archivo:
  - repo_motor/bus/builder_relaunch.py
  - repo_motor/tests/test_supervisor.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - env var `BUILDER_START_VERIFY_TIMEOUT_SECONDS`
  - helper `bus/builder_relaunch.py::_verify_builder_start()`
  - eventos `BUILDER_RELAUNCH_ATTEMPTED`
- shared_dependencies:
  - `bus/supervisor.py` (read-only; wrapper/topologia de relaunch)
  - `tests/test_relaunch_evidence_capsule.py` (read-only; familia de relaunch relacionada)
  - cierre canonico `python scripts/run_pytest_safe.py --level all`

## PLAN-011E-001 -- xdist opt-in local medido para subset unitario

- objetivo: introducir un camino local y explicito de paralelizacion xdist para subset unitario, con medicion auditable y fallback seguro a serial, sin tocar el cierre canonico ni el default del runner.
- tickets: [WOT-2026-011e]
- depends_on: []
- superficies_archivo:
  - repo_motor/pyproject.toml
  - repo_motor/uv.lock
  - repo_motor/scripts/run_pytest_safe.py
  - repo_motor/tests/unit/test_run_pytest_safe.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - CLI `python scripts/run_pytest_safe.py --level unit --xdist-workers <N|auto> -- tests/unit`
  - artefacto runtime `.agent/runtime/pytest-safe/last-run.json`
- shared_dependencies:
  - `scripts/pre_handoff_guard.py` (read-only; contrato canonico `level=all` + `args_mode=default_discovery`)
  - `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
  - frontera `011e <-> 010m <-> 011i` (local opt-in vs CI vs default futuro)


## PLAN-011F-001 -- Contrato PS1 multiplataforma y barrera de encoding

- objetivo: fijar el contrato de fuente para PowerShell (`*.ps1`) en el motor: line endings explicitos, launcher sin BOM ni mojibake, y cobertura determinista del guard de encoding sobre los scripts PowerShell reales.
- tickets: [WOT-2026-011f]
- depends_on: [WOT-2026-010w, WOT-2026-011c, WOT-2026-011j]
- superficies_archivo:
  - repo_motor/.gitattributes
  - repo_motor/scripts/launch_agent_terminals.ps1
  - repo_motor/scripts/encoding_guard.py
  - repo_motor/tests/test_encoding_integrity.py
  - repo_motor/tests/test_launch_agent_terminals_script.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - contrato git de `*.ps1` en `.gitattributes`
  - barrido repo-wide de `scripts/encoding_guard.py`
  - CLI `python scripts/check_encoding_guard.py scripts/launch_agent_terminals.ps1`
- shared_dependencies:
  - evidencia de fuente `WOT-2026-011c` (BOM por `-Encoding UTF8` en PS 5.1)
  - fix funcional previo `WOT-2026-011j` (writers BOM-safe ya in-scope)
  - tests estructurales del launcher y estabilidad de opencode (read-only)

## PLAN-011G-001 -- Politica explicita de loop rapido vs cierre canonico

- objetivo: explicitar en prompts y Quickstart la frontera entre diagnostico rapido local y cierre canonico de ticket, alineando Builder, Manager y Orchestrator sin tocar tooling ni gates.
- tickets: [WOT-2026-011g]
- depends_on: [WOT-2026-010c, WOT-2026-010q]
- superficies_archivo:
  - repo_motor/prompts/orchestrator_launch_builder.md
  - repo_motor/prompts/manager_review.md
  - repo_motor/prompts/orchestrator_pipeline.md
  - repo_motor/QUICKSTART.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - artefacto canonico de suite `repo_motor/.agent/runtime/pytest-safe/last-run.json`
  - handoff/cierre `--pre-handoff`, `--mark-ready`, `--manager-approve`
  - terminologia `loop rapido` vs `cierre canonico`
- shared_dependencies:
  - `prompts/audit_agent_output.md` (read-only; principio de evidencia)
  - `AGENTS.md` y `QUICKSTART.md` (contrato publico de comandos)
  - observaciones `obs-20260619-background-wallclock-not-canonical` y `obs-20260620-last-run-canonical-lives-in-motor`


## PLAN-010X-001 -- Reemplazo OSS de gitleaks en CI

- objetivo: sustituir en `security-audit.yml` el uso de `gitleaks/gitleaks-action@v2` por una invocacion CLI OSS de gitleaks, manteniendo el escaneo fail-closed y una barrera de regresion del workflow sin tocar la politica portable de allowlists.
- tickets: [WOT-2026-010x]
- depends_on: []
- superficies_archivo:
  - repo_motor/.github/workflows/security-audit.yml
  - repo_motor/tests/unit/test_hook_ci_alignment.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - GitHub Actions workflow `security-audit.yml`
  - paso `Run Gitleaks`
  - barrera `tests/unit/test_hook_ci_alignment.py`
- shared_dependencies:
  - `agent_system/templates/gitleaks.config.toml` (read-only; politica portable ya fijada)
  - `.pre-commit-config.yaml` (read-only; el workflow sigue delegando pre-commit por separado)
  - historico `WOT-2026-004a` / `WOT-2026-004b` (read-only; contexto de politica y falsos positivos)

## PLAN-010M-001 -- Piloto CI xdist acotado sobre quality-gates

- objetivo: anadir un piloto CI xdist aditivo y acotado en `quality-gates.yml`, reutilizando la capacidad opt-in creada por `011e` sin tocar el default del runner ni el cierre canonico `--level all`.
- tickets: [WOT-2026-010m]
- depends_on: [WOT-2026-010j, WOT-2026-010k, WOT-2026-011e]
- superficies_archivo:
  - repo_motor/.github/workflows/quality-gates.yml
  - repo_motor/tests/unit/test_quality_gates_workflow.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - GitHub Actions workflow `quality-gates.yml`
  - CLI `python scripts/run_pytest_safe.py --level unit --xdist-workers <N>`
  - cierre canonico `python scripts/run_pytest_safe.py --level all`
- shared_dependencies:
  - `scripts/run_pytest_safe.py` y `tests/unit/test_run_pytest_safe.py` (read-only; contrato xdist ya fijado por 011e)
  - `scripts/pre_handoff_guard.py` (read-only; el handoff sigue exigiendo `--level all`)
  - frontera `011e <-> 010m <-> 011i` (local opt-in vs piloto CI vs default futuro)

## PLAN-011H-001 -- Barrera de archivado tambien en mark-ready

- objetivo: cerrar fail-closed el auto-archivado de `--mark-ready` cuando deja `archive_rename_uncommitted`, reutilizando la razon estable de `011a` sin introducir auto-commit del archivador.
- tickets: [WOT-2026-011h]
- depends_on: [WOT-2026-011a, WOT-2026-011d]
- superficies_archivo:
  - repo_motor/.agent/agent_controller.py
  - repo_motor/tests/test_agent_controller.py
  - repo_motor/tests/test_pre_handoff_guard.py
  - repo_motor/tests/unit/test_scope_gate.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - CLI `python .agent/agent_controller.py --mark-ready --project-root <repo_destino>`
  - helper `_auto_archive_closed_artifacts()`
  - razon estable `archive_rename_uncommitted`
- shared_dependencies:
  - `scripts/pre_handoff_guard.py` y `scripts/delivery_hygiene_check.py` (read-only; diagnostico existente)
  - closeout endurecido por `011a` (read-only; fuente del contrato de razon/remediacion)
  - cierre canonico `python scripts/run_pytest_safe.py --level all`

## PLAN-013B-002 -- [CANCELADO / ABSORBED por PLAN-011I-001]

- estado: absorbed (cancelado por premisa falsa; ver `CG-WOT-2026-013b.md` FINAL y `ticket_contracts.md` T-013B-001).
- objetivo (ANULADO): "hacer parallel-safe `test_project_root_resolution.py`" quedo refutado. El rojo del
  subset unit bajo xdist no es una familia de tests aislable sino contencion de reparto cross-archivo
  (propiedad del runner): 3 corridas dieron 12<->37 fallos con archivo dominante variable; cada archivo pasa
  aislado bajo `-n 8`. Este plan NO es un grafo operativo activo y no debe planificarse.
- tickets: [WOT-2026-013b] (absorbed)
- sucesor: PLAN-011I-001 (la politica de reparto `--dist loadscope` vive ahi).

## PLAN-011I-001 -- [NOT-PURSUED]

- estado: not-pursued (ver `CG-WOT-2026-011i.md`; `ticket_contracts.md` T-011I-001).
- objetivo (ANULADO): "default xdist + loadscope para --level unit" quedo refutado. loadscope no estabiliza
  el subset (3 corridas: 3->1->3 failed); los 3 tests persistentes pasan serial y dependen de estado global
  del proceso (cwd/git/escaneo), no aislable por reparto. Este plan NO es un grafo operativo activo.
- tickets: [WOT-2026-011i] (not-pursued); absorbio [WOT-2026-013b] (tambien cerrado)
- solucion vigente: opt-in local `011e` + piloto CI non-blocking `010m`. `--level all` serial e intacto.
- follow-up opcional (no contratado): robustecer los 3 tests global-state-bound para paralelizacion.

## PLAN-013C-001 -- [BLOCKED-FINAL]

- estado: blocked-final (ver `CG-WOT-2026-013c.md`; `ticket_contracts.md` T-013C-001).
- objetivo (ANULADO): "robustecer 3 tests global-state tests-only" quedo refutado: la cura exige tocar el
  rglob de producto (project_scanner/project_paths) o romper la invariante sandbox-dentro (test_windows_safe).
  Este plan NO es un grafo operativo activo.
- tickets: [WOT-2026-013c] (blocked-final)
- solucion vigente: opt-in xdist 011e + piloto CI 010m. `--level all` serial e intacto.
- sucesor recomendado (no contratado): ticket de PRODUCTO para escaneo robusto ante borrados concurrentes.


## PLAN-013D-001 -- Escaneo robusto de proyecto ante borrados concurrentes

- objetivo: endurecer las 3 travesias de escaneo verificadas en PRODUCTO (`scripts/project_scanner.py` en `_collect_local_modules()` y `scan_project()`, `agent_system/scripts/project_paths.py` en `resolve_paths()`) para que toleren subdirectorios volatiles borrados por otros workers, sin tocar la politica del runner ni mover el sandbox fuera del arbol.
- tickets: [WOT-2026-013d]
- depends_on: [WOT-2026-013c]
- superficies_archivo:
  - repo_motor/scripts/project_scanner.py
  - repo_motor/agent_system/scripts/project_paths.py
  - repo_motor/tests/unit/test_project_scanner.py
  - repo_motor/tests/test_project_paths.py
  - repo_motor/tests/unit/test_detect_version.py
  - repo_motor/tests/unit/test_no_inline_ticket_regex.py
  - repo_motor/tests/conftest.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `scan_project()`
  - `_collect_local_modules()`
  - `ProjectPathsResolver.resolve_paths()`
  - `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load`
- shared_dependencies:
  - `tests/sandbox/test_runtime/` como superficie volatil real (baseline `session_dirs=566`); su limpieza se expresa via `tests/conftest.py`, no como edicion manual del arbol sandbox
  - `scripts/run_pytest_safe.py` y politica xdist/default (read-only; frontera cerrada por 011e/010m/011i)
  - `tests/unit/test_windows_safe_temp_runtime.py` como guardia de la invariante sandbox-dentro (read-only)


## PLAN-013E-001 -- Inventario auditable y poda segura de la suite

- objetivo: producir un inventario durable de la suite del motor que clasifique familias de tests por valor y riesgo, dejando follow-ups pequenos para poda segura sin tocar runner, CI ni producto en esta ronda.
- tickets: [WOT-2026-013e]
- depends_on: [WOT-2026-010j, WOT-2026-010k, WOT-2026-011e, WOT-2026-010m, WOT-2026-013d]
- superficies_archivo:
  - repo_motor/docs/test_performance/test_suite_audit_WOT-2026-013e.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - CLI `python scripts/run_pytest_safe.py --level all -- --durations=50`
  - suite `tests/` + metadata de marks/skip + docs historicas en `docs/test_performance/`
  - artefacto runtime `.agent/runtime/pytest-safe/last-run.json`
- shared_dependencies:
  - `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml` (read-only; contrato actual del runner y gates)
  - `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_followup.md`, `docs/test_performance/test_selection.md` (read-only; evidencia previa)
  - `tests/README.md` y `tests/ARCHITECTURE.md` (read-only; mapa de la suite)
  - frontera cerrada `011e <-> 010m <-> 011i` y cierre `013d` (read-only; no reabrir xdist ni runner)


## PLAN-013F-001 -- Poda segura de `tests/deprecated/`

- objetivo: retirar del motor los tests Goose ya deprecados y excluidos del runner, dejando evidencia durable del retiro sin tocar `pytest.ini`, el runner ni otras familias legacy.
- tickets: [WOT-2026-013f]
- depends_on: [WOT-2026-013e]
- superficies_archivo:
  - repo_motor/tests/deprecated/
  - repo_motor/tests/integration/RETIRED_TESTS.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `pytest.ini` (`norecursedirs`, read-only)
  - `python -m pytest tests --collect-only -q -p no:cacheprovider`
  - `python scripts/run_pytest_safe.py --level all`
- shared_dependencies:
  - `docs/test_performance/test_suite_audit_WOT-2026-013e.md` (read-only; origen del follow-up)
  - `scripts/cleanup_legacy.py` y `tests/unit/test_cleanup_legacy.py` (read-only; distinguir script legacy vs tests a podar)
  - `tests/test_goose_native_skill.py` y `tests/unit/test_ejemplo.py` (read-only; fuera de scope en esta ronda)


## PLAN-013G-001 -- Diagnostico reproducible de `test_upgrade_path_suggestion`

- objetivo: producir un reporte durable que explique el coste anomalo de `test_upgrade_path_suggestion` con medicion fresca y reproducible, sin tocar test, runner ni producto.
- tickets: [WOT-2026-013g]
- depends_on: [WOT-2026-013e]
- superficies_archivo:
  - repo_motor/docs/test_performance/test_upgrade_cost_WOT-2026-013g.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `python -m pytest tests/unit/test_detect_version.py -q --durations=10`
  - `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion -q --durations=10`
  - `validate --json --project-root <repo_destino>`
- shared_dependencies:
  - `docs/test_performance/test_performance_baseline.md` y `test_performance_variance.md` (read-only; evidencia historica)
  - `docs/test_performance/test_suite_audit_WOT-2026-013e.md` (read-only; origen del follow-up)
  - `tests/unit/test_detect_version.py` (read-only; superficie analizada sin modificar)

## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|--------------------|------------|---------------|
| PLAN-001 | un manifiesto nuevo en repo_destino | contratos prompt-skill y discovery del motor en lectura | inventario obsoleto si otro ticket mueve prompts/skills durante el analisis | congelar HEAD inicial y repetir inventario antes del handoff | no |
| PLAN-010D-001 | lifecycle del controller, supervisor, guard de handoff, tests y artefacto runtime `paused/*.json` | bus global, proyecciones markdown, delivery_authority=repo_motor con estado operativo en repo_destino | drift si otro ticket toca bus/controller/supervisor o si Builder intenta cerrar con una pausa activa ajena | serializar contra tickets que toquen bus/controller/supervisor; derivar estado desde bus primero; ejecutar `validate --json --project-root <repo_destino>` y `run_pytest_safe` final sobre la union | no |

| PLAN-011G-001 | prompts/documentacion de Builder/Manager/Orchestrator y Quickstart; bitacora en repo_destino | semantica canonica de suite/handoff/cierre ya fijada por tooling y memoria reciente | conflicto si otro ticket toca los mismos prompts/docs y reintroduce lenguaje ambiguo sobre evidencia diagnostica vs cierre | serializar con tickets que toquen `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md` o `QUICKSTART.md`; revalidar encoding + `validate --json` al cerrar | no |
| PLAN-010X-001 | workflow de seguridad CI + barrera de alineacion del workflow; bitacora en repo_destino | semilla portable de gitleaks, `.pre-commit-config.yaml`, historico 004a/004b | conflicto si otro ticket toca `security-audit.yml`, la politica de gitleaks o `test_hook_ci_alignment.py` mientras 010x migra el paso OSS | serializar con tickets que toquen workflow de seguridad, politica de gitleaks o la barrera de alineacion; revalidar tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-012B-001 | gate nuevo + tests + integracion en dispatcher del motor; bitacora en repo_destino | resolucion topologica del destino, contrato backlog fijado por 012a, dispatch de gates y closeout | conflicto si otro ticket toca `run_gates_dispatch.py`, cambia el schema de backlog o relaja `Reactivation`/estados mientras 012b implementa el gate | serializar con tickets que toquen backlog contract, dispatch de gates o barreras de cierre; validar siempre contra `repo_destino` real | no |
| PLAN-011B-001 | seam de timeout en relaunch (`bus/builder_relaunch.py`) + tests de supervisor; bitacora en repo_destino | `bus/supervisor.py`, eventos `BUILDER_RELAUNCH_ATTEMPTED`, cierre canonico `--level all` | conflicto si otro ticket toca relaunch/supervisor o cambia timeouts/politica de cierre mientras 011b vuelve deterministas las pruebas | serializar con tickets que toquen `bus/builder_relaunch.py`, `bus/supervisor.py` o criterios de cierre; revalidar tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-013A-001 | fixture/driver de `tests/test_controller_integration.py`; bitacora en repo_destino | `.agent/agent_controller.py` read-only, runtime/bus copiados por sandbox, cierre canonico `--level all` | conflicto si otro ticket toca el mismo test o cambia la forma de resolver project_root/topologia del controller mientras 013a arregla el fixture | serializar con tickets que toquen `tests/test_controller_integration.py` o la resolucion de project_root del controller; revalidar test aislado + archivo completo + `--level all` al cerrar | no |
| PLAN-011E-001 | opt-in xdist local en runner + lockfile/tests del motor; medicion en repo_destino | `run_pytest_safe.py`, `last-run.json`, contrato canonico de handoff, `pyproject.toml`/`uv.lock` | conflicto si otro ticket toca el runner, el lockfile o la politica de cierre/performance mientras 011e ajusta el camino local | serializar con tickets que toquen `run_pytest_safe.py`, `pyproject.toml`/`uv.lock` o criterios de handoff; revalidar `--level all` + `validate` al cerrar | no |
| PLAN-011F-001 | `.gitattributes`, launcher PS1, encoding guard y tests del motor; bitacora en repo_destino | contrato multiplataforma de `*.ps1`, evidencia 011c/011j y barreras de encoding | conflicto si otro ticket toca `launch_agent_terminals.ps1`, `.gitattributes` o el scope repo-wide del guard mientras 011f normaliza la fuente | serializar con tickets que toquen launcher, line endings o `encoding_guard.py`; revalidar `check_encoding_guard.py`, tests focales y `validate --json` al cerrar | no |
| PLAN-010M-001 | workflow `quality-gates.yml` + barrera dedicada del workflow; bitacora en repo_destino | runner xdist ya fijado por `011e`, handoff canonico `--level all`, frontera con `011i` | conflicto si otro ticket toca `quality-gates.yml`, la politica xdist o el default del runner mientras 010m introduce el piloto CI | serializar con tickets que toquen `quality-gates.yml`, `scripts/run_pytest_safe.py` o la politica xdist/default; revalidar tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-011H-001 | `mark-ready` en `.agent/agent_controller.py` + barreras de handoff/guard; bitacora en repo_destino | razon estable `archive_rename_uncommitted`, auto-archivado de plan/audit, cierre canonico `--level all` | conflicto si otro ticket toca `--mark-ready`, `pre_handoff_guard`, auto-archivado o contrato de cierres mientras 011h endurece el handoff | serializar con tickets que toquen `.agent/agent_controller.py`, `scripts/pre_handoff_guard.py`, `tests/test_agent_controller.py` o `tests/test_pre_handoff_guard.py`; revalidar tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-013B-002 | [CANCELADO/ABSORBED] sin superficie operativa | n/a (absorbido por PLAN-011I-001) | n/a -- premisa refutada (ver `CG-WOT-2026-013b.md`); no se planifica | ninguna; la deuda real (politica de reparto) la lleva PLAN-011I-001 | n/a |
| PLAN-011I-001 | [NOT-PURSUED] sin superficie operativa | n/a (default xdist no perseguido; ver `CG-WOT-2026-011i.md`) | n/a -- premisa loadscope refutada; opt-in 011e+010m es el estado final | ninguna; follow-up opcional = robustecer 3 tests global-state (no contratado) | n/a |
| PLAN-013C-001 | [BLOCKED-FINAL] sin superficie operativa | n/a (cura en producto; ver `CG-WOT-2026-013c.md`) | n/a -- la cura toca rglob de producto o rompe invariante sandbox; tests-only no basta | ninguna; sucesor = ticket de producto (escaneo robusto a borrados concurrentes) | n/a |
| PLAN-013D-001 | product scanner/project_paths + tests focales/fixture de sandbox; bitacora en repo_destino | `tests/sandbox/test_runtime` volatil, runner xdist read-only, invariante sandbox-dentro | conflicto si otro ticket toca `project_scanner`, `project_paths`, `tests/conftest.py` o reabre la politica xdist/default mientras 013d endurece el escaneo | serializar con tickets que toquen escaneo de proyecto, fixture de sandbox o politica xdist; revalidar triple xdist x3 + tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-013E-001 | reporte durable en repo_motor + bitacora en repo_destino | docs de performance previas, runner read-only, frontera xdist cerrada, suite `tests/` | conflicto si otro ticket toca `docs/test_performance/`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml` o reabre xdist/default mientras 013e clasifica valor/poda | serializar con tickets que toquen runner/gates/docs de performance; repetir inventario contra el HEAD final y revalidar `validate --json --project-root <repo_destino>` | no |
| PLAN-013F-001 | retiro de `tests/deprecated/` + actualizacion de `tests/integration/RETIRED_TESTS.md`; bitacora en repo_destino | contrato `pytest.ini` read-only, follow-up `013e`, evidencia canonica `run_pytest_safe` | conflicto si otro ticket toca `pytest.ini`, `tests/integration/RETIRED_TESTS.md` o revive Goose/otros candidatos legacy mientras 013f poda el directorio excluido | serializar con tickets que toquen el runner, el ledger de tests retirados o el historico Goose; revalidar collect-only 3111 + `python scripts/run_pytest_safe.py --level all` + `validate --json --project-root <repo_destino>` | no |
| PLAN-013G-001 | reporte durable en repo_motor + bitacora en repo_destino | historial 010j/010p/013e, test focal read-only, validate canonico | conflicto si otro ticket toca `tests/unit/test_detect_version.py`, docs de performance o reabre la discusion como fix de codigo mientras 013g sigue siendo analisis | serializar con tickets que toquen ese test o docs de performance; revalidar mediciones y `validate --json --project-root <repo_destino>` al cerrar | no |
| PLAN-013H-001 | archivador/cierre canonico + barreras de git real; bitacora en repo_destino | detector `archive_rename_uncommitted`, historico 011a/011h, `session_closeout.py` y reconcile solo de lectura | conflicto si otro ticket toca `archive_collaboration_artifacts.py`, `session_closeout.py`, `tests/test_archive_collaboration_artifacts.py` o `tests/test_session_closeout.py` mientras 013h cambia la semantica del archivado | serializar con tickets que toquen closeout/archivado; revalidar pruebas focales con repo git real + `python scripts/run_pytest_safe.py --level all` + `validate --json --project-root <repo_destino>` | no |
| PLAN-013I-001 | higiene de sandbox en `tests/conftest.py` + barreras de scanner/runtime; bitacora en repo_destino | atribucion 013g, cura de producto 013d read-only, triple xdist heredado, `run_pytest_safe` read-only | conflicto si otro ticket toca `tests/conftest.py`, barreras de sandbox o reabre `project_scanner`/`project_paths`/politica xdist mientras 013i acota el purge | serializar con tickets que toquen la higiene de sandbox o las barreras heredadas; revalidar focales + triple xdist x3 + `python scripts/run_pytest_safe.py --level all` + `validate --json --project-root <repo_destino>` al cerrar | no |
| PLAN-013J-001 | gate del backlog + tests + regla de pipeline sobre autoridad del FLT; bitacora en repo_destino | backlog vivo del destino, contrato frozen, scope gate/handoff read-only | conflicto si otro ticket toca `check_backlog_contract.py`, `prompts/orchestrator_pipeline.md`, el schema de backlog o la semantica de FLT/contract authority mientras 013j cierra la duplicidad | serializar con tickets que toquen backlog contract o la regla de autoridad del FLT; revalidar tests del gate + `python scripts/run_pytest_safe.py --level all` + `validate --json --project-root <repo_destino>` al cerrar | no |
parallelism_notes: 008a debe ejecutarse en exclusiva respecto de cualquier ticket
que mueva o renombre prompts, skills, manifests o discovery. 010d debe ejecutarse
en exclusiva respecto de cualquier ticket que toque bus, controller, supervisor,
state projection, pre-handoff o lifecycle runtime.

## Forbidden Surfaces por plan

- PLAN-001: todo el repo_motor es read-only; no tocar prompts/, skills/, scripts/,
  tests/, MANIFEST.*, AGENTS.md, PROJECT.md, QUICKSTART.md ni llms*.txt.
- PLAN-010D-001: no tocar `privada/`, `.env`, `.agent/runtime/memory/`, tickets
  010e/010f/010g/010h/010i/008d ni documentacion general (`QUICKSTART.md`,
  `INTERACTION_MODES.md`) en v1.
- No tocar bus/controller/runtime del destino salvo proyecciones producidas por
  el controller.

- PLAN-013E-001: no tocar `tests/`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml`, `uv.lock`, CI/workflows ni `scripts/run_gates_dispatch.py`; no borrar, `xfail`, `skip` ni relajar tests; no reabrir `011e`, `010m`, `011i` ni `013d`.
- PLAN-013F-001: no tocar `pytest.ini`, `scripts/run_pytest_safe.py`, `scripts/cleanup_legacy.py`, `tests/test_goose_native_skill.py`, `tests/unit/test_ejemplo.py`, CI/workflows ni producto fuera de `tests/deprecated/` y `tests/integration/RETIRED_TESTS.md`.
- PLAN-013G-001: no tocar `tests/unit/test_detect_version.py`, producto Python, `scripts/run_pytest_safe.py`, `pytest.ini`, CI/workflows ni superficies fuera del reporte y `execution_log.md`.
- PLAN-013H-001: no auto-commitear artefactos historicos desde el archivador; no relajar `archive_rename_uncommitted`; no tocar `scripts/run_pytest_safe.py`, CI/workflows, `privada/` ni tickets cerrados fuera de la familia de closeout/archivado.

## Merge Regression Audit

No hay merge productivo en 008a. Antes de cerrar, repetir el inventario contra el
mismo HEAD o registrar el nuevo HEAD y reconciliar cualquier drift. Los tickets
posteriores deben ejecutar discovery, collision check, contract check y suite
completa sobre la union de cambios.

Para 010d, cualquier merge con otro ticket que toque bus/controller/supervisor
requiere revalidar la union con `run_pytest_safe`, `validate --json --project-root <repo_destino>`
y una auditoria especifica de secuencias/eventos de pausa y resume.

Para 010m, cualquier merge con tickets que toquen `quality-gates.yml`, `scripts/run_pytest_safe.py` o la politica de xdist/default exige revalidar la union con `python -m pytest tests/unit/test_quality_gates_workflow.py -q`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 011b, cualquier merge con tickets que toquen `bus/builder_relaunch.py`, `bus/supervisor.py` o la politica de cierre/performance obliga a revalidar la union con tests focales de relaunch, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 013a, cualquier merge con tickets que toquen `tests/test_controller_integration.py` o la resolucion de `project_root` del controller obliga a revalidar el test aislado, el archivo completo y `python scripts/run_pytest_safe.py --level all`.
Para 011g, cualquier merge con tickets que toquen `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md` o `QUICKSTART.md` obliga a revalidar la coherencia textual de `loop rapido` vs `cierre canonico`, `check_encoding_guard.py` sobre los docs tocados y `validate --json --project-root <repo_destino>`.
Para 010x, cualquier merge con tickets que toquen `.github/workflows/security-audit.yml`, `tests/unit/test_hook_ci_alignment.py` o la politica/config de gitleaks obliga a revalidar la union con `python -m pytest tests/unit/test_hook_ci_alignment.py -v`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 011h, cualquier merge con tickets que toquen `.agent/agent_controller.py`, `scripts/pre_handoff_guard.py`, `tests/test_agent_controller.py` o `tests/test_pre_handoff_guard.py` obliga a revalidar la union con tests focales de handoff/archivado, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 013b, cualquier merge con tickets que toquen `tests/unit/test_project_root_resolution.py`, `scripts/run_pytest_safe.py` o `runtime/project_root.py` obliga a revalidar la union con `python scripts/run_pytest_safe.py --level unit --xdist-workers auto`, `python -m pytest tests/unit -q`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 011i, cualquier merge con tickets que toquen `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `quality-gates.yml` o la politica xdist/default obliga a revalidar la union con tests focales del runner, `python scripts/run_pytest_safe.py --level unit`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Nota historica 013c (BLOCKED-FINAL, ver `CG-WOT-2026-013c.md`): el aislamiento tests-only no era viable; la cura pertenece a un ticket de producto (rglob robusto a borrados concurrentes). No hay plan activo de 013c que serializar.
Para 013d, cualquier merge con tickets que toquen `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`, `tests/conftest.py` o la politica de xdist/default obliga a revalidar la union con el triple xdist (`test_upgrade_path_suggestion`, `test_scan_current_project`, `test_no_inline_ticket_regex`) en 3 corridas consecutivas, los tests focales de scanner/project_paths, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 013e, cualquier merge con tickets que toquen `docs/test_performance/`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml` o la politica xdist/default obliga a revalidar la union con el inventario final contra el HEAD mergeado, `python scripts/check_encoding_guard.py docs/test_performance/test_suite_audit_WOT-2026-013e.md` y `validate --json --project-root <repo_destino>`.
Para 013f, cualquier merge con tickets que toquen `pytest.ini`, `tests/integration/RETIRED_TESTS.md`, `tests/test_goose_native_skill.py` o candidatos legacy vecinos obliga a revalidar la union con `python -m pytest tests --collect-only -q -p no:cacheprovider`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 013g, cualquier merge con tickets que toquen `tests/unit/test_detect_version.py`, `docs/test_performance/` o la politica del runner obliga a revalidar la union con medicion fresca comparable y `validate --json --project-root <repo_destino>`.
Para 013h, cualquier merge con tickets que toquen `scripts/archive_collaboration_artifacts.py`, `scripts/session_closeout.py`, `scripts/closeout_steps/archival.py`, `tests/test_archive_collaboration_artifacts.py` o `tests/test_session_closeout.py` obliga a revalidar la union con las pruebas focales de archivado/cierre sobre repo git real, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.


## PLAN-013H-001 -- Cierre sin limbo del archivado canonico

- objetivo: eliminar la herencia recurrente de `archive_rename_uncommitted` en la ruta real de archivado/cierre, sin auto-commitear historicos y sin relajar las barreras fail-closed existentes.
- tickets: [WOT-2026-013h]
- depends_on: [WOT-2026-011h, WOT-2026-013g]
- superficies_archivo:
  - repo_motor/scripts/archive_collaboration_artifacts.py
  - repo_motor/scripts/closeout_steps/archival.py
  - repo_motor/scripts/session_closeout.py
  - repo_motor/tests/test_archive_collaboration_artifacts.py
  - repo_motor/tests/test_session_closeout.py
  - repo_motor/tests/test_agent_controller.py
  - repo_motor/tests/test_pre_handoff_guard.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `archive_collaboration_artifacts.py`
  - `session_closeout.py`
  - `scripts.closeout_steps.archival.step_archive_collaboration()`
  - razon estable `archive_rename_uncommitted`
- shared_dependencies:
  - `scripts/delivery_hygiene_check.py` (read-only; detector canonico del limbo)
  - `.agent/agent_controller.py` y `--mark-ready` (read-only salvo evidencia contraria; `011h` ya cubrio ese frente)
  - `scripts/reconcile_ticket.py` (read-only; herramienta de recuperacion, no cierre normal)

## PLAN-013I-001 -- Higiene de purge de sandbox para latencia operacional

- objetivo: reducir o acotar la latencia operacional del purge de sandboxes huerfanos en `tests/conftest.py`, manteniendo la higiene defensiva de `013d` y sin tocar producto, runner, CI ni la politica xdist/default.
- tickets: [WOT-2026-013i]
- depends_on: [WOT-2026-013d, WOT-2026-013g]
- superficies_archivo:
  - repo_motor/tests/conftest.py
  - repo_motor/tests/unit/test_project_scanner.py
  - repo_motor/tests/unit/test_windows_safe_temp_runtime.py
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - `tests.conftest::_purge_orphan_session_dirs()`
  - fixture `tests.conftest::_project_temp_environment()`
  - `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load`
- shared_dependencies:
  - `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` (read-only; atribucion verificada del coste)
  - `scripts/project_scanner.py` y `agent_system/scripts/project_paths.py` (read-only; cura de producto ya cerrada por `013d`)
  - `tests/unit/test_detect_version.py` y `tests/unit/test_no_inline_ticket_regex.py` (read-only; barreras de no-regresion heredadas)
  - `scripts/run_pytest_safe.py` y politica `011e <-> 010m <-> 011i` (read-only; frontera cerrada)

- PLAN-013I-001: no tocar `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`, `tests/unit/test_detect_version.py`, `tests/unit/test_no_inline_ticket_regex.py`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml`, `uv.lock`, CI/workflows ni la politica xdist/default cerrada por `011e`, `010m`, `011i`.

Para 013i, cualquier merge con tickets que toquen `tests/conftest.py`, `tests/unit/test_project_scanner.py`, `tests/unit/test_windows_safe_temp_runtime.py`, `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py` o la politica xdist/default obliga a revalidar la union con los focales de sandbox, el triple xdist en 3 corridas consecutivas, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.

## PLAN-013J-001 -- Una sola fuente de verdad para FLT en backlog vs contrato

- objetivo: eliminar la deriva entre el FLT de las fichas detalladas de `backlog.md` y el contrato frozen, reforzando la validacion del backlog y explicitando la autoridad del contrato/work_plan sin tocar scope gate ni handoff.
- tickets: [WOT-2026-013j]
- depends_on: []
- superficies_archivo:
  - repo_motor/scripts/check_backlog_contract.py
  - repo_motor/tests/unit/test_check_backlog_contract.py
  - repo_motor/prompts/orchestrator_pipeline.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - CLI `scripts/check_backlog_contract.py --project-root <repo_destino>`
  - `repo_destino/.agent/collaboration/backlog.md` (fichas detalladas)
  - contrato frozen `repo_destino/.agent/planning/ticket_contracts.md`
  - `work_plan.md` como proyeccion activa del contrato
- shared_dependencies:
  - `.agent/scope_gate.py` y `scripts/pre_handoff_guard.py` (read-only; autoridad del FLT y cierre fail-closed)
  - `skills/manager-create-work-plan/SKILL.md` y `prompts/audit_cf_ticket_contract.md` (read-only; contexto de generacion/contrato)
  - `backlog.md` del destino como cola viva, no como segunda fuente de verdad del packet

- PLAN-013J-001: no tocar `.agent/scope_gate.py`, `scripts/pre_handoff_guard.py`, `.agent/agent_controller.py`, `scripts/check_deliverables_exist.py`, CI/workflows, `privada/` ni convertir `backlog.md` en autoridad paralela del FLT.

Para 013j, cualquier merge con tickets que toquen `scripts/check_backlog_contract.py`, `tests/unit/test_check_backlog_contract.py`, `prompts/orchestrator_pipeline.md`, el schema de `backlog.md` o la semantica de FLT/contract authority obliga a revalidar la union con `python -m pytest tests/unit/test_check_backlog_contract.py -q -p no:cacheprovider`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
