# work_plan.md -- WOT-2026-010w

## Metadata

- **ID:** WOT-2026-010w
- **Contract ID:** T-010W-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Endurecer el pipeline de cierre canonico en Windows corrigiendo los
`subprocess.run(..., text=True)` de `scripts/closeout_steps/support.py` y
`scripts/closeout_steps/rotation.py` para fijar `encoding="utf-8",
errors="replace"`. El objetivo es que `--session-close --dry-run` y el cierre
real no revienten con `UnicodeDecodeError` al capturar salida no-ASCII de los
scripts de closeout o de comandos git con paths UTF-8.

## Non-goals

- No cambiar la logica funcional del closeout.
- No mover el fix al controller o a un reader-thread global.
- No tocar otros `subprocess.run` fuera de `closeout_steps`.
- No cambiar la semantica de `check_versioned_filenames`.
- No tocar dependencias.

## Premisas verificadas antes de Builder

- `WOT-2026-010v` esta COMPLETED y publicado; el proyecto esta sano y el
  blocker vive en la herramienta de cierre, no en el estado operativo.
- El intento real de `python .agent/agent_controller.py --session-close --dry-run
  --force --project-root <repo_destino>` fallo en Windows con
  `UnicodeDecodeError` al decodificar stdout/stderr de un subprocess del closeout.
- `scripts/closeout_steps/support.py:40` (`run_script`) es el call site
  central: ejecuta scripts del closeout que emiten texto no-ASCII.
- El mismo patron reaparece en `support.py:287` (`git ls-files`) y
  `rotation.py:367` (`git status --short`) como riesgo latente con paths
  no-ASCII.
- Existen tests vivos en `tests/test_session_closeout.py` que permiten blindar
  la regresion sin abrir una suite paralela.

## Decision Arquitectonica

La correccion debe quedarse local a `scripts/closeout_steps/`: el problema no
es de negocio sino de decode en tres call sites concretos. El fix correcto es
explicitar `encoding="utf-8", errors="replace"` en esos `subprocess.run`,
manteniendo intacta la logica del closeout y evitando mover la responsabilidad
al controller o a un wrapper global.

## Files Likely Touched

### repo_motor

- `scripts/closeout_steps/support.py`
- `scripts/closeout_steps/rotation.py`
- `tests/test_session_closeout.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/session_closeout.py`
- `.agent/agent_controller.py`
- `AGENTS.md`
- `backlog.md`
- `ticket_contracts.md`
- salida fallida del dry-run de cierre en `execution_log.md`
- `bus/runtime/events`

## Forbidden Surfaces

- Mover el fix al controller o a un reader-thread global.
- Tocar otros `subprocess.run` fuera de `closeout_steps`.
- Cambiar la logica funcional del closeout.
- Cambiar la semantica de `check_versioned_filenames`.
- Tocar `validate`, bus, runtime o eventos.
- Tocar dependencias.

## Criterios binarios

- `scripts/closeout_steps/support.py:run_script` fija `encoding="utf-8",
  errors="replace"` en su `subprocess.run`.
- `scripts/closeout_steps/support.py:check_versioned_filenames` fija
  `encoding="utf-8", errors="replace"` en su `subprocess.run`.
- `scripts/closeout_steps/rotation.py:step_git_clean` fija
  `encoding="utf-8", errors="replace"` en su `subprocess.run`.
- Existe al menos un test de regresion en `tests/test_session_closeout.py` que
  ejecuta la ruta real de `run_script` contra un script temporal que imprime
  un em dash u otra salida UTF-8 alta y demuestra que la salida se captura sin
  `UnicodeDecodeError`.
- `python .agent/agent_controller.py --session-close --dry-run --force --project-root <repo_destino>`
  deja de fallar por `UnicodeDecodeError` en Windows.
- `python -m pytest tests/test_session_closeout.py -v` pasa.
- `ruff check`, `uv run ruff format --check`, `python scripts/run_pytest_safe.py --level all`
  y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-010w.md` y parar si la correccion exige mover el fix al
controller/reader-thread, tocar subprocess fuera de `closeout_steps` o
reescribir la semantica funcional de los steps de cierre.
