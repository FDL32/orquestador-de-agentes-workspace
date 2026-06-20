# work_plan.md -- WOT-2026-011g
## Metadata
- **ID:** WOT-2026-011g
- **Contract ID:** T-011G-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** documentation
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Explicitar y unificar en prompts/docs la diferencia entre `loop rapido` de diagnostico local y `cierre canonico` de ticket, para que Builder, Manager y Orchestrator no presenten evidencia parcial como handoff o cierre real.
## Non-goals
- No tocar `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py`, `.agent/agent_controller.py`, `scripts/run_gates_dispatch.py` ni `bus/review_bridge.py`.
- No cambiar semantica de suite, handoff o closeout; solo documentar y alinear la politica ya vigente.
- No retirar ni reabrir `011h` dentro de este ticket; cualquier normalizacion de backlog sobre ese ticket queda fuera de scope.
## Premisas verificadas antes de Builder
- La politica actual existe como fragmentos en `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md`, `prompts/audit_agent_output.md` y `QUICKSTART.md`, pero no queda declarada como una frontera corta y consistente.
- Las observaciones `obs-20260619-background-wallclock-not-canonical` y `obs-20260620-last-run-canonical-lives-in-motor` documentan confusion recurrente reciente sobre que cuenta como evidencia canonica.
- El ticket es puramente documental: si la documentacion veraz exigiera tocar tooling, el resultado correcto es `CONTRACT_GAP`.
## Decision Arquitectonica
`011g` centraliza la politica en texto y alinea sus consumidores, pero no reabre tooling. La via preferida es anadir una seccion explicita en `QUICKSTART.md` y sincronizar el lenguaje de los prompts principales con esa misma distincion: `loop rapido` sirve para diagnostico local; `cierre canonico` exige suite canonia en HEAD, `validate 0/0` y handoff/cierre con eventos reales.
## Files Likely Touched
### repo_motor
- prompts/orchestrator_launch_builder.md
- prompts/manager_review.md
- prompts/orchestrator_pipeline.md
- QUICKSTART.md
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- prompts/audit_agent_output.md
- AGENTS.md
- PROJECT.md
- .agent/runtime/memory/observations.jsonl
- .agent/runtime/memory/MEMORY.md
## Forbidden Surfaces
- tocar tooling (`run_pytest_safe.py`, `pre_handoff_guard.py`, `.agent/agent_controller.py`, `run_gates_dispatch.py`, `review_bridge.py`)
- tocar tests, CI/workflows o gates
- introducir criterios de codigo en un ticket documental
- usar `011g` para normalizar `011h` o cualquier otra deuda de backlog no documental
## Criterios binarios
- Existe una seccion explicita y corta que nombre `loop rapido` y `cierre canonico`, y delimite que evidencia vale para cada uno.
- `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md` y `QUICKSTART.md` quedan alineados entre si sobre suite canonia, `validate`, handoff y cierre.
- Ningun texto tocado sigue permitiendo presentar pytest focal, wall-clock en background o tests aislados verdes como sustituto de suite canonica / `READY_FOR_REVIEW` / cierre canonico.
- El diff permanece documental: no toca scripts, gates, controller, tests ni CI.
- `python scripts/check_encoding_guard.py <docs_tocados>` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica forma de resolver contradicciones documentales exige tocar tooling productivo.
- Parar si el ticket deja de ser puramente documental y necesita gates de codigo o sandbox.
- Parar si otro ticket activo cambia las mismas superficies de prompt/doc y obliga a serializacion antes de seguir.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011g.md` si dejar la politica veraz y consistente exige cambiar semantica de `run_pytest_safe.py`, `pre_handoff_guard.py`, `.agent/agent_controller.py`, `run_gates_dispatch.py` o `review_bridge.py`, o si la deuda real no es documental sino de tooling.
