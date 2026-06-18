# work_plan.md -- WOT-2026-008e

## Metadata

- **ID:** WOT-2026-008e
- **Contract ID:** T-008E-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Ejecutar el rename versionado `prompts/review_manager.md` -> `prompts/manager_review.md`, mantener `prompts/review_manager.md` como stub-alias compatible, actualizar los 6 consumidores vivos declarados en `DEC-008D-001`, retirar `review_manager` de `KNOWN_LEGACY_NAMES` sustituyendolo por `legacy_aliases: [review_manager]` en el frontmatter canonico, y cerrar con `python scripts/discover_skills.py --check-naming`, `--check-contract`, `check_skill_collisions.py`, suite canonica y `validate --json` en verde.

## Premisas verificadas antes de Builder

- `WOT-2026-008d` esta COMPLETED y fijo `DEC-008D-001`.
- `DEC-008D-001` asigna explicitamente el rename `review_manager -> manager_review` a `008e`.
- `review_manager` esta tolerado por `KNOWN_LEGACY_NAMES`; 008e debe retirar esa excepcion hardcodeada y reemplazarla por `legacy_aliases: [review_manager]` en `prompts/manager_review.md`.
- El patron de stub-alias vivo existe en `prompts/audit_plan.md`.

## Decision Arquitectonica

`prompts/manager_review.md` sera la fuente canonica. `prompts/review_manager.md` permanecera como stub-alias compatible hasta que 008e demuestre que los consumidores vivos actualizados usan el canonico y que el alias solo queda como superficie de compatibilidad documentada. La compatibilidad no se implementa con manifest central ni sidecar JSON: `discover_skills.py --check-naming` debe leer frontmatter de prompts canonicos, construir el set de aliases declarados y tolerar stubs cuyo stem aparezca en `legacy_aliases`.

## Non-goals

- No migrar otros prompts/skills.
- No tocar bus runtime/events manualmente.
- No crear manifest central, registry.json ni sidecar JSON.
- No tocar `pre_handoff_guard.py` ni politica de gates.
- No retirar otros aliases o shims no relacionados.
- No tocar dependencias.

## Files Likely Touched

### repo_motor

- `prompts/review_manager.md`
- `prompts/manager_review.md`
- `skills/man-review-implementation/SKILL.md`
- `skills/audit-pipeline/SKILL.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `prompts/audit_complete_motor_destination.md`
- `prompts/audit_pipeline.md`
- `prompts/orchestrator_pipeline.md`
- `scripts/discover_skills.py`
- `tests/test_check_naming.py`
- `tests/test_discover_skills.py`
- `docs/registry/INDEX.md`
- `docs/registry/README.md`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/decisions/DEC-008D-001-naming-convention.md`
- `scripts/check_skill_collisions.py`
- `scripts/run_gates_dispatch.py`
- `scripts/pre_handoff_guard.py`
- `bus/`
- `.agent/runtime/events/`

## Manager-only

- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/AUDIT_WOT-2026-008e.md`
- `.agent/collaboration/STRATEGY_WOT-2026-008e.md`
- `.agent/planning/ticket_contracts.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- Bus runtime/events editado manualmente.
- `pre_handoff_guard.py`.
- `registry.json`, manifest central o sidecar JSON.
- Dependencias.
- Rename de otros prompts/skills.
- Borrado de `review_manager.md` sin stub.

## Fase 0 obligatoria

1. Confirmar `T-008E-001` frozen y `008d` completed.
2. Capturar baseline:
   - `python scripts/discover_skills.py --check-naming`
   - `python scripts/discover_skills.py --check-contract`
   - `python scripts/check_skill_collisions.py`
   - `python scripts/discover_skills.py --json`
   - `rg "review_manager|manager_review" prompts skills scripts docs tests --glob "!**/sandbox/**"`
3. Confirmar que los consumidores vivos coinciden con los 6 declarados en la DEC o emitir CONTRACT_GAP.
4. Registrar baseline y seams en `execution_log.md` antes de tocar codigo.

## Criterios binarios

- `prompts/manager_review.md` contiene el prompt canonico y estrena el patron de frontmatter YAML en prompts usando `parse_frontmatter()` existente; incluye `legacy_aliases: [review_manager]` y conserva en el cuerpo, como texto buscable, las lineas literales `Skill canonica: skills/man-review-implementation/SKILL.md` y `contract_id: cid-man-review-v2`.
- `prompts/review_manager.md` queda como stub-alias compatible estilo `audit_plan.md`; `audit_plan.md` es precedente solo de forma de stub, no del mecanismo de tolerancia. `--check-naming` tolera el stub por `legacy_aliases` del canonico parseado con `parse_frontmatter()`, no por `KNOWN_LEGACY_NAMES`.
- Los 6 consumidores vivos declarados en DEC quedan actualizados al canonico o documentan alias de compatibilidad sin romper `--check-contract`.
- `KNOWN_LEGACY_NAMES` ya no contiene `review_manager`; la compatibilidad vive en frontmatter `legacy_aliases`, con tests que fallan si el alias se tolera solo por hardcode.
- `python scripts/discover_skills.py --check-naming` pasa sin excepciones hardcodeadas, lee `legacy_aliases` del prompt canonico con `parse_frontmatter()`, y tiene test del parse real de prompt con frontmatter.
- `python scripts/discover_skills.py --check-contract` pasa.
- `python scripts/check_skill_collisions.py` pasa.
- `python scripts/discover_skills.py --json` conserva paridad funcional de trigger_map; `python scripts/discover_skills.py --generate-index` actualiza el indice y `python scripts/discover_skills.py --check-index` queda verde.
- `rg "review_manager" prompts skills scripts docs tests --glob "!**/sandbox/**"` solo encuentra stub, `legacy_aliases`, docs historicas/deprecacion o tests de compatibilidad; tests se verifican tambien via pytest.
- Tests focales, ruff/format sobre Python tocado, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` pasan en verde.

## CONTRACT_GAP behavior

Emitir `CG-WOT-2026-008e.md` si aparecen consumidores vivos adicionales de alto riesgo, si el stub no puede mantener compatibilidad, si el rename rompe `--check-contract`, o si hay que tocar bus/runtime.

## STOP conditions

Parar si no hay baseline; si hay mas de 6 consumidores vivos no declarados; si no puede mantenerse el stub; si el cambio exige tocar bus/runtime o dependencias; si `--check-contract` no puede quedar verde.