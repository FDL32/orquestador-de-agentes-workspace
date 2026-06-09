# MEMORY

Regenerated: 2026-06-09T00:00:00Z

Total observations: 21

- Audit-Skeptical-Review (1 observations)
- Audit-Closeout (1 observations)
- Atomic-Requeue-Claim (1 observations)
- Builder-Evidence-Gate (1 observations)
- Builder-Validates-Existing-Work (1 observations)
- Bus-First-Read-Authority (1 observations)
- Canonical-Consumer-Recovery (1 observations)
- Cleanup-vs-Bus-Reconcile (1 observations)
- Dual-Contract-Sync (1 observations)
- Double-Requeue-Diagnostics (1 observations)
- Delivery-Hygiene (1 observations)
- One-Line-Fix-Contract-Pattern (1 observations)
- Orthogonal-Validator-Tests (1 observations)
- Planning-Snippets-Are-Executable-Spec (1 observations)
- Planning-Test-Existence-Check (1 observations)
- Plan-Test-Path-Verification (1 observations)
- Recovery-Idempotency (1 observations)
- Runtime-Proof-For-Concurrency-Fixes (1 observations)
- Session-Bootstrap-Audit-Snapshot (1 observations)
- Ticket-Letter-Recovery-Rule (1 observations)
- Scope-Gate-Path-Format (1 observations)

## audit-closeout
- Closed the installer idempotency audit. Key invariant: detect_destination_residues() must not rely only on source-vs-dest comparison; INSTALLER_MANAGED_PATHS separates once-deposited destination-owned

## auditor-skeptic-review
- The strongest review role is an auditor who looks for counterexamples in the real codebase and test suite, because a contract can be internally consistent and still be wrong in a specific mock, race, or timestamp comparison.

## atomic-requeue-claim
- Cross-process requeue authority should be a real atomic claim keyed by (ticket_id, trigger_seq), not a read-modify-write watermark. The watermark can be a fast-path, but it cannot survive concurrent supervisor/subprocess races.

## builder-evidence-gate
- When Builder can declare ready without implementation evidence, Manager spends review cycles detecting an obvious no-op. The durable defense is a --mark-ready evidence gate that checks real file chang

## builder-validates-existing-work
- When the implementation is already committed, Builder adds the most value by validating against AUDIT, TP checks, tests, and closeout gates instead of reimplementing work that already exists.

## bus-first-read-authority
- For operational launch, resume, and recovery decisions, derive ticket state from the event bus first and treat TURN.md/STATE.md as fallback or documentary projections only. Architectural rule from WT-2026-216; related: canonical-consumer-recovery, cleanup-vs-bus-reconcile.

## canonical-consumer-recovery
- When a critical bus trigger outlives its main consumer, the durable fix is to ensure the canonical consumer runs again rather than adding a second authority. Architectural rule from WT-2026-212; related: bus-first-read-authority.

## cleanup-vs-bus-reconcile
- Local runtime cleanup and bus reconciliation are different recovery classes: terminal bus + stale runtime => clean local only; non-terminal bus + confirmed drift => reconcile in bus; unreadable or contradictory bus => abort. Operational preflight rule for WT-2026-214; related: bus-first-read-authority, canonical-consumer-recovery.

## dual-contract-sync
- When a planning correction lands during review, apply it to both work_plan.md and PLAN_WT-*. work_plan.md drives validation and canonical state; PLAN_WT-* is the technical contract Builder reads.

## double-requeue-diagnostics
- If two BUILDER_RELAUNCH_ATTEMPTED events for the same ticket have different rounds, requeue_ticket() ran twice for the same decision. And when outcome=success appears in older bus history, it only proves launcher exit 0, not Builder liveness.

## delivery-hygiene
- El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descriptivo. Patron observado: WT-2026-186 commiteado como WP-2026-176, WT-2026-189 sin commit hasta cierre manual, WT-2026-1

## one-line-fix-contract-pattern
- For one-line fixes with real regression risk, the useful contract is exact but small: old -> new mutation, the test that breaks by design, and the symmetric anti-regressions around the change.

## orthogonal-validator-tests
- For validators with multiple failure modes, keep tests orthogonal: each test should exercise exactly one failure mode while all other fields remain valid. Avoid using one dramatic invalid fixture to c

## planning-snippets-are-executable-spec
- Regexes, literal strings, and import paths inside a plan behave like executable specification because Builder often copies them verbatim; validate them before launch or the contract itself becomes the source of a broken test.

## planning-test-existence-check
- Before freezing Tests Esperados, verify whether each named test already exists. Existing tests are non-regression checks, not new deliverables, and listing them as new can lead to duplicate coverage and scope drift.

## plan-test-path-verification
- Before closing a technical plan, verify proposed test file paths against the filesystem. Wrong test paths have caused repeated planning drift and can make Builder create tests in the wrong location.

## recovery-idempotency
- Recovery paths must be idempotent against the primary mechanism. Before emitting a corrective event or relaunching an agent, check whether the target event already exists in the bus for the same ticke

## runtime-proof-for-concurrency-fixes
- For concurrency and cross-process fixes, green tests are necessary but not sufficient; confirm at least one real runtime cycle with bus evidence because scheduler timing can invalidate conclusions drawn from mocks alone.

## session-bootstrap-audit-snapshot
- In this repo_destino, a fresh `.agent/runtime/audit/AUDIT.md` is worth keeping after canonical closeout because the local session bootstrap can trust that snapshot first instead of reconstructing context from scattered collaboration files on every restart.

## ticket-letter-recovery-rule
- Every plan starts from a completed `...a` ticket. Tickets `...b`, `...c`, `...d` and later letters are for planned splits or for fixes discovered after the `...a` closeout. And when a shell-launched Builder leaves the bus short of canonical termination, the durable path is root-cause analysis first, then chat closeout of the `...a`, then remediation through derived tickets instead of trying to repair the bus through the live bus itself.

## scope-gate-path-format
- Files Likely Touched must use the same path strings returned by git diff --name-only. Prefixing them with orquestador_de_agentes/ breaks the scope gate even when the correct file changed.

---

## Archive Pointers

No archive files yet.

Stats: kept=21, deduped=0, dropped=0, archived=0
