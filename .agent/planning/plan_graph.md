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
## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|--------------------|------------|---------------|
| PLAN-001 | un manifiesto nuevo en repo_destino | contratos prompt-skill y discovery del motor en lectura | inventario obsoleto si otro ticket mueve prompts/skills durante el analisis | congelar HEAD inicial y repetir inventario antes del handoff | no |
| PLAN-010D-001 | lifecycle del controller, supervisor, guard de handoff, tests y artefacto runtime `paused/*.json` | bus global, proyecciones markdown, delivery_authority=repo_motor con estado operativo en repo_destino | drift si otro ticket toca bus/controller/supervisor o si Builder intenta cerrar con una pausa activa ajena | serializar contra tickets que toquen bus/controller/supervisor; derivar estado desde bus primero; ejecutar `validate --json --project-root <repo_destino>` y `run_pytest_safe` final sobre la union | no |

| PLAN-012B-001 | gate nuevo + tests + integracion en dispatcher del motor; bitacora en repo_destino | resolucion topologica del destino, contrato backlog fijado por 012a, dispatch de gates y closeout | conflicto si otro ticket toca `run_gates_dispatch.py`, cambia el schema de backlog o relaja `Reactivation`/estados mientras 012b implementa el gate | serializar con tickets que toquen backlog contract, dispatch de gates o barreras de cierre; validar siempre contra `repo_destino` real | no |
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
