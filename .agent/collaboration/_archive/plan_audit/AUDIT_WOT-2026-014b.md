# AUDIT_WOT-2026-014b

## Scope
- Ticket WOT-2026-014b, code, repo_motor.
- Objetivo auditado: run_pytest_safe detecta runner (pytest si esta; fallback unittest si no) + last-run.json consistente,
  sin cambiar el comportamiento para repos con pytest.

## TP Check
- TP-01: deteccion sobre el INTERPRETE DE TESTS objetivo (no el del proceso actual); fallback a python -m unittest discover.
- TP-02: repos con pytest -> comportamiento IDENTICO (test que lo fija).
- TP-03: barrera mutation-verified: pytest-ausente -> selecciona unittest + last-run.json exit 0; sin el fix FALLA por No module named pytest.
- TP-04: la clausula "declarar runner en sitio estable" es NON-GOAL (resuelto); no se impone runner unico.
- TP-05: cierre con run_pytest_safe --level all (ruta pytest del motor) + validate.

## Regression Focus
- Falso verde a evitar: un test que solo verifica la rama pytest (ya presente) sin probar el fallback unittest con pytest-ausente.
- No romper el contrato de last-run.json (campos del gate de handoff).

## Closing Rule
- No aprobar si cambia el comportamiento para repos con pytest, si rompe el contrato de last-run.json, si la barrera no
  prueba el fallback unittest mutation-verified, o sin el SHA del commit del repo_motor.
