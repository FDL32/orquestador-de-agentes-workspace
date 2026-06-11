## Wing: engine

### Domain: ap-nn-cross-cutting-architecture

#### R-002: AP-NN numbering system established as cross-cutting convention linking 3 artifac

AP-NN numbering system established as cross-cutting convention linking 3 artifacts: skills/_shared/anti-patterns.md (canonical source of IDs + names), bui-implement-from-plan/references/code-rules.md (Builder preventive rules, detailed examples), man-review-implementation/references/review-checklist.md (Manager BLOCKER checklist). Adding a new AP requires touching all 3. observations.jsonl can carry anti_pattern_id field to link findings to AP-NN. AP-01..AP-08 active. Origin: session 2026-05-25.

*Source: session-2026-05-25*

## Wing: meta

### Domain: manager-review-rubric

#### R-011: AP-08 candidate: Test coverage drift. The Builder runs the existing suite, sees

AP-08 candidate: Test coverage drift. The Builder runs the existing suite, sees it pass, and declares quality gates satisfied — but the new functions introduced in the diff have no direct tests. The suite passing is not evidence of coverage when the new code is never called by any test. Manager rule: when the diff introduces new functions (def, method, classmethod), verify that at least one test in test_*.py calls each new function directly. Absence of direct test coverage for new functions = BLOCKER, even if the full suite passes. Origin: WP-2026-139 audit — 3 new methods (_parse_canonical_anti_patterns, _load_canonical_anti_patterns, _render_canonical_anti_pattern_inventory) had zero tests; Manager approved without noticing.

#### R-012: BLOCKER pattern: Boolean truthiness regression in changed return contracts. When

BLOCKER pattern: Boolean truthiness regression in changed return contracts. When a method changes from returning implicit None to returning explicit bool, all callers must be updated from generic truthiness guards (if not x, if x, while x) to identity checks (is False, is True). Mixing None/False/True under a falsy guard silently breaks when the method is monkeypatched to return None (common in tests) or called from a legacy path that predates the type change. Manager must grep all callers in the diff and verify no if not / if pattern remains. Any surviving generic guard = CHANGES. Origin: WP-2026-137 bug audit.

#### R-013: BLOCKER pattern: Exclusive resource acquisition without reentrancy guard. When a

BLOCKER pattern: Exclusive resource acquisition without reentrancy guard. When a method acquires an exclusive resource (O_CREAT|O_EXCL, flock, Lock.acquire, lock-file creation) AND can be reached from more than one call site or called twice on the same instance (e.g. standalone call + internal call from a wrapper), there must be an explicit instance-level reentrancy guard. Without it, the second call hits the exclusion check with its own PID alive and returns False, silently aborting the caller. Manager should grep all call sites of the method in the diff and repo. No reentrancy guard = CHANGES. Origin: WP-2026-137 bug audit.

#### R-014: Validator evidence gate: when a work_plan explicitly declares a validator as a q

Validator evidence gate: when a work_plan explicitly declares a validator as a quality gate (skills/validate_all.py, agent_controller --validate, ruff, pytest), the Manager must find explicit output from that validator showing a clean result in execution_log.md. Declared validator + absent evidence = BLOCKER. This applies especially to scaffolding and documentation tickets where standard code gates do not run automatically. Origin: WP-2026-133 audit.

#### R-015: deliverable_type classification for scaffolding tickets: when Files Likely Touch

deliverable_type classification for scaffolding tickets: when Files Likely Touched contains only structural non-Python files (.gitkeep, empty dirs, placeholders, config stubs) with no logic, the correct deliverable_type is documentation, not code. Using code triggers ruff+pytest rubric which produces false noise on files with no logic. Manager should flag code classification for pure-scaffolding tickets as a planning error (SUGGESTIONS). Origin: WP-2026-133 audit.


### Domain: return_type_falsy_guard

#### R-018: WP-2026-137: Changing a method return type from None->bool (bootstrap) requires

WP-2026-137: Changing a method return type from None->bool (bootstrap) requires updating callers from "if not method():" to "if method() is False:". The falsy guard caused a test regression: existing test monkeypatched bootstrap to "lambda: None", so "if not None" was True and run_reactive exited immediately. Rule: when a method previously returned None and is refactored to return bool, always use "is False" guards in callers to avoid false-positive exits on None-returning mocks or legacy callers.


### Domain: review-quality

#### R-019: AP-12: WP-2026-157: the review packet built from git diff HEAD hid brand-new unt

AP-12: WP-2026-157: the review packet built from git diff HEAD hid brand-new untracked files, so the Manager saw an incomplete/partial diff while the real deliverables lived outside the tracked set. Rule: review packets must include new untracked deliverables explicitly, not only tracked-file diffs.


### Domain: silent_subprocess_failure_pattern

#### R-022: subprocess.run with capture_output=True silently discards stderr/stdout unless r

subprocess.run with capture_output=True silently discards stderr/stdout unless returncode is checked. Pattern: always store subprocess result and log stderr to sys.stderr on rc != 0, especially for state-transition subprocesses where silent failure breaks re-engagement chains.


### Domain: ticket-structure-risk-heuristic

#### R-027: Structural complexity predicts regression risk better than file count. Tickets t

Structural complexity predicts regression risk better than file count. Tickets that apply the same atomic operation N times (e.g. create .gitkeep in 7 dirs) carry near-zero regression risk regardless of file count — majority-scaffolding scope = light review. Tickets that change behavior across multiple call sites or layers carry high risk even with few files — cross-layer behavior changes = deep review. Use as context signal when calibrating review depth, not as a hard blocker criterion. Origin: WP-2026-133 vs WP-2026-137 contrast.

## Wing: project

### Domain: builder-contract

#### R-001: When Builder can declare ready without implementation evidence, Manager spends r

When Builder can declare ready without implementation evidence, Manager spends review cycles detecting an obvious no-op. The durable defense is a --mark-ready evidence gate that checks real file changes and non-boilerplate execution_log evidence, not longer prompt instructions.

*Source: WT-2026-191*


### Domain: delivery-hygiene

#### R-003: Closed the installer idempotency audit. Key invariant: detect_destination_residu

Closed the installer idempotency audit. Key invariant: detect_destination_residues() must not rely only on source-vs-dest comparison; INSTALLER_MANAGED_PATHS separates once-deposited destination-owned paths (glossary.md, microagents/) from true residues. is_preserved() means never sync from motor, not exclude-from-prune. Follow-up tickets WT-2026-187 and WT-2026-188 remain in backlog.

*Source: WT-2026-186*

#### R-004: El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descr

El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descriptivo. Patron observado: WT-2026-186 commiteado como WP-2026-176, WT-2026-189 sin commit hasta cierre manual, WT-2026-187 con mensajes pre-handoff checkpoint. El Builder cierra el trabajo tecnico correctamente pero el packaging del commit falla sistematicamente.

*Source: WT-2026-189*


### Domain: testing

#### R-006: For validators with multiple failure modes, keep tests orthogonal: each test sho

For validators with multiple failure modes, keep tests orthogonal: each test should exercise exactly one failure mode while all other fields remain valid. Avoid using one dramatic invalid fixture to cover multiple checks, because it hides which rule failed and can leave validators under-specified.

*Source: WT-2026-191*
