# Work Plan: WOT-2026-005d - Audit completo motor-destino: patrones host-extends y memoria

## Metadata
- **ID:** WOT-2026-005d
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Elevar los incidentes 002/003 a patrones estrategicos en el audit completo: resolvers/bootstraps, fail-open, bus no-verificable y capas de memoria
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (cambio documental; reversible via git)
- **Depende de:** WOT-2026-005c (completed)
- **Origen:** session-2026-06-14-host-extends-learnings

## Decision Arquitectonica
El audit completo debe evaluar la integracion motor-destino de CUALQUIER destino (no solo
este dogfooding), elevando los incidentes host-extends a patrones estrategicos sin incrustar
cronica. Se endurecen secciones existentes (portabilidad, calidad, observabilidad, fuentes)
para cubrir resolvers/bootstraps, fail-open en validators/hooks/launchers/CI, distincion
bus-ausente vs bus-violado, y memoria por capas con chequeo de promocion por schema. Se
referencian las fuentes canonicas (005b/005c/005a) en vez de duplicar sus checklists.

## Files Likely Touched (repo_motor)
prompts/audit_complete_motor_destination.md

## Read/inspect only
- `prompts/destination_bootstrap.md`, `skills/orchestrate-pipeline/references/destination-preflight.md`,
  `skills/system-health-audit/SKILL.md`, `prompts/memory_upload.md` (fuentes a referenciar).

## Manager-only
- Revision documental (no toca skill: no requiere skill_collisions, pero se corre por higiene).

## Non-goals
- NO duplicar checklists completas de otros prompts; referenciar fuentes canonicas.
- NO añadir gates ni runtime; NO crear higiene de mojibake masivo (ticket aparte si aparece).

## Criterios binarios de cierre
- [ ] La seccion de portabilidad exige auditar resolvers/bootstraps ademas de imports.
- [ ] La seccion de calidad incluye fail-open en validators, hooks, launchers, CI y
      fallback/stubs de topologia.
- [ ] Observabilidad distingue `bus ausente/no verificable` de `bus presente/evento violado`
      (especialmente CI o clone limpio).
- [ ] Memoria evalua por separado Claude privada, portable motor y portable destino, y
      comprueba si el schema real permite promocion.
- [ ] Fuentes minimas incluyen `destination_bootstrap.md`, `orchestrate-pipeline/SKILL.md`,
      `destination-preflight.md`, `system-health-audit/SKILL.md` y `memory_upload.md`.
- [ ] `check_encoding_guard.py` pasa; validate destino 0; motor solo este archivo; commit con WOT-2026-005d.

## STOP / escalado
- No duplicar checklists de 005b/005c; referenciar fuentes canonicas.
- Si aparece mojibake masivo no acotado, abrir higiene separada (no mezclar aqui).

## Gates (deliverable_type: documentation)
- `check_encoding_guard.py prompts/audit_complete_motor_destination.md`.
- `check_skill_collisions.py` exit 0 (higiene; no se toca skill).
- `validate --project-root .` 0; `check_motor_pristine --check` (solo este archivo).

## Entregables
- `prompts/audit_complete_motor_destination.md` endurecido.
- `orchestrator_pipeline/reports/closeout_WOT-2026-005d.md`.
