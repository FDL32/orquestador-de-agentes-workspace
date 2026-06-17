# Work Plan: WOT-2026-010q

> Origen: la review de `WOT-2026-010o` detecto que el pre-handoff podia aceptar
> un `last-run.json` fresco y verde de una corrida focal como si fuese evidencia
> de suite canonica completa.

## Metadata

- **ID:** WOT-2026-010q
- **Contract ID:** T-010Q-001
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010o (cerrado)

## Objetivo

Endurecer el gate de pre-handoff para que "fresh green" signifique suite
canonica real. El handoff debe exigir que `last-run.json` corresponda a
`python scripts/run_pytest_safe.py --level all` sin argumentos explicitos de
tests, ademas de estar terminado, verde y apuntar al `HEAD` actual.

## Hechos verificados

- `010o` cerro con evidencia correcta: `last-run.json` tenia `level="all"`,
  `args_mode="default_discovery"`, `exit_code=0` y `tested_commit_sha==HEAD`.
- Antes de ese cierre, una corrida focal reciente podia cumplir
  `status/exit_code/sha` y aun asi no representar suite canonica.
- `010l` queda bloqueado por este ticket: el selector focal solo es seguro para
  iteracion Builder si el handoff rechaza evidencia focal.

## Fase 0: Diagnostico antes del cambio

Confirmar en codigo antes de editar:

- ruta exacta del guard que lee `.agent/runtime/pytest-safe/last-run.json`
- campos actuales que escribe `scripts/run_pytest_safe.py`
- comportamiento actual ante `level="unit"` con `exit_code=0` y SHA fresca
- comportamiento actual ante `level="all"` con `args_mode="explicit_args"`

Registrar en `execution_log.md`:

- funcion o modulo exacto que implementa `_check_canonical_suite_fresh_green`
- fixture/test existente que conviene extender
- resultado esperado de los dos casos barrera

## Files Likely Touched

### repo_motor
- `scripts/pre_handoff_guard.py` o el modulo real que implementa
  `_check_canonical_suite_fresh_green`
- `tests/test_pre_handoff_guard.py`
- `AGENTS.md` o `QUICKSTART.md` solo si hace falta documentar la semantica
  estricta de "suite canonica"

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010q.md`
- `.agent/collaboration/AUDIT_WOT-2026-010q.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only

- `scripts/run_pytest_safe.py`
- `.agent/agent_controller.py`
- `prompts/launch_builder.md`
- `docs/test_performance/test_performance_followup_WOT-2026-010k.md`

## Manager-only

- `validate --json --project-root <repo_destino>` final en 0/0
- verificar que el fix no cambia `run_pytest_safe.py` ni la politica del runner

## Decision Arquitectonica

- El selector focal puede existir para iteracion, pero no puede satisfacer el
  handoff canonico.
- El esquema de `last-run.json` ya contiene la informacion necesaria; `010q`
  debe consumir `level` y `args_mode`, no cambiar el schema.
- El diagnostico del bloqueo debe ser self-service: indicar el campo invalido y
  el comando de remediacion.

## Criterios Binarios

- [ ] Un `last-run.json` con `level="unit"`, `status="finished"`,
      `exit_code=0` y `tested_commit_sha==HEAD` bloquea el handoff.
- [ ] Un `last-run.json` con `level="all"` pero
      `args_mode="explicit_args"` bloquea el handoff.
- [ ] Un `last-run.json` con `level="all"`,
      `args_mode="default_discovery"`, `status="finished"`, `exit_code=0` y
      `tested_commit_sha==HEAD` permite el handoff si el resto de gates estan
      satisfechos.
- [ ] El diagnostico de bloqueo nombra una causa concreta como
      `not_full_suite` o equivalente y remedia con
      `python scripts/run_pytest_safe.py --level all` sin args explicitos.
- [ ] No cambia `scripts/run_pytest_safe.py`, no cambia politica de runner y no
      relaja ningun gate existente.
- [ ] `ruff check`, tests focales de pre-handoff y
      `validate --json --project-root <repo_destino>` terminan verdes.

## Non-goals

- NO implementar selector focal.
- NO agrupar gates ni cambiar flujo Manager.
- NO optimizar tiempos de suite.
- NO tocar cache, xdist o sharding.
- NO cambiar el schema de `last-run.json`.

## Forbidden Surfaces

- `scripts/run_pytest_safe.py`
- cache pytest
- xdist/sharding
- politica Builder/Manager
- `privada/`
- `.env`
- bus editado manualmente
