# Work Ticket - WT-2026-235a

## Metadata
- **ID:** WT-2026-235a
- **Title:** Manager review bridge: decisiones autoritativas y CHANGES con blockers
- **Scope:** system/review-bridge-decision-contract
- **Priority:** Critica
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-204, WT-2026-234a

## Objetivo
Evitar que el Manager bridge emita decisiones accionables falsas o incompletas.
`APPROVE` y `CHANGES` solo pueden salir de una fuente final autoritativa; `CHANGES`
ademas requiere estructura completa y blockers no vacios. Si la decision no cumple
ese contrato, el bridge debe degradar a `INSPECT` y no relanzar Builder.

## Problema
En `WT-2026-234a`, el Manager automatico emitio en dos rondas
`REVIEW_DECISION -> changes` con `payload.blockers == ""`. El supervisor hizo lo
correcto al bloquear el handoff con `HANDOFF_BLOCKED reason=empty_blockers`, pero el
Builder quedo sin instrucciones accionables y se generaron relaunches ciegos.

La auditoria del bus confirma una causa mas grave: el fallback `text_regex` puede
escanear el transcript completo y capturar literales `DECISION: CHANGES` o
`DECISION: APPROVE` que aparecen en la propia plantilla del review packet, no en un
veredicto final real del Manager. Eso puede producir tanto `CHANGES` vacio como un
falso `APPROVE` silencioso.

## Contrato
- `APPROVE` solo es valido desde `json_final_answer`.
- `CHANGES` solo es valido si cumple las condiciones siguientes: procede de
  `json_final_answer`, contiene `## SUMMARY`, contiene `## BLOCKERS`, contiene
  `## SUGGESTIONS` y `blockers.strip()` no esta vacio.
- `json_last_text`, `json_no_decision`, `text_regex` y parse methods ausentes
  (`None` o cadena vacia) no pueden emitir `APPROVE` ni `CHANGES`; deben degradar
  a `INSPECT`.
- Si `CHANGES` no cumple estructura o blockers, degradar a `INSPECT` con
  `failure_reason=changes_structure_invalid`.
- El evento `REVIEW_DECISION` debe incluir `parse_method` y `failure_reason` cuando
  exista degradacion.
- No tocar la logica de seguridad del supervisor: su `HANDOFF_BLOCKED` por blockers
  vacios queda como segunda red.

## Decision Arquitectonica
El fix se aplica en `bus/review_bridge.py`, antes de emitir `REVIEW_DECISION`,
porque ahi se combinan procedencia (`parse_method`) y payload (`blockers`,
`missing_sections`). El supervisor conserva su guard de `empty_blockers` como red
de seguridad, pero no debe decidir si el veredicto del Manager es autoritativo.

## Non-goals
- No modificar `bus/event_bus.py` ni imponer schema global en esta pasada.
- No cambiar `bus/supervisor.py` salvo que un test demuestre una dependencia directa
  inevitable.
- No cambiar prompts de Manager como sustituto del gate automatico.
- No introducir analisis semantico complejo ni dependencias nuevas.

## Fases

### Fase 0 - Baseline del bug
- Reproducir con tests el comportamiento actual:
  - transcript con plantilla `DECISION: APPROVE/CHANGES` sin veredicto final;
  - NDJSON que termina en `tool-calls` sin `final_answer`;
  - `CHANGES` sin bloque `## BLOCKERS` accionable.
- Confirmar el baseline de estos tres casos: plantilla reflejada produce decision
  fuerte, NDJSON sin final_answer produce decision fuerte, o `CHANGES` invalido
  produce `blockers=""`.

### Fase 1 - Procedencia autoritativa
- Endurecer `bus/review_bridge.py` para que `text_regex` no pueda devolver
  `APPROVE` ni `CHANGES`.
- Si `parse_method != "json_final_answer"` para una decision fuerte, devolver
  `INSPECT`.
- Conservar trazabilidad mediante `parse_method` en el payload emitido.

### Fase 2 - Payload de CHANGES
- Hacer que `_validate_changes_structure()` muerda de verdad.
- Si `decision == CHANGES` y falta estructura o `blockers.strip()` esta vacio:
  - degradar a `INSPECT`;
  - persistir causa en feedback;
  - emitir `REVIEW_DECISION` con `decision=inspect`,
    `failure_reason=changes_structure_invalid`, `missing_sections` y `parse_method`;
  - no dejar payload que active requeue ciego.

### Fase 3 - Tests y gates
- Anadir tests focales en `tests/test_manager_review_bridge.py`.
- Ejecutar ruff y pytest focal.
- Ejecutar `agent_controller.py --validate --json --project-root <repo_destino>` como
  gate Manager, no Builder.

## Files Likely Touched

### repo_motor - Builder
- `bus/review_bridge.py`
- `tests/test_manager_review_bridge.py`

### repo_destino - Manager only
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-235a.md`
- `.agent/collaboration/AUDIT_WT-2026-235a.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Superficies prohibidas para Builder
- Paths bajo raiz `repo_destino`: `<repo_destino>/**`.
- `.agent/collaboration/**`
- `.agent/runtime/**`
- `bus/supervisor.py`, salvo hallazgo verificado y justificado antes de editar.
- `bus/event_bus.py`.

## Criterios de aceptacion
- `text_regex` no puede producir `APPROVE` ni `CHANGES`.
- Transcript con plantilla interna `DECISION: APPROVE/CHANGES` pero sin veredicto
  final autoritativo produce `INSPECT`.
- NDJSON terminado en `tool-calls` sin `final_answer` produce `INSPECT`.
- `CHANGES` sin blockers estructurados se degrada a `INSPECT` con
  `failure_reason=changes_structure_invalid`.
- `CHANGES` estructurado con blockers no vacios sigue produciendo `CHANGES` y
  conserva `payload.blockers`.
- `APPROVE` desde fuente final autoritativa sigue produciendo `APPROVE`.
- `REVIEW_DECISION` incluye `parse_method`; si hay degradacion incluye
  `failure_reason`.
- `pytest tests/test_manager_review_bridge.py -q` pasa.
- `ruff check bus/review_bridge.py tests/test_manager_review_bridge.py` pasa.

## TP Check
TP-01: el test reproduce el falso positivo por plantilla reflejada.
TP-02: `text_regex` queda degradado a `INSPECT` para decisiones fuertes.
TP-03: `CHANGES` invalido no emite blockers vacios ni dispara requeue ciego.
TP-04: `CHANGES` valido conserva blockers accionables para el supervisor.
TP-05: `APPROVE` valido sigue funcionando desde fuente autoritativa.
TP-06: `REVIEW_DECISION` deja trazabilidad de `parse_method` y degradacion.
TP-07: no se toca `supervisor.py` ni `event_bus.py` sin evidencia nueva.
