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
| Alta | WOT-2026-013r | Corregir mock-drift de test_upgrade.py + cerrar duplicacion UpgradeManager | motor/upgrade-integrity | pending | WOT-2026-013s | session-2026-06-25-motor-closeout | - |
| Alta | WOT-2026-013t | Deduplicar UpgradeManager (upgrade.py vs upgrade_agent_system.py) / binding shutil independiente | motor/upgrade-integrity | pending | WOT-2026-013r | CG-WOT-2026-013r (Paso 2 escalado) | condition:reaprobacion-humana-paso2 |
| Media | WOT-2026-013k | Politica de retencion para notifications_*.md versionado | motor/runtime-retention | deferred | - | session-2026-06-22-close-audit | condition:higiene-dogfooding-local-no-portable |
| Baja | WOT-2026-013l | Retencion local para runtime/reviews, review_packets, observations.bak | motor/runtime-retention | deferred | - | session-2026-06-22-close-audit | condition:higiene-dogfooding-local-no-portable |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013j CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only; `013j` blindo el drift backlog<->contrato FLT con gate ejecutable. `013m` (overall_status del closeout respeta blocking=False) quedo ENTREGADO Y VERIFICADO fuera del lifecycle de bus (commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de FAIL a WARN): movido a historico como implemented-and-verified, sin eventos de bus por no haberse bootstrappeado como ticket activo. `013n` cerro canonico 2026-06-22: el motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin falsear `COMPLETED`. `013o` CERRO COMPLETED en el bus (terminal) pero contra TARGET EQUIVOCADO: saneo `repo_destino/observations.jsonl` (limpio, 17 errores) y dejo SIN sanear el `repo_motor/observations.jsonl` (168 errores --strict, VERIFICADO 2026-06-25). NO se reabre (ID terminal); el saneamiento real del MOTOR se trato como ticket NUEVO `013s`, ya cerrado canonico y movido a historico. Follow-up vivo actual: `013r`, que corrige el mock-drift de `test_upgrade.py` y cierra la duplicacion `UpgradeManager` ahora que el bloqueo de schema quedo despejado. `013k`/`013l` siguen DIFERIDOS por ser higiene del repo de dogfooding LOCAL que NO viaja a otros proyectos (VERIFICADO POR BYTES: `notifications_*` y runtime gitignored estan excluidos de MANIFEST.distribute y MANIFEST.workspace). El historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013r - Corregir mock-drift de test_upgrade.py + cerrar duplicacion UpgradeManager
- **Prioridad:** Alta
- **Scope:** motor/upgrade-integrity
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013s (sucesor de 013o; 013o cerro contra target equivocado)
- **Reactivation:** -
- **Origen:** session-2026-06-25-motor-closeout.
- **Contrato canonico (FUENTE UNICA):** `.agent/planning/work_plan_WOT-2026-013r.md`.
  Fuente de verdad del problema: FP-012 en
  `repo_motor/docs/KNOWN_FAILURE_PATTERNS.md`. El cuerpo del ticket (premise
  re-check, secuencia minima fija paso 1/paso 2, DoD, STOP) vive SOLO en el
  packet. Esta fila es indice; no duplicar el detalle aqui.

### WOT-2026-013t - Deduplicar UpgradeManager / binding shutil independiente (Paso 2 de 013r)
- **Prioridad:** Alta
- **Scope:** motor/upgrade-integrity
- **Estado:** pending (requiere REAPROBACION humana explicita; Paso 2 escalado desde 013r)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013r
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

### WOT-2026-013k - Politica de retencion para notifications_*.md versionado
- **Prioridad:** Media
- **Scope:** motor/runtime-retention
- **Estado:** deferred
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** condition:higiene-dogfooding-local-no-portable
- **Origen:** session-2026-06-22-close-audit (auditoria de superficies que crecen).
- **Diferido (2026-06-22):** VERIFICADO POR BYTES que `collaboration/archive/` esta EXCLUIDO de `MANIFEST.distribute` (l.112) y `MANIFEST.workspace` (l.92) => `notifications_*.md` NO viaja a otros proyectos. Es higiene del repo de dogfooding LOCAL, no mejora de portabilidad/instalabilidad. Ademas la retencion correcta es consolidacion (mantener trazabilidad), no poda; mas delicado que 013l. Reactivar solo si el ruido operativo local molesta o en una pasada de mantenimiento del repo dogfooding.
- **Problema:** `repo_destino/.agent/collaboration/archive/` acumula snapshots `notifications_*.md` VERSIONADOS (12 trackeados, ~9.5MB) que `agent_controller` anade al rotar la proyeccion. A diferencia de `runtime/reviews|review_packets|events` (gitignored, solo disco), estos entran en el repo y en cada clone, creciendo sin techo. NO es basura por ticket; es falta de politica de retencion. Nota: `check_no_history_truncation.py` solo exige compensacion de archivo al truncar `execution_log`, NO prohibe podar notifications archivados (verificado en 013j-followup).
- **Objetivo:** introducir retencion para `notifications_*.md` (mantener los N ultimos o por edad), archivando o podando el resto fuera del arbol versionado, sin perder la rotacion viva que el controller necesita.
- **Superficie (resumen, no FLT autoritativo):** el codigo del controller que rota notifications + posible script de retencion; no tocar la superficie viva `notifications.md`.
- **Criterios binarios:** el conteo de `notifications_*.md` versionados queda acotado por politica; la rotacion viva sigue funcionando; ningun test de proyeccion/controller regresa; `validate` verde.
- **STOP:** si acotar la retencion rompe la rotacion viva o algun consumidor del historico; si la unica via es borrar historico util sin archivar -> re-encuadrar.

### WOT-2026-013l - Retencion local para runtime gitignored (reviews, packets, memory .bak)
- **Prioridad:** Baja
- **Scope:** motor/runtime-retention
- **Estado:** deferred
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** -
- **Reactivation:** condition:higiene-dogfooding-local-no-portable
- **Origen:** session-2026-06-22-close-audit.
- **Diferido (2026-06-22):** estas superficies son gitignored => NO viajan a otros proyectos ni a la publicacion; es solo disco del operador. Diferido por no aportar a "motor limpio para otros proyectos". Es el mas simple de los dos diferidos; si se retoma uno, este antes que 013k.
- **Problema:** `runtime/reviews` (~5.1MB, 106 files), `runtime/review_packets` (~2MB, 47), `observations.jsonl.bak.*` (12) crecen sin techo en DISCO local. Estan gitignored => NO contaminan repo ni publicacion, solo el disco del operador. Prioridad baja precisamente por eso.
- **Objetivo:** politica de retencion por edad/conteo para esas superficies gitignored, idealmente integrada en el closeout o un script de mantenimiento opt-in. NO incluir `events/archive`, `audits/system_health` ni `_archive/plan_audit` (historico util versionado, fuera de scope).
- **Superficie (resumen, no FLT autoritativo):** script de retencion / paso opt-in del closeout para rutas runtime gitignored.
- **Criterios binarios:** existe una via auditable para podar por edad/conteo esas 3 superficies sin tocar historico util; no borra nada versionado; `validate` verde.
- **STOP:** si la retencion toca superficies versionadas o historico util; si exige cambiar gitignore o el contrato de runtime.
