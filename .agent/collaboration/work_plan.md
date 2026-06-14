# Work Plan: WOT-2026-005a - Separacion memoria privada vs portable en memory_upload

## Metadata
- **ID:** WOT-2026-005a
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Añadir a `prompts/memory_upload.md` una decision explicita de destino de memoria (privada/portable) con evidencia y condicion de promocion
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (cambio documental; reversible via git)
- **Depende de:** WOT-2026-003b (completed), WOT-2026-003c (completed)
- **Origen:** session-2026-06-14-host-extends-learnings

## Decision Arquitectonica
El prompt ya distingue tres memorias y un campo "Donde deberia vivir", pero no obliga a
DECIDIR el destino con contrato antes de escribir. En el ciclo host-extends se guardo
aprendizaje util en memoria Claude privada sin criterio claro de cuando promoverlo a
portable validable. Se añade una seccion de decision obligatoria que crystaliza: declarar
destino (Claude privada / portable motor / portable destino / varias), evidencia requerida
por destino, condicion de promocion a `observations.jsonl` (schema + consumidor real) y la
prohibicion de añadir entradas portables sobre un schema en drift. Cambio documental: no
toca codigo de memoria ni schema.

## Files Likely Touched (repo_motor)
prompts/memory_upload.md

## Read/inspect only
- `skills/_shared/ap-schema.md` (schema canonico referenciado).
- `bus/memory_loader.py` (consumidor; solo para confirmar que no se toca codigo).

## Manager-only
- Revision documental (single review, deliverable_type=documentation): claridad, que las
  tres memorias quedan separadas y que la decision de destino es obligatoria y binaria.

## Non-goals
- NO cambiar el schema de `observations.jsonl` ni codigo de memoria.
- NO ampliar la higiene de redaccion mas alla de `memory_upload.md` (eso es WT-2026-250c).
- NO añadir dependencias.

## Criterios binarios de cierre
- [ ] El prompt distingue las tres memorias y EXIGE declarar destino antes de escribir.
- [ ] Si una observacion se marca portable, el prompt exige validacion de schema o la
      etiqueta `NO PROMOVIBLE` con motivo.
- [ ] Si `observations.jsonl` esta en drift de schema, el prompt prohibe añadir nuevas
      entradas portables sin ticket de migracion.
- [ ] `check_encoding_guard.py` pasa sobre `prompts/memory_upload.md`.
- [ ] `validate --project-root .` (destino) 0 errores; motor solo cambia este archivo.
- [ ] Commit en repo_motor con WOT-2026-005a.

## STOP / escalado
- Si aparece necesidad de cambiar schema o codigo de memoria, abrir ticket code separado.
- Si el saneo de redaccion excede `memory_upload.md`, derivar a WT-2026-250c.

## Gates (deliverable_type: documentation)
- `check_encoding_guard.py prompts/memory_upload.md`.
- `validate --project-root .` (destino) 0 errores.
- `check_motor_pristine --check` (solo este archivo cambia en el motor).
- Existencia del deliverable (el archivo editado).

## Entregables
- `prompts/memory_upload.md` con la seccion de decision de destino + regla de drift.
- `orchestrator_pipeline/reports/closeout_WOT-2026-005a.md`.
