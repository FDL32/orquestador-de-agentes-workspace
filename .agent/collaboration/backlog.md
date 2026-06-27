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
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked | - | session-2026-06-11-security-followup | condition:uv-resuelve-pip>=26.1.2 |
| Baja | WOT-2026-014j | Test cosmetico false-green: el resolve() del link-branch de motor_link no tiene barrera real (pasa con y sin fix en NTFS) | motor/topology-resolution | pending | - | session-2026-06-27-014x-closeaudit | - |
| Baja | WOT-2026-014k | Tension de orden en el cierre full-audit: Bloque 1.3bis escribe follow-ups en backlog (sin commit) pero Bloque 3 prepush exige arbol limpio -> el propio follow-up bloquea el cierre | motor/closeout-hygiene | pending | - | session-2026-06-27-014x-closeaudit | - |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013j CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only; `013j` blindo el drift backlog<->contrato FLT con gate ejecutable. `013m` (overall_status del closeout respeta blocking=False) quedo ENTREGADO Y VERIFICADO fuera del lifecycle de bus (commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de FAIL a WARN): movido a historico como implemented-and-verified, sin eventos de bus por no haberse bootstrappeado como ticket activo. `013n` cerro canonico 2026-06-22: el motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin falsear `COMPLETED`. `013o` CERRO COMPLETED en el bus (terminal) pero contra TARGET EQUIVOCADO: saneo `repo_destino/observations.jsonl` (limpio, 17 errores) y dejo SIN sanear el `repo_motor/observations.jsonl` (168 errores --strict, VERIFICADO 2026-06-25). NO se reabre (ID terminal); el saneamiento real del MOTOR se trato como ticket NUEVO `013s`, ya cerrado canonico y movido a historico. `013r` ya cerro canonico 2026-06-25: corrigio el mock-drift de `test_upgrade.py` con DoD enmendado a barrera de binding y dejo `013t` como deuda estructural opcional. ``013v`` ya cerro canonico 2026-06-25: hizo explicita la semantica de `reviews/` por `mtime` de directorio sin tocar el algoritmo de orden, y la blindo con help/docstring/tests. `013l`, `013v` y `013k` quedan resueltos como familia de bajo riesgo en runtime-retention gitignored. `013t` YA CERRO CANONICO 2026-06-25 (COMPLETED + SUPERVISOR_CLOSED en bus, commit motor `a1b99af`): un unico owner editable de `UpgradeManager` (`scripts.upgrade_agent_system`) con `scripts.upgrade` como re-export y copy-seam shutil/datetime inequivoco. La familia 013 queda CERRADA sin tickets vivos. El historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-014j - Test cosmetico false-green en resolve() del link-branch de runtime.motor_link
- **Prioridad:** Baja
- **Scope:** motor/topology-resolution
- **Estado:** pending (detectado en la pasada adversarial de cierre de sesion 2026-06-27, auditando el lote 014x)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente; deuda residual de WOT-2026-014e)
- **Reactivation:** -
- **Origen:** session-2026-06-27-014x-closeaudit (Bloque 2 del cierre full-audit sobre los commits c2ff098/e1b1030).
- **Problema (VERIFICADO en mutacion):** WOT-2026-014e endurecio con barrera real el arg-branch
  (`test_resolve_motor_root_arg_branch_returns_resolved_path` asserta su precondicion
  `raw_path != raw_path.resolve()`, mutation-verified). Pero tres tests del link-branch
  -`test_motor_link.py::test_resolve_motor_root_returns_resolved_path`,
  `test_run_gates_dispatch.py::test_resolve_motor_root_path_returns_resolved_path`,
  `test_check_destino_publish_ready.py::test_resolves_motor_from_link_json`- son FALSE-GREEN
  en Windows/NTFS: alimentan `str(tmp_path/...)` que ya es canonico, asi que `Path(x) == Path(x).resolve()`
  pasa con y SIN el `.resolve()` de `runtime/motor_link.py:43`. VERIFICADO por mutacion durante el cierre:
  quitar `.resolve()` del canonico dejo esos 3 tests en verde (no detectan la regresion). El docstring de
  uno admite "may not be canonical on all FSes" pero nunca asserta la precondicion.
- **Objetivo:** dar barrera real al `.resolve()` del link-branch del canonico: alimentar una ruta
  NO canonica (p.ej. `sub/..`) como ya hace el arg-branch test endurecido, de modo que sin el `.resolve()`
  el test FALLE.
- **Criterio binario de cierre:** mutation-verified: quitar `.resolve()` de `runtime/motor_link.py:43`
  hace FALLAR al menos un test del link-branch; con el fix, verde. La evidencia de cierre cita el SHA motor.
- **Non-goal:** no reescribir el arg-branch test (ya correcto); no tocar la logica de resolucion, solo el test.


### WOT-2026-014k - Tension de orden entre Bloque 1.3bis (escribir follow-ups) y Bloque 3 (arbol limpio) del cierre full-audit
- **Prioridad:** Baja
- **Scope:** motor/closeout-hygiene
- **Estado:** pending (detectado en vivo durante el cierre full-audit de la sesion 2026-06-27)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Reactivation:** -
- **Origen:** session-2026-06-27-014x-closeaudit (reproducido en vivo: prepush --closeout-mode bloqueo el cierre por backlog.md sucio).
- **Problema (VERIFICADO en vivo):** `prompts/orchestrator_session_close_full_audit.md` Bloque 1.3bis
  ordena ESCRIBIR los follow-ups del motor en `<destino>/.agent/collaboration/backlog.md` SIN commitear
  (la regla de cola viva reserva ese commit a humano/Manager). Pero el Bloque 3 (`--session-close`) corre
  `prepush_check --closeout-mode` -> `delivery_hygiene_check.check_git_tree_clean`, cuya allowlist
  (`EXPECTED_CLOSEOUT_RUNTIME_ARTIFACTS = ["session_close_report.md"]`) NO incluye `backlog.md`. VERIFICADO:
  con `--closeout-mode`, `session_close_report.md` SI se perdona (014a funciona), pero `backlog.md` modificado
  por el propio Bloque 1.3bis deja el arbol sucio y BLOQUEA el cierre (exit 1). Asi, registrar cualquier
  follow-up durante el cierre full-audit se auto-bloquea el cierre operativo.
- **Objetivo:** eliminar la contradiccion entre los dos bloques. Opciones a evaluar al activar (NO congeladas):
  (A) que el cierre full-audit registre los follow-ups en backlog DESPUES del `--session-close`, no antes;
  (B) anadir `backlog.md` a una allowlist de cierre SOLO cuando el unico cambio es una fila/ficha de follow-up
  con evidencia (riesgo: no enmascarar trabajo productivo); (C) que Bloque 1.3bis emita la ficha pegable como
  fallback y el humano la integre fuera del arbol del cierre. Decidir con cuidado de no debilitar el gate.
- **Criterio binario de cierre:** un cierre full-audit que registra >=1 follow-up de motor con evidencia
  completa el `--session-close` en verde sin commitear el follow-up via el closeout y sin enmascarar cambios
  productivos no esperados; barrera mutation-verified que reproduzca el bloqueo actual. La evidencia cita el SHA motor.
- **Non-goal:** no debilitar `delivery_hygiene_check` para artefactos NO esperados; no auto-commitear el backlog
  via el closeout (rompe el contrato de cola viva).
