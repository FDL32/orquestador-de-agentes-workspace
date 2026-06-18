# STRATEGY_WOT-2026-008c.md

## Enfoque

1. Confirmar premisas vivas: dependencia 008b cerrada, layout real de `prompts/` y `skills/`, estado de `docs/registry/` y consumidores actuales.
2. Disenar el registry como artefacto generado determinista, con orden estable y campos pequenos pero suficientes para desbloquear 008d.
3. Generar `docs/registry/INDEX.md` desde la misma fuente; no mantener dos verdades manuales.
4. Anadir check stale que regenere en memoria o compare contra output esperado y falle con remediacion clara.
5. Mantener discovery/collision con paridad observable. Si no hace falta tocarlos, documentar la razon y no inventar acoplamiento.

## Campos minimos sugeridos

- `path`
- `artifact_type`
- `owner`
- `source`
- `canonical_source`
- `status`
- `aliases`
- `triggers`
- `disable_model_invocation`
- `compat_notes`

El Builder puede ajustar nombres si mantiene equivalencia semantica y lo documenta.

## Tests esperados

- Test de generacion determinista del registry.
- Test de stale-check que falla si `INDEX.md` o registry divergen.
- Test de cobertura minima para prompts y skills reales.
- Tests existentes de discovery/collision si esas superficies se tocan.

## Riesgos

- Scope creep hacia 008d: cualquier move/rename/shim migration debe parar.
- Registry demasiado ambicioso: preferir campos utiles y verificables a modelado perfecto.
- Drift por escritura manual: el INDEX debe derivarse, no editarse a mano.
- Consumidores vivos no identificados: si aparece uno no clasificable, CONTRACT_GAP.

## Gates

- `python -m pytest <tests focales>` o runner seguro si el Builder lo prefiere.
- `ruff check` y `ruff format --check` sobre Python tocado.
- `python scripts/check_encoding_guard.py <archivos tocados>`.
- `python scripts/run_pytest_safe.py --level all` antes de handoff para cumplir 010q.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` en 0/0.