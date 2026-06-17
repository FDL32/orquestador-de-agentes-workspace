# Work Plan: WOT-2026-010g

> Origen: el cierre de sesion detecto artefactos con semantica legacy/deprecated
> sin clasificar (`prompts/audit_plan.md` stub alias,
> `skills/setup-agent-system/references/quickstart-checklist.md` legacy,
> Goose/Claw deprecated en `AGENTS.md`, piezas Goose dentro de
> `skills/refactor-manager/`). Antes de mover, archivar o eliminar nada, hay que
> inventariar y clasificar.

## Metadata

- **ID:** WOT-2026-010g
- **Contract ID:** T-010G-001
- **Estado:** COMPLETED
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Depends on:** WOT-2026-010c (completed)

## Objetivo

Producir un inventario clasificado de `prompts/` y `skills/` del `repo_motor`
ANTES de mover, archivar o eliminar cualquier pieza legacy. Esta fase es
estrictamente de auditoria read-only: NO mueve, NO renombra y NO borra ningun
archivo. Cualquier accion destructiva se difiere a un ticket de follow-up
explicito.

## Decision Arquitectonica

Decisiones del Manager para este ticket:

- **Esto es analysis, no mixed:** el deliverable unico es un reporte de
  inventario. No se ajustan aliases ni docs en este ticket (eso seria mixed y
  abriria scope destructivo prematuro).
- **delivery_authority = repo_destino:** el reporte es un artefacto de auditoria
  puntual de esta sesion (`destination-only` por su propia clasificacion), no
  tooling portable. Sigue el precedente de `WOT-2026-008a`, cuyo analysis vivio
  en `.agent/docs/` del `repo_destino`. Por tanto NO exige commit productivo en
  `repo_motor` ni pytest/ruff: el cierre se basa en existencia del artefacto +
  `validate` 0/0.
- El motor se LEE (read-only) para inventariar; no se escribe en el.

## Hechos verificados (premise re-check read-only, 2026-06-17)

Las 4 premisas del origen siguen vigentes:
- `prompts/audit_plan.md` existe como stub alias -> `audit_ticket_contract.md`
  (renombrado en 010a). [candidato `alias-compat`]
- `skills/setup-agent-system/references/quickstart-checklist.md` existe.
  [candidato `legacy-retained` o `deprecated-removable`, decidir por consumidores]
- `AGENTS.md` menciona Goose/Claw como deprecated (WT-2026-254a).
  [historia/`legacy-retained`]
- `skills/refactor-manager/` contiene `goose-skill.json` + `goose_integration.py`.
  [candidatos `deprecated-removable`, pendiente de gate de consumidores]
- Tamano del inventario: 20 prompts (`prompts/*.md`) + 31 skills
  (`skills/*/`). Acotado y abordable en un solo reporte.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de redactar:

- la lista completa de `prompts/*.md` y `skills/*/` del `repo_motor`
  (`ls prompts/*.md`, `ls -d skills/*/`);
- el seam de busqueda de consumidores vivos: `rg <basename>` sobre `repo_motor`
  (scripts, prompts, skills, tests, `.agent/`) y sobre `repo_destino` cuando
  aplique, ANTES de proponer cualquier move/delete;
- el precedente de artefacto analysis (`.agent/docs/` del destino, 008a).

Registrar en `execution_log.md`: lista inventariada, seam de consumidores usado
y cualquier hallazgo que cambie el alcance.

## Clasificacion requerida (taxonomia, una etiqueta por artefacto o grupo de archivos)

- `canonical`: fuente viva del motor portable.
- `alias-compat`: stub o alias necesario para compatibilidad de nombres.
- `legacy-retained`: historia o referencia conservada deliberadamente.
- `deprecated-removable`: candidato a retirada tras demostrar CERO consumidores.
- `destination-only`: pertenece a historia operativa del `repo_destino`, no al
  motor portable.

## Reglas de clasificacion

- Si ayuda a instalar/operar cualquier destino -> `repo_motor` (canonical).
- Si documenta una sesion/ticket concreto de este destino -> `repo_destino`
  (`destination-only`).
- Si es compatibilidad de nombres antiguos -> `alias-compat`, se conserva como
  stub hasta que una gate confirme cero consumidores.
- Si es historia fiel -> `legacy-retained`, NO se reescribe ni moderniza.
- `deprecated-removable` SOLO si `rg` demuestra cero consumidores vivos; si hay
  duda, degrada a `legacy-retained`, no a removable.

## Files Likely Touched

### repo_destino
- `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md` (nuevo: el reporte)
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only (repo_motor, NO escribir)

- `prompts/` (los 20 `*.md`)
- `skills/` (las 31 carpetas)
- `AGENTS.md`
- `scripts/discover_skills.py`, `scripts/check_skill_collisions.py`
- cualquier consumidor encontrado via `rg`

## Manager-only

- verificar que el inventario cubre los 20 prompts + 31 skills sin huecos;
- verificar que cada `deprecated-removable` cita evidencia `rg` de cero
  consumidores;
- verificar que no se ejecuto ningun move/delete;
- `validate --json --project-root <repo_destino>` final 0/0.

## Criterios Binarios

- [ ] Existe `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md` con un
      inventario completo de `prompts/` y `skills/`: estado por archivo o grupo
      de archivos con una etiqueta de la taxonomia.
- [ ] Cada candidato a move/delete cita evidencia `rg` de consumidores vivos
      (o su ausencia) ANTES de proponerlo.
- [ ] Lista explicita de candidatos `destination-only` (mover a `repo_destino`)
      con justificacion.
- [ ] Lista explicita de candidatos a archivar en `repo_motor` con nota de
      rollback.
- [ ] CERO cambios destructivos: ningun archivo movido/renombrado/borrado en este
      ticket. Cualquier accion queda como follow-up con ticket propio.
- [ ] No se migran referencias historicas `WP-`/`WT-` ni comentarios de historia
      fiel.
- [ ] `check_encoding_guard.py <reporte>` exit 0 y
      `validate --json --project-root <repo_destino>` termina 0 errors / 0 warnings.

## Non-goals

- NO mover/eliminar/renombrar archivos en esta fase de inventario.
- NO migrar referencias `WP-`/`WT-` ni reescribir historia fiel.
- NO ajustar aliases ni docs (eso seria mixed; aqui es analysis puro).
- NO mezclar con `WOT-2026-010e`, `WOT-2026-010d` ni `WOT-2026-008d`.
- NO escribir nada en el `repo_motor`.

## Forbidden Surfaces

- cualquier move/delete/rename en `prompts/` o `skills/` del motor
- escritura en el `repo_motor`
- `privada/`
- `.env`
- `.agent/runtime/memory/`
- bus editado manualmente
- referencias historicas `WP-`/`WT-` y comentarios de historia fiel
