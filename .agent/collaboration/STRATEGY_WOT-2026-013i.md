# STRATEGY_WOT-2026-013i -- Higiene de purge de sandbox para latencia operacional

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `013g` ya atribuyo el coste dominante al purge de `tests/conftest.py`.
- `013d` ya fijo la necesidad de higiene del sandbox y la frontera producto-vs-harness.
- El ticket correcto no es `test_detect_version.py` ni `project_scanner.py`: el frente editable es `tests/conftest.py`.
- Cualquier "mejora" que reintroduzca residuos o requiera reabrir xdist/producto es drift de scope.

## Plan tecnico

1. Releer la ruta real del coste:
   - `tests/conftest.py`
   - `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`
   - barreras heredadas de `013d`
2. Medir before con comandos comparables en el mismo host:
   - costo focal del setup/purge
   - estado del sandbox antes/despues
3. Elegir un cambio minimo en harness:
   - reducir trabajo redundante del purge, o
   - acotar mejor el volumen purgado por sesion sin dejar residuos peligrosos
4. Cubrir la nueva semantica con barreras reales:
   - tests sobre `tests/conftest.py`
   - barreras de scanner/runtime que demuestren no-regresion
5. Cerrar con gates canonicos:
   - focales
   - triple xdist x3
   - `run_pytest_safe --level all`
   - `validate --json --project-root <repo_destino>`

## Riesgos y antidotos

- **Falso ahorro:** medir siempre en el mismo host y separar setup de call.
- **Debilitar la barrera de `013d`:** rechazar cualquier cambio que deje residuos o mueva la deuda al siguiente run.
- **Reabrir producto/xdist por inercia:** si hace falta tocar esas superficies, emitir `CONTRACT_GAP`.
- **Mock drift:** preferir evidencia con sandbox real y asserts sobre residuos/latencia observable.

## No hacer

- No tocar `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`, `tests/unit/test_detect_version.py` ni `tests/unit/test_no_inline_ticket_regex.py`.
- No cambiar el runner, `pytest.ini`, CI o la politica xdist/default.
- No declarar exito solo porque el sandbox estaba casualmente limpio al medir.
