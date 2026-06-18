# Work Plan: WOT-2026-010s

> Origen: `WOT-2026-010r` decidio adoptar de forma hibrida la taxonomia user-invoked/model-invoked inspirada en `mattpocock/skills`. Este ticket implementa soporte compatible; NO retira `triggers:` de los SKILL.md.

## Metadata

- **ID:** WOT-2026-010s
- **Contract ID:** T-010S-001
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010r (completed), WOT-2026-010t (completed)

## Objetivo

Introducir soporte backward-compatible para `disable-model-invocation` en discovery/resolution de skills sin romper `trigger_map`. Las skills user-invoked pueden conservar `triggers:` para compatibilidad de dispatch, pero quedan marcadas como no invocables por modelo. Las skills model-invoked siguen disponibles para auto-invocacion cuando su metadata lo permita.

## Hechos verificados de arranque

- `010r` esta cerrado y documenta seis consumidores reales de `triggers`.
- `010t` esta cerrado y aporta vocabulario de review para evitar seams inventados.
- `disable-model-invocation` no existe aun en skills locales.
- `triggers:` existe en los SKILL.md y se consume para `trigger_map`; retirarlo en masa seria breaking.
- Ticket scope ajustado: el backlog decia "retirar triggers"; este contrato lo corrige a migracion hibrida segura. La retirada queda fuera de 010s.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar codigo:

- consumidores reales de `triggers`: `scripts/discover_skills.py`, `bus/skill_resolver.py`, `scripts/check_skill_collisions.py`, `scripts/local_audit.py`, `scripts/orquestador.py`, `scripts/validate_agent_config.py`;
- tests existentes para discovery/resolver/collisions: `tests/test_discover_skills.py`, `tests/unit/test_skill_discovery.py`, `tests/test_check_skill_collisions.py`, `tests/test_approval_state_revision_and_skill_access.py`;
- formato actual de `python scripts/discover_skills.py --json` y claves que produce;
- si `v1.0.1` del repo externo cambia `docs/invocation.md`; si invalida el contrato, emitir CONTRACT_GAP.

Nota operativa: evita `rg` sobre `tests/sandbox/test_runtime/**` sin exclusiones; hay carpetas `opencode-review-*` con acceso denegado que no son fallo del contrato.

Registrar en `execution_log.md`:

- consumidores confirmados;
- baseline `trigger_map` antes del cambio;
- decision hibrida: `triggers` se conserva, `disable-model-invocation` se anade como metadata semantica.

## Files Likely Touched

### repo_motor
- `scripts/discover_skills.py`
- `bus/skill_resolver.py`
- `scripts/check_skill_collisions.py`
- `scripts/local_audit.py`
- `scripts/orquestador.py`
- `scripts/validate_agent_config.py`
- `tests/test_discover_skills.py`
- `tests/unit/test_skill_discovery.py`
- `tests/test_check_skill_collisions.py`
- `tests/test_approval_state_revision_and_skill_access.py`
- `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`
- `CREDITS.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010s.md`
- `.agent/collaboration/AUDIT_WOT-2026-010s.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`
- `.agent/planning/ticket_contracts.md`

## Read/inspect only

- `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
- `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`
- `skills/*/SKILL.md`
- `prompts/`
- `.agent/runtime/events/`

## Manager-only

- verificar que `trigger_map` no se rompe;
- verificar que `disable-model-invocation` no se usa como excusa para ocultar skills del dispatch manual;
- verificar que no se copia bundle externo;
- verificar que no se hace retirada masiva de `triggers:`.

## Decision Arquitectonica

- Migracion hibrida: `triggers` sigue siendo el contrato de dispatch manual/legacy.
- `disable-model-invocation: true` significa user-invoked: el modelo no debe auto-invocar esa skill, pero un humano/trigger explicito puede seguir usandola.
- Ausencia del campo equivale a backward-compatible model-invoked por defecto, salvo reglas locales existentes.
- `discover_skills.py` debe exponer metadata suficiente para que consumidores posteriores distingan `user_invoked` vs `model_invoked` sin romper claves existentes.
- La paridad de `trigger_map` antes/despues es barrera obligatoria.

## Criterios Binarios

- [ ] `discover_skills.py` parsea `disable-model-invocation` como booleano estable y lo expone en cada skill descubierta.
- [ ] `trigger_map` de `discover_skills.py --json` conserva los mismos triggers para skills existentes antes/despues del cambio.
- [ ] `bus/skill_resolver.py` respeta la metadata sin romper allowlists por nombre o trigger.
- [ ] `check_skill_collisions.py`, `local_audit.py`, `orquestador.py` y `validate_agent_config.py` no interpretan mal el nuevo campo.
- [ ] Hay tests de barrera para `disable-model-invocation: true`, ausencia del campo, valor invalido y paridad de `trigger_map`.
- [ ] `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md` documenta la semantica local, compatibilidad y ruta de retirada futura.
- [ ] `CREDITS.md` incluye fila `WOT-2026-010s` con source pinneado, licencia MIT y `Adapted`.
- [ ] No se eliminan `triggers:` de los SKILL.md en este ticket.
- [ ] No se toca bus runtime ni eventos manualmente.
- [ ] Tests focales pasan, ruff/format pasan, encoding guard pasa y `validate --json` termina 0 errors / 0 warnings.

## Non-goals

- NO retirar `triggers:` de SKILL.md.
- NO cambiar la UX de comandos slash.
- NO copiar archivos del bundle externo.
- NO introducir dependencias.
- NO modificar prompts salvo que se detecte CONTRACT_GAP.
- NO tocar `privada/`, `.env`, bus runtime ni eventos manualmente.

## Forbidden Surfaces

- `skills/*/SKILL.md` para retirada masiva de `triggers:`
- `prompts/`
- `pyproject.toml`
- `uv.lock`
- `.agent/runtime/events/`
- `.agent/runtime/reviews/`
- bundle externo copiado
- `privada/`
- `.env`