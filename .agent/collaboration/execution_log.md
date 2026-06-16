# Execution Log: WOT-2026-010a - Glosario nomenclatura + renames de artefactos

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010a
- **Contract ID:** T-010A-001
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD: 4b61b4b (WOT-2026-009g cerrado/publicado)
- Destino HEAD: e5d8dae (009g canonical close)
- Validate previo: 0/0
- 008b + 009g: cerrados/publicados (tags checkpoint/review-WOT-2026-008b y -009g)

## Baseline grep (fotografia inicial, NO numero fijo)

Patrones del contrato en prompts/ skills/ scripts/ (sin __pycache__/sandbox):
- WP-[YYYY]: plan-template.md:7, man-create-work-plan/SKILL.md:79
- PLAN_WP: session_bootstrap.md, deep-research/SKILL.md, plan-quality-checklist.md,
  man-create-work-plan/SKILL.md (x4), ticket-anti-patterns.md,
  archive_collaboration_artifacts.py, pre_handoff_guard.py
- PLAN_WT: audit_plan.md, archive_collaboration_artifacts.py, pre_handoff_guard.py
- AUDIT_WT: audit_complete_motor_destination.md, audit_plan.md,
  pre_handoff_guard.py, validate_ticket_prose.py
- audit_plan.md refs: orchestrator_pipeline.md, orchestrate-pipeline/SKILL.md

bus/ticket_id.py: TICKET_ID_PATTERN ya acepta [A-Z]{3} (cubre WOT) - NO tocar.

## Decisiones del propietario (AskUserQuestion 2026-06-16)

- Rename scope: solo generadores + consumidores; NO historicos fisicos.
- Consumidores aceptan canonical (STRATEGY_WOT-*, AUDIT_WOT-*) + legacy-compat
  (PLAN_WT/WP-*, AUDIT_WT/WP-*); NO eliminar legacy.
- audit_plan.md -> stub alias breve -> audit_ticket_contract.md (fuente real).

## Implementacion (orden del contrato)

### 1. Glosario canonico
- AGENTS.md seccion "Glosario de nomenclatura de ticket (WOT-2026-010a)":
  WOT canonical / WP-WT legacy / familia-plan / work_plan.md / STRATEGY_WOT- /
  AUDIT_WOT- / clases canonical vs legacy-compat / audit_ticket_contract.md.

### 2. Generadores activos (foco backlog + 4 extra hallados por la gate)
Foco backlog:
- skills/man-create-work-plan/SKILL.md: ID WP-[YYYY]-[NNN] -> WOT-[YYYY]-[NNN][x];
  PLAN_WP-/AUDIT_WP- -> STRATEGY_WOT-/AUDIT_WOT- (4 bloques).
- references/plan-template.md: ID -> WOT-[YYYY]-[NNN][x].
- references/plan-quality-checklist.md: PLAN_WP/AUDIT_WP -> STRATEGY_WOT/AUDIT_WOT.
- prompts/session_bootstrap.md: PLAN_WP-/AUDIT_WP- -> STRATEGY_WOT-/AUDIT_WOT-.
- skills/deep-research/SKILL.md: lectura canonical + nota legacy-compat.
- skills/_shared/ticket-anti-patterns.md: PLAN_WP/AUDIT_WP -> STRATEGY_WOT/AUDIT_WOT.
4 extra hallados por la gate (NO estaban en el foco fijo del backlog):
- skills/bui-implement-from-plan/references/log-format.md: Plan ID WP-XXX -> WOT-XXX.
- skills/man-resolve-escalation/SKILL.md: Plan ID WP-XXX -> WOT-XXX.
- skills/man-review-implementation/references/verdict-format.md: WP-2026-001 -> WOT-2026-001.
- skills/man-review-implementation/SKILL.md: Plan ID WT-XXX -> WOT-XXX.
launch_builder.md: solo ref historica WT-2026-257a (mojibake example) = legacy, no tocada.

### 3. Rename audit_plan.md -> audit_ticket_contract.md + stub alias
- prompts/audit_ticket_contract.md: copia con titulo nuevo, refs internas
  PLAN_WT-/AUDIT_WT- -> STRATEGY_WOT-/AUDIT_WOT- (+ nota legacy), WT-...a -> WOT-...a.
- prompts/audit_plan.md: stub alias 11 lineas, primera linea apunta al nuevo,
  sin contrato duplicado.
- Refs canonicas actualizadas: orchestrator_pipeline.md (x3), orchestrate-pipeline/SKILL.md (x2).
- prompts/audit_complete_motor_destination.md: AUDIT_WT-* -> AUDIT_WOT-* + nota legacy.

### 4. Consumidores de codigo (canonical + legacy-compat, sin eliminar legacy)
- scripts/archive_collaboration_artifacts.py: + STRATEGY_RE; parse_wp_number
  recorre (STRATEGY_RE, PLAN_RE, AUDIT_RE). PLAN_/AUDIT_ legacy conservados.
- scripts/pre_handoff_guard.py: WORKSPACE_EXCLUDED_PREFIXES + STRATEGY_WOT-/AUDIT_WOT-
  (canonical) conservando PLAN_WP-/PLAN_WT-/AUDIT_WP-/AUDIT_WT- (legacy-compat).
- .agent/motor_checkpoint.py: misma actualizacion simetrica de WORKSPACE_EXCLUDED_PREFIXES.
- bus/review_bridge.py: helper _resolve_strategy_file (canonical-first, legacy fallback);
  P4 prompt incluye STRATEGY_/PLAN_ legacy; nota system-generated artifacts.
- scripts/validate_ticket_prose.py: glob canonical AUDIT_[A-Z]{3}-* primero (cubre
  AUDIT_WOT-*), WP-/WT- conservados como legacy-compat; mensajes actualizados.
- bus/ticket_id.py: NO tocado (TICKET_ID_PATTERN ya acepta [A-Z]{3} = WOT).

### Tests de barrera (canonical aceptado)
- tests/unit/test_archive_collaboration_artifacts.py::test_parse_wp_number_canonical_strategy
- tests/test_review_bridge.py: 4 tests de _resolve_strategy_file (canonical-first,
  legacy fallback, canonical-wins, none-when-missing).

## Gate grep final (clasificacion)

Patrones WP-[YYYY]/WT-[YYYY]/PLAN_WP/PLAN_WT/AUDIT_WT/audit_plan.md en
prompts/ skills/ scripts/ (sin __pycache__/sandbox). Cada hit clasificado:
- canonical: audit_ticket_contract.md (5), audit_complete_motor_destination.md (1),
  deep-research/SKILL.md (2) — todos usan STRATEGY_WOT-/AUDIT_WOT- con nota legacy.
- legacy-compat: audit_plan.md stub (1), archive_collaboration_artifacts.py (3),
  pre_handoff_guard.py (6), validate_ticket_prose.py (4) — todos etiquetados.
- bug: 0.
- no clasificado fuera de seccion legacy: 0.
Generadores de ID legacy activos (Plan ID/ID con WP-/WT-): CERO.

## Gates finales

```
python scripts/check_encoding_guard.py            # exit 0
ruff check .                                       # exit 0 - All checks passed!
python -m pytest [consumidores tocados, 299 tests] # 299 passed
python -m pytest [barrera canonical, 75 tests]     # 75 passed
python scripts/discover_skills.py --check-contract # exit 0 (rename no rompe dispatch)
python .agent/agent_controller.py --validate --json --project-root <destino>  # 0/0
```
