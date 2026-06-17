# Execution Log: WOT-2026-010o - Determinismo del evidence-gate en tests

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-010o
- **Contract ID:** T-010O-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010k` cerro canonico y dejo este follow-up identificado en backlog.
- El problema a resolver es de determinismo de tests, no de politica funcional
  del evidence-gate.

## Fase 0 - Completada

### Seam exacto confirmado en codigo

El acoplamiento NO esta en `bus/review_bridge.py` ni en `bus/evidence.py`: ambos
modulos ya estan limpiamente parametrizados por `project_root`/`motor_root`
(`Path`), y casi todas las instancias de `ReviewBridge(...)` en
`tests/test_manager_review_bridge.py` y `tests/test_review_bridge.py` usan
`project_root=tmp_path` (55+ call sites verificados). `runtime/motor_link.py`
tampoco tiene cache ni fallback a variables de entorno: lee
`project_root/.agent/config/motor_destination_link.json` exclusivamente, asi
que con `tmp_path` siempre resuelve `None`.

El seam real esta en `scripts/manager_review_bridge.py`:

- `_state_path()` (linea 81-82) y `_checkpoint_path()` (linea 85-86) llaman a
  `_project_root()` (linea 41-43), que delega en
  `runtime.project_root.resolve_project_root()`.
- `resolve_project_root()` (runtime/project_root.py linea 34) da precedencia
  absoluta a la variable de entorno `AGENT_PROJECT_ROOT` si esta seteada, y
  solo si no lo esta cae a derivar la raiz desde `__file__` (el propio
  `repo_motor`).
- `_tick()` (scripts/manager_review_bridge.py linea 506) llama a
  `_load_state()` -> `_state_path()` y, en su camino de exito, a
  `_save_state()` / `_save_checkpoint()` (lineas 582-583) -> escriben en
  `<AGENT_PROJECT_ROOT>/.agent/runtime/manager_bridge_state.json` y
  `bridge_checkpoint.json`.
- El objeto `ReviewBridge` que cada test pasa a `_tick(review=...)` SI esta
  aislado (`project_root=tmp_path`), pero `_tick()` no usa ese
  `review.project_root` para resolver el estado del bridge: usa las funciones
  modulo-nivel `_state_path()`/`_checkpoint_path()`, que ignoran por completo
  el `project_root` del objeto y leen/escriben donde apunte
  `AGENT_PROJECT_ROOT` en el proceso actual.

Existe ya un mecanismo de aislamiento explicito para este mismo problema
(`_setup_project_root(tmp_path)` + fixture `_restore_project_root`,
`tests/test_manager_review_bridge.py` linea ~3233-3240), pero esta aplicado
solo a los tests de checkpoint (`@pytest.mark.usefixtures("_restore_project_root")`
desde la linea ~3245). Los tests `test_tick_does_not_call_reconcile_state`
(linea 2929), `test_tick_detects_ready_for_review_without_reconcile` (linea
2991) y `test_tick_no_concurrent_state_error` (linea 3075) llaman a `_tick()`
sin fijar `AGENT_PROJECT_ROOT`, dejando la resolucion de
`_state_path()`/`_checkpoint_path()` a merced del valor que tenga el proceso
en ese momento.

### Por que el diff de `010k` quedo descartado como causa raiz

`010k` no toco `bus/review_bridge.py`, `scripts/manager_review_bridge.py` ni
estos tests. El seam descrito arriba es preexistente: cualquier corrida de
`run_pytest_safe --level all` ejecutada dentro de una sesion de dogfooding
real (donde el orquestador exporta `AGENT_PROJECT_ROOT` apuntando al
`repo_destino` activo, segun AGENTS.md "Regla de `AGENT_PROJECT_ROOT`") hace
que estos tres tests lean Y ESCRIBAN sobre
`repo_destino/.agent/runtime/manager_bridge_state.json` /
`bridge_checkpoint.json` reales, en vez de un fixture. Confirmado
empiricamente: con `AGENT_PROJECT_ROOT` sin definir en el proceso actual,
`python scripts/run_pytest_safe.py --level all` corrio limpio
(2910 passed, 20 skipped, 0 failed) en este mismo HEAD del motor — es decir,
el fallo NO es deterministico por codigo de `010k`, sino por el valor de esa
variable de entorno en el momento de la corrida, lo que coincide con el
patron de "6 fallos transitorios" observado durante `010k` (corrida dentro de
una sesion con `AGENT_PROJECT_ROOT` activo) vs. esta corrida aislada (sin esa
variable).

### Estrategia de desacoplamiento elegida

No hace falta cambiar la API publica del evidence-gate ni de
`scripts/manager_review_bridge.py`. La fuente del estado a inyectar es la
misma variable de entorno que el codigo de produccion ya consulta
(`AGENT_PROJECT_ROOT`), siguiendo el patron ya existente en
`_setup_project_root`/`_restore_project_root`:

- Extender el aislamiento ya probado (`_setup_project_root(tmp_path)` +
  `_restore_project_root`) a los tres tests de `_tick()` que hoy no lo usan,
  de forma que `_state_path()`/`_checkpoint_path()` resuelvan dentro de
  `tmp_path` en vez del valor ambiental real.
- No se requiere fixture de repo git temporal nueva para este sub-hallazgo:
  el seam de `_tick()` es de resolucion de archivos JSON de estado del
  bridge, no de evidencia git. Los casos `APPROVE`/`CHANGES` contra repo git
  controlado (via `tests/test_pre_handoff_guard.py::init_git_repo`, ya usado
  en `tests/test_review_bridge.py::TestReviewBridgeEvidence`) siguen siendo
  la via correcta para los tests que SI ejercitan `classify_review_packet`/
  `resolve_evidence` contra git real, y esos ya estan correctamente aislados.
- No se toca `bus/review_bridge.py`, `bus/evidence.py` ni
  `runtime/motor_link.py`: son production code ya bien parametrizado.

## Fase 1 - Implementacion

- Escaneo automatizado de todos los call sites de `_tick(`/`_bridge_heartbeat(`
  en `tests/test_manager_review_bridge.py` (unico archivo que importa
  `scripts.manager_review_bridge`; `tests/test_review_bridge.py` no usa ese
  modulo y no estaba expuesto a este seam).
- Encontrados 3 candidatos sin isolation aparente; 2 resultaron falsos
  positivos tras inspeccion (`test_bridge_heartbeat_includes_cursor_and_sequence`
  pasa un `BridgeState` construido a mano, sin tocar disco;
  `test_main_once_reads_state_from_disk_without_startup_reconcile` mockea
  `_tick` y `SequentialTicketSupervisor`/`ReviewBridge` completos, sin I/O real
  hacia `_state_path()`/`_checkpoint_path()`).
- Unico gap real: `test_tick_does_not_call_reconcile_state` (linea 2929)
  llamaba a `_tick()` sin `_mock_bridge_state_path(monkeypatch, tmp_path)`.
  Fix aplicado: una linea añadida al inicio del test
  (`tests/test_manager_review_bridge.py`).
- Verificacion empirica del seam: ejecutar el test con
  `AGENT_PROJECT_ROOT` apuntando al `repo_destino` real, antes y despues del
  fix. En ambos casos no se creo `manager_bridge_state.json` real porque el
  test fija `active_ticket=None` y `_tick()` retorna antes de llegar a
  `_load_state()` (linea 516-521) — el riesgo en este test especifico era
  latente, no activo, pero el fix es la higiene correcta y alinea el test con
  el patron ya usado en los otros 5 tests de `_tick()` del mismo archivo.
- No se creo fixture nueva de repo git temporal: la cobertura `APPROVE`/
  `CHANGES` contra repo controlado ya existe en
  `tests/test_review_bridge.py::TestReviewBridgeEvidence` (usa
  `tests/test_pre_handoff_guard.py::init_git_repo`), ejercitando el mismo
  codigo de clasificacion (`classify_review_packet`/`resolve_evidence`) que
  determina APPROVE vs REJECTED en produccion, sin tocar el `repo_destino`
  real.

## Gates ejecutados

- `python -m pytest tests/test_manager_review_bridge.py tests/test_review_bridge.py -v -k tick`:
  27 passed.
- `python -m pytest tests/test_manager_review_bridge.py tests/test_review_bridge.py -q`:
  193 passed.
- `ruff check tests/test_manager_review_bridge.py`: All checks passed.
- `python scripts/run_pytest_safe.py --level all` (baseline, antes del fix,
  con `AGENT_PROJECT_ROOT` sin definir): 2910 passed, 20 skipped, 0 failed.
- `python scripts/run_pytest_safe.py --level all` (baseline pre-commit,
  con `AGENT_PROJECT_ROOT` sin definir, HEAD 8e83b3d):
  2910 passed, 20 skipped, 0 failed — 42m47s.
- Commit productivo: `591bec5` — pre-commit hooks todos verdes.
- `python scripts/run_pytest_safe.py --level all` (post-commit, HEAD 591bec5,
  segunda pasada post-CHANGES): 2910 passed, 20 skipped, 0 failed — 5m44s.
  last-run.json: level=all, exit_code=0, tested_commit_sha=591bec5, status=finished.
- `validate --json`: 0 errors / 0 warnings.

### Nota: fix solo en capa de test, sin cambio de politica del evidence-gate

El unico archivo modificado es `tests/test_manager_review_bridge.py` (diff:
+5 lineas, una llamada a `_mock_bridge_state_path(monkeypatch, tmp_path)` en
`test_tick_does_not_call_reconcile_state`). No se toco ningun modulo de
produccion (`bus/review_bridge.py`, `bus/evidence.py`, `scripts/manager_review_bridge.py`,
`runtime/motor_link.py`) ni la politica funcional del evidence-gate
(APPROVE vs CHANGES). El `motor_destination_link.json` permanece intacto.

### Tiempo de suite (seguimiento para performance)

La corrida `--level all` con `AGENT_PROJECT_ROOT` sin definir tardo 42m47s
(2567s). La corrida `010k` tardo ~28min. La variacion puede reflejar carga
del sistema. Candidato para follow-up si se abre WOT sobre rendimiento de suite.

## Estado actual

- Current state: WOT-2026-010o READY_FOR_REVIEW

## Gates esperados

- `python -m pytest tests/test_manager_review_bridge.py tests/test_review_bridge.py -v`
- `python scripts/run_pytest_safe.py --level all`
- `ruff check <python_tocados>`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`


Manager approved canonical closeout for WOT-2026-010o