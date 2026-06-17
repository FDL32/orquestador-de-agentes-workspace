# Execution Log: WOT-2026-010h - Propagar prefijo per-project a prompts

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010h
- **Contract ID:** T-010H-001
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010a` (completed) fijo el glosario de nomenclatura y el gate
  `check_ticket_nomenclature.py`; 010h propaga la regla de prefijo per-project a
  los prompts de arranque/auditoria que aun no la explicitan.
- `WOT-2026-010l` (completed, motor 915d2be) cerro el ciclo anterior; su
  archivado de `STRATEGY_`/`AUDIT_` se ejecuta al arrancar 010h (ver nota de
  arranque).

## Fase 0 - PENDIENTE

### Seams a confirmar (Builder)

- redaccion de referencia de la regla per-project en `session_bootstrap.md`
  (lineas 59,62,88);
- orden de fuente canonico (AGENTS.md/CLAUDE.md primario; `--validate`
  como verificacion);
- gap real por prompt (destino_bootstrap parcial; los 2 audit_* en 0);
- ausencia de ejemplos vivos `WP-`/`WT-` nuevos.

### Notas de arranque (Manager)

- Premisas re-verificadas read-only por el Manager el 2026-06-17: regex
  per-project vigente en `bus/ticket_id.py`; gap confirmado por grep en los 4
  prompts.
- **Deuda de archivado controlada:** los artefactos `STRATEGY_WOT-2026-010l.md`
  / `AUDIT_WOT-2026-010l.md` siguen vivos porque el archivador excluye el ticket
  activo; ahora que el work_plan apunta a 010h, deben archivarse con
  `scripts/archive_collaboration_artifacts.py` y COMMITEARSE en el mismo arranque
  para no dejar delete+untracked (incidente reconciliado en 010l).
- Preflight esperado para Builder: runtime bootstrap + `validate --json` 0/0
  antes de tocar codigo.
