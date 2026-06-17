# AUDIT_WOT-2026-010g -- Criterios de auditoria

## Contrato estructural

- [ ] El unico entregable es el reporte de inventario en
      `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md` (repo_destino).
- [ ] CERO escrituras en el `repo_motor`. CERO move/delete/rename de prompts o
      skills. `git status` del motor limpio salvo lecturas.
- [ ] No se ajustan aliases ni docs (es analysis, no mixed).

## Evidencia minima

- [ ] El reporte cubre los 20 prompts + 31 skills sin huecos, cada uno con UNA
      etiqueta de la taxonomia.
- [ ] Cada candidato `deprecated-removable` o a move cita evidencia `rg` de
      consumidores (presencia o ausencia), no afirmacion sin prueba.
- [ ] Existe lista de candidatos `destination-only` con justificacion.
- [ ] Existe lista de candidatos a archivar en motor con nota de rollback.
- [ ] `check_encoding_guard.py <reporte>` exit 0.
- [ ] `validate --json --project-root <repo_destino>` termina 0/0.

## Anti-patrones a rechazar

- Declarar `deprecated-removable` sin `rg` que pruebe cero consumidores.
- Cualquier move/delete/rename ejecutado en este ticket.
- Escribir en el `repo_motor` (rompe delivery_authority y aislamiento).
- Reescribir o modernizar historia fiel / referencias `WP-`/`WT-`.
- Inventario con huecos (prompts o skills sin clasificar).
- Cierre citado sin existencia del artefacto + validate 0/0.
