# Memory Profile (L3)

Total observations: 6

High-level profile of project memory for quick context loading. This is the first memory tier loaded (before L2 rules and L1 raw observations).

## Active Domains

- delivery-hygiene: 2 observations
- bus-architecture: 1 observations
- review-quality: 1 observations
- testing: 1 observations
- builder-contract: 1 observations

## Active Tickets Referenced

- WT-2026-186
- WT-2026-189
- WT-2026-191

## Recent Signals

- [delivery-hygiene] El cierre canonico no valida que el ultimo commit del ticket tenga mensaje descriptivo. Patron observado: WT-2026-186 commiteado como WP-2026-176, WT- (migrated:WT-2026-191)
- [audit-closeout] Closed the installer idempotency audit. Key invariant: detect_destination_residues() must not rely only on source-vs-dest comparison; INSTALLER_MANAGE (migrated:WT-2026-191)
- [recovery-idempotency] Recovery paths must be idempotent against the primary mechanism. Before emitting a corrective event or relaunching an agent, check whether the target  (migrated:WT-2026-191)
- [plan-test-path-verification] Before closing a technical plan, verify proposed test file paths against the filesystem. Wrong test paths have caused repeated planning drift and can  (migrated:WT-2026-191)
- [orthogonal-validator-tests] For validators with multiple failure modes, keep tests orthogonal: each test should exercise exactly one failure mode while all other fields remain va (migrated:WT-2026-191)
- [builder-evidence-gate] When Builder can declare ready without implementation evidence, Manager spends review cycles detecting an obvious no-op. The durable defense is a --ma (migrated:WT-2026-191)
