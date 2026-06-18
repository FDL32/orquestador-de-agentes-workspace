# execution_log.md -- WOT-2026-008h

**Estado:** COMPLETED

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

## Builder - Manager CHANGES resueltos (2026-06-18)

Manager veredicto CHANGES: 1 consumidor vivo legacy (ALTO) + falta test de prose viva (MEDIO). Ambos corregidos.

### ALTO - refs bare legacy supervivientes
- Causa raiz: el sed de migracion capturo solo "prompts/<legacy>.md". orchestrator_pipeline.md:1082 ("BUILDER implementa con launch_builder.md") era ref BARE (sin prompts/) -> escapo. Mi claim "7 restantes legitimos" fue impreciso: mi grep de verificacion tambien exigia prompts/.
- Barrido completo de refs bare: encontradas 4 vivas (orchestrator_pipeline:1082, orchestrator_session_bootstrap:138, orchestrator_destination_bootstrap:100, orchestrator_refactor_bootstrap:3). Todas repuntadas a orchestrator_*. llms regenerado.
- Verificacion final: grep bare+qualified legacy en consumidores vivos = 0 (solo quedan stubs con su cabecera, DEC historicos, comentarios fuera FLT).

### MEDIO - test de regresion de prose viva
- Anadido test_no_live_prose_reference_to_legacy_names: escanea consumidores OPERATIVOS vivos (canonicos + audit prompts + README/QUICKSTART/AGENTS/CLAUDE + skills) por refs legacy bare o con prompts/, saltando cabeceras de stub "# Legacy alias:" y docs historicos.
- BARRERA VERIFICADA: reintroduje L1082 legacy -> test FALLA (caza el bug exacto del Manager); restaurado -> PASA. No es falso verde.

### Gates post-fix
- Focal: pytest test_migration_bootstrap.py test_check_naming.py -q -> 46 passed.
- --check-naming/--check-contract/--check-index EXIT 0; ruff All checks passed; encoding EXIT 0.
- Commit productivo: e5975eb.
- Pendiente: suite canonica level=all contra HEAD + re-handoff.

### Cierre de evidencia - suite cerrada limpia (re-run)

- La corrida previa dejo last-run.json en status=started/exit=None (interrumpida). Relanzada limpia.
- run_pytest_safe --level all sobre e5975eb: 3006 passed, 20 skipped, 0 failed (377.85s).
- last-run.json CERRADO: status=finished, exit_code=0, tested_commit_sha=e5975eb == HEAD.
- validate --json repo_destino: 0 errors / 0 warnings. STATE=008h/READY_FOR_REVIEW. Motor limpio.


Manager approved canonical closeout for WOT-2026-008h