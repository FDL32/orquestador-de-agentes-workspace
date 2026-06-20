# STRATEGY_WOT-2026-011e.md

## Objetivo tecnico
Introducir un camino local, medido y opt-in de `pytest-xdist` para subset unitario explicito, preservando intacto el camino canonico de cierre (`--level all` + `args_mode=default_discovery`).

## Secuencia propuesta
1. Releer `run_pytest_safe.py`, `test_run_pytest_safe.py`, `pre_handoff_guard.py` y la linea base de performance ya medida.
2. Declarar `pytest-xdist` en dependencias dev y actualizar `uv.lock`.
3. Anadir un flag opt-in en `run_pytest_safe.py` que solo habilite xdist para subset unitario explicito.
4. Registrar metadata estable en `last-run.json` sobre solicitud, activacion, workers y motivo de fallback.
5. Construir tests de barrera para la ruta xdist y para el fallback seguro a serial.
6. Medir en este host el mismo subset unitario en serial y en xdist, y dejar ambas cifras en `execution_log.md`.
7. Cerrar con `ruff`, tests focales, `python scripts/run_pytest_safe.py --level all` y `validate --json`.

## Restriccion deliberada
`011e` no reabre CI (`010m`) ni cambia el default del runner (`011i`). Si la unica forma de ganar tiempo exige tocar `pre_handoff_guard.py`, el ticket debe parar y devolver `CONTRACT_GAP`.