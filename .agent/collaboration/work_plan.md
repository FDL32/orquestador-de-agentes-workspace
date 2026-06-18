# work_plan.md -- WOT-2026-008g

## Metadata

- **ID:** WOT-2026-008g
- **Contract ID:** T-008G-001
- **Estado:** COMPLETED
- **ROL activo esperado:** MANAGER
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Crear y revisar una DEC documental verificable para vocabulario y naming por rol. Cumplimiento medible: existe `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`, `AGENTS.md` contiene "Backends y roles", `discover_skills.py --check-naming` termina en exit 0, encoding guard termina en exit 0 y `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.

## Non-goals

- No realizar renames fisicos de prompts, skills o scripts.
- No modificar frontmatter de prompts o skills.
- No modificar bus, supervisor runtime ni eventos.
- No expandir man-/bui- a manager-/builder-.

## Premisas verificadas antes de Builder

- WOT-2026-008f esta COMPLETED.
- WOT-2026-008d y WOT-2026-008e estan COMPLETED y son la base de naming + rename piloto.
- DEC-008D-001 existe; 008g formaliza una regla implicita en _PIPELINE_ACTIONS / --check-naming.
- supervisor ya existe como actor runtime del bus; la DEC lo documenta, no lo redefine.
- audit_* es familia transversal de tarea, no propiedad del rol auditor.

## Decision Arquitectonica

La autoridad del ticket es `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md` en repo_motor. `AGENTS.md` se actualiza solo para reflejar la distincion Backends y roles.

## Files Likely Touched

### repo_motor

- `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
- `AGENTS.md`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `prompts/`
- `skills/`
- `bus/supervisor.py`
- `.agent/agent_controller.py`
- `docs/decisions/DEC-008D-001-naming-convention.md`
- `scripts/discover_skills.py`

## Manager-only

- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-008g.md`
- `.agent/collaboration/AUDIT_WOT-2026-008g.md`
- `.agent/planning/ticket_contracts.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- Renames o moves de prompts, skills o scripts.
- Modificar frontmatter.
- Tocar WOT-2026-008f o sus artefactos productivos.
- Expandir man-/bui- a manager-/builder-.
- Tocar bus runtime/events manualmente.
- Dependencias nuevas.
- `privada/` o `.env`.

## Entregables

1. `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`.
2. `AGENTS.md` con seccion "Backends y roles".
3. Evidencia en `execution_log.md`.

## Criterios binarios

- Existe la DEC en repo_motor.
- La DEC contiene vocabulario canonico, roles canonicos, supervisor runtime, regla actor/family, criterio de desempate, tabla congelada y plan de lotes.
- La tabla clasifica 20 prompts fisicos: 5 futuros orchestrator_*, 1 manager_*, 12 audit_* family, 1 memory_* family, 1 contract_formation_* family y 1 legacy stub.
- AGENTS.md contiene "Backends y roles".
- `python scripts/discover_skills.py --check-naming` pasa.
- `python scripts/check_encoding_guard.py docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md AGENTS.md` pasa.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.
- Diff de repo_motor limitado a DEC + AGENTS.md.
- No hay renames ni frontmatter.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008g.md` y parar si algun prompt no puede clasificarse con actor/family, si la DEC requiere codigo/runtime, si la tabla contradice el inventario real o si aparece un rename.