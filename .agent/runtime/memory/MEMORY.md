# MEMORY

Regenerated: 2026-06-20T23:14:46.435621+00:00

Total observations: 58

- Architecture (21 observations)
- Atomic-Requeue-Claim (1 observations)
- Auditor-Skeptic-Pattern (1 observations)
- Backlog-Summary-Detail-Reconcile-After-Rescope (1 observations)
- Bom-Breaks-Lightweight-Validators (1 observations)
- Builder-Evidence-Gate (1 observations)
- Builder-Validates-Existing-Work (1 observations)
- Bus-First-Read-Authority (1 observations)
- Canonical-Consumer-Recovery (1 observations)
- Canonical-Suite-Measurement (1 observations)
- Chat-Manager-Builder-Recovery (1 observations)
- Cleanup-Vs-Bus-Reconcile (1 observations)
- Delivery-Hygiene (1 observations)
- Double-Requeue-Diagnostics (1 observations)
- Dual-Contract-Sync (1 observations)
- Manager-Is-Fix-Surface (1 observations)
- Manual-Review-Hygiene (1 observations)
- Motor-Destino-Topology (2 observations)
- One-Line-Fix-Contract-Pattern (1 observations)
- Orthogonal-Validator-Tests (1 observations)
- Plan-Test-Path-Verification (1 observations)
- Planning-Snippets-Are-Executable-Spec (1 observations)
- Planning-Test-Existence-Check (1 observations)
- Post-Write-Verification (2 observations)
- Recovery-Idempotency (1 observations)
- Runtime-Memory-Storage (1 observations)
- Runtime-Proof-For-Concurrency-Fixes (1 observations)
- Scope-Gate-Path-Format (1 observations)
- Session-Bootstrap-Audit-Snapshot (1 observations)
- Session-Close-May-Need-Final-Memory-Commit (1 observations)
- Suite-Performance (1 observations)
- Ticket-Completion (4 observations)
- Ticket-Letter-Recovery-Rule (1 observations)

## architecture
- Decisiones arquitectonicas documentadas en WOT-2026-010c
- Decisiones arquitectonicas documentadas en WOT-2026-008c
- Decisiones arquitectonicas documentadas en WOT-2026-010a
- Decisiones arquitectonicas documentadas en WOT-2026-009g
- Decisiones arquitectonicas documentadas en WOT-2026-008b
- Decisiones arquitectonicas documentadas en WOT-2026-009d
- Decisiones arquitectonicas documentadas en WOT-2026-003d
- Decisiones arquitectonicas documentadas en WOT-2026-005d
- Decisiones arquitectonicas documentadas en WOT-2026-005c
- Decisiones arquitectonicas documentadas en WOT-2026-005b

## atomic-requeue-claim
- Cross-process requeue authority should be a real atomic claim keyed by (ticket_id, trigger_seq), not a read-modify-write watermark. The watermark is a fast-path, but it cannot survive concurrent super

## auditor-skeptic-pattern
- The strongest review role is an auditor who searches for counterexamples in the real codebase and test suite, not a second pass that only judges whether the contract sounds plausible. That role catche

## backlog-summary-detail-reconcile-after-rescope
- When a ticket is re-scoped or closed through follow-up reviews, the backlog table and the detailed ticket cards can drift apart. Before final closeout, reconcile both layers so the summary rows and de

## bom-breaks-lightweight-validators
- UTF-8 with BOM can make lightweight validators and Windows subprocess readers fail as if frontmatter or text were missing entirely. In operational artifacts parsed with regex or line-prefix heuristics

## builder-evidence-gate
- When Builder can declare ready without implementation evidence, Manager spends review cycles detecting an obvious no-op. The durable defense is a --mark-ready evidence gate that checks real file chang

## builder-validates-existing-work
- When the implementation is already committed, Builder's job is not to reimplement it but to verify it systematically against the AUDIT, TP checks, tests, and closure gates. In that situation the highe

## bus-first-read-authority
- For operational launch, resume, and recovery decisions, derive ticket state from the event bus first and treat TURN.md/STATE.md as fallback or documentary projections only. WT-2026-216 established thi

## canonical-consumer-recovery
- When a critical bus trigger outlives its main consumer, the durable fix is to ensure the canonical consumer runs again rather than adding a second authority. WT-2026-212 applied this by having review_


---

[MEMORY.md truncated at 80 lines. Full history available in observations.jsonl]