# Execution Log: WOT-2026-007a - Contract Formation Pipeline v0 (contrato documental minimo)

## Metadata
**Estado:** COMPLETED
- **ID:** WOT-2026-007a
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Rol activo:** ORQUESTADOR
- **Accion:** CLOSED -> revision independiente APROBADO + reconcile_ticket.py

## Resumen
- Pipeline orquestado (FALLBACK_SIN_TASK_TOOL). Builder de un ticket documentation de
  autoridad repo_motor: entregables en el motor, estado de ticket en el destino.
- Implementado el contrato documental minimo del Contract Formation Pipeline v0 (provisional
  hasta ratificacion en 007b). Sin tocar runtime/bus/controller/scripts/CI.

## Entregables creados (repo_motor)
- `prompts/contract_formation_pipeline.md`: fases (0-7), roles, maquina de status
  (draft/review/frozen/invalidated), DEC-* tiers (T1a<=3/ronda, T1b/c, T2), evidence rules,
  plan_graph + Impact Simulation, STOP y handoff a orchestrator_pipeline.md (gate 2.a).
- `docs/contract_formation/README.md`: indice humano + mapa de plantillas + principios.
- `docs/contract_formation/templates/repo_charter.md`: Product Intent, Architecture
  Constraints, Non-Goals, Quality Bar, Security Constraints, OBJ-* + failure_modes,
  Negative Audit Checklist.
- `docs/contract_formation/templates/ticket_contract.md`: status, Objective/Plan-Link,
  Premise + Premise Re-check, Context Baseline, Files Likely Touched, Forbidden Surfaces,
  DoD, STOP, CONTRACT_GAP behavior, clarification budget 0.
- `docs/contract_formation/templates/evidence_catalog.md`: tipo/fiabilidad/corroboracion/
  injection_risk; regla T1a no se sostiene en evidencia externa no corroborada.
- `docs/contract_formation/templates/contract_gap.md`: CG-<TICKET_ID> con gap_type, evidencia
  y handoff frozen->invalidated de vuelta a genesis.
- `MANIFEST.workspace`: `.agent/planning/` declarado destino-keep (analogo a audits).

## Decision .agent/planning/ + MANIFEST.workspace
`.agent/planning/` se declara superficie destino-keep en MANIFEST.workspace (precedente:
`.agent/audits/system_health/`). MANIFEST gobierna copy_tree, no prune; la persistencia
tambien queda protegida del prune por el guard git-tracked del instalador (WOT-2026-003d).
Se declara ya, en vez de diferir, para no bloquear 007b.

## Gates y evidencia real (comandos exactos)
- `python scripts/check_encoding_guard.py <6 entregables + MANIFEST.workspace>` (cwd=motor)
  -> exit 0. Todos sin BOM, LF uniforme (convencion motor `*.md eol=lf`).
- `git add ... && git diff --cached --check` (motor) -> exit 0 (sin trailing whitespace).
- `git diff --cached --stat` (motor) -> 7 files changed, 394 insertions(+).
- `agent_controller --validate --json --project-root <destino>` -> registrado abajo en Resultado.

## Cierre canonico
- Manager review: APROBADO, blockers=[]; decision artifact `.agent/runtime/reviews/decision_WOT-2026-007a.json`.
- Commit repo_motor: `7bf57f8 docs(WOT-2026-007a): add contract formation v0`.
- Reparacion canonica del flujo FALLBACK: primero `scripts/reconcile_ticket.py` emitio `STATE_CHANGED->COMPLETED` y `SUPERVISOR_CLOSED`; al detectar que faltaba `BUILDER_EXIT`, se uso el flujo sancionado del controller: `--reopen-terminal-ticket`, `--mark-ready --force`, `--manager-approve WOT-2026-007a --force`.
- Resultado del controller: `manager-approve` cerro el ticket y limpio estado auxiliar.
- Validate final: `python <motor>/.agent/agent_controller.py --validate --json --project-root <destino>` -> exit 0, 0 errors, 0 warnings.

## Resultado
- WOT-2026-007a COMPLETED.
- Contrato documental v0 queda provisional hasta ratificacion/correccion en WOT-2026-007b.
- Siguiente ticket recomendado: WOT-2026-007b (validacion vertical idea -> contrato -> backlog -> Builder sin aclaraciones).

---

# WOT-2026-007g — Extender validate_plan_graph (paralelizable estricto + Merge Regression Audit)

## Quality Gates

- `ruff check scripts/validate_contract_formation.py tests/unit/test_validate_contract_formation.py docs/contract_formation/templates/plan_graph.md docs/contract_formation/examples/python_service_minimal/plan_graph.md tests/fixtures/contract_formation/valid/plan_graph.md` -> exit 0, All checks passed
- `python -m pytest tests/unit/test_validate_contract_formation.py -v` -> 43/43 passed
- `python -m pytest tests/unit/ -v` -> 1075/1075 passed
- `python scripts/check_encoding_guard.py scripts/validate_contract_formation.py tests/unit/test_validate_contract_formation.py docs/contract_formation/templates/plan_graph.md docs/contract_formation/examples/python_service_minimal/plan_graph.md tests/fixtures/contract_formation/valid/plan_graph.md` -> exit 0 (clean)
- No nuevas dependencias introducidas (stdlib-only)

## Cambios realizados

1. `scripts/validate_contract_formation.py`: Nueva funcion `_validate_paralelizable_values()` + extended `validate_plan_graph()` con validacion estricta de `paralelizable` (yes/no/after PLAN-\\d+) y chequeo de seccion `## Merge Regression Audit`.
2. `tests/unit/test_validate_contract_formation.py`: 7 nuevos tests (6 para plan_graph + 1 template regression).
3. `docs/contract_formation/templates/plan_graph.md`: Valor formal `yes` en celda de ejemplo.
4. `docs/contract_formation/examples/python_service_minimal/plan_graph.md`: Migrado `no -- unico plan` -> `no`.
5. `tests/fixtures/contract_formation/valid/plan_graph.md`: Migrado `no -- unico plan` -> `no` + anadida seccion `## Merge Regression Audit`.

## DoD cumplido

- [x] `validate_plan_graph` rechaza `paralelizable: no -- unico plan` con error explicito
- [x] `validate_plan_graph` acepta yes, no, after PLAN-001, after PLAN-002 (tests positivos)
- [x] `validate_plan_graph` rechaza ausencia de `## Merge Regression Audit`
- [x] Ejemplo canonico pasa el validador actualizado
- [x] Template muestra valores formales en columna Paralelizable
- [x] `ruff check .` exit 0
- [x] `pytest` suite verde (1075/1075)
- [x] Sin dependencias nuevas (stdlib-only)