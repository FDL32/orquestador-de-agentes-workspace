# Execution Log WOT-2026-002c

**Estado:** IN_PROGRESS

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
host-extends-aware (follow-up de motor). A2d cierra con alcance FASE 1 + FASE 2: 163
motor-provides retirados + 7 legacy archivados. Pendiente: verificacion (validate,
clone-demo, CI) + follow-ups de motor en backlog.
