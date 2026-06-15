# Taxonomy Migration Manifest -- WOT-2026-008a

> deliverable_type: analysis. NO implementation. Single deliverable in
> repo_destino. STOP if written to repo_motor.

## 0. Metadata + root verification

- ticket_id: WOT-2026-008a / contract: T-008A-001 (frozen)
- delivery_authority: repo_destino
- AGENT_PROJECT_ROOT at run: UNSET -> writes targeted explicitly to repo_destino;
  validate run with --project-root <repo_destino>. (Root not trusted from env;
  this is the failure mode that contaminated the motor on the prior attempt.)
- repo_motor HEAD: ece7524 (git status --short: empty, verified before/after)
- repo_destino HEAD: 1feb0a7
- generated_at: 2026-06-15
- Inspection is read-only against repo_motor; the only writes are this file and
  execution_log.md in repo_destino.

## 1. Premise Re-check (read-only, evidence)

Premise: "el layout del motor es mayoritariamente plano y discovery/collision no
soportan skills anidadas." -> CONFIRMED (not a CONTRACT_GAP).

Counts (commands run in repo_motor):
- prompts/*.md = 19
- skills/**/SKILL.md = 29 (on disk)
- skills/**/PROMPT_TEMPLATE.md = 2
- skills/**/references/*.md = 33
- skills/_shared/*.md = 3
- llms*.txt = 2 (llms.txt, llms-full.txt) + scripts/build_llms.py
- MANIFEST.* = 2 (MANIFEST.distribute, MANIFEST.workspace)

Flatness demonstrated with code lines:
- scripts/discover_skills.py:99  `for skill_dir in sorted(directory.iterdir()):`
- scripts/discover_skills.py:297 `for skill_dir in sorted(skills_dir.iterdir()):`
  -> one level only; `skills/<cat>/<skill>/SKILL.md` would NOT be found.
- scripts/check_skill_collisions.py:54 `*root.glob("skills/*/SKILL.md")`
- scripts/check_skill_collisions.py:55 `*root.glob(".agent/skills/*/SKILL.md")`
  -> one level only.

Machine runs (no files modified):
- `python scripts/discover_skills.py --json` -> total_skills=28, total_triggers=87
- `python scripts/check_skill_collisions.py` -> "OK: no skill name or trigger collisions"

### DISCOVERY-GAP-1 (material finding)

discover_skills reports 28 skills but 29 SKILL.md exist on disk. The missing one
is `skills/man-review-implementation/SKILL.md` -- the canonical Manager review
skill. Its triggers `/review`, `code-review`, `/approve` are ALL absent from the
trigger_map; it appears in no discovered path. Candidate root cause (read-only,
not confirmed by debug): the directory name `man-review-implementation` differs
from the frontmatter `name: code-review`. Effect: agents relying on trigger
discovery cannot reach the Manager review skill; only the paired prompt
`prompts/review_manager.md` and the hardcoded bridge reach it. Owner:
DISCOVERY-INFRA follow-up ticket. This does NOT falsify the flat-premise, so no
CONTRACT_GAP; it is a defect to fix downstream.

### External reference (manifest-first), gh authenticated

- mattpocock/skills (129k stars; take the pattern, not gospel; it is a personal
  .claude dir, not an orchestrator): `.claude-plugin/plugin.json` lists explicit
  skill paths; layout is
  `skills/<engineering|productivity|deprecated|in-progress|misc|personal>/<skill>/SKILL.md`
  = ONE category level; per-skill progressive-disclosure docs (e.g. tdd/mocking.md);
  `deprecated/` and `in-progress/` exist on disk but are excluded from plugin.json
  -> the manifest, not the filesystem, defines the active API.
- OKF (GoogleCloudPlatform/knowledge-catalog okf/SPEC.md): markdown + YAML
  frontmatter, no schema registry, Concept-ID = path without .md, index.md router
  per level, links for relations. Supports minimal frontmatter + generated index,
  not a rigid taxonomy.

## 2. Surface separation (machine-executed / contract / documentation)

