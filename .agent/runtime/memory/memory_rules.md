# Memory Rules (L2)

Total rules: 24

Rules derived deterministically from observations.jsonl. Each rule carries an ID (R-XXX), domain, wing, source ticket, and signal text.

## Wing: engine

### Domain: bus-architecture

#### R-006: For operational launch, resume, and recovery decisions, derive ticket state from

For operational launch, resume, and recovery decisions, derive ticket state from the event bus first and treat TURN.md/STATE.md as fallback or documentary projections only. WT-2026-216 established this as the canonical read path by routing launcher decisions through StateMachine.derive_state_from_events() before consulting TURN.md.

*Source: WT-2026-216*

#### R-007: Local runtime cleanup and bus reconciliation are different recovery classes. If

Local runtime cleanup and bus reconciliation are different recovery classes. If the previous ticket is already terminal in the bus, clean stale local runtime only; if it is non-terminal with confirmed drift, reconcile explicitly in the bus; if the bus is unreadable or contradictory, abort without closing anything. This is the preflight contract for WT-2026-214.

*Source: WT-2026-214*

#### R-008: Recovery paths must be idempotent against the primary mechanism. Before emitting

Recovery paths must be idempotent against the primary mechanism. Before emitting a corrective event or relaunching an agent, check whether the target event already exists in the bus for the same ticket and decision.

*Source: WT-2026-191*

#### R-009: When a critical bus trigger outlives its main consumer, the durable fix is to en

When a critical bus trigger outlives its main consumer, the durable fix is to ensure the canonical consumer runs again rather than adding a second authority. WT-2026-212 applied this by having review_bridge force a real supervisor tick after REVIEW_DECISION=CHANGES instead of relaunching Builder directly.

*Source: WT-2026-212*


## Wing: meta

### Domain: delivery-hygiene

#### R-013: This system starts every plan with a base `...a` ticket; `...b` and later letter

This system starts every plan with a base `...a` ticket; `...b` and later letters are for plan splits or post-close fixes. When a shell-launched Builder leaves the bus short of canonical termination, analyze the root cause first, close the `...a` by chat, and move remediation to derived tickets instead of trying to fix the bus through the live bus path.

*Source: WT-2026-243a*

#### R-014: Ticket WT-2026-251a completado: ** Centralizar ticket-ID regex y extender a pref

Ticket WT-2026-251a completado: ** Centralizar ticket-ID regex y extender a prefijos de 2-3 letras (deliverable_type=code)

*Source: WT-2026-251a*


### Domain: review-quality

#### R-016: Any regex, import path, literal string, or code snippet inside a plan acts as ex

Any regex, import path, literal string, or code snippet inside a plan acts as executable specification because Builder tends to copy it verbatim. Validate those snippets before launch; a bad escape sequence or malformed literal turns the contract itself into the source of a failing test.

*Source: WT-2026-201*

#### R-017: Before closing a technical plan, verify proposed test file paths against the fil

Before closing a technical plan, verify proposed test file paths against the filesystem. Wrong test paths have caused repeated planning drift and can make Builder create tests in the wrong location.

*Source: WT-2026-191*

#### R-018: Before freezing 'Tests Esperados' in a plan or audit, verify whether each named

Before freezing 'Tests Esperados' in a plan or audit, verify whether each named test already exists in the suite. Existing tests are non-regression checks, not new Builder deliverables; listing them as new can cause duplicated tests or scope confusion.

*Source: WT-2026-201*

#### R-019: For concurrency or cross-process coordination fixes, passing tests is necessary

For concurrency or cross-process coordination fixes, passing tests is necessary but not sufficient. Confirm at least one runtime cycle with real bus evidence, because scheduler timing and process races can stay invisible to unit tests even when the code and mocks look correct.

*Source: WT-2026-199*

#### R-020: For one-line fixes with high regression risk, the minimum useful contract is sma

For one-line fixes with high regression risk, the minimum useful contract is small and exact: name the symbol or line that changes as old -> new, name the test that breaks by design, and name the symmetric anti-regressions on both sides of the change. Beyond that, contract detail tends to have diminishing returns.

*Source: WT-2026-200*

#### R-021: The Manager is not an untouchable narrator layer. If the fault lives in review i

The Manager is not an untouchable narrator layer. If the fault lives in review instructions, prompt contracts, or parser expectations, correcting the Manager itself is part of normal system hardening and should be documented as such.

*Source: WOT-2026-001c*

#### R-022: The strongest review role is an auditor who searches for counterexamples in the

