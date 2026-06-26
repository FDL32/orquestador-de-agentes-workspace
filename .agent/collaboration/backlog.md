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
| Media | WOT-2026-014a | closeout self-dirty: prepush (delivery_hygiene) bloquea por el session_close_report.md que el cierre escribe | motor/closeout-hygiene | pending | - | session-2026-06-26-cleanup-triage | - |
| Media | WOT-2026-014b | run_pytest_safe asume pytest; falso rojo en repos destino que usan unittest | motor/test-runner-portability | pending | - | session-2026-06-26-extractor-EXF-2026-005a | - |
| Alta | WOT-2026-014d | Re-encodar SKILL.md builder-self-audit + ampliar SUSPICIOUS_CODEPOINTS del guard | motor/devex-encoding | pending | - | session-2026-06-26-docs-audit | - |
| Media | WOT-2026-014e | Unificar resolve_motor_root en motor_link (drift .resolve() ausente) | motor/topology-resolution | pending | - | session-2026-06-26-docs-audit | - |
| Media | WOT-2026-014f | Unificar helpers de descubrimiento/parseo de manager_feedback (3 copias -> 1 canonica importada) | motor/closeout-hygiene | pending | - | session-2026-06-26-docs-audit | - |
| Media | WOT-2026-014g | Desync frontmatter name vs carpeta en 6 skills + gate name==dir ausente | motor/skills-discovery | pending | - | session-2026-06-26-docs-audit | - |
| Baja | WOT-2026-014h | Extraer scope-verification del orquestador.py DEPRECATED | motor/legacy-deprecation | pending | - | session-2026-06-26-docs-audit | - |
| Baja | WOT-2026-014i | Bump GitHub Actions a versiones no-Node20 (checkout/setup-python/upload-artifact) en workflows motor+workspace | ci/actions-version-bump | pending | - | session-2026-06-26-security-audit-flake | - |
> Solapamiento `011e <-> 010m`: resuelto como `keep-both-with-boundary` (011e = paralelizacion runner local opt-in; 010m = piloto xdist en CI). No fusionar; respetar la frontera local-vs-CI.

## Fichas detalladas (tickets vivos)

> Familia 013e-013j CERRADA (`completed`, confirmado en bus): `013e` inventario de suite; `013f` podo `tests/deprecated/`; `013g` explico el coste `unknown` (purge de sandbox); `013h` elimino el limbo recurrente `archive_rename_uncommitted` (staging en origen); `013i` arreglo el purge no-op por `PermissionError` en `.git` read-only; `013j` blindo el drift backlog<->contrato FLT con gate ejecutable. `013m` (overall_status del closeout respeta blocking=False) quedo ENTREGADO Y VERIFICADO fuera del lifecycle de bus (commit motor 3bbfea2, 62 tests verdes, --session-close --dry-run paso de FAIL a WARN): movido a historico como implemented-and-verified, sin eventos de bus por no haberse bootstrappeado como ticket activo. `013n` cerro canonico 2026-06-22: el motor reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales honestos sin falsear `COMPLETED`. `013o` CERRO COMPLETED en el bus (terminal) pero contra TARGET EQUIVOCADO: saneo `repo_destino/observations.jsonl` (limpio, 17 errores) y dejo SIN sanear el `repo_motor/observations.jsonl` (168 errores --strict, VERIFICADO 2026-06-25). NO se reabre (ID terminal); el saneamiento real del MOTOR se trato como ticket NUEVO `013s`, ya cerrado canonico y movido a historico. `013r` ya cerro canonico 2026-06-25: corrigio el mock-drift de `test_upgrade.py` con DoD enmendado a barrera de binding y dejo `013t` como deuda estructural opcional. ``013v`` ya cerro canonico 2026-06-25: hizo explicita la semantica de `reviews/` por `mtime` de directorio sin tocar el algoritmo de orden, y la blindo con help/docstring/tests. `013l`, `013v` y `013k` quedan resueltos como familia de bajo riesgo en runtime-retention gitignored. `013t` YA CERRO CANONICO 2026-06-25 (COMPLETED + SUPERVISOR_CLOSED en bus, commit motor `a1b99af`): un unico owner editable de `UpgradeManager` (`scripts.upgrade_agent_system`) con `scripts.upgrade` como re-export y copy-seam shutil/datetime inequivoco. La familia 013 queda CERRADA sin tickets vivos. El historico util (events/archive, audits, _archive/plan_audit) NO se poda. `002c` (`completed-partial`) y `256a` (`blocked` externo) siguen fuera por naturaleza.


