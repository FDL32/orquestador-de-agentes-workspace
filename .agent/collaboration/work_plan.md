# Work Plan: WOT-2026-010p

> Origen: durante `WOT-2026-010o` se confundio tiempo real de pytest con espera
> operativa del agente en modo background. El objetivo es medir y documentar,
> no alterar tiempos de suite ni cambiar gates.

## Metadata

- **ID:** WOT-2026-010p
- **Contract ID:** T-010P-001
- **Estado:** APPROVED
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010o, WOT-2026-010q (cerrados)

## Objetivo

Ejecutar exactamente una corrida de
`python scripts/run_pytest_safe.py --level all -- --durations=50` y registrar:
comando, wall-clock total en minutos y segundos, `exit_code`,
`tested_commit_sha`, `level`, `args_mode` y top durations. Si esa primera
corrida termina en menos de 10 minutos wall-clock, ejecutar una segunda corrida
del mismo comando y registrar el delta absoluto y porcentual entre ambas; si
termina en 10 minutos o mas, registrar el STOP literal
`segunda_corrida_omitida_por_coste`. Escribir el resultado en
`docs/test_performance/test_performance_variance_WOT-2026-010p.md` y anadir a
`INTERACTION_MODES.md` esta regla literal: suites con duracion esperada menor
de 10 minutos van en foreground; background solo se usa con progreso
verificable. El ticket no cambia codigo de runner, gates, cache, xdist ni
selector focal.

## Hechos verificados

- `010o` produjo una observacion falsa de `~43min` por espera/polling de modo
  background, mientras la corrida directa real fue de minutos.
- `010q` ya blindo el handoff para exigir `level=all` y
  `args_mode=default_discovery`.
- El siguiente cambio de politica (`010l`) debe esperar a un reporte que
  incluya una categoria literal final entre: `entorno/I-O`,
  `test inestable`, `nuevo hotspot verificable`, `no concluyente`, mas el
  wall-clock observado y el delta entre corridas cuando exista segunda corrida.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de escribir el reporte:

- ubicacion y formato de `docs/test_performance/`
- evidencia disponible de `010j`, `010k`, `010o` y `010q`
- comando exacto para capturar `--durations=50` mediante `run_pytest_safe`
- superficie canonica donde documentar regla foreground/background

Registrar en `execution_log.md`:

- si se ejecutan una o dos corridas
- tiempo wall-clock, `exit_code`, `tested_commit_sha`, `level`, `args_mode`
- decision binaria sobre segunda corrida:
  ejecutar segunda corrida solo si la primera termina en menos de 10 minutos
  wall-clock; si tarda 10 minutos o mas, registrar STOP con motivo
  `segunda_corrida_omitida_por_coste`

## Files Likely Touched

### repo_motor
- `docs/test_performance/test_performance_variance_WOT-2026-010p.md`
- `INTERACTION_MODES.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010p.md`
- `.agent/collaboration/AUDIT_WOT-2026-010p.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only

- `scripts/run_pytest_safe.py`
- `pytest.ini`
- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
- `docs/test_performance/test_performance_followup_WOT-2026-010k.md`
- `.agent/runtime/pytest-safe/last-run.json`

## Manager-only

- `validate --json --project-root <repo_destino>` final en 0/0
- revisar que el reporte no propone cambios de politica sin ticket nuevo

## Decision Arquitectonica

- `010p` es analysis/documentation: no optimiza tests.
- Foreground/background es disciplina operativa, no un nuevo flag.
- Si las mediciones no son concluyentes, el resultado correcto es decir
  `no concluyente` y abrir follow-up focal, no inventar una optimizacion.

## Criterios Binarios

- [ ] Existe `docs/test_performance/test_performance_variance_WOT-2026-010p.md`.
- [ ] El reporte registra al menos una corrida `run_pytest_safe --level all`
      con `--durations=50`, o documenta STOP si no puede completarse.
- [ ] Si hay dos corridas, compara top outliers; si hay una, registra de forma
      literal si la segunda se omitio por `segunda_corrida_omitida_por_coste`
      (primera corrida >=10 min) o por otro STOP concreto nombrado.
- [ ] Cada corrida registrada incluye wall-clock, `exit_code`,
      `tested_commit_sha`, `level` y `args_mode`.
- [ ] Documenta la regla foreground/background en `INTERACTION_MODES.md`:
      suites esperadas <10 min en foreground; background solo con polling o
      progreso verificable.
- [ ] Clasifica la conclusion como `entorno/I-O`, `test inestable`,
      `nuevo hotspot verificable` o `no concluyente`.
- [ ] No toca `scripts/run_pytest_safe.py`, `run_gates_dispatch.py`, cache,
      xdist, sharding ni politica de cierre.
- [ ] `validate --json --project-root <repo_destino>` termina 0/0.

## Non-goals

- NO alterar tiempos de tests.
- NO activar cache, xdist, sharding ni selector focal.
- NO modificar `scripts/run_pytest_safe.py`.
- NO bloquear retroactivamente `010o` o `010q`.

## Forbidden Surfaces

- `scripts/run_pytest_safe.py`
- `scripts/run_gates_dispatch.py`
- cache pytest
- xdist/sharding
- politica Builder/Manager
- bus editado manualmente
