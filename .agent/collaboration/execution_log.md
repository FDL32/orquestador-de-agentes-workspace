# Execution Log: WOT-2026-010k - Hotspots reales de suite

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-010k
- **Contract ID:** T-010K-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010j` cerro con baseline de performance reutilizable.
- `WOT-2026-010n` cerro resolviendo el gate de deliverables en `repo_motor`.
- Packet `010k` preparado para Builder con contrato re-scoped.

## Fase 0 - Diagnostico

Confirmado en codigo antes de editar (commit `repo_motor` `c7249b8`):

- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md` linea
  33-34 confirma los dos hotspots con tiempos `162.29s` (`test_scan_current_project`)
  y `61.99s` (`test_repo_has_no_live_retired_topology_terms`), ambos atribuidos
  a filesystem real (scan/`rglob`), no a `git/subprocess`.
- `tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project`
  (linea 487-510) llama `scan_project(project_root)` **dos veces completas**
  sobre el repo real solo para comparar `result == result2` (determinismo).
  El coste real esta en `scan_project` (`scripts/project_scanner.py:615`):
  `rglob("*")` + `sha256_file` + `extract_imports` por archivo `.py`, sin
  estado mutable entre llamadas salvo el campo `generated` (que el propio
  test descarta antes de comparar). Repetir el escaneo completo del arbol
  real es 2x el coste de I/O para verificar una propiedad que no requiere
  reescanear el arbol completo dos veces.
- `tests/unit/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms`
  (linea 43-69) hace `rglob("*")` sobre todo `PROJECT_ROOT` y `read_text`
  completo de cada archivo no excluido. `EXCLUDED_PARTS` ya excluye
  `sandbox`, `.git`, caches, pero no filtra por extension salvo un set
  pequeno de binarios (imagenes); sigue leyendo cualquier `.json`, `.log`,
  `.xml` grande sin necesidad real, dado que el contrato observable es
  "no debe aparecer terminologia legacy retirada en archivos de texto vivos".
- Ninguno de los dos cambios propuestos elimina la API observable real: el
  primero sigue invocando `scan_project` sobre el repo real al menos una vez
  con las mismas aserciones de contenido; el segundo sigue leyendo el
  contenido real de todo archivo de texto plausible, solo evita leer
  binarios/extensiones irrelevantes que nunca podrian contener el patron.
- Existe barrera roja->verde viable: un test puede forzar temporalmente el
  shortcut a comportarse como antes (sin el filtro/optimizacion) y verificar
  que el smoke test lo detecta.
- Medicion before/after viable con el mismo comando focal (`pytest <test> -v`),
  mismo entorno local, mismo commit salvo el diff del ticket.

### Tiempos before (mismo entorno, commit `c7249b8`)

| Test | Comando | Tiempo before |
|------|---------|----------------|
| `test_scan_current_project` | `python -m pytest tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project -v -m slow` | `133.36s` |
| `test_repo_has_no_live_retired_topology_terms` | `python -m pytest tests/unit/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms -v` | `50.01s` |

Variacion esperada frente a los `162.29s`/`61.99s` de `010j` por diferencias
de entorno/carga de maquina entre mediciones; el orden de magnitud y el
hotspot dominante (filesystem real) se confirma igual.

### Razon de no tocar otros outliers en esta ronda

El contrato `T-010K-001` y el `work_plan.md` activo limitan el alcance a
estos dos tests (los dos hotspots de mayor tiempo wall-clock identificados
por `010j`, ~46.8% del tiempo total de suite). Otros outliers menores
(`59.22s`, `27.34s`, etc.) no estan priorizados por este ticket; mezclarlos
aqui seria re-scope no autorizado y diluiria la medicion before/after de los
dos hotspots contractuales.

## Fase 1 - Implementacion

### Hotspot 1: `test_scan_current_project`

- Se elimino la segunda llamada `scan_project(project_root)` y la
  comparacion `result == result2` en
  `tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project`.
  Esa propiedad de determinismo ya esta cubierta de forma barata por
  `test_scan_project_deterministic` (fixture sintetica `tmp_path`, 3
  archivos), por lo que repetirla a escala del repo real era coste
  redundante sin cobertura nueva.
- Se preservaron intactas todas las aserciones de contenido real
  (`total_files > 100`, categoria `python`, `importMap`), que son el
  contrato observable real del test.
- No se toco `scripts/project_scanner.py` ni `scan_project`.

### Hotspot 2: `test_repo_has_no_live_retired_topology_terms`