### WOT-2026-014a - closeout self-dirty: prepush bloquea por su propio reporte
- **Prioridad:** Media
- **Scope:** motor/closeout-hygiene
- **Estado:** pending (identificado en la pasada de limpieza 2026-06-26; reproducido en vivo esta sesion).
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-cleanup-triage (triage adversarial de items diferidos).
- **Problema (VERIFICADO en codigo + en vivo):** `scripts/session_closeout.py` escribe su
  reporte real en `.agent/runtime/memory/session_close_report.md` (`REPORT_REL`, **tracked**,
  se commitea en cada cierre). El paso 2 del pipeline, `prepush_check` ->
  `delivery_hygiene_check.check_git_tree_clean` (`scripts/delivery_hygiene_check.py:~260`),
  corre `git status --porcelain` **sin allowlist** y marca ese reporte como arbol sucio,
  abortando el cierre (exit 1, bloqueante). En cambio el paso 25,
  `closeout_steps/rotation.py:step_git_clean` (~linea 389), SI tiene allowlist
  (`expected_patterns` incluye `session_close_report.md`) y lo perdona. La asimetria hace
  el cierre **circular**: si una corrida previa dejo el reporte sin commitear, la siguiente
  corrida falla en su propio artefacto. Esta sesion obligo a `git checkout` del reporte
  para conseguir un arbol limpio antes de que `--session-close` pasara.
- **Aclaracion (premisa falsa descartada):** un subagente afirmo "el reporte esta gitignored,
  no puede bloquear prepush" -> **FALSO**: `git ls-files` confirma que esta tracked y SI
  bloqueo en vivo. No es by-design limpio.
- **Decision congelada para materializacion:** **Opcion A**.
  El ticket debe extraer una allowlist/constante compartida para artefactos runtime
  esperados del closeout y aplicarla solo en la ruta de higiene relevante para el
  cierre, sin debilitar el gate pre-push general frente a cambios productivos no
  esperados. **Opcion B** y **Opcion C** quedan descartadas en esta ronda:
  auto-commit del reporte altera el contrato del cierre y mover el reporte a ruta
  gitignored abre un cambio de producto/artefacto mayor que no se necesita para
  cerrar el bug reproducido.
- **Objetivo:** eliminar la circularidad sin debilitar el gate pre-push general, con barrera
  que reproduzca el bloqueo (reporte sucio -> prepush falla) y verifique que el fix lo resuelve.
- **Criterio binario de cierre:** una segunda corrida consecutiva de `--session-close --force`
  (con el reporte de la primera sin commitear) NO falla en delivery_hygiene por el propio
  reporte; y un test de barrera reproduce el bloqueo previo (mutation-verified: sin el fix, FALLA).
- **Non-goal:** no debilitar `delivery_hygiene_check` para artefactos NO esperados; no tocar
  el contrato de `prepush_check` para usos fuera del closeout.
- **STOP/escalado:** si la opcion elegida implica cambiar el contrato de un gate pre-push
  usado fuera del closeout, escalar a decision humana antes de implementar.
- **Riesgos:** falso verde si la allowlist es demasiado amplia (permitiria pushear con trabajo
  real sin commitear); por eso la barrera debe distinguir "reporte runtime esperado" de
  "cambio productivo sin commitear".


