# PLAN WOT-2026-003e - gates-dispatch sin tests locales

## Pasos
1. `scripts/run_gates_dispatch.py`: añadir `def has_local_tests(project_root: Path) -> bool`
   que devuelve True si `project_root/"tests"` existe y contiene al menos un archivo que
   matchee `test_*.py` o `*_test.py` (rglob), False en caso contrario.
2. En `run_code_gates()`, reemplazar el bloque pytest-safe por:
   - si `has_local_tests(PROJECT_ROOT)`: correr `run_pytest_safe.py` (logica actual,
     propagar rc != 0);
   - si no: `print("[dispatch] No local tests under <root>/tests; skipping pytest-safe "
     "(destino sin tests locales). CI uses validate-state.")` y continuar (no fallar).
3. Test en `tests/unit/test_run_gates_dispatch.py`: `has_local_tests` False (sin dir / dir
   vacio) y True (con `tests/test_x.py`). Usa tmp_path.

## Seams / invariantes
- El skip es imposible si hay tests locales (deteccion estructural por filesystem).
- `run_pytest_safe` no se modifica; su exit code se respeta cuando hay tests.

## Evidencia esperada
- Diff del dispatcher; test de `has_local_tests` verde; ruff 0; suite motor verde.

## STOP
- Ver work_plan. No acoplar a `pytest --collect-only`; no ocultar fallos reales.
