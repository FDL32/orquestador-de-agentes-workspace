# Execution Log: WOT-2026-009a - Pre-Builder contract gate deliverable-aware

## Metadata

**Estado:** READY_FOR_REVIEW
- **ID:** WOT-2026-009a
- **Contract ID:** T-009A-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD: ece7524
- Destino HEAD: 46389d0
- Validate previo: 0 errors / 0 warnings (estado limpio tras 008a COMPLETED)
- work_plan.md: APPROVED (creado en este arranque)

## Implementacion (Builder)

### Cambios en repo_motor (commit 440e878)

**`.agent/scope_gate.py`**
- Extrae `_extract_section_paths(lines, heading, project_root)` como helper reutilizable.
- Añade `_DOC_DELIVERABLE_TYPES = frozenset({"analysis", "documentation", "research"})`.
- `parse_files_likely_touched` ahora acepta `deliverable_type="code"` (kw-only).
  Para doc types: si no hay `## Files Likely Touched`, parsea `## Builder` como fallback.
- `check_scope_gate` acepta `deliverable_type="code"` y lo pasa al parser fn.

**`.agent/agent_controller.py`**
- Wrapper `parse_files_likely_touched`: lee `deliverable_type` con `_read_deliverable_type` y lo pasa a scope_gate.
- Wrapper `check_scope_gate`: lee `deliverable_type` y lo pasa a scope_gate.

**`tests/unit/test_scope_gate_deliverable_aware.py`** (nuevo)
- 9 tests de barrera: negativo backward-compat, 5 positivos doc types, 2 negativos code/mixed, 1 FLT priority.

**`prompts/orchestrator_pipeline.md`**
- Sección `## 3.b Pre-Builder preflight gate` documentando validate 0/0 como gate fail-closed antes del Builder.

**`prompts/launch_builder.md`**
- Sección `## Preflight (WOT-2026-009a)` indicando que Builder no arranca si preflight no pasó 0/0.

### Gates ejecutados

- `ruff check`: exit 0 (pre-commit pass)
- `ruff format`: exit 0 (pre-commit pass)
- `pytest tests/unit/test_scope_gate_deliverable_aware.py`: 9/9 passed
- `python scripts/run_pytest_safe.py`: exit 0 (suite completa)
- `python scripts/check_encoding_guard.py prompts/orchestrator_pipeline.md prompts/launch_builder.md`: exit 0
- Motor commit: 440e878

### Validate final

```
python .agent/agent_controller.py --validate --json --project-root <destino>
```

### Validate final

- Motor validate: 0 errors / 0 warnings (exit 0)
- Destino validate: 0 errors / 1 warning (bus_drift: no STATE_CHANGED event para WOT-2026-009a)
  - Warning esperado: delivery_authority=repo_motor; el bus del destino no recibe eventos del motor.
- Motor git status: limpio (git status --short = empty)
- Motor HEAD: 440e878

Reporte final: Artefacto motor 440e878. Validate motor: exit code 0, 0 errors, 0 warnings.


Scope override: delivery_authority=repo_motor; rutas FLT relativas al motor resuelven en destino como inexistentes; diff real del motor valida contra work_plan del motor (commit 440e878, pre-commit green). Affected files: .agent/agent_controller.py, .agent/scope_gate.py, prompts/launch_builder.md, prompts/orchestrator_pipeline.md, tests/unit/test_scope_gate_deliverable_aware.py
## CHANGES fixes (B1/B2/B3)

### B1 — bus_drift
- `--mark-ready --force --scope-override` ejecutado: emitio STATE_CHANGED READY_FOR_REVIEW al bus del destino.
- Validate destino post-mark-ready: 0 errors / 1 warning scope.
- Warning scope residual ESPERADO: delivery_authority=repo_motor; el diff del destino toca solo
  archivos de colaboracion (execution_log, work_plan, STATE, TURN) que estan en la excludelist del
  scope gate por diseno. El gate autoritativo es el del motor (0/0). No es un bug — es el limite
  de diseno del scope gate del destino para tickets repo_motor.

### B2 — callsites adicionales de parse_files_likely_touched
- Linea ~1549 (_check_implementation_evidence best-effort check): parcheada.
- Linea ~3494 (staging/mark-ready path): parcheada.
- Motor commit: 9b7666f. Ruff + suite green.

### B3 — preflight enforcement
- orchestrator_pipeline.md seccion 3.b: claim explicitado como "protocolo de prompt obligatorio";
  enforcement runtime en launcher/supervisor es follow-up, no deliverable de este ticket.
- Motor commit: 9b7666f.

### Validate final B1/B2/B3

- Motor validate: 0 errors / 0 warnings (exit 0) — gate autoritativo.
- Motor git status: limpio (9b7666f clean).
- Destino validate: 0 errors / 1 warning scope (esperado, delivery_authority=repo_motor).
- Motor HEADs: 440e878 (feat) + 9b7666f (fix CHANGES).

Reporte final: Motor commits 440e878 + 9b7666f. Motor validate: exit code 0, 0 errors, 0 warnings.
