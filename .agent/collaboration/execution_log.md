# Execution Log -- WOT-2026-013n

**Estado:** READY_FOR_REVIEW

## MANAGER - WOT-2026-013n - Bootstrap operativo

Ticket activado para limpiar la deuda estructural de terminalidad honesta no-exito del motor, sin falsear `COMPLETED` para `WT-2026-239a` ni `WOT-2026-013c`.

Packet activo en repo_destino:
- `OBJ-013N-001` en `repo_charter.md`
- `PLAN-013N-001` en `plan_graph.md`
- `T-013N-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013n.md` y `AUDIT_WOT-2026-013n.md` activos para Builder

Premisa operativa del Builder:
- releer `events.jsonl` y la evidencia viva de `WT-2026-239a` / `WOT-2026-013c`
- localizar todas las listas locales de terminalidad antes de tocar codigo
- centralizar la autoridad en `state_machine` o helper equivalente, sin mapear a `COMPLETED`
- preservar intacto el camino `READY_TO_CLOSE -> COMPLETED -> SUPERVISOR_CLOSED`

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `222da77`
- repo_destino HEAD = `f063692`
- `validate --json --project-root <repo_destino>` = `0 errors / 0 warnings`
- evidencia disparadora: `WT-2026-239a` sigue con bus historico en `READY_FOR_REVIEW` pese a supersession honesta; `WOT-2026-013c` vive como `BLOCKED-FINAL` contractual; hoy `state_machine`, `reconcile_ticket`, `preflight_reconcile`, `archive_event_bus`, `session_closeout`, `get_launcher_state` y `check_destino_publish_ready` no comparten autoridad para esos finales no-exito


## WOT-2026-013n - Fase 0 (diagnostico)

Preflight: validate 0/0; STATE/work_plan/TURN apuntan a WOT-2026-013n; deliverable_type=code.

Seams confirmados (autoridad de terminalidad fragmentada hoy):
- bus/state_machine.py:35 `is_approved_or_terminal` -> solo COMPLETED.
- bus/state_machine.py:106 `NON_TERMINAL_STATES` (modulo) -> 7 estados.
- bus/supervisor.py:75 redeclara `NON_TERMINAL_STATES` local DIVERGENTE (6 estados; le falta CONTRACT_BLOCKED frente al del state_machine).
- scripts/reconcile_ticket.py:46 `TERMINAL_STATES = {"COMPLETED","CLOSED"}` (CLOSED literal legacy).
- scripts/preflight_reconcile.py:142 `{"COMPLETED","CLOSED"}` literal.
- scripts/archive_event_bus.py:45 `TERMINAL_STATES = {"COMPLETED","HUMAN_GATE"}`.
- scripts/session_closeout.py:89 `TERMINAL_STATES = {"COMPLETED","HUMAN_GATE"}`.
- scripts/closeout_steps/archival.py:194 `to_state == "COMPLETED"` literal.
- scripts/get_launcher_state.py:92 turn_map: solo COMPLETED -> (MANAGER, CREATE_PLAN, COMPLETED).
- scripts/check_destino_publish_ready.py:45 `_PUBLISHABLE_STATUSES` incluye COMPLETED.
- bus/builder_locks.py:27 `RELAUNCH_BLOCKED_STATES` -> HUMAN_GATE, READY_TO_CLOSE, COMPLETED.

Hallazgos:
- CLOSED vive SOLO como literal suelto en reconcile_ticket/preflight_reconcile; NO esta en el enum TicketState. Se mantiene como legado absorbido por la autoridad, sin promocionarlo a estado canonico.
- WT-2026-239a: bus en READY_FOR_REVIEW + MANAGER_REVIEW_WT-2026-239a.md "no apruebo" (supersession honesta, no trabajo incompleto). VERIFICADO EN BUS.
- WOT-2026-013c: blocked-final contractual (CONTRACT_GAP), follow-up = producto nuevo. VERIFICADO EN DOCUMENTACION.
- No aparece necesidad de ABANDONED -> sin CONTRACT_GAP, scope se mantiene.

Por que bus/ y supervisor.py siguen dentro de FLT: supervisor.py:75 mantiene una lista local divergente de no-terminalidad que DEBE consumir la autoridad compartida (criterio binario explicito); sin tocarla, el fix quedaria a medias (medio-fix prohibido por STRATEGY).

Decision: autoridad unica en state_machine.py (IRREVERSIBLE_TERMINAL_STATES + helper is_terminal_state que absorbe CLOSED legacy). Consumidores convergen en ella.