- machine-executed (consumed by code; breaks if moved without updating consumers):
  prompts referenced by scripts/build_llms.py, scripts/collect_system_health.py,
  scripts/encoding_guard.py; skills consumed by discover_skills.py /
  check_skill_collisions.py; MANIFEST.* read by install/sync; llms*.txt generated
  by build_llms.py.
- contract checks: prompts/audit_cf_*.md, prompts/audit_agent_output.md,
  prompts/review_manager.md (paired to man-review-implementation via source_prompt).
- documentation / pasteable context: bootstrap prompts, skills/_shared/*.md,
  skills/**/references/*.md (progressive-disclosure, loaded on demand).

## 3. Inventory (every path classified)

kind legend: router | workflow | audit | skill | template | reference | shared |
script | manifest | generated | bootstrap | contract

### 3.1 prompts/*.md (19) -- public API = file path (NO frontmatter/triggers today)

| path | kind | paired skill | consumers | proposed home | risk |
|------|------|--------------|-----------|---------------|------|
| audit_agent_output.md | audit/contract | audit-pipeline | audit skills, manual | prompts/ (router-indexed) | low |
| audit_bus.md | audit | (none) | manual | needs skill or route from system-health | med |
| audit_cf_plan_graph.md | contract | cf pipeline | contract_formation | keep separate (prog. disclosure) | low |
| audit_cf_repo_charter.md | contract | cf pipeline | contract_formation | keep separate | low |
| audit_cf_ticket_contract.md | contract | cf pipeline | contract_formation | keep separate | low |
| audit_complete_motor_destination.md | audit | (none) | manual | router-indexed | low |
| audit_git_publication.md | audit | audit-git-publication | skill | paired-stable | low |
| audit_pipeline.md | audit | audit-pipeline | skill | paired-stable | low |
| audit_plan.md | audit | grill-work-plan? | manual | router-indexed | low |
| audit_post_change_system_health.md | audit | system-health-audit | skill | paired-stable | low |
| contract_formation_pipeline.md | router/workflow | (none) | manual | promote to skill/router | med |
| destination_bootstrap.md | bootstrap | setup-agent-system? | destino agents | keep | low |
| launch_builder.md | workflow | launcher | launcher | machine-adjacent, keep | med |
| memory_upload.md | workflow | memory-consolidate? | manual | route from memory skill | low |
| orchestrator_pipeline.md | router/workflow | orchestrate-pipeline | skill | keep; do NOT split yet | med |
| refactor_bootstrap.md | bootstrap | refactor-manager | manual | thin alias of session+refactor | low |
| review_manager.md | contract | man-review-implementation | bridge, manual | paired-stable (see GAP-1) | high |
| session_bootstrap.md | bootstrap | (none) | new agents | keep canonical | low |
| session_close_chat.md | workflow | session-close-observations / man-session-closeout | manual | route from closeout skills | low |

Note: 10/19 prompts are audit/contract. Prompts have NO frontmatter today ->
they are not trigger-discoverable; only path-addressable.

### 3.2 skills/**/SKILL.md (29) -- public API = triggers + name

Discovered (28): audit-git-publication, audit-pipeline, bui-implement-from-plan,
bui-run-quality-gates, bui-self-audit, bui-write-deliverable, code-audit,
create-agent-skill, deep-research, graphify, grill-work-plan, local-audit,
man-create-work-plan, man-resolve-escalation, man-session-closeout,
memory-consolidate, orchestrate-pipeline, project-finalize, refactor-manager,
repo-compare, scaffold-python-project, secure-existing-project,
session-close-observations, setup-agent-system, system-health-audit,
systematic-debugging, test-driven-development, version-changelog.
NOT discovered (1): man-review-implementation (DISCOVERY-GAP-1).

Role families (existing partial taxonomy-by-prefix):
- bui-* (4): bui-implement-from-plan, bui-run-quality-gates, bui-self-audit, bui-write-deliverable
- man-* (4): man-create-work-plan, man-resolve-escalation, man-review-implementation, man-session-closeout
- audit-* (2): audit-git-publication, audit-pipeline
- session-* (1): session-close-observations
- unprefixed (18): code-audit, create-agent-skill, deep-research, graphify,
  grill-work-plan, local-audit, memory-consolidate, orchestrate-pipeline,
  project-finalize, refactor-manager, repo-compare, scaffold-python-project,
  secure-existing-project, setup-agent-system, system-health-audit,
  systematic-debugging, test-driven-development, version-changelog

