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
| Alta | WOT-2026-011h | Barrera de archivado tambien en mark-ready | motor/collab-hygiene | pending | WOT-2026-011a, WOT-2026-011d | session-2026-06-19-improvement-backlog | - |
| Media | WOT-2026-011i | Default xdist + `--dist loadscope` para `--level unit` (absorbe 013b) | motor/test-suite-perf | pending | WOT-2026-011e, WOT-2026-010m | session-2026-06-19-improvement-backlog | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |

> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

### WOT-2026-011h - Barrera de archivado tambien en mark-ready
- **Prioridad:** Alta
- **Scope:** motor/collab-hygiene
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011a, WOT-2026-011d
- **Reactivation:** -
- **Origen:** session-2026-06-19-improvement-backlog.
- **Problema (VERIFICADO):** `011a` ya cerro fail-closed la ruta de `--session-close` ante `archive_rename_uncommitted`, pero `--mark-ready` sigue auto-archivando `PLAN_/AUDIT_` cerrados desde `.agent/agent_controller.py` y puede dejar el mismo limbo `D old + ?? new` para que el Manager lo reconcilie a mano despues del handoff. La razon estable y la remediacion ya existen; falta cerrar el mismo hueco en el camino de handoff.
- **Objetivo:** hacer que `--mark-ready` falle cerrado cuando su auto-archivado deje `archive_rename_uncommitted`, reutilizando el mismo diagnostico estable y sin introducir auto-commit del archivador.
- **Files Likely Touched:**
  - repo_motor: `.agent/agent_controller.py`
  - repo_motor: `tests/test_agent_controller.py`
  - repo_motor: `tests/test_pre_handoff_guard.py`
  - repo_motor: `tests/unit/test_scope_gate.py`
- **Criterios binarios:** `--mark-ready` bloquea con razon estable `archive_rename_uncommitted` si su auto-archivado deja limbo; el diagnostico conserva origen, destino y remediacion exacta; el caso limpio sigue dejando `READY_FOR_REVIEW` sin falso positivo; existe al menos una barrera FAIL-sin/PASS-con sobre la ruta real de `--mark-ready`; `python -m pytest tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py -q`, `ruff check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `uv run ruff format --check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si la unica forma de cerrar el hueco es auto-commitear el archivador; si la deteccion solo puede expresarse como `dirty tree` generico y no como `archive_rename_uncommitted`; o si reproducir la mutacion real exige tocar `--session-close` otra vez en vez de la ruta de handoff, parar y emitir `CG-WOT-2026-011h.md`.

### WOT-2026-011i - Default xdist + `--dist loadscope` para `--level unit` (absorbe 013b)
- **Prioridad:** Media
- **Scope:** motor/test-suite-perf
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011e, WOT-2026-010m
- **Reactivation:** -
- **Origen:** session-2026-06-19-improvement-backlog.
- **Problema (VERIFICADO):** `011e` resolvio el opt-in local y `010m` cerro el piloto CI sin contaminar el cierre canonico. `013b` (absorbido aqui; ver `CG-WOT-2026-013b.md`) demostro con 3 corridas que el rojo del subset unit bajo xdist NO es una familia de tests aislable: con reparto por defecto (`--dist load`) el conteo oscila 12<->37 y el archivo dominante cambia entre corridas identicas (cada archivo pasa aislado bajo `-n 8`). Es contencion de reparto cross-archivo, propiedad del runner. La via verde es `--dist loadscope` (agrupa por archivo), que es justo lo que 013b tenia prohibido tocar. Por eso 013b se absorbe y la politica de reparto vive aqui.
- **Objetivo:** convertir `python scripts/run_pytest_safe.py --level unit` en un camino xdist por defecto, AUDITABLE y ESTABLE, usando `--dist loadscope` para eliminar la contencion cross-archivo demostrada por 013b; preservando `--level all` serial, respetando args explicitos y manteniendo un escape estable a serial (`--xdist-workers 1`).
- **Files Likely Touched:**
  - repo_motor: `scripts/run_pytest_safe.py`
  - repo_motor: `tests/unit/test_run_pytest_safe.py`
- **Criterios binarios:** `python scripts/run_pytest_safe.py --level unit` habilita xdist por defecto CON `--dist loadscope` y metadata estable en `last-run.json`; el subset unit queda verde y ESTABLE en >=3 corridas seguidas (refutando el no-determinismo 12<->37 que documento 013b); `python scripts/run_pytest_safe.py --level unit --xdist-workers 1` conserva un camino serial auditable; `python scripts/run_pytest_safe.py --level all` sigue serial; la barrera `tests/unit/test_run_pytest_safe.py` protege el nuevo default, el modo loadscope y el escape a serial; `python -m pytest tests/unit/test_run_pytest_safe.py -q`, `ruff check scripts/run_pytest_safe.py tests/unit/test_run_pytest_safe.py`, `uv run ruff format --check scripts/run_pytest_safe.py tests/unit/test_run_pytest_safe.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si activar el default unitario exige tocar CI, `pre_handoff_guard.py`, el dispatcher o cambiar la semantica de `--level all`; si no existe un escape serial estable con el CLI actual; o si `--dist loadscope` NO estabiliza el subset unit (sigue habiendo rojo no determinista), parar y emitir `CG-WOT-2026-011i.md`.

> Todos los tickets vivos restantes ya tienen ficha congelable y orden de ejecucion claro para pipeline: `011h -> 011i` (011i absorbe 013b). `002c` y `256a` quedan fuera por naturaleza (`completed-partial` y `blocked` externo).
