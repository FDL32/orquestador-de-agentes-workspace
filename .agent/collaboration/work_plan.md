# work_plan.md -- WOT-2026-008g

## Metadata

- **ID:** WOT-2026-008g
- **Contract ID:** T-008G-001
- **Estado:** READY_TO_START
- **ROL activo esperado:** BUILDER
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Crear la DEC de vocabulario y naming por rol que fija el contrato terminologico del sistema: backend IA vs rol vs artefacto, roles canonicos, regla actor_/family_, tabla congelada de prompts y plan de migracion por lotes. Este ticket es documental: sin renames, sin frontmatter, sin tocar 008f.

Para verificar el cumplimiento, se validará que existe `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md` y `AGENTS.md` actualizados, y que la ejecución de `python .agent/agent_controller.py --validate --json` finaliza con 0 errors y 0 warnings (una vez bootstrap-ticket emita el evento correspondiente).

## Non-goals

- No realizar renames físicos de archivos de prompts, skills o scripts.
- No modificar el frontmatter de ningún prompt o skill (por ejemplo, el campo `role` u otros).
- No modificar la lógica runtime de bus, supervisor ni ningún componente runtime.


## Premisas verificadas antes de Builder

- WOT-2026-008f esta COMPLETED antes de materializar 008g.
- WOT-2026-008d y WOT-2026-008e estan COMPLETED y sirven como base de naming + rename piloto.
- DEC-008D-001 existe; 008g formaliza una regla implicita en _PIPELINE_ACTIONS / --check-naming, no afirma que esa regla ya estuviera escrita.
- supervisor ya existe como actor runtime del bus; la DEC lo documenta, no lo redefine.
- audit_* es familia transversal de tarea, no propiedad del rol auditor.

## Decision Arquitectonica

La autoridad del ticket sera docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md en repo_motor. AGENTS.md se actualiza solo para reflejar la distincion Backends y roles. Los renames quedan serializados a tickets posteriores con shims.

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

## Fase 0 obligatoria

1. Confirmar T-008G-001 frozen y WOT-2026-008f COMPLETED.
2. Inventariar prompts fisicos y confirmar la tabla de 20 entradas.
3. Confirmar que supervisor existe como runtime (`bus/supervisor.py`, `actor="SUPERVISOR"`).
4. Confirmar que audit_* tiene consumidores multi-rol o transversales y no debe forzarse a auditor_*.
5. Registrar en execution_log.md los comandos usados y cualquier discrepancia.

## Criterios binarios

- Existe `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`.
- La DEC contiene vocabulario canonico, roles canonicos, supervisor-runtime, regla actor/family, criterio de desempate, tabla congelada de prompts y plan de lotes.
- AGENTS.md contiene la seccion Backends y roles con backend IA / rol / artefacto / supervisor.
- La tabla clasifica 20 prompts fisicos: 5 futuros orchestrator_*, 1 manager_*, 12 audit_* family, 1 memory_* family, 1 contract_formation_* family y 1 legacy stub.
- La DEC no dice que DEC-008D-001 ya escribia family-wins; dice que 008g formaliza un mecanismo implicito en _PIPELINE_ACTIONS / --check-naming.
- `python scripts/discover_skills.py --check-naming` pasa.
- `python scripts/check_encoding_guard.py docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md AGENTS.md` pasa.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.
- El diff del repo_motor se limita a la DEC y AGENTS.md; no hay renames.

## CONTRACT_GAP behavior

Emitir CG-WOT-2026-008g.md si algun prompt no puede clasificarse con la regla actor/family, si AGENTS.md requiere reescritura amplia fuera de vocabulario, si la DEC necesita tocar codigo/runtime, o si la tabla congelada contradice el inventario real.

## STOP conditions

Parar si aparece cualquier rename, frontmatter edit, cambio de bus/runtime, dependencia nueva o cambio productivo ajeno a DEC/AGENTS.md.