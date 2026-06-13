# Orphans Decision Document - WOT-2026-002b

## Metadata

- **Ticket:** WOT-2026-002b (alias: WOT-AUDIT-ORPHANS)
- **Date:** 2026-06-13
- **Author:** Builder (Claude Code, claude-sonnet-4-6)
- **Reference:** `.agent/docs/triage_manifest.md` (bucket `huerfano-needs-decision`, frozen 2026-06-13)
- **Deliverable type:** analysis
- **NOTE:** This document ONLY decides. It does NOT move, delete, or rename any file.
  Execution (git mv / removal) is A2d / WOT-2026-002c.

---

## Summary of Evidence Method

For each orphan:
1. `git -C <destino> grep -n <basename>` (live invocations in destino)
2. `git -C <motor> grep -n <basename>` (functional equivalent or absence in motor)
3. Read the file to assess domain and functionality.
4. Apply the frozen rubric: system tooling -> motor; operational state / integration /
   host config / domain -> destino; dead (no live call + superseded or deprecated) ->
   archive-legacy.

---

## Decision Table

| # | Orphan | Invocation in destino (key hits) | Equivalent/hit in motor | Domain | Decision | Barrier for A2d? |
|---|--------|----------------------------------|------------------------|--------|----------|-----------------|
| 1 | `scripts/artifact_graph.py` | `scripts/audit_codebase.py:81` (ruff focus list only, not imported or called by any live entrypoint) | No equivalent (`git -C motor grep artifact_graph`: no hits) | System tooling - DAG utility; no live caller outside defunct cluster | archive-legacy | NO |
| 2 | `scripts/audit_codebase.py` | `CHANGELOG.md:202,228,253,256` (historical); no CI, skill, or hook invokes it today; backlog.md:255 notes the code-audit skill is inejecutable (calls non-existent motor copy) | No equivalent in motor (`git -C motor grep audit_codebase`: no hits) | System tooling - codebase audit orchestrator; dead cluster head | archive-legacy | NO |
| 3 | `scripts/rollback_agent_system.py` | `scripts/upgrade_agent_system.py:123,269` (string in recovery messages only, not a Python import or subprocess call); `agent_system/UPGRADE_GUIDE.md:169,176,193,198,203` (doc references) | Motor has `scripts/rollback.py` (canonical equivalent); motor CHANGELOG:816 explicitly: "Exact duplicate of canonical scripts/rollback.py" | System tooling - rollback is motor-level; motor's `scripts/rollback.py` is the canonical version | archive-legacy | NO |
| 4 | `scripts/state_drift.py` | `scripts/audit_codebase.py:18-21,54,80` (imported by dead cluster head only; no live external caller); `git -C destino grep state_drift` = only docs and the dead cluster | Motor `tests/test_launcher_state_from_bus.py:305` (unrelated test variable name); no functional motor copy of the script itself. Role superseded by `agent_controller --validate` (confirmed in triage_manifest) | System tooling - drift detection; role fully covered by `agent_controller --validate` since the system migrated from `.session/` to `.agent/collaboration/` canonical paths (state_drift.py still reads `.session/` which no longer exists) | archive-legacy | NO |
| 5 | `scripts/test_refactor_manager_skill.py` | `CHANGELOG.md:693` (historical gate evidence only); no CI, hook, or runner invokes it today; `git -C destino grep test_refactor_manager_skill` = only docs | No equivalent in motor (`git -C motor grep test_refactor_manager_skill`: no hits) | System tooling - integration smoke-test for refactor-manager skill; one-shot historical test, no live runner | archive-legacy | NO |
| 6 | `tests/test_ticket_007_context_recovery.py` | `git -C destino grep test_ticket_007`: only doc/backlog references (no pytest runner, no CI step invokes it). BUT: imports `hooks.pre_compact_hook` which IS live (see #7); test validates real functions in that live hook | No equivalent in motor (`git -C motor grep test_ticket_007`: no hits; motor has its own `tests/unit/test_pre_compact_hook.py`) | Analysis: the TEST is for the destino's TICKET-007 feature which is the live pre_compact_hook. The test exercises real functions (extract_work_plan_keywords, rank_observations, format_memory_section, _build_state_content). However the test lives in `tests/` not `tests/unit/` and is not collected by any live runner today. Decision: archive-legacy (the motor now has full test coverage for this hook in `tests/unit/test_pre_compact_hook.py`; the destino test is superseded) | archive-legacy | NO (but note: if `tests/` ever added to pytest scope, these tests would pass against the live hook) |
| 7 | `.agent/hooks/pre_compact_hook.py` | `tests/test_ticket_007_context_recovery.py:13` (imports it; test is orphan too). `agent_system/scripts/install_agent_system.py:266` (registers it in PreCompact hook wiring). `agent_system/scripts/clean_for_deployment.ps1:224` (references it). The motor's `.claude/settings.json:31` wires PreCompact to `.agent/hooks/pre_compact_hook.py` as candidate path. | Motor has `.agent/hooks/pre_compact_hook.py` (350 lines; v2 with `bus.memory_loader` integration). The destino copy is the OLD TICKET-007 version (357 lines; no memory_loader). Functionally DIVERGED: motor version is newer and the motor's `tests/unit/test_pre_compact_hook.py` covers it. | System framework - pre-compact hook is generic framework tooling, not destino-domain. The motor already owns the canonical version. The destino copy is a stale diverged copy of the motor original. | archive-legacy | YES - must be reconciled: A2d must verify the motor version is wired correctly before removing the destino copy, because the PreCompact wiring in `.claude/settings.json` (motor) resolves `root/.agent/hooks/pre_compact_hook.py` as a candidate. A2d must confirm the motor hook resolves when operating on the destino. |
| 8 | `.agent/microagents/onboarding.md` | `git -C destino grep onboarding`: `.agent/microagents/onboarding.md` is referenced by `.agent/glossary.md:11,27` as a doc pointer. No code loads or imports it programmatically. | Motor has `agent_system/templates/microagents/onboarding.md` (identical content confirmed by read comparison). Motor's `scripts/install_agent_system.py:908-919` copies it to destino during install/sync. | System framework - this is an installer-managed template copy, not a host override. Content is identical to motor template. | archive-legacy | YES - A2d must remove it ONLY after confirming the motor installer can re-provision it on next sync. Removing without re-sync creates a gap. |
| 9 | `.agent/glossary.md` | `git -C destino grep glossary`: `.agent/microagents/onboarding.md:11,27` references it (doc-to-doc pointer only; no code import). | Motor has `agent_system/templates/glossary.md` (identical content confirmed by read comparison). Motor's `scripts/install_agent_system.py:910-919` provisions it; `INSTALLER_MANAGED_PATHS:52` explicitly marks it as installer-managed. | System framework - installer-managed template copy. Content is identical to motor template. | archive-legacy | YES - same as #8: A2d must remove ONLY after confirming motor installer re-provisions on next sync. |
| 10 | `.goosehints` | `git -C destino grep goosehints`: `scripts/upgrade_agent_system.py:39` (cleanup list), `.claude/rules/02-multi-agent-system.md:19` (deprecated note), `CHANGELOG.md:702` (historical). Deprecated consumer (Goose/Claw) not active. | Motor has `.goosehints` with deprecation header `[DEPRECATED - WT-2026-254a]`; motor's `scripts/upgrade_agent_system.py:50` lists it for cleanup. Both repos' `AGENTS.md` and `.claude/rules/` mark Goose/Claw as deprecated. | Deprecated integration artifact - Goose deprecated per WT-2026-254a; no live consumer. | archive-legacy | NO |

---

## Decisions: archive-legacy Evidence Summary

### #1 artifact_graph.py
- Dead: only caller is `scripts/audit_codebase.py:81` (ruff focus list in a dead cluster head, not a live import or subprocess call).
- No motor equivalent.
- No live entrypoint outside the dead cluster.

### #2 audit_codebase.py
- Dead: CHANGELOG references are historical; no CI/skill/hook invokes it today.
- backlog.md:255 confirms the code-audit skill is inejecutable (references a motor-side copy that does not exist).
- No motor equivalent; it was a standalone audit orchestrator for an older workflow.

### #3 rollback_agent_system.py
- Motor CHANGELOG:816 explicitly: "Exact duplicate of canonical scripts/rollback.py".
- Motor canonical equivalent confirmed: `scripts/rollback.py` (functional parity; motor version is canonical).
- The destino `scripts/upgrade_agent_system.py:123,269` only embeds the old script name as a string in recovery message templates, not as a live Python call.

### #4 state_drift.py
- Only caller is `scripts/audit_codebase.py` (dead cluster).
- The script reads `.session/work_plan.md` which no longer exists (canonical path is `.agent/collaboration/work_plan.md`); the script's check would silently return `True` (no-op) on the current repo layout.
- Role is fully covered by `agent_controller --validate` (triage_manifest, confirmed: motor `agent_controller.py` validates state drift against `.agent/collaboration/`).

### #5 test_refactor_manager_skill.py
- One-shot integration test from a historical ticket gate (CHANGELOG:693).
- No live runner, no CI step, no conftest picks it up.
- No motor equivalent (motor has its own skill tests under `tests/`).

### #6 test_ticket_007_context_recovery.py
- Not collected by any live pytest runner; no CI step references it.
- The functions it tests ARE live (in `.agent/hooks/pre_compact_hook.py`), but the motor now owns canonical test coverage (`tests/unit/test_pre_compact_hook.py`).
- Tests would still pass if collected, but they are superseded by motor tests.

### #7 .agent/hooks/pre_compact_hook.py (stale-diverged motor copy)
- Motor has its own canonical `.agent/hooks/pre_compact_hook.py` (v2, 350 lines, integrates `bus.memory_loader`).
- Destino copy is TICKET-007 version (357 lines, no memory_loader, older architecture).
- The destino copy is a stale-diverged copy of what was originally motor framework code.

### #8 .agent/microagents/onboarding.md
- Confirmed installer-managed: motor `scripts/install_agent_system.py:52` lists `glossary.md` and `microagents` in `INSTALLER_MANAGED_PATHS`.
- Content identical to `agent_system/templates/microagents/onboarding.md`.

### #9 .agent/glossary.md
- Confirmed installer-managed: motor `INSTALLER_MANAGED_PATHS:52` explicitly includes `glossary.md`.
- Content identical to `agent_system/templates/glossary.md`.
- Motor `tests/unit/test_install_agent_system.py:391-438` validates installer management of glossary.

### #10 .goosehints
- Deprecated per WT-2026-254a (cited in `.claude/rules/02-multi-agent-system.md:14`, `AGENTS.md:7`, motor `.goosehints:1`).
- No live consumer (Goose/Claw are deprecated).
- Motor also has this file marked deprecated; motor `scripts/upgrade_agent_system.py:50` lists it for cleanup.

---

## Barriers for A2d (WOT-2026-002c)

These orphans are classified `archive-legacy` but require reconciliation steps BEFORE
or DURING A2d to avoid breaking live wiring:

| Orphan | Barrier description |
|--------|---------------------|
| `.agent/hooks/pre_compact_hook.py` (#7) | A2d must confirm the motor's `.agent/hooks/pre_compact_hook.py` resolves correctly when the destino's `.claude/settings.json` PreCompact hook fires. The motor settings.json:31 wires PreCompact to a candidate list that includes `root/.agent/hooks/pre_compact_hook.py`. If the destino session root resolves to the destino and not the motor, removing the destino copy will break PreCompact silently. A2d must verify or update the destino `.claude/settings.json` to point to the motor copy before removal. |
| `.agent/microagents/onboarding.md` (#8) | A2d must run `python scripts/install_agent_system.py --sync --project-root <destino>` after removal to re-provision from motor template, or removal leaves a permanent gap in the onboarding chain. |
| `.agent/glossary.md` (#9) | Same as #8. Installer-managed; A2d must re-sync after removal to restore from `agent_system/templates/glossary.md`. |

Orphans with NO A2d barrier (safe to archive without extra steps):
- #1 `scripts/artifact_graph.py`
- #2 `scripts/audit_codebase.py`
- #3 `scripts/rollback_agent_system.py`
- #4 `scripts/state_drift.py`
- #5 `scripts/test_refactor_manager_skill.py`
- #6 `tests/test_ticket_007_context_recovery.py`
- #10 `.goosehints`

---

## Corrections to triage_manifest.md

The triage_manifest declared a "vacio-hasta-prueba" conclusion for destino domain content.
This analysis confirms that conclusion: none of the 10 orphans implement authentic
repo_destino domain behavior. All 10 are classified as framework/system tooling or
deprecated artifacts.

**No corrections needed.** The "vacio-hasta-prueba" conclusion holds for this bucket.
The "motor-equivalent confirmed" for pre_compact_hook, onboarding, and glossary
refines the triage notes (triage said "ambiguous/posible host-specific"); this analysis
resolves the ambiguity: all three are installer-managed motor framework artifacts, not
host overrides.

Additionally, the triage note for `.agent/hooks/pre_compact_hook.py` said "motor
`.agent/hooks/` has `guard_paths.py`/`__init__.py` but NOT this hook". This is
**incorrect**: the motor DOES have `.agent/hooks/pre_compact_hook.py` (350 lines,
confirmed via `git -C motor ls-files .agent/hooks/`). The triage note was stale;
the motor added its canonical version (v2) after the destino copy was created.

---

## Grep Evidence Index (full citations)

### artifact_graph.py
- destino: `scripts/audit_codebase.py:81` (Path in ruff focus list)
- motor: no hits (`git -C motor grep artifact_graph` = empty)

### audit_codebase.py
- destino: `CHANGELOG.md:202,228,253,256,264,270,1160` (historical), `scripts/audit_codebase.py:78` (self-ref), `.agent/docs/triage_manifest.md:35,42,43,45` (doc)
- motor: no hits (`git -C motor grep audit_codebase` = empty)
- NO live invocation from `.github/`, `skills/`, `.claude/commands/`, `prompts/`

### rollback_agent_system.py
- destino: `scripts/upgrade_agent_system.py:123,269` (string in dict, not subprocess call), `agent_system/UPGRADE_GUIDE.md:169,176,193,198,203,317,326,352,353,372,481`, `CHANGELOG.md:428,462,543,548`
- motor: `CHANGELOG.md:816,830-834` (explicit "Exact duplicate of scripts/rollback.py"); `scripts/upgrade_agent_system.py:484` (string); motor canonical = `scripts/rollback.py`

### state_drift.py
- destino: `scripts/audit_codebase.py:18-21,54,80` (import and use within dead cluster), `CHANGELOG.md:246,257,265`
- motor: `tests/test_launcher_state_from_bus.py:305` (unrelated variable; not this script)

### test_refactor_manager_skill.py
- destino: `CHANGELOG.md:693` (historical evidence string)
- motor: no hits

### test_ticket_007_context_recovery.py
- destino: `tests/test_ticket_007_context_recovery.py` (self), imports `hooks.pre_compact_hook`; backlog/work_plan refs only
- motor: no hits

### pre_compact_hook.py
- destino: `tests/test_ticket_007_context_recovery.py:13,65,87,89,107,253,279,281,282,309,313,318` (test file), `agent_system/scripts/install_agent_system.py:266` (registers hook), `agent_system/scripts/clean_for_deployment.ps1:224` (path ref)
- motor: motor `.agent/hooks/pre_compact_hook.py` EXISTS (350 lines v2); motor `.claude/settings.json:31` wires PreCompact to it; `tests/unit/test_pre_compact_hook.py` (25 motor tests)

### onboarding.md
- destino: `.agent/glossary.md:11,27` (doc-to-doc pointer only)
- motor: `agent_system/templates/microagents/onboarding.md` (identical content); `scripts/install_agent_system.py:52,908-919,1063,1171` (installer-managed); `tests/unit/test_install_agent_system.py:413,421,422` (install test)

### glossary.md
- destino: `.agent/microagents/onboarding.md:11,27` (doc-to-doc only)
- motor: `agent_system/templates/glossary.md` (identical content); `scripts/install_agent_system.py:52,910-919` (INSTALLER_MANAGED_PATHS); `tests/unit/test_install_agent_system.py:391-438`

### .goosehints
- destino: `scripts/upgrade_agent_system.py:39` (cleanup list), `.claude/rules/02-multi-agent-system.md:19`, `.claude/rules/03-skills-discovery.md:20`
- motor: `.goosehints:1` (`[DEPRECATED - WT-2026-254a]` header); `AGENTS.md:7`; `scripts/upgrade_agent_system.py:50` (cleanup list); `.claude/rules/02-multi-agent-system.md:14` (deprecated)

---

## Manager review addendum (WOT-2026-002b review, 2026-06-13)

APROBADO con una refinacion de clasificacion para A2d. Spot-check adversarial del
"dead cluster" confirmado: ninguna skill `code-audit` del destino invoca
`audit_codebase.py` (backlog ticket cerrado lo reescribio a `vulture/deadcode/ruff`);
ningun entrypoint Python vivo importa el cluster. Decisiones 1-6 y 10: archive-legacy
solido.

**Refinacion #7, #8, #9 (precision de accion para A2d):** la evidencia de este mismo
doc demuestra que `pre_compact_hook.py`, `microagents/onboarding.md` y `glossary.md`
tienen version canonica en el motor y son **installer-managed** (`INSTALLER_MANAGED_PATHS`).
Por tanto su clasificacion operativa precisa es **motor-provides (installer-managed)**,
no `archive-legacy` muerto. La diferencia importa para A2d:

- `archive-legacy` = mover a `_archive/` (almacen muerto, no se re-provee).
- `motor-provides (installer-managed)` = retirar la copia del destino; el motor/installer
  la RE-PROVEE en el siguiente `install --sync`. El artefacto sigue VIVO via motor.

Accion correcta de A2d para #7/#8/#9: retirar la copia del destino y **re-sincronizar
desde el motor** (o, para #7, verificar/actualizar el wiring de `.claude/settings.json`
para que PreCompact resuelva al hook del motor) ANTES de dar por cerrada la retirada.
NO archivar-a-tumba. Esto los suma al set motor-provides de A2d (junto a
`agent_system/`, `skills/`, los 7 scripts comunes, `tests/`, `.agent/README.md`).

Las notas de "Barreras para A2d" de este doc ya prescriben la accion correcta; este
addendum solo corrige el LABEL para que el registro canonico no induzca un
archive-a-tumba erroneo.
