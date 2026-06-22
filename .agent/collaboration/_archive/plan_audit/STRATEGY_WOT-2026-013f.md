# STRATEGY_WOT-2026-013f -- Poda segura de `tests/deprecated/`

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `tests/deprecated/` no se recolecta hoy porque `pytest.ini` lo excluye via `norecursedirs`.
- Los dos archivos del directorio estan marcados `DEPRECATED (WT-2026-254a)` y pertenecen al subsistema Goose ya retirado.
- `013e` ya acoto este follow-up como poda pequena; `test_ejemplo`, `test_goose_native_skill` y `013g` quedan fuera de scope.
- `scripts/cleanup_legacy.py` menciona el antiguo `scripts/test_goose_realworld.py`; no es un consumidor vivo del directorio `tests/deprecated/`.

## Plan tecnico

1. Reconfirmar la premisa en modo read-only:
   - `pytest.ini`
   - `tests/deprecated/test_goose_triggers.py`
   - `tests/deprecated/test_goose_realworld.py`
   - `scripts/cleanup_legacy.py`
   - `tests/integration/RETIRED_TESTS.md`
2. Capturar baseline pre-poda con `python -m pytest tests --collect-only -q -p no:cacheprovider` y registrar el 3111 en `execution_log.md`.
3. Retirar `tests/deprecated/` con un diff minimo (`git rm` acotado al directorio).
4. Anadir una entrada en `tests/integration/RETIRED_TESTS.md` que deje explicito:
   - que los tests retirados cubrian Goose
   - que Goose quedo deprecado por `WT-2026-254a`
   - que el directorio ya estaba excluido del runner, por lo que la poda no reduce la recoleccion canonica
5. Repetir el collect-only post-poda y exigir el mismo conteo (3111).
6. Ejecutar `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`.
7. Cerrar `execution_log.md` con comandos exactos, conteos pre/post y evidencia canonica final.

## Riesgos y antidotos

- **Consumidor vivo oculto:** buscar referencias primero y distinguir legacy/historico de consumidor canonico antes de borrar.
- **Deriva a runner o legacy vecinos:** mantener `pytest.ini`, `test_goose_native_skill.py` y `test_ejemplo` en `Forbidden Surfaces`.
- **Poda sin trazabilidad:** no basta con borrar; el retiro debe quedar en `tests/integration/RETIRED_TESTS.md`.
- **Suite verde pero cierre no reconciliado:** la evidencia final debe usar `run_pytest_safe.py --level all` reconciliado con el HEAD entregado.

## No hacer

- No tocar `pytest.ini`, `scripts/run_pytest_safe.py` ni producto vivo.
- No convertir el ticket en limpieza general de Goose o legacy.
- No usar output historico de `013e` como sustituto del collect-only y suite de esta ronda.
