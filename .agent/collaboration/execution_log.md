# Execution Log: WOT-2026-010n - Gate de deliverables namespaced

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010n
- **Contract ID:** T-010N-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010j` aparcado via `CONTRACT_GAP` canonical:
  - archivo `contract_gaps/CG-WOT-2026-010j.md`
  - evento `CONTRACT_GAP` emitido en bus
- `T-010N-001` congelado en planning docs.
- Packet `010n` preparado para Builder.

## Fase 0 - Diagnostico

Seams confirmados en codigo (lectura directa, no relato):

- `scripts/check_deliverables_exist.py::extract_paths_from_work_plan` (pre-fix)
  escaneaba la seccion `## Files Likely Touched` igual que `## Deliverables`,
  con un solo `PROJECT_ROOT` global (`resolve_project_root()` o
  `TEST_PROJECT_ROOT`), sin ninguna logica de namespace. Las subcabeceras
  `### repo_motor` / `### repo_destino` solo se distinguian de
  `Read/inspect only` / `Manager-only` (que si se saltaban via
  `skip_subsection`); ambos namespaces FLT reales caian en la misma rama
  "subheader sin marcador de skip" y se resolvian contra `PROJECT_ROOT`
  (= `--project-root`, el repo_destino).
- `.agent/scope_gate.py::parse_flt_namespaced` ya resuelve esto
  correctamente: recibe `motor_root` y `project_root` por separado,
  bucketiza `### repo_motor` -> `motor_root`, `### repo_destino` ->
  `project_root`, y lineas planas (sin subcabecera) segun
  `delivery_authority` (via `read_delivery_authority`). Namespaces
  desconocidos (`### algo_raro`) se descartan (`ns == "unknown": continue`).
- `runtime/motor_link.py::resolve_motor_root(project_root)` es el resolver
  canonico de motor_root: lee
  `project_root/.agent/config/motor_destination_link.json`, devuelve
  `Path(motor_root)` si existe en disco, o `None` si el link no existe o el
  motor_root no existe.
- `scripts/pre_handoff_guard.py::parse_files_likely_touched` ya combina
  ambos: llama `scope_gate.parse_flt_namespaced(content, motor_root=...,
  project_root=..., delivery_authority=...)` y devuelve la union de ambos
  buckets. Es el patron de referencia que replique en el fix.
- `.agent/agent_controller.py::_check_declared_deliverables_exist` (linea
  ~1519) importa `extract_paths_from_work_plan` directamente (no subprocess)
  y resuelve cada path con `.exists()`. Se llama de forma incondicional
  desde `_check_implementation_evidence`, que el propio codigo etiqueta
  "WP-2026-188 Phase 4: Builder ready evidence gate (unconditional - not
  bypassable)". Confirmado empiricamente en el ciclo de `010j`: `--force` NO
  salta este chequeo.
- `Read/inspect only` y `Manager-only` nunca entran a
  `_parse_flt_section` (corta en `## ` no-`### `), por lo que sus bullets no
  se pueden confundir con deliverables Builder via el camino FLT. Esto se
  verifico con un test dedicado.

### Reproduccion del caso real de `010j`

- Comando real bloqueado (ciclo previo, en este mismo turno de sesion):
  `python .agent/agent_controller.py --mark-ready --project-root
  C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
- Deliverable real en `repo_motor`:
  `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
  (commit `c05dbfe`, 9438 bytes, verificado con `check_encoding_guard.py`
  exit 0).
- Resultado del gate (pre-fix): `Missing declared deliverables:
  C:\...\orquestador_de_agentes_workspace\docs\test_performance\test_performance_baseline_WOT-2026-010j.md`
  -- el gate buscaba el archivo dentro de **repo_destino**, no repo_motor.
  Codigo de salida: 1 (handoff bloqueado).
- Reproducido como test de regresion automatizado:
  `tests/unit/test_check_deliverables_exist.py::test_wot_010j_real_case_motor_deliverable_resolves_against_motor_root`.
  Confirmado rojo contra el codigo pre-fix (via `git stash` del archivo
  modificado) y verde post-fix.

### Desvio de scope

- Ninguno. El fix se limito a `scripts/check_deliverables_exist.py` y sus
  tests, exactamente las rutas declaradas en `### repo_motor` del FLT de
  este ticket.

## Fase 1 - Implementacion

