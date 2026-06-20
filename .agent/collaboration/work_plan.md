# work_plan.md -- WOT-2026-013a
## Metadata
- **ID:** WOT-2026-013a
- **Contract ID:** T-013A-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Hacer robusto `tests/test_controller_integration.py::test_approved_pending_returns_builder_implement` en aislamiento, arreglando el drift de topologia del fixture sandbox sin tocar codigo productivo del controller ni introducir una feature nueva.
## Non-goals
- No tocar `.agent/agent_controller.py` ni anadir `--validate-topology` en este ticket.
- No tocar `runtime/`, `bus/`, `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` ni CI/workflows.
- No convertir el fix en una reescritura general del sandbox ni en una deuda arquitectonica encubierta.
## Premisas verificadas antes de Builder
- `python -m pytest tests/test_controller_integration.py -k approved_pending -q` sigue fallando hoy con `AssertionError: No JSON en output del controller`.
- El rojo esta acotado al fixture/driver de `tests/test_controller_integration.py`, no a una regresion productiva confirmada del controller real.
- El ticket se congela como fix test-only: si para volverlo verde hay que tocar controller productivo, el resultado correcto es `CONTRACT_GAP`.
## Decision Arquitectonica
`013a` resuelve solo la topologia de prueba. La via preferida es ejecutar el controller real con `project_root`/entorno apuntando al sandbox o eliminar la dependencia de `__file__.parent.parent` dentro del propio test, pero sin convertir ese aprendizaje en una feature nueva de produccion. El contrato prohibe tocar `.agent/agent_controller.py`; si eso no basta, el Builder debe bloquear y devolver follow-up.
## Files Likely Touched
### repo_motor
- tests/test_controller_integration.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- .agent/agent_controller.py
- runtime/
- bus/
- .agent/runtime/pytest-safe/last-run.json
- .agent/collaboration/backlog.md
## Forbidden Surfaces
- tocar `.agent/agent_controller.py`
- anadir `--validate-topology` o cualquier feature nueva de produccion
- tocar runtime, bus, handoff, runner o CI
- escribir eventos del bus manualmente
## Criterios binarios
- `python -m pytest tests/test_controller_integration.py -k approved_pending -q` pasa en aislamiento.
- El fix permanece acotado a `tests/test_controller_integration.py`.
- Existe barrera FAIL-sin/PASS-con para el mismo test aislado.
- `python -m pytest tests/test_controller_integration.py -q`, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- `execution_log.md` deja constancia explicita de que el ticket resolvio drift de topologia de test sin tocar produccion.
## STOP conditions
- Parar si el unico fix viable toca `.agent/agent_controller.py` o exige feature nueva de topologia.
- Parar si el sandbox requiere reescritura sistemica fuera del test.
- Parar si el test ya no reproduce el rojo aislado al re-check.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013a.md` si el rojo aislado no puede resolverse dentro de `tests/test_controller_integration.py`, si el fix exige tocar el controller productivo, o si la deuda real resulta ser una arquitectura de sandbox fuera del alcance del ticket.
