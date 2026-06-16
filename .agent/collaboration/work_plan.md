# Work Plan: WOT-2026-010a

> Origen: revision de nomenclatura (2026-06-16). Depende de WOT-2026-008b y
> WOT-2026-009g (ambos cerrados/publicados, motor 4b61b4b).

## Metadata

- **ID:** WOT-2026-010a
- **Contract ID:** T-010A-001
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-008b, WOT-2026-009g

## Objetivo

Glosario canonico de nomenclatura de ticket + renames de artefactos, atacando la
causa VIVA (generadores que crean nombres + consumidores que los validan), sin
migracion arqueologica de historicos.

Decisiones canonicas (fijadas por el propietario):
- `WOT-` es el prefijo canonico de ticket (tres letras). `WP-`/`WT-` = legacy
  historico, SIN migracion masiva.
- "Plan" se reserva para el plan/familia completo (ej. `WOT-2026-009` familia).
  NO para el artefacto de un ticket.
- `work_plan.md` permanece como contrato operativo del ticket activo (sin cambio).
- `PLAN_WT-<ID>.md` -> `STRATEGY_WOT-<ID>.md` (estrategia tecnica; libera "PLAN").
- `AUDIT_WT-<ID>.md` -> `AUDIT_WOT-<ID>.md` (solo prefijo WT->WOT).
- `prompts/audit_plan.md` -> `prompts/audit_ticket_contract.md` con stub alias.

## Decision Arquitectonica

**Alcance de rename (confirmado por el propietario):** solo generadores +
consumidores. NO renombrar ni un solo archivo historico fisico
(`_archive/plan_audit/`). Solo renombrar artefactos VIVOS del ticket activo si
existieran; ahora no existe ninguno, asi que no se crea ni migra nada.

**Consumidores de codigo aceptan dos clases:**
- `canonical`: `STRATEGY_WOT-*`, `AUDIT_WOT-*`
- `legacy-compat`: `PLAN_WT-*`, `PLAN_WP-*`, `AUDIT_WT-*`, `AUDIT_WP-*`

El rename es semantico/operativo, no arqueologico. Los consumidores AÃ‘ADEN los
patrones canonicos SIN eliminar los legacy (alias de transicion).

**audit_plan.md:** `audit_ticket_contract.md` es la fuente real. `audit_plan.md`
queda como stub alias breve cuya primera linea apunta al nombre nuevo. NO
contiene contrato operativo duplicado.

## Orden de ejecucion (obligatorio)

1. Glosario canonico (doc).
2. Generadores activos (skills/prompts que CREAN o ENSEÃ‘AN IDs/artefactos).
3. Rename `audit_plan.md` -> `audit_ticket_contract.md` + stub alias + 2 refs.
4. Consumidores/validadores de codigo (aÃ±adir canonical, conservar legacy-compat).
5. Gate grep clasificatoria.

## Files Likely Touched

