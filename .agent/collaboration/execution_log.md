# Execution Log: WOT-2026-010i - Review packet hardening

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010i
- **Contract ID:** T-010I-001
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010e` cerro canonicamente y dejo fallos de review convertidos en
  aprendizaje reutilizable.
- `WOT-2026-010q` ya exige suite canonica real al handoff.
- `WOT-2026-010l` queda bloqueado hasta cerrar este hardening.

## Fase 0 - COMPLETADA

### Seams confirmados

- **Scope/handoff:** `run_guard()` en `scripts/pre_handoff_guard.py:573` orquesta
  todas las barreras. Lee diff via `get_changed_files()`, scope via
  `parse_files_likely_touched()`.
- **Parser FLT canonico:** vive en `.agent/scope_gate.py` (NO en
  `scripts/scope_gate.py` como dice el FLT — ver desviacion abajo).
  `_extract_section_paths(lines, heading, project_root)` ya extrae rutas de
  cualquier seccion markdown por heading. **No existe parser de Forbidden
  Surfaces** — hay que anadirlo reutilizando ese helper.
- **Commit visible:** NO existe barrera de commit-visible por ticket. El guard
  actual verifica work_plan committed (`assert_work_plan_committed`) y suite
  canonica, pero no que el commit productivo mencione el ticket_id. Hay
  `git_log_recent_files()` en scope_gate como referencia de patron git-log.
- **`_resolve_destino()`:** `scripts/encoding_post_write_hook.py:46`. Contrato
  correcto: lee `destination_root` de `motor_destination_link.json` (linea 54),
  no `motor_root`. Prioriza env `AGENT_PROJECT_ROOT`. Devuelve `Path|None`.
- **Tests existentes:** `tests/test_pre_handoff_guard.py` (41 tests, sin
  forbidden/commit-visible). `tests/unit/test_scope_gate.py`,
  `test_check_deliverables_exist.py`, `test_encoding_post_write_hook.py` vivos.

### Decisiones de implementacion por barrera

1. **Forbidden Surfaces:** anadir `parse_forbidden_surfaces(content, *, root)` en
   `.agent/scope_gate.py` reutilizando `_extract_section_paths`. Consumirla en
   `run_guard()` tras la deteccion de dirty_files: si un changed file resuelve a
   una ruta Forbidden, bloquear con `forbidden_surface_violation` nombrando la
   ruta.
2. **Commit visible code/mixed:** anadir `assert_ticket_commit_visible()` en
   `pre_handoff_guard.py`. Para deliverable_type code/mixed, busca el ticket_id
   en los mensajes de los ultimos N commits del repo_motor. Si no aparece y el
   arbol no tiene el commit → bloquea con remediacion. Doc-types se eximen
   (reutiliza `_SUITE_REQUIRED_TYPES = {code, mixed}` como criterio).
3. **Test semantico `_resolve_destino`:** la funcion ya es correcta; anadir test
   en `test_encoding_post_write_hook.py` con link donde
   `destination_root != motor_root` y afirmar que retorna `destination_root`.

### Desviacion de scope (CEM)

- **FLT declara `scripts/scope_gate.py`; el archivo real es `.agent/scope_gate.py`.**
  El parser FLT/Forbidden vive en `.agent/scope_gate.py`. Tocar ese archivo es
  necesario para cumplir el contrato (parser de Forbidden Surfaces reutilizable).
  Justificacion: el FLT nombra el modulo logico por su rol; la ruta fisica
  canonica es `.agent/scope_gate.py` (confirmado por glob). No es scope creep:
  es el mismo modulo que el contrato pretende endurecer. Registrado antes de
  tocarlo, segun regla de whitelist operativa.
- `scripts/scope_gate.py` no existe en el repo; no se crea un duplicado.
- **Resolucion (confirmada con usuario):** enmendar el FLT del work_plan.md para
  que diga `.agent/scope_gate.py`, implementar el parser reutilizable ahi, y
  mantener `pre_handoff_guard.py` como consumidor. FLT enmendado antes del
  cambio productivo para evitar scope-override en handoff.

## Fase 1 - Implementacion COMPLETADA

### Barreras producidas (repo_motor, commit `fdd55b6`)

1. **Forbidden Surfaces ejecutable**
   - `.agent/scope_gate.py::parse_forbidden_surfaces()` (reutiliza
     `_extract_section_paths`; entradas conceptuales como `cache pytest` no
     generan falso positivo).
   - `scripts/pre_handoff_guard.py::check_forbidden_surfaces()` consumido en
     `run_guard()` seccion 5.b; bloquea nombrando la ruta.

2. **Commit visible code/mixed**
   - `scripts/pre_handoff_guard.py::assert_ticket_commit_visible()`; busca el
     ticket en los ultimos 20 commits del repo_motor. Doc-types exentos.
     Fail-closed ante fallo de git. Integrado en `run_guard()` seccion 2.c.

3. **Test semantico `_resolve_destino`**
   - `tests/unit/test_encoding_post_write_hook.py::
     test_resolve_destino_returns_destination_root_not_motor_root` afirma el
     valor exacto retornado + negativo `!= motor_root`.

4. **Test de fallback honesto**
   - Ya existia `test_check_subprocess_invokes_check_encoding_guard` (observa el
     efecto real de subprocess detectando BOM). No se anade duplicado cosmetico.

### Tests nuevos/modificados

- `TestForbiddenSurfacesBarrier` (3 tests: hit bloquea, no-hit pasa, conceptual
  no falso-positivo).
- `TestCommitVisibleBarrier` (4 tests: code sin commit bloquea, mixed con commit
  pasa, analysis exento, fallo git fail-closed).
- `test_resolve_destino_returns_destination_root_not_motor_root` (semantico).
- Helper `commit_ticket_marker` + `write_green_last_run(ticket_id=...)`: los
  tests e2e existentes ahora aterrizan un commit que nombra el ticket (refleja
  el flujo real de handoff). 9 llamadas actualizadas.

### Evidencia FAIL-sin / PASS-con (barrera Forbidden)

- CON FIX: `check_forbidden_surfaces` con un diff que toca
  `scripts/run_pytest_safe.py` (Forbidden) -> reporta `run_pytest_safe.py` ->
  BLOQUEA.
- SIN FIX: el flujo previo no consultaba Forbidden; el path solo habria sido
  `scope_discrepancy` (no bloqueante) -> handoff pasaria. Demostrado via script
  directo contra `pre_handoff_guard` (exit 0, assert verde).

### Gates ejecutados

- `python -m pytest tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py
  tests/unit/test_check_deliverables_exist.py
  tests/unit/test_encoding_post_write_hook.py -q`: **93 passed**
- `ruff check <8 archivos tocados>`: All checks passed
- `ruff format --check <8 archivos>`: all formatted (tras `ruff format`)
- `check_encoding_guard.py <doc + py + artefactos colaboracion>`: sin errores
- `run_pytest_safe.py --level all`: **2921 passed, 20 skipped, 0 failed** (5m32s);
  `level=all`, `args_mode=default_discovery`, `exit_code=0`,
  `tested_commit_sha=fdd55b6 == HEAD`
- `validate --json --project-root repo_destino`: 0 errors / 0 warnings (abajo)

### Desviacion de scope resuelta

- FLT enmendado: `scripts/scope_gate.py` -> `.agent/scope_gate.py` ANTES del
  cambio productivo. El diff productivo cae 100% dentro del FLT enmendado; no se
  necesita scope-override.

## Estado actual

- Current state: WOT-2026-010i READY_FOR_REVIEW