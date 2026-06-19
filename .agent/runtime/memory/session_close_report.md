# Session Close Report

**Generated:** 2026-06-19 12:02:45 UTC
**Dry Run:** No
**Skip Slow:** Yes

## Session Window

- **Start:** from last report (2026-06-19 09:11:19 UTC)
- **End:** 2026-06-19 12:02:45 UTC

## Tickets

- WOT-2026-010w

## Steps

| # | Step | Status | Blocking | Detail |
|---|------|--------|----------|--------|
| 1 | resolve_tickets | PASS | No | Source: detected in session window. Tickets: ['WOT-2026-010w'] |
| 2 | prepush_check | PASS | Yes | All blocking quality checks passed |
| 3 | local_audit | PASS | No | Local audit snapshot captured |
| 4 | validate_ticket_prose | PASS | No | Ticket prose validated, clean |
| 5 | observations_all | SKIP | No | Skipped by --skip-slow |
| 6 | memory_consolidate | SKIP | No | Skipped by --skip-slow |
| 7 | upstream_learnings_ttl | PASS | No | No pending learnings near TTL expiry |
| 8 | cleanup_builder_session | SKIP | No | builder_session.json already absent |
| 9 | archive_collaboration | PASS | No | Collaboration artifacts archived |
| 10 | rotate_review_queue | SKIP | No | Fewer entries than KEEP_ENTRIES; nothing to archive |
| 11 | archive_manager_feedback | SKIP | No | Kept 1 file(s); No files archived |
| 12 | archive_execution_log | PASS | No | Execution log archived |
| 13 | archive_event_bus | PASS | No | Event bus terminal tickets archived |
| 14 | manifest_check | PASS | No | MANIFEST.distribute exists in repo_motor |
| 15 | portability_paths | PASS | No | No absolute workspace paths found |
| 16 | versioned_filenames | FAIL | No | Ticket IDs found in versioned filenames (10): docs/protocol/archive_rename_hygiene_WOT-2026-010u.md, docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md, docs/protocol/motor_destination_integration_WOT-2026-008f.md, docs/protocol/review_packet_hardening_WOT-2026-010i.md, docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md, docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md, docs/test_performance/test_performance_baseline_WOT-2026-010j.md, docs/test_performance/test_performance_followup_WOT-2026-010k.md, docs/test_performance/test_performance_variance_WOT-2026-010p.md, docs/test_performance/test_selection_WOT-2026-010l.md |
| 17 | git_clean | PASS | No | Tree clean (0 expected runtime file(s) dirty) |

## Overall: FAIL

## Manual Recommendations

The following checks are recommended but not automated in this pipeline:

- `code-audit` - Deep code quality analysis (run manually if significant Python changes)
- `builder-self-audit` - Self-audit of builder output (run manually for complex tickets)
