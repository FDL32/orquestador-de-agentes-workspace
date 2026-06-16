# Work Plan: WOT-2026-010c

> Origen: 010a se publico con la suite canonica ROJA (test_no_inline_ticket_regex)
> porque el cierre cito "N passed" sin cruzar "0 failed". CI GitHub Quality Gates
> fallo en 842184a y 585fadb. 010b lo arreglo (69d53c1); 010c cierra la grieta
> de proceso que lo permitio.

## Metadata

- **ID:** WOT-2026-010c
- **Contract ID:** T-010C-001
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010b

## Objetivo

Convertir en barrera ejecutable la leccion de 010a: el handoff (`--mark-ready`)
debe exigir evidencia FRESCA y literal de que `run_pytest_safe` cerro con
`0 failed`, no solo que existe la palabra "passed" en el log. Una suite canonica
roja NUNCA debe poder pasar a READY_FOR_REVIEW.

Root cause viva (VERIFICADO en codigo 2026-06-16):
- `agent_controller.py::_check_log_has_quality_gate_evidence` (linea 1436, de
  WT-2026-203) busca markers `("pytest", "ruff", "passed", ...)` en
  execution_log.md. Buscar "passed" NO implica "0 failed": un log con
  "2801 passed, 1 failed" contiene "passed" y pasaria el check actual.
- No hay ninguna verificacion de que `run_pytest_safe` haya corrido con
  exit_code 0 fresco antes del handoff.

## Decision Arquitectonica

- **Fuente de evidencia canonica (VERIFICADO):** `run_pytest_safe.py` persiste
  `<motor>/.agent/runtime/pytest-safe/last-run.json` con campos
  `exit_code`, `status`, `finished_at`, `command` (linea 480/499/526). NO se
  parsea stdout fragil: la gate lee el JSON canonico que el runner ya garantiza.
- **Criterio doble de la gate:**
  - `status == "finished"` (no "started"/"dry-run"/crash): el run llego al final.
  - `exit_code == 0`: en pytest, exit_code != 0 significa fallo, error o "no
    tests collected"; el runner fuerza exit 1 si detecta state-leak
    (linea 512-514). status finished + exit_code 0 == 0 failed real.
- **Frescura por `tested_commit_sha` (NO por timestamp):** VERIFICADO que
  `last-run.json` hoy NO captura el commit testeado. Scope ampliado (autorizado
  por el propietario 2026-06-16) para que `run_pytest_safe.py` escriba
  `tested_commit_sha = git rev-parse HEAD` en el summary. La gate compara
  `tested_commit_sha == HEAD actual del repo de entrega`. Robusto: no depende de
  relojes ni de orden temporal. Un run de un commit anterior queda detectado por
  SHA distinto, no por timestamp. Cambio minimo: un campo en el summary, sin
  parsing de stdout ni cambio de comportamiento del runner.
- **Skip auditable por deliverable_type:** la gate SOLO aplica a `code`/`mixed`.
  Para `documentation`/`research`/`analysis` produce un skip AUDITABLE
  (`canonical_suite: skipped=true, reason=deliverable_type=<x>`), no un bloqueo.
  Respeta el dispatch por deliverable_type ya existente.
- **Punto de integracion:** la gate vive en `scripts/pre_handoff_guard.py`
  (donde ya estan las barreras de handoff de 009g/009c) y la invoca
  `agent_controller._handle_mark_ready` via `_run_pre_handoff_guard`. Asi cubre
  la puerta `--mark-ready` sin duplicar logica.
- **Fail-closed (barrera, no best-effort):** si `last-run.json` no existe, no es
  parseable, `status != finished`, `exit_code != 0`, o `tested_commit_sha !=
  HEAD`, la gate BLOQUEA con diagnostico self-service. No silenciar excepciones
  (leccion guard-helper-must-fail-closed).
- **Diagnostico self-service estructurado:** al bloquear, el dict expone
  `canonical_suite` con: `last_run_json` (ruta), `reason` (cual criterio fallo),
  `remediation` (`python scripts/run_pytest_safe.py` + commitear antes), y
  `canonical_suite_error` (mensaje human-readable). Log a revisar:
  `.agent/runtime/pytest-safe/last-run.log`.
- **NO confundir con:** scope gate (archivos fuera de FLT) ni con la barrera
  work_plan-committed de 009g. Esta es una barrera ADICIONAL y separada:
  "la suite canonica cerro en verde fresco contra el commit que se va a entregar".

## Orden de ejecucion (obligatorio)

1. Test de barrera PRIMERO (TDD): con `last-run.json` exit_code=1, la gate
   bloquea; con exit_code=0 fresco, permite. Debe FALLAR sin el fix.
2. Helper `assert_canonical_suite_green(motor_root, head_ts) -> (bool, diag)` en
   `pre_handoff_guard.py`.
