# execution_log.md -- WOT-2026-010w

## Metadata

- **Ticket:** WOT-2026-010w
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-010w`.
- Motivo: desbloquear el cierre de sesion canonico en Windows; el proyecto
  esta sano y el blocker vive en la herramienta de closeout.
- Causa raiz verificada:
  - `scripts/closeout_steps/support.py:40` (`run_script`) usa
    `subprocess.run(..., text=True)` sin `encoding`
  - `scripts/closeout_steps/support.py:287` (`check_versioned_filenames`)
    repite el patron
  - `scripts/closeout_steps/rotation.py:367` (`step_git_clean`) repite el
    patron
- Sintoma observado: `UnicodeDecodeError` cp1252 al capturar salida UTF-8
  alta de scripts del closeout o de comandos git con paths no-ASCII.
- Pendiente de Builder: fijar `encoding="utf-8", errors="replace"` en los tres
  call sites, blindar `tests/test_session_closeout.py`, demostrar que el
  `--session-close --dry-run --force` ya no revienta y cerrar con suite
  canonica + validate 0/0.

## Manager Bootstrap

- Packet materializado para `WOT-2026-010w`.
- `ticket_contracts.md`, `work_plan.md`, `STRATEGY_WOT-2026-010w.md` y
  `AUDIT_WOT-2026-010w.md` alineados al mismo scope.
- `--bootstrap-ticket WOT-2026-010w` emitio `STATE_CHANGED -> IN_PROGRESS`
  (bus seq 1370).
- `--reset-turn --force` recompuso `TURN.md` a
  `BUILDER / WOT-2026-010w / IMPLEMENT`.
- `validate --json --project-root <repo_destino>` quedo en
  `0 errors / 0 warnings` tras el bootstrap.
