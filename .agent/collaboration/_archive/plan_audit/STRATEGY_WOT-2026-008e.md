# STRATEGY_WOT-2026-008e.md

## Enfoque

1. Baseline read-only: discovery naming, contract, collisions, json, check-index y rg de consumidores.
2. Crear `prompts/manager_review.md` como copia canonica del prompt actual.
3. Convertir `prompts/review_manager.md` en stub-alias compatible estilo `audit_plan.md`; `audit_plan.md` es precedente solo de forma de stub, no del mecanismo de tolerancia.
4. Adoptar explicitamente Opcion B: `manager_review.md` sera el primer prompt con frontmatter YAML; `--check-naming` debe reutilizar `parse_frontmatter()` existente, no un parser nuevo.
5. Anadir frontmatter YAML en `prompts/manager_review.md` con `legacy_aliases: [review_manager]`, preservando en el cuerpo las lineas literales `Skill canonica: skills/man-review-implementation/SKILL.md` y `contract_id: cid-man-review-v2`.
6. Extender `_check_prompt_names` / `--check-naming` para parsear frontmatter de prompts canonicos y tolerar stubs cuyo stem aparezca en `legacy_aliases`.
7. Actualizar consumidores vivos al canonico cuando sea seguro: `source_prompt` de `man-review-implementation` y prose en skills/prompts declarados por DEC.
8. Retirar `review_manager` de `KNOWN_LEGACY_NAMES` y ajustar tests.
9. Regenerar `docs/registry/INDEX.md` con `discover_skills.py --generate-index` y verificar `--check-index`.

## Tests esperados

- `tests/test_check_naming.py` (modifica existente): reescribir `test_legacy_name_tolerated` para que la tolerancia venga de frontmatter `legacy_aliases`, no de `KNOWN_LEGACY_NAMES`.
- `tests/test_check_naming.py` (modifica existente): reescribir `test_legacy_tolerance_masks_a_real_detection` como barrera equivalente: sin alias declarado, el stub `review_manager` falla `--check-naming`; con alias declarado, pasa.
- `tests/test_check_naming.py` (nuevo caso): verifica que `parse_frontmatter()` parsea el frontmatter real de un prompt canonico con `legacy_aliases: [review_manager]`.
- `tests/test_discover_skills.py` (modifica existente): `--check-contract` pasa con `source_prompt: prompts/manager_review.md` y el cuerpo conserva `Skill canonica: skills/man-review-implementation/SKILL.md` + `contract_id: cid-man-review-v2`.
- Focal real sobre archivos tocados.

## Riesgos

- Romper `source_prompt`: bloquear.
- Mover `contract_id` o `Skill canonica` solo al YAML y romper `--check-contract`: bloquear.
- Dejar prose viva apuntando al nombre antiguo sin ser stub/docs historicas: bloquear.
- Borrar alias legacy en vez de stub: bloquear.
- Ampliar rename a otros prompts: bloquear.

## Gates

- `python scripts/discover_skills.py --check-naming`
- `python scripts/discover_skills.py --check-contract`
- `python scripts/check_skill_collisions.py`
- `python scripts/discover_skills.py --json`
- `python scripts/discover_skills.py --generate-index`
- `python scripts/discover_skills.py --check-index`
- `rg "review_manager|manager_review" prompts skills scripts docs tests --glob "!**/sandbox/**"`
- `python -m pytest tests/test_check_naming.py tests/test_discover_skills.py -v` mas tests focales reales
- `ruff check` y `ruff format --check` sobre Python tocado
- `python scripts/check_encoding_guard.py <archivos tocados>`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0