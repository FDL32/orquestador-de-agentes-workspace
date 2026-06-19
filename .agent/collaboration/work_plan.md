# work_plan.md -- WOT-2026-008j

## Metadata

- **ID:** WOT-2026-008j
- **Contract ID:** T-008J-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Renombrar atomicamente las cuatro skills `bui-*` a `builder-*` y migrar sus
consumidores vivos operativos sin tocar `manager-*` ni `audit_*`, sin cambiar
`triggers`, sin romper `prompts/orchestrator_launch_builder.md` ni
`--check-contract`, y preservando la paridad funcional del discovery. El nombre
de directorio de skill se trata como superficie interna del bundle; la
compatibilidad se garantiza actualizando consumidores vivos y manteniendo los
mismos triggers, no inventando un segundo resolver de aliases.

## Non-goals

- No tocar `manager-*` ni reabrir `008i`.
- No tocar `audit_*` ni reabrir `008k`.
- No cambiar `triggers`.
- No cambiar `contract_id`.
- No tocar bus, runtime o eventos.
- No introducir dependencias nuevas.
- No redisenar discovery salvo ajustes estrictamente necesarios para el rename.

## Premisas verificadas antes de Builder

- `WOT-2026-008g`, `008h`, `008i` y `008k` estan COMPLETED.
- `DEC-008G-001` serializa `008j` como el lote de expansion `bui-*` ->
  `builder-*`.
- `prompts/orchestrator_launch_builder.md` sigue siendo el prompt canonico del
  Builder y hoy referencia `skills/bui-implement-from-plan/SKILL.md` con
  `contract_id: cid-bui-implement-v1`.
- Los cuatro directorios candidatos son hoy:
  - `skills/bui-implement-from-plan/`
  - `skills/bui-run-quality-gates/`
  - `skills/bui-self-audit/`
  - `skills/bui-write-deliverable/`
- Hay consumidores vivos operativos de esos nombres en prompts, skills,
  `.claude`, catalogo, docs operativos y tests; no basta con pasar
  `--check-naming`.
- `008j` NO depende de stubs ejecutables de skill: la compatibilidad viva se
  mide sobre `triggers`, `source_prompt` y referencias operativas.
- La leccion de `008i` queda absorbida aqui: `Files Likely Touched` se declara
  a nivel fichero, no a nivel directorio, porque el `scope_gate` compara
  ficheros del diff y no hace prefix matching sobre carpetas.

## Decision Arquitectonica

Esta pasada usa migracion atomica de nombres de skill, no stubs de skill.
Motivo: igual que en `008i`, discovery no tiene hoy un mecanismo canonico y
declarativo de alias runtime para skills equivalente a `legacy_aliases:` de
prompts. Crear uno dentro de `008j` ampliaria el scope y el grafo de
compatibilidad.

Regla de compatibilidad del ticket:
- conservar triggers y semantica de dispatch;
- actualizar bindings y consumidores vivos a `builder-*`;
- tolerar restos `bui-*` solo en historia, DEC, changelog, backlog o tests de
  compatibilidad explicitamente justificados.

Si aparece un consumidor runtime real del path legacy `skills/bui-*`, eso es
`CONTRACT_GAP`, no una invitacion a improvisar un resolver paralelo.

## Files Likely Touched

### repo_motor

