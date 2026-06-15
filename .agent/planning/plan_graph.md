# plan_graph.md -- WOT-2026-007f

## PLAN-001 -- Integracion CONTRACT_GAP en bus/controller/projection

- **Objetivo:** implementar el ciclo completo: Builder emite evento CONTRACT_GAP
  -> controller acepta la transicion -> state_projection_sync deriva estado
  BLOCKED -> --validate detecta incoherencias.
- **Tickets:** T-007F-001
- **Dependencias de plan:** ninguna (PLAN-001 es el unico plan de 007f).
- **shared_dependencies:**
  - bus/event_bus.py (nuevo event type CONTRACT_GAP; reentry guard)
  - .agent/agent_controller.py (nueva transicion + validacion)
  - runtime/state_projection_sync.py (derivar BLOCKED desde evento)
  - tests/unit/ (tests nuevos; sin romper suite existente)
- **Superficies de archivo:**
  - bus/event_bus.py (modificado)
  - .agent/agent_controller.py (modificado)
  - runtime/state_projection_sync.py (modificado)
  - tests/unit/test_contract_gap_integration.py (nuevo)

---

## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|-------------------|------------|---------------|
| PLAN-001 | event_bus.py, agent_controller.py, state_projection_sync.py, tests/unit/ | event_bus.py (central), agent_controller.py (central) | Cualquier ticket que toque bus o controller en paralelo | Serializar; no lanzar otro ticket de bus/controller con 007f activo | no |

Colision critica: event_bus.py y agent_controller.py son superficies centrales
del motor. Cualquier ticket paralelo que los toque genera conflicto de merge
y alta probabilidad de regression. PLAN-001 debe ejecutarse en exclusiva.

parallelism_notes: unico plan; no aplica paralelismo entre planes.

---

## Merge Regression Audit

No aplica con un unico plan. Sin embargo, por ser superficies centrales (bus +
controller), antes de cerrar 007f: ejecutar python scripts/run_pytest_safe.py
sobre la suite completa y verificar 0 regresiones. Si la suite falla en tests
pre-existentes de bus o controller, reclasificar como requires_serialization
con otro ticket activo y abrir CONTRACT_GAP.

---

## Forbidden Surfaces (para tickets derivados de PLAN-001)

Todo ticket de PLAN-001 tiene prohibido tocar:

- prompts/ y skills/ (sin modificar).
- scripts/validate_contract_formation.py (pertenece a 007c/007g; fuera de scope).
- .agent/collaboration/TURN.md (protegido por guard_paths; solo el controller).
- privada/, .env, credenciales de ningun tipo.
- MANIFEST.distribute y MANIFEST.workspace (cambio de frontera requiere ticket separado).
- Logica de memoria (bus/memory_loader.py, scripts/memory_consolidate.py).
