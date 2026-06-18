# STRATEGY_WOT-2026-008c.md

## Enfoque

1. Confirmar `DEC-008B-001`: Opcion 4, discovery recursivo sin manifest; `registry.json` queda prohibido en 008c.
2. Confirmar el comando vivo que genera `docs/registry/INDEX.md` desde discovery, empezando por `scripts/discover_skills.py --generate-index`.
3. Anadir o endurecer un stale-check que compare el INDEX versionado con el output generado.
4. Mantener la autoridad en filesystem + frontmatter de `SKILL.md`; el indice es solo proyeccion humana.
5. Mantener discovery/collision con paridad observable. Si no hace falta tocar collision, documentar la razon y no inventar acoplamiento.

## Tests esperados

- Test de generacion determinista de `INDEX.md` desde discovery.
- Test de stale-check que falla si `INDEX.md` queda desactualizado.
- Test que confirma que el flujo no requiere `registry.json`.
- Tests existentes de discovery/collision si esas superficies se tocan.

## Riesgos

- Reintroducir manifest central contra `DEC-008B-001`: bloquear como CONTRACT_GAP.
- Convertir `INDEX.md` en fuente manual: debe quedar generado y verificable.
- Scope creep hacia 008d: cualquier move/rename/shim migration debe parar.
- Drift por metadata nueva de 010s: verificar `disable-model-invocation` sin cambiar su semantica.

## Gates

- `python -m pytest tests/test_registry_catalog.py tests/test_discover_skills.py tests/test_check_skill_collisions.py -v` o subset focal justificado.
- `ruff check` y `ruff format --check` sobre Python tocado.
- `python scripts/check_encoding_guard.py <archivos tocados>`.
- `python scripts/run_pytest_safe.py --level all` antes de handoff para cumplir 010q.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0.