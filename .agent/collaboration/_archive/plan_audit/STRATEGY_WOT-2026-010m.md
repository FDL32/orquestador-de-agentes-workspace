# STRATEGY_WOT-2026-010m.md

## Objetivo tecnico
Consumir en CI la capacidad xdist ya creada por `011e` mediante un piloto aditivo y acotado en `quality-gates.yml`, manteniendo intacto el cierre canonico serial del runner.

## Secuencia propuesta
1. Releer `quality-gates.yml`, `run_pytest_safe.py`, la barrera local de `011e` y la evidencia de performance de `010j/010k`.
2. Identificar el punto exacto del workflow donde puede vivir un piloto xdist sin tocar la corrida canonica ni otros workflows.
3. Implementar el piloto CI con `scripts/run_pytest_safe.py` + `--xdist-workers`, manteniendo separacion explicita frente al camino serial.
4. Anadir una barrera dedicada de workflow que falle si desaparece el piloto o si la corrida canonica adopta xdist por accidente.
5. Dejar en `execution_log.md` el resultado del piloto y la justificacion de por que sigue siendo piloto y no default.
6. Cerrar con tests focales, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json`.

## Restriccion deliberada
`010m` no reabre el contrato del runner ni de handoff. Si el piloto solo puede vivir tocando `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` o convirtiendo xdist en default implicito, el ticket debe parar y devolver `CONTRACT_GAP`.