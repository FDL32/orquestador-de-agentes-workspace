# work_plan.md -- WOT-2026-008h

## Metadata

- **ID:** WOT-2026-008h
- **Contract ID:** T-008H-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Ejecutar el rename versionado de cinco prompts del orchestrator a nombres `orchestrator_*`, manteniendo compatibilidad con stubs y actualizando consumidores vivos. Cumplimiento medible: existen los cinco prompts canonicos nuevos, los cinco nombres viejos sobreviven como stubs, `source_prompt` y referencias vivas apuntan al canonico, y `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.

## Non-goals

- No renombrar `prompts/orchestrator_pipeline.md`.
- No migrar skills `man-*` o `bui-*`.
- No tocar bus, runtime o eventos.
- No cambiar dependencias ni politicas del launcher.

## Premisas verificadas antes de Builder

- WOT-2026-008g esta COMPLETED y `DEC-008G-001` es la autoridad.
- `orchestrator_pipeline.md` ya es canonico y no entra en el rename.
- `launch_builder.md` sigue siendo exception lexical; por tanto la migracion no se puede probar solo con `--check-naming`.
- `skills/bui-implement-from-plan/SKILL.md` usa `source_prompt: prompts/launch_builder.md` y debe actualizarse.

## Decision Arquitectonica

El ticket replica el patron versionado de 008e: cada nombre canonico nuevo nace como archivo fuente y el nombre viejo sobrevive como stub de compatibilidad. La prueba de migracion se apoya en consumidores vivos, `source_prompt`, registry y stubs presentes; no se acepta como evidencia unica que `--check-naming` siga verde.

## Files Likely Touched

### repo_motor

- `prompts/launch_builder.md`
- `prompts/orchestrator_launch_builder.md`
- `prompts/session_bootstrap.md`
- `prompts/orchestrator_session_bootstrap.md`
- `prompts/session_close_chat.md`
- `prompts/orchestrator_session_close_chat.md`
- `prompts/destination_bootstrap.md`
- `prompts/orchestrator_destination_bootstrap.md`
- `prompts/refactor_bootstrap.md`
- `prompts/orchestrator_refactor_bootstrap.md`
- `prompts/orchestrator_pipeline.md`
- `prompts/audit_complete_motor_destination.md`
- `prompts/audit_git_publication.md`
- `skills/bui-implement-from-plan/SKILL.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `skills/setup-agent-system/SKILL.md`
- `skills/setup-agent-system/references/quickstart-checklist.md`
- `skills/refactor-manager/SKILL.md`
- `scripts/build_llms.py`
- `MANIFEST.distribute`
- `docs/registry/INDEX.md`
- `README.md`
- `QUICKSTART.md`
- `AGENTS.md`
- `CLAUDE.md`
- `llms.txt`
- `llms-full.txt`
- `tests/test_migration_bootstrap.py`
- `tests/test_check_naming.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
- `scripts/discover_skills.py`
- `CHANGELOG.md`
- `bus/runtime/events`

## Forbidden Surfaces

- Renombrar `prompts/orchestrator_pipeline.md`.
- Tocar `man-*`/`bui-*`.
- Tocar bus/runtime/events manualmente.
- Tocar dependencias.
- Editar frontmatter fuera de `source_prompt` cuando aplique.

## Criterios binarios

- Existen los cinco prompts canonicos nuevos `orchestrator_*`.
- Los cinco nombres viejos quedan como stubs de compatibilidad.
- `source_prompt` del Builder apunta al nuevo canonico.
- Los consumidores vivos declarados en FLT usan el nombre canonico nuevo o documentan explicitamente el stub.
- `orchestrator_pipeline.md` sigue sin rename y con referencias actualizadas.
- `MANIFEST.distribute`, `INDEX.md`, `README.md`, `QUICKSTART.md`, `AGENTS.md`, `CLAUDE.md`, `llms.txt` y `llms-full.txt` quedan alineados donde aplique.
- La prueba de migracion no descansa solo en `--check-naming`; tambien se verifica con `rg`, stubs presentes y `source_prompt` actualizado.
- `discover_skills.py --check-naming`, `--check-index`, encoding guard, tests focales, `run_pytest_safe --level all` y `validate --json` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008h.md` y parar si algun prompt viejo no puede mantenerse como stub, si aparece un consumidor vivo no declarado de alto riesgo, si el rename exige tocar runtime/bus o si la compatibilidad requiere un cambio de gate no previsto.