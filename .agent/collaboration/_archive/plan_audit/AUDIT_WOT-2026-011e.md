# AUDIT_WOT-2026-011e.md

## Preguntas binarias de auditoria
- `pytest-xdist` queda incorporado al entorno dev y al lockfile sin tocar CI ni el default del runner?
- El flag nuevo de `run_pytest_safe.py` es explicitamente opt-in y mantiene backward-compat cuando no se usa?
- La paralelizacion solo se habilita para subset unitario explicito y, fuera de ese contrato, cae a serial con razon auditable?
- `last-run.json` registra metadata suficiente para saber si xdist se solicito, se activo y por que se replego si no?
- Existen tests FAIL-sin/PASS-con para la ruta xdist y para el fallback seguro?
- El camino canonico (`python scripts/run_pytest_safe.py --level all`) sigue verde y `validate --json --project-root <repo_destino>` termina en 0/0?

## Hallazgos a rechazar
- Cualquier cambio que toque `scripts/pre_handoff_guard.py`, `scripts/run_gates_dispatch.py` o workflows de CI.
- Cualquier implementacion que convierta xdist en default implicito o que permita xdist sobre la suite canonica de cierre.
- Cualquier fallback que sea silencioso o que no deje razon estable en stdout/artefacto runtime.
- Cualquier medicion sin comparar el mismo subset unitario en serial y en xdist sobre el mismo host.