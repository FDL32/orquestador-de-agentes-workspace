# Work Ticket - WT-2026-242b

## Metadata
- **ID:** WT-2026-242b
- **Title:** Contención para shells Builder huérfanas en stale_builder_round
- **Scope:** system/stale-builder-orphan-containment
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-242a

## Objetivo
Implementar la capa de contención para shells Builder huérfanas en agent_controller,
de modo que un stale_builder_round no emita HANDOFF_BLOCKED cuando el ticket ya está
en READY_FOR_REVIEW, READY_TO_CLOSE, HUMAN_GATE o COMPLETED.

## Contrato
- Scope mínimo: solo agent_controller.py y tests.
- Aplicar la lógica en ambos call sites documentados:
  - `_handle_mark_ready` (~2726)
  - `_handle_pre_handoff` (~3650)
- El evento canónico nuevo es exactamente: `STALE_BUILDER_ORPHAN`
- No tocar launcher ni review_bridge salvo evidencia nueva fuerte.
- No introducir dependencia en PID persistido todavía; usar identidad mínima ticket_id + round + bus_state.
- Mantener el bloqueo actual intacto cuando el ticket siga en IN_PROGRESS (HANDOFF_BLOCKED).

## Files Likely Touched
- `.agent/agent_controller.py`
- `tests/unit/test_mark_ready_idempotency.py`
- `tests/test_agent_controller.py`

## Decision Arquitectonica
- La contencion se implementa en `agent_controller` porque es la capa mas segura
  para ignorar shells huerfanas sin matar procesos.
- El evento `STALE_BUILDER_ORPHAN` permite trazabilidad sin contaminar el bus
  con `HANDOFF_BLOCKED` una vez que el ticket ya esta mas alla de
  `IN_PROGRESS`.
- La identidad usada en este ticket es minima (`ticket_id + round + bus_state`);
  el endurecimiento por PID queda diferido a un ticket posterior.

## Non-goals
- No diagnosticar todavia el gap de deteccion en launcher.
- No introducir reconciliacion agresiva ni cierre de procesos.
- No cambiar la logica de review bridge ni de manager closeout.

## Cambios realizados

### 1. `_is_bus_state_post_success()` (nueva función helper)
```python
POST_SUCCESS_STATES = frozenset({
    "READY_FOR_REVIEW", "READY_TO_CLOSE", "HUMAN_GATE", "COMPLETED",
})
```

### 2. `_handle_mark_ready` (~2726) - stale_builder_round guard
- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN` y retorna 0
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED` y retorna 1 (comportamiento original)

### 3. `_handle_pre_handoff` (~3650) - stale_builder_round guard
- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN` y retorna `{"valid": True}`
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED` (comportamiento original)

## Tests
- `test_mark_ready_idempotency.py`: 6 tests (4 orphan states + payload check + IN_PROGRESS preserve)
- `test_agent_controller.py`: 3 tests (pre_handoff orphan + round_ok pass-through)
- 3 tests pre-existentes reparados (verificaban assert_not_called en todo el bus)

## Quality Gates
- `python -m pytest tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py -q`
- `python -m ruff check .agent/agent_controller.py tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py`
- `python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
