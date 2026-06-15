# Work Plan: WOT-2026-007f

## Metadata

- **ID:** WOT-2026-007f
- **Contract ID:** T-007F-001
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-007c (COMPLETED ce83621 / 5dafbc7), WOT-2026-007e (COMPLETED 1dc5447), WOT-2026-007g (COMPLETED ce83621)
- **Contract source:** .agent/planning/ticket_contracts.md (T-007F-001, status: frozen)

## Objetivo

Integrar CONTRACT_GAP como evento de bus operativo con tres superficies concretas:

1. bus/event_bus.py: acepta y emite evento de tipo CONTRACT_GAP; reentry guard
   evita duplicados por mismo ticket_id + gap_type.
2. .agent/agent_controller.py: transicion a estado CONTRACT_BLOCKED cuando hay
   evento CONTRACT_GAP; --validate detecta proyeccion incoherente (evento sin
   archivo CG o archivo CG sin evento).
3. runtime/state_projection_sync.py: deriva CONTRACT_BLOCKED desde evento CONTRACT_GAP.
4. tests/unit/test_contract_gap_integration.py: cubre premise_false,
   forbidden_surface_needed, missing_acceptance y payload seguro.

## Non-goals

- No crear UI ni CLI dedicado para gaps de contrato.
- No reparar automaticamente el contrato cuando se detecta un gap.
- No propagar gaps entre tickets en runtime (un gap bloquea solo su ticket).
- No cambiar el schema del archivo CG-*.md definido en 007c.
- No tocar tickets ni flujos que no usan Contract Formation.
- No modificar logic de memoria ni consolidacion (bus/memory_loader.py).

## Decision Arquitectonica

El evento CONTRACT_GAP se disenio como evento de bus (no como archivo de flag ni
campo en work_plan.md) porque:

- El bus es la fuente de verdad canonico del ciclo de vida del ticket;
  un gap que no emite evento puede no detectarse si work_plan.md se edita a mano.
- El reentry guard de event_bus.py protege contra duplicados sin logica adicional.
- --validate ya lee el bus para inferir estado; extenderlo con CONTRACT_GAP no
  requiere nuevo mecanismo, solo un nuevo event_type y una nueva regla de coherencia.
- El payload minimo (ticket_id, gap_type, cg_file_path) mantiene el bus libre de
  datos sensibles que podrian estar en las premisas del destino.

## Files Likely Touched

- Builder: bus/event_bus.py
- Builder: .agent/agent_controller.py
- Builder: bus/state_machine.py
- Builder: .agent/state_validation.py
- Builder: tests/conftest.py (barrera anti-leak solicitada en review)
- Builder: tests/unit/test_contract_gap_integration.py (nuevo)
- Builder: tests/unit/test_motor_bus_isolation_barrier.py (nuevo)
- Read/consume only: scripts/state_projection_sync.py
- Read only: docs/contract_formation/templates/contract_gap.md
- Read only: scripts/validate_contract_formation.py

## Criterios Binarios (DoD)

- [ ] bus/event_bus.py: test de emision de evento CONTRACT_GAP pasa (exit 0).
- [ ] agent_controller.py --validate: acepta ticket en estado CONTRACT_BLOCKED
      con evento CONTRACT_GAP presente; retorna exit 0 con 0 errors.
- [ ] agent_controller.py --validate: retorna exit 1 con error explicito si hay
      evento CONTRACT_GAP sin archivo CG-*.md o archivo CG sin evento.
- [ ] state_projection_sync.py: test de proyeccion CONTRACT_BLOCKED pasa (exit 0).
- [ ] Test premise_false: gap_type=premise_false -> ticket queda CONTRACT_BLOCKED, no COMPLETED (exit 0).
- [ ] Test forbidden_surface_needed: gap_type=forbidden_surface_needed -> CONTRACT_BLOCKED (exit 0).
- [ ] Test missing_acceptance: gap_type=missing_acceptance -> CONTRACT_BLOCKED (exit 0).
- [ ] Payload del evento en events.jsonl contiene exactamente: ticket_id, gap_type, cg_file_path
      (assert set(payload.keys()) == {"ticket_id", "gap_type", "cg_file_path"}).
- [ ] ruff check . -> exit 0.
- [ ] python scripts/run_pytest_safe.py -> exit 0 (suite completa, 0 regresiones + nuevos tests).
- [ ] git diff HEAD -- prompts/ skills/ MANIFEST.distribute MANIFEST.workspace
      bus/memory_loader.py scripts/memory_consolidate.py -> sin cambios.
- [ ] La barrera pytest anti-leak restaura el bus real y falla con el nodeid del test contaminante; tests negativos y suite completa pasan.

## STOP conditions

- Si events.jsonl del destino activo ya contiene eventos CONTRACT_GAP de otro origen:
  abrir CG-T-007F-001.md, no improvisar schema.
- Si agent_controller.py tiene enum cerrado de estados que rechaza CONTRACT_BLOCKED:
  abrir CG-T-007F-001.md y escalar.
- Si otro ticket activo toca bus/event_bus.py o .agent/agent_controller.py:
  detener y serializar con ese ticket antes de continuar.
- Si el contrato en .agent/planning/ticket_contracts.md cambia durante este ticket:
  detener y volver a Contract Formation.

## Premise Re-check (ejecutar antes del primer commit)

- grep -r CONTRACT_GAP bus/ runtime/ .agent/agent_controller.py -> 0 resultados.
- python scripts/run_pytest_safe.py -> exit 0.
- python .agent/agent_controller.py --validate -> 0 errors / 0 warnings.
- git log --oneline -1 -- bus/event_bus.py .agent/agent_controller.py -> sin commits activos en estas superficies.

## Forbidden Surfaces

- prompts/ y skills/ (sin modificar)
- scripts/validate_contract_formation.py (fuera de scope de este ticket)
- .agent/collaboration/TURN.md (guard_paths; solo controller puede escribirlo)
- privada/, .env, credenciales de ningun tipo
- MANIFEST.distribute, MANIFEST.workspace
- bus/memory_loader.py, scripts/memory_consolidate.py