The strongest review role is an auditor who searches for counterexamples in the real codebase and test suite, not a second pass that only judges whether the contract sounds plausible. That role catches failure modes the Manager can miss when the contract is internally consistent but still wrong.

*Source: WT-2026-199*

#### R-023: When a planning correction lands during review, apply it to both `work_plan.md`

When a planning correction lands during review, apply it to both `work_plan.md` and `PLAN_WT-*`. They are not redundant copies: `work_plan.md` drives validation and canonical state, while `PLAN_WT-*` is the technical contract Builder reads. In WT-2026-193, fixing paths in only one file and the function name in only the other caused two extra review rounds.

*Source: WT-2026-193*


## Wing: project

### Domain: builder-contract

#### R-001: Cross-process requeue authority should be a real atomic claim keyed by (ticket_i

Cross-process requeue authority should be a real atomic claim keyed by (ticket_id, trigger_seq), not a read-modify-write watermark. The watermark is a fast-path, but it cannot survive concurrent supervisor/subprocess races. trigger_seq must be mandatory; None should fail closed.

*Source: WT-2026-199*

#### R-002: Files Likely Touched must use paths relative to the motor git repo, in the same

Files Likely Touched must use paths relative to the motor git repo, in the same string format returned by `git diff --name-only`. Example correct: `bus/redact.py`. Example incorrect: `orquestador_de_agentes/bus/redact.py`. The scope gate intersects those strings directly; the prefixed form yields an empty intersection and blocks `--mark-ready`. Observed again in WT-2026-193 after the same trap already appeared in WT-2026-198.

*Source: WT-2026-193*

#### R-003: When Builder can declare ready without implementation evidence, Manager spends r

When Builder can declare ready without implementation evidence, Manager spends review cycles detecting an obvious no-op. The durable defense is a --mark-ready evidence gate that checks real file changes and non-boilerplate execution_log evidence, not longer prompt instructions.

*Source: WT-2026-191*

#### R-004: When the implementation is already committed, Builder's job is not to reimplemen

When the implementation is already committed, Builder's job is not to reimplement it but to verify it systematically against the AUDIT, TP checks, tests, and closure gates. In that situation the highest-value Builder work is evidence gathering, gap detection, and clean canonical closeout.

*Source: WT-2026-199*

#### R-005: When the implementation is already verified but the bus or session-close path dr

When the implementation is already verified but the bus or session-close path drifts, the low-noise recovery is to close the base `...a` by chat with evidence and move infra fixes to derived tickets. Several intensive sessions validated this as a durable operating pattern.

*Source: WOT-2026-001b*


### Domain: delivery-hygiene

#### R-010: El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descr

El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descriptivo. Patron observado: WT-2026-186 commiteado como WP-2026-176, WT-2026-189 sin commit hasta cierre manual, WT-2026-187 con mensajes pre-handoff checkpoint. El Builder cierra el trabajo tecnico correctamente pero el packaging del commit falla sistematicamente.

*Source: WT-2026-189*

#### R-011: If two BUILDER_RELAUNCH_ATTEMPTED events for the same ticket have different roun

If two BUILDER_RELAUNCH_ATTEMPTED events for the same ticket have different rounds, requeue_ticket() ran twice for the same decision. And when outcome=success appears in older bus history, it only proves launcher exit 0, not Builder liveness; the new taxonomy must distinguish builder_started_verified from builder_launch_unverified.

*Source: WT-2026-199*

#### R-012: In this repo_destino, keeping a fresh `.agent/runtime/audit/AUDIT.md` after cano

In this repo_destino, keeping a fresh `.agent/runtime/audit/AUDIT.md` after canonical closeout shortens safe restarts because the next session can trust one local snapshot first instead of reconstructing context from scattered collaboration files.

*Source: WT-2026-242c*

#### R-015: UTF-8 with BOM can make lightweight validators and Windows subprocess readers fa

UTF-8 with BOM can make lightweight validators and Windows subprocess readers fail as if frontmatter or text were missing entirely. In operational artifacts parsed with regex or line-prefix heuristics, write UTF-8 without BOM and force UTF-8 decoding in subprocesses.

*Source: WOT-2026-001c*


### Domain: testing

#### R-024: For validators with multiple failure modes, keep tests orthogonal: each test sho

For validators with multiple failure modes, keep tests orthogonal: each test should exercise exactly one failure mode while all other fields remain valid. Avoid using one dramatic invalid fixture to cover multiple checks, because it hides which rule failed and can leave validators under-specified.

*Source: WT-2026-191*

