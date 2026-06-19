# STRATEGY_WOT-2026-008j.md

## Enfoque

Ticket de blast radius medio-alto: renombra cuatro skills builder desde el
prefijo corto `bui-*` al canonico largo `builder-*`, preservando dispatch por
triggers y bindings prompt<->skill. El riesgo real no esta en el rename fisico,
si no en los consumidores prose/path vivos que aun apuntan al nombre legacy,
en especial `orchestrator_launch_builder`, `.claude/agents/builder.md` y las
skills que encadenan `bui-self-audit` y `bui-run-quality-gates` en el flujo.

## Fase 0 - Baseline y seams

1. Releer `DEC-008G-001` y fijar que `008j` es el lote de builder skills.
2. Capturar baseline de:
   - `python scripts/discover_skills.py --check-naming`
   - `python scripts/discover_skills.py --check-contract`
   - `python scripts/check_skill_collisions.py`
   - `python scripts/discover_skills.py --check-index`
   - `python scripts/discover_skills.py --json`
3. Inventariar referencias vivas a:
   - `bui-implement-from-plan`
   - `bui-run-quality-gates`
   - `bui-self-audit`
   - `bui-write-deliverable`
4. Confirmar seams criticos:
   - `prompts/orchestrator_launch_builder.md` -> anchor + `contract_id`
   - `prompts/orchestrator_pipeline.md` y `skills/orchestrate-pipeline/SKILL.md`
   - `.claude/agents/builder.md` y `.claude/commands/agent-build.md`
   - `skills/project-finalize/SKILL.md`
   - `docs/registry/INDEX.md`
5. Registrar en `execution_log.md` el baseline pre/post esperado y cualquier
   consumidor que parezca runtime real en vez de prose/documentacion.

## Fase 1 - Implementacion minima

1. Renombrar los cuatro directorios `bui-*` a `builder-*`.
2. Actualizar dentro de cada skill:
   - heading/body si menciona el nombre legacy;
   - referencias cruzadas entre builder skills;
   - `name:` solo donde siga acoplado semanticamente al prefijo corto.
3. Actualizar `prompts/orchestrator_launch_builder.md` para que el binding
   canonico apunte a `skills/builder-implement-from-plan/SKILL.md`,
   preservando `contract_id: cid-bui-implement-v1`.
4. Actualizar consumidores vivos declarados en FLT a `builder-*`.
5. Regenerar `docs/registry/INDEX.md` y alinear `skills/README.md`, `AGENTS.md`
   y `llms-full.txt` si reflejan los nombres canonicos.
6. No tocar `triggers`, `contract_id`, `manager-*` ni `audit_*`.

## Fase 2 - Barreras

Los tests deben cubrir al menos:
- binding `orchestrator_launch_builder.md` -> `builder-implement-from-plan`
  sin romper `--check-contract`;
- ausencia de referencias prose vivas a `bui-*` en consumidores operativos del
  lote;
- paridad funcional de triggers antes/despues del rename;
- referencias de README/registry/catalogo alineadas con los nombres canonicos.

## Riesgos a vigilar

- Descubrir demasiado tarde un consumidor runtime real del path legacy.
- Probar solo `--check-naming` y venderlo como migracion completa.
- Romper `orchestrator_launch_builder.md`/`contract_id` al cambiar el path
  canonico del Builder.
- Derivar a `manager-*`, `audit_*` o a un sistema nuevo de aliases de skill.