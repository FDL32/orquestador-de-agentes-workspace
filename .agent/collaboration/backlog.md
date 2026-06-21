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
| Alta | WOT-2026-013c | Robustecer 3 tests global-state para ejecucion paralela | motor/test-suite-hygiene | pending | WOT-2026-011e, WOT-2026-010m | session-2026-06-21-post-011h-followup | - |
| Alta | WOT-2026-002c | A2d: eliminar copias motor-provides + ejecutar decisiones (FASE3 diferida) | system/host-extends | completed-partial | WOT-2026-002a, WOT-2026-002b | session-2026-06-13-host-extends | condition:install-sync-revendor-resuelto |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

### WOT-2026-013c - Robustecer 3 tests global-state para ejecucion paralela
- **Prioridad:** Alta
- **Scope:** motor/test-suite-hygiene
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-011e, WOT-2026-010m
- **Reactivation:** -
- **Origen:** session-2026-06-21-post-011h-followup.
- **Problema (VERIFICADO):** `011i` cerro como `not-pursued` la via de runner/default: los 3 tests persistentes `test_upgrade_path_suggestion`, `test_scan_current_project` y `test_no_inline_ticket_regex` pasan serial y siguen ligados a estado global del proceso/repo (`cwd`, git y escaneo del proyecto vivo). La deuda real ya no es de politica xdist, sino de higiene de tests.
- **Objetivo:** volver esos 3 tests parallel-safe sin tocar `scripts/run_pytest_safe.py`, CI ni el default xdist. El entregable es de aislamiento de tests; cualquier recuperacion futura del default se decide despues, con evidencia nueva.
- **Files Likely Touched:**
  - repo_motor: `tests/unit/test_detect_version.py`
  - repo_motor: `tests/unit/test_project_scanner.py`
  - repo_motor: `tests/unit/test_no_inline_ticket_regex.py`
  - repo_motor: `tests/conftest.py`
- **Criterios binarios:**
  - Los 3 tests citados quedan verdes en serial y tambien verdes juntos bajo `python -m pytest <triple> -q -n 8 --dist load`.
  - El diff productivo queda acotado a superficies de test/fixture; no toca runner, CI, controller ni codigo de producto.
  - Existe al menos una barrera FAIL-sin/PASS-con sobre el rojo real de concurrencia/estado compartido.
  - `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q`, `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q -n 8 --dist load`, `ruff` sobre Python tocado, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si cualquier fix exige tocar `scripts/run_pytest_safe.py`, `quality-gates.yml`, `runtime/`, controller o codigo de producto; si al corregir esos 3 aparece otra familia roja dominante bajo xdist; o si la reproduccion deja de estar anclada en estos tests y pasa a ser deuda de runner otra vez, parar y emitir `CG-WOT-2026-013c.md`.

> Tickets vivos accionables: `013c` es el unico. `002c` (`completed-partial`) y `256a` (`blocked` externo) quedan fuera por naturaleza. `011i` y `013b` cerraron honestamente como `not-pursued` / `absorbed`: el default xdist no se reabre por inercia, solo si `013c` deja evidencia nueva.