### WOT-2026-014b - run_pytest_safe debe soportar repos destino en unittest
- **Prioridad:** Media
- **Scope:** motor/test-runner-portability
- **Estado:** pending (identificado al operar un repo_destino real: Extractor_Facturas_PDF_Seguro, EXF-2026-005a, 2026-06-26).
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26 cerrando EXF-2026-005a en el destino Extractor (app en unittest, sin pytest declarado).
- **Problema (VERIFICADO en vivo):** `scripts/run_pytest_safe.py` asume que el `.venv` del
  destino tiene **pytest**. Un `repo_destino` que vive en **unittest** (caso real:
  Extractor tiene 25 `unittest.TestCase`, pytest NO en su pyproject) produce un **falso
  rojo** en el gate canonico `run_pytest_safe --level all` (`No module named pytest`)
  aunque la suite real pase 25/25 con `python -m unittest`. Acopla "suite canonica" a un
  runner concreto, rompiendo la agnosticidad del motor frente a destinos no-pytest.
- **Workaround usado (parche operativo, NO arquitectura):** `uv pip install pytest` solo en
  el `.venv` del destino (sin tocar su pyproject/uv.lock); pytest descubre y corre los
  unittest nativamente. Desbloquea pero no resuelve la desalineacion de fondo.
- **Objetivo:** que `run_pytest_safe` detecte el runner (pytest si esta instalado; fallback a
  `python -m unittest discover` si no) y emita `last-run.json` igual en ambos modos, con el
  mismo criterio `tested_commit_sha == HEAD`. Opcionalmente: declarar el runner canonico del
  destino en un sitio estable (pyproject/config/contrato) para eliminar la ambiguedad.
- **Criterio binario de cierre:** sobre un destino unittest SIN pytest instalado,
  `run_pytest_safe --level all` corre la suite unittest, sale EXIT 0 si pasa, y escribe
  `last-run.json` con `tested_commit_sha`, `exit_code` y `level`; un test de barrera
  reproduce el falso rojo previo (sin el fix, FALLA por `No module named pytest`).
- **Non-goal:** no cambiar el contrato de gates para repos que SI usan pytest; no imponer un
  runner unico a los destinos.
