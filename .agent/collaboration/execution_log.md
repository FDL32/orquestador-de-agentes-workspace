# execution_log.md -- WOT-2026-008h

**Estado:** READY_FOR_REVIEW

## Manager Preflight

- WOT-2026-008g cerrado canonicamente antes de abrir 008h.
- T-008H-001 materializado como contrato frozen.
- Objetivo: rename versionado de cinco prompts de orchestrator con stubs, sin tocar `orchestrator_pipeline.md` ni migrar skills `man-*`/`bui-*`.
- Riesgo clave declarado: los nombres viejos siguen siendo lexicalmente validos; la prueba de migracion debe apoyarse en consumers/stubs/source_prompt, no solo en `--check-naming`.
- Pendiente de Builder: baseline, rename, actualizacion de consumidores, gates y handoff canonico.
## Builder Fase 0 - Diagnostico + baseline (2026-06-18)

- Preflight verde: validate 0/0; STATE=008h/IN_PROGRESS; TURN=BUILDER/008h/IMPLEMENT.
- Baseline gates: --check-naming EXIT 0; --check-index EXIT 0.
- Huella real del PROMPT (rg "<nombre>.md|prompts/<nombre>", excl sandbox): 33 archivos. CLAVE: separar referencia-al-prompt de substring de funcion/variable. Ej: session_bootstrap aparece en bus/supervisor.py, builder_lifecycle.py, tests de relaunch como FUNCION/VAR del bus, NO como el prompt -> NO se tocan (non-goal: no tocar bus).
- source_prompt seam: skills/bui-implement-from-plan/SKILL.md declara source_prompt: prompts/launch_builder.md -> debe migrar a orchestrator_launch_builder.md.
- llms.txt / llms-full.txt son GENERADOS por scripts/build_llms.py (en FLT) -> se regeneran, no se editan a mano.

### Consumidores no declarados en FLT (clasificados, NO bloquean)

rg del prompt encontro referencias fuera del FLT. Clasificacion:
- COMENTARIO/DOCSTRING (prosa, no operativo): bus/memory_loader.py:181, scripts/memory_context.py:6, scripts/install_agent_system.py:63, scripts/launch_agent_terminals.ps1:1330, PROJECT.md:15, CLOSURE_MODEL.md:65-67, .agent/runtime/memory/UPSTREAM_LEARNINGS.md, CHANGELOG.md. Mencionan el nombre del prompt como texto; el STUB de compatibilidad los cubre (el archivo legacy sigue existiendo).
- LINK MARKDOWN vivo: .claude/rules/00-startup.md:5 -> prompts/session_bootstrap.md. Apunta al stub que SOBREVIVE -> no se rompe.
- Decision CEM: NO es CONTRACT_GAP. El contrato exige stub por cada nombre viejo precisamente para que estas referencias-prosa/historia/links sigan resolviendo. El FLT cubre los consumidores OPERATIVOS (source_prompt, registry, onboarding). No toco bus/scripts/PROJECT/CHANGELOG (fuera de FLT + non-goals); los stubs garantizan compat.

## Builder Fase 1 - Implementacion (2026-06-18)

- 5 renames via git mv (preserva historia): launch_builder/session_bootstrap/session_close_chat/destination_bootstrap/refactor_bootstrap -> orchestrator_*.
- 5 stubs de compat creados en rutas legacy (patron review_manager/audit_plan). orchestrator_pipeline.md NO renombrado.
- NO se necesita legacy_aliases: los 5 nombres son lexicalmente validos (launch/session/etc no son pipeline-action), --check-naming verde con o sin migracion -> prueba via stubs/source_prompt/rg.
- source_prompt en bui-implement-from-plan/SKILL.md -> orchestrator_launch_builder.md. --check-contract verde (anchor+contract_id preservados por git mv).
- Consumidores FLT actualizados (sed prompts/<legacy>.md -> prompts/orchestrator_<legacy>.md): orchestrate-pipeline, setup-agent-system+checklist, refactor-manager skills; audit_complete_motor_destination, audit_git_publication, orchestrator_pipeline prompts; README, QUICKSTART, AGENTS, CLAUDE.
- MANIFEST.distribute: 6 canonicos orchestrator + stubs legacy listados (precedente review_manager).
- scripts/build_llms.py: rutas legacy hardcodeadas (L82-88, L122) -> canonicos. llms.txt/llms-full.txt regenerados.
- INDEX regenerado (lista 5 canonicos + stubs como archivos reales).
- Refs prosa internas en los canonicos nuevos repuntadas a canonicos.

### Consumidores no declarados FLT (clasificados Fase 0, cubiertos por stub)
- rg final del prompt: bajo de 33 a 7 archivos. Los 7: INDEX/MANIFEST (stubs son archivos reales), UPSTREAM_LEARNINGS/PROJECT/CHANGELOG/CLOSURE_MODEL (historia/prosa fuera FLT), .claude/rules/00-startup.md (link al stub que sobrevive). Cero consumidor OPERATIVO legacy.

## Builder Fase 2 - Tests + Gates

- tests/test_migration_bootstrap.py: test_session_bootstrap_references_real_bootstrap_command REPUNTADO al canonico (regresion natural roja->verde: el stub ya no tiene el cuerpo operativo, el canonico si). +6 TestOrchestratorRename008h (canonicos existen, stubs sobreviven+apuntan, stub no duplica cuerpo, source_prompt canonico, compat NO via KNOWN_LEGACY_NAMES, ningun skill liga a legacy).
- Focal: pytest test_migration_bootstrap.py -q -> 28 passed; test_check_naming.py -> 17 passed.
- --check-naming/--check-contract/--check-index EXIT 0; encoding guard EXIT 0; 0 control chars en stubs heredoc (gap v1).
- ruff All checks passed; format unchanged.
- Commit productivo: 8b7b260.
- Pendiente: suite canonica level=all contra HEAD + handoff.
