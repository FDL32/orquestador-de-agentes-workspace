# STRATEGY_WOT-2026-010d

## Contexto verificado

- `bus/state_machine.py:TicketState` NO contiene `PAUSED` hoy.
- `.agent/state_validation.py:VALID_LOG_STATES` NO acepta `PAUSED` hoy.
- `.agent/agent_controller.py` ya tiene un patron real de recuperacion por flag: `_handle_resume_human_gate()`.
- `.agent/agent_controller.py::_get_event_bus()` y `bus/event_bus.py:EventBus.emit()` ya cubren la emision canonica y el control de secuencias.
- `scripts/pre_handoff_guard.py` hoy no inspecciona `paused/` ni diagnosticos `paused_ticket_*`.
- `bus/supervisor.py` y `bus/builder_locks.py` enumeran estados explicitos; si no se actualizan, `PAUSED` quedara fuera de la logica de liveness/relaunch.
- `runtime/ui_state_projector.py` deriva el ticket activo desde supervisor, work_plan y TURN; puede necesitar ajuste si queremos que la UI refleje `PAUSED` de forma explicita.
- `STATE.md` sigue en `WOT-2026-010c / COMPLETED`; esto es pre-arranque, no un bug de implementacion de 010d. El bootstrap al bus ocurre despues de esta fase.

## Decision register

| Decision | Tier | Estado | Nota |
|----------|------|--------|------|
| DEC-010D-001 | T1a | accepted | bus como autoridad de lectura |
| DEC-010D-002 | T1a | accepted | una sola pausa activa en v1 |
| DEC-010D-003 | T1a | accepted | conservar `ACTIVE_TICKET` |
| DEC-010D-004 | T2 | accepted | `stash_ref=null` si no hay diff |

## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|--------------------|------------|---------------|
| PLAN-010D-001 | controller, state machine, supervisor, pre-handoff, tests, artefacto `paused/*.json` | bus global, proyecciones markdown, multi-root `repo_motor + repo_destino`, `delivery_authority=repo_motor` | drift si otro ticket toca bus/controller; packaging sucio si la pausa ajena queda activa; confusion de root si el artefacto se escribe fuera de `repo_destino` | serializar contra tickets de bus/controller; resolver `project-root` explicitamente; validar con `--project-root <repo_destino>`; bloquear `mark-ready` si existe pausa activa ajena o corrupta | no |

## Enfoque recomendado

1. **TDD primero**
   - Crear `tests/unit/test_pause_ticket.py` y `tests/unit/test_resume_ticket.py`.
   - Reusar `tmp_path`, fixtures de bus y patrones de los tests de `manager-approve`, `mark-ready` y `pre_handoff_guard` ya existentes.
   - Incluir una barrera real para el corte de sesion: pausa, nueva instancia, deteccion de pausa activa y bloqueo de handoff.
   - Anadir al menos un test explicito para `--abort-paused-ticket` fail-closed o stub auditable.

2. **Estado y validacion primero, antes del CLI**
   - Anadir `PAUSED` en `bus/state_machine.py:TicketState` y ajustar `is_work_state()` para tratarlo como estado no terminal.
   - Anadir `PAUSED` a `.agent/state_validation.py:VALID_LOG_STATES`.
   - Revisar lectores de estado en `bus/supervisor.py` y `bus/builder_locks.py` para que no clasifiquen `PAUSED` como desconocido o terminal.

3. **Persistencia canonica de la pausa**
   - En `.agent/agent_controller.py`, introducir helpers pequenos y probables: `_paused_dir()`, `_pause_artifact_path(ticket_id)`, `_load_pause_artifact()`, `_write_pause_artifact()` y `_collect_pause_git_snapshot()`.
   - El JSON debe escribirse en `repo_destino/.agent/collaboration/paused/`.
   - Guardar `bus_last_seq_global` desde el ultimo evento del bus y `ticket_last_seq` desde el ultimo evento del ticket pausado.
   - La mitigacion multi-root concreta es: codigo en `repo_motor`, artefacto en `repo_destino`, y todas las validaciones operativas ejecutadas con `--project-root <repo_destino>`.

4. **Flags CLI**
   - Implementar `--pause-ticket` y `--resume-ticket` siguiendo el patron de `_handle_resume_human_gate()` para validaciones, salida JSON y stderr.
   - Implementar `--abort-paused-ticket` como camino completo o como stub fail-closed con diagnostico auditable y schema `ABORTED` persistente.

5. **Guardas de packaging y relaunch**
   - `scripts/pre_handoff_guard.py` debe bloquear cuando exista una pausa activa ajena o un JSON corrupto.
   - `agent_controller --validate` debe emitir diagnosticos especificos `paused_ticket_active` / `paused_ticket_corrupt`, no un fallo opaco.

6. **Proyecciones y UX minima**
   - Confirmar la proyeccion de `TURN.md` durante la pausa y dejarla fijada en el mismo camino canonico que actualiza `STATE.md`.
   - `runtime/ui_state_projector.py` solo se toca cuando la UI no refleje bien `PAUSED` o recomiende archivos incorrectos.

## Riesgos a vigilar

- **Dirty tree parcial:** si la restauracion falla y deja cambios a medias, rompe el contrato principal del ticket.
- **Reentry del mismo ticket:** un evento posterior del ticket pausado invalida el resume; no se puede ignorar.
- **Compatibilidad multi-root:** el artefacto vive en `repo_destino`, pero el diff productivo de 010d vive en `repo_motor`; la implementacion debe respetar `delivery_authority=repo_motor` sin perder el `project-root` operativo.
- **Falso verde de tests:** no basta con comprobar que existe el JSON; los tests deben verificar contenido util (`changed_paths`, `diff_stat`, seqs, bloqueo real en pre-handoff, abort fail-closed).

## Gates sugeridos para Builder

- `python -m pytest tests/unit/test_pause_ticket.py tests/unit/test_resume_ticket.py tests/test_pre_handoff_guard.py`
- `python scripts/run_pytest_safe.py --project-root <repo_destino>`
- `ruff check .`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`