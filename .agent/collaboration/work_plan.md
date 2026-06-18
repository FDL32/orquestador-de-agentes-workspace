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

Crear un registry generado y verificable para prompts/skills y una proyeccion `docs/registry/INDEX.md` derivada de esa fuente. El ticket debe dejar una base estable para `WOT-2026-008d` sin mover, renombrar ni retirar artefactos.

## Premisas verificadas antes de Builder

- `WOT-2026-008b` esta cerrado y es la dependencia directa de `008c`.
- `WOT-2026-010r`, `WOT-2026-010s`, `WOT-2026-010t` y `WOT-2026-010u` estan cerrados; informan el diseno, pero no amplian el scope de `008c`.
- El registry debe ser una autoridad generada, no una lista manual mantenida a mano.
- La migracion de naming/shims pertenece a `WOT-2026-008d`, no a este ticket.


## Decision Arquitectonica

El ticket adopta un registry generado manifest-first como fuente canonica y conserva `INDEX.md` como proyeccion humana derivada. La decision reduce drift antes de `008d`, mantiene discovery/collision verificables y evita que una migracion de nombres se base en inventario manual.

## Non-goals

- No migrar naming, shims ni aliases de `WOT-2026-008d`.
- No mover, renombrar ni borrar prompts o skills.
- No cambiar politica de invocation ni retirar `triggers:`.
- No instalar dependencias ni copiar bundles externos.
## Files Likely Touched

### repo_motor - Builder

- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/generate_registry_catalog.py`
- `scripts/check_registry_catalog.py`
- `docs/registry/README.md`
- `docs/registry/INDEX.md`
- `docs/registry/registry.json`
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
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- No mover, renombrar ni borrar carpetas de `prompts/` o `skills/`.
- No retirar `triggers:` ni cambiar la semantica de `disable-model-invocation`.
- No copiar bundles externos ni instalar dependencias.
- No tocar `pyproject.toml`, `uv.lock`, bus runtime/events, `privada/` ni `.env`.
- No ejecutar la migracion de naming/shims de `WOT-2026-008d`.

## Impact Simulation

| Superficie | Impacto esperado | Riesgo | Mitigacion | Paralelizable |
|------------|------------------|--------|------------|---------------|
| `docs/registry/registry.json` | Nueva fuente generada versionada | stale o orden no determinista | check de regeneracion + tests de orden estable | No con 008d |
| `docs/registry/INDEX.md` | Proyeccion humana generada | drift manual | check que compare contenido generado | No con 008d |
| discovery/collision | Puede reutilizar metadata o conservar paridad | romper trigger_map o collisions | tests existentes + paridad observable | No con 010s ya cerrado |
| prompts/skills layout | Solo lectura | scope creep hacia moves | Forbidden Surfaces + CONTRACT_GAP | No con migraciones |
| repo_destino | Estado operativo del ticket | drift de bus/proyecciones | bootstrap + validate 0/0 | No |

## Criterios binarios de cierre

- Existe un registry generado determinista en `docs/registry/registry.json` o equivalente declarado por Builder.
- `docs/registry/INDEX.md` se genera desde el registry y no queda como indice manual divergente.
- Existe un check que falla si registry o INDEX estan stale respecto a prompts/skills reales.
- El registry cubre prompts, skills, `PROMPT_TEMPLATE.md`, referencias/templates compartidas y consumidores relevantes declarados por `008a/008b`.
- Cada entrada incluye ruta, tipo de artefacto, owner/source, canonical_source, estado, aliases/triggers cuando aplique y notas de compatibilidad si existen shims.
- Se distingue layout fisico de alias logico; no se ejecuta ninguna migracion de naming/shims de `008d`.
- Discovery/collision conservan paridad observable o documentan por que quedan read-only.
- Tests focales, ruff, encoding guard y `validate --json --project-root <repo_destino>` terminan en verde.

## STOP / CONTRACT_GAP

Emitir `CG-WOT-2026-008c.md` y detener si el inventario no puede generarse deterministamente, si el INDEX no puede derivarse del registry, si aparece consumidor vivo no clasificable, si el cambio exige migrar nombres/shims, o si el stale-check solo puede ser pass-open.

## Instruccion de arranque Builder

Antes de implementar, releer `prompts/launch_builder.md`, confirmar `STATE.md/TURN.md` apuntando a `WOT-2026-008c`, ejecutar validate 0/0, y registrar Fase 0 en `execution_log.md`. Builder no debe tocar superficies Manager-only salvo `execution_log.md`.