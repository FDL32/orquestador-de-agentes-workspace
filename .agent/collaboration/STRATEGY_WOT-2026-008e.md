# STRATEGY_WOT-2026-008e.md

## Enfoque

1. Baseline read-only: discovery naming, contract, collisions, json y rg de consumidores.
2. Crear `prompts/manager_review.md` como copia canonica del prompt actual.
3. Convertir `prompts/review_manager.md` en stub-alias compatible estilo `audit_plan.md`.
4. Actualizar consumidores vivos al canonico cuando sea seguro: `source_prompt` de `man-review-implementation` y prose en skills/prompts declarados por DEC.
5. Retirar `review_manager` de `KNOWN_LEGACY_NAMES` y ajustar tests.
6. Regenerar INDEX/README solo si discovery proyecta alias/naming metadata.

## Tests esperados

- `tests/test_check_naming.py`: review_manager ya no necesita estar en `KNOWN_LEGACY_NAMES`; manager_review pasa; stub legacy no rompe el gate.
- `tests/test_discover_skills.py`: `--check-contract` pasa con `source_prompt` actualizado.
- Focal real sobre archivos tocados.

## Riesgos

- Romper `source_prompt`: bloquear.
- Dejar prose viva apuntando al nombre antiguo sin ser stub/docs historicas: bloquear.
- Borrar alias legacy en vez de stub: bloquear.
- Ampliar rename a otros prompts: bloquear.

## Gates

- `python scripts/discover_skills.py --check-naming`
- `python scripts/discover_skills.py --check-contract`
- `python scripts/check_skill_collisions.py`
- `python scripts/discover_skills.py --json`
- `python -m pytest tests/test_check_naming.py tests/test_discover_skills.py -v` mas tests focales reales
- `ruff check` y `ruff format --check` sobre Python tocado
- `python scripts/check_encoding_guard.py <archivos tocados>`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0