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
