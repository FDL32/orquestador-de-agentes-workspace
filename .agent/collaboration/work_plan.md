# Work Plan: WOT-2026-007g

## Metadata

- **ID:** WOT-2026-007g
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-007c (COMPLETED), WOT-2026-007e (COMPLETED)
- **Blocks:** WOT-2026-007f (007f must rebase against final contract after 007g)

## Objetivo

Extender `scripts/validate_contract_formation.validate_plan_graph` para enforce:

1. Valor estricto `paralelizable` en cada fila de la tabla Impact Simulation:
   valores permitidos: `yes`, `no`, o `after PLAN-\d+` (case-insensitive).
2. Presencia de seccion `## Merge Regression Audit` en el plan_graph.

## Decision Arquitectonica

El valor `paralelizable` se valida como campo estructurado y no como prosa. Los
comentarios humanos viven en una columna separada `parallelism_notes` o en prosa
fuera del valor. El validador localiza la columna por cabecera `Paralelizable`
para que anadir columnas auxiliares no cambie el contrato ni genere falsos
positivos.

## Non-goals

- No integrar `CONTRACT_GAP` en runtime, bus ni controller; eso queda para WOT-2026-007f.
- No reorganizar prompts/skills ni taxonomia de carpetas; eso queda para WOT-2026-008a.
- No cambiar el formato general de `plan_graph.md` fuera de `paralelizable` y `Merge Regression Audit`.

## Files Likely Touched

- scripts/validate_contract_formation.py
- tests/unit/test_validate_contract_formation.py
- docs/contract_formation/examples/python_service_minimal/plan_graph.md
- docs/contract_formation/templates/plan_graph.md
- tests/fixtures/contract_formation/valid/plan_graph.md

## Criterios Binarios (DoD)

- [x] `validate_plan_graph` rechaza `paralelizable: no -- unico plan` con error explicito.
- [x] `validate_plan_graph` acepta `yes`, `no`, `after PLAN-001`, `after PLAN-002`.
- [x] `validate_plan_graph` acepta una columna `parallelism_notes` separada sin confundirla con `Paralelizable`.
- [x] `validate_plan_graph` rechaza ausencia de seccion `## Merge Regression Audit`.
- [x] Ejemplo canonico `python_service_minimal/plan_graph.md` pasa el validador actualizado.
- [x] Template `plan_graph.md` muestra valores formales en columna `Paralelizable`.
- [x] `ruff check scripts/validate_contract_formation.py tests/unit/test_validate_contract_formation.py` exit 0.
- [x] `python -m pytest tests/unit/test_validate_contract_formation.py -q` exit 0.
- [x] `python -m pytest tests/unit -q` exit 0.
- [x] No se introdujeron dependencias nuevas (stdlib-only).

## STOP conditions

- Si la migracion del ejemplo canonico rompe otro ticket o artefacto dependiente: CONTRACT_GAP, no improvisar.
- Si se detecta que `parallelism_notes` requiere schema change en mas de 2 artefactos: escalar, no ampliar scope.

## Forbidden Surfaces

- `bus/`, `runtime/`, `agent_controller.py`, `ticket_supervisor.py` -- sin tocar.
- `prompts/` -- sin tocar (incluyendo `contract_formation_pipeline.md`).
- `.agent/collaboration/` -- solo proyecciones operativas y bitacora del ticket.

## CONTRACT_GAP behavior

Si el Builder encuentra un artefacto no listado que requiere cambio, escribe
`contract_gaps/CG-WOT-2026-007g.md` y bloquea el ticket.

## Builder clarification rate esperado

0 -- la decision de formato estricto esta fijada. Si hay duda sobre un artefacto
concreto, abrir CONTRACT_GAP, no clarificar.
