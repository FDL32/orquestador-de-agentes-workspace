# AUDIT WT-2026-245a - Cerrar gaps residuales de prefijos de tres letras en bus y review bridge

## Estado
APPROVED

## Objetivo de auditoria
Verificar que el soporte a prefijos de tres letras queda cerrado en las capas residuales del bus del motor, sin reabrir cambios innecesarios en superficies ya compatibles.

## TP Check
- TP-01: verificado - la secuencia es unica: grep de entrada, fix de bus/review bridge, gates de cierre.
- TP-02: verificado - los observables son concretos: coincidencias de grep, diff en dos archivos, exit codes de gates.
- TP-03: verificado - `Files Likely Touched` enumera `bus/review_bridge.py`, `bus/supervisor.py` y el test unitario entregable.
- TP-04: verificado - el patron objetivo es explicito: `(?:WP|WT|[A-Z]{3})-\d{4}-[A-Za-z0-9]+`.
- TP-05: verificado - PLAN y AUDIT describen la misma secuencia y los mismos dos archivos.
- TP-06: verificado - el TP Check audita el plan, no sustituye los gates funcionales.
- TP-07: verificado - no se deja abierto volver a tocar launcher/controller/validate sin evidencia nueva.

## Fases de revision

### Fase 1 - Evidencia de entrada
- Verificar que existe grep o evidencia literal de patrones `WP|WT` residuales en `bus/review_bridge.py` y `bus/supervisor.py`.

### Fase 2 - Implementacion
- Verificar que el diff queda limitado a `bus/review_bridge.py`, `bus/supervisor.py` y `tests/unit/test_ticket_prefix_compat.py`, salvo ampliacion de scope justificada.
- Verificar que los cambios cubren parseo de IDs, delimitacion de bloques y numeracion relevante para prefijos de tres letras siguiendo la matriz del plan:
  - expandir parseos string en `review_bridge.py:131`, `supervisor.py:450,453`, `supervisor.py:634-637`
  - conservar `WP|WT` + `\d+` en `supervisor.py:458-459` y `supervisor.py:614` porque esas rutas alimentan `int()`

### Fase 3 - Compatibilidad backward
- Verificar evidencia de que `WP-*` y `WT-*` siguen funcionando tras el cambio.
- Verificar evidencia de que un ticket `CTL-*` ya no queda bloqueado por parseos cerrados en estas capas.
- Verificar que existe un test unitario verde que cubre `WP-*`, `WT-*` y `CTL-*`.
- Verificar que no aparece `ValueError` ni regresion equivalente por haber ampliado indebidamente un parseo numerico.

### Fase 4 - Quality gates
- Verificar exit code 0 de `ruff`, `pytest tests/unit/test_ticket_prefix_compat.py -q`, `pytest tests -q` y `validate --json --project-root`.

## Blockers
- No existe evidencia de entrada que justifique tocar `bus/review_bridge.py` o `bus/supervisor.py`.
- El diff toca archivos fuera de `Files Likely Touched` sin ampliacion de scope justificada.
- Se amplio un parseo que alimenta `int()` y el cambio introduce riesgo o evidencia de `ValueError` para tickets `CTL-*`.
- Persiste al menos un parseo string residual que limite prefijo o sufijo frente al patron canonico `(?:WP|WT|[A-Z]{3})-\d{4}-[A-Za-z0-9]+` en la superficie objetivo del ticket.
- `WP-*` o `WT-*` dejan de funcionar tras el cambio.
- No existe o falla `tests/unit/test_ticket_prefix_compat.py`.
- La suite `pytest tests -q` introduce una regresion preexistente o nueva ligada al cambio.
- Cualquiera de los gates bloqueantes falla.
