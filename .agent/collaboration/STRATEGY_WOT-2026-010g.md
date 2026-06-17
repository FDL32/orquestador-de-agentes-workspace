# STRATEGY_WOT-2026-010g -- Inventario clasificado de prompts/skills legacy

## Hechos verificados

- 20 prompts + 31 skills en el motor; inventario acotado a un reporte.
- Las 4 premisas del origen (audit_plan stub, quickstart-checklist,
  Goose/Claw deprecated, refactor-manager con Goose) estan confirmadas vivas.
- 008a (analysis previo) escribio su artefacto en `.agent/docs/` del destino:
  precedente para `delivery_authority=repo_destino` sin contaminar el motor.

## Plan tecnico

1. Listar `prompts/*.md` (20) y `skills/*/` (31) del motor.
2. Para cada uno, asignar UNA etiqueta de la taxonomia
   (canonical / alias-compat / legacy-retained / deprecated-removable /
   destination-only).
3. Para todo candidato a move/delete, ejecutar `rg <basename>` sobre motor y
   destino y CITAR el resultado (consumidores vivos o su ausencia) en el reporte.
4. Producir dos listas accionables: candidatos `destination-only` (mover a
   destino) y candidatos a archivar en motor, ambas con rollback/justificacion.
5. Escribir el reporte en
   `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md` del destino.
6. NO ejecutar ningun move/delete; cerrar con artefacto + validate 0/0.

## Riesgos

- **Accion destructiva prematura:** mover/borrar en fase de inventario.
  Mitigacion: Forbidden Surfaces explicitas + criterio binario de cero cambios.
- **Falso `deprecated-removable`:** declarar removable sin probar cero
  consumidores. Mitigacion: `rg` obligatorio; ante duda -> `legacy-retained`.
- **Contaminar el motor:** escribir el reporte en el motor. Mitigacion:
  delivery_authority=repo_destino, artefacto en `.agent/docs/`.
- **Reescribir historia fiel:** Mitigacion: non-goal explicito.

## No hacer

- No mover, renombrar ni borrar nada en `prompts/`/`skills/`.
- No escribir en el `repo_motor`.
- No migrar `WP-`/`WT-` ni modernizar historia.
- No mezclar con 010e/010d/008d.
