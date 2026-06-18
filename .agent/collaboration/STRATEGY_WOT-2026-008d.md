# STRATEGY_WOT-2026-008d.md

## Enfoque

1. Fase 0 read-only: confirmar contrato, 008c cerrado, baseline de discovery/collision/json y consumidores del piloto.
2. Escribir primero `docs/decisions/DEC-008D-001-naming-convention.md`; sin DEC no se renombra nada.
3. Implementar `discover_skills.py --check-naming` como autoridad preferente de naming, con tests fail-closed.
4. Integrar el gate en `scripts/run_gates_dispatch.py` para que los perfiles aplicables lo ejecuten.
5. Aplicar como maximo un piloto pequeno y reversible, con shim/stub legacy y referencias prose/frontmatter actualizadas atomicamente.
6. Regenerar/actualizar `docs/registry/INDEX.md` y README solo si los campos de naming declarados lo requieren.

## Tests esperados

- Tests de `discover_skills.py --check-naming`: nombre valido, nombre invalido, legacy permitido, shim permitido y fail-closed.
- Tests de `run_gates_dispatch.py` que demuestren que el gate invoca `--check-naming` en perfiles aplicables.
- Tests de `--check-contract`/frontmatter si se toca prompt/skill piloto.
- Test o evidencia de paridad pre/post de `discover_skills.py --json` salvo renames/aliases declarados.

## Riesgos

- Renombrar antes de DEC: bloquear.
- Crear manifest central contra 008c/DEC-008B: bloquear.
- Convertir `pre_handoff_guard` en God Gate: bloquear.
- Shim que rompe `source_prompt`/`contract_id`: bloquear.
- Scope creep hacia migracion masiva o retirada de shims: bloquear.

## Gates

- `python scripts/discover_skills.py --check-contract`
- `python scripts/check_skill_collisions.py`
- `python scripts/discover_skills.py --check-naming`
- `python -m pytest tests/test_discover_skills.py tests/unit/test_run_gates_dispatch.py -v` mas tests focales reales tocados
- `ruff check` y `ruff format --check` sobre Python tocado
- `python scripts/check_encoding_guard.py <archivos tocados>`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0