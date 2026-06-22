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
| Baja | WOT-2026-013g | Diagnosticar coste no explicado de test_upgrade_path_suggestion (~60-70s) | motor/test-performance | pending | WOT-2026-013e | session-2026-06-22-test-suite-audit-followup | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> `013e` cerro canonicamente como `completed` (bus `STATE_CHANGED -> COMPLETED`, seq 1302): produjo el inventario auditable de la suite (`docs/test_performance/test_suite_audit_WOT-2026-013e.md`). Hallazgo central: la suite (3111 tests) es mayoritariamente `core regression` / `structural gate`; NO hay grasa significativa para poda masiva. De sus 4 follow-ups, solo se promueven los dos accionables de bajo riesgo: `013f` (poda limpia de `tests/deprecated/`) y `013g` (diagnostico del unico coste `unknown`). FU-013E-1 (clasificar `test_ejemplo`/`test_goose_native_skill`) y FU-013E-4 (consolidar `scope_gate*`/`pre_handoff*`) NO se promueven: FU-4 tocaria barreras structural-gate por un solape no confirmado (riesgo de sobreingenieria que el propio reporte advierte). `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013g - Diagnosticar coste no explicado de test_upgrade_path_suggestion
- **Prioridad:** Baja
- **Scope:** motor/test-performance
- **Estado:** pending
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013e
- **Reactivation:** -
- **Origen:** session-2026-06-22-test-suite-audit-followup (FU-013E-3).
- **Problema:** `test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion` aparece como outlier #2-#3 (~59-70s en baselines 010j/010p) con cuerpo trivial (3 asserts). El coste no es atribuible a logica propia visible; 010j lo dejo como observacion abierta. Es el unico `unknown` de coste del inventario 013e.
- **Objetivo:** explicar la causa real del coste (p.ej. setup de clase/modulo caro atribuido por pytest al primer test, fixture compartida, escaneo) con `--durations` aislado por test, sin tocar el test, y proponer (o descartar con evidencia) una optimizacion local tipo 010k.
- **Files Likely Touched:**
  - repo_motor: `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`
  - repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** repo_motor `tests/unit/test_detect_version.py`, `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_variance.md`
- **Criterios binarios:** reporte durable que explique el coste con medicion reproducible; separa [V] verificado de [I] inferencia; recomienda optimizacion local o cierra "sin optimizacion segura" con evidencia; no toca el test ni producto en este ticket; `validate` 0/0.
- **STOP:** si explicar el coste exige reescribir el test o tocar producto -> re-encuadrar como ticket code aparte; si la medicion no es reproducible entre corridas, documentar la varianza y parar.
