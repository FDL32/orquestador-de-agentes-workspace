# work_plan.md -- WOT-2026-011j
## Metadata
- **ID:** WOT-2026-011j
- **Contract ID:** T-011J-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Corregir la fuente BOM in-scope en el launcher/runtime PowerShell del repo_motor y dejar explicitado que WOT-2026-012a debe regenerar sus archives historicos una vez saneada la fuente viva, sin editar a mano `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md` dentro de este ticket.
## Non-goals
- No editar manualmente `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md`.
- No tocar `scripts/check_encoding_guard.py`.
- No relanzar ni cerrar WOT-2026-012a dentro de 011j.
- No ampliar el ticket a una caza general de writers PowerShell fuera de la superficie declarada.
## Premisas verificadas antes de Builder
- WOT-2026-011c quedo COMPLETED y su reporte durable existe en `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`.
- `backlog.md` activo ya esta limpio para el encoding guard.
- Los 3 control chars que siguen bloqueando 012a viven solo en `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md`.
- `scripts/launch_agent_terminals.ps1` mantiene escrituras PowerShell BOM-prone in-scope (`Set-Content -Encoding UTF8`, `Out-File -Encoding UTF8`).
## Decision Arquitectonica
011j es un fix puntual de fuente en repo_motor, no una regeneracion de historico documental. El Builder debe endurecer el writer BOM-prone in-scope, probar la barrera de regresion y dejar en `execution_log.md` que el rojo restante de `_archive/backlog_*` se resuelve reactivando 012a para regenerar esos artefactos desde la fuente viva ya limpia.
## Files Likely Touched
### repo_motor
- scripts/launch_agent_terminals.ps1
- tests/test_opencode_config_stability.py
- tests/test_launch_agent_terminals_script.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- .agent/runtime/audit/bom_source_audit_WOT-2026-011c.md
- .agent/collaboration/backlog.md
- .agent/collaboration/_archive/backlog_done.md
- .agent/collaboration/_archive/backlog_pre_012a.md
- .agent/collaboration/CG-WOT-2026-012a.md
- .agent/agent_controller.py
- scripts/check_encoding_guard.py
- tests/test_launcher_ps1_syntax.py
## Forbidden Surfaces
- .agent/collaboration/_archive/backlog_done.md
- .agent/collaboration/_archive/backlog_pre_012a.md
- scripts/check_encoding_guard.py
- .agent/collaboration/TURN.md
- .agent/collaboration/STATE.md
- bus/runtime/events manuales
## Criterios binarios
- El diff elimina las escrituras PowerShell BOM-prone que 011j declare in-scope y las sustituye por un patron BOM-safe verificable.
- Existe al menos una barrera de regresion que falla sin el fix y pasa con el fix para la primitiva o ruta tocada por 011j.
- `tests/test_opencode_config_stability.py` sigue verde y demuestra que el patron BOM-safe existente no regresa.
- 011j no edita manualmente `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md`; deja explicito en `execution_log.md` que esos artefactos se regeneraran al relanzar 012a.
- `python scripts/check_encoding_guard.py` sobre las superficies propias del ticket queda verde.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` queda en 0 errors / 0 warnings.
## STOP conditions
- Parar si ya no existe ningun writer BOM-prone in-scope en repo_motor.
- Parar si la unica forma de poner verde el ticket exige editar manualmente los archives de 012a.
- Parar si el fix real exige tocar `agent_controller.py` o el guard de encoding fuera de la superficie declarada.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011j.md` si el re-check demuestra que la superficie real del fix ya no coincide con el contrato o si el rojo restante pertenece solo a la regeneracion de 012a y no a un writer BOM-prone activo.
