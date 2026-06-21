# work_plan.md -- WOT-2026-013e
## Metadata
- **ID:** WOT-2026-013e
- **Contract ID:** T-013E-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** analysis
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Producir un inventario durable y auditable de la suite del motor que clasifique familias de tests por valor y riesgo (`core regression`, `structural gate`, `legacy candidate`, `redundant candidate`, `unknown`), dejando follow-ups pequenos y verificables para poda segura sin tocar tests, runner, CI ni producto en esta ronda.
## Non-goals
- No tocar `tests/`.
- No tocar `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml` ni `uv.lock`.
- No tocar CI/workflows ni `scripts/run_gates_dispatch.py`.
- No reabrir `011e`, `010m`, `011i` ni `013d`.
- No borrar, `xfail`, `skip` ni relajar tests en este ticket.
- No mezclar runner, CI, producto y poda masiva en una sola propuesta.
## Premisas verificadas antes de Builder
- `010j` ya dejo una baseline durable de la suite y refuto `git/subprocess` como hotspot dominante.
- `010k` ya documento y cerro follow-ups locales sobre hotspots reales de filesystem/scan.
- `011e`, `010m` y `011i` ya cerraron la frontera local/CI/default de xdist; `013e` no debe reabrir esa familia sin evidencia nueva suficiente para `CONTRACT_GAP`.
- `013d` ya cerro la causa raiz de producto ligada a borrados concurrentes; el ticket actual es de analisis de suite, no de producto.
- `validate --json --project-root <repo_destino>` estaba en 0 errors / 0 warnings antes del bootstrap de `013e`.
## Decision Arquitectonica
`013e` es un ticket de `analysis`: el deliverable es un reporte durable en `repo_motor/docs/test_performance/` mas evidencia operacional en `execution_log.md`. Las superficies `tests/`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml` y la documentacion previa son contexto `Read/inspect only`; no se convierten en scope productivo ni en entregables Builder.
## Files Likely Touched
### repo_motor
- docs/test_performance/test_suite_audit_WOT-2026-013e.md
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- tests/
- tests/README.md
- tests/ARCHITECTURE.md
- scripts/run_pytest_safe.py
- pytest.ini
- pyproject.toml
- docs/test_performance/test_performance_baseline.md
- docs/test_performance/test_performance_followup.md
- docs/test_performance/test_selection.md
- .agent/runtime/pytest-safe/last-run.json
- .agent/collaboration/backlog.md
## Forbidden Surfaces
- tests/
- scripts/run_pytest_safe.py
- pytest.ini
- pyproject.toml
- uv.lock
- CI/workflows
- scripts/run_gates_dispatch.py
- scripts/pre_handoff_guard.py
- privada/
- .env
- eventos del bus escritos manualmente
- cualquier re-apertura de `011e`, `010m`, `011i` o `013d`
- borrar, `xfail`, `skip` o relajar tests en este ticket
## Criterios binarios
- Existe un reporte durable en `repo_motor/docs/test_performance/test_suite_audit_WOT-2026-013e.md`.
- El reporte inventaria la suite por familias o subsistemas con conteo auditable y clasificacion `core regression`, `structural gate`, `legacy candidate`, `redundant candidate` o `unknown`.
- Cada clasificacion explicita si esta soportada por evidencia verificada o por inferencia limitada.
- El reporte lista tests o familias lentas, marks/skip estructurales, barreras canonicas del runner/handoff y cualquier debt legacy detectable sin tocar codigo productivo.
- El reporte identifica follow-ups pequenos y verificables para poda o refactor, cada uno con superficie acotada y sin mezclar runner, CI, producto y borrado masivo.
- El reporte deja explicito que `013e` no borra ni relaja tests y que las fronteras cerradas por `011e`, `010m`, `011i` y `013d` quedan fuera de scope salvo evidencia nueva que obligue a `CONTRACT_GAP`.
- `execution_log.md` registra una linea final: `Reporte docs/test_performance/test_suite_audit_WOT-2026-013e.md creado. Validate: exit code 0, 0 errors, 0 warnings.`
- `git diff --name-only` del `repo_motor` se limita al artefacto documental del ticket.
- `python scripts/check_encoding_guard.py docs/test_performance/test_suite_audit_WOT-2026-013e.md` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la unica forma de justificar una clasificacion exige editar tests o tooling.
- Parar si el resultado depende de output viejo no reconciliado con el HEAD actual.
- Parar si la recomendacion util solo puede expresarse como poda masiva o como reabrir la familia xdist/producto en vez de abrir follow-ups pequenos.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013e.md` si el inventario no puede separar barreras core/estructurales de candidatos a poda sin tocar `tests/`, runner, CI o producto; si la evidencia actual no permite proponer follow-ups pequenos con criterio verificable; o si la auditoria exige reabrir una frontera ya cerrada de `011e`, `010m`, `011i` o `013d`.
