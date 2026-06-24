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
| Alta | WOT-2026-013o | Saneamiento estricto de observations.jsonl portable | motor/memory-schema | pending | WOT-2026-013n | session-2026-06-22-memory-upload | - |
| Alta | WOT-2026-013r | Corregir mock-drift de test_upgrade.py + cerrar duplicacion UpgradeManager | motor/upgrade-integrity | pending | WOT-2026-013o | session-2026-06-25-motor-closeout | - |
| Media | WOT-2026-013k | Politica de retencion para notifications_*.md versionado | motor/runtime-retention | deferred | - | session-2026-06-22-close-audit | condition:higiene-dogfooding-local-no-portable |
| Baja | WOT-2026-013l | Retencion local para runtime/reviews, review_packets, observations.bak | motor/runtime-retention | deferred | - | session-2026-06-22-close-audit | condition:higiene-dogfooding-local-no-portable |
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013j CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only; `013j` blindo el drift backlog<->contrato FLT con gate ejecutable. `013m` (overall_status del closeout respeta blocking=False) quedo ENTREGADO Y VERIFICADO fuera del lifecycle de bus (commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de FAIL a WARN): movido a historico como implemented-and-verified, sin eventos de bus por no haberse bootstrappeado como ticket activo. `013n` cerro canonico 2026-06-22: el motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin falsear `COMPLETED`. Follow-ups vivos: `013o`, que debe dejar `observations.jsonl` en `--strict` verde antes de promover nuevas memorias portables, y `013r`, que corrige el mock-drift de `test_upgrade.py` y cierra la duplicacion `UpgradeManager` una vez despejado el bloqueo de schema. `013k`/`013l` siguen DIFERIDOS por ser higiene del repo de dogfooding LOCAL que NO viaja a otros proyectos (VERIFICADO POR BYTES: `notifications_*` y runtime gitignored estan excluidos de MANIFEST.distribute y MANIFEST.workspace). El historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-013o - Saneamiento estricto de observations.jsonl portable
- **Prioridad:** Alta
- **Scope:** motor/memory-schema
- **Estado:** pending
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013n
- **Reactivation:** -
- **Origen:** session-2026-06-22-memory-upload.
- **Problema:** `observations.jsonl` del `repo_motor` falla `python scripts/validate_observations.py --strict --file <obs>` con drift de schema verificado. La evidencia actual marca 29 entradas con `applies_to` no canonico en `repo_motor/.agent/runtime/memory/observations.jsonl`, mientras el `repo_destino` usado como contraste esta limpio (0 entradas no canonicas). No es un unico problema: hay corrupcion de datos en `applies_to` y dominios fuera del enum canonico. La observacion nueva de `013n` sobre seams duplicados seria valida por si sola, pero no conviene escribir memoria portable nueva sobre una base que hoy rompe el contrato estricto del motor.
- **Objetivo:** dejar `repo_motor/.agent/runtime/memory/observations.jsonl` en `--strict` verde separando explicitamente (A) reparacion determinista de datos para los `applies_to` cruzados y (B) decision de contrato para los dominios fuera de enum (mapearlos a dominios canonicos o ampliar el enum con barreras y docs). Una vez verde, decidir de forma auditable si se inserta la observacion diferida de `013n`.
- **Superficie (resumen, no FLT autoritativo):** migrador/validador/schema del motor (`migrate_observations.py`, `validate_observations.py`, `ap-schema.md` y tests) + `repo_motor/.agent/runtime/memory/observations.jsonl`; reutilizar el migrador existente en vez de bypass manual. Si se ejecuta por ruta explicita, usar `python scripts/migrate_observations.py --apply --file <repo_motor>/.agent/runtime/memory/observations.jsonl`.
- **Criterios binarios:** `observations.jsonl` queda verde en `--strict`; los 14 errores de datos se corrigen con evidencia linea-a-linea; los 3 errores de dominio quedan resueltos por decision explicita de contrato (no por fallback silencioso); si la observacion diferida de `013n` se inserta, entra solo despues del verde estricto y mantiene el archivo valido.
- **STOP:** si alguna de las 17 lineas no puede repararse sin reinterpretacion semantica no verificable; si la decision de dominios obliga a redisenar la taxonomia completa de memoria; si el fix exige tocar memorias portables del motor (`repo_motor/.agent/runtime/memory/observations.jsonl`) en la misma ronda.

### WOT-2026-013r - Corregir mock-drift de test_upgrade.py + cerrar duplicacion UpgradeManager
- **Prioridad:** Alta
- **Scope:** motor/upgrade-integrity
- **Estado:** pending
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** WOT-2026-013o
- **Reactivation:** -
- **Origen:** session-2026-06-25-motor-closeout.
- **Problema:** `tests/unit/test_upgrade.py` importa `UpgradeManager` desde `scripts.upgrade_agent_system`, pero parchea `scripts.upgrade.shutil.copytree` / `copy2` (8 ocurrencias verificadas). El verde actual no intercepta las copias reales del codigo bajo test (`scripts/upgrade_agent_system.py:148,151,199,202`) y por tanto da confianza falsa sobre una operacion destructiva. Ademas, `upgrade.py` y `upgrade_agent_system.py` mantienen forks casi identicos de `UpgradeManager`, mientras `README.md` apunta al fork opuesto como canonico.
- **Objetivo:** cerrar el falso verde de upgrade de forma verificable: (A) repuntar los patch al modulo realmente importado o unificar el consumer hacia un unico `UpgradeManager`, (B) resolver la duplicacion estructural `upgrade.py` vs `upgrade_agent_system.py` o documentar explicitamente la frontera si no se unifican en este ticket, y (C) dejar una barrera que falle-sin-fix cuando `copytree` / `copy2` del codigo bajo test no se intercepten. La promocion del aprendizaje FP-012 a `observations.jsonl` solo se evalua despues de `013o`, con schema estricto ya saneado.
- **Superficie (resumen, no FLT autoritativo):** `tests/unit/test_upgrade.py`, `scripts/upgrade_agent_system.py`, `scripts/upgrade.py`, `README.md` y tests/gates relacionados con upgrade; NO tocar memoria portable en la misma ronda salvo que `013o` ya haya cerrado verde.
- **Criterios binarios:** la suite de upgrade falla sin el fix correcto (por ejemplo, monkeypatch de `copytree`/`copy2` real a `raise`); el patch apunta al modulo que de verdad se importa; cualquier duplicacion restante de `UpgradeManager` queda eliminada o explicitamente justificada y alineada con `README`; `ruff`, `validate` y la bateria focal de upgrade quedan verdes.
- **STOP:** si unificar los forks obliga a redisenar todo el flujo de install/upgrade; si la correccion del mock-drift depende de una reinterpretacion no verificable de cual `UpgradeManager` es canonico; si el ticket intenta mezclar el fix de codigo con la migracion de schema de memoria portable.

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