3. Wire en `run_guard` (puerta `--mark-ready`).
4. Diagnostico self-service (que falto, como rerun, que log revisar).
5. Gates + cierre canonico (incluida la propia gate sobre si misma).

## Files Likely Touched

### repo_motor
- `scripts/pre_handoff_guard.py`
- `.agent/agent_controller.py`
- `scripts/run_pytest_safe.py`
- `tests/test_pre_handoff_guard.py`

Notas (no son parte del FLT parseable):
- `scripts/pre_handoff_guard.py`: helper `assert_canonical_suite_green` +
  campo `canonical_suite` en el dict de `run_guard`, fail-closed.
- `.agent/agent_controller.py`: que `_handle_mark_ready` propague el bloqueo
  (ya invoca el guard via `_run_pre_handoff_guard`; verificar que el nuevo
  campo bloquea).
- `scripts/run_pytest_safe.py`: CAMBIO MINIMO autorizado - escribir
  `tested_commit_sha = git rev-parse HEAD` en el summary. SIN parsing de stdout,
  SIN otro cambio de comportamiento del runner.
- `tests/test_pre_handoff_guard.py`: tests de barrera (ausente/corrupto/
  status!=finished/exit!=0/stale-sha/fresco-verde bloquean o permiten segun
  corresponda; doc/research/analysis skip auditable; mark-ready propaga diag).

## Read/inspect only

- `scripts/run_pytest_safe.py` (FUENTE del `last-run.json`; no reimplementar;
  VERIFICADO: escribe exit_code/status/finished_at).
- `.agent/agent_controller.py` funcion `_check_log_has_quality_gate_evidence`
  (el check debil actual; la nueva gate lo complementa, no lo sustituye).

## Manager-only

- Ejecutar `run_pytest_safe` completo leido hasta `0 failed`.
- Ejecutar `validate --json` final 0/0.

## Criterios Binarios

- [ ] `run_pytest_safe.py` escribe `tested_commit_sha = git rev-parse HEAD` en
      `last-run.json` (cambio minimo, sin tocar comportamiento del runner).
- [ ] Helper `assert_canonical_suite_green` existe en `pre_handoff_guard.py`,
      lee `last-run.json` y delega en su shape canonico (NO parsea stdout).
- [ ] `last-run.json` ausente -> BLOQUEA (fail-closed).
- [ ] `last-run.json` corrupto/no parseable -> BLOQUEA (fail-closed).
- [ ] `status != "finished"` -> BLOQUEA.
- [ ] `exit_code != 0` -> BLOQUEA.
- [ ] `tested_commit_sha != HEAD` actual (run stale) -> BLOQUEA.
- [ ] `status == finished` + `exit_code == 0` + `tested_commit_sha == HEAD` ->
      PERMITE avanzar.
- [ ] `deliverable_type` documentation/research/analysis -> skip AUDITABLE
      (`canonical_suite.skipped == true`), NO bloqueo.
- [ ] Diagnostico self-service estructurado: `last_run_json`, `reason`,
      `remediation`, `canonical_suite_error`. Log: `last-run.log`.
- [ ] Barrera verificada: test con exit_code=1 confirma bloqueo y con
      exit_code=0 fresco confirma paso. Debe FALLAR sin el helper.
- [ ] La gate NO duplica scope gate ni work_plan-committed (009g); NO sustituye
      `_check_log_has_quality_gate_evidence` (coexisten).
- [ ] `ruff check .` exit 0.
- [ ] Tests focales exit 0.
- [ ] `run_pytest_safe` completo leido hasta `0 failed`.
- [ ] `validate --json` destino 0/0 al cierre.

## Non-goals

- NO sustituir `_check_log_has_quality_gate_evidence`: la nueva gate es
  adicional (defensa en profundidad). Tocarlo seria scope creep.
- NO parsear el stdout/texto del log como fuente primaria: el JSON es canonico.
- NO crear un segundo runner ni un gate paralelo de pytest.
- NO bloquear tickets documentation/research/analysis por esta gate si su
  deliverable_type no exige pytest (respetar dispatch por deliverable_type).
- NO tocar el scope gate, la barrera work_plan-committed, ni `bus/state_machine.py`.

## Forbidden Surfaces

- `scripts/run_pytest_safe.py`: SOLO el cambio minimo autorizado
  (`tested_commit_sha`). NADA de parsing de stdout, NADA de cambio de
  comportamiento del runner, NO reimplementar su shape.
- `bus/state_machine.py`.
- `_check_log_has_quality_gate_evidence` (no sustituir; la gate coexiste).
- `privada/` y `.env`.
- Scope de 010d, 010e, 008d.
- `scripts/validate_ticket_prose.py`.
