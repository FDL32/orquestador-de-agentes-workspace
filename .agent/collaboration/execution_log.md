# Execution Log WOT-2026-002c

**Estado:** COMPLETED

## Metadata

- **ID:** WOT-2026-002c
- **deliverable_type:** code
- **delivery_authority:** repo_destino
- **Alias historico:** WOT-AUDIT-A2d
- **Rol activo:** BUILDER
- **Accion:** EXECUTE

## Resumen

- Pipeline. Manager redacto `work_plan.md`, `PLAN_WOT-2026-002c.md` y
  `AUDIT_WOT-2026-002c.md` para WOT-2026-002c (A2d).
- ID canonico por regla 0.d: sigue a WOT-2026-002b (cerrado: 48754f8 + a9e5f38).
  `WOT-AUDIT-A2d` queda como alias historico. 002d absorbed (premisa obsoleta).
- Objetivo: retirar las copias motor-provides (~163 git rm), archivar el set muerto a
  `_legacy/` (7), retirar los 3 installer-managed con re-sync. Por buckets, commits
  separados, reversible via git. Barreras 002a (pytest/tests) y 002b (installer-managed)
  incorporadas.
- Decisiones del usuario: ejecutar A2d ahora (staged + barreras); retirar tests/ +
  follow-up de motor para el gates-dispatch sin tests locales.
- code + delivery_authority=repo_destino: M3 en el destino. Doble review adversarial (sec.6).

## FASE 0 - Reconciliacion (read-only) [COMPLETADA]

**Baseline pre-retirada (git ls-files --cached):**
- Total tracked: 335
- agent_system/: 113
- skills/: 41
- scripts/ motor-provides (7): run_pytest_safe, discover_skills, upgrade_agent_system, detect_agent_system_version, test_refactoring_impact, test_refactor_kit_portable, test_refactor_kit_performance
- tests/test_event_bus_hygiene.py: 1
- .agent/README.md: 1
- Bucket 2 legacy cluster (7): artifact_graph, audit_codebase, rollback_agent_system, state_drift, test_refactor_manager_skill, test_ticket_007_context_recovery, .goosehints
- Bucket 3 installer-managed (3): pre_compact_hook.py, onboarding.md, glossary.md

**Invocadores vivos por pieza:**

### run_pytest_safe.py
- Referencias encontradas en: skills/ (motor-provides, se elimina), AGENTS.md y CHANGELOG.md (docs), .agent/collaboration/ (plan/log docs), .agent/docs/ (analisis docs), scripts/detect_agent_system_version.py (motor-provides, se elimina), scripts/test_refactoring_impact.py (motor-provides, se elimina), .claude/rules/ (documentacion, no ejecutable), .claude/settings.local.json (gitignored/personal, excluido)
- CI .github/workflows/quality-gates.yml: redeseniado (WOT-AUDIT-CI) - NO referencia run_pytest_safe. Confirmado: el workflow usa _motor agent_controller --validate solamente.
- **Invocadores vivos trackeados fuera de zonas excluidas: 0. CLEAR.**

### discover_skills.py
- Referencias en: _legacy/ (gitignored/gittracked - se archivara en FASE 1), skills/ (motor-provides), CHANGELOG.md (doc), .agent/collaboration/ (docs), CI workflow (redeseniado, NO llama discover_skills localmente)
- .claude/rules/03-skills-discovery.md: documentacion (no ejecutable)
- **Invocadores vivos trackeados fuera de zonas excluidas: 0. CLEAR.**

### upgrade_agent_system.py, detect_agent_system_version.py
- Referencias en: work_plan docs, triage, CHANGELOG (historico), .claude/rules/ (doc)
- scripts/upgrade_agent_system.py se refiere a si mismo (siendo eliminado)
- **Invocadores vivos trackeados: 0. CLEAR.**

### test_refactoring_impact.py, test_refactor_kit_portable.py, test_refactor_kit_performance.py
- Referencias solo en: work_plan docs, triage, CHANGELOG (historico), .agent/docs/ (analisis)
- .claude/settings.local.json (gitignored/personal): test_refactor_kit_performance.py listado pero excluido
- **Invocadores vivos trackeados: 0. CLEAR.**

