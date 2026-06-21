# AUDIT_WOT-2026-013c.md

## Preguntas binarias
- El triple exacto pasa en serial.
- El triple exacto pasa junto bajo `-n 8 --dist load`.
- El diff toca solo `tests/unit/test_detect_version.py`, `tests/unit/test_project_scanner.py`, `tests/unit/test_no_inline_ticket_regex.py` y/o `tests/conftest.py`.
- Existe evidencia FAIL-sin/PASS-con del rojo real de concurrencia/estado compartido.
- No se ha tocado `scripts/run_pytest_safe.py`, CI, controller, runtime ni codigo de producto.
- `ruff`, `run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.

## Hallazgos a rechazar
- Verde solo serial, sin verde paralelo del triple.
- Fix apoyado en runner/politica xdist/default en lugar de fixtures/tests.
- Mocks o aserciones debilitadas que cambian el significado del test.
- Ampliacion de scope a otra familia sin `CONTRACT_GAP`.