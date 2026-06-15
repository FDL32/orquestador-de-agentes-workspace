# Work Plan: WOT-2026-007g

## Metadata

- **ID:** WOT-2026-007g
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-007c (COMPLETED)
- **Blocks:** WOT-2026-007f (007f must rebase against final contract after 007g)

## Objetivo

Extender `scripts/validate_contract_formation.validate_plan_graph` para enforce:

1. Valor estricto `paralelizable` en cada fila de la tabla Impact Simulation:
   valores permitidos: `yes`, `no`, o `after PLAN-\d+` (case-insensitive).
2. Presencia de seccion `## Merge Regression Audit` en el plan_graph.

**Decision de diseno (fijada pre-Builder):**
- `paralelizable` es un valor estricto: `yes`, `no`, `after PLAN-001`, etc.
- Comentarios adicionales van en columna separada `parallelism_notes`
  (o texto libre despues de `|` si la tabla lo permite, no concatenado al valor).
- El ejemplo canonico `docs/contract_formation/examples/python_service_minimal/plan_graph.md`
  tiene actualmente `no -- unico plan` -- debe migrarse a `no`.
- El fixture valido `tests/fixtures/contract_formation/valid/` (si contiene plan_graph)
  tambien debe migrarse.

## Files Likely Touched

- **Builder:** `scripts/validate_contract_formation.py` (funcion `validate_plan_graph`)
- **Builder:** `tests/unit/test_validate_contract_formation.py` (nuevos tests negativos y positivos)
- **Builder:** `docs/contract_formation/examples/python_service_minimal/plan_graph.md`
  (migrar `no -- unico plan` -> `no`; texto descriptivo a campo/prosa aparte)
- **Builder:** `docs/contract_formation/templates/plan_graph.md`
  (mostrar valores formales en columna Paralelizable)
- **Read/inspect only:** `tests/fixtures/contract_formation/valid/` (verificar si hay plan_graph fixture; migrar si lo hay)

## Criterios Binarios (DoD)

- [ ] `validate_plan_graph` rechaza `paralelizable: no -- unico plan` con error explicito.
- [ ] `validate_plan_graph` acepta `yes`, `no`, `after PLAN-001`, `after PLAN-002` (tests positivos).
- [ ] `validate_plan_graph` rechaza ausencia de seccion `## Merge Regression Audit`.
- [ ] Ejemplo canonico `python_service_minimal/plan_graph.md` pasa el validador actualizado.
- [ ] Template `plan_graph.md` muestra valores formales en columna Paralelizable.
- [ ] `ruff check .` exit 0.
- [ ] `python scripts/run_pytest_safe.py` exit 0 (suite verde, incluye tests 007g).
- [ ] No se introdujeron dependencias nuevas (stdlib-only).

## STOP conditions

- Si la migracion del ejemplo canonico rompe otro ticket o artefacto dependiente: CONTRACT_GAP, no improvisar.
- Si se detecta que `parallelism_notes` requiere schema change en mas de 2 artefactos: escalar, no ampliar scope.

## Forbidden Surfaces

- `bus/`, `runtime/`, `agent_controller.py`, `ticket_supervisor.py` -- sin tocar.
- `prompts/` -- sin tocar (incluyendo `contract_formation_pipeline.md`).
- `.agent/collaboration/` -- sin tocar excepto `execution_log.md` para bitacora.

## CONTRACT_GAP behavior

Si el Builder encuentra un artefacto no listado que requiere cambio, escribe
`contract_gaps/CG-WOT-2026-007g.md` y bloquea el ticket.

## Builder clarification rate esperado

0 -- la decision de formato estricto esta fijada. Si hay duda sobre un artefacto
concreto, abrir CONTRACT_GAP, no clarificar.