- Diagnostico medido en codigo (no relato): `PROJECT_ROOT.rglob("*")` no
  puede podar subarboles; aunque `EXCLUDED_PARTS` incluye `"sandbox"`,
  `rglob` igual desciende a `tests/sandbox/test_runtime/` completo antes de
  que `_is_excluded` lo descarte. Medicion aislada confirmo
  `tests/sandbox/` solo = `383706` entradas, contra `518` archivos reales
  que sobreviven el filtro (>99.8% de la enumeracion se descartaba sin
  usarse).
- Se sustituyo `rglob("*")` por un helper nuevo `_iter_candidate_files(root)`
  basado en `os.walk` con poda in-place
  (`dirnames[:] = [d for d in dirnames if d not in EXCLUDED_PARTS]`), que
  evita descender a los directorios excluidos en lugar de enumerarlos y
  descartarlos.
- `_is_excluded(relative_path)` se mantiene como segundo filtro tras la
  poda (cubre `EXCLUDED_PATHS`, archivos exactos no podables a nivel de
  directorio). El resto del contrato (extensiones binarias excluidas,
  lectura real de contenido, regex `LEGACY_PATTERN`, mensaje de asercion)
  no cambio.

### Documentacion

- Creado `docs/test_performance/test_performance_followup_WOT-2026-010k.md`
  con diagnostico, cambio, before/after y no-goals respetados para ambos
  hotspots.

### Desvio de scope

- Ninguno. Cambios limitados a los dos archivos de test declarados en el
  FLT, mas el reporte de follow-up contractual.

## Fase 2 - Tests

Anadidos a `tests/unit/test_no_legacy_topology_terms.py` (helper/fixture
nueva = `_iter_candidate_files`):

- `test_iter_candidate_files_smoke_no_shortcut`: compara el resultado de
  `_iter_candidate_files` contra `rglob("*")` sin poda + filtro
  `_is_excluded` sobre el mismo arbol sintetico; exige el mismo conjunto de
  archivos. Prueba que la poda es optimizacion de rendimiento, no cambio de
  comportamiento.
- `test_iter_candidate_files_does_not_descend_into_excluded_dirs`: smoke
  test SIN el shortcut (via `monkeypatch.setattr` vaciando
  `EXCLUDED_PARTS`), confirma que sin la poda el archivo del directorio
  excluido SI aparece — prueba que la poda (y no otra cosa) es la causa de
  su ausencia en el resultado real.

`test_scan_current_project` no requirio fixture/helper nueva (solo
eliminacion de codigo redundante), por lo que no aplica el requisito de
smoke test para esa parte.

## Quality Gates

Comandos ejecutados y salida real (`repo_motor`, commit base `c7249b8`):

- `python -m pytest tests/unit/test_project_scanner.py tests/unit/test_no_legacy_topology_terms.py -v`
  -> `39 passed in 52.61s`.
- `ruff check tests/unit/test_project_scanner.py tests/unit/test_no_legacy_topology_terms.py`
  -> `All checks passed!`.
- `uv run ruff format --check tests/unit/test_project_scanner.py tests/unit/test_no_legacy_topology_terms.py`
  -> inicialmente `1 file would be reformatted`; aplicado `ruff format`,
  reverificado `2 files already formatted` (exit 0); tests re-corridos
  post-formato, siguen verdes.
- `python scripts/run_pytest_safe.py --level all` -> `2910 passed, 20
  skipped in 373.01s (0:06:13)` (8 tests nuevos respecto a la baseline de
  `2902` de `010j`/`010n`).
  - `last-run.json` (autoridad real, no wrapper/pipe): `exit_code: 0`,
    `status: finished`, `tested_commit_sha` == HEAD `c7249b8` (working tree
    con el diff del ticket sin commitear al momento de la corrida).
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  -> `0 errors / 0 warnings` (ver seccion final de este log).

## Medicion before/after (mismo comando focal, mismo entorno, mismo commit base)

| Test | Comando | Before | After | Delta |
|------|---------|--------|-------|-------|
| `test_scan_current_project` | `pytest tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project -v -m slow` | `133.36s` | `52.73s` | `-80.63s` (`-60.5%`) |
| `test_repo_has_no_live_retired_topology_terms` | `pytest tests/unit/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms -v` | `50.01s` | `0.22s` | `-49.79s` (`-99.6%`) |
| **Total ambos** | — | `183.37s` | `52.95s` | `-130.42s` (`-71.1%`) |

Detalle completo en
`docs/test_performance/test_performance_followup_WOT-2026-010k.md`.

## Criterios Binarios — verificacion

- [x] Solo optimiza `test_scan_current_project`,
      `test_repo_has_no_live_retired_topology_terms` o sus fixtures
      directas. Verificado: diff limitado a esos dos archivos de test mas
      el reporte de follow-up.
