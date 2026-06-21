# execution_log.md -- WOT-2026-010m
## Metadata
- **Ticket:** WOT-2026-010m
**Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-010m.
- Motivo: `010x` ya cerro canonicamente; `011e` completo desbloqueo el consumo real de `pytest-xdist`; `011i` sigue prematuro porque cambiar el default del runner requiere antes validar un piloto CI acotado; el usuario pidio preparar `010m` como siguiente ciclo.
- Contrato congelado: `T-010M-001`.
- Frontera fijada antes de Builder: workflow `quality-gates.yml` + barrera `tests/unit/test_quality_gates_workflow.py`; tocar el runner, el guard de handoff o convertir xdist en default dispara `CONTRACT_GAP`.
## Premise Re-check requerido al Builder
- Releer `.github/workflows/quality-gates.yml`, `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `docs/test_performance/test_performance_baseline_WOT-2026-010j.md` y `docs/test_performance/test_performance_followup_WOT-2026-010k.md`.
- Confirmar que `quality-gates.yml` aun no usa `--xdist-workers`, que `011e` quedo cerrado y que el cierre canonico sigue exigiendo `python scripts/run_pytest_safe.py --level all`.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de empezar la implementacion.
## Restriccion cross-ticket
- `010m` consume la capacidad xdist creada por `011e`, pero no reabre `scripts/run_pytest_safe.py`, no mueve el default del runner (`011i`) y no toca otros workflows.
- Si los tests no parallel-safe exigen redisenar el selector/runner o aislar superficies fuera del workflow y su barrera, el resultado correcto es `CG-WOT-2026-010m.md`.
## BUILDER - WOT-2026-010m - Piloto CI xdist aditivo

### Fase 0 - Baseline + condicion de reactivacion
- Ticket estaba deferred con Reactivation condition:011e-estable-y-barrera-state-leak-verde. VERIFICADO: 011e COMPLETED (motor 27fe28f), pero su cierre documenta 3 tests no-parallel-safe (flakes bajo xdist). CONSECUENCIA DE DISENO: el piloto CI debe ser NON-BLOCKING, porque correr xdist sobre el subset unit con esos 3 flakes fallaria no-deterministamente. El AUDIT lo respalda ("rechazar redisenar runner por los no-parallel-safe; dejar piloto acotado").
- .github/workflows/quality-gates.yml: paso "Run Pytest Safe" corre run_pytest_safe.py serial sin args (canonico). tests/unit/test_quality_gates_workflow.py NO existia (creado).
- run_pytest_safe.py + pre_handoff_guard: contrato xdist (011e) y exigencia --level all (cierre) confirmados intactos, NO tocados.

### Fase 1 - Piloto (aditivo, non-blocking)
- Nuevo paso "Run Pytest (xdist pilot, non-blocking)" en quality-gates.yml: `uv run python scripts/run_pytest_safe.py --level unit --xdist-workers auto` con `continue-on-error: true`. Reutiliza el seam opt-in de 011e. El paso canonico "Run Pytest Safe" (serial, sin xdist, bloqueante) queda INTACTO. Resto del workflow sin cambios. YAML valido (yaml.safe_load); encoding 0.

### Fase 2 - Barreras (tests/unit/test_quality_gates_workflow.py, 5 tests)
- test_xdist_pilot_exists / _is_non_blocking / _pilot_uses_runner: exigen el piloto (--xdist-workers + continue-on-error true + via run_pytest_safe).
- test_canonical_serial_run_still_exists / _canonical_run_is_not_continue_on_error: protegen que el canonico NO adopte xdist ni se ablande a non-blocking.
- Verificacion FAIL-sin/PASS-con: revertido workflow a HEAD -> 3 barreras del PILOTO FAIL (No xdist pilot step); restaurado -> 5 passed. Las 2 barreras del canonico pasan en ambos estados (protegen, no son la barrera del piloto) -> reportadas aparte.

### Separacion piloto CI vs cierre canonico (auditable)
- Piloto CI = observacion non-blocking de xdist en quality-gates.yml; NUNCA falla el job ni es gate.
- Cierre canonico = run_pytest_safe --level all serial (sin xdist), validate 0/0, mark-ready con eventos. xdist NO entra en el camino canonico (sigue siendo 011i convertir default).

### Gates
- Tests focales: `python -m pytest tests/unit/test_quality_gates_workflow.py -q` -> 5 passed in 0.13s.
- Ruff: All checks passed! | Ruff format: 1 file already formatted | Encoding (workflow+test): exit 0.


Manager approved canonical closeout for WOT-2026-010m
## BUILDER - WOT-2026-011h - Barrera de archivado tambien en mark-ready

### Fase 0 - Premise re-check (read-only)
- 011a COMPLETED (commits 4532d1a fail-closed closeout uncommitted rename, 28bc7f4 non-zero/timeout) y 011d COMPLETED (28bbe85) verificados via git log.
- Relectura: `_auto_archive_closed_artifacts()` (controller L1013) mueve PLAN_/AUDIT_/STRATEGY_ con shutil.move SIN commit; `_handle_mark_ready()` (L2767) lo invoca en L3144 DESPUES del pre_handoff_guard y ANTES de _sync_mark_ready_targets (READY_FOR_REVIEW). El detector estable `check_archive_rename_complete` (reason `archive_rename_uncommitted`) ya existe en scripts/delivery_hygiene_check.py y lo reusa pre_handoff_guard L935. CONFIRMADO el hueco: el guard pre-handoff corre ANTES del archivado de mark-ready, no atrapa el limbo que mark-ready crea.
- validate --json: errors=0 warnings=0.

### Fase 1 - Fix (fail-closed, sin auto-commit)
- Nuevo helper `_check_mark_ready_archive_rename()` en controller: carga el detector canonico desde _MOTOR_ROOT/scripts/delivery_hygiene_check.py y corre `check_archive_rename_complete(PROJECT_ROOT)`. Devuelve None si limpio o no hay .git; dict con reason estable `archive_rename_uncommitted` (origen+destino+comando reconcile) si limbo; reason `archive_rename_guard_error` fail-closed si el detector no carga/ejecuta (paridad con pre_handoff_guard).
- Insertado en `_handle_mark_ready` entre el archivado (L3144) y _sync_mark_ready_targets: si bloquea, imprime diagnostico y `return 1` ANTES de emitir READY_FOR_REVIEW. NO auto-commit: solo expone el comando reconcile.

### Fase 2 - Barreras (ruta real de mark-ready, no helper aislado)
- 3 tests nuevos en TestExternalMotorCheckpointTopology, todos via `_handle_mark_ready` real con topologia motor+workspace real (git tmp):
  - test_mark_ready_blocks_when_archive_leaves_uncommitted_rename: parchea _auto_archive para crear el limbo real (D old + ?? new); exige code==1, reason `archive_rename_uncommitted`, origen+destino+comando reconcile, y que el rename siga SIN commitear (invariante no-auto-commit).
  - test_mark_ready_clean_archive_reaches_ready_for_review: archivado no-op -> code==0, sin falso positivo.
  - test_mark_ready_archive_guard_fails_closed_on_detector_error: fuerza fallo de carga del detector -> code==1 reason `archive_rename_guard_error`.
- Helper `_seed_archival_detector(motor_repo)` copia el detector real al motor temp (mark-ready lo resuelve desde _MOTOR_ROOT). Aplicado tambien a los 3 tests existentes de mark-ready que parchean _MOTOR_ROOT, que de otro modo bloquearian (correctamente) por fail-closed.
- Verificacion FAIL-sin/PASS-con: revertido controller a HEAD -> test_..._blocks FALLA (mark-ready alcanza READY pese al limbo); restaurado -> 3 passed.

### Gates
- `python -m pytest tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py -q` -> 177 passed.
- `ruff check` (4 archivos) -> All checks passed! | `ruff format --check` (4 archivos) -> 4 files already formatted | encoding -> exit 0.

### Fase 2b - Reparacion adicional (suite --level all destapo regresion fuera del FLT)
- La suite canonica --level all contra bd16e9d arrojo 3 failed (no solo passed; lectura literal del .log): tests/test_mark_ready_motor_scope.py (test_motor_commit_inside_flt_passes, _json_output, test_flt_not_resolved_against_destination).
- Causa identica a los 3 de test_agent_controller.py: parchean _MOTOR_ROOT a un motor temp sin scripts/delivery_hygiene_check.py, asi que el nuevo guard fail-closed (correctamente) bloquea con reason archive_rename_guard_error.
- Decision (no ablandar el guard): mantener fail-closed (alineado con "guard helper must fail-closed"; ablandarlo abriria un agujero si el detector desaparece del motor). En su lugar, sembrar el detector real en el helper centralizado `_monkeypatch_mark_ready` (cubre los 7 tests que lo usan). Los setattr directos (test_pre_handoff_still_commits_motor, test_dirty_tree_remains_blocked) no llegan al archivado y no requieren cambio.
- FLT-gap declarado: tests/test_mark_ready_motor_scope.py NO estaba en Files Likely Touched del contrato, pero es la misma ruta real de mark-ready que el cambio toca; repararlo es obligado para 0 failed. Se incluye en el commit.
- Verificacion: tests/test_mark_ready_motor_scope.py 14 passed; combinado motor_scope+agent_controller 124 passed; idempotency+manager_approve 32 passed (salen temprano por idempotencia, no llegan al guard). ruff/format/encoding del archivo: limpios.