### repo_motor
- `AGENTS.md`
- `skills/man-create-work-plan/SKILL.md`
- `skills/man-create-work-plan/references/plan-template.md`
- `skills/man-create-work-plan/references/plan-quality-checklist.md`
- `prompts/session_bootstrap.md`
- `prompts/launch_builder.md`
- `skills/deep-research/SKILL.md`
- `skills/_shared/ticket-anti-patterns.md`
- `prompts/audit_plan.md`
- `prompts/audit_ticket_contract.md`
- `prompts/orchestrator_pipeline.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `prompts/audit_complete_motor_destination.md`
- `scripts/archive_collaboration_artifacts.py`
- `scripts/pre_handoff_guard.py`
- `bus/review_bridge.py`
- `.agent/motor_checkpoint.py`
- `scripts/validate_ticket_prose.py`
- `scripts/check_ticket_nomenclature.py`
- `scripts/create_checkpoint.py`
- `scripts/graph_context.py`
- `scripts/launch_agent_terminals.ps1`
- `scripts/session_close_observations.py`
- `scripts/session_closeout.py`
- `scripts/state_projection_probe.py`
- `scripts/ticket_activity_monitor.py`
- `skills/_shared/ap-schema.md`
- `skills/bui-implement-from-plan/references/code-rules.md`
- `skills/deep-research/references/research-template.md`
- `skills/man-review-implementation/references/verdict-format.md`
- `skills/memory-consolidate/SKILL.md`
- `skills/project-finalize/SKILL.md`
- `skills/refactor-manager/SKILL.md`
- `skills/repo-compare/references/output-format.md`
- `skills/session-close-observations/SKILL.md`
- `skills/session-close-observations/references/filter-rules.md`
- `skills/session-close-observations/references/schema.md`

Notas (no son parte del FLT parseable):
- Generadores: man-create-work-plan + references, session_bootstrap,
  launch_builder, deep-research, ticket-anti-patterns.
- Renames con alias: audit_plan -> audit_ticket_contract (+ stub), refs en
  orchestrator_pipeline y orchestrate-pipeline.
- Consumidores codigo: archive/pre_handoff_guard/review_bridge/motor_checkpoint/
  validate_ticket_prose anaden STRATEGY_WOT-/AUDIT_WOT- conservando legacy.
- `prompts/audit_complete_motor_destination.md`: ref a AUDIT_WT-* a clasificar.

### Read/inspect only
- `bus/ticket_id.py` (TICKET_ID_PATTERN ya acepta `[A-Z]{3}` -> WOT; no tocar)
- `_archive/plan_audit/` (historicos; NO tocar)

### Manager-only
- Ejecutar gate grep de aceptacion y validar clasificacion (`scripts/check_ticket_nomenclature.py`).
- Ejecutar `validate --json` final 0/0.

## Criterios Binarios

- [ ] Glosario canonico creado (familia/plan / ticket / work_plan.md /
      STRATEGY_ / AUDIT_ / prefijo WOT / WP-WT legacy).
- [ ] Ningun prompt/template/skill activo genera `WP-[YYYY]`, `WT-[YYYY]`,
      `PLAN_WP`, `PLAN_WT`, `AUDIT_WT` salvo en seccion marcada como legacy/compat.
- [ ] Gate grep: cada hit de `WP-[YYYY]`/`WT-[YYYY]`/`PLAN_WP`/`PLAN_WT`/
      `AUDIT_WT`/`audit_plan.md` en `prompts/`+`skills/`+`scripts/` clasificado
      como `canonical`, `legacy-compat` o `bug`. La gate falla si queda algun
      hit no clasificado fuera de seccion legacy/compat.
- [ ] Consumidores de codigo aceptan `STRATEGY_WOT-*`/`AUDIT_WOT-*` (canonical)
      Y conservan `PLAN_WT-*`/`PLAN_WP-*`/`AUDIT_WT-*`/`AUDIT_WP-*` (legacy-compat).
- [ ] `audit_plan.md` es stub alias (primera linea -> audit_ticket_contract.md),
      sin contrato operativo duplicado. `audit_ticket_contract.md` es la fuente.
- [ ] Las 2 refs canonicas de audit_plan (orchestrator_pipeline.md,
      orchestrate-pipeline/SKILL.md) apuntan al nombre nuevo.
- [ ] encoding guard OK en Markdown/prompts/skills tocados.`r`n- [ ] `python scripts/check_ticket_nomenclature.py` exit 0 (sin generadores legacy; historia/legacy-tagged permitidos).
- [ ] `ruff check .` exit 0.
- [ ] tests focales de consumidores/validadores tocados exit 0.
- [ ] `validate --json` destino 0/0 al cierre.

## Non-goals

- NO migrar los 161+72 archivos historicos `WP-`/`WT-` (es otra familia de
  tickets, no este).
- NO renombrar archivos en `_archive/plan_audit/` ni ningun historico fisico.
- NO eliminar los patrones legacy de los consumidores: se conservan como
  legacy-compat con alias de transicion (romperlos dejaria sin archivar los
  tickets historicos).
- NO tocar `bus/ticket_id.py`: el patron ya acepta el prefijo de tres letras
  (WOT); reabrirlo esta fuera de scope.
- NO crear artefactos `STRATEGY_WOT-`/`AUDIT_WOT-` para tickets que no existen;
  el rename es de generadores/consumidores, no de creacion arqueologica.

## Forbidden Surfaces

- `_archive/plan_audit/` y cualquier historico `PLAN_WP-`/`PLAN_WT-`/`AUDIT_WP-`/
  `AUDIT_WT-` (NO renombrar archivos historicos).
- `bus/ticket_id.py` (el patron ya acepta WOT; no reabrir).
- `privada/` y `.env`.
- Scope de cualquier otro ticket.
- NO eliminar patrones legacy de los consumidores (romperia archivado/guard de
  tickets historicos sin alias).