### WOT-2026-014d - Re-encodar a UTF-8 limpio skills/builder-self-audit/SKILL.md y ampliar SUSPICIOUS_CODEPOINTS del encoding_guard al rango Latin-1 supplement suelto
- **Prioridad:** Alta
- **Scope:** motor/devex-encoding
- **Estado:** pending (detectado en la auditoria docs/scripts 2026-06-26)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-docs-audit (auditoria adversarial de scripts/prompts/skills del motor)
- **Problema (VERIFICADO en codigo):** `skills/builder-self-audit/SKILL.md` (skill OBLIGATORIA del gate de calidad) tiene ~29 lineas con mojibake / bytes Latin-1 supplement sueltos (rango 0x80-0x9F mas 0xC0, 0xC6, 0xDC, 0xDD); p.ej. `skills/builder-self-audit/SKILL.md:55` tiene un byte Latin-1 espurio (codepoint 0xC0) en el header del Paso 1, donde deberia ir un em-dash. La corrupcion afecta los marcadores OK/Error/separador de los Pasos 1-7. El gate de encoding reporta un falso EXIT=0 porque los codepoints corruptos (0x94, 0xC0, 0xC6, 0xDC, 0xDD, 0x85, 0x8C, 0x92) NO estan en `SUSPICIOUS_CODEPOINTS` de `scripts/encoding_guard.py:28-35` (= {0x00C3, 0x00C2, 0x00E2, 0x00F0, 0x0102, 0xFFFD}): el guard caza el lead-byte del doble-encoding canonico pero NO esta corrupcion concreta, asi que pasa en verde (drift silencioso). El dano es preexistente, arrastrado en el rename WOT-2026-008j (commit 9d1d75b), y afecta a un solo archivo. Importa para los agentes porque builder-self-audit es obligatoria antes de marcar cualquier tarea completada (la invocan builder-implement-from-plan Paso 6 y project-finalize Paso 9): el agente recibe simbolos sin significado justo en la skill que define el gate, y el guard no lo bloquea.
- **Objetivo:** Re-encodar `skills/builder-self-audit/SKILL.md` a UTF-8 limpio (marcadores OK/Error/separador coherentes con el resto de skills) y endurecer `scripts/encoding_guard.py` con una BARRERA ROBUSTA POR CLASE, NO una lista negra de bytes especificos (que seria gato-y-raton y dejaria pasar la proxima corrupcion impredecible): (i) flaguear TODO el rango de control C1 `0x80-0x9F` como clase -sin uso legitimo en texto, cubre 0x85/0x8C/0x92/0x94-; (ii) anadir `content.decode('utf-8', errors='strict')` como capa COMPLEMENTARIA para bytes UTF-8 invalidos. PRECISION VERIFICADA: este archivo decodifica como UTF-8 VALIDO (0 U+FFFD), asi que la corrupcion son codepoints validos-pero-erroneos y `strict` SOLO NO la detecta -> el chequeo de rango C1 es el que la atrapa; `strict` cubre la otra clase (bytes invalidos). Los Latin-1 espurios (0xC0/0xC6/0xDC/0xDD) son letras legitimas mal usadas: el re-encode del archivo las corrige, pero el guard NO puede prohibirlas en bloque (romperia texto valido).
- **Criterio binario de cierre:** (a) `skills/builder-self-audit/SKILL.md` arroja 0 matches de bytes de control C1 (0x80-0x9F) y los Latin-1 espurios quedan corregidos a su caracter intencional (em-dash/marcador); (b) los marcadores unicode del archivo quedan coherentes con el resto de skills del ecosistema; (c) **BARRERA PRIMARIA DE CIERRE** (mutation-verified): tras endurecer el guard, `check_encoding_guard` FALLA (exit!=0) si se reinyecta (i) cualquier control char C1 del rango 0x80-0x9F o (ii) un byte UTF-8 invalido. CASO NEGATIVO EXPLICITO que demuestra que strict-decode solo NO basta: una cadena que ES UTF-8 valido pero contiene un control char C1 (p.ej. U+0094) debe PASAR `decode('utf-8',errors='strict')` y AUN ASI ser flagueada por el chequeo de rango; ademas el guard ANTES del fix deja pasar el caso real de builder-self-audit mientras el endurecido lo bloquea; (d) la evidencia de cierre cita el SHA del commit motor que contiene el fix (convencion del backlog, p.ej. 013t cito a1b99af).
- **Non-goal:** No re-encodar las otras 30 skills ni normalizar lineas en blanco del ecosistema; el alcance se limita estrictamente a este archivo (`skills/builder-self-audit/SKILL.md`) y al set `SUSPICIOUS_CODEPOINTS` del guard.


