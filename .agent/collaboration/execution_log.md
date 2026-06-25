# Execution Log -- WOT-2026-013u

**Estado:** COMPLETED

## Bootstrap operativo -- WOT-2026-013u

Ticket NUEVO activado para corregir el drift entre el contrato CLI documentado y el parser real de `agent_controller.py` en acciones de closeout/review con `--ticket`.

Procedencia (VERIFICADO 2026-06-25):
- `WOT-2026-013r` ya cerro canonico en `COMPLETED` y expuso este follow-up operativo durante el cierre real.
- El packet canonico de `013u` vive en `.agent/planning/work_plan_WOT-2026-013u.md`.
- La cola viva conserva `013u` como follow-up actual de alta prioridad en la familia 013.

Bus: bootstrap pendiente via `--bootstrap-ticket` tras alinear las proyecciones vivas.

Nota para el Builder:
- El ticket NO depreca la via posicional; exige conservar compatibilidad mientras arregla `--ticket`.
- La barrera de `reopen-terminal-ticket` queda FIJADA en `tests/test_agent_controller.py`.
- `bus/**`, `runtime/**` y `scripts/run_pytest_safe.py` quedan fuera de scope.

## Fase 0 - Diagnostico (Builder, 2026-06-25, cwd=repo_motor, HEAD=8e84a25)

Seams confirmados (VERIFICADO POR BYTES + empirico):
- Help (`agent_controller.py -h`): `--manager-approve <ticket>` (l.17) y
  `--request-changes <ticket>` (l.18) muestran `<ticket>`; PERO
  `--reopen-terminal-ticket` (l.21) aparece SIN `<ticket>` aunque su parser lo
  consume (l.6030-6033).
- Condicion invertida en la rama `--ticket` (l.6020):
  `if idx + 1 >= len(sys.argv) and not sys.argv[idx + 1].startswith("--")`.
  Pide que `--ticket` sea el ULTIMO arg (fuera de rango) Y a la vez accede a ese
  indice -> contradictorio + IndexError potencial -> NUNCA asigna `ticket_id`.
  Las ramas posicionales (l.6024/6028/6032) usan la condicion CORRECTA
  (`idx + 1 < len(sys.argv)`).
- Estructura if(--ticket)/elif(posicional): correcta para precedencia; solo la
  condicion de la rama `--ticket` esta invertida.

Reproduccion empirica (dispatch CLI real, no handler):
- `--manager-approve --ticket WOT-TEST-001 ...` -> `{"error": "No ticket_id provided"}` (BUG).
- `--manager-approve WOT-TEST-001 ...` -> `{"error": "Ticket WOT-TEST-001 does not
  match active ticket WOT-2026-013u"}` (posicional SI captura el ticket; falla
  despues por no coincidir, sin tocar el bus -> seam ideal para barrera sin mutar estado).

Superficies de test versionadas confirmadas:
- `tests/test_agent_controller.py::test_agent_controller_help_lists_critical_flags`
  (usa subprocess `-h`; modelo para probar dispatch CLI real).
- `tests/unit/test_manager_approve.py` (invoca `_handle_manager_approve` directo;
  el contrato pide barrera por PARSER real, no solo handler).
- `tests/unit/test_request_changes_requeue.py`.

Desviaciones de scope: ninguna. Fix = corregir l.6020 + alinear help de
`--reopen-terminal-ticket` + barreras. bus/runtime/run_pytest_safe NO se tocan.

## Fase 1 + Fase 2 - Implementacion, barreras y gates (Builder, 2026-06-25)

Cambios en `.agent/agent_controller.py` (FLT):
- Parser de `--ticket` (antes l.6020): condicion invertida
  `idx + 1 >= len(sys.argv)` -> `idx + 1 < len(sys.argv)` (igual que las ramas
  posicionales). Comentario justificante WOT-2026-013u inline. La estructura
  if(--ticket)/elif(posicional) se conserva: `--ticket` tiene precedencia y las
  formas posicionales siguen soportadas.
- Help: `--reopen-terminal-ticket` ahora muestra `<ticket>` (consume uno); el
  control flag `--ticket` documenta que las 3 acciones aceptan AMBAS formas
  (posicional y `--ticket <id>`).

Verificacion empirica (dispatch CLI real, sin mutar bus; WOT-TEST-001 no coincide
con el activo -> falla limpio):
- `--manager-approve --ticket WOT-TEST-001` -> "does not match active ticket"
  (antes: "No ticket_id provided"). Idem `--request-changes --ticket` y
  `--reopen-terminal-ticket --ticket`. Formas posicionales: siguen capturando.

Barreras (Fase 2) en las 3 superficies versionadas (probando el PARSER real via
subprocess, no handlers internos):
- `tests/test_agent_controller.py`:
  - `test_agent_controller_help_lists_critical_flags` extendido: exige
    `--reopen-terminal-ticket <ticket>` + documentacion de ambas formas.
  - `test_ticket_parser_reads_control_flag_before_positional_fallback` (nuevo).
  - `test_reopen_terminal_ticket_accepts_ticket_flag` (nuevo) +
    `test_reopen_terminal_ticket_positional_still_supported` (nuevo).
- `tests/unit/test_manager_approve.py`: `TestManagerApproveCLIContract` con
  `test_manager_approve_accepts_ticket_flag` + `_positional_ticket_still_supported`.
- `tests/unit/test_request_changes_requeue.py`:
  `test_request_changes_accepts_ticket_flag` + `_positional_ticket_still_supported`.

Evidencia mutation-verified (DoD l.97 y l.99): reintroduje la condicion invertida
-> las 4 barreras de `--ticket` FALLARON
("'does not match active ticket' in '... No ticket_id provided ...'" AssertionError).
Restaure el fix -> 133 passed.

Gates (comandos exactos + exit):
- `pytest tests/test_agent_controller.py tests/unit/test_manager_approve.py
  tests/unit/test_request_changes_requeue.py -q` -> 133 passed (exit 0).
- `ruff check` (4 archivos) -> All checks passed. `ruff format --check` -> formatted.
- `validate --json --force --project-root <repo_destino>` -> 0 errors / 0 warnings.
- Suite canonica `run_pytest_safe --level all`: se corre al HEAD post-commit (last-run.json).

Scope: sin creep. Solo `.agent/agent_controller.py` + las 3 superficies de test del
FLT. bus/runtime/run_pytest_safe/prompts/skills NO tocados. Sin migracion a argparse.


Manager approved canonical closeout for WOT-2026-013u