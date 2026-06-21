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
| Media | WOT-2026-013e | Auditar valor, uso y poda segura de la suite de tests | motor/test-suite-audit | pending | WOT-2026-013d | session-2026-06-21-test-suite-audit-followup | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> `013d` ya cerro canonicamente como `completed`: endurecio el escaneo de PRODUCTO ante borrados concurrentes y dejo verde el triple xdist sin reabrir la politica del runner. `013e` queda como unico ticket accionable vivo para auditar valor, duplicidad y poda segura de la suite de tests. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


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
