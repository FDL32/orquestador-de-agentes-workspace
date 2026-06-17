# Execution Log: WOT-2026-010j - Baseline de performance de suite

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010j
- **Contract ID:** T-010J-001
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Packet contractual preparado en `repo_destino`:
  - `work_plan.md`
  - `STRATEGY_WOT-2026-010j.md`
  - `AUDIT_WOT-2026-010j.md`
- Bootstrap canonico emitido en bus:
  - `STATE_CHANGED -> IN_PROGRESS` para `WOT-2026-010j`
- Proyecciones activas alineadas para arranque Builder:
  - `STATE.md` -> `WOT-2026-010j / IN_PROGRESS`
  - `TURN.md` -> `BUILDER / IMPLEMENT`

## Fase 0 - Diagnostico (seams confirmados en codigo)

- `LEVEL_CHOICES = {"unit", "integration", "all"}` en `run_pytest_safe.py:82`;
  `--level all` existe.
- `normalize_pytest_args` (`run_pytest_safe.py:409-420`): `level == "all"` no
  inyecta ningun `-m`; los otros niveles si filtran. Confirmado leyendo codigo.
- `pytest.ini:11` -> `addopts = -p no:cacheprovider`. pytest-cache deshabilitado
  por contrato, confirmado.
- `python -c "import xdist"` -> `ModuleNotFoundError: No module named 'xdist'`.
  pytest-xdist no instalado hoy, confirmado.
- Grep de `selector_focal|focal_select` en `scripts/` y `bus/` -> 0 resultados.
  Selector focal por diff no existe como flujo canonico activo, confirmado.
- Conteos auxiliares (grep `-rl` sobre `tests/*.py`):
  - `subprocess`: 53 archivos.
  - `git`/`git_init`/`GIT_DIR`: 32 archivos.
  - `tmp_path`/`tmpdir` (filesystem real): 119 archivos.
  - `agent_controller`/`bus`: 185 archivos.
  - marca `integration`: 5/2922 tests (`pytest --collect-only -m integration`).
  - marca `slow`: 1/2922 tests (`pytest --collect-only -m slow`).
- Sin desviaciones de scope detectadas en esta fase.

## Fase 1 - Medicion canonica

- Comando: `python scripts/run_pytest_safe.py --level all -- --durations=50`
  desde `repo_motor`.
- Exit code real: `0` (leido de `.agent/runtime/pytest-safe/last-run.json`,
  campo `exit_code`, no del pipe de consola que enmascararia el codigo real).
- Resultado pytest: `2902 passed, 20 skipped in 479.12s (0:07:59)`.
- Top-7 outliers de `--durations=50` suman `377.25s` de `479.12s` (~78.7% del
  tiempo en 0.24% de los tests). El test mas lento (`test_scan_current_project`,
  162.29s) y el segundo (`test_repo_has_no_live_retired_topology_terms`,
  61.99s) son escaneo de filesystem real, no subprocess/git.
- **Hipotesis subprocess/git: REFUTADA como causa dominante.** Solo
  `67.41s` (~14% del tiempo total) de los outliers son atribuibles a archivos
  con `subprocess`; el escaneo de filesystem aporta `224.28s` (~46.8%), mas
  del triple.
- Conteos auxiliares (grep sobre `tests/*.py`): `subprocess` 53 archivos,
  `git` 32 archivos, `tmp_path`/`tmpdir` 119 archivos, `agent_controller`/`bus`
  185 archivos, marca `integration` 5/2922, marca `slow` 1/2922.
- Reporte durable creado en
  `repo_motor/docs/test_performance/test_performance_baseline_WOT-2026-010j.md`.
- Existencia verificada por lectura directa (no solo confirmacion de la
  herramienta de escritura): `test -f` -> existe, 9438 bytes, contenido
  inspeccionado con `head -3`.
- Recomendacion del reporte: re-scopear `WOT-2026-010k` (su premisa de origen
  subprocess/git no es el hotspot dominante); mantener `WOT-2026-010l` y
  `WOT-2026-010m` sin cambios de prioridad.
- Sin desviaciones de scope. No se toco codigo del runner, gates ni politica
  de ejecucion.

## Quality gates

- `check_encoding_guard.py docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
  (desde `repo_motor`): exit 0.
- `validate --json --project-root <repo_destino>`: confirmado 0 errors / 0
  warnings antes del arranque de esta fase (ver turno previo del Orquestador).
  Re-ejecucion final delegada a Manager-only segun plan.

## Entrega

- Bitacora resembrada para `WOT-2026-010j` antes del arranque Builder.
- Commit motor: `c05dbfe` — "docs(WOT-2026-010j): baseline de performance de
  suite con medicion real". Archivo unico:
  `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
  (146 insertions, archivo nuevo).
- Diff motor confirmado limpio de scope creep: `git status --short` tras el
  commit solo muestra `prompts/audit_agent_output.md` modificado (pre-existente,
  fuera del FLT de `010j`, no tocado por este ticket).
