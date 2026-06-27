# Execution Log -- WOT-2026-014a

**Estado:** IN_PROGRESS

## Preparacion
- Packet canonico de WOT-2026-014a en work_plan.md + rubrica en AUDIT_WOT-2026-014a.md.
- Opcion A congelada: allowlist compartida de artefactos runtime esperados + parametro opt-in en
  check_git_tree_clean; default sin cambios; el closeout pasa la allowlist; B y C descartadas.

## Handoff al Builder
- FLT: scripts/delivery_hygiene_check.py, scripts/closeout_steps/rotation.py, scripts/prepush_check.py,
  tests/unit/test_closeout_self_dirty_allowlist.py.
- Barrera: reporte esperado sin commitear FALLA sin el fix; con allowlist del cierre se perdona; cambio
  PRODUCTIVO sin commitear SIGUE marcando sucio.
- Restriccion: NO debilitar el default de check_git_tree_clean (pre-push general); NO Opcion B ni C.

## Siguiente paso canonico
- validate; bootstrap-ticket; reset-turn; lanzar Builder.

## Builder Evidence - WOT-2026-014a (commit fe8ac4b)

**Timestamp:** 2026-06-27

### Commit
- SHA: fe8ac4b979f802b5e4e1202def1812fe533cea25
- Message: fix(closeout): WOT-2026-014a opt-in runtime-artifact allowlist threaded through closeout prepush
- Files changed: 5 (delivery_hygiene_check.py, rotation.py, prepush_check.py, gates.py, test_closeout_self_dirty_allowlist.py)

### 4-case barrier (check_git_tree_clean) - all PASS
(a) expected report + NO allowlist -> FAILS: test_case_a_expected_report_no_allowlist_fails PASSED
(b) expected report + closeout allowlist -> forgiven: test_case_b_expected_report_with_allowlist_passes PASSED
(c) productive file + closeout allowlist -> STILL FAILS: test_case_c_productive_file_with_allowlist_still_fails PASSED
(d) default (no allowlist) behavior preserved: test_case_d_clean_tree_passes_with_no_allowlist PASSED, test_case_d_dirty_tree_fails_with_no_allowlist PASSED

### gates.py integration behavioral mutation test
- Test: test_case_e_gates_step_prepush_passes_closeout_mode_behavioral
- Approach: monkeypatches run_script_fn to capture actual command list at runtime
- FAIL-WITHOUT-FIX (mutation: removed --closeout-mode from command list, comment intact):
  AssertionError: INTEGRATION GAP: step_prepush_check does not pass --closeout-mode to prepush_check.py.
  Actual args: [--project-root, ...]
- PASS-WITH-FIX (restored): PASSED

### Gates
- Focal pytest: 9 passed in 1.35s
- ruff check: All checks passed
- ruff format --check: 5 files already formatted
- validate: 0 errors / 0 warnings

### Canonical suite
- run_pytest_safe.py --level all: exit_code=0, level=all
- 3252 passed, 20 skipped in 112.33s
- tested_commit_sha: fe8ac4b979f802b5e4e1202def1812fe533cea25 == HEAD

### Motor state
- git status --porcelain: (clean)
- No CRLF in any committed file
- No sandbox artifacts committed
