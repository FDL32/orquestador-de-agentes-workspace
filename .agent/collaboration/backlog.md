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
| Alta | WOT-2026-013m | overall_status del closeout debe respetar blocking=False | motor/session-closeout | pending | - | session-2026-06-22-close-audit | - |
| Media | WOT-2026-013k | Politica de retencion para notifications_*.md versionado | motor/runtime-retention | pending | - | session-2026-06-22-close-audit | - |
| Baja | WOT-2026-013l | Retencion local para runtime/reviews, review_packets, observations.bak | motor/runtime-retention | pending | - | session-2026-06-22-close-audit | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013i CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` del archivado (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only (latencia recurrente ~39s -> ~0s en estado estable). FU-013E-1 y FU-013E-4 NO se promueven (FU-4 tocaria structural-gate por un solape no confirmado). De la revision de 013i nace `013j`: el drift estructural backlog<->contrato en FLT, ya patron repetido. De la auditoria de cierre de sesion (2026-06-22) nacen tres mas: `013m` (alta: el `overall_status` del closeout ignora `blocking=False` y un paso no-bloqueante tumba `--session-close`), `013k` (retencion de `notifications_*.md` VERSIONADO que crece el repo sin techo) y `013l` (baja: retencion de runtime gitignored -- reviews/packets/.bak -- que solo crece disco local). La auditoria confirmo que NO hay crecimiento sin techo en temporales de prueba (sandbox/tmp/pytest-safe sanos tras 013i); el historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


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

### WOT-2026-013m - overall_status del closeout debe respetar blocking=False
- **Prioridad:** Alta
- **Scope:** motor/session-closeout
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** -
- **Origen:** session-2026-06-22-close-audit (descubierto al intentar el cierre canonico).
- **Problema:** `scripts/session_closeout.py::SessionReport.overall_status` retorna FAIL ante CUALQUIER step FAIL sin consultar `s.blocking`, contradiciendo su docstring ("FAIL if any blocking step failed"). Efecto verificado: `versioned_filenames` (marcado `blocking=False` en `closeout_steps/support.py`) tumba `--session-close` con exit 1 aunque sea no-bloqueante. Bloquea cierres de sesion sin que exista deuda realmente bloqueante.
- **Objetivo:** que `overall_status` honre el flag `blocking`: un step `FAIL` no-bloqueante debe reflejarse (p.ej. como WARN o FAIL informativo) pero NO forzar exit 1 del pipeline. Preservar el bloqueo real de los steps `blocking=True` (prepush_check, archive_rename_uncommitted, etc.).
- **Superficie (resumen, no FLT autoritativo):** `scripts/session_closeout.py` (overall_status + codigo de exit) y su test; el FLT canonico lo fija el contrato frozen.
- **Criterios binarios:** un step `blocking=False` en FAIL no produce exit 1 del pipeline; los steps `blocking=True` siguen bloqueando; barrera de regresion que falla sin el fix; `run_pytest_safe --level all` y `validate` verdes.
- **STOP:** si arreglar overall_status exige redisenar el modelo de StepResult o tocar la semantica de los gates bloqueantes; si algun consumidor depende del comportamiento actual (FAIL-ante-cualquier-FAIL), documentarlo antes de cambiar.

### WOT-2026-013k - Politica de retencion para notifications_*.md versionado
- **Prioridad:** Media
- **Scope:** motor/runtime-retention
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** -
- **Origen:** session-2026-06-22-close-audit (auditoria de superficies que crecen).
- **Problema:** `repo_destino/.agent/collaboration/archive/` acumula snapshots `notifications_*.md` VERSIONADOS (12 trackeados, ~9.5MB) que `agent_controller` anade al rotar la proyeccion. A diferencia de `runtime/reviews|review_packets|events` (gitignored, solo disco), estos entran en el repo y en cada clone, creciendo sin techo. NO es basura por ticket; es falta de politica de retencion.
- **Objetivo:** introducir retencion para `notifications_*.md` (mantener los N ultimos o por edad), archivando o podando el resto fuera del arbol versionado, sin perder la rotacion viva que el controller necesita.
- **Superficie (resumen, no FLT autoritativo):** el codigo del controller que rota notifications + posible script de retencion; no tocar la superficie viva `notifications.md`.
- **Criterios binarios:** el conteo de `notifications_*.md` versionados queda acotado por politica; la rotacion viva sigue funcionando; ningun test de proyeccion/controller regresa; `validate` verde.
- **STOP:** si acotar la retencion rompe la rotacion viva o algun consumidor del historico; si la unica via es borrar historico util sin archivar -> re-encuadrar.

### WOT-2026-013l - Retencion local para runtime gitignored (reviews, packets, memory .bak)
- **Prioridad:** Baja
- **Scope:** motor/runtime-retention
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** -
- **Origen:** session-2026-06-22-close-audit.
- **Problema:** `runtime/reviews` (~5.1MB, 106 files), `runtime/review_packets` (~2MB, 47), `observations.jsonl.bak.*` (12) crecen sin techo en DISCO local. Estan gitignored => NO contaminan repo ni publicacion, solo el disco del operador. Prioridad baja precisamente por eso.
- **Objetivo:** politica de retencion por edad/conteo para esas superficies gitignored, idealmente integrada en el closeout o un script de mantenimiento opt-in. NO incluir `events/archive`, `audits/system_health` ni `_archive/plan_audit` (historico util versionado, fuera de scope).
- **Superficie (resumen, no FLT autoritativo):** script de retencion / paso opt-in del closeout para rutas runtime gitignored.
- **Criterios binarios:** existe una via auditable para podar por edad/conteo esas 3 superficies sin tocar historico util; no borra nada versionado; `validate` verde.
- **STOP:** si la retencion toca superficies versionadas o historico util; si exige cambiar gitignore o el contrato de runtime.
