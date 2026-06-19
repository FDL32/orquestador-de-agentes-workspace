# STRATEGY_WOT-2026-012a.md

## Enfoque

`WOT-2026-012a` separa primero el problema documental del problema de gating.
La meta es dejar `backlog.md` como cola viva parseable y sacar el historico a un
archivo aparte con evidencia auditable, sin meter ese movimiento dentro del
closeout ni del `mark-ready`. El gate fail-closed se construira despues en
`WOT-2026-012b`, sobre un formato ya estable.

## Fase 0 - Baseline y snapshot

1. Releer `backlog.md` y clasificar filas vivas vs terminales con el
   vocabulario cerrado del contrato.
2. Confirmar que `011e <-> 010m` ya queda resuelto como
   `keep-both-with-boundary` y no reabrir esa decision dentro del ticket.
3. Materializar un snapshot pre-corte como commit git explicito o como
   `.agent/collaboration/_archive/backlog_pre_012a.md` antes de mover nada.
4. Registrar en `execution_log.md` el baseline: numero de filas terminales y de
   fichas `###` candidatas a movimiento.

## Fase 1 - Corte del historico por bloques logicos

1. Mover las filas terminales del backlog activo al historico en bloques
   reconocibles, no por copy-paste disperso.
2. Mover tambien las fichas `###` que ya no pertenecen a la cola viva,
   preservando integra `### WOT-2026-012a`.
3. Mantener trazabilidad suficiente para que el diff del corte sea auditable.

## Fase 2 - Normalizacion de la cola viva

1. Dejar la tabla activa con schema estable y parseable, incluyendo
   `Reactivation`.
2. Asegurar que `Reactivation` solo admita `-` para estados activos sin
   trigger, y que `deferred` / `completed-partial` usen triggers estructurados
   (`WOT-...`, `commit:<sha>`, `external:<ref>`, `condition:<slug>`).
3. Garantizar que toda ficha obligatoria usa encabezado exacto
   `### WOT-...`.

## Fase 3 - Evidencia y cierre

1. Medir antes/despues: filas terminales movidas, fichas `###` movidas y
   reduccion material del backlog activo.
2. Confirmar que la cola viva ya no contiene estados terminales.
3. Ejecutar `check_encoding_guard.py` y `validate --json --project-root`.
4. Dejar en `execution_log.md` la evidencia literal del snapshot, del corte y de
   las validaciones finales.

## Riesgos a vigilar

- Perder historico por un corte demasiado manual o poco auditable.
- Dejar `Reactivation` como texto libre, inutil para el gate de `012b`.
- Borrar o mover accidentalmente `### WOT-2026-012a`, dejando al Builder sin
  trazabilidad operativa dentro del historico.
- Reabrir por accidente el solapamiento `011e <-> 010m` en vez de respetar la
  frontera ya decidida.
