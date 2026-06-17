# Execution Log: WOT-2026-010q - Suite canonica real en pre-handoff

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010q
- **Contract ID:** T-010Q-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010o` cerro canonico y dejo verificado el caso real:
  `last-run.json` debe tener `level="all"` y
  `args_mode="default_discovery"` para representar suite canonica.
- `WOT-2026-010l` queda pendiente hasta cerrar este guard.

## Fase 0 - COMPLETADA

### Seam exacto

- Funcion: `assert_canonical_suite_green` en `scripts/pre_handoff_guard.py:387-490`
- Valida actualmente: `status == "finished"`, `exit_code == 0`,
  `tested_commit_sha == HEAD`
- GAP confirmado: NO valida `level` ni `args_mode` (lineas 445-483)

### Campos de `last-run.json`

`run_pytest_safe.py` escribe desde el inicio del run (lineas 488-503):
- `level` (ej. `"all"`, `"unit"`)
- `args_mode` (ej. `"default_discovery"`, `"explicit_args"`)
- `status`, `exit_code`, `tested_commit_sha`

El schema ya existe; no se necesita cambiar el runner.

### Tests a extender

- `TestCanonicalSuiteGreenGate` en `tests/test_pre_handoff_guard.py:842`
- Helper `_write_last_run` (estatico, linea 851) — usado para tests barrera
- Helper `write_green_last_run` (linea 51) — escribe solo 3 campos actualmente;
  debe incluir `level="all"` y `args_mode="default_discovery"` para que
  `test_fresh_green_passes` y los tests de integracion sigan pasando
- Tests positivos existentes (ej. `test_guard_passes_clean_tree_with_m3:91`)
  llaman a `write_green_last_run` — si se actualiza ese helper, quedan cubiertos

### Plan de implementacion

1. Anadir validacion `level == "all"` y `args_mode == "default_discovery"` en
   `assert_canonical_suite_green` despues de la check de SHA
2. Actualizar `write_green_last_run` para incluir los dos campos nuevos
3. Anadir 3 tests barrera en `TestCanonicalSuiteGreenGate`:
   - `level="unit"` bloquea
   - `level="all"` + `args_mode="explicit_args"` bloquea
   - `level="all"` + `args_mode="default_discovery"` pasa (test positivo robusto)
4. Actualizar `test_fresh_green_passes` para usar los campos completos

## Fase 1 - Implementacion COMPLETADA

### Cambios producidos

**`scripts/pre_handoff_guard.py`** (repo_motor) — +24 lineas despues del check de SHA:
- Valida `level == "all"`: bloquea con `reason="not_full_suite (level=...)"` y
  remediacion `python scripts/run_pytest_safe.py --level all`
- Valida `args_mode == "default_discovery"`: bloquea con `reason="not_full_suite
  (args_mode=...)"` y misma remediacion
- `return True` ahora incluye `level` y `args_mode` en el diag

**`tests/test_pre_handoff_guard.py`** (repo_motor) — +103 lineas:
- `write_green_last_run`: ahora incluye `level="all"` y `args_mode="default_discovery"`
  para que todos los tests de integracion existentes sigan validos
- `test_fresh_green_passes`: actualizado con campos completos
- `test_focal_level_unit_blocks`: barrera rojo->verde (level=unit bloquea)
- `test_explicit_args_blocks`: barrera rojo->verde (level=all+explicit_args bloquea)
- `test_canonical_suite_passes_all_fields`: positivo con los 5 campos completos

### Gates ejecutados

- `python -m pytest tests/test_pre_handoff_guard.py -v`: 41 passed / 0 failed
- `ruff check scripts/pre_handoff_guard.py tests/test_pre_handoff_guard.py`: All checks passed
- Commit productivo: `849e7d52` (repo_motor main)
- `python scripts/run_pytest_safe.py --level all`: 2913 passed / 20 skipped / 0 failed
  (6m07s). `level=all`, `args_mode=default_discovery`, `exit_code=0`,
  `tested_commit_sha=849e7d52d4153a4904beb812f171c3281acccabb == HEAD`
- `validate --json --project-root repo_destino`: 0 errors / 0 warnings

## Estado actual

- Current state: WOT-2026-010q READY_FOR_REVIEW

## Nota de handoff

- Fix es exclusivamente en tests y guard de pre-handoff; no toca `run_pytest_safe.py`
  ni politica Builder/Manager ni schema de `last-run.json`
- Los 3 tests barrera prueban que el gate habria bloqueado el primer intento de
  handoff de WOT-2026-010o (que tenia level=unit)
