# plan_graph.md -- Plan WOT-2026-008

## PLAN-001 -- Inventario y contrato de migracion

- objetivo: producir el manifiesto verificable de taxonomia y compatibilidad que
  enlaza OBJ-001, OBJ-002 y OBJ-003.
- tickets: [WOT-2026-008a]
- depends_on: [WOT-2026-007d]
- superficies_archivo:
  - repo_destino/.agent/docs/taxonomy_migration_WOT-2026-008a.md
  - repo_destino/.agent/collaboration/execution_log.md
- interfaces:
  - prompts/*.md y su contrato source_prompt/Skill canonica
  - skills/*/SKILL.md, name, triggers y contract_id
  - scripts/discover_skills.py y scripts/check_skill_collisions.py (read-only)
- shared_dependencies:
  - MANIFEST.distribute y MANIFEST.workspace (read-only)
  - AGENTS.md, PROJECT.md, QUICKSTART.md, llms*.txt y tests (read-only)

## Impact Simulation

| Plan | Superficies | Shared deps | Conflicto esperado | Mitigacion | Paralelizable |
|------|-------------|-------------|--------------------|------------|---------------|
| PLAN-001 | un manifiesto nuevo en repo_destino | contratos prompt-skill y discovery del motor en lectura | inventario obsoleto si otro ticket mueve prompts/skills durante el analisis | congelar HEAD inicial y repetir inventario antes del handoff | no |

parallelism_notes: 008a debe ejecutarse en exclusiva respecto de cualquier ticket
que mueva o renombre prompts, skills, manifests o discovery.

## Forbidden Surfaces por plan

- PLAN-001: todo el repo_motor es read-only; no tocar prompts/, skills/, scripts/,
  tests/, MANIFEST.*, AGENTS.md, PROJECT.md, QUICKSTART.md ni llms*.txt.
- No tocar bus/controller/runtime del destino salvo proyecciones producidas por
  el controller.

## Merge Regression Audit

No hay merge productivo en 008a. Antes de cerrar, repetir el inventario contra el
mismo HEAD o registrar el nuevo HEAD y reconciliar cualquier drift. Los tickets
posteriores deben ejecutar discovery, collision check, contract check y suite
completa sobre la union de cambios.