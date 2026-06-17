# Audit Checklist: WOT-2026-010r

## Blockers

- The report does not exist at `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`.
- The report modifies or requires modifying `skills/`, `prompts/`, discovery code, resolver code, Manager review code, `CREDITS.md`, dependency files, bus, or private files.
- The report treats mattpocock/skills as code to install or copy instead of ideas to evaluate.
- Release metadata is cited without a source or without noting `gh` failure when applicable.
- Local consumer counts are repeated from chat without a reproducible command.
- Evidence and inference are mixed without labels.
- `validate --json --project-root <repo_destino>` is not 0/0.

## Acceptance Checks

- Confirms `010g` inventory is the local baseline.
- Covers all release pieces named in the contract.
- Maps impact on `008c`, `008d`, `010s`, and `010t`.
- States that CREDITS is deferred until adoption tickets.
- Contains a clear recommendation and a clear rejection/defer list.
- Encoding guard passes for the report and packet files touched.

## Anti-patterns

- Scope creep: doing `010s` or `010t` inside `010r`.
- Porting external files instead of adapting concepts.
- Replacing `triggers` without proving trigger_map parity.
- Adding elegant vocabulary to Manager review without concrete checklist entries.
- Treating unauthenticated `gh` as a blocker when public fetch is enough for analysis.
