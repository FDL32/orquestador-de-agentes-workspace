# execution_log.md -- WOT-2026-010w

## Metadata

- **Ticket:** WOT-2026-010w
**Estado:** COMPLETED
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

## Builder Fase 0 - Diagnostico + baseline (2026-06-19)

- Preflight verde: validate 0/0; STATE=010w/IN_PROGRESS; TURN=BUILDER/010w/IMPLEMENT.
- Causa raiz confirmada (sesion anterior): subprocess.run(..., text=True) sin encoding -> Windows usa cp1252 -> UnicodeDecodeError con byte alto (0x8d) abortando --session-close.
- 3 CALL SITES reales verificados (ninguno tiene encoding=):
  1. support.py:40 run_script() - subprocess.run directo, ejecuta scripts del closeout (emiten no-ASCII). ESTE es el que reviento en vivo.
  2. support.py:284 check_versioned_filenames() - subprocess_run(git ls-files), inyectado = subprocess.run real (session_closeout.py:334). Riesgo latente paths no-ASCII.
  3. rotation.py:364 step_git_clean() - subprocess_run(git status --short), inyectado = subprocess.run real (session_closeout.py:531). Riesgo latente.
- Los read_text/open del modulo ya usan encoding="utf-8" (correctos, no se tocan).
- test canonico tests/test_session_closeout.py existe (30KB) -> regresion sin suite paralela.
- Clausula legacy (Fase 0): closeout_steps/ es codigo vivo del motor, sin stubs # Legacy alias:. Los 7 stubs de prompts (launch_builder, review_manager, session_*, audit_plan, etc.) detectados en sesion previa siguen pendientes de retirada pero estan FUERA de este FLT; ya documentados como candidate-to-retire. No se tocan aqui.
- Sin desviacion de scope. Sin CONTRACT_GAP: el fix es local a los 3 call sites.

## Builder Fase 1/2 + hallazgo de scope

### Fase 1
- 3 call sites con encoding="utf-8", errors="replace": support.py:46 (run_script), support.py:291 (check_versioned_filenames git ls-files), rotation.py:369 (step_git_clean git status).
- PRUEBA EN VIVO: --session-close --dry-run --force ya NO lanza UnicodeDecodeError (antes: traceback reader-thread; ahora: completa, FAIL solo por versioned_filenames no-bloqueante).

### Fase 2
- tests/test_session_closeout.py: test_run_script_captures_high_utf8_output_without_decode_error. Ejecuta run_script REAL (no mock) contra un child que escribe UTF-8 (em dash U+2014 + comillas curvas) a su stdout buffer; verifica returncode 0 + em dash preservado.
- Nota: el child fuerza UTF-8 (sys.stdout.buffer.write(...encode utf-8)) porque el default de consola Windows es cp1252; asi se aisla el path del PADRE (run_script) que es lo que arregla 010w.
- REGRESION VERIFICADA: revertir encoding en run_script -> test FALLA; restaurado -> PASA.
- Focal: 55 passed (era 54 +1). ruff All checks passed; format clean; encoding guard EXIT 0.

### HALLAZGO DE SCOPE (no-FLT, NO commiteado en 010w)
- prompts/orchestrator_launch_builder.md aparece modificado (clausula legacy-stub + STRATEGY_WOT-{{TICKET_ID}}.md / PLAN_ legacy-compat). NO es parte de 010w (FLT = support.py, rotation.py, test_session_closeout.py). Es una edicion de plantilla independiente.
- DECISION CEM: NO incluir en el commit de 010w para no contaminar el scope del fix de encoding. Se deja dirty para que el Orquestador/humano lo commitee aparte como cambio de prompt. Registrado como hallazgo.

### Cierre de evidencia - suite
- run_pytest_safe --level all sobre 149d821: 3026 passed, 20 skipped, 0 failed (777.57s).
- last-run.json: finished, exit_code=0, tested_commit_sha=149d821 == HEAD.
- Motor dirty restante: prompts/orchestrator_launch_builder.md (cambio de plantilla del Orquestador, NO-FLT de 010w; no commiteado por el Builder).


Manager approved canonical closeout for WOT-2026-010w