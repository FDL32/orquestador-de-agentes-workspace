# work_plan.md -- WOT-2026-012a
## Metadata
- **ID:** WOT-2026-012a
- **Contract ID:** T-012A-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** documentation
- **Builder clarification budget:** 0
- **delivery_authority:** repo_destino
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Reestructurar `backlog.md` para separar cola viva e historico, fijar formato parseable estable y regenerar `_archive/backlog_done.md` / `_archive/backlog_pre_012a.md` desde la fuente viva ya limpia tras el cierre de `011j`.
## Non-goals
- No tocar `scripts/launch_agent_terminals.ps1` ni sanear el BOM/mojibake preexistente del propio `.ps1`; esa deuda queda explicitamente en `011f`.
- No modificar `--session-close`, `--mark-ready` ni el archivador del closeout.
- No editar `bus/runtime/events` manualmente.
- No introducir nuevos tickets ni reabrir `011j` dentro de `012a`.
## Premisas verificadas antes de Builder
- `WOT-2026-011j` quedo `COMPLETED` y corrigio la fuente BOM-safe del writer PowerShell in-scope.
- `backlog.md` sigue mezclando cola viva + historico + ticket terminal `011j`, por lo que la deuda estructural de `012a` sigue vigente.
- `T-012A-001` ya esta congelado en `ticket_contracts.md`.
- La deuda del BOM/mojibake preexistente del propio `scripts/launch_agent_terminals.ps1` queda fuera de scope de `012a` y pasa a `011f`.
## Decision Arquitectonica
`012a` se limita al corte documental y estructural del backlog en `repo_destino`. La fuente BOM del writer PowerShell ya fue corregida en `011j`; el BOM/mojibake preexistente del propio archivo `.ps1` del motor es una deuda distinta de encoding fuente y se seguira por `011f`, para no mezclar regeneracion historica de backlog con saneado del launcher.
## Files Likely Touched
### repo_destino
- .agent/collaboration/backlog.md
- .agent/collaboration/_archive/backlog_done.md
- .agent/collaboration/_archive/backlog_pre_012a.md
- .agent/collaboration/execution_log.md
## Read/inspect only
- CHANGELOG.md
- .agent/collaboration/STATE.md
- .agent/collaboration/TURN.md
- .agent/planning/ticket_contracts.md
- historico previo de backlog.md
- filas 011e..011i
- WOT-2026-010m
## Forbidden Surfaces
- scripts/archive_collaboration_artifacts.py
- scripts/session_closeout.py
- --session-close / --mark-ready
- edicion manual de bus/runtime/events
- cualquier saneado del `.ps1` del motor dentro de este ticket
## Criterios binarios
- `backlog.md` activo deja de contener terminales mezclados con la cola operativa.
- Existe un historico separado mantenido por paso explicito del Manager, no por el archivador del closeout.
- La tabla activa queda como unica fuente parseable con columna `Reactivation`.
- La seccion `### WOT-2026-012a` se conserva integra en el historico movido.
- Existe snapshot pre-corte portable en `_archive/backlog_pre_012a.md` o evidencia equivalente documentada.
- `python scripts/check_encoding_guard.py` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si aparece perdida de historico no auditable.
- Parar si el formato parseable exige volver a depender de comentarios HTML.
- Parar si el corte exige tocar el archivador del closeout o el saneado del `.ps1` del motor.
## CONTRACT_GAP
Emitir `CG-WOT-2026-012a.md` si el snapshot no puede materializarse de forma portable, si la seccion `### WOT-2026-012a` no puede conservarse integra en el historico, o si la unica forma de verde exige absorber la deuda de `011f`.
