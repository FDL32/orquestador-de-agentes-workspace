# Work Ticket - WT-2026-224a

## Metadata
- **ID:** WT-2026-224a
- **Title:** Supervisor relaunch guard: no spawnear round nuevo con Builder vivo
- **Scope:** system/supervisor-relaunch
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-221a, WT-2026-221b

## Problema
Tras `REVIEW_DECISION=CHANGES`, el sistema ya bloquea al Builder stale cuando
intenta `--pre-handoff` o `--mark-ready`, pero el supervisor todavia puede
relanzar un round nuevo mientras `_builder_alive()` seguiria considerando vivo
al Builder anterior.
En la sesion de `WT-2026-221b` se observo el patron completo: round N sigue
trabajando durante aproximadamente 7 minutos, supervisor dispara round N+1 y solo al cierre se
descubre el conflicto. Eso consume tiempo, contexto y ruido en el bus.

## Objetivo
Introducir una barrera minima y medible para que el supervisor suprima el
relaunch cuando `_builder_alive()` siga devolviendo `True` para el Builder del
round activo.

Resultados esperados:
1. si `_builder_alive()` devuelve `True`, `_relaunch_builder()` no abre una
   nueva ventana;
2. el bloqueo deja evidencia observable y accionable en el bus;
3. si `_builder_alive()` devuelve `False` porque falta el lock, existe un
   `BUILDER_EXIT` posterior al lock o el lock ya no esta fresco, el relaunch
   sigue funcionando;
4. existe al menos un test que reproduzca el overlap y demuestre que el relaunch
   se suprime.

## Contrato CEM v0
- Contrato antes que fix.
- Evidencia antes que relato.
- Rigor proporcional: toca supervisor y orquestacion de rounds.
- Ninguna afirmacion sin artefacto verificable.
- Si aparece cambio fuera de scope, clasificarlo y justificarlo antes de tocarlo.

## Decision Arquitectonica
- La barrera debe vivir en la ruta real de relaunch del supervisor, no en un
  wrapper documental ni en el cierre del Builder.
- El criterio minimo de supresion es binario:
  `_builder_alive()` devuelve `True` porque no existe `BUILDER_EXIT` posterior
  al `lock_started_at` y el `builder_lock.txt` sigue fresco por mtime < 15 min
  => no relanzar.
- El fix inicial debe ser local a `_relaunch_builder()` y reusar
  `_builder_alive()` como autoridad canonica de liveness, junto con el registro
  existente del resultado del relaunch.

## Decision de implementacion minima
- No redisenar el protocolo completo supervisor/Builder.
- No introducir heartbeats nuevos ni watchdogs largos.
- No tocar `WT-2026-221c` ni `WT-2026-223a`.
- Reutilizar `_builder_alive()`, `builder_lock.txt` y el round del supervisor
  antes de spawnear.

## Evidencia minima esperada
El cierre debe dejar, con artefactos verificables:
- seam real confirmado en `bus/supervisor.py`;
- prueba de que `_builder_alive()` suprime relaunch cuando el lock sigue fresco
  y no hay `BUILDER_EXIT` posterior;
- prueba de que el relaunch sigue permitido cuando `_builder_alive()` devuelve
  `False`;
- salida de tests focales;
- salida de `ruff`;
- `agent_controller.py --validate --json --project-root .` sin errores ni warnings.

## Non-goals
- No resolver todavia un heartbeat completo de Builder.
- No reescribir el claim atomico de requeue.
- No mezclar la gestion de nomenclatura de tickets.
- No mover el gate al launcher ni al controller.

## Fases
### Fase 0: Diagnostico del camino real
- Confirmar en codigo:
  - donde `_relaunch_builder()` decide lanzar;
  - como se valida hoy `builder_lock.txt`;
  - donde existe ya evidencia de `builder_lock_fresh`;
  - que funcion canonica decide hoy si el Builder sigue vivo.

### Fase 1: Barrera de relaunch
- Antes del spawn, comprobar si `_builder_alive()` sigue devolviendo `True`.
- Si la comprobacion devuelve `True`, suprimir relaunch y dejar razon
  estructurada.

### Fase 2: Pruebas
- Reproducir overlap con `builder_lock.txt` fresco y sin `BUILDER_EXIT`
  posterior.
- Verificar que el relaunch se suprime.
- Verificar camino valido cuando el lock no protege un Builder vivo.

## Files Likely Touched
- `bus/supervisor.py`
- `tests/test_relaunch_topology.py`
- `tests/test_launch_agent_terminals_script.py`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-224a.md`
- `.agent/collaboration/AUDIT_WT-2026-224a.md`
- `.agent/collaboration/execution_log.md`

## Seams confirmados
- `bus/supervisor.py:_relaunch_builder()` alrededor de L2022: punto real donde
  el supervisor incrementa round y relanza Builder.
- `bus/supervisor.py:_bootstrap_requeue_if_needed()` alrededor de L822-L939:
  ya usa `builder_lock_fresh` para no reencolar en bootstrap; sirve como
  precedente funcional.
- `bus/supervisor.py:_builder_alive()` alrededor de L1605-L1650: autoridad
  canonica de liveness; usa `BUILDER_EXIT` posterior al lock y mtime del lock,
  sin depender del PID como autoridad.
- `bus/supervisor.py:_verify_builder_start()` alrededor de L2294-L2387:
  ya verifica lock fresco tras spawn; superficie util para no duplicar criterio.
- `tests/test_relaunch_topology.py:test_relaunch_blocks_on_invalid_topology()`:
  prueba existente que entra por `_relaunch_builder()` y sirve de base para la
  nueva barrera.

## Calidad
- Ejecutar tests focales del supervisor/relaunch.
- Ejecutar al menos un test gobernante del overlap.
- Ejecutar `ruff check` sobre archivos Python modificados.
- Ejecutar `agent_controller.py --validate --json --project-root .` en el
  `repo_destino` antes de marcar ready.

## TP Check
TP-01: el diagnostico identifica el camino real de `_relaunch_builder()`.
TP-02: `_builder_alive()` devuelve `True` y suprime relaunch.
TP-03: `_builder_alive()` devuelve `False` y permite relaunch.
TP-04: el bloqueo deja razon estructurada observable.
TP-05: existe test de reproduccion del overlap.
TP-06: no hay scope creep hacia `WT-2026-221c` o `WT-2026-223a`.

## Criterio binario de salida
- `agent_controller.py --validate --json --project-root .` devuelve 0 errores y
  0 warnings.
- Existe al menos 1 test nuevo que demuestre que `_builder_alive()` suprime el
  relaunch.
- Existe al menos 1 test nuevo que demuestre el camino valido cuando
  `_builder_alive()` devuelve `False`.
- El supervisor deja evidencia verificable del bloqueo en el bus o salida
  estructurada equivalente.
