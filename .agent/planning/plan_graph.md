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

