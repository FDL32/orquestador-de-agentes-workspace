# Memory Rules (L2)

Total rules: 6

Rules derived deterministically from observations.jsonl. Each rule carries an ID (R-XXX), domain, wing, source ticket, and signal text.

## Wing: engine

### Domain: bus-architecture

#### R-002: Recovery paths must be idempotent against the primary mechanism. Before emitting

Recovery paths must be idempotent against the primary mechanism. Before emitting a corrective event or relaunching an agent, check whether the target event already exists in the bus for the same ticket and decision.

*Source: WT-2026-191*


## Wing: meta

### Domain: review-quality

#### R-005: Before closing a technical plan, verify proposed test file paths against the fil

Before closing a technical plan, verify proposed test file paths against the filesystem. Wrong test paths have caused repeated planning drift and can make Builder create tests in the wrong location.

*Source: WT-2026-191*


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