### test_event_bus_hygiene.py
- Solo en work_plan y triage_manifest (docs)
- **Invocadores vivos trackeados: 0. CLEAR.**

### .agent/README.md
- `diff .agent/README.md <motor>/.agent/README.md` -> DIFIEREN (titulo diferente, contenido customizado para destino, rutas absolutas del destino, texto de higiene personalizado)
- **STOP#3 ACTIVADO: .agent/README.md CUSTOMIZADO vs motor. NO se retira. KEEP.**

### Skills paridad
- Destino tiene 16 skill dirs/archivos bajo skills/ (15 dirs + validate_all.py + README.md + _shared)
- Todos existen en el motor: `git ls-files skills/ | cut -d'/' -f1-2 | sort -u` del destino vs motor -> 0 diferencias
- **Paridad OK. No STOP#2.**

### pre_compact_hook wiring
- Destino .claude/settings.json: solo tiene PreToolUse (guard_paths). NO tiene PreCompact hook.
- El pre_compact_hook.py del destino NO esta actualmente cableado en PreCompact del destino.
- Motor .claude/settings.json: tiene PreCompact con candidatos [root/orquestador_de_agentes/.agent/hooks/pre_compact_hook.py, root/.agent/hooks/pre_compact_hook.py, root/agent_system/.agent/hooks/pre_compact_hook.py]
- Accion FASE 3: agregar PreCompact hook al destino .claude/settings.json apuntando a candidato del motor; luego git rm .agent/hooks/pre_compact_hook.py.
- **Wiring resuelto antes de rm: safe to proceed.**

**Snapshot del motor:** orchestrator_pipeline/session_close/motor_before_WOT-2026-002c.json (existia pre-FASE 0).

**FASE 0 resultado: CLEAR para Fases 1, 2, 3. STOP#3 activo: .agent/README.md permanece.**

---

## FASE 1 - archive-legacy [HECHA: commit 1a2d700]

Bucket 2 (7 archivos): artifact_graph, audit_codebase, rollback_agent_system, state_drift, test_refactor_manager_skill -> _legacy/scripts/; test_ticket_007_context_recovery -> _legacy/tests/; .goosehints -> _legacy/. git mv reversible.

## FASE 2 - motor-provides [HECHA: commit bf451f2]