- `scripts/check_deliverables_exist.py`:
  - Se añadio `resolve_motor_root()` (honra `TEST_MOTOR_ROOT` para tests;
    en produccion delega en `runtime.motor_link.resolve_motor_root(PROJECT_ROOT)`,
    con fallback a `PROJECT_ROOT` cuando no existe `motor_destination_link.json`
    -- caso motor-como-root / standalone).
  - Se separo `extract_paths_from_work_plan` en dos funciones: 
    `_extract_paths_from_generic_sections` (logica legacy intacta para
    `## Deliverables` / `must create` / `must modify`, sin concepto de
    namespace) y `_extract_flt_paths` (delega en
    `scope_gate.parse_flt_namespaced` + `scope_gate.read_delivery_authority`
    para resolver `### repo_motor` contra `motor_root` y `### repo_destino`
    / lineas planas contra `PROJECT_ROOT` segun `delivery_authority`).
  - No se toco el runner de pytest, politica de performance, ni closeout
    fuera del gate.
  - No se duplico el deliverable de `010j` en `repo_destino`.
  - El fix permanece fail-closed: rutas con namespace `unknown` se
    descartan (no se agregan como existentes ni se asumen resueltas);
    rutas declaradas inexistentes en el namespace correcto siguen
    bloqueando con diagnostico que incluye el path resuelto.

## Fase 2 - Tests

Añadidos a `tests/unit/test_check_deliverables_exist.py` (suite completa
8/8 verde, incluye los 3 tests legacy sin regresion):

- `test_wot_010j_real_case_motor_deliverable_resolves_against_motor_root`:
  reproduce el caso real de 010j (motor_root y destino_root separados via
  `TEST_MOTOR_ROOT`/`TEST_PROJECT_ROOT`); rojo pre-fix, verde post-fix.
- `test_namespaced_repo_motor_deliverable_passes`: deliverable real en
  `### repo_motor` resuelve y pasa.
- `test_namespaced_repo_destino_deliverable_passes_no_regression`:
  deliverable real en `### repo_destino` sigue pasando.
- `test_namespaced_repo_motor_missing_deliverable_fails_closed`: path
  namespaced inexistente sigue bloqueando (exit 1, mensaje con el nombre
  del archivo faltante).
- `test_read_inspect_only_and_manager_only_not_treated_as_deliverables`:
  confirma que `## Read/inspect only` y `## Manager-only` no se leen como
  deliverables Builder.

## Quality gates (evidencia real, no relato)

```
python -m pytest tests/test_pre_handoff_guard.py tests/unit/test_check_deliverables_exist.py -v
-> 46 passed in 13.82s

ruff check scripts/check_deliverables_exist.py tests/unit/test_check_deliverables_exist.py
-> All checks passed!

uv run ruff format --check scripts/check_deliverables_exist.py tests/unit/test_check_deliverables_exist.py
-> 2 files already formatted (after 1 reformat applied)

python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
-> {"errors": {... todas vacias ...}, "warnings": {}}
```

### Verificacion end-to-end del caso real (sin overrides de test)

Reproducida la invocacion real del controller (`AGENT_PROJECT_ROOT` seteado
a repo_destino, import directo de `extract_paths_from_work_plan`, sin
`TEST_MOTOR_ROOT`/`TEST_PROJECT_ROOT`) contra el `work_plan.md` activo de
`010n`: los 3 deliverables `### repo_motor` (incluido este mismo
`scripts/check_deliverables_exist.py`) y los 2 `### repo_destino`
resolvieron `True` (existen) contra sus roots correctos via
`motor_destination_link.json` real.

## Criterios Binarios (ver work_plan.md) - estado

- [x] Existe barrera de regresion roja->verde que reproduce el caso real de `010j`.
- [x] Deliverable Builder en `repo_motor` pasa el gate.
- [x] Deliverable Builder en `repo_destino` sigue pasando sin regresion.
- [x] Ruta namespaced invalida/missing falla cerrado con diagnostico (path + missing).
- [x] `Read/inspect only` / `Manager-only` ignorados como deliverables Builder.
- [ ] `WOT-2026-010j` puede cerrar canonicamente sin duplicar el reporte (pendiente: reintentar tras handoff de 010n).
- [x] `validate --json --project-root <repo_destino>` termina 0 errors / 0 warnings.
