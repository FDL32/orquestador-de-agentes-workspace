# STRATEGY_WOT-2026-013n

## Objetivo tecnico
Introducir terminalidad honesta no-exito para `SUPERSEDED` y `BLOCKED_FINAL` con una sola autoridad compartida, propagandola a las vistas/gates que hoy siguen pidiendo `COMPLETED` para verse limpias.

## Riesgos a evitar
- falso verde: mapear `SUPERSEDED` o `BLOCKED_FINAL` a `COMPLETED`, o preservar `CLOSED` como pseudo-estado canonico
- medio fix: corregir `state_machine` pero dejar listas locales divergentes en closeout/reconcile/launcher/publication
- overreach: abrir `ABANDONED`, tocar controller o reescribir el lifecycle entero
- handoff surprise: tocar `bus/` y `supervisor.py` sin dejar claro en `execution_log.md` por que el scope es valido, exponiendo ruido evitable en `--pre-handoff`
- regresion de exito: romper `READY_TO_CLOSE -> COMPLETED -> SUPERVISOR_CLOSED`

## Fase 0 - Relectura adversarial
1. Confirmar en bus real que `WT-2026-239a` no es trabajo incompleto sino supersession honesta, y que `WOT-2026-013c` es `blocked-final` contractual. Nombre canonico a introducir en enum: `BLOCKED_FINAL` (guion bajo); el historico `BLOCKED-FINAL` del planning es solo etiqueta documental.
2. Localizar en codigo cada consumidor que decide terminalidad o publicabilidad con listas locales, incluyendo el residuo legacy `CLOSED` fuera del enum y la redeclaracion de `NON_TERMINAL_STATES` en `bus/supervisor.py`.
3. Si aparece un tercer estado imprescindible no evidenciado (`ABANDONED`), parar por CONTRACT_GAP en vez de ensanchar el ticket.

## Fase 1 - Autoridad compartida
1. Extender `TicketState` con `SUPERSEDED` y `BLOCKED_FINAL`, o helper canonico equivalente en `state_machine`.
2. Hacer que `is_approved_or_terminal`, `NON_TERMINAL_STATES` y derivacion/consumidores converjan en esa misma autoridad. `CLOSED` debe quedar absorbido como legado no-enum, no como estado nuevo de `TicketState`.
3. Mantener `READY_TO_CLOSE` como no terminal y `COMPLETED` como terminal de exito.

## Fase 2 - Consumidores relevantes
1. Propagar la autoridad a `supervisor`, `builder_locks`, `reconcile_ticket`, `preflight_reconcile`, `archive_event_bus`, `session_closeout`, `closeout_steps/archival`, `get_launcher_state` y `check_destino_publish_ready`.
2. Corregir solo la semantica de terminalidad/publicabilidad; no cambiar controller, handoff ni CI.

## Fase 3 - Barreras
1. Crear `tests/unit/test_terminal_states.py` como deliverable nuevo, con FAIL-sin/PASS-con para `SUPERSEDED` y `BLOCKED_FINAL` en la autoridad compartida y al menos un consumidor de cierre.
2. Ajustar `tests/test_launcher_state_from_bus.py` como extension de suite existente para que ambos estados desemboquen en `MANAGER / CREATE_PLAN` o semantica terminal equivalente.
3. Ajustar `tests/evals/test_eval_requeue.py` como extension de suite existente para que los nuevos terminales bloqueen relaunch/requeue como `COMPLETED`.

## Gates objetivo
- `python -m pytest tests/unit/test_terminal_states.py tests/test_launcher_state_from_bus.py tests/evals/test_eval_requeue.py -q -p no:cacheprovider`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Cierre esperado
El Builder entrega solo codigo del motor + evidencia en `execution_log.md`. La posible reconciliacion real de `239a` / `013c` a sus nuevos estados honestos es paso posterior del Manager, no se fabrica durante la implementacion salvo que el contrato lo pida explicitamente.

