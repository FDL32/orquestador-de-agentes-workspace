# work_plan.md -- WOT-2026-013j
## Metadata
- **ID:** WOT-2026-013j
- **Contract ID:** T-013J-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Eliminar la deriva entre el `Files Likely Touched` de las fichas detalladas de `backlog.md` y el contrato frozen, reforzando la validacion del backlog y explicitando la autoridad del contrato/work_plan sin tocar scope gate ni handoff.
## Non-goals
- No tocar `.agent/scope_gate.py`, `scripts/pre_handoff_guard.py`, `.agent/agent_controller.py` ni `scripts/check_deliverables_exist.py`.
- No convertir `backlog.md` en una segunda autoridad del FLT.
- No reabrir `010n`, `011h` ni cambiar la semantica del handoff canonico.
- No hacer un rediseno mayor del lifecycle de packet.
## Premisas verificadas antes de Builder
- El FLT canonico vive en `ticket_contracts.md` y luego en `work_plan.md`, no en la ficha detallada del backlog.
- `scripts/check_backlog_contract.py` valida hoy la tabla viva y el header de las fichas, pero no el cuerpo de una ficha con FLT duplicado/divergente.
- El patron fue recurrente en `013h` y `013i`; no es una desviacion aislada del usuario.
- Si la unica salida exige tocar scope gate, handoff o controller, el ticket debe bloquear por `CG-WOT-2026-013j.md`.
## Decision Arquitectonica
`013j` es un ticket `code` de contrato/proceso del motor. La correccion permitida vive en el gate del backlog y en la regla de pipeline que fija la autoridad del FLT. El contrato frozen y `work_plan.md` siguen siendo la unica fuente de verdad operativa; el backlog solo puede resumir o referenciar, no re-declarar un FLT divergente.
## Files Likely Touched
### repo_motor
- scripts/check_backlog_contract.py
- tests/unit/test_check_backlog_contract.py
- prompts/orchestrator_pipeline.md
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- .agent/collaboration/backlog.md
- .agent/planning/ticket_contracts.md
- .agent/collaboration/work_plan.md
- scripts/pre_handoff_guard.py
- .agent/scope_gate.py
- skills/manager-create-work-plan/SKILL.md
- prompts/audit_cf_ticket_contract.md
## Forbidden Surfaces
- .agent/scope_gate.py
- scripts/pre_handoff_guard.py
- .agent/agent_controller.py
- scripts/check_deliverables_exist.py
- CI/workflows
- backlog.md como autoridad paralela del FLT
- privada/
- .env
- eventos del bus escritos manualmente
## Criterios binarios
- Existe una sola fuente de verdad operativa para el FLT: la ficha detallada del backlog deja de poder re-declararlo de forma divergente, o el gate correspondiente falla cerrado con diagnostico explicito antes del handoff.
- Existe al menos una barrera de regresion en `tests/unit/test_check_backlog_contract.py` que falla sin el fix sobre una ficha con `Files Likely Touched` duplicado/divergente y pasa con el fix.
- `prompts/orchestrator_pipeline.md` deja explicita la autoridad del contrato frozen / `work_plan.md` sobre el FLT si el flujo seguira leyendo la ficha detallada del backlog.
- `python -m pytest tests/unit/test_check_backlog_contract.py -q -p no:cacheprovider` termina verde.
- `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- No se debilitan `scope_gate`, `pre_handoff_guard` ni la autoridad del contrato frozen.
## STOP conditions
- Parar si el patron real no vive en la validacion/generacion del backlog sino en otra superficie no declarada.
- Parar si la unica salida verde consiste en aceptar dos fuentes de verdad sincronizadas manualmente.
- Parar si el fix pide ampliar scope a lifecycle de packet completo en vez de un cambio acotado.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013j.md` si la unica salida segura exige tocar `scope_gate`, `pre_handoff_guard`, `agent_controller.py` o convertir `backlog.md` en autoridad paralela del FLT.
