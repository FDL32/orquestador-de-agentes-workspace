# Execution Log: WOT-2026-009g - Pre-handoff work_plan commit guard

## Metadata

**Estado:** READY_FOR_REVIEW
- **ID:** WOT-2026-009g
- **Contract ID:** T-009G-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD: 869b920 (WOT-2026-008b cerrado/publicado)
- Destino HEAD: 303d313 (backlog 009g/010a debt)
- Validate previo: 0/0
- Causa raiz verificada: work_plan.md en LIVE_SURFACES_REL de pre_handoff_guard.py:39 y motor_checkpoint.py:35 (dos puertas)

## Implementacion

### Barrier pre-fix (VERIFICADO)
```
python -m pytest tests/unit/test_motor_checkpoint.py -x -q
# FAILED: AttributeError: module has no attribute 'assert_work_plan_committed'
# 1 failed in 0.34s
```

### Cambios realizados (motor HEAD: d245ba5)

- .agent/motor_checkpoint.py: helper assert_work_plan_committed() delegando en scope_gate.get_changed_files; detecta unstaged/staged/untracked/deleted; diag con uncommitted_work_plan:true + path + remediation
- scripts/pre_handoff_guard.py: puerta 1 - run_guard() invoca helper; bloquea con uncommitted_work_plan:True + remediation
- .agent/agent_controller.py: puerta 2 - _handle_pre_handoff invoca helper antes de 3 return 0 (docs bypass, motor auto-commit, idempotent); emite HANDOFF_BLOCKED al bus
- tests/unit/test_motor_checkpoint.py (NUEVO): 9 tests
- tests/test_pre_handoff_guard.py::TestWorkPlanCommitGuard: 3 tests integracion
- 5 test setups actualizados con precondicion correcta (commit work_plan.md)

### Quality Gates

```
ruff check .                                     # exit 0
python -m pytest [68 tests focales]              # 68 passed in 27.34s
python .agent/agent_controller.py --validate     # 0 errors / 0 warnings
```

### Criterios binarios

- [x] Helper assert_work_plan_committed en motor_checkpoint.py delegando en scope_gate.get_changed_files
- [x] pre_handoff_guard.py bloquea con uncommitted_work_plan:true + ruta + remediation
- [x] _handle_pre_handoff invoca helper antes de los 3 return 0 exitosos
- [x] work_plan.md SIGUE en ambas LIVE_SURFACES_REL
- [x] Barrera 008b: test_barrier_008b_false_green_is_closed PASS post-fix
- [x] Tests 4 estados porcelain: unstaged, staged, untracked, deleted
- [x] Test control: live surfaces dirty no bloquea
- [x] ruff exit 0, tests focales 68 passed, validate 0/0

## Commit motor

d245ba5 feat(WOT-2026-009g): add work_plan commit guard to pre-handoff


Scope override: 5 existing test setups updated to commit work_plan.md as required precondition by WOT-2026-009g new guard; all files are test files adjusting for the new behaviour enforced by the ticket. Affected files: .agent/agent_controller.py, .agent/motor_checkpoint.py, scripts/pre_handoff_guard.py, tests/test_agent_controller.py, tests/test_mark_ready_motor_scope.py, tests/test_pre_handoff_guard.py, tests/test_pre_handoff_motor_productive_changes.py, tests/test_pre_handoff_multirepo.py, tests/unit/test_motor_checkpoint.py
## Ronda 2 — Manager CHANGES (fail-closed)

Manager review WOT-2026-009g: CHANGES. 2 hallazgos.

### ALTO (corregido) — guard silenciaba fallos del helper
Causa: `except (ImportError, Exception): pass` en run_guard (copiado del
patron best-effort de 009c). Para un ticket que cierra falso verde, un
guard roto que pasa en silencio ES un falso verde.

Fix (motor 4b61b4b):
- pre_handoff_guard.run_guard: en excepcion del helper -> valid=False +
  work_plan_guard_error (sin silent pass).
- _handle_pre_handoff: wrap del helper; en excepcion -> bloquea +
  HANDOFF_BLOCKED(reason=work_plan_guard_error).
- 2 tests fail-closed nuevos (monkeypatch helper que lanza): ambas
  puertas bloquean.

### MEDIO (corregido) — validate no era 0/0
3 warnings, dos causas:
1. FLT scope: rutas `### repo_motor` con comentarios parenteticos inline
   no parseaban (patron conocido: FLT bare paths). Fix: rutas desnudas +
   notas separadas. Ademas declarados los 4 test files ajustados.
2. contaminacion_productiva PLAN/AUDIT_WOT-2026-008b.md: residuo del
   cierre de 008b (archivado a _archive/plan_audit sin commitear).
   Reconciliado en destino f4b235d (rename 100%, contenido identico
   verificado por diff vs HEAD).

Validate tras fix: 0 errors / 0 warnings (esperado tras recommit work_plan).

### Gates ronda 2
```
ruff check .                  # exit 0
python -m pytest [70 focales]  # 70 passed in 29.30s
```

Commit motor: 4b61b4b fix(WOT-2026-009g): fail-closed work_plan guard
