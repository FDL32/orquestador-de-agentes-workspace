# STRATEGY_WOT-2026-013o

## Objetivo tecnico
Dejar `observations.jsonl` del `repo_destino` en `--strict` verde saneando primero la base corrupta y cerrando explicitamente la decision de contrato sobre dominios, sin promover memoria portable nueva durante esta ronda.

## Riesgos a evitar
- falso verde: dejar `validate_observations.py --strict` pasando por fallback silencioso o por reinterpretacion no verificable
- medio fix: reparar solo el archivo del destino sin alinear migrador, validador, schema y barreras
- overreach: abrir una reforma amplia de taxonomia, tocar `bus/memory_loader.py` o memoria portable del motor
- contaminacion semantica: insertar la observacion diferida de `013n` antes de tener una base `--strict` verde
- handoff surprise: tocar superficies fuera de FLT y exponer ruido evitable en `--pre-handoff`

## Fase 0 - Relectura adversarial
1. Reejecutar `validate_observations.py --strict` sobre el archivo real y conservar el conteo literal de 17 errores.
2. Separar con evidencia las 14 lineas de corrupcion de datos de las 3 lineas de posible decision de contrato (`collaboration`, `test-performance`).
3. Releer `scripts/migrate_observations.py`, `scripts/validate_observations.py`, `skills/_shared/ap-schema.md`, `bus/memory_loader.py`, `scripts/memory_consolidate.py`, `tests/test_migration_bootstrap.py` y `tests/unit/test_validate_observations.py` para fijar seams y barreras reales.
4. Si alguna linea exige reinterpretacion semantica no verificable o tocar consumidores fuera de scope, parar por `CONTRACT_GAP`.

## Fase 1 - Reparacion minima con autoridad
1. Corregir de forma determinista el patron `applies_to <- domain` reutilizando el migrador existente en vez de bypass manual.
2. Resolver los 3 `domain` fuera de enum por decision explicita de contrato: mapear con justificacion verificable o ampliar enum/schema/validador/tests de manera acotada.
3. Mantener backup, rollback e idempotencia del migrador.
4. Mantener fuera de scope cualquier promotion de memoria portable nueva.

## Fase 2 - Barreras
1. Extender `tests/test_migration_bootstrap.py` y `tests/unit/test_validate_observations.py` sin crear suites paralelas.
2. Exigir al menos un FAIL-sin/PASS-con para el patron `applies_to <- domain`.
3. Verificar explicitamente que la decision sobre `domain` no cae en fallback silencioso.

## Gates objetivo
- `python scripts/validate_observations.py --strict --file <repo_destino>/.agent/runtime/memory/observations.jsonl`
- `python -m pytest tests/test_migration_bootstrap.py tests/unit/test_validate_observations.py -q -p no:cacheprovider`
- `python scripts/run_pytest_safe.py --level all`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Cierre esperado
El Builder entrega diff productivo del motor, base saneada del destino y evidencia explicita de que `013o` no promueve memoria portable nueva; la observacion diferida de `013n` queda fuera de scope hasta una ronda posterior sobre base `--strict` verde.
