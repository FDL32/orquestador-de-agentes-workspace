# AUDIT WOT-2026-003e - gates-dispatch sin tests locales

## Objetivo
Verificar que el dispatcher salta pytest SOLO cuando no hay tests locales, sin ocultar
fallos reales cuando los hay, con barrera de test.

## Reglas de revision
- Revisar el diff real de `run_gates_dispatch.py`.
- Confirmar que `has_local_tests` es deteccion estructural (filesystem), no `--collect-only`.
- Confirmar que con tests presentes el flujo es identico al anterior (rc propagado).
- Rechazar test cosmetico / floor assertion / mock drift.

## Hallazgos bloqueantes tipicos
- CRITICO: el skip ocurre tambien cuando HAY tests (oculta fallos).
- CRITICO: se traga cualquier exit code de pytest indiscriminadamente.
- ALTO: no hay barrera de test de `has_local_tests`.
- MEDIO: se modifico `run_pytest_safe.py` (fuera de scope).

## TP Check
TP-01: `has_local_tests` False sin tests/ y con tests/ vacio; True con test_*.py. (test)
TP-02: skip auditable (log explicito) solo cuando False; pytest corre cuando True. (diff)
TP-03: rc de pytest se propaga cuando hay tests (fallo real no se oculta). (diff)
TP-04: barrera de test real (no cosmetica). (test)
TP-05: ruff 0; suite motor verde; validate destino 0; commit con WOT-2026-003e. (command/git)

## Rechazo inmediato
- Skip posible con tests presentes; o exit code tragado; o sin barrera de test.