### WOT-2026-014e - Unificar lectura de motor_root en runtime.motor_link (drift de .resolve() ausente en copia divergente)
- **Prioridad:** Media
- **Scope:** motor/topology-resolution
- **Estado:** pending (detectado en la auditoria docs/scripts 2026-06-26)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-docs-audit (auditoria adversarial de scripts/prompts/skills del motor)
- **Problema (VERIFICADO en codigo):** `runtime/motor_link.py:21-46` es el canonico declarado ("single point of truth") para resolver el motor root desde `motor_destination_link.json` y devuelve `Path(motor_root).resolve()` (linea 43, ruta absoluta normalizada). Pese a ello, DOS scripts reimplementan la lectura del mismo JSON en vez de importar el canonico: `scripts/run_gates_dispatch.py:46-60` (`resolve_motor_root_path`) y `scripts/check_destino_publish_ready.py:57-70` (`_resolve_motor_root`). Estas copias ya divergieron en silencio: `scripts/check_destino_publish_ready.py:67` retorna `candidate` SIN `.resolve()`, mientras que `scripts/run_gates_dispatch.py:59` (`candidate.resolve()`) y el canonico (linea 43) SI resuelven. `scripts/check_deliverables_exist.py` ya consume el canonico (viabilidad de importacion probada). El drift del `.resolve()` ausente es la prueba de que las copias divergieron sin deteccion: un agente que modifique la topologia motor/destino debe encontrar y editar 3 copias en vez de 1.
- **Objetivo:** Que `scripts/run_gates_dispatch.py` y `scripts/check_destino_publish_ready.py` importen `resolve_motor_root` de `runtime.motor_link` como unica fuente de resolucion del motor root, conservando localmente solo la precedencia `arg > env > link` (no la relectura del JSON).
- **Criterio binario de cierre:** (1) Ambos scripts importan `resolve_motor_root` de `runtime.motor_link` y ya no reabren `motor_destination_link.json` para extraer `motor_root`; la precedencia local arg>env>link se conserva. (2) El grep de bloques que reabren `motor_destination_link.json` para `motor_root` (solo `runtime/motor_link.py` + consumidores legitimos de `destination_root`) queda como AYUDA de verificacion, NO como gate. (3) Ninguna ruta de codigo retorna `motor_root` sin `.resolve()`. (4) **BARRERA PRIMARIA DE CIERRE** (mutation-verified), codificada como TEST UNITARIO COMMITEADO en la suite del motor (no un check de grep en el log): inyecta un `motor_root` sin resolver y verifica que la ruta canonica lo `.resolve()`-a; sin el fix (copia que retorna el path crudo) el path sin normalizar pasa y el test FALLA. (5) La suite de tests existente queda verde. (6) La evidencia de cierre cita el SHA del commit motor que contiene el fix.
- **Non-goal:** NO tocar `scripts/encoding_post_write_hook.py` (lee otra clave, `destination_root`, consumidor distinto) ni `scripts/check_motor_destination_integration.py` (reusa `resolve_motor_link`, no duplica). No anadir un `resolve_destination_root` ni unificar la resolucion de `destination_root` en este ticket.


### WOT-2026-014f - Unificar helpers de descubrimiento/parseo de manager_feedback (3 copias triplicadas -> 1 definicion canonica importada)
- **Prioridad:** Media
- **Scope:** motor/closeout-hygiene
- **Estado:** pending (detectado en la auditoria docs/scripts 2026-06-26)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-docs-audit (auditoria adversarial de scripts/prompts/skills del motor)
- **Problema (VERIFICADO en codigo):** La premisa original de "3 copias reales" quedo
  **stale**. Hoy existen **2 implementaciones reales + 1 wrapper de compatibilidad**:
  `scripts/archive_collaboration_artifacts.py:248` (`find_manager_feedback_files`) y `:268`
  (`extract_ticket_id_from_feedback`) son la version CLI/base; `scripts/closeout_steps/archival.py:211`
  (`_find_manager_feedback_files`) y `:228` (`_extract_ticket_id_from_feedback`) son la copia
  privada real del closeout; `scripts/session_closeout.py:489-499` ya NO reimplementa, sino
  que delega mediante wrappers de compatibilidad a helpers importados. Ademas, las dos
  implementaciones reales no tienen la misma firma: la de `archive_collaboration_artifacts.py`
  usa `extract_ticket_id_from_feedback(filename: str)`, mientras la de
  `closeout_steps/archival.py` usa `_extract_ticket_id_from_feedback(filename: str, *,
  ticket_id_pattern: str)`. Sin fijar cual firma canonica gana, el ticket deja una decision
  de producto abierta al Builder.
- **Decision congelada para materializacion:** la firma canonica debe ser la del closeout,
  con `ticket_id_pattern` explicito (`filename: str, *, ticket_id_pattern: str`) porque es la
  mas general y preserva el control del patron desde el consumidor. Para eliminar la duda de
  direccion de import, la definicion canonica debe vivir en un modulo neutro e importable del
  motor (NO en `session_closeout.py`), y tanto el CLI/base como el closeout deben importar de
  ahi; `closeout_steps/archival.py` puede actuar como hogar transitorio solo si la extraccion a
  ese modulo comun queda cerrada dentro del mismo ticket, no como canonico final implicito.
