# Work Plan: WOT-2026-010j

> Origen: la suite canonica del motor tiene una latencia suficiente para
> degradar el feedback del ciclo Builder/Manager y hoy no existe una baseline
> reproducible con tiempo total, top-50 por `--durations`, distribucion por
> familias y contraste entre `subprocess`/`git` y otros grupos reales de coste.
> Antes de cambiar gates, selector focal o paralelizacion, toca medir y dejar
> un artefacto durable.

## Metadata

- **ID:** WOT-2026-010j
- **Contract ID:** T-010J-001
- **Estado:** READY_TO_START
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010c (cerrado/COMPLETED)

## Pre-launch note

- `STATE.md` y `TURN.md` siguen reflejando el cierre de `010f`; este packet no
  arranca el bus ni cambia el ticket activo. El bootstrap canonico ocurre al
  iniciar la sesion formal del Builder.
- La hipotesis `subprocess`/`git` es **INFERENCIA** previa al ticket. `010j`
  debe confirmarla o refutarla con medicion, no repetirla como hecho.

## Objetivo

Producir una baseline durable y reproducible de performance de la suite del
motor para elegir entre `010k`, `010l`, `010m` o re-scope segun dos criterios
medidos: mayor porcentaje del tiempo total atribuible al hotspot dominante y
mayor riesgo de falso-verde o deriva contractual si ese hotspot no se aborda.
La baseline debe capturar como minimo: tiempo total de ejecucion, top-50 tests
mas lentos, agrupacion por modulos/familias y conteos auxiliares de
`subprocess`, `git`, filesystem real, controller/bus, `integration` y `slow`.
El deliverable es analitico: un reporte en `repo_motor` y un packet trazable,
sin tocar la politica de ejecucion todavia.

Frase guia: "Medir primero, decidir despues con metrica; si la premisa cambia,
cambia el siguiente ticket."

## Metricas de salida exigidas

- **Tiempo total:** duracion wall-clock de `python scripts/run_pytest_safe.py --level all -- --durations=50`.
- **Ranking lento:** lista top-50 emitida por pytest `--durations=50`.
- **Agrupacion por familias:** resumen por modulo o archivo de test cuando el
  output permita agruparlos sin inferencia fuerte.
- **Conteos auxiliares:** numero de archivos o tests que referencian
  `subprocess`, `git`, filesystem real, controller/bus, `integration`, `slow`.
- **Decision del siguiente ticket:** recomendacion priorizada (`010k`, `010l`,
  `010m` o re-scope) basada en los datos anteriores y no en intuicion.

## Hechos verificados (no asumir)

- `scripts/run_pytest_safe.py` ya acepta `--level all` y argumentos extra para
  pytest; con `level=all` no anade filtro `-m`.
- `pytest-cache` sigue deshabilitado por contrato (`pytest.ini` + runner).
- `integration` y `slow` son una porcion pequena de la suite; excluirlas no
  cambia sustancialmente el coste total.
- `pytest-xdist` no esta instalado hoy; no se introduce en este ticket.
- `run_pytest_safe.py` ya acepta subsets manuales, pero el selector por diff
  aun no existe.

## Decision de alcance

- **Analisis durable, no runtime:** el reporte vive en
  `repo_motor/docs/test_performance/` para que sea comparable y versionable.
- **Medicion canonica completa:** usar `python scripts/run_pytest_safe.py --level all -- --durations=50`.
- **Separar hechos de inferencias:** cualquier conclusion sobre `subprocess`,
  `git`, import-time, fixtures de controller o estado compartido debe venir del
  reporte, no del relato previo.
- **Sin cambios de politica:** este ticket no activa cache, xdist, selector
  focal ni modificaciones de gates.

## Orden de ejecucion (obligatorio)

1. Verificar estado previo: `validate --json --project-root <repo_destino>`
   antes de medir; registrar si aparecen `ticket_prose`, `bus_drift` o
   `invariants` previos al arranque.
2. Ejecutar la medicion canonica con `--level all -- --durations=50`.
3. Complementar la medicion con seis conteos verificables:
   `subprocess`, `git`, filesystem real, controller/bus, `integration`, `slow`.