Classification: all are `skill` kind; public API (triggers/name) must stay stable.
3 skills have NO triggers in frontmatter (bui-self-audit, systematic-debugging,
test-driven-development) -> invokable only by name/path, a discoverability gap.

### 3.3 templates / shared / references / scripts / manifests / generated

| path(s) | kind | owner | consumers | proposed home | risk |
|---------|------|-------|-----------|---------------|------|
| skills/refactor-manager/PROMPT_TEMPLATE.md | template | refactor-manager | skill | keep in skill dir | low |
| skills/repo-compare/PROMPT_TEMPLATE.md | template | repo-compare | skill | keep in skill dir | low |
| skills/_shared/anti-patterns.md | shared | multiple skills | skills | keep _shared (or index) | med |
| skills/_shared/ap-schema.md | shared | multiple skills | skills | keep _shared | med |
| skills/_shared/ticket-anti-patterns.md | shared | multiple skills | skills | keep _shared | med |
| skills/**/references/*.md (33) | reference | owning skill | that skill | keep IN skill dir (prog. disclosure) | low |
| scripts/discover_skills.py | script | infra | launcher/agents | infra; manifest-first candidate | high |
| scripts/check_skill_collisions.py | script | infra | CI/gates | infra | med |
| scripts/build_llms.py | script | infra | generates llms*.txt | infra | med |
| MANIFEST.distribute | manifest | motor boundary | install/sync | keep root | high |
| MANIFEST.workspace | manifest | workspace boundary | install/sync | keep root | high |
| llms.txt / llms-full.txt | generated | build_llms.py | external/agents | generated, never hand-edit | med |

references-by-skill (33 total, all classified as `reference`, owner = the skill):
audit-pipeline(1), bui-implement-from-plan(2), bui-run-quality-gates(1),
code-audit(2), create-agent-skill(2), deep-research(1), man-create-work-plan(3),
man-resolve-escalation(1), man-review-implementation(2), man-session-closeout(3),
orchestrate-pipeline(1), project-finalize(3), repo-compare(2),
scaffold-python-project(2), secure-existing-project(2),
session-close-observations(2), setup-agent-system(1), version-changelog(2).

## 4. Taxonomy depth -- HYPOTHESIS, not decision

Hypothesis H1: "max one category level" (skills/<cat>/<skill>/) is sufficient.
Evidence FOR: OKF (flat + index), mattpocock (one category level at scale),
system-prompt leaks (flat named sections).
Evidence AGAINST / cost: our discover_skills + collision are flat-only
(skills/*/SKILL.md); adopting categories REQUIRES either recursive discovery OR a
manifest-first registry FIRST, else 1+ skills vanish (cf. GAP-1 already shows a
single missing skill breaks the count silently).
Conclusion: depth is a tradeoff gated by the discovery mechanism, NOT a free
choice. -> see DEC-008-004.

## 5. Registry: manifest-first vs glob/recursive

Three distinct concerns that must not be conflated:
- public API: the trigger/name (and prompt path) an agent uses -> MUST stay stable.
- physical layout: where files live on disk -> can change if API + index updated.
- generated index: a derived router (INDEX.md or plugin.json) -> never hand-edited.

Options:
- A. glob flat (status quo): simple; blocks categories; silent gaps (GAP-1).
- B. recursive glob (skills/**/SKILL.md): enables categories; still no explicit
  API control; dedup/name issues persist (GAP-1 root cause unaddressed).
- C. manifest-first (mattpocock plugin.json style): an explicit list of canonical
  paths is the source of truth; layout free; deprecated/in-progress excluded by
  omission; index generated from it. Decouples API from layout.

Recommendation (for DEC-008-004): C (manifest-first) as the registry, with a
GENERATED index, keeping triggers/names as the stable public API. This removes the
"recursive discovery must come first" dependency for any future categorization.

