# Strategy: WOT-2026-010t

## Intent

Turn the `010r` recommendation into practical Manager review language. This is documentation work: checklist, shared anti-pattern reference, CREDITS attribution, and one protocol note with a real example.

## External Source Handling

- Use `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md` as local baseline.
- Re-check `mattpocock/skills` tag/SHA before editing. If `gh` is available, prefer `gh release view` / `gh api`; otherwise document public fetch limitation.
- Do not copy long text. Adapt concepts in local words.
- Add CREDITS row only for this adopted vocabulary ticket.

## Local Edits

1. `skills/man-review-implementation/references/review-checklist.md`
   - Add a compact section for design-vocabulary review questions.
   - Questions must be actionable: what is the interface, what is the test surface, what seam/adapter exists, what deletion test says.

2. `skills/_shared/anti-patterns.md`
   - Add or refine an AP entry for invented seam/adapter or vocabulary-driven overengineering.
   - Make it distinct from AP-03 zero-logic wrapper.

3. `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`
   - Explain vocabulary in local terms.
   - Apply it to one existing artifact, preferably WOT-2026-009b scope_gate.
   - Contrast diagnosing-bugs with systematic-debugging and preserve 3-attempt stop.

4. `CREDITS.md`
   - Add one row for WOT-2026-010t.
   - Source should be pinned to the chosen tag/SHA and license MIT.
   - `Adapted`, not `Ported`.

## Encoding Risk

Existing review docs may contain mojibake. If the Builder touches those files, the final encoding guard must pass on the touched files. Normalize only the touched files needed for the ticket, and keep the diff reviewable.

## Gates

- Existence/read check for the protocol doc.
- `python scripts/check_encoding_guard.py <all touched markdown files>`.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` -> 0/0.
- No pytest/ruff unless code is touched, which should trigger STOP/CONTRACT_GAP.