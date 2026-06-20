# work_plan.md -- WOT-2026-012b
## Metadata
- **ID:** WOT-2026-012b
- **Contract ID:** T-012B-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Convertir el contrato de cola viva fijado por `012a` en un gate fail-closed ejecutable desde `repo_motor`, leyendo `repo_destino/.agent/collaboration/backlog.md` solo por `--project-root` o `AGENT_PROJECT_ROOT`.
## Non-goals
- No reestructurar otra vez `backlog.md`; `012a` ya fijo el formato.
- No tocar `scripts/archive_collaboration_artifacts.py`, `scripts/session_closeout.py`, `--mark-ready` ni el archivador del closeout.
- No depender de comentarios HTML o prose libre para extraer semantica.
- No degradar silenciosamente a warning permanente; el rollout solo puede ser explicito y acotado.
- No editar `bus/runtime/events` manualmente.
## Premisas verificadas antes de Builder
- `WOT-2026-012a` ya quedo `COMPLETED` y dejo la cola viva en formato parseable con columna `Reactivation`.
- `T-012B-001` ya esta congelado en `ticket_contracts.md`.
- El gate debe ejecutarse desde `repo_motor`, pero leer `repo_destino` de forma topologica; depender del cwd dogfooding seria un bug.
- La cola viva ya no debe contener `012a` como ticket activo ni terminal mezclado.
## Decision Arquitectonica
`012b` introduce una barrera unica en `repo_motor`: validar solo la tabla activa del backlog vivo y fallar cerrada ante drift estructural o semantico. La autoridad del dato sigue en `repo_destino`; el motor solo la consume via `--project-root` o `AGENT_PROJECT_ROOT`, sin leer seeds del motor ni acoplarse al archivador del closeout.
## Files Likely Touched
### repo_motor
- scripts/check_backlog_contract.py
- tests/unit/test_check_backlog_contract.py
- tests/unit/test_no_legacy_topology_terms.py
- tests/unit/test_run_gates_dispatch.py
- scripts/run_gates_dispatch.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- .agent/collaboration/backlog.md
- .agent/collaboration/STATE.md
- .agent/collaboration/TURN.md
- scripts/check_deliverables_exist.py
- scripts/validate_ticket_prose.py
## Forbidden Surfaces
- lectura de `backlog.md` relativa al cwd
- dependencia en HTML comments o prose libre
- vocabulario nuevo de estados fuera del cerrado por `012a`
- edicion manual de `bus/runtime/events`
- tocar archivador, session close o barreras de cierre ajenas
## Criterios binarios
- Existe `scripts/check_backlog_contract.py` y falla con `exit != 0` ante violaciones estructurales o semanticas obligatorias.
- Falla cerrado si faltan `--project-root` y `AGENT_PROJECT_ROOT`.
- Parsea solo la tabla activa y valida columnas, encabezados `### WOT-...`, vocabulario cerrado de `Status` y formato permitido de `Reactivation`.
- La lista de estados vivos queda codificada en el gate: `pending`, `blocked`, `deferred`, `ready-for-review`, `awaiting-manager`, `completed-partial`.
- Existe barrera de regresion que demuestra PASS con backlog valido y FAIL sin `--project-root`/`AGENT_PROJECT_ROOT`.
- `ruff`, tests focales, suite aplicable y `validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si el parser necesita HTML comments o prose libre.
- Parar si el gate lee accidentalmente el seed del motor en vez del `repo_destino`.
- Parar si la semantica de `Reactivation` no puede distinguir trigger estructurado de prosa vaga.
- Parar si la unica integracion posible es warning permanente.
## CONTRACT_GAP
Emitir `CG-WOT-2026-012b.md` si el backlog post-`012a` no expone schema suficiente, si la resolucion topologica del destino no puede fallar cerrada, o si la integracion exige acoplar el gate al archivador del closeout.