## 6. Single canonical source per resource + shims

- Each resource has exactly ONE canonical home (table sec.3). A paired
  prompt<->skill (e.g. review_manager.md <-> man-review-implementation via
  source_prompt) are TWO layers of ONE resource, not duplicates: prompt = content,
  skill = entry/workflow.
- Any move uses a read-only, temporary shim (old path -> note pointing to the new
  canonical), each shim tagged with a removal ticket + version. No silent renames
  of public triggers/names.

## 7. DEC-008 (human decisions; Builder budget = 0, recommendations only)

- DEC-008-001: Categorize skills by role/domain (one level) vs keep flat-by-prefix.
  Recommend: defer to after DEC-008-004; the prefix taxonomy already partially works.
- DEC-008-002: Add minimal frontmatter to prompts (id, kind, stage, role,
  description, paired_skill, contract_id, status, tags). Recommend YES; enables a
  prompts index without renames. No derived fields (no line-count/date -> drift).
- DEC-008-003: Generated prompts/INDEX.md + skills index (router). Recommend YES,
  generated only.
- DEC-008-004: Manifest-first registry (plugin.json-style) vs glob/recursive
  discovery. Recommend manifest-first (option C, sec.5). Highest leverage.
- DEC-008-005: Promote contract_formation_pipeline.md to a formal skill/router;
  give audit_bus.md a skill or route it from system-health. Recommend YES.
- DEC-008-006: deprecated/ + in-progress/ convention (mattpocock pattern) instead
  of inline [DEPRECATED] tags; first verify dead Goose/Claw refs. Recommend YES.

## 8. Decomposition into follow-up tickets (with deps)

1. WOT-2026-008b DISCOVERY-INFRA: implement the manifest-first registry + generated
   index; FIX DISCOVERY-GAP-1 (man-review-implementation). Blocks 008c/008d.
   Gates: ruff, pytest-safe, discover/collision parity test (registry == disk).
2. WOT-2026-008c PROMPTS MIGRATION: add frontmatter + prompts index; shims for any
   moved path. Depends on 008b. Gates: encoding guard, build_llms parity.
3. WOT-2026-008d SKILLS MIGRATION: optional category layout (only if DEC-008-001
   YES); update registry; preserve triggers/names. Depends on 008b.
4. WOT-2026-008e SHIM RETIREMENT: remove temporary shims after N versions.
   Depends on 008c + 008d.

## 9. Risks / STOP / rollback / gates per phase

Risks:
- R1 (high): moving a skill without updating discovery/registry -> the skill
  vanishes (GAP-1 is the existing proof this happens silently).
- R2 (high): renaming a public trigger/name -> breaks bridge/launcher invocation.
- R3 (med): editing generated llms*.txt by hand -> drift; must regenerate.
- R4 (med): touching MANIFEST.* -> install/sync boundary breakage.

STOP conditions (inherited + reinforced): no move/rename/delete; no motor edits;
no shims created in this ticket; no implementation; stop if the motor HEAD changes
mid-ticket; STOP if any deliverable is written outside repo_destino.

Rollback: this ticket is analysis-only; rollback = delete this file. Migration
tickets (008b-e) each land behind their own gates with shim-based reversibility.

Gates per migration phase (for later tickets, not run here):
- ruff check . ; python scripts/run_pytest_safe.py
- python scripts/discover_skills.py --json (registry vs disk parity == 0 diff)
- python scripts/check_skill_collisions.py (no collisions)
- encoding guard on changed markdown
- python .agent/agent_controller.py --validate --json --project-root <destino> -> 0/0
- git status --short of repo_motor stays empty when authority=destino

## 10. Completeness statement

All inventoried paths (19 prompts + 29 SKILL.md + 2 PROMPT_TEMPLATE.md +
33 references + 3 _shared + 3 scripts + 2 manifests + 2 generated) are classified
in section 3. No resource left unclassified. One discovery defect (GAP-1) found and
assigned to 008b. Premise (flat discovery) confirmed in code; no CONTRACT_GAP.