`git rm -r agent_system/` (113) + `git rm -r skills/` (41, paridad OK) + 7 scripts
motor-provides + `tests/test_event_bus_hygiene.py`. `.agent/README.md` NO retirado
(STOP#3: customizado). 163 retirados. Reversible via historial; el motor tiene las copias.

## FASE 3 - installer-managed [DIFERIDA - incidente install --sync]

**Incidente:** la accion prevista (git rm de los 3 installer-managed + `install --sync`
para re-provisionar onboarding/glossary) fallo: `install_agent_system.py --sync`
**re-vendoriza el bundle COMPLETO** en el destino (re-creo `agent_system/` con caches
.ruff_cache/.pytest_cache/__pycache__ + runtime) y borro en el working tree
deliverables destino-keep (`resource_precedence.md`, `triage_manifest.md`,
`orphans_decision_WOT-2026-002b.md`). install --sync es la herramienta EQUIVOCADA para
host-extends: su contrato es provisionar el bundle, no retirarlo.

**Alerta de seguridad (FALSO POSITIVO de atribucion):** el detector marco que el
subagente "anadio" a `.claude/settings.json` reglas wildcard de Bash (`python3:*`,
`for f:*`) y un dominio WebFetch `paperclip.ing`. Verificado por git: ese contenido
**ya estaba en el commit inicial `468844d`** (pre-existente en el repo destino, no
introducido por esta sesion; `git diff HEAD .claude/settings.json` = vacio). Es config
pre-existente del destino para revision del humano, no daño de esta sesion.

**Recuperacion (sin tocar 1a2d700/bf451f2):** `git restore` de los deliverables
destino-keep borrados, de los 3 installer-managed (undo del git rm de FASE 3), y de las
modificaciones de install --sync (version_manifest, memory_rules, STATE/TURN). `rm -rf`
del `agent_system/` untracked (solo caches + runtime de install --sync, no el bundle).
Estado recuperado = post-FASE-2 limpio. Los 3 installer-managed permanecen como
destino-keep.

**Decision:** FASE 3 DIFERIDA. Los 3 installer-managed se conservan hasta un install
host-extends-aware (follow-up de motor). A2d cierra con alcance FASE 1 + FASE 2: 162
motor-provides retirados + 7 legacy archivados. Pendiente: verificacion (validate,
clone-demo, CI) + follow-ups de motor en backlog.

## Manager review (doble pasada, §6) - 2026-06-14

- **Rev1 (verificacion):** FASE 2 (bf451f2) retiro SOLO motor-provides (162; git
  diff-filter=D sin rutas fuera de los buckets); `.agent/README.md` conservado (STOP#3);
  destino-keep intacto (collaboration 105/runtime 8/config 3/.claude 11); validate 0/0;
  motor pristine (687d5b9); CI sin refs a copias retiradas.
- **Rev2 (adversarial):** clone-demo -> el destino SIN agent_system/skills opera via
  motor (discover_skills exit 0, validate clone 0 errors) = host-extends real; FASE 0
  confirmo 0 invocadores vivos; el incidente install --sync se recupero sin tocar los
  commits legitimos; la alerta de seguridad es falso positivo (settings.json
  pre-existente en 468844d). No se pudo refutar el cierre parcial.
- **Decision:** APROBADO_PARCIAL. Artifact: .agent/runtime/reviews/decision_WOT-2026-002c.json
- **Follow-ups (motor):** MOTOR-FU-001 (install host-extends-aware -> desbloquea FASE 3),
  MOTOR-FU-002 (gates-dispatch sin tests locales).

## Gate final

A2d parcial: FASE 1 (1a2d700, 7 legacy a _legacy/) + FASE 2 (bf451f2, 162 motor-provides
git rm). Recovery 791787b (incidente install --sync). Clone-demo verde (destino opera
via motor sin las copias). validate destino 0/0, motor pristine 687d5b9, CI sin refs,
destino-keep intacto, 0 flujo vivo roto. FASE 3 diferida a MOTOR-FU-001. ruff/pytest-safe
N/A (retirada via git rm/mv; tests/ motor-provides retirado). All checks passed for
WOT-2026-002c (alcance FASE 1+2).


Scope override: Retirada masiva A2d: 162 motor-provides (agent_system/skills/7-scripts/test_event_bus_hygiene) + 7 legacy a _legacy/, segun triage_manifest + orphans_decision_WOT-2026-002b. FLT declara las superficies como directorios; el scope gate enumera archivos individuales (esperado en ticket de retirada). FASE 0 confirmo 0 invocadores vivos; destino-keep intacto; clone-demo verde.. Affected files: .agent/collaboration/AUDIT_WOT-2026-002c.md, .agent/collaboration/PLAN_WOT-2026-002c.md, .agent/collaboration/STATE.md, .agent/collaboration/backlog.md, .agent/collaboration/work_plan.md, .goosehints, _legacy/.goosehints, _legacy/scripts/artifact_graph.py, _legacy/scripts/audit_codebase.py, _legacy/scripts/rollback_agent_system.py, _legacy/scripts/state_drift.py, _legacy/scripts/test_refactor_manager_skill.py, _legacy/tests/test_ticket_007_context_recovery.py, agent_system/.agent/README.md, agent_system/.agent/agent_controller.py, agent_system/.agent/collaboration/STATE.md, agent_system/.agent/collaboration/TURN.md, agent_system/.agent/collaboration/execution_log.md, agent_system/.agent/completion_checker.py, agent_system/.agent/hooks/guard_paths.py, agent_system/.agent/known_models.json, agent_system/.agent/session_tracker.py, agent_system/.agent_allowlist.json, agent_system/.agent_common_rules.md, agent_system/.agent_denylist.json, agent_system/.builder_rules, agent_system/.claude/README.md, agent_system/.clawrules, agent_system/.gitignore, agent_system/.goosehints, agent_system/.manager_rules, agent_system/.ruff.toml, agent_system/AGENT_SECURITY.md, agent_system/EMPEZAR-AQUI.md, agent_system/README.md, agent_system/UPGRADE_GUIDE.md, agent_system/__init__.py, agent_system/docs/00-INDICE.md, agent_system/docs/01-INSTALACION.md, agent_system/docs/02-GUIA-COMPLETA.md, agent_system/docs/03-SEGURIDAD.md, agent_system/docs/04-FAQ.md, agent_system/docs/MANIFEST_SPEC.md, agent_system/docs/reference/UPGRADE_GUIDE.md, agent_system/docs/reference/agent.md, agent_system/docs/reference/agent_seguridad.md, agent_system/docs/reference/anti-patterns.md, agent_system/docs/reference/closure-best-practices.md, agent_system/docs/reference/project-template.md, agent_system/pytest.ini, agent_system/refactor_kit/README.md, agent_system/refactor_kit/__init__.py, agent_system/refactor_kit/install_refactor_kit.py, agent_system/refactor_kit/prompt_templates/01_analysis.md, agent_system/refactor_kit/prompt_templates/02_plan.md, agent_system/refactor_kit/prompt_templates/03_refactor.md, agent_system/refactor_kit/prompt_templates/04_validation.md, agent_system/refactor_kit/prompt_templates/05_iteration.md, agent_system/refactor_kit/refactor_manager.py, agent_system/scripts/clean_for_deployment.ps1, agent_system/scripts/detect_agent_system_version.py, agent_system/scripts/discover_skills.py, agent_system/scripts/install_agent_system.py, agent_system/scripts/manifest_validator.py, agent_system/scripts/orquestador.py, agent_system/scripts/project_paths.py, agent_system/scripts/rollback_agent_system.py, agent_system/scripts/run_pytest_safe.py, agent_system/scripts/scaffold_tests.py, agent_system/scripts/test_refactor_kit_portable.py, agent_system/scripts/upgrade_agent_system.py, agent_system/skills/README.md, agent_system/skills/bui-implement-from-plan/SKILL.md, agent_system/skills/bui-implement-from-plan/references/code-rules.md, agent_system/skills/bui-implement-from-plan/references/log-format.md, agent_system/skills/bui-run-quality-gates/SKILL.md, agent_system/skills/bui-run-quality-gates/references/common-fixes.md, agent_system/skills/bui-self-audit/SKILL.md, agent_system/skills/bui-self-audit/references/.gitkeep, agent_system/skills/create-agent-skill/SKILL.md, agent_system/skills/create-agent-skill/references/frontmatter-template.md, agent_system/skills/create-agent-skill/references/skill-anatomy.md, agent_system/skills/graphify/SKILL.md, agent_system/skills/man-create-work-plan/SKILL.md, agent_system/skills/man-create-work-plan/references/plan-template.md, agent_system/skills/man-create-work-plan/references/risk-guide.md, agent_system/skills/man-resolve-escalation/SKILL.md, agent_system/skills/man-resolve-escalation/references/escalation-levels.md, agent_system/skills/man-review-implementation/SKILL.md, agent_system/skills/man-review-implementation/references/review-checklist.md, agent_system/skills/man-review-implementation/references/verdict-format.md, agent_system/skills/project-finalize/SKILL.md, agent_system/skills/project-finalize/references/closeout-checklist.md, agent_system/skills/project-finalize/references/closeout-modes.md, agent_system/skills/project-finalize/references/closeout-plan-template.md, agent_system/skills/scaffold-python-project/SKILL.md, agent_system/skills/scaffold-python-project/references/gitignore-template.md, agent_system/skills/scaffold-python-project/references/pyproject-template.md, agent_system/skills/secure-existing-project/SKILL.md, agent_system/skills/secure-existing-project/references/cascade-config-pattern.md, agent_system/skills/secure-existing-project/references/security-checklist.md, agent_system/skills/setup-agent-system/SKILL.md, agent_system/skills/setup-agent-system/references/quickstart-checklist.md, agent_system/skills/validate_all.py, agent_system/skills/version-changelog/SKILL.md, agent_system/skills/version-changelog/references/changelog-template.md, agent_system/skills/version-changelog/references/semver-decision-guide.md, agent_system/templates/repo_root/.gitignore.template, agent_system/templates/repo_root/AGENT_SECURITY.md.template, agent_system/templates/repo_root/CHANGELOG.md.template, agent_system/templates/repo_root/CLAUDE.md.template, agent_system/templates/repo_root/PROJECT.md.template, agent_system/templates/repo_root/README.md.template, agent_system/templates/repo_root/pytest.ini.template, agent_system/templates/repo_root/scripts/run_pytest_safe.py.template, agent_system/templates/repo_root/tests/ARCHITECTURE.md.template, agent_system/templates/repo_root/tests/README.md.template, agent_system/templates/repo_root/tests/__init__.py.template, agent_system/templates/repo_root/tests/_temp_runtime.py.template, agent_system/templates/repo_root/tests/conftest.py.template, agent_system/templates/repo_root/tests/unit/__init__.py.template, agent_system/templates/repo_root/tests/unit/test_ejemplo.py.template, agent_system/templates/repo_root/tests/unit/test_windows_safe_temp_runtime.py.template, agent_system/tests/test_guard_paths.py, agent_system/tests/test_hooks.py, agent_system/tests/test_semantic_logger.py, scripts/artifact_graph.py, scripts/audit_codebase.py, scripts/detect_agent_system_version.py, scripts/discover_skills.py, scripts/rollback_agent_system.py, scripts/run_pytest_safe.py, scripts/state_drift.py, scripts/test_refactor_kit_performance.py, scripts/test_refactor_kit_portable.py, scripts/test_refactor_manager_skill.py, scripts/test_refactoring_impact.py, scripts/upgrade_agent_system.py, skills/README.md, skills/_shared/SKILL.md, skills/_shared/references/README.md, skills/bui-implement-from-plan/SKILL.md, skills/bui-implement-from-plan/references/code-rules.md, skills/bui-implement-from-plan/references/log-format.md, skills/bui-run-quality-gates/SKILL.md, skills/bui-run-quality-gates/references/common-fixes.md, skills/bui-self-audit/SKILL.md, skills/bui-self-audit/references/.gitkeep, skills/create-agent-skill/SKILL.md, skills/create-agent-skill/references/frontmatter-template.md, skills/create-agent-skill/references/skill-anatomy.md, skills/graphify/SKILL.md, skills/man-create-work-plan/SKILL.md, skills/man-create-work-plan/references/plan-template.md, skills/man-create-work-plan/references/risk-guide.md, skills/man-resolve-escalation/SKILL.md, skills/man-resolve-escalation/references/escalation-levels.md, skills/man-review-implementation/SKILL.md, skills/man-review-implementation/references/review-checklist.md, skills/man-review-implementation/references/verdict-format.md, skills/project-finalize/SKILL.md, skills/project-finalize/references/closeout-checklist.md, skills/project-finalize/references/closeout-modes.md, skills/project-finalize/references/closeout-plan-template.md, skills/refactor-manager/SKILL.md, skills/refactor-manager/goose-skill.json, skills/refactor-manager/references/README.md, skills/scaffold-python-project/SKILL.md, skills/scaffold-python-project/references/gitignore-template.md, skills/scaffold-python-project/references/pyproject-template.md, skills/secure-existing-project/SKILL.md, skills/secure-existing-project/references/cascade-config-pattern.md, skills/secure-existing-project/references/security-checklist.md, skills/setup-agent-system/SKILL.md, skills/setup-agent-system/references/quickstart-checklist.md, skills/validate_all.py, skills/version-changelog/SKILL.md, skills/version-changelog/references/changelog-template.md, skills/version-changelog/references/semver-decision-guide.md, tests/test_event_bus_hygiene.py, tests/test_ticket_007_context_recovery.py

Manager approved canonical closeout for WOT-2026-002c