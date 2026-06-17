# STRATEGY_WOT-2026-010j -- Baseline de performance de suite

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `scripts/run_pytest_safe.py` acepta `--level all` y argumentos extra para
  pytest.
- `level=all` no anade filtro `-m`; por tanto `--durations=50` observa la
  suite completa del runner seguro.
- `pytest-cache` sigue deshabilitado por contrato.
- `pytest-xdist` no esta instalado hoy; no se usa en este ticket.
- La hipotesis `subprocess`/`git` viene de inspeccion/grep y debe tratarse como
  inferencia hasta que el reporte la confirme o la refute.

## Plan tecnico

1. Medir la suite completa con el runner seguro:
   `python scripts/run_pytest_safe.py --level all -- --durations=50`
2. Extraer del output:
   - tiempo total,
   - top 50 tests lentos,
   - top modulos lentos si se pueden agrupar desde el output,
   - anomalías de entorno o de runner.
3. Complementar con conteos verificables por codigo:
   - archivos/tests que referencian `subprocess`,
   - archivos/tests que referencian `git`,
   - tests con filesystem real,
   - tests que tocan controller/bus,
   - marcas `integration` y `slow`.
4. Redactar un reporte durable en `repo_motor/docs/test_performance/`.
5. Cerrar el reporte con una recomendacion concreta del siguiente ticket:
   `010k`, `010l`, `010m` o re-scope si la premisa cae.

## Riesgos y antidotos

- **Falso verde por medir solo unit:** evitarlo usando `--level all`.
- **Cristalizacion de hipotesis:** si `subprocess`/`git` no emerge como cuello,
  decirlo explicitamente y no empujar `010k`.
- **Artefacto no durable:** el reporte va en `repo_motor`, no en memoria del
  destino.
- **Existencia vs encoding:** verificar lectura real del reporte y luego
  encoding; no confundir ambas pruebas.

## Salida esperada del reporte

- Resumen ejecutivo del tiempo total.
- Tabla o lista de top tests lentos.
- Top modulos/familias lentas.
- Conteos auxiliares (`subprocess`, `git`, filesystem, controller/bus,
  `integration`, `slow`) con su etiqueta: VERIFICADO o INFERENCIA.
- Recomendacion del siguiente ticket ejecutable y por que.

## No hacer

- No tocar runner, gates, CI o politica de cierre.
- No proponer optimizacion irreversible sin dato.
- No esconder si la medicion no fue viable; en ese caso, abrir `CONTRACT_GAP`.