- **Objetivo:** Dejar una sola definicion canonica real de cada helper de
  descubrimiento/parseo en un modulo importable del motor y que
  `archive_collaboration_artifacts.py`, `closeout_steps/archival.py` y
  `session_closeout.py` consuman esa definicion comun; `session_closeout.py` puede conservar
  wrappers de compatibilidad mientras no introduzcan una tercera implementacion real.
- **Criterio binario de cierre:** (1) Un TEST DE ARQUITECTURA COMMITEADO en la suite del
  motor afirma que existe exactamente 1 implementacion real de descubrimiento y 1 de parseo
  para `manager_feedback`; `session_closeout.py` puede conservar wrappers delgados de
  compatibilidad, pero no cuerpos logicos divergentes. (2) `archive_collaboration_artifacts.py`
  y `session_closeout.py` importan el helper canonico en vez de redefinir logica propia.
  (3) **BARRERA PRIMARIA DE CIERRE** (mutation-verified): mutar el helper canonico (via
  import-identity) cambia el comportamiento observable en CLI, paso de archival y wrapper de
  `session_closeout`; sin el fix, al menos uno de los consumidores no recibe la mutacion y el
  test FALLA. (4) La suite de tests de closeout queda verde. (5) La evidencia de cierre cita
  el SHA del commit motor que contiene el fix.
- **Non-goal:** NO unificar la politica de SELECCION de tickets (el `_can_prove_close` por bus events del closeout y la lista explicita `ticket_ids` del CLI se conservan separadas). Solo se unifican los helpers de descubrimiento/parseo.


### WOT-2026-014g - Resolver desync name: frontmatter vs nombre de carpeta en 6 skills y anadir gate name==dir en discovery
- **Prioridad:** Media
- **Scope:** motor/skills-discovery
- **Estado:** pending (detectado en la auditoria docs/scripts 2026-06-26)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-docs-audit (auditoria adversarial de scripts/prompts/skills del motor)
- **Problema (VERIFICADO en codigo):** 6 skills tienen `name:` en el frontmatter distinto del nombre de su carpeta, y el titulo del cuerpo usa el nombre largo (carpeta): `manager-create-work-plan` -> `name: create-work-plan`; `manager-review-implementation` -> `name: code-review`; `manager-resolve-escalation` -> `name: resolve-escalation`; `builder-run-quality-gates` -> `name: run-quality-gates`; `builder-self-audit` -> `name: self-audit`; `builder-write-deliverable` -> `name: write-deliverable`. La resolucion en si NO se rompe: `scripts/discover_skills.py:117` keya el dict por `skill_dir.name` (carpeta) y usa tambien triggers, asi que el `name` corto no participa del dispatch (la "colision con el builtin /code-review" es coincidencia nominal, no dispatch real). El dano es de consistencia/observabilidad: el catalogo/INDEX y `allowed_names` de `validate_skill_access` (`bus/skill_resolver.py:208`) publican el name corto mientras carpetas y titulos usan el largo, y no existe gate que detecte la divergencia (`check_skill_collisions`/`_check_skill_names` solo validan kebab-case/actor-first, nunca comparan `name` con `skill_dir.name`). Esa doble identidad obliga al agente a re-derivar a que skill corresponde cada referencia de `orchestrate-pipeline` (que las nombra por carpeta) y rompe la trazabilidad nombre<->ruta.
- **Objetivo:** Alinear identidad nombre<->ruta haciendo `name:` igual al nombre de carpeta (kebab largo) en las 6 skills, ajustar el titulo del cuerpo para que coincida, y anadir en `discover_skills`/`check_skill_collisions` una regla que falle cuando `name != skill_dir.name`.
- **Criterio binario de cierre:** Las 6 skills tienen `name:` identico al nombre de su carpeta y el titulo del cuerpo coincide; existe en `discover_skills.py` una regla que falla cuando `name != skill_dir.name`; barrera mutation-verified: un test con una skill fixture cuyo `name` difiere de su carpeta hace fallar el gate nuevo, y al retirar el gate ese mismo caso pasa silenciosamente. La evidencia de cierre cita el SHA del commit motor que contiene el fix.
- **Non-goal:** NO hacer canonico el name corto (forzaria renombrar carpetas, titulos y referencias cruzadas de `orchestrate-pipeline`); NO abordar el supuesto conflicto con el builtin `/code-review` (no es dispatch real); NO tocar las reglas existentes de kebab-case/actor-first (DEC-008D-001).


