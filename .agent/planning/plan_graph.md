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

## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|--------------------|------------|---------------|
| PLAN-001 | un manifiesto nuevo en repo_destino | contratos prompt-skill y discovery del motor en lectura | inventario obsoleto si otro ticket mueve prompts/skills durante el analisis | congelar HEAD inicial y repetir inventario antes del handoff | no |
| PLAN-010D-001 | lifecycle del controller, supervisor, guard de handoff, tests y artefacto runtime `paused/*.json` | bus global, proyecciones markdown, delivery_authority=repo_motor con estado operativo en repo_destino | drift si otro ticket toca bus/controller/supervisor o si Builder intenta cerrar con una pausa activa ajena | serializar contra tickets que toquen bus/controller/supervisor; derivar estado desde bus primero; ejecutar `validate --json --project-root <repo_destino>` y `run_pytest_safe` final sobre la union | no |

| PLAN-012B-001 | gate nuevo + tests + integracion en dispatcher del motor; bitacora en repo_destino | resolucion topologica del destino, contrato backlog fijado por 012a, dispatch de gates y closeout | conflicto si otro ticket toca `run_gates_dispatch.py`, cambia el schema de backlog o relaja `Reactivation`/estados mientras 012b implementa el gate | serializar con tickets que toquen backlog contract, dispatch de gates o barreras de cierre; validar siempre contra `repo_destino` real | no |
| PLAN-011B-001 | seam de timeout en relaunch (`bus/builder_relaunch.py`) + tests de supervisor; bitacora en repo_destino | `bus/supervisor.py`, eventos `BUILDER_RELAUNCH_ATTEMPTED`, cierre canonico `--level all` | conflicto si otro ticket toca relaunch/supervisor o cambia timeouts/politica de cierre mientras 011b vuelve deterministas las pruebas | serializar con tickets que toquen `bus/builder_relaunch.py`, `bus/supervisor.py` o criterios de cierre; revalidar tests focales + `--level all` + `validate` al cerrar | no |
| PLAN-013A-001 | fixture/driver de `tests/test_controller_integration.py`; bitacora en repo_destino | `.agent/agent_controller.py` read-only, runtime/bus copiados por sandbox, cierre canonico `--level all` | conflicto si otro ticket toca el mismo test o cambia la forma de resolver project_root/topologia del controller mientras 013a arregla el fixture | serializar con tickets que toquen `tests/test_controller_integration.py` o la resolucion de project_root del controller; revalidar test aislado + archivo completo + `--level all` al cerrar | no |
| PLAN-011E-001 | opt-in xdist local en runner + lockfile/tests del motor; medicion en repo_destino | `run_pytest_safe.py`, `last-run.json`, contrato canonico de handoff, `pyproject.toml`/`uv.lock` | conflicto si otro ticket toca el runner, el lockfile o la politica de cierre/performance mientras 011e ajusta el camino local | serializar con tickets que toquen `run_pytest_safe.py`, `pyproject.toml`/`uv.lock` o criterios de handoff; revalidar `--level all` + `validate` al cerrar | no |
| PLAN-011F-001 | `.gitattributes`, launcher PS1, encoding guard y tests del motor; bitacora en repo_destino | contrato multiplataforma de `*.ps1`, evidencia 011c/011j y barreras de encoding | conflicto si otro ticket toca `launch_agent_terminals.ps1`, `.gitattributes` o el scope repo-wide del guard mientras 011f normaliza la fuente | serializar con tickets que toquen launcher, line endings o `encoding_guard.py`; revalidar `check_encoding_guard.py`, tests focales y `validate --json` al cerrar | no |
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
Para 012b, cualquier merge con tickets que toquen `run_gates_dispatch.py`, el
schema del backlog o reglas de `Reactivation` obliga a revalidar la union con
tests del gate, `run_pytest_safe` si aplica y `validate --json --project-root <repo_destino>`.
Para 011b, cualquier merge con tickets que toquen `bus/builder_relaunch.py`, `bus/supervisor.py` o la politica de cierre/performance obliga a revalidar la union con tests focales de relaunch, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>`.
Para 013a, cualquier merge con tickets que toquen `tests/test_controller_integration.py` o la resolucion de `project_root` del controller obliga a revalidar el test aislado, el archivo completo y `python scripts/run_pytest_safe.py --level all`.
