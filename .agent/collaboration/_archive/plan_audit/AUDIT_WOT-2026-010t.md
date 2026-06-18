# Audit Checklist: WOT-2026-010t

## Blockers

- Code, discovery, resolver, bus, prompts, dependency files or external bundle copied.
- No CREDITS row despite adopting external vocabulary.
- CREDITS row is unpinned, license missing, or says `Ported` without copied-text justification.
- Review checklist contains abstract definitions only, no actionable Manager questions.
- Anti-pattern entry forces new abstractions instead of detecting overengineering.
- Protocol note lacks a real existing artifact example.
- `diagnosing-bugs` adaptation weakens or removes the 3-attempt stop from `systematic-debugging`.
- Encoding guard or validate fails.

## Acceptance Checks

- Checklist asks: interface? test surface? seam? adapter? deletion test?
- Anti-patterns distinguish invented seam/adapter from useful boundary.
- Protocol doc applies vocabulary to a real artifact, not a hypothetical module.
- The ticket remains documentation-only.
- All touched markdown passes encoding guard.
- `validate --json` is 0 errors / 0 warnings.

## Non-blocking but useful

- If v1.0.1 does not affect codebase-design, mention that briefly.
- If review-checklist normalization causes large diff, explain it in execution_log.