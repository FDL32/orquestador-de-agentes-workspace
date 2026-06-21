# Backlog (cola viva)

> Cola viva de tickets candidatos y en curso del workspace.
> NO es estado activo: el ticket activo vive en `work_plan.md`.
> Historico de tickets terminales: `.agent/collaboration/_archive/backlog_done.md`.
> Snapshot pre-corte WOT-2026-012a: `.agent/collaboration/_archive/backlog_pre_012a.md`.

## Politica

- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -- repo destino real.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` -- repo portable con `.git` propio.
- **Escritura:** humano o Manager; Builder solo lo toca si el plan lo pide explicitamente.
- **Contrato de cola viva (WOT-2026-012a):**
  - La tabla `Vista rapida` es la UNICA fuente parseable. No usar comentarios HTML como semantica obligatoria.
  - Estados permitidos en cola viva: `pending`, `blocked`, `deferred`, `ready-for-review`, `awaiting-manager`, `completed-partial`.
  - Estados terminales (`completed`, `done`, `closed`, `absorbed`) NO viven aqui: al cerrar, el Manager los mueve a `_archive/backlog_done.md` en un commit de documentacion (NUNCA via archivador del closeout/mark-ready).
  - Columna `Reactivation` obligatoria: `-` para estados activos sin trigger; `deferred`/`completed-partial`/`blocked` declaran trigger estructurado (`WOT-...`, `commit:<sha>`, `external:<ref>`, `condition:<slug>`).
  - `completed` solo cuando el bus confirma `STATE_CHANGED -> COMPLETED`; antes, usar `ready-for-review` o `awaiting-manager`.

## Vista rapida

| Prioridad | Ticket | Titulo | Scope | Estado | Depende de | Origen | Reactivation |
|-----------|--------|--------|-------|--------|------------|--------|--------------|
| Alta | WOT-2026-002c | A2d: eliminar copias motor-provides + ejecutar decisiones (FASE3 diferida) | system/host-extends | completed-partial | WOT-2026-002a, WOT-2026-002b | session-2026-06-13-host-extends | condition:install-sync-revendor-resuelto |
| Alta | WOT-2026-013d | Escaneo robusto de proyecto ante borrados concurrentes | motor/project-scan | pending | WOT-2026-013c | session-2026-06-21-013c-product-followup | - |
| Media | WOT-2026-013e | Auditar valor, uso y poda segura de la suite de tests | motor/test-suite-audit | pending | WOT-2026-013d | session-2026-06-21-test-suite-audit-followup | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> `013c` cerro como `blocked-final` (CG) y su follow-up correcto ya no es tests-only: `013d` recoge la cura en PRODUCTO sobre `project_scanner` / `project_paths`, con prueba xdist estable y limpieza determinista del sandbox volatil. `013e` queda registrado como auditoria transversal futura para inventariar valor, duplicidad y poda segura de la suite de tests, fuera del scope de `013d`. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013d - Escaneo robusto de proyecto ante borrados concurrentes
- **Prioridad:** Alta
- **Scope:** motor/project-scan
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013c
- **Reactivation:** -
- **Origen:** session-2026-06-21-013c-product-followup.
- **Problema (VERIFICADO):** `013c` demostro que el rojo xdist no nace en una familia aislable de tests, sino en el escaneo de PRODUCTO: `scripts/project_scanner.py` hace `rglob("*.py")` en `_collect_local_modules()` y `rglob("*")` en `scan_project()`, mientras `agent_system/scripts/project_paths.py` hace `rglob(".agent")` en `resolve_paths()`. Los tres recorridos pueden descender a `tests/sandbox/test_runtime/session_*` mientras otros workers borran subarboles, provocando `FileNotFoundError`/`Acceso denegado` antes del filtro de exclusion. Baseline verificado: `tests/sandbox/test_runtime` contiene `session_dirs=566`.
- **Objetivo:** volver robusto el escaneo de proyecto ante borrados concurrentes y ruido de sandbox volatil, sin tocar la politica del runner ni reabrir el default xdist. El entregable es producto + barreras de test que demuestren que el triple rojo historico queda estable bajo xdist.
- **Files Likely Touched:**
  - repo_motor: `scripts/project_scanner.py`
  - repo_motor: `agent_system/scripts/project_paths.py`
  - repo_motor: `tests/unit/test_project_scanner.py`
  - repo_motor: `tests/test_project_paths.py`
  - repo_motor: `tests/unit/test_detect_version.py`
  - repo_motor: `tests/unit/test_no_inline_ticket_regex.py`
  - repo_motor: `tests/conftest.py`
- **Criterios binarios:** los 3 puntos de escaneo verificados (`scripts/project_scanner.py` en `_collect_local_modules` y `scan_project`, `agent_system/scripts/project_paths.py` en `resolve_paths`) quedan robustos frente a subdirectorios que desaparecen durante la travesia; existe limpieza determinista del ruido en `tests/sandbox/test_runtime`, gestionada via fixture/harness en `tests/conftest.py` (el sandbox es efecto colateral controlado, no superficie de edicion manual), y el baseline/post queda registrado en `execution_log.md`; `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` queda verde en al menos 3 corridas consecutivas sobre el mismo host; `python -m pytest tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py -q`, `ruff` sobre Python tocado, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes; el diff productivo queda acotado a escaneo de producto + tests/fixtures declarados, sin tocar runner, CI ni default xdist.
- **STOP:** si la unica cura segura exige tocar `scripts/run_pytest_safe.py`, `quality-gates.yml`, CI o la politica default/opt-in de xdist; si la unica forma de estabilizar el triple verde exige mover el sandbox fuera del arbol o romper la invariante custodiada por `tests/unit/test_windows_safe_temp_runtime.py`; o si la reproduccion deja de concentrarse en las superficies declaradas y reaparece como deuda de runner/global-state ajena, parar y emitir `CG-WOT-2026-013d.md`.


### WOT-2026-013e - Auditar valor, uso y poda segura de la suite de tests
- **Prioridad:** Media
- **Scope:** motor/test-suite-audit
- **Estado:** pending
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013d
- **Reactivation:** -
- **Origen:** session-2026-06-21-test-suite-audit-followup.
- **Problema (HIPOTESIS A VERIFICAR):** la suite ya supera los 3000 tests y probablemente mezcla regresiones core, barreras estructurales, tests legacy y candidatos redundantes. Hoy no existe un inventario auditable que distinga "proteccion imprescindible" de "ruido historico" antes de proponer podas.
- **Objetivo:** producir un inventario razonado de la suite por familias y riesgo, clasificando cada bloque como `core regression`, `structural gate`, `legacy candidate`, `redundant candidate` o `unknown`, con evidencia suficiente para abrir tickets pequenos de poda sin borrar a ciegas.
- **Files Likely Touched:**
  - repo_motor: `tests/`
  - repo_motor: `scripts/run_pytest_safe.py`
  - repo_motor: `docs/test_performance/`
  - repo_destino: `.agent/collaboration/execution_log.md`
- **Criterios binarios:** existe inventario por familias con conteo y clasificacion; se listan tests lentos, saltados, barreras estructurales y candidatos redundantes con evidencia; no se borra ni relaja ningun test en este ticket; el resultado deja follow-ups pequenos y verificables, no una propuesta masiva de poda.
- **STOP:** si la auditoria exige borrar o reescribir tests en el mismo ticket; si no puede distinguir evidencia de uso/valor real frente a intuicion; o si la poda segura requiere mezclar runner, CI y producto en una sola pasada, parar y re-encuadrar.
