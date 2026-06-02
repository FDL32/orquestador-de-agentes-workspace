# Work Ticket - WT-2026-214

## Metadata
- **ID:** WT-2026-214
- **Title:** Protocolo de forced close en preflight para ticket anterior y runtime stale
- **Scope:** system/preflight-reconcile
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** MANAGER
- **Depende de:** WT-2026-210, WT-2026-216

## Problema
Hoy el launcher ya lee el bus como autoridad primaria para decidir qué agente lanzar, pero el preflight todavía no distingue formalmente entre dos clases de recuperación:

1. limpiar runtime local stale del ticket anterior;
2. reconciliar historia en el bus emitiendo cierre canónico del ticket anterior.

Ese hueco fue la raíz operativa del drift que explotó en `WT-2026-205`: se podía abrir un ticket nuevo con `work_plan.md` y `STATE.md` avanzados mientras `supervisor_state.json`, `manager_bridge_state.json`, `builder_lock.txt` y el bus seguían anclados al ticket anterior.

El riesgo ahora es integrar `reconcile_ticket.py` “a pelo” en el launcher y volver a mezclar operaciones locales reversibles con cierres históricos irreversibles en el bus.

## Decision Arquitectonica
- El bus sigue siendo la fuente canónica para decidir si un ticket previo está terminal o no.
- El preflight debe separar explícitamente:
  - limpieza local de runtime stale;
  - reconciliación canónica en el bus.
- `reconcile_ticket.py` se invoca solo cuando el ticket previo no es terminal y el drift está confirmado.
- Si el ticket previo ya está terminal en el bus, el launcher limpia artefactos locales pero no emite eventos nuevos.
- Si el bus es ilegible, ambiguo o contradictorio, el preflight aborta sin cerrar nada.
- La decisión debe apoyarse en la derivación canónica del bus, no en heurísticas sobre `TURN.md`.

## Non-goals
- No rediseñar `reconcile_ticket.py` completo ni convertirlo en daemon.
- No tocar todavía la terminalidad profunda de `StateMachine.derive_state_from_events()`; eso queda para ticket de especificación/hardening posterior.
- No resolver aquí la duplicación del mapping `TicketState -> (role, action)`.
- No reabrir la deuda del doble `STATE_CHANGED` de `--mark-ready`; eso sigue siendo `WT-2026-213`.
- No cambiar la UX general del launcher más allá del preflight y sus mensajes/abortos.

## Fases
### Fase 0: Contrato de decisión
- Fijar los tres casos del preflight:
  - ticket previo terminal en bus + runtime stale -> limpiar local, no reconciliar;
  - ticket previo no terminal + drift claro -> reconciliar en bus;
  - bus ilegible o señales contradictorias -> abortar.
- Definir qué señales mínimas componen “drift claro” y cuáles son “contradictorias”.

### Fase 1: Inventario del preflight actual
- Mapear `Repair-StartupBridgeState`, `Repair-StartupSupervisorState`, `Assert-StartupAlignment` y `Remove-StaleRuntimeArtifacts`.
- Confirmar dónde se detecta hoy `SupervisorLastTicketId` / `BridgeLastTicketId` distinto de `WorkPlanId`.
- Identificar el mejor punto para decidir entre cleanup local y `reconcile_ticket.py`.

### Fase 2: Implementación mínima
- Añadir una decisión de reconciliación previa a la limpieza destructiva del runtime.
- Reutilizar el estado derivado del bus para saber si el ticket previo está terminal.
- Invocar `scripts/reconcile_ticket.py` con `--ticket` y `--reason` solo en el caso no terminal.
- Mantener el cleanup local actual para el caso terminal.

### Fase 3: Verificación
- Probar drift con ticket previo terminal -> no se emiten eventos nuevos, solo limpieza local.
- Probar drift con ticket previo no terminal -> se invoca reconciliación canónica.
- Probar bus ilegible o estado no determinable -> aborta preflight sin cerrar nada.
- Verificar que el caso sano no cambia.

### Fase 4: Deuda remanente
- Documentar si la integración automática deja huecos para terminalidad profunda del bus.
- Separar cualquier follow-up de limpieza o refactor del launcher/reconciler.

## Files / surfaces likely touched
Esta lista es informativa y no un scope gate; el ticket se valida por el contrato de reconciliación del preflight.

### Writable deliverables
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-214.md`
- `.agent/collaboration/AUDIT_WT-2026-214.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

### Code / tests expected
- `scripts/launch_agent_terminals.ps1`
- `scripts/reconcile_ticket.py` (solo si hace falta exponer una interfaz más clara)
- `scripts/get_launcher_state.py` (solo si hace falta helper adicional de estado)
- `tests/test_launch_agent_terminals_script.py` (existente; no-regresión)
- `tests/test_reconcile_ticket.py` (existente; ampliar si procede)
- `tests/test_wt_2026_214_preflight_reconcile.py`

## Calidad
- No contradecir `backlog.md`, `STATE.md`, `TURN.md` ni la memoria recién consolidada sobre `cleanup-vs-bus-reconcile`.
- Registrar comandos y resultados si se ejecutan cambios o tests.
- Mantener separación explícita entre cleanup local y reconciliación histórica.
- No introducir una heurística que cierre tickets si el bus no puede leerse con confianza.
- Quality gates mínimos:
  - Desde `orquestador_de_agentes/`: `uv run pytest tests/test_launch_agent_terminals_script.py tests/test_reconcile_ticket.py tests/test_wt_2026_214_preflight_reconcile.py -q`
  - Desde `orquestador_de_agentes/`: `uv run ruff check scripts/reconcile_ticket.py scripts/get_launcher_state.py tests/test_wt_2026_214_preflight_reconcile.py`
  - Validación manual:
    - drift con ticket previo terminal;
    - drift con ticket previo no terminal;
    - bus ilegible o contradictorio.
- Estrategia de test prescrita para Case B:
  - no basta con testear que `launch_agent_terminals.ps1` contiene cierta string;
  - la lógica de decisión del preflight debe extraerse a un helper Python testeable;
  - los tests de Case B deben verificar que la invocación de `reconcile_ticket.py` ocurre, ya sea con mocks de `subprocess.run` sobre el helper o con invocación real del reconciler en `tmp_path`.

## TP Check
TP-01: el preflight distingue formalmente entre cleanup local y reconciliación en bus.
TP-02: si el ticket previo ya está terminal en el bus, no se emiten eventos nuevos; solo se limpia runtime stale.
TP-03: si el ticket previo no está terminal y el drift es claro, el launcher invoca `reconcile_ticket.py` con razón explícita.
TP-04: si el bus es ilegible o contradictorio, el preflight aborta sin reconciliar ni limpiar de forma engañosa.
TP-05: el caso sano permanece intacto cuando no hay drift entre ticket activo y runtime.
TP-06: existen tests focales de los tres casos y pasan en verde con `pytest`; `ruff` pasa en las superficies tocadas.
TP-07: la distinción cleanup local vs reconciliación histórica queda documentada como contrato del sistema.

## Resultado
- Implementacion aprobada y commiteada en el motor antes del cierre.
- Cierre canonico ejecutado con `scripts/reconcile_ticket.py`.
- El reconciler emitio `STATE_CHANGED -> COMPLETED` y `SUPERVISOR_CLOSED` para `WT-2026-214`.
- Runtime local limpiado: `builder_lock.txt`, `supervisor_lock.txt` y claim de requeue del ticket.