4. Redactar el reporte durable en `repo_motor/docs/test_performance/`.
5. Verificar existencia real del reporte y encoding limpio.
6. Recomendar el siguiente ticket ejecutable con evidencia, explicando:
   hipotesis evaluada, metrica observada, criterio de prioridad medido
   (`%` del tiempo total atribuible al hotspot y/o riesgo de falso-verde
   evitado) y ticket descartado si aplica.

## Files Likely Touched

### repo_motor
- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`

### repo_destino
- `.agent/collaboration/work_plan.md`

Notas (no forman parte del FLT parseable):
- Los scripts y tests inspeccionados (`scripts/run_pytest_safe.py`,
  `scripts/run_gates_dispatch.py`, `pytest.ini`, `pyproject.toml`, `tests/`,
  `.agent/agent_controller.py`) son **read/inspect only**.
- Si el Builder detecta que necesita tocar codigo del motor para poder medir,
  debe emitir `CONTRACT_GAP`; eso queda fuera de `010j`.

## Read/inspect only

- `scripts/run_pytest_safe.py`
- `scripts/run_gates_dispatch.py`
- `pytest.ini`
- `pyproject.toml`
- `tests/`
- `.agent/agent_controller.py`
- `.agent/runtime/pytest-safe/`

## Manager-only

- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  final 0/0.
- Verificar existencia real del reporte durable en `repo_motor`.
- Verificar que el diff productivo del motor se limita al artefacto documental
  del ticket.

## Expected Evidence

- Comando de medicion exacto:
  `python scripts/run_pytest_safe.py --level all -- --durations=50`
- Reporte con:
  - tiempo total,
  - top tests lentos,
  - top modulos lentos,
  - peso relativo de `subprocess`/`git`,
  - conteos de tests/archivos por categoria relevante,
  - recomendacion del siguiente ticket ejecutable con metrica, razon y orden.
- Verificacion de existencia real del reporte por lectura o check compatible con
  el entorno, mas verificacion separada de encoding. El encoding guard no
  sustituye la prueba de existencia.

## Decision Arquitectonica

- Este ticket produce un artefacto `analysis` en `repo_motor` porque la baseline
  debe ser durable, comparable entre sesiones y reutilizable por `010k`, `010l`
  y `010m`.
- La medicion se hace con `run_pytest_safe.py --level all` para conservar el
  contrato real del runner seguro. Medir con subsets, cache o paralelizacion
  cambiaria la pregunta del ticket.
- El packet no arranca el bus: la preparacion contractual ocurre antes del
  bootstrap formal del Builder. Por eso `bus_drift` e `invariants` previos al
  ticket se documentan como esperables hasta que el supervisor abra `010j`.

## Criterios Binarios

- [ ] Se ejecuto `python scripts/run_pytest_safe.py --level all -- --durations=50`
      o existe evidencia verificable de por que no fue viable.
- [ ] Existe `repo_motor/docs/test_performance/test_performance_baseline_WOT-2026-010j.md`.
- [ ] El reporte incluye tiempo total, top tests lentos, top modulos lentos y
      peso relativo de `subprocess`/`git`.
- [ ] El reporte distingue hechos verificados de inferencias y confirma o
      refuta la hipotesis `subprocess`/`git`.
- [ ] El reporte cuenta archivos/tests con `subprocess`, `git`, filesystem real,
      controller/bus y marcas `integration`/`slow`.
- [ ] El reporte recomienda el siguiente ticket ejecutable con evidencia, no
      por intuicion.
- [ ] `check_encoding_guard.py` pasa sobre el reporte y los artefactos de packet
      tocados.
- [ ] `validate --json --project-root <repo_destino>` exit 0, 0 errors, 0 warnings.

## Non-goals

- NO modificar `run_pytest_safe.py`, `run_gates_dispatch.py`, `pytest.ini`,
  `pyproject.toml` ni la politica Builder/Manager.
- NO activar cache, xdist, sharding ni selector focal.
- NO tocar tests productivos salvo que la medicion documental lo exija y el
  contrato se rehaga.
- NO tratar la hipotesis `subprocess`/`git` como conclusion previa.

## Forbidden Surfaces

- `scripts/run_pytest_safe.py`
- `scripts/run_gates_dispatch.py`
- `pytest.ini`
- `pyproject.toml`
- `uv.lock`
- cualquier modulo Python productivo del motor
- `privada/` y `.env`
- bus editado manualmente
