# ticket_contracts.md -- WOT-2026-007f

> Solo contratos frozen pasan a work_plan.md.
> CONTRACT_GAP es la unica via para invalidar.

---

## T-007F-001 -- Integracion runtime de CONTRACT_GAP en bus/controller

- **ticket:** T-007F-001
- **status:** frozen
- **Objective-Link:** OBJ-001 (Representacion operativa de gaps de contrato)
- **Plan-Link:** PLAN-001
- **Premise:**
  - El bus acepta eventos de tipo arbitrario (no hay enum cerrado en event_bus.py).
  - agent_controller.py --validate puede extenderse sin romper VALID_PLAN_STATES existentes.
  - La derivacion de estado vive en bus/state_machine.py (derive_state_from_events);
    scripts/state_projection_sync.py la consume. Un nuevo event type puede mapearse a
    un nuevo estado sin cambio de schema de events.jsonl. [amendment 2026-06-15: ver seccion final]
  - No existe ya un evento CONTRACT_GAP en el bus del destino activo.
  - Python 3.10+ disponible; sin dependencias nuevas necesarias.
- **Premise Re-check (read-only antes de activar):**
  - Verificar: grep -r CONTRACT_GAP bus/ runtime/ .agent/agent_controller.py -> 0 resultados.
  - Verificar: python scripts/run_pytest_safe.py -> suite verde (0 fallos pre-existentes).
  - Verificar: python .agent/agent_controller.py --validate -> 0 errors / 0 warnings.
  - Verificar: git log --oneline -1 -- bus/event_bus.py .agent/agent_controller.py -> si retorna un commit del ticket activo actual, serializar antes de arrancar.
- **Context Baseline Evidence:** git_head motor (>= ce83621), validate_result (0/0),
  suite_result (exit 0 de run_pytest_safe.py), contract_gap_absent (grep confirma ausencia).
- **Files Likely Touched:**
  - Builder: bus/event_bus.py (emit_contract_gap: event type + reentry guard + path canonico)
  - Builder: .agent/agent_controller.py (_validate_contract_gap_coherence)
  - Builder: bus/state_machine.py (estado CONTRACT_BLOCKED + derive_state_from_events)
  - Builder: .agent/state_validation.py (CONTRACT_BLOCKED en VALID_LOG_STATES)
  - Builder: tests/unit/test_contract_gap_integration.py (nuevo; casos: premise_false,
    forbidden_surface_needed, missing_acceptance, coherencia, path canonico)
  - Builder: tests/conftest.py (barrera fail-closed contra escrituras al bus real del motor)
  - Builder: tests/unit/test_motor_bus_isolation_barrier.py (nuevo; pruebas de la barrera)
  - Read/consume only: scripts/state_projection_sync.py (deriva via state_machine, sin modificar)
  - Read only: docs/contract_formation/templates/contract_gap.md (referencia schema)
  - Read only: scripts/validate_contract_formation.py (campos CG requeridos)
- **Forbidden Surfaces:**
  - prompts/ y skills/ (sin modificar)
  - scripts/validate_contract_formation.py (fuera de scope)
  - .agent/collaboration/TURN.md (guard_paths; solo controller)
  - privada/, .env, credenciales
  - MANIFEST.distribute, MANIFEST.workspace
  - bus/memory_loader.py, scripts/memory_consolidate.py
- **DoD:**
  - bus/event_bus.py acepta y emite evento CONTRACT_GAP sin error.
  - agent_controller.py --validate acepta ticket en estado CONTRACT_BLOCKED cuando
    evento presente; falla ante proyeccion incoherente (evento sin archivo CG o viceversa).
  - bus/state_machine.py deriva CONTRACT_BLOCKED desde evento CONTRACT_GAP;
    scripts/state_projection_sync.py proyecta ese estado sin modificacion propia.
  - Test premise_false: gap_type=premise_false -> ticket queda CONTRACT_BLOCKED, no COMPLETED.
  - Test forbidden_surface_needed: gap_type=forbidden_surface_needed -> ticket queda CONTRACT_BLOCKED, no COMPLETED.
  - Test missing_acceptance: gap_type=missing_acceptance -> ticket queda CONTRACT_BLOCKED, no COMPLETED.
  - Payload del evento CONTRACT_GAP en events.jsonl contiene solo ticket_id, gap_type y cg_file_path (test: assert set(payload.keys()) == {"ticket_id", "gap_type", "cg_file_path"}).
  - cg_file_path es la ruta relativa canonica contract_gaps/CG-<ticket_id>.md; emit_contract_gap
    rechaza rutas absolutas y traversal (test negativo parametrizado real).
  - Los tests de coherencia invocan _validate_contract_gap_coherence() real (no booleanos
    preparados): evento sin CG -> error, CG sin evento -> error, ambos presentes -> sin error.
  - La barrera pytest anti-leak restaura el events.jsonl real y falla el test contaminante con su nodeid; prueba negativa verificada.
  - ruff check . exit 0.
  - python scripts/run_pytest_safe.py suite verde (0 regresiones + nuevos tests pasan).
  - git diff HEAD -- prompts/ skills/ MANIFEST.distribute MANIFEST.workspace bus/memory_loader.py scripts/memory_consolidate.py -> vacio (0 cambios en Forbidden Surfaces).
