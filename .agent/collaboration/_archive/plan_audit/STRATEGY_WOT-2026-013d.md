# STRATEGY_WOT-2026-013d

## Objetivo
Hacer robusto el escaneo del proyecto ante borrados concurrentes en `project_scanner` y `project_paths`, manteniendo intacta la politica del runner y demostrando estabilidad xdist real sobre el triple historico.

## Fase 0 - Baseline reproducible
1. Releer los 3 sitios `rglob` verificados y los 4 tests/fixures relevantes.
2. Recapturar baseline de `tests/sandbox/test_runtime` (`session_dirs`, ruido residual, permisos anomalos si aparecen).
3. Reproducir el triple xdist sintomatico con `-n 8 --dist load` y fijar la firma exacta del rojo antes de tocar nada.

## Fase 1 - Fix de producto
1. Endurecer `scripts/project_scanner.py` en `_collect_local_modules()` y `scan_project()` para tolerar subdirectorios que desaparecen durante la travesia.
2. Endurecer `agent_system/scripts/project_paths.py` en `resolve_paths()` con la misma filosofia fail-closed/robusta.
3. Mantener intacta la semantica de producto fuera de la robustez ante borrados concurrentes.

## Fase 2 - Higiene de sandbox y barreras
1. Expresar la limpieza del sandbox via fixture/harness en `tests/conftest.py`.
2. A?adir barreras FAIL-sin/PASS-con en tests focales que distingan claramente entre ruido de sandbox y robustez de escaneo.
3. Registrar en `execution_log.md` el baseline y la reconciliacion usada.

## Fase 3 - Verificacion fuerte
1. Verificar tests focales seriales.
2. Verificar el triple xdist en 3 corridas consecutivas sobre el mismo host.
3. Ejecutar `ruff`, `ruff format --check`, `run_pytest_safe.py --level all` y `validate --json`.

## Riesgos explicitados
- El fix podria cubrir solo uno de los dos `rglob` de `project_scanner`; eso seria insuficiente.
- La limpieza del sandbox por si sola no vale como cura si el producto sigue explotando durante el escaneo.
- Si la unica salida verde exige mover el sandbox fuera del arbol o tocar runner/CI, el ticket debe parar por `CONTRACT_GAP`.
