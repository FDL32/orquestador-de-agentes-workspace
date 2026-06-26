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
| Media | WOT-2026-014c | tree-scan de classify_publication debe respetar .gitignore (escanear lo publicable, no el disco) | motor/publication-audit | pending | - | session-2026-06-26-extractor-adopt | - |
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
- **Decision a resolver (el ticket DEBE elegir una, no asumir):**
  - **Opcion A:** dar a `check_git_tree_clean` la misma allowlist de artefactos runtime
    esperados que `step_git_clean` (extraer `expected_patterns` a una constante compartida).
    Riesgo: la allowlist NO debe debilitar el gate pre-push **general** (delivery_hygiene se
    usa fuera del closeout). Acotar la allowlist al contexto closeout o exigir que el reporte
    este staged.
  - **Opcion B:** que el closeout **commitee** el reporte como ultimo paso (flujo previsto),
    dejando el arbol limpio; documentar que ese commit es parte del cierre.
  - **Opcion C:** mover el reporte a una ruta gitignored y dejar solo un puntero tracked.
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


### WOT-2026-014c - tree-scan de classify_publication debe respetar .gitignore (escanear lo publicable, no el disco)
- **Prioridad:** Media
- **Scope:** motor/publication-audit
- **Estado:** pending (identificado al publicar un repo_destino real: Extractor_Facturas_PDF_Seguro, sesion 2026-06-26; falso positivo DECIDE_PENDING/exit 3 documentado en AUDIT_PUBLICATION_2026-06-26_v2.md).
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depende de:** - (independiente)
- **Origen:** session-2026-06-26-extractor-adopt, cerrando EXF-2026-005a en el destino Extractor; el tree-scan bloqueo por contenido de archivos ignorados/no-trackeados.
- **Problema (VERIFICADO en codigo + reproduccion empirica):** El tree-scan de
  `classify_publication` NO respeta `.gitignore`; el history-scan, en la practica, si
  (solo ve blobs commiteados). Asimetria CONFIRMADA por lectura y por reproduccion.
  - Tree-scan: `_scan_tree_secrets` (L337-350) se alimenta de `_collect_repo_files`
    (L253-260), que arma `untracked = all_files - tracked` donde `all_files =
    _walk_repo_files(...)` (L258-259). `_walk_repo_files` (L263-285) recorre **el disco
    completo** con `repo_root.rglob("*")` (L275) y solo filtra por un set **hardcodeado**
    `ignored_dirs = {.git, .venv, venv, __pycache__, .pytest_cache, .ruff_cache,
    node_modules}` (L265-273, aplicado en L279) mas `runtime_excludes` (L282). El unico
    filtro extra dentro del scan es `_is_excluded` (L343), que usa `EXCLUDE_PATTERNS`
    hardcodeados (L48-67) menos `ALLOW_PUBLISH_PATTERNS` (L68-71), **NO** el `.gitignore`
    del repo. No hay `git check-ignore`, ni `git ls-files --others --exclude-standard`, ni
    parser de `.gitignore` en ninguna parte (grep: las unicas apariciones de "gitignore"
    son L33 como extension de texto y L609 como clave de salida `gitignore_proposed`,
    ninguna es un filtro). Resultado: cualquier archivo git-ignored que no caiga en un dir
    hardcodeado entra al universo a escanear.
  - History-scan: `_scan_history_secrets` (L361-407), alimentado por `git rev-list --all`
    + `git ls-tree -r <commit>` (L373-374) leyendo blobs con `git show` (L390). Por
    construccion solo expone contenido **commiteado** (trackeado); un archivo git-ignored
    y nunca commiteado no puede aparecer.
  - **Falso positivo concreto:** en la publicacion del Extractor el script salio
    **DECIDE_PENDING (exit 3)** (AUDIT_PUBLICATION_2026-06-26_v2.md L7, L15). El tree-scan
    leyo `.agent/context/destination_map.md` y `.agent/context/project-map.json`
    (ignorados + `git rm --cached`, siguen en disco => leidos pero NO publicados). En la
    variante exit-1 (memoria del proyecto) el disparo fue el placeholder
    `API_KEY=your_api_key_here` en un bundle legacy ignorado y no trackeado
    (`publica/repo/agent_system/docs/01-INSTALACION.md`). En ambos casos
    `tree_secret_scan.ok=false` por contenido de archivos que git NUNCA publicaria, mientras
    `history_secret_scan.ok=true` (0 findings sobre la historia). Veredicto humano de Pasada B:
    PUBLICABLE (el exit del script no es veredicto final).
