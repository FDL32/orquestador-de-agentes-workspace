# Execution Log

**Estado:** IN_PROGRESS


## WT-2026-205
- Reconciliacion canonicamente cerrada en el bus.
- Runtime anterior purgado para permitir el arranque limpio del siguiente ticket.

## WT-2026-210
- Auditoria integral del bus completada.
- Artefacto de arquitectura entregado en `orquestador_de_agentes/docs/BUS_ARCHITECTURE_WT-2026-210.md`.
- Reconciler de ticket creado como herramienta de mantenimiento en `orquestador_de_agentes/scripts/reconcile_ticket.py`.

## WT-2026-211
- Inicio documental: 2026-06-02.
- Objetivo: centralizar la materializacion de `TURN.md`, `STATE.md` y `execution_log.md` durante la transicion.
- Restriccion: no integrar `reconcile_ticket.py` al launcher en este ticket.
- Estado documental: IN_PROGRESS.
- Validacion externa al loop: aprobada por Manager tras tests focales y `ruff` en el motor.
- Cierre canonico solicitado para el bus del workspace.

## WT-2026-212
- Inicio documental: 2026-06-02.
- Objetivo: garantizar un consumidor durable de `REVIEW_DECISION=CHANGES`.
- Restriccion: no reabrir la competencia de proyecciones cerrada en `WT-2026-211`.
- Implementacion: `review_bridge.py` garantiza un tick real del supervisor mediante `_ensure_durable_changes_consumer(...)` cuando no queda supervisor vivo tras `CHANGES`.
- Validacion: `uv run pytest orquestador_de_agentes\\tests\\test_wt_2026_212_durable_changes.py orquestador_de_agentes\\tests\\test_manager_review_bridge.py -q` -> 108 passed.
- Validacion focal: `uv run pytest orquestador_de_agentes\\tests\\test_wt_2026_212_durable_changes.py -q` -> 2 passed.
- Calidad: `uv run ruff check orquestador_de_agentes\\bus\\review_bridge.py orquestador_de_agentes\\tests\\test_wt_2026_212_durable_changes.py` -> All checks passed.
- Estado documental: COMPLETED.

## WT-2026-216
- Inicio documental: 2026-06-02.
- Objetivo: hacer que el launcher lea el bus en vez de `TURN.md` para decidir que agente lanzar.
- Restriccion: no reabrir la competencia de proyecciones cerrada en `WT-2026-211`.
- Motivacion: convertir el rescate durable de `WT-2026-212` en fallback excepcional y no en camino habitual.
- Implementacion: `launch_agent_terminals.ps1` intenta `get_launcher_state.py` antes de leer `TURN.md`; el helper deriva estado canonico con `StateMachine.derive_state_from_events()`.
- Validacion: `uv run pytest orquestador_de_agentes\\tests\\test_launch_agent_terminals_script.py orquestador_de_agentes\\tests\\test_wt_2026_216_launcher_bus_read.py -q` -> 21 passed.
- Calidad: `uv run ruff check orquestador_de_agentes\\scripts\\get_launcher_state.py orquestador_de_agentes\\tests\\test_launch_agent_terminals_script.py orquestador_de_agentes\\tests\\test_wt_2026_216_launcher_bus_read.py` -> All checks passed.
- Nota residual: el mapeo `TicketState -> (role, action)` esta duplicado entre el helper y el supervisor; queda como deuda de limpieza posterior, no bloqueante.
- Estado documental: COMPLETED.

## WT-2026-214
- Inicio documental: 2026-06-02.
- Objetivo: integrar reconciliacion automatica en preflight sin mezclar cleanup local y cierre historico en el bus.
- Restriccion: si el bus es ilegible, ambiguo o contradictorio, el launcher debe abortar sin cerrar nada.
- Base conceptual: memorias `bus-first-read-authority`, `canonical-consumer-recovery` y `cleanup-vs-bus-reconcile` ya consolidadas.
- Implementacion:
  - `scripts/preflight_reconcile.py`: helper Python con `derive_preflight_decision()` para `ALIGNED`, `CLEANUP_LOCAL`, `RECONCILE` y `ABORT`.
  - `scripts/launch_agent_terminals.ps1`: nueva `Invoke-PreflightReconcile` antes de la reparacion destructiva; usa `Get-StartupAlignment` como lectura inicial.
  - `reconcile_ticket.py` se invoca solo para `RECONCILE`.
- Validacion:
  - `uv run pytest tests/test_wt_2026_214_preflight_reconcile.py -q` -> 11 passed.
  - `uv run pytest tests/test_launch_agent_terminals_script.py tests/test_reconcile_ticket.py tests/test_wt_2026_214_preflight_reconcile.py -q` -> 31 passed.
  - `uv run ruff check scripts/reconcile_ticket.py scripts/get_launcher_state.py scripts/preflight_reconcile.py tests/test_wt_2026_214_preflight_reconcile.py tests/test_reconcile_ticket.py tests/test_launch_agent_terminals_script.py` -> All checks passed.
- Cobertura de TP Checks:
  - TP-01: `test_preflight_returns_distinct_decisions` verifica los casos.
  - TP-02: `test_terminal_prev_ticket_returns_cleanup` y `test_terminal_via_supervisor_closed` -> `CLEANUP_LOCAL` sin eventos nuevos.
  - TP-03: `test_non_terminal_prev_ticket_returns_reconcile` y `test_non_terminal_in_review_returns_reconcile` -> `RECONCILE`.
  - TP-04: abortos por bus ilegible o contradictorio cubiertos por tests focales.
  - TP-05: `test_no_runtime_state_returns_aligned` y `test_same_ticket_returns_aligned` -> `ALIGNED`.
  - TP-06: tests verdes y `ruff` limpio.
  - TP-07: distincion documentada en docstring y contrato de decision.
- Cierre canonico: `scripts/reconcile_ticket.py --ticket WT-2026-214` emitio `STATE_CHANGED -> COMPLETED` y `SUPERVISOR_CLOSED`; limpio locks y claim de requeue antes de la migracion fisica del workspace.
- Estado documental: COMPLETED.

## WT-2026-208
- Inicio documental: 2026-06-03.
- Objetivo: estabilizar la suite global del motor tras la transicion workspace+motor.
- Baseline real tras cambios iniciales del Builder: 45 failed, 1772 passed, 21 skipped, 43 errors.
- Pasada 1 - paths/cwd/assets: cambios validos en tests de integration/scope/bus drift/launcher preflight y `scripts/run_llm_evals.py`.
- Validacion Pasada 1: `python -m pytest tests/test_completion_integration.py tests/test_launcher_preflight.py tests/unit/test_bus_drift_detection.py tests/unit/test_scope_gate.py tests/unit/test_run_llm_evals.py -q` -> 36 passed.
- Calidad Pasada 1: `python -m ruff check tests/test_completion_integration.py tests/test_launcher_preflight.py tests/unit/test_bus_drift_detection.py tests/unit/test_scope_gate.py tests/unit/test_run_llm_evals.py scripts/run_llm_evals.py` -> All checks passed.
- Pendiente: Fase 2 sigue concentrada en `tests/unit/test_upgrade.py` y `tests/unit/test_migrate_legacy_project.py`; no cerrar sin rerun global final.
- Nota de scope: `.agent/agent_controller.py` queda fuera de Pasada 1 para revision separada; `.agent/hooks/__init__.py` queda sin commitear por estar fuera del scope actual.
- Estado documental: IN_PROGRESS.

