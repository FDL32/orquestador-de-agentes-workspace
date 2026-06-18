# Strategy: WOT-2026-010r

## Intent

Produce one durable analysis report in `repo_motor` that lets the Manager decide whether mattpocock/skills v1.0.0 should influence local skill taxonomy and Manager review vocabulary.

## Source Handling

1. Try `gh release view mattpocock-skills@1.0.0 --repo mattpocock/skills --json tagName,name,publishedAt,body`.
2. If `gh` is unauthenticated, record the literal failure and use the public GitHub release page or API via fetch.
3. Treat release claims as external documentation until checked against local code.
4. Verify license before recommending any later adoption.

## Local Checks

Run read-only searches and record exact commands:

- consumer search for YAML/frontmatter `triggers` usage;
- search for `disable-model-invocation`;
- read `010g` inventory and compare categories;
- inspect `008c/008d` backlog entries;
- inspect candidate `010s/010t` rows if present.

## Report Shape

The report should contain:

- source baseline: tag, release commit, publish time, license evidence, source URL;
- external pieces table: piece, type, release claim, dependency/breaking note, local relevance;
- local consumer inventory: file, symbol or behavior, evidence command, risk;
- impact matrix for `008c`, `008d`, `010s`, `010t`;
- recommendation: adopt, adapt, reject, defer;
- CREDITS policy: no row in `010r`, candidate rows only for adoption tickets;
- STOP/risks for later Builder tickets.

## Evidence Rules

- Mark `VERIFICADO` only when backed by release page, local file read, grep command, or validate output.
- Mark `INFERENCIA` when interpreting relevance or future impact.
- Do not promote provisional counts from previous chats unless reproduced.

## Gates

- Existence/read check for `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`.
- `python scripts/check_encoding_guard.py docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` with 0 errors / 0 warnings.
