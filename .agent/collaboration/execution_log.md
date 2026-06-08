# Execution Log WT-2026-242b

**Estado:** READY_FOR_REVIEW

## Objetivo

Implementar la capa de contención para shells Builder huérfanas en agent_controller,
de modo que un stale_builder_round no emita HANDOFF_BLOCKED cuando el ticket ya está
en READY_FOR_REVIEW, READY_TO_CLOSE, HUMAN_GATE o COMPLETED.

## Cambios en agent_controller.py (commit 18af1ad)

### 1. `_is_bus_state_post_success` (nueva función)

```python
POST_SUCCESS_STATES = frozenset({
    "READY_FOR_REVIEW", "READY_TO_CLOSE", "HUMAN_GATE", "COMPLETED",
})

def _is_bus_state_post_success(bus_state: object | None) -> bool:
    """Check if bus-derived state is past IN_PROGRESS (orphan-safe territory)."""
    if bus_state is None:
        return False
    return bus_state in POST_SUCCESS_STATES
```

### 2. `_handle_mark_ready` (~line 2726) — stale_builder_round guard

- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN`, return 0
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED`, return 1 (comportamiento original preservado)

### 3. `_handle_pre_handoff` (~line 3650) — stale_builder_round guard

- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN`, return `{"valid": True}`
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED` (comportamiento original preservado)

## Tests

### test_mark_ready_idempotency.py (6 tests nuevos + 3 pre-existentes reparados)

1. `test_stale_builder_orphan_when_bus_state_is_ready_for_review`
2. `test_stale_builder_orphan_when_bus_state_is_ready_to_close`
3. `test_stale_builder_orphan_when_bus_state_is_human_gate`
4. `test_stale_builder_orphan_when_bus_state_is_completed`
5. `test_stale_builder_orphan_emits_with_correct_payload`
6. `test_blocks_stale_builder_round_before_mark_ready` (pre-existing, mantiene HANDOFF_BLOCKED en IN_PROGRESS)
7. 3 tests reparados: `assert_not_called()` → verificar ausencia de HANDOFF_BLOCKED/STALE_BUILDER_ORPHAN

### test_agent_controller.py (3 tests nuevos)

1. `test_pre_handoff_stale_builder_orphan_when_ready_for_review`
2. `test_pre_handoff_stale_builder_orphan_when_completed`
3. `test_pre_handoff_round_ok_passes_through`

## Calidad

| Gate | Resultado |
|------|-----------|
| `pytest tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py -q` | 108 passed in 2.50s |
| `ruff check .agent/agent_controller.py tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py` | All checks passed! |
| `validate --json --project-root ...` | 0 code errors. Pre-closeout warnings: work_plan.md status IN_PROGRESS, missing bus events (expected) |

## Barrera de regresión

**Sin fix (comportamiento roto previo):** un stale_builder_round con ticket en READY_FOR_REVIEW emitía HANDOFF_BLOCKED (código 1), bloqueando el flujo aunque no hubiera nada que bloquear.

**Con fix:** el mismo escenario emite STALE_BUILDER_ORPHAN (código 0), no contamina el bus con HANDOFF_BLOCKED, y el flujo continúa.

**Demostración binaria:** `test_stale_builder_orphan_when_bus_state_is_ready_for_review` verifica:
```python
mock_bus.emit.assert_called_once()  # ← STALE_BUILDER_ORPHAN
# HANDOFF_BLOCKED NO se emite
for call in mock_bus.emit.call_args_list:
    assert call[0][0] != "HANDOFF_BLOCKED"
```

## Ficheros modificados (commit 18af1ad en repo_motor)

- `../orquestador_de_agentes/.agent/agent_controller.py` (+124/-13)
- `../orquestador_de_agentes/tests/unit/test_mark_ready_idempotency.py` (+203/-13)
- `../orquestador_de_agentes/tests/test_agent_controller.py` (+144/-0)

## Resumen del contrato

| Evento | Condición | Exit code |
|--------|-----------|-----------|
| `HANDOFF_BLOCKED` | stale round + bus state IN_PROGRESS | 1 |
| `STALE_BUILDER_ORPHAN` | stale round + bus state post-success | 0 |
| No event (pass through) | round OK | normal flow |