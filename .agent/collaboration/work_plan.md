# work_plan.md -- WOT-2026-013g
## Metadata
- **ID:** WOT-2026-013g
- **Contract ID:** T-013G-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** analysis
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Explicar con medicion reproducible el coste anomalo de `tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion`, produciendo un reporte durable en `repo_motor` sin tocar el test, runner ni producto en esta ronda.
## Non-goals
- No tocar `tests/unit/test_detect_version.py`.
- No tocar producto Python, `scripts/run_pytest_safe.py` ni `pytest.ini`.
- No mezclar el ticket con una optimizacion code de `010k` ni con follow-ups adyacentes.
- No tocar CI/workflows ni otras familias de tests.
## Premisas verificadas antes de Builder
- `010j` y `010p` ya documentaron a `test_upgrade_path_suggestion` como outlier #2-#3 (~59-70s) sin causa explicada.
- `013e` lo clasifico como el unico hotspot `unknown` y lo promovio a follow-up analitico (`FU-013E-3`).
- El cuerpo visible del test sigue siendo trivial (3 asserts sobre `suggest_upgrade_path`), asi que el coste probable esta fuera de la logica local del cuerpo.
- `validate --json --project-root <repo_destino>` estaba en 0 errors / 0 warnings antes del bootstrap de `013g`.
## Decision Arquitectonica
`013g` es un ticket de `analysis`: el deliverable es un reporte durable en `docs/test_performance/` mas evidencia operacional en `execution_log.md`. Las mediciones pueden ejecutar pytest focal como instrumento de investigacion, pero NO convierten el ticket en cambio de codigo ni autorizan tocar el test o el producto.
## Files Likely Touched
### repo_motor
- docs/test_performance/test_upgrade_cost_WOT-2026-013g.md
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- tests/unit/test_detect_version.py
- docs/test_performance/test_performance_baseline.md
- docs/test_performance/test_performance_variance.md
- docs/test_performance/test_suite_audit_WOT-2026-013e.md
- .agent/runtime/pytest-safe/last-run.json
## Forbidden Surfaces
- tests/unit/test_detect_version.py
- cualquier otro test
- producto Python
- scripts/run_pytest_safe.py
- pytest.ini
- CI/workflows
- privada/
- .env
- eventos del bus escritos manualmente
## Criterios binarios
- Existe un reporte durable en `repo_motor/docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`.
- El reporte documenta mediciones reproducibles que expliquen la mayor parte del coste observado o cierra explicitamente `sin optimizacion segura` con evidencia.
- El reporte separa [V] verificado de [I] inferencia en cada conclusion sustantiva.
- El reporte recomienda una optimizacion local concreta o descarta intervenir en este ticket, sin tocar test ni producto.
- `execution_log.md` registra una linea final: `Reporte docs/test_performance/test_upgrade_cost_WOT-2026-013g.md creado. Validate: exit code 0, 0 errors, 0 warnings.`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
## STOP conditions
- Parar si la explicacion real exige editar `tests/unit/test_detect_version.py` o producto.
- Parar si la causa solo puede expresarse como intuicion no medida.
- Parar si la medicion depende de output historico no reconciliado en vez de evidencia fresca comparable.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013g.md` si la unica forma de explicar el coste exige editar el test o producto, si la medicion no es reproducible entre corridas comparables, o si el deliverable deja de ser puramente analitico.
