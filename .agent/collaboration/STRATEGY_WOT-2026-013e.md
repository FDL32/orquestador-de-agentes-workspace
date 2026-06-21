# STRATEGY_WOT-2026-013e -- Inventario auditable de valor de la suite

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `010j` ya dejo una baseline durable de la suite y una lectura inicial de costes.
- `010k` ya documento follow-ups locales sobre hotspots reales; no convierte `013e` en ticket de optimizacion.
- `011e`, `010m` y `011i` ya cerraron la frontera xdist local/CI/default; `013e` no debe reabrir esa familia.
- `013d` ya cerro la deuda de producto ligada al escaneo concurrente; el ticket actual no toca producto.
- El deliverable del ticket es documental (`analysis`), no diff de codigo.

## Plan tecnico

1. Releer la evidencia previa ya durable:
   - `docs/test_performance/test_performance_baseline.md`
   - `docs/test_performance/test_performance_followup.md`
   - `docs/test_performance/test_selection.md`
2. Releer el mapa de la suite y el contrato del runner actual:
   - `tests/README.md`
   - `tests/ARCHITECTURE.md`
   - `scripts/run_pytest_safe.py`
   - `pytest.ini`
   - `.agent/runtime/pytest-safe/last-run.json`
3. Inventariar en modo read-only las familias top-level bajo `tests/` y los marcadores estructurales visibles (`slow`, `integration`, `skipif`, `xfail` o equivalentes).
4. Cruzar cada familia con evidencia disponible para clasificarla como:
   - `core regression`
   - `structural gate`
   - `legacy candidate`
   - `redundant candidate`
   - `unknown`
5. Redactar un reporte durable en `docs/test_performance/test_suite_audit_WOT-2026-013e.md` con:
   - conteos auditable por familias/subsistemas
   - evidencia verificada vs inferencia limitada
   - tests/familias lentas
   - marks/skip estructurales
   - barreras canonicas de runner/handoff
   - debt legacy detectable
   - follow-ups pequenos y verificables
6. Cerrar `execution_log.md` con la linea contractual de artefacto + validate.

## Riesgos y antidotos

- **Deriva a poda directa:** evitarla manteniendo `tests/` como `Forbidden Surface`.
- **Reabrir familia xdist/runner:** si aparece esa necesidad, detener con `CONTRACT_GAP` en vez de ensanchar el ticket.
- **Clasificacion por intuicion:** etiquetar explicitamente cualquier conclusion no corroborada como inferencia limitada.
- **Scope difuso de follow-ups:** proponer solo follow-ups pequenos con superficie acotada y criterio verificable.

## No hacer

- No editar tests, runner, CI ni producto.
- No relajar ni proponer `skip`/`xfail` como salida rapida.
- No presentar output viejo o no reconciliado con el HEAD actual como evidencia suficiente.
