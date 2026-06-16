# Execution Log: WOT-2026-008b - Discovery/frontmatter hardening

## Metadata

**Estado:** READY_FOR_REVIEW
- **ID:** WOT-2026-008b
- **Contract ID:** T-008B-001
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Rol activo:** MANAGER
- **Accion:** CREATE_PLAN

## Baseline

- Motor HEAD: 7848018 (docs: align destination lifecycle setup guidance)
- Destino HEAD: 32d4581 (docs: refine 008 taxonomy backlog contract)
- Validate previo: 0/0 (VERIFICADO 2026-06-16)
- BOM confirmado: `skills/man-review-implementation/SKILL.md` (efbbbf)
- Discovery gap: 28/29 SKILL.md visibles; --check-contract exit 0 (falso verde)

## Plan creado

- `work_plan.md`: APPROVED
- `PLAN_WOT-2026-008b.md`: estrategia tecnica completa
- `AUDIT_WOT-2026-008b.md`: TP Check + STOP conditions + checklist adversarial
- Validate post-plan: pendiente (ejecutar tras bootstrap-ticket)

## Phase 3: Tests de regresion (TDD — barrera primero)

- Archivo: `tests/unit/test_discover_skills_bom.py` (nuevo, repo_motor)
- 7 tests: 4 FAILED pre-fix (barrera verificada), 7 PASSED post-fix
- TestBomVisibility: test_bom_skill_is_discovered, test_bom_skill_not_lost_in_multi_skill_dir, test_parse_frontmatter_handles_bom
- TestCheckContractBom: test_check_contract_detects_bom_skill_with_missing_prompt, test_check_contract_passes_for_bom_skill_without_contract_fields
- TestBomBarridoReal: test_no_bom_in_skill_files, test_no_bom_in_prompts

## Phase 1: Fix discover_skills.py

- Archivo: `scripts/discover_skills.py:72` (repo_motor)
- Cambio: `encoding="utf-8"` → `encoding="utf-8-sig"` en `parse_frontmatter()`
- Efecto: BOM consumido transparentemente; `content.startswith("---")` ahora True para archivos BOM

## Phase 2: Eliminar BOM de SKILL.md

- Archivo: `skills/man-review-implementation/SKILL.md` (repo_motor)
- BOM pre-fix: bytes `efbbbf` al inicio (detectado via `open(path,'rb').read()[:3]`)
- BOM post-fix: primeros bytes = `2d2d2d` = `---` (frontmatter correcto)
- Discovery post-fix: 29/29 SKILL.md visibles; `--check-contract` exit 0 correcto

## Phase 4: Barrido BOM

- Barrido `skills/**/SKILL.md`: 29 archivos. BOM encontrado: ninguno post-fix.
  El unico BOM era `skills/man-review-implementation/SKILL.md` (eliminado en Phase 2).
- Barrido `prompts/*.md`: todos sin BOM. test_no_bom_in_prompts PASSED confirma.
- Evidencia: `TestBomBarridoReal::test_no_bom_in_skill_files PASSED` y
  `TestBomBarridoReal::test_no_bom_in_prompts PASSED` (2026-06-16)

## Phase 5: Clasificacion ghost triggers

Fuentes: `agents.json` skill_allowlists (destino) + `discover_skills.py --json` post-fix.

- Vivos (trigger en FM): /implement, /tdd, /debug, /refactor, /review, /compare, /schedule — 7 triggers
- BOM-casualty restaurado: /review (era invisible por BOM; ahora vivo en man-review-implementation)
- Ghost-pending (allowlist, sin skill FM): /impl, /test, /fix, /validate, /inspect, /orchestrate, /archive, /report — 8 triggers
- Ghost-partial: /audit (self-audit tiene `audit` sin slash en FM; allowlist usa /audit con slash)
- Deuda documentada: 8 ghost-pending + 1 ghost-partial. Accion: tickets 008e/008f o nuevo ticket.
  No bloquea cierre de 008b.

Artefacto: `docs/decisions/DEC-008B-002-discovery-triggers.md` — tabla completa derivada.

## Phase 6: DECs

- `docs/decisions/DEC-008B-001-registry-model.md`: 4 opciones comparadas; DECIDED: discovery recursivo sin manifest (opcion 4 — estado actual)
- `docs/decisions/DEC-008B-002-discovery-triggers.md`: 3 opciones comparadas; DECIDED: triggers en frontmatter como API propia (opcion A)
- Ambos artefactos existen en disco, repo_motor. Verificable con ls.


Scope override: docs/decisions/ DEC files are declared in work_plan under Files Likely Touched as DEC-008B-001-registry-model.md and DEC-008B-002-discovery-triggers.md; skills/man-review-implementation/SKILL.md and tests/unit/test_discover_skills_bom.py are explicitly listed; all 5 files are within the declared scope of WOT-2026-008b. Affected files: docs/decisions/DEC-008B-001-registry-model.md, docs/decisions/DEC-008B-002-discovery-triggers.md, skills/man-review-implementation/SKILL.md, tests/unit/test_discover_skills_bom.py