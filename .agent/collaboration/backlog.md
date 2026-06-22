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
| Media | WOT-2026-013i | Higiene de purge de sandbox para latencia operacional | motor/test-runtime-hygiene | pending | WOT-2026-013d, WOT-2026-013g | session-2026-06-22-post-013g-review | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> `013e` cerro canonicamente como `completed` (bus `STATE_CHANGED -> COMPLETED`, seq 1302): produjo el inventario auditable de la suite (`docs/test_performance/test_suite_audit_WOT-2026-013e.md`). Hallazgo central: la suite (3111 tests) es mayoritariamente `core regression` / `structural gate`; NO hay grasa significativa para poda masiva. `013f` podo `tests/deprecated/` sin regresiones y `013g` explico el unico coste `unknown`: el tiempo dominante lo absorbe el `setup` por purge de sandboxes huerfanos, no el cuerpo del test ni producto. De ese cierre nacen exactamente dos follow-ups accionables: `013h` para eliminar el limbo recurrente `archive_rename_uncommitted` del archivado canonico y `013i` para atacar la latencia operacional del purge sin debilitar la barrera de `013d`. FU-013E-1 (clasificar `test_ejemplo`/`test_goose_native_skill`) y FU-013E-4 (consolidar `scope_gate*`/`pre_handoff*`) NO se promueven: FU-4 tocaria barreras structural-gate por un solape no confirmado (riesgo de sobreingenieria que el propio reporte advierte). `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013i - Higiene de purge de sandbox para latencia operacional
- **Prioridad:** Media
- **Scope:** motor/test-runtime-hygiene
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013d, WOT-2026-013g
- **Reactivation:** -
- **Origen:** session-2026-06-22-post-013g-review.
- **Problema:** `013g` verifico que el coste dominante del outlier no vive en `test_upgrade_path_suggestion`, sino en el `setup` que purga cientos de sandboxes huerfanos desde `tests/conftest.py`. La barrera protege salud del arbol tras `013d`, pero hoy introduce latencia operacional visible cuando se acumula basura historica.
- **Objetivo:** reducir el coste del purge de sandbox o acotarlo mejor, sin reabrir la familia xdist ni debilitar la limpieza defensiva introducida por `013d`.
- **Files Likely Touched:**
  - repo_motor: `tests/conftest.py`
  - repo_motor: `tests/unit/test_detect_version.py`
  - repo_motor: `tests/unit/test_project_scanner.py`
  - repo_motor: `docs/test_performance/test_performance_variance.md`
- **Criterios binarios:** existe medicion before/after del purge sobre el mismo host; la latencia del setup baja o queda acotada con evidencia sin reintroducir residuos en `tests/sandbox/test_runtime`; las barreras historicas de `013d` siguen verdes; `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **STOP:** si cualquier mejora segura exige tocar producto, runner, CI o reabrir la decision cerrada de xdist; si el purge rapido reintroduce flakes por residuos, parar y documentar por que la latencia actual es el coste aceptado.