- [x] La optimizacion se centra en filesystem/scan o setup repetido; no
      reabre `git/subprocess`. Verificado: ambos costes eran de filesystem
      real (escaneo redundante y enumeracion sin poda), medido en codigo.
- [x] Mantiene tests de contrato que validan comportamiento real cuando ese
      comportamiento es la API observable. Verificado: las aserciones de
      contenido real de `test_scan_current_project` se preservaron
      intactas; el segundo hotspot sigue leyendo contenido real de todo
      archivo de texto no excluido.
- [x] Cada helper/fixture nueva (`_iter_candidate_files`) queda cubierta
      por smoke test sin shortcut. Verificado:
      `test_iter_candidate_files_does_not_descend_into_excluded_dirs`.
- [x] Demuestra mejora con medicion before/after bajo condiciones
      comparables, mismo comando focal, mismo entorno, mismo commit salvo
      el diff del ticket. Verificado: tabla arriba.
- [x] No reduce cobertura semantica ni introduce falso-verde. Verificado:
      suite focal 39/39 verde, suite canonica completa 2910 passed (8 mas
      que la baseline previa por los smoke tests nuevos), 0 regresiones.
- [x] `validate --json --project-root <repo_destino>` termina con 0
      errors / 0 warnings al handoff. Verificado abajo.

## Saneamiento post-review (segunda pasada)

Manager senalo dos hallazgos antes de aprobar:

1. **ALTO — FLT no coincide con el diff real:** `work_plan.md` (Objetivo y
   FLT) citaba `tests/test_project_scanner.py` y
   `tests/test_no_legacy_topology_terms.py`, rutas obsoletas heredadas del
   prompt de lanzamiento. El commit real `55d84bb` toca
   `tests/unit/test_project_scanner.py` y
   `tests/unit/test_no_legacy_topology_terms.py` (confirmado via `find`
   antes de editar, en su momento). Corregido: `work_plan.md` Objetivo y
   FLT actualizados a `tests/unit/...`, con nota explicando la discrepancia
   y su origen.
2. **MEDIO — `validate --json` no estaba en 0/0 real:** quedaban 3
   warnings: `Out of scope (motor): .agent\runtime\events\events.jsonl`
   (artefacto runtime gitignored, no productivo) y dos
   `contaminacion_productiva (repo_destino)` por
   `AUDIT_WOT-2026-010n.md`/`STRATEGY_WOT-2026-010n.md`. Investigado: estos
   dos archivos ya habian sido movidos por el archivador a
   `_archive/plan_audit/` pero ese movimiento nunca se commiteo, dejandolos
   como diff uncommitted en `repo_destino` (mismo patron que `f4b235d` y
   `20151da`: "archival left uncommitted at closeout"). Corregido: commit
   `64ed1c4` reconcilia el movimiento de archivado, ajeno al scope de
   `010k` pero bloqueante para su `validate` limpio.

### Validate final

`python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
tras el saneamiento: `{"errors": {...todo []...}, "warnings": {}}` — 0
errors / 0 warnings real, sin el warning residual de `events.jsonl` (el bus
de `repo_motor` quedo commiteado limpio en `8e83b3d` tras la creacion final
del checkpoint M3 y el handoff).

### Suite canonica re-verificada post-saneamiento

`python scripts/run_pytest_safe.py --level all` -> `2910 passed, 20 skipped
in 324.63s`. `last-run.json`: `exit_code: 0`, `status: finished`,
`tested_commit_sha` == HEAD `17f41a4` en el momento de esa corrida (working
tree limpio). Una corrida intermedia mostro 6 fallos en
`test_manager_review_bridge.py`/`test_review_bridge.py`; investigado y
confirmado como acoplamiento de entorno preexistente (esos tests ejecutan
el evidence-gate real contra el `repo_destino` real via
`motor_destination_link.json`, no mockeado, y son sensibles al estado de
git de `repo_destino` en el momento exacto de la corrida) — reproducido
incluso revirtiendo temporalmente esos archivos de test al commit baseline
`c7249b8`, y resuelto sin tocar codigo al re-correr con el repo_destino en
estado estable. No es una regresion introducida por `010k`.

Checkpoint M3 final: tag `checkpoint/review-WOT-2026-010k` -> commit
`dd09199` (penultimo HEAD antes del commit final de bus `8e83b3d`, que solo
registra el propio evento de `--mark-ready` y no requiere nuevo
checkpoint).

Scope override: WOT-2026-010k deliverable lives in repo_motor. Affected files: tests/unit/test_no_legacy_topology_terms.py, tests/unit/test_project_scanner.py

Manager approved canonical closeout for WOT-2026-010k