- **Objetivo:** que el tree-scan opere sobre **lo que git PUBLICARIA** = trackeado +
  untracked-NO-ignorado, excluyendo SOLO lo git-ignored. Fix minimo localizado en
  `_collect_repo_files` (L253-260): obtener el universo desde git en vez de desde el disco,
  equivalente a `git ls-files -co --exclude-standard` (es decir, `tracked = git ls-files`
  + `untracked = git ls-files --others --exclude-standard`), conservando `runtime_excludes`
  (out_path) como guarda. El codigo ya invoca git por subprocess (`_git_lines`, L136-138) y
  ya separa tracked/untracked en `RepoFiles`, por lo que el cambio queda acotado;
  `_walk_repo_files` queda redundante (decidir si se elimina o se mantiene como red de
  seguridad secundaria). Verificado empiricamente que `git ls-files -co --exclude-standard`
  (a) EXCLUYE un archivo ignorado (`legacy_docs/old.md`, confirmado por `git check-ignore`)
  y (b) INCLUYE un untracked-no-ignorado (`new_untracked.md`, publicable con `git add -A`).
- **Criterio binario de cierre (matriz de aceptacion explicita, atada a los flags de git):**
  sobre un repo git de prueba, cada archivo de prueba contiene un `API_KEY=...`; el tree-scan
  corregido (universo = `git ls-files -co --exclude-standard` = trackeado `-c` cached +
  untracked-NO-ignorado `-o` others, excluyendo lo ignorado via `--exclude-standard`) debe
  satisfacer las TRES filas a la vez:
  - (a) archivo **git-ignored** (cubierto por `.gitignore`; `git check-ignore -v <path>`
    matchea; NO aparece en `git ls-files -co --exclude-standard`) -> el tree-scan **NO** lo
    flaguea (ni DECIDE ni BLOQUEADO_POR_SECRETO).
  - (b) archivo **trackeado** (`git ls-files <path>` lo lista; entra como `-c` cached) -> el
    tree-scan **SI** detecta el secreto.
  - (c) archivo **untracked pero NO ignorado** (publicable con `git add -A`; `git status` lo
    muestra `??` y `git check-ignore` NO matchea; entra como `-o` others) -> el tree-scan
    **SI** detecta el secreto.
  Falso-verde parcial a EVITAR: restringir el universo a solo `git ls-files` (sin
  `-o --exclude-standard`) pasa (a) y (b) pero **FALLA la fila (c)** -> dejaria de detectar
  secretos en untracked publicables. El history-scan permanece sin cambios.
- **Barrera sugerida (mutation-verified):** test que crea un archivo ignorado con
  `API_KEY=...` (placeholder o secreto-de-ejemplo) y verifica que el tree-scan NO lo
  flaguea; sin el fix (universo = disco via `_walk_repo_files`) el test DEBE fallar porque
  el archivo ignorado se escanea y dispara DECIDE/BLOQUEADO. Complementar con un test que
  confirme la deteccion en (b) trackeado y (c) untracked-no-ignorado para que el fix no
  degrade cobertura.
- **Non-goal:** NO tocar el history-scan (`_scan_history_secrets`, L361-407): ya es correcto
  (solo ve blobs commiteados, los git-ignored-no-commiteados no pueden aparecer). NO
  resolver aqui el **FP-010** (KNOWN_FAILURE_PATTERNS.md L463-510): ese es un modo DISTINTO
  (falso positivo INTRA-archivo por over-match lexico de palabras-cabecera dentro de un
  archivo que SI se publica; fix = endurecer la regex exigiendo valor asignado + allowlist
  de fixtures). ESTE ticket es un falso positivo de ALCANCE/SCOPE (el archivo flagueado NO
  se publica porque esta git-ignored; fix = acotar el set de entrada del scan al universo de
  git). No cerrar como duplicado de FP-010. NO imponer un comportamiento que pierda deteccion
  en untracked-NO-ignorado (restringir a solo `git ls-files` seria incorrecto: un untracked
  no-ignorado SI se publica con `git add -A`).
