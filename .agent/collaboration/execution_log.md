# Execution Log: WOT-2026-010l - Selector focal por diff

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010l
- **Contract ID:** T-010L-001
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010j` dejo baseline durable de performance y definio el contexto de
  coste de suite.
- `WOT-2026-010i` cerro el hardening de packet/scope previo a introducir un
  atajo local de iteracion.
- `WOT-2026-010q` sigue siendo la barrera canonica de handoff full-suite.

## Fase 0 - COMPLETADA

### Preflight verificado

- `validate --json --project-root <repo_destino>`: 0 errors / 0 warnings.
- `STATE.md` -> `WOT-2026-010l` / `IN_PROGRESS`; `TURN.md` -> BUILDER / IMPLEMENT /
  `WOT-2026-010l`; `work_plan.md` activo apunta a `WOT-2026-010l`. Runtime
  bootstrappeado para este ticket; ninguna proyeccion anclada a ticket anterior.

### Seams confirmados (en codigo)

- **Diff real (seam canonico):** `.agent/scope_gate.py::get_changed_files(*,
  project_root, motor_root, run_fn)` (linea 322). Devuelve un `set[str]` de
  rutas absolutas resueltas, o `None` cuando no hay repo git. Ese `None` es la
  senal natural de fail-open: si no se puede leer el diff, se replega a suite
  canonica. NO se abre un parser git paralelo; el selector reutiliza este seam.
- **Args/target por defecto en runner:** `scripts/run_pytest_safe.py`:
  `parse_args()` (linea 337) usa `nargs=REMAINDER` para `pytest_args`;
  `pytest_args_mode()` (391) distingue `default_discovery` vs `explicit_args`;
  `default_test_target()` (395) = `tests/`; `normalize_pytest_args()` (409)
  aplica el filtro de `--level`. El selector focal entra como modo opt-in
  (flag nuevo) que produce `pytest_args` explicitos -> `args_mode=explicit_args`,
  por lo que NO puede satisfacer el handoff de 010q por construccion.
- **Tests existentes:**
  - `tests/unit/test_run_pytest_safe.py`: cubre `pytest_args_mode` /
    `default_test_target` (default_discovery vs explicit_args).
  - `tests/test_pre_handoff_guard.py::TestCanonicalSuiteGreenGate`:
    `test_focal_level_unit_blocks`, `test_explicit_args_blocks`,
    `test_canonical_suite_passes_all_fields` ya prueban que una corrida focal o
    con args explicitos NO satisface el handoff. El no-regression de 010l se
    apoya en estas barreras vivas.
  - `tests/unit/test_run_gates_dispatch.py`: cubre dispatch por
    `deliverable_type` (no toca seleccion focal).

### Decision de mapeo archivo->tests

- Modulo nuevo `scripts/test_selection.py` (stdlib only), reutilizando
  `get_changed_files` para el diff. Mapeo conservador y auditable:
  - `tests/**/test_*.py` y `tests/**/*_test.py` cambiados -> se incluyen ellos
    mismos.
  - codigo bajo `scripts/<name>.py` -> heuristica de nombre: tests cuyo nombre
    contenga `<name>` (`test_<name>.py` / `<name>_test.py`) en `tests/`.
  - cualquier ruta que no resuelva a un test concreto y seguro -> NO se adivina;
    contribuye a fail-open si el set queda vacio.
- **Fail-open (replegar a suite canonica completa) cuando:**
  - `get_changed_files` devuelve `None` (git no disponible / diff falla);
  - hay cambios en archivos troncales: `pyproject.toml`, `pytest.ini`,
    `.agent/**` (config estructural que invalida un subset seguro);
  - el mapeo seguro no resuelve ningun test;
  - el conjunto resuelto es vacio.
  Cada repliegue devuelve una `reason` auditable (string), nunca pass-open
  silencioso.

### Integracion en el runner

- Flag opt-in `--select-from-diff` en `run_pytest_safe.py`. Cuando se pasa, el
  runner pide el subset a `test_selection`; si el selector replega, el runner
  imprime la razon y corre la suite canonica (sin args explicitos). El selector
  es ergonomia local: por construccion produce `explicit_args` cuando hay subset,
  asi que 010q sigue bloqueando ese run para `--mark-ready`.

### Desviaciones de scope

- Ninguna. Todos los archivos a tocar estan en Files Likely Touched.
  `scripts/test_selection.py` es archivo nuevo ya declarado en el FLT.
- `tests/unit/test_run_gates_dispatch.py` estaba en el FLT pero NO se toco: el
  selector focal no acopla con el dispatch por `deliverable_type`. Anadir un test
  ahi seria cosmetico (viola la rubrica test-util). El scope gate verifica
  pertenencia al FLT, no que todo el FLT se modifique; sin desviacion.

## Fase 1 - Implementacion COMPLETADA

### Entrega productiva (repo_motor)

1. **`scripts/test_selection.py` (nuevo)** — selector focal por diff, stdlib only.
   `select_focal_tests(*, project_root, motor_root, run_fn=None) -> SelectionResult`.
   Reutiliza `scope_gate.get_changed_files` (sin parser git paralelo). Mapeo
   conservable: test cambiado -> a si mismo; `scripts/<name>.py` -> tests cuyo
   nombre contiene `<name>`. Fail-open con `reason` auditable: `no_diff_available`,
   `empty_diff`, `structural_change` (`pyproject.toml`/`pytest.ini`/`.agent/**`),
   `no_safe_mapping`. Nunca pass-open silencioso.
2. **`scripts/run_pytest_safe.py`** — flag opt-in `--select-from-diff`;
   `resolve_focal_args()` + `apply_focal_selection()`. Un subset se anexa como
   args explicitos (`args_mode=explicit_args`), asi 010q sigue bloqueando el run
   para `--mark-ready`. `last-run.json` registra `focal_selection.{requested,
   fell_open,reason}`. Modo sin flag = identico al anterior (aditividad total).
3. **`docs/test_performance/test_selection_WOT-2026-010l.md`** — invocacion,
   mapeo, tabla de razones de fail-open y como detectar el repliegue.

### Evidencia FAIL-open / subset (script directo)

- `structural_change`: diff toca `pyproject.toml` -> `mode=fallback`,
  `reason=structural_change...`.
- subset: diff toca `scripts/run_pytest_safe.py` -> `mode=subset`,
  `tests=['tests/test_run_pytest_safe.py']` (reproducible).

## Fase 2 - Tests COMPLETADA

### Tests nuevos

- `tests/unit/test_run_pytest_safe.py` (barreras + positivo):
  - `test_selector_git_failure_falls_open` (diff falla -> fallback);
  - `test_selector_structural_change_falls_open[pyproject.toml|pytest.ini|.agent/x.py]`
    (archivo troncal -> fallback);
  - `test_selector_unmapped_change_falls_open` (sin mapeo seguro -> fallback);
  - `test_selector_empty_diff_falls_open` (diff vacio -> fallback);
  - `test_selector_safe_subset_is_reproducible` (positivo: subset reproducible);
  - `test_runner_resolve_focal_args_uses_real_selector` (invariante: subset XOR
    fallback, nunca pass-open silencioso, sobre el selector real);
  - `test_selection_module_uses_scope_gate_seam_not_parallel_parser`
    (anti-patron: reusa seam, no abre parser git).
- `tests/test_pre_handoff_guard.py::TestCanonicalSuiteGreenGate::
  test_focal_selector_run_does_not_satisfy_handoff` (no-regresion 010q: una
  corrida focal = `explicit_args` -> handoff sigue bloqueado).

### Gates ejecutados (comando exacto + resultado literal)

- `python -m pytest tests/unit/test_run_pytest_safe.py tests/test_pre_handoff_guard.py
  tests/unit/test_run_gates_dispatch.py -q` -> **70 passed in 55.62s**
- `ruff check <5 archivos tocados>` -> **All checks passed!**
- `ruff format --check <5 archivos>` -> **5 files already formatted**
- `check_encoding_guard.py <5 py + doc + 4 artefactos colaboracion>` -> exit 0,
  sin output (limpio).
- `validate --json --project-root <repo_destino>` -> **0 errors / 0 warnings**.
- `run_pytest_safe.py --level all` (suite canonica) -> **2932 passed, 20 skipped,
  0 failed in 347.05s (5m47s)**. `last-run.json`: `status=finished`,
  `exit_code=0`, `level=all`, `args_mode=default_discovery`,
  `tested_commit_sha=915d2be == HEAD`.

### Entrega (repo_motor)

- Commit productivo: `915d2be` (`feat(WOT-2026-010l): diff-driven focal test
  selector with fail-open to canonical suite`). El ticket aparece en el mensaje.
- M3 checkpoint: tag `checkpoint/review-WOT-2026-010l` sobre `915d2be`.
- 5 archivos: `scripts/test_selection.py` (nuevo), `scripts/run_pytest_safe.py`,
  `tests/unit/test_run_pytest_safe.py`, `tests/test_pre_handoff_guard.py`,
  `docs/test_performance/test_selection_WOT-2026-010l.md`.