### WOT-2026-014h - Extraer la logica viva de scope-verification fuera del orquestador.py DEPRECATED
- **Prioridad:** Baja
- **Scope:** motor/legacy-deprecation
- **Estado:** pending (detectado en la auditoria docs/scripts 2026-06-26)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-docs-audit (auditoria adversarial de scripts/prompts/skills del motor)
- **Problema (VERIFICADO en codigo):** `scripts/orquestador.py` (731 lineas) lleva el banner `[DEPRECATED - WT-2026-254a]` en `scripts/orquestador.py:6-8` y conserva los adapters legacy de los engines Goose/Claw (ya retirados; Claude Code excluido por diseno). Pero el mismo archivo muerto contiene logica viva enterrada al final: `snapshot_paths` (`:518`), `detect_changed_files` (`:547`), `classify_scope` (`:566`) y `generate_scope_report` (`:629`), todas cubiertas por `tests/test_orquestador_scope.py` (12610 bytes), que importa explicitamente de `scripts.orquestador`. Como el repo se llama "orquestador_de_agentes", un agente asume que `orquestador.py` es el corazon del sistema y gasta contexto leyendo cientos de lineas de adapters Goose/Claw muertos antes de toparse con el banner DEPRECATED; la scope-verification viva queda invisibilizada dentro de un archivo marcado como historico.
- **Objetivo:** Mover las 4 funciones de scope-verification (`snapshot_paths`, `detect_changed_files`, `classify_scope`, `generate_scope_report`) a un modulo NO-deprecado (p.ej. `scripts/scope_verification.py`), reapuntar el test, y dejar `orquestador.py` como cascaron Goose/Claw sin codigo vivo consumido por otros modulos.
- **Criterio binario de cierre:** Las 4 funciones residen en el modulo nuevo no-deprecado; `tests/test_orquestador_scope.py` importa desde ese modulo nuevo (ya no desde `scripts.orquestador`) y pasa en verde; ningun consumidor importa `orquestador` como modulo Python para esa logica viva tras la extraccion, verificado mediante BUSQUEDA TRANSVERSAL (Impact Simulation, audit_agent_output 2.c): no solo en el motor sino tambien en el workspace de dogfooding (`orquestador_de_agentes_workspace`) y en cualquier destino que tenga el archivo vendorizado. NOTA VERIFICADA: `orquestador.py` NO esta en `MANIFEST.distribute`/`MANIFEST.workspace`, asi que el instalador NO lo vendoriza a destinos -> blast-radius acotado a motor + dogfooding; aun asi, si la busqueda transversal halla algun consumidor de las funciones extraidas, conservar un re-export shim en `orquestador.py` (como hizo 013t con `scripts.upgrade`) hasta confirmar 0 consumidores. La evidencia de cierre cita el SHA del commit motor que contiene el fix.
- **Non-goal:** NO borrar `scripts/orquestador.py` en este mismo cambio (la retirada total del cascaron es un follow-up posterior); el cascaron permanece pero ANTES de retirarlo en el follow-up debe verificarse que ningun modulo lo importa y que el modo `--skill` (delega via subprocess a `discover_skills.py`, no por import Python) ya no se referencia. RIESGO RESIDUAL EXPLICITO (Impact Simulation): el MANIFEST ACOTA pero NO prueba 0 consumidores -pueden existir copias manuales o consumidores fuera de manifest-; por eso la AUTORIDAD de "0 consumidores" es la busqueda transversal real (`grep -rn 'import.*orquestador|from scripts.orquestador'` en motor + workspace de dogfooding + destinos conocidos), NO el manifest. Si aparece cualquiera, re-export shim antes de vaciar. NO tocar los adapters Goose/Claw ni reintroducir esos engines.