- `skills/bui-implement-from-plan/SKILL.md`
- `skills/bui-implement-from-plan/references/code-rules.md`
- `skills/bui-implement-from-plan/references/log-format.md`
- `skills/builder-implement-from-plan/SKILL.md`
- `skills/builder-implement-from-plan/references/code-rules.md`
- `skills/builder-implement-from-plan/references/log-format.md`
- `skills/bui-run-quality-gates/SKILL.md`
- `skills/bui-run-quality-gates/references/common-fixes.md`
- `skills/builder-run-quality-gates/SKILL.md`
- `skills/builder-run-quality-gates/references/common-fixes.md`
- `skills/bui-self-audit/SKILL.md`
- `skills/bui-self-audit/references/.gitkeep`
- `skills/builder-self-audit/SKILL.md`
- `skills/builder-self-audit/references/.gitkeep`
- `skills/bui-write-deliverable/SKILL.md`
- `skills/bui-write-deliverable/references/.gitkeep`
- `skills/builder-write-deliverable/SKILL.md`
- `skills/builder-write-deliverable/references/.gitkeep`
- `prompts/orchestrator_launch_builder.md`
- `prompts/orchestrator_pipeline.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `.claude/agents/builder.md`
- `.claude/commands/agent-build.md`
- `scripts/closeout_steps/support.py`
- `skills/project-finalize/SKILL.md`
- `skills/refactor-manager/PROMPT_TEMPLATE.md`
- `skills/repo-compare/PROMPT_TEMPLATE.md`
- `skills/deep-research/SKILL.md`
- `skills/README.md`
- `skills/validate_all.py`
- `skills/create-agent-skill/SKILL.md`
- `skills/create-agent-skill/references/frontmatter-template.md`
- `docs/registry/INDEX.md`
- `AGENTS.md`
- `llms-full.txt`
- `tests/test_discover_skills.py`
- `tests/test_check_naming.py`
- `tests/test_agent_readme_references.py`
- `tests/test_registry_catalog.py`
- `tests/test_migration_bootstrap.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
- `docs/decisions/DEC-008D-001-naming-convention.md`
- `docs/decisions/DEC-008B-002-discovery-triggers.md`
- `CHANGELOG.md`
- `backlog.md`
- `ticket_contracts.md`
- `.agent/runtime/memory/memory_rules.md`
- `.agent/runtime/memory/UPSTREAM_LEARNINGS.md`
- `bus/runtime/events`

## Forbidden Surfaces

- Tocar `manager-*`.
- Tocar `audit_*`.
- Cambiar `triggers`.
- Cambiar `contract_id`.
- Introducir aliases runtime nuevos para skills.
- Tocar bus/runtime/events manualmente.
- Tocar dependencias.

## Criterios binarios

- Existen los cuatro directorios canonicos `skills/builder-implement-from-plan/`,
  `skills/builder-run-quality-gates/`, `skills/builder-self-audit/` y
  `skills/builder-write-deliverable/`.
- `prompts/orchestrator_launch_builder.md` referencia
  `skills/builder-implement-from-plan/SKILL.md` y conserva
  `contract_id: cid-bui-implement-v1`.
- Los consumidores vivos declarados en FLT usan `builder-*` al cierre.
- `rg` de `bui-implement-from-plan|bui-run-quality-gates|bui-self-audit|bui-write-deliverable`
  sobre superficies operativas solo deja historia/DEC/changelog/backlog/tests de
  compatibilidad justificadas.
- Referencias en `.agent/runtime/memory/` se toleran como historia viva; no se
  actualizan en este ticket ni cuentan como consumidores operativos del lote.
- `python scripts/discover_skills.py --check-contract` queda verde.
- `python scripts/discover_skills.py --check-naming` queda verde.
- `python scripts/check_skill_collisions.py` queda verde.
- `python scripts/discover_skills.py --check-index` queda verde tras regenerar
  `docs/registry/INDEX.md`.
- La paridad pre/post de discovery conserva los mismos triggers funcionales; el
  diff del JSON queda limitado a rutas/nombres derivados por el rename.
- Existe una barrera que detecta referencias prose vivas a los nombres `bui-*`
  en consumidores operativos del lote.
- `AGENTS.md`, `skills/README.md` y `llms-full.txt`, si mencionan estas skills,
  quedan alineados con `builder-*`.
- `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all`
  y `validate --json --project-root <repo_destino>` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008j.md` y parar si aparece un consumidor runtime real del
path `skills/bui-*`, si preservar compatibilidad exige un alias de skill no
soportado limpiamente por discovery, o si el rename deriva a `manager-*`,
`audit_*` o a cambios de trigger/dispatch.
