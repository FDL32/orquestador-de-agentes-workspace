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
| Baja | WOT-2026-010m | Piloto xdist en CI para subset unitario aislado | motor/ci-performance | pending | WOT-2026-010j, WOT-2026-010k, WOT-2026-011e | session-2026-06-17-suite-performance | - |
| Baja | WOT-2026-011i | Si 011e sale estable: evaluar default unit en run_pytest_safe.py | motor/test-suite-perf | pending | WOT-2026-011e | session-2026-06-19-improvement-backlog | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |

> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

### WOT-2026-010m - Piloto xdist en CI para subset unitario aislado
- **Prioridad:** Baja
- **Scope:** motor/ci-performance
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-010j, WOT-2026-010k, WOT-2026-011e
- **Reactivation:** -
- **Origen:** session-2026-06-17-suite-performance.
- **Problema (VERIFICADO):** `011e` ya introdujo `pytest-xdist` como opt-in local en `scripts/run_pytest_safe.py`, pero `.github/workflows/quality-gates.yml` sigue ejecutando solo la ruta serial canonica. La frontera `011e <-> 010m <-> 011i` ya esta decidida: `010m` solo puede pilotar CI sobre una superficie aislada, sin cambiar el default del runner ni contaminar el cierre canonico `--level all`.
- **Objetivo:** anadir un piloto CI xdist estrictamente aditivo y acotado a la superficie permitida del ticket, demostrando que consume la capacidad ya creada por `011e` sin tocar el runner, sin volver xdist implicito y sin relajar el fail-closed del workflow.
- **Files Likely Touched:**
  - repo_motor: `.github/workflows/quality-gates.yml`
  - repo_motor: `tests/unit/test_quality_gates_workflow.py`
- **Criterios binarios:** el workflow incorpora un piloto CI xdist estable y acotado, sin eliminar ni alterar la corrida serial canonica existente; el piloto usa `scripts/run_pytest_safe.py` con `--xdist-workers <N>` solo sobre la superficie permitida del ticket y el camino canonico en CI sigue sin xdist; existe una barrera FAIL-sin/PASS-con que falla si desaparece el piloto o si la corrida canonica adopta xdist por accidente; `python -m pytest tests/unit/test_quality_gates_workflow.py -q`, `ruff check tests/unit/test_quality_gates_workflow.py`, `uv run ruff format --check tests/unit/test_quality_gates_workflow.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si el piloto CI no puede definirse sin tocar `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` o el dispatcher; si la unica via verde convierte xdist en default o lo mete en la corrida canonica `--level all`; o si los tests no parallel-safe obligan a redisenar el selector/runner en vez de dejar un piloto acotado, parar y emitir `CG-WOT-2026-010m.md`.

> Solo tickets vivos con ficha congelada. El resto de tickets vivos (`011h`, `011i`, `002c`, `256a`) mantienen contrato resumido en la tabla hasta su congelado formal.