## WOT-2026-013n - Fase 1/2 (implementacion + tests)

Autoridad compartida en bus/state_machine.py:
- enum TicketState += SUPERSEDED, BLOCKED_FINAL (irreversibles, no-exito).
- IRREVERSIBLE_TERMINAL_STATES = {COMPLETED, SUPERSEDED, BLOCKED_FINAL} (fuente unica).
- NON_SUCCESS_TERMINAL_STATES = {SUPERSEDED, BLOCKED_FINAL}.
- is_terminal_state(state|str|None) helper; absorbe literal legacy "CLOSED" sin meterlo al enum.
- terminal_state_strings(include_legacy=) para consumidores string-based.
- is_approved_or_terminal consulta IRREVERSIBLE_TERMINAL_STATES.
- CLOSED queda como _LEGACY_TERMINAL_LITERALS, NO promocionado a TicketState.
- READY_TO_CLOSE sigue no-terminal; COMPLETED sigue cierre de exito.

Consumidores convergidos en la autoridad:
- bus/supervisor.py: elimina NON_TERMINAL_STATES local divergente, importa la canonica (corrige bug latente: la local omitia CONTRACT_BLOCKED).
- bus/builder_locks.py: RELAUNCH_BLOCKED_STATES |= NON_SUCCESS_TERMINAL_STATES.
- scripts/reconcile_ticket.py: TERMINAL_STATES = terminal_state_strings() (incluye CLOSED legacy).
- scripts/preflight_reconcile.py: _terminal_state delega en is_terminal_state.
- scripts/archive_event_bus.py + session_closeout.py: TERMINAL_STATES = terminal_state_strings() | {HUMAN_GATE} (HUMAN_GATE preservado como close de escalada propio del archivado).
- scripts/closeout_steps/archival.py: _bus_confirms_close usa is_terminal_state(to_state).
- scripts/get_launcher_state.py: turn_map + _role_action_for_state mapean SUPERSEDED/BLOCKED_FINAL a (MANAGER, CREATE_PLAN) -> lado terminal.
- scripts/check_destino_publish_ready.py: _PUBLISHABLE_STATUSES += SUPERSEDED, BLOCKED_FINAL.

Tests:
- tests/unit/test_terminal_states.py (NUEVO, 16 tests): FAIL-sin/PASS-con para SUPERSEDED y BLOCKED_FINAL en la autoridad; CLOSED reconocido como literal pero NO enum; READY_TO_CLOSE no-terminal; derive_state_from_events mapea los nuevos; reconcile TERMINAL_STATES incluye autoridad.
- tests/test_launcher_state_from_bus.py (EXT): ambos estados -> MANAGER/CREATE_PLAN (lado terminal del launcher), no BUILDER.
- tests/evals/test_eval_requeue.py (EXT): ambos en RELAUNCH_BLOCKED_STATES, no en NON_TERMINAL_STATES, requeue_ticket los bloquea.

Barrera FAIL-sin/PASS-con: confirmada (pre-fix is_terminal solo COMPLETED -> SUPERSEDED/BLOCKED_FINAL no-terminal -> test_new_states_are_terminal habria fallado).

Gates (comandos exactos, exit codes):
- python -m pytest tests/unit/test_terminal_states.py tests/test_launcher_state_from_bus.py tests/evals/test_eval_requeue.py -q -p no:cacheprovider -> 42 passed, exit 0.
- uv run ruff check <13 archivos FLT> -> All checks passed!, exit 0.
- uv run ruff format --check <13 archivos> -> 13 files already formatted, exit 0.
- python scripts/run_pytest_safe.py --level all -> 3122 passed, 20 skipped, exit 0.
- validate --json --project-root <repo_destino> -> 0 errors / 0 warnings.

Por que 239a y 013c ya no requieren COMPLETED para verse terminales:
- WT-2026-239a puede reconciliarse a SUPERSEDED (terminal honesto): launcher lo manda a MANAGER/CREATE_PLAN, builder_locks bloquea relaunch, archive/closeout lo archivan, publish lo acepta -- sin falsear exito.
- WOT-2026-013c puede declararse BLOCKED_FINAL con identico tratamiento terminal.
- La reconciliacion real de 239a/013c a sus nuevos estados es paso POSTERIOR del Manager; este ticket solo entrega el modelo + barreras, no fabrica esos eventos.

CLOSED como legado no-enum: es_terminal_state("CLOSED")=True via _LEGACY_TERMINAL_LITERALS; "CLOSED" not in TicketState.__members__ (test lo verifica).
