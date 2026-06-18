# Strategy: WOT-2026-010s

## Enfoque

Implementar una migracion hibrida y conservadora. Primero se anade lectura y exposicion del campo `disable-model-invocation`; despues se actualizan consumidores para que toleren la nueva metadata sin cambiar el dispatch por `triggers`.

## Orden recomendado

1. Capturar baseline de `python scripts/discover_skills.py --json` y guardar conteo/hash de `trigger_map` en `execution_log.md`.
2. Escribir tests rojos para:
   - `disable-model-invocation: true` se parsea como bool true;
   - ausencia del campo conserva comportamiento legacy;
   - valores no booleanos producen diagnostico o fallback explicito, no silencio ambiguo;
   - `trigger_map` no cambia para fixtures legacy.
3. Implementar helper pequeno en `discover_skills.py`, preferiblemente una funcion local tipo `_derive_invocation_mode(fm)` o equivalente.
4. Propagar metadata a consumidores solo donde sea necesario para no romper claves existentes.
5. Documentar semantica local en `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`.
6. Actualizar `CREDITS.md` con source pinneado.

## Riesgos

- Romper `trigger_map` por confundir user-invoked con no-dispatchable.
- Cambiar consumidores que solo necesitaban tolerar una clave nueva.
- Crear un seam innecesario; aplicar AP-16 de 010t.
- Tests falsos verdes si solo verifican presencia de clave y no paridad de dispatch.

## Gates esperados

- `python -m pytest tests/test_discover_skills.py tests/unit/test_skill_discovery.py tests/test_check_skill_collisions.py tests/test_approval_state_revision_and_skill_access.py -q`
- `ruff check scripts/discover_skills.py bus/skill_resolver.py scripts/check_skill_collisions.py scripts/local_audit.py scripts/orquestador.py scripts/validate_agent_config.py tests/test_discover_skills.py tests/unit/test_skill_discovery.py tests/test_check_skill_collisions.py tests/test_approval_state_revision_and_skill_access.py`
- `ruff format --check <mismos paths>`
- `python scripts/check_encoding_guard.py <archivos tocados>`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## CONTRACT_GAP

Emitir CONTRACT_GAP si la implementacion requiere retirar `triggers:`, cambiar prompts, modificar bus runtime, instalar dependencias, o si `v1.0.1` invalida la semantica asumida de `docs/invocation.md`.