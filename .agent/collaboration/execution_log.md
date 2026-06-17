# Execution Log: WOT-2026-010g - Inventario clasificado de prompts/skills legacy

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010g
- **Contract ID:** T-010G-001
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010c` (completed) fijo el gate de cierre con evidencia literal de
  suite; 010g es analysis read-only y no depende de esa barrera mas alla de la
  cadena de dependencias.
- `WOT-2026-010h` (completed, motor 8dbfcda) cerro el ciclo anterior; su
  archivado de `STRATEGY_`/`AUDIT_` se ejecuta al arrancar 010g.

## Fase 0 - PENDIENTE

### Seams a confirmar (Builder)

- lista completa `prompts/*.md` (20) y `skills/*/` (31) del motor;
- seam de consumidores vivos: `rg <basename>` sobre motor + destino antes de
  proponer cualquier move/delete;
- precedente de artefacto analysis: `.agent/docs/` del destino (008a).

### Notas de arranque (Manager)

- **Premisas re-verificadas read-only (2026-06-17):** las 4 (audit_plan stub,
  quickstart-checklist, Goose/Claw en AGENTS.md, refactor-manager con
  goose-skill.json/goose_integration.py) siguen vigentes. Inventario: 20
  prompts + 31 skills.
- **delivery_authority=repo_destino (decision Manager):** el reporte es un
  analysis puntual `destination-only`; vive en `.agent/docs/` del destino
  (precedente 008a). NO exige commit productivo en motor ni pytest/ruff. Cierre
  = artefacto existe + validate 0/0.
- **Aislamiento del motor:** 010g LEE el motor (read-only) pero NO escribe en el.
  Cero move/delete/rename.
- **Deuda de archivado controlada:** los artefactos `STRATEGY_WOT-2026-010h.md`
  / `AUDIT_WOT-2026-010h.md` siguen vivos porque el archivador excluye el ticket
  activo; ahora que el work_plan apunta a 010g, deben archivarse con
  `scripts/archive_collaboration_artifacts.py` y COMMITEARSE en el mismo arranque
  para no dejar delete+untracked (incidente reconciliado en 010l).
- Preflight esperado para Builder: runtime bootstrap + `validate --json` 0/0
  antes de tocar nada.
