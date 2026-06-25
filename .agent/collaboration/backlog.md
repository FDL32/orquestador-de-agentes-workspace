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
| Baja | WOT-2026-013t | Deduplicar UpgradeManager (upgrade.py vs upgrade_agent_system.py) / binding shutil independiente | motor/upgrade-integrity | deferred | - | CG-WOT-2026-013r (deuda estructural opcional) | condition:deuda-opcional-no-bloquea-013r |
| Media | WOT-2026-013k | Extender retencion local para notifications_*.md gitignored en collaboration/archive | motor/runtime-retention | pending | WOT-2026-013l | session-2026-06-22-close-audit + audit_cf_ticket_contract 2026-06-25 | - |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013j CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only; `013j` blindo el drift backlog<->contrato FLT con gate ejecutable. `013m` (overall_status del closeout respeta blocking=False) quedo ENTREGADO Y VERIFICADO fuera del lifecycle de bus (commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de FAIL a WARN): movido a historico como implemented-and-verified, sin eventos de bus por no haberse bootstrappeado como ticket activo. `013n` cerro canonico 2026-06-22: el motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin falsear `COMPLETED`. `013o` CERRO COMPLETED en el bus (terminal) pero contra TARGET EQUIVOCADO: saneo `repo_destino/observations.jsonl` (limpio, 17 errores) y dejo SIN sanear el `repo_motor/observations.jsonl` (168 errores --strict, VERIFICADO 2026-06-25). NO se reabre (ID terminal); el saneamiento real del MOTOR se trato como ticket NUEVO `013s`, ya cerrado canonico y movido a historico. `013r` ya cerro canonico 2026-06-25: corrigio el mock-drift de `test_upgrade.py` con DoD enmendado a barrera de binding y dejo `013t` como deuda estructural opcional. ``013v`` ya cerro canonico 2026-06-25: hizo explicita la semantica de `reviews/` por `mtime` de directorio sin tocar el algoritmo de orden, y la blindo con help/docstring/tests. `013l` y `013v` quedan resueltos como pareja de bajo riesgo en runtime-retention gitignored. Ticket vivo actual de la familia 013: `013k` (cuarta superficie gitignored de retencion local: `collaboration/archive/notifications_*.md`, re-encuadrada tras auditoria contractual 2026-06-25). Deuda estructural opcional restante: `013t` (dedup/binding independiente en upgrade). El historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013t - Deduplicar UpgradeManager / binding shutil independiente (Paso 2 de 013r)
- **Prioridad:** Alta
- **Scope:** motor/upgrade-integrity
- **Estado:** pending (reactivado 2026-06-25 para preparar packet + bootstrap canonico; el ticket activo se gobierna desde `work_plan.md`). (DEUDA ESTRUCTURAL OPCIONAL; NO bloquea el cierre de 013r). El DoD de 013r se enmendo (2026-06-25, reaprobacion humana) a la barrera de binding; 013t queda como mejora futura para deduplicar los forks si se decide sanear la duplicacion.
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente; 013r ya cerro su aprendizaje con DoD enmendado)
- **Origen:** CG-WOT-2026-013r (`.agent/planning/contract_gaps/CG-WOT-2026-013r.md`).
- **Problema:** `scripts.upgrade.shutil IS scripts.upgrade_agent_system.shutil` (objeto
  modulo compartido), por lo que repuntar el target del patch en `test_upgrade.py` es
  indistinguible en runtime y el DoD binario de 013r ("revertir patches -> pytest FALLA")
  es inalcanzable sin tocar codigo productivo. Los dos forks definen clases
  `UpgradeManager` distintas (`upgrade.py` vs `upgrade_agent_system.py`); `README:104`
  declara canonico `upgrade.py` pero el test ejercita el otro fork.
- **Objetivo:** dar a cada fork binding de shutil independiente (o deduplicar los forks
  y alinear `README`), de modo que parchear el modulo equivocado deje de interceptar y
  "revertir el fix -> FALLA" sea verificable. Referencia: FP-012.
- **Non-goal:** no redisenar el flujo completo de install/upgrade (clausula STOP de 013r).

### WOT-2026-013k - Extender retencion local para notifications_*.md gitignored en collaboration/archive
- **Prioridad:** Media
- **Scope:** motor/runtime-retention
- **Estado:** pending (re-encuadrado 2026-06-25 tras auditoria contractual; el ticket activo se gobierna desde `work_plan.md`).
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013l (COMPLETED; utileria base ya entregada)
- **Reactivation:** -
- **Origen:** session-2026-06-22-close-audit + `audit_cf_ticket_contract.md` (2026-06-25).
- **Correccion de premisa (2026-06-25):** VERIFICADO POR BYTES que `repo_destino/.agent/collaboration/archive/notifications_*.md` NO esta versionado: `git ls-files` devuelve 0 hits, `git check-ignore -v` apunta a `.gitignore:72` (`.agent/collaboration/archive/`), y `git log -- .agent/collaboration/archive/notifications_*.md` no muestra historial trackeado. La deuda real es LOCAL y gitignored, igual que `013l`, no historico versionado.
- **Problema:** `repo_destino/.agent/collaboration/archive/` acumula snapshots locales gitignored `notifications_*.md` creados por la rotacion de notifications. Hoy la utilidad opt-in de `013l` poda `reviews/`, `review_packets/` y `observations.jsonl.bak.*`, pero deja fuera esta cuarta superficie local; el crecimiento sigue sin politica explicita.
- **Objetivo:** extender `scripts/prune_runtime_retention.py` para incluir `collaboration/archive/notifications_*.md` como cuarta superficie gitignored, con `dry-run/apply` explicitos y sin tocar otros artefactos de `collaboration/archive/` ni la superficie viva `notifications.md`.
- **Superficie (resumen, no FLT autoritativo):** `scripts/prune_runtime_retention.py` + `tests/unit/test_prune_runtime_retention.py`; NO tocar el controller ni closeout.
- **Criterios binarios:** el selector reconoce `notifications_*.md` como superficie local opt-in; conserva solo los N mas recientes de esa familia; nunca selecciona otros archivos de `collaboration/archive/`; la CLI sigue requiriendo `--dry-run|--apply`; `validate` verde.
- **STOP:** si la unica forma de incluir `notifications_*.md` exige tocar `agent_controller.py`, `session_closeout`, `bus/**` o seleccionar archivos de `collaboration/archive/` ajenos a `notifications_*.md` -> `CONTRACT_GAP` y re-pausa.


