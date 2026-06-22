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
| Media | WOT-2026-013j | Reconciliar duplicidad de FLT entre backlog.md y contrato frozen | motor/backlog-contract-drift | pending | - | session-2026-06-22-post-013i-review | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013i CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` del archivado (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only (latencia recurrente ~39s -> ~0s en estado estable). FU-013E-1 y FU-013E-4 NO se promueven (FU-4 tocaria structural-gate por un solape no confirmado). De la revision de 013i nace `013j`: el drift estructural backlog<->contrato en FLT, ya patron repetido. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013j - Reconciliar duplicidad de FLT entre backlog.md y contrato frozen
- **Prioridad:** Media
- **Scope:** motor/backlog-contract-drift
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** -
- **Origen:** session-2026-06-22-post-013i-review (patron repetido al ajustar packets de 013f/013h).
- **Problema:** las fichas detalladas de `backlog.md` re-declaran el `Files Likely Touched` que ya vive en el contrato frozen (`ticket_contracts.md` / `work_plan.md`). Las dos copias divergen y obligan a reconciliacion manual del packet antes de lanzar Builder (visto en 013h, y el propio usuario tuvo que ajustar el FLT del packet de 013h para que coincidiera). Patron estructural, ya recurrente.
- **Objetivo:** definir una sola fuente de verdad para el FLT y eliminar o reconciliar la duplicidad, de modo que el backlog no re-declare FLT que pertenece al contrato frozen. El cambio debe vivir en la generacion/validacion del packet del motor, sin debilitar el scope gate ni el contrato frozen.
- **Superficie (resumen, no FLT autoritativo):** el FLT canonico lo declara el contrato frozen (`ticket_contracts.md`) y luego `work_plan.md`; esta ficha no lo re-declara. A grandes rasgos toca el gate/validador del backlog y su test en el motor.
- **Criterios binarios:** una sola fuente de verdad para el FLT; el backlog deja de divergir del contrato frozen, o existe una barrera que detecta la divergencia antes del handoff; el scope gate y el contrato frozen siguen intactos; `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` verdes.
- **STOP:** si la unica via exige debilitar el scope gate o el contrato frozen; si reconciliar la duplicidad obliga a un rediseno mayor del lifecycle de packet en vez de un cambio acotado -> re-encuadrar antes de implementar.
