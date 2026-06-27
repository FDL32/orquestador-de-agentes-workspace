# Plan de Trabajo: WOT-2026-014b

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014b
- **Estado:** COMPLETED
- **Titulo:** run_pytest_safe soporta repos destino en unittest (fallback cuando no hay pytest)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014B-001
- **Plan-Link:** PLAN-014B-001
- **Builder clarification budget:** 0

## Objetivo
Que scripts/run_pytest_safe.py detecte el runner del interprete de tests: usa pytest si esta instalado;
si NO, hace fallback a `python -m unittest discover`; y emite last-run.json igual en ambos modos
(tested_commit_sha, exit_code, level), con el mismo criterio tested_commit_sha == HEAD.
Verificacion del objetivo (que comando/test lo demuestra): un test de barrera mutation-verified que,
forzando pytest-ausente (monkeypatch del probe), selecciona el runner unittest y produce last-run.json
exit 0 sobre un proyecto fixture con un unittest.TestCase; sin el fix (pytest hardcodeado) ese caso
FALLA por "No module named pytest". Ver DoD.

## Resolucion de la clausula abierta (CONGELADA por orquestacion)
La clausula "Opcionalmente: declarar el runner canonico del destino en un sitio estable
(pyproject/config/contrato)" queda como NON-GOAL de 014b: es un follow-up separado, NO entregable de
este ticket. 014b se limita a la deteccion + fallback + last-run.json consistente.

## Premise (VERIFICADO en vivo)
run_pytest_safe asume pytest en el .venv del destino. Un destino en unittest sin pytest produce falso
rojo en el gate canonico (No module named pytest) aunque la suite real pase con python -m unittest.
El comando se construye y ejecuta en subprocess (stream_pytest, ~L372) sobre el interprete resuelto.

## Premise Re-check (cwd=repo_motor, solo lectura)
grep -nE "stream_pytest|-m pytest|interpreter|resolve_test_interpreter|last-run.json|tested_commit_sha" scripts/run_pytest_safe.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
Condicion de arranque: el comando se construye SIEMPRE como pytest; no hay deteccion de runner ni fallback unittest.

## Decision Arquitectonica
- Factorizar la SELECCION de runner en una funcion testable (p.ej. select_test_runner / build_test_command)
  que, dado el interprete de tests resuelto, PRUEBA si tiene pytest (p.ej. `<interp> -c "import pytest"`
  o find_spec en el interprete objetivo) y devuelve:
  - si pytest disponible -> el comando pytest ACTUAL (comportamiento sin cambios para repos con pytest);
  - si NO -> `<interp> -m unittest discover` (sobre el directorio de tests configurado).
- last-run.json se escribe identico en ambos modos (tested_commit_sha, exit_code, level); opcionalmente
  un campo informativo `runner: pytest|unittest` para observabilidad (no cambia el contrato del gate).
- El criterio tested_commit_sha == HEAD NO cambia.

## Files Likely Touched (relativos a repo_motor)
- scripts/run_pytest_safe.py
- tests/unit/test_run_pytest_safe_runner_detection.py

Aclaraciones: la deteccion debe ser sobre el INTERPRETE DE TESTS objetivo (no el del proceso actual).
No reescribir el locking ni el resto del runner; solo anadir deteccion + fallback en la construccion del comando.

## Read/inspect only
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- El comportamiento para repos que SI tienen pytest: IDENTICO (no se cambia el contrato del gate).
- El contrato de last-run.json (campos exigidos por el gate de handoff): no se rompe; solo se anaden
  campos informativos opcionales si hace falta.
- NO imponer un runner unico ni declarar el runner canonico en pyproject/config (NON-GOAL).
- El locking / runtime dirs / state-leak barrier de run_pytest_safe: read-only salvo el seam de seleccion de comando.
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal
python -m pytest tests/unit/test_run_pytest_safe_runner_detection.py -q
python -m ruff check scripts/run_pytest_safe.py tests/unit/test_run_pytest_safe_runner_detection.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico (el motor SI tiene pytest -> ruta pytest sin cambios):
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO declarar el runner canonico del destino en un sitio estable (follow-up separado).
- NO cambiar el contrato de gates para repos con pytest.
- NO imponer un runner unico a los destinos.

## CONTRACT_GAP / STOP
- Si la deteccion de pytest en el interprete objetivo no se puede hacer sin cambiar el contrato de last-run.json.
- Si el fallback unittest exige un directorio de tests no descubrible de forma estable.
-> emitir CG-WOT-2026-014b.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] BARRERA mutation-verified: forzando pytest-ausente (monkeypatch del probe), run_pytest_safe selecciona
  el runner unittest y, sobre un proyecto fixture con un unittest.TestCase que pasa, escribe last-run.json
  con tested_commit_sha, exit_code 0 y level; sin el fix (pytest hardcodeado) ese caso FALLA por "No module named pytest".
- [ ] Con pytest disponible, el comando construido es el pytest ACTUAL (test que fija el comportamiento sin cambios).
- [ ] last-run.json conserva los campos exigidos por el gate (tested_commit_sha, exit_code, level) en ambos modos.
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD (ruta pytest, motor con pytest).
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014b), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.
