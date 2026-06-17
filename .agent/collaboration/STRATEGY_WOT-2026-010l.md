# STRATEGY_WOT-2026-010l -- Selector focal por diff

## Hechos verificados

- `run_pytest_safe.py` ya soporta args explicitos y deja rastro de
  `args_mode` en `last-run.json`.
- `010q` ya impide cerrar handoff con una corrida focal; eso permite que `010l`
  optimice iteracion local sin tocar la politica de cierre.
- `010i` ya endurecio commit-visible y Forbidden Surfaces; el diff de `010l`
  debe quedarse en runner + tests + nota documental.

## Plan tecnico

1. Confirmar el seam exacto para diff real y reusar el existente.
2. Implementar o conectar un resolvedor archivo->tests conservador y auditable.
3. Tratar como `structural fallback` los cambios en `pyproject.toml`,
   `pytest.ini`, `.agent/**` y cualquier resolucion vacia/insegura.
4. Integrar el selector en `run_pytest_safe.py` sin romper los modos actuales.
5. Anadir tests de barrera para diff fallido, archivo troncal, resolucion vacia
   y caso seguro con subset reproducible.
6. Documentar en un reporte breve como invocar el selector y como detectar
   cuando replega a la suite canonica.

## Riesgos

- **Parser paralelo:** reimplementar `git diff` fuera de seams existentes.
- **Falso verde:** permitir subset cuando el cambio es estructural.
- **Scope creep:** tocar dispatch, CI, cache o `last-run.json`.
- **Heuristica opaca:** mapa archivo->tests dificil de auditar.

## No hacer

- No tocar `pre_handoff_guard.py` para debilitar `010q`.
- No meter xdist, cache ni sharding.
- No depender de SaaS o herramientas externas.
- No presentar un selector focal como evidencia suficiente de closeout.
