# Work Ticket - WT-2026-225a

## Metadata
- **ID:** WT-2026-225a
- **Title:** Durable projection catch-up cuando el bus va por delante
- **Scope:** system/projection-reconcile
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-214, WT-2026-216, WT-2026-224a

## Problema
En `WT-2026-224a` vimos un fallo de autoridad/proyeccion ya catalogado como
`FP-001`: el bus quedo en un estado mas reciente que `STATE.md` y `TURN.md`.
Caso observado: el bus ya habia emitido `READY_FOR_REVIEW`, mientras el
`repo_destino` seguia en `IN_PROGRESS`. Ese drift contamina el siguiente
arranque y puede relanzar el agente equivocado o forzar reconciliaciones
manuales evitables.

## Objetivo
Implementar, en arranque o preflight, una deteccion binaria de drift donde
`last_processed_sequence < max(bus seq)` y usarla para reproyectar `STATE.md` y
`TURN.md` antes de decidir que agente lanzar.

Resultados esperados:
1. si `last_processed_sequence` queda por detras del maximo `seq` del bus, el
   sistema detecta drift antes del launch;
2. cuando el bus refleja `READY_FOR_REVIEW` y `STATE.md` sigue en
   `IN_PROGRESS`, la proyeccion se corrige antes de decidir rol/accion;
3. la reconciliacion deja evidencia verificable mediante un `STATE.md` o
   `TURN.md` actualizado y una salida estructurada o evento canonico asociado;
4. existe al menos un test que reproduzca el drift tipo `bus ahead of
   projection`.

## Contrato CEM v0
- Contrato antes que fix.
- Evidencia antes que relato.
- Rigor proporcional: toca proyecciones, launcher y autoridad de estado.
- Ninguna afirmacion sin artefacto verificable.
- Si aparece cambio fuera de scope, clasificarlo y justificarlo antes de tocarlo.

## Decision Arquitectonica
- La fuente de verdad sigue siendo el bus; `STATE.md` y `TURN.md` son
  proyecciones derivadas.
- El catch-up debe ocurrir antes de lanzar agente operativo si el drift esta
  confirmado.
- El fix inicial debe ser local y reusar el camino canonico de lectura del bus;
  no redisenar todavia el writer/proyector completo.

## Decision de implementacion minima
- No reabrir el rediseño completo del supervisor.
- No tocar `WT-2026-221c`, `WT-2026-223a` ni el protocolo de rounds.
- Reusar el estado derivado del bus y la reconciliacion/preflight existente
  antes de introducir un writer paralelo, heartbeats nuevos o locks nuevos.

## Evidencia minima esperada
El cierre debe dejar, con artefactos verificables:
- seam real confirmado donde se decide el launch y donde se conoce
  `last_processed_sequence`;
- prueba de drift reproducible con `bus=READY_FOR_REVIEW` y
  `STATE.md=IN_PROGRESS`;
- prueba de que la reconciliacion ocurre antes de lanzar el agente;
- salida de tests focales;
- salida de `ruff`;
- `agent_controller.py --validate --json --project-root .` sin errores ni
  warnings.

## Non-goals
- No resolver todavia `builder_launch_unverified`.
- No redisenar el contrato completo de `builder_lock`.
- No mezclar el registry de failure patterns con la implementacion del fix.
- No mover la autoridad fuera del bus.

## Fases
### Fase 0: Diagnostico del camino real
- Confirmar en codigo:
  - donde el launcher deriva el estado operativo;
  - donde vive `last_processed_sequence`;
  - donde se puede detectar que el bus va por delante;
  - que funcion, helper o comando canonico puede reproyectar `STATE.md` y
    `TURN.md`.

### Fase 1: Catch-up de proyeccion
- Antes del launch, comparar `last_processed_sequence` con el maximo `seq` del
  bus y confirmar si la proyeccion local quedo por detras.
- Si hay drift confirmado, reproyectar `STATE.md` y `TURN.md` desde el ultimo
  estado derivado del bus antes de decidir rol/accion.

### Fase 2: Pruebas
- Reproducir el caso `bus=READY_FOR_REVIEW` con `STATE.md=IN_PROGRESS`.
- Verificar que el catch-up ocurre antes de decidir el rol.
- Verificar que, si `last_processed_sequence >= max(bus seq)` y
  `STATE.md`/`TURN.md` ya reflejan el bus, el launch no reescribe proyecciones.

## Files Likely Touched
- `scripts/launch_agent_terminals.ps1`
- `scripts/get_launcher_state.py`
- `bus/supervisor.py`
- `tests/test_launch_agent_terminals_script.py`
- `tests/test_wt_2026_216_launcher_bus_read.py`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-225a.md`
- `.agent/collaboration/AUDIT_WT-2026-225a.md`
- `.agent/collaboration/execution_log.md`

## Seams confirmados
- `scripts/get_launcher_state.py`: helper canonico que deriva rol/accion desde
  el bus; base real para detectar drift sin confiar en `TURN.md`.
- `scripts/launch_agent_terminals.ps1:Get-ActiveRole`: ruta real de decision del
  launcher; debe consumir estado correcto antes de lanzar.
- `.agent/runtime/supervisor_state.json:last_processed_sequence`: senal local de
  cuanto del bus fue procesado/proyectado.
- `bus/supervisor.py`: writer/proyector operacional que materializa
  `STATE.md`/`TURN.md` desde transiciones del bus.
- `tests/test_wt_2026_216_launcher_bus_read.py`: base natural para el nuevo test
  de drift entre bus y proyecciones.

## Calidad
- Ejecutar tests focales del launcher, bus read o proyeccion.
- Ejecutar al menos un test nuevo que reproduzca el drift y su correccion.
- Ejecutar `ruff check` sobre archivos Python modificados.
- Ejecutar `agent_controller.py --validate --json --project-root .` en el
  `repo_destino` antes de marcar ready.

## TP Check
TP-01: el diagnostico identifica el camino real donde se decide el launch.
TP-02: existe deteccion binaria de drift cuando
`last_processed_sequence < max(bus seq)`.
TP-03: el catch-up corrige `STATE.md` y `TURN.md` desde el ultimo estado
derivado del bus antes del launch.
TP-04: el catch-up deja evidencia verificable en archivos proyectados y salida
estructurada o evento asociado.
TP-05: existe test de reproduccion del drift con `READY_FOR_REVIEW` en bus y
`IN_PROGRESS` en `STATE.md`, y el test falla sin el fix.
TP-06: no hay scope creep hacia tickets de rounds, locks o nomenclatura.

## Criterio binario de salida
- `agent_controller.py --validate --json --project-root .` devuelve 0 errores y
  0 warnings.
- Existe al menos 1 test nuevo que demuestre que el drift se detecta cuando
  `last_processed_sequence < max(bus seq)`.
- Existe al menos 1 test nuevo que demuestre que el catch-up ocurre antes de
  lanzar agente con `READY_FOR_REVIEW` en bus y `IN_PROGRESS` en `STATE.md`.
- El sistema deja evidencia verificable de la reconciliacion de proyecciones.
