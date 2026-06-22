# work_plan.md -- WOT-2026-013n
## Metadata
- **ID:** WOT-2026-013n
- **Contract ID:** T-013N-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Modelar `SUPERSEDED` y `BLOCKED_FINAL` como estados terminales honestos del runtime para que validadores, vistas, closeout y publication checks no exijan falsear `COMPLETED` en tickets como `WT-2026-239a` y `WOT-2026-013c`.
## Non-goals
- No reescribir el lifecycle exitoso `READY_TO_CLOSE -> COMPLETED -> SUPERVISOR_CLOSED`.
- No tocar `.agent/agent_controller.py`, CI/workflows ni editar `events.jsonl` a mano.
- No introducir `ABANDONED` salvo que Fase 0 demuestre con evidencia que el contrato quedaria roto sin un tercer estado.
- No reconciliar tickets reales a `COMPLETED` solo para silenciar vistas.
## Premisas verificadas antes de Builder
- `bus/state_machine.py` sigue tratando `COMPLETED` como unica terminalidad irreversible explicita; el string legacy `CLOSED` existe solo como literal suelto fuera del enum y no debe promocionarse a nuevo estado canonico.
- `scripts/archive_event_bus.py`, `scripts/reconcile_ticket.py`, `scripts/preflight_reconcile.py`, `scripts/session_closeout.py`, `scripts/check_destino_publish_ready.py` y `scripts/get_launcher_state.py` contienen hoy heuristicas locales de terminalidad o publicabilidad que no reconocen `SUPERSEDED`/`BLOCKED_FINAL`.
- `WT-2026-239a` conserva evidencia honesta de rechazo y supersession; no es trabajo incompleto a rescatar.
- `WOT-2026-013c` esta declarado `BLOCKED-FINAL` en planning; el follow-up correcto es producto nuevo, no reabrir el ticket tests-only.
## Decision Arquitectonica
`013n` es un ticket `code` del motor sobre la semantica de terminalidad. La autoridad debe vivir en una representacion compartida del runtime (enum/helper), y los consumidores deben consultarla en vez de duplicar listas locales. El ticket solo cubre los dos estados ya evidenciados (`SUPERSEDED`, `BLOCKED_FINAL`) y debe mantener intacto el cierre exitoso existente.
## Files Likely Touched
### repo_motor
- bus/state_machine.py
- bus/supervisor.py
- bus/builder_locks.py
- scripts/get_launcher_state.py
- scripts/archive_event_bus.py
- scripts/reconcile_ticket.py
- scripts/preflight_reconcile.py
- scripts/session_closeout.py
- scripts/closeout_steps/archival.py
- scripts/check_destino_publish_ready.py
- tests/unit/test_terminal_states.py
- tests/test_launcher_state_from_bus.py
- tests/evals/test_eval_requeue.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- .agent/runtime/events/events.jsonl
- .agent/collaboration/_archive/backlog_done.md
- .agent/collaboration/MANAGER_REVIEW_WT-2026-239a.md
- .agent/planning/plan_graph.md
- .agent/planning/contract_gaps/CG-WOT-2026-013c.md
- scripts/collect_system_health.py
- prompts/audit_post_change_system_health.md
- bus/event_bus.py
- scripts/manager_review_bridge.py
## Forbidden Surfaces
- .agent/agent_controller.py
- CI/workflows
- .agent/runtime/events/events.jsonl editado manualmente
- introducir `ABANDONED` sin evidencia nueva de Fase 0
- forzar `WT-2026-239a` o `WOT-2026-013c` a `COMPLETED`
- privada/
- .env
## Criterios binarios
- Existe una autoridad compartida de terminalidad irreversible que reconoce `SUPERSEDED` y `BLOCKED_FINAL` sin mapearlos a `COMPLETED`.
- El string legacy `CLOSED` deja de actuar como pseudo-estado canonico y no se promociona a nuevo miembro de `TicketState`.
- `bus/supervisor.py` deja de mantener una lista local divergente de no-terminalidad y consume la autoridad compartida del runtime.
- `scripts/archive_event_bus.py`, `scripts/reconcile_ticket.py`/`scripts/preflight_reconcile.py`, `scripts/session_closeout.py`/`closeout_steps/archival.py`, `scripts/get_launcher_state.py` y `scripts/check_destino_publish_ready.py` usan esa autoridad o quedan alineados con ella.
- Existe al menos una barrera de regresion que falla sin el fix y pasa con el fix para `SUPERSEDED`, y otra para `BLOCKED_FINAL`, sin romper el camino `COMPLETED` actual.
- `tests/unit/test_terminal_states.py` se crea como deliverable nuevo; `tests/test_launcher_state_from_bus.py` y `tests/evals/test_eval_requeue.py` se extienden sin crear suites duplicadas.
- `python -m pytest tests/unit/test_terminal_states.py tests/test_launcher_state_from_bus.py tests/evals/test_eval_requeue.py -q -p no:cacheprovider` termina verde.
- `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- El fix no reabre `239a` ni `013c` como trabajo activo ni degrada el contrato de cierre exitoso.
## STOP conditions
- Parar si `239a` o `013c` no sostienen la premisa tras releer bus/contrato reales.
- Parar si la unica salida segura exige redisenar de forma amplia el event schema o el lifecycle completo.
- Parar si el fix necesita tocar `.agent/agent_controller.py`, handoff o CI.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013n.md` si la unica salida segura exige un tercer estado no evidenciado (`ABANDONED`), una migracion amplia de consumidores no declarados, o cambios en controller/handoff/CI.