### WOT-2026-014i - Bump GitHub Actions a versiones no-Node20 (checkout/setup-python/upload-artifact/setup-uv) en workflows del motor y del workspace
- **Prioridad:** Baja
- **Scope:** ci/actions-version-bump
- **Estado:** pending (detectado al validar en CI el fix del flake de Security Audit, sesion 2026-06-26)
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente; el fix del flake gitleaks entro como commit de CI 2d69d57 del workspace, NO como ticket)
- **Origen:** session-2026-06-26-security-audit-flake (al confirmar verde el reemplazo de gitleaks-action@v2 por el CLI OSS, la anotacion de Node-20 quedo visible en el run).
- **Problema (VERIFICADO en CI + en codigo):** Los runs de GitHub Actions emiten la anotacion
  "Node.js 20 is deprecated. The following actions ... are being forced to run on Node.js 24"
  (ref: github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners).
  VERIFICADO en el run del workspace 28269573551 (2026-06-26): `actions/checkout@v4`,
  `actions/setup-python@v5`, `actions/upload-artifact@v4`. Las mismas action-pins viven en
  AMBOS repos (lectura directa de los YAML):
  - Motor: `.github/workflows/security-audit.yml` (checkout@v4, astral-sh/setup-uv@v5,
    setup-python@v5), `quality-gates.yml` (checkout@v4, setup-uv@v5, setup-python@v5),
    `monthly-deps-bump.yml` (checkout@v4, setup-uv@v5, setup-python@v5).
  - Workspace: `.github/workflows/security-audit.yml` (checkout@v4, setup-python@v5,
    upload-artifact@v4), `quality-gates.yml` (checkout@v4 x2, setup-python@v5).
  Hoy NO bloquea: el motor lleva `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` que fuerza Node24
  y GitHub aun ejecuta los v4/v5 sobre Node24. Pero es deuda con fecha de caducidad: cuando
  GitHub retire el shim, esas pins haran hard-fail. El otro disparador historico,
  `gitleaks/gitleaks-action@v2`, ya se elimino del workspace (commit de CI 2d69d57).
- **Objetivo:** Subir cada action marcada a su major actual que ya NO targetea Node20 (VERIFICAR
  contra las releases de cada action EN EL MOMENTO de implementar; no fijar el numero aqui),
  en los workflows de ambos repos, SIN tocar la logica de los jobs. Revisar si
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` sigue siendo necesario tras el bump (probablemente
  retirable, pero solo tras confirmar que ninguna action restante lo requiere).
- **Decision a resolver al activar (cross-repo):** este ticket toca DOS repos (motor +
  workspace), cada uno con su propio `.github/`. Decidir si se ejecuta como un solo ticket de
  mantenimiento con doble superficie (commit motor + commit workspace separados) o se parte en
  dos. La `delivery_authority` declarada (repo_motor) cubre la superficie canonica; los
  workflows del workspace NO los vendoriza el motor (workspace de agente puro), asi que su bump
  es un commit workspace paralelo, no parte del diff del motor.
- **Criterio binario de cierre:** tras el bump, un push que dispare cada workflow afectado (en
  motor y en workspace) produce 0 anotaciones de Node-20-deprecation para las actions
  bumpeadas y los workflows quedan verdes. La evidencia de cierre cita el/los SHA de los
  commits (motor y workspace) que contienen el bump. **Gates canonicos del ticket al
  materializar:** al ser cambio de YAML/CI puro, la validacion principal es externa y queda
  como `Manager-only`: workflow green post-push + ausencia de anotacion Node20. Localmente, el
  Builder solo debe verificar sintaxis/estructura de los YAML tocados y `validate --json` del
  workspace; `ruff`/`pytest` no cuentan como evidencia principal del cierre de este ticket.
- **Non-goal:** NO cambiar la logica ni los pasos de ningun job (solo las versiones de las
  actions); NO re-tocar el step de gitleaks (ya migrado al CLI OSS en 2d69d57); NO retirar
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` sin confirmar antes que ninguna action restante lo
  necesita.


