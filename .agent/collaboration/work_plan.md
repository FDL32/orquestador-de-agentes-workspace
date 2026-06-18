# work_plan.md -- WOT-2026-008c

## Metadata

- **ID:** WOT-2026-008c
- **Contract ID:** T-008C-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Formalizar `docs/registry/INDEX.md` como proyeccion generada por discovery recursivo y anadir una barrera stale-check que falle si el indice queda desactualizado respecto a `discover_skills.py --generate-index`. El ticket respeta `DEC-008B-001`: no crea `registry.json` ni introduce manifest central.

## Premisas verificadas antes de Builder

- `WOT-2026-008b` esta cerrado y es la dependencia directa de `008c`.
- `DEC-008B-001` adopta Opcion 4: discovery recursivo sin manifest.
- `DEC-008B-001` prohibe crear `registry.json` en `008c`.
- `docs/registry/INDEX.md` ya declara ser autogenerado por `discover_skills.py --generate-index`.
- La migracion de naming/shims pertenece a `WOT-2026-008d`, no a este ticket.

## Decision Arquitectonica

`008c` sigue la decision congelada `DEC-008B-001`: el filesystem y el frontmatter de `SKILL.md` siguen siendo la autoridad; `INDEX.md` es una proyeccion generada para humanos. La barrera nueva debe detectar drift del indice, no crear una segunda fuente de verdad.

## Non-goals

- No crear `docs/registry/registry.json` ni ningun manifest central equivalente.
- No crear `generate_registry_catalog.py` ni `check_registry_catalog.py`.
- No migrar naming, shims ni aliases de `WOT-2026-008d`.
- No mover, renombrar ni borrar prompts o skills.
- No cambiar politica de invocation ni retirar `triggers:`.
- No instalar dependencias ni copiar bundles externos.

## Files Likely Touched

### repo_motor - Builder

- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `docs/registry/README.md`
- `docs/registry/INDEX.md`
- `tests/test_registry_catalog.py`
- `tests/test_discover_skills.py`
- `tests/test_check_skill_collisions.py`

### repo_motor - Read/inspect only

- `docs/decisions/DEC-008B-001-registry-model.md`
- `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`
- `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
- `skills/`
- `prompts/`
- `scripts/local_audit.py`
- `scripts/validate_agent_config.py`
- `bus/skill_resolver.py`

### repo_destino - Builder

- `.agent/collaboration/execution_log.md`

### repo_destino - Manager-only

- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/AUDIT_WOT-2026-008c.md`
- `.agent/collaboration/STRATEGY_WOT-2026-008c.md`
- `.agent/planning/ticket_contracts.md`
- `.agent/planning/contract_gaps/CG-WOT-2026-008c.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- No crear `registry.json` o manifest central.
- No mover, renombrar ni borrar carpetas de `prompts/` o `skills/`.
- No retirar `triggers:` ni cambiar la semantica de `disable-model-invocation`.
- No copiar bundles externos ni instalar dependencias.
- No tocar `pyproject.toml`, `uv.lock`, bus runtime/events, `privada/` ni `.env`.
- No ejecutar la migracion de naming/shims de `WOT-2026-008d`.

## Impact Simulation

| Superficie | Impacto esperado | Riesgo | Mitigacion | Paralelizable |
|------------|------------------|--------|------------|---------------|
| `discover_skills.py --generate-index` | Autoridad generadora del indice | cambiar discovery sin querer | tests de paridad y snapshot controlado | No con 008d |
| `docs/registry/INDEX.md` | Proyeccion humana generada | drift manual | stale-check que compare output generado | No con 008d |
| discovery/collision | Puede requerir helper/check de stale | romper trigger_map o collisions | tests existentes + paridad observable | No con 010s ya cerrado |
| prompts/skills layout | Solo lectura | scope creep hacia moves | Forbidden Surfaces + CONTRACT_GAP | No con migraciones |
| repo_destino | Estado operativo del ticket | drift de bus/proyecciones | bootstrap + validate 0/0 | No |

## Criterios binarios de cierre

- `docs/registry/INDEX.md` se genera desde `discover_skills.py --generate-index` o comando equivalente ya existente en discovery.
- Existe un stale-check que falla si `INDEX.md` diverge del output generado.
- El check no crea ni requiere `registry.json`.
- El indice generado cubre las skills descubiertas y conserva metadata relevante ya soportada por discovery, incluido `status`, `triggers` y `disable-model-invocation` cuando aplique.
- Se documenta en `docs/registry/README.md` que el modelo vigente es discovery recursivo sin manifest central.
- Se distingue layout fisico de alias logico; no se ejecuta ninguna migracion de naming/shims de `008d`.
- Discovery/collision conservan paridad observable o documentan por que quedan read-only.
- Tests focales, ruff, encoding guard, suite canonica y `validate --json --project-root <repo_destino>` terminan en verde.

## STOP / CONTRACT_GAP

Emitir `CG-WOT-2026-008c.md` y detener si el INDEX no puede derivarse de discovery, si aparece consumidor vivo no clasificable, si el cambio exige crear `registry.json`, si exige migrar nombres/shims, o si el stale-check solo puede ser pass-open.

## Instruccion de arranque Builder

Antes de implementar, releer `prompts/launch_builder.md`, confirmar `STATE.md/TURN.md` apuntando a `WOT-2026-008c`, ejecutar validate 0/0, y registrar Fase 0 en `execution_log.md`. Builder no debe tocar superficies Manager-only salvo `execution_log.md`.