- **STOP conditions:**
  - Si events.jsonl del destino activo ya contiene eventos CONTRACT_GAP de otro origen:
    CONTRACT_GAP, no improvisar schema.
  - Si agent_controller.py tiene logica de estados cerrada que no acepta extension
    limpia: CONTRACT_GAP y escalar.
  - Si otro ticket activo toca event_bus.py o agent_controller.py: detener, serializar.
  - Si el contrato cambia durante el ticket: volver a Contract Formation.
- **CONTRACT_GAP behavior:** el Builder escribe contract_gaps/CG-T-007F-001.md,
  bloquea el ticket y lo devuelve a Contract Formation. No improvisar schema.
- **Builder clarification rate esperado:** 0 (contrato autocontenido).
  Si surge duda de diseno sobre el schema del evento, es un STOP, no una clarificacion.
- **Integration cross-ticket:**
  - Ningun ticket activo debe tocar bus/event_bus.py o agent_controller.py en paralelo.
  - Post-007f: tickets que usaban CONTRACT_GAP documental podran emitirlo al bus.
- **Mapeo a work_plan.md:**
  ```
  Metadata: ID T-007F-001, Estado READY_TO_START, deliverable_type code,
  delivery_authority repo_motor.
  Objetivo: [copiar DoD completo]
  Files Likely Touched: [copiar de contrato]
  Criterios Binarios: [copiar DoD]
  STOP conditions: [copiar de contrato]
  ```
  Ningun campo se inventa: todo proviene del contrato frozen.

---

## Contract amendment (post-implementation, 2026-06-15)

**Tipo:** correccion de defecto de Contract Formation (NO CONTRACT_GAP de premisa).

**Por que no es CONTRACT_GAP:** la premisa del contrato (el bus acepta event types
nuevos; el controller es extensible; un event type mapea a un estado nuevo) se mantuvo
verdadera y la implementacion tuvo exito. No hubo premise_false ni missing_acceptance.
El defecto fue una declaracion factual erronea de superficies en el propio contrato,
detectada en review independiente del Manager. Abrir un CONTRACT_GAP retroactivo seria
teatro; la via correcta es enmendar y dejar el registro auditable.

**Declaraciones originales erroneas (conservadas para historia fiel):**
- Files Likely Touched declaraba `runtime/state_projection_sync.py` (ruta inexistente;
  el archivo real es `scripts/state_projection_sync.py`).
- Premise y DoD asumian que la derivacion de estado se editaba en
  `state_projection_sync.py`. En realidad la derivacion canonica vive en
  `bus/state_machine.py` (`derive_state_from_events`), y `scripts/state_projection_sync.py`
  la consume sin modificacion (verificado por test_state_projection_sync_derives_contract_blocked).

**Superficies reales (corregidas arriba):**
- `bus/event_bus.py`, `.agent/agent_controller.py` (ya declaradas, correctas).
- `bus/state_machine.py` y `.agent/state_validation.py` (estaban sin declarar; ahora declaradas).
- `scripts/state_projection_sync.py` reclasificado a read/consume-only.

**Leccion para la familia 007:** `audit_cf_ticket_contract` debe verificar que cada ruta
de Files Likely Touched exista en disco (o este marcada como `new`) antes de freezar.
Una ruta declarada inexistente es un blocker de Contract Formation, no un detalle.

---

## Fila de backlog generada

| Prioridad | Ticket | Titulo | Estado | Depende de |
|-----------|--------|--------|--------|------------|
| Baja | T-007F-001 | Integracion runtime CONTRACT_GAP | READY_TO_START | WOT-2026-007c, 007e, 007g (todos COMPLETED) |
