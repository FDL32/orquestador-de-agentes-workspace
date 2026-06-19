# execution_log.md -- WOT-2026-010v

## Metadata

- **Ticket:** WOT-2026-010v
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-010v`.
- Motivo: cerrar la deuda recurrente del encoding guard que no detecta control
  chars ASCII `<32` no-whitespace y ya produjo ruido real de packaging en
  `008f` y `008j`.
- Premisa verificada: `010e` ya centralizo la deteccion en
  `scripts.encoding_guard`; este ticket endurece esa fuente de verdad, no abre
  una via paralela.
- Pendiente de Builder: confirmar seams, implementar deteccion compartida,
  blindar tests del CLI y del hook, y cerrar con suite canonica + validate 0/0.

## Manager Bootstrap

- Packet materializado para `WOT-2026-010v`.
- `--bootstrap-ticket WOT-2026-010v` emitio `STATE_CHANGED -> IN_PROGRESS`.
- `validate --json --project-root <repo_destino>` termino en `0 errors / 0 warnings`.
- `--reset-turn --force` recompuso `TURN.md` a `BUILDER / WOT-2026-010v / IMPLEMENT`.

## Builder Fase 0 - Diagnostico + baseline (2026-06-19)

- Preflight verde: validate 0/0; STATE=010v/IN_PROGRESS; TURN=BUILDER/010v/IMPLEMENT.
- Baseline tests focales: pytest test_encoding_integrity.py + test_encoding_post_write_hook.py -> 294 passed, 15 skipped.
- Seams confirmados:
  - scripts/encoding_guard.py es la fuente de verdad. file_issues(path) -> tuple (mojibake, q_in_word) [2-tuple] (L148).
  - CLI check_encoding_guard.py:70 desempaqueta "mojibake, q_in_word = file_issues(...)".
  - Hook encoding_post_write_hook.py:114 desempaqueta igual.
  - Ambos consumidores usan el MISMO file_issues -> anadir deteccion ahi la heredan los dos sin detector paralelo.
- Plan: find_control_chars(text) nuevo (bytes <32 excepto \t \n \r); file_issues pasa a 3-tuple (mojibake, q_in_word, control_chars); CLI y hook desempaquetan 3 y reportan el nuevo error. \t \n \r \r\n NO disparan.
- Clase de fallo verificada en 008f (work_plan) y 008j (execution_log): control chars <32 pasaron hasta packaging porque el guard solo mira bytes >127 (mojibake/BOM). Gap v1 Bash/heredoc sigue FUERA de scope.
- Sin desviacion de scope.

## Builder Fase 1/2 - Implementacion + Tests

### Fase 1
- encoding_guard.py: NUEVO find_control_chars(text) -> bytes <0x20 excepto \t \n \r (frozenset _ALLOWED_CONTROL_CHARS); reporta snippets <0xNN>. file_issues() pasa a 3-tuple (mojibake, q_in_word, control_chars).
- check_encoding_guard.py: desempaqueta 3, reporta "Control chars detected"; allowlist-clean considera los 3. _collect_file_errors() extraido (C901 main).
- encoding_post_write_hook.py: desempaqueta 3, ERROR control_chars + ACTION, has_error incluye control_chars. Sin detector paralelo (hereda de file_issues).
- CRLF valido (\r y \n permitidos). Bash/heredoc gap v1 FUERA de scope.

### Fase 2
- test_encoding_integrity.py: existentes a 3-tuple + assert control_chars; NUEVOS test_check_encoding_guard_explicit_path_blocks_control_chars (parametrize \x00\x07\x0b\x0c, subprocess CLI) + test_..._allows_tab_lf_cr.
- test_encoding_post_write_hook.py: import pytest; helper _write_control_chars; NUEVOS test_control_chars_detected_as_error (parametrize) + test_tab_lf_cr_pass_clean.
- REGRESION VERIFICADA: neutralice find_control_chars (if True: continue) -> 8 failed; restaurado -> 10 passed. FAIL-sin-fix / PASS-con-fix demostrado.
- Focal: 304 passed, 15 skipped (era 294 -> +10). BOM/mojibake/q-mark siguen verdes.
- Gates: ruff All checks passed; format clean; dogfood (guard sobre archivos tocados) EXIT 0; 0 control chars en los 5 archivos.
- Commit productivo: 6e55f86.
- Pendiente: suite canonica level=all contra HEAD + handoff.

### Cierre de evidencia - suite
- run_pytest_safe --level all sobre 6e55f86: 3024 passed, 20 skipped, 0 failed (784.52s).
- last-run.json: finished, exit_code=0, tested_commit_sha=6e55f86 == HEAD.
