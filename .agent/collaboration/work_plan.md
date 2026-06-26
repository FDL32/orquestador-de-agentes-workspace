# Plan de Trabajo: WOT-2026-014c

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-014c
- **Estado:** COMPLETED
- **Titulo:** Hacer que el tree-scan de classify_publication respete .gitignore
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014C-001
- **Plan-Link:** PLAN-014C-001
- **Builder clarification budget:** 0 (la premisa, FLT, barrera primaria y
  criterios binarios ya fijan el cambio minimo y evitan decisiones abiertas)

## Objetivo
Cambiar `scripts/classify_publication.py` para que el tree-scan opere sobre lo
que git publicaria de verdad (`tracked + untracked no ignorado`) en vez de
recorrer el disco completo, y dejar una barrera automatica en
`tests/test_classify_publication.py` que falle si reaparece el falso positivo
contra archivos git-ignored.

## Premise
La implementacion actual de `classify_publication` mezcla dos universos
distintos: el history-scan ya opera sobre blobs commiteados, pero el tree-scan
monta `untracked = _walk_repo_files(...) - tracked` y `_walk_repo_files()`
recorre el disco via `repo_root.rglob("*")` con una lista hardcodeada de
directorios a saltar. Eso mete en el analisis archivos git-ignored que git no
publicaria. El fix correcto es de alcance, no de regex ni de deteccion de
secretos: el universo del tree-scan debe salir de git, no del filesystem.

## Premise Re-check (cwd=repo_motor, solo lectura)
```powershell
rg -n "_collect_repo_files|_walk_repo_files|_scan_tree_secrets|_scan_history_secrets|gitignore_proposed" scripts/classify_publication.py
rg -n "ignored|gitignore|untracked|tree_secret_scan|history_secret_scan" tests/test_classify_publication.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

Condicion de arranque (VERIFICABLE):
- `scripts/classify_publication.py` sigue obteniendo el universo del tree-scan
  desde `_walk_repo_files(...)` o equivalente basado en disco, no desde
  `git ls-files -co --exclude-standard`.
- `tests/test_classify_publication.py` todavia no cubre de forma explicita la
  matriz completa `ignored / tracked / untracked-no-ignored`.
- `validate` del workspace sigue en `0 errors / 0 warnings` antes de tocar el
  ticket.

Si esta premisa no reproduce, PARA y documenta el drift antes de modificar
codigo o tests.

## Decision Arquitectonica
La fuente de verdad del universo publicable debe ser git. Por tanto,
`_collect_repo_files()` debe construir:
- `tracked` desde `git ls-files`
- `untracked` desde `git ls-files --others --exclude-standard`

`runtime_excludes` (por ejemplo `out_path`) se conserva como filtro adicional
local del script, pero no sustituye a `.gitignore`.

Consecuencias:
- `history_scan` NO se toca.
- no se introduce parser propio de `.gitignore`.
- `_walk_repo_files()` solo puede sobrevivir si queda claro que ya no define el
  universo del tree-scan; si queda muerto, eliminarlo es aceptable.

## Plan - secuencia minima fija
### Paso 1 - reconfirmar seam y cobertura actual
- Confirmar en `scripts/classify_publication.py` que el tree-scan depende de
  `_collect_repo_files()` y que la version previa todavia toma archivos desde
  disco.
- Confirmar en `tests/test_classify_publication.py` la cobertura existente y
  localizar el mejor bloque para anadir la matriz nueva sin crear archivo
  paralelo.

### Paso 2 - acotar el universo del tree-scan a git
- Reescribir `_collect_repo_files()` para usar git como autoridad del universo
  publicable.
- Mantener la separacion `RepoFiles(tracked=..., untracked=...)`.
- Mantener `runtime_excludes` para que el artefacto de salida no se autoescanee.

### Paso 3 - barrera mutation-verified
- Anadir o ajustar tests en `tests/test_classify_publication.py` para cubrir
  simultaneamente:
  - archivo git-ignored con `API_KEY=...` -> NO debe ser flagueado por
    `tree_secret_scan`.
  - archivo tracked con `API_KEY=...` -> SI debe ser flagueado.
  - archivo untracked pero no ignorado con `API_KEY=...` -> SI debe ser
    flagueado.
- Verificar explicitamente el fail-sin-fix de la fila `ignored`: sin el cambio
  del universo, ese caso debe disparar `DECIDE` o `BLOQUEADO_POR_SECRETO`.

### Paso 4 - gates focales y cierre
- Ejecutar la bateria focal del ticket.
- Registrar evidencia literal en `execution_log.md`.
- Preparar el commit productivo del `repo_motor` con `WOT-2026-014c` en el
  mensaje.

## Files Likely Touched (relativos a repo_motor)
- `scripts/classify_publication.py`
- `tests/test_classify_publication.py`

Aclaraciones (no parte de las rutas):
- `scripts/classify_publication.py`: el cambio debe quedar localizado en el
  seam que define el universo del tree-scan; no redisenar la clasificacion
  completa.
- `tests/test_classify_publication.py`: extender la suite existente con la
  matriz nueva; no abrir un archivo de test paralelo para el mismo seam.

## Read/inspect only
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md`
- `docs/KNOWN_FAILURE_PATTERNS.md`
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\AUDIT_WOT-2026-014c.md`

## Forbidden Surfaces
- `scripts/classify_publication.py` fuera del seam del universo publicable:
  `_scan_history_secrets`, regex de secretos, buckets de clasificacion y
  veredictos globales quedan read-only salvo ajuste estrictamente derivado del
  fix de alcance.
- `tests/` fuera de `tests/test_classify_publication.py`: prohibido abrir una
  segunda suite para este seam.
- `docs/KNOWN_FAILURE_PATTERNS.md`, `README.md`, `CHANGELOG.md`: contexto
  read-only en esta ronda; no forman parte del entregable productivo.
- `repo_motor/.agent/**`, `repo_motor/bus/**`, `repo_motor/runtime/**`:
  fuera de scope.
- nuevas dependencias, parser custom de `.gitignore`, cambios en el
  history-scan o en la politica de secretos fuera del universo de entrada:
  prohibido.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```powershell
python -m pytest tests/test_classify_publication.py -q
python -m ruff check scripts/classify_publication.py tests/test_classify_publication.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO tocar `_scan_history_secrets()` ni reinterpretar la historia git.
- NO resolver aqui falsos positivos intra-archivo como FP-010.
- NO restringir el universo a solo `git ls-files` si eso elimina la deteccion
  de `untracked` publicables.
- NO introducir una allowlist de archivos ignorados como parche puntual; la
  correccion debe ser de clase, basada en git.

## CONTRACT_GAP / STOP
- Si el fix exige tocar regex de secretos, buckets o veredictos globales fuera
  del seam del universo publicable.
- Si la matriz `ignored / tracked / untracked-no-ignored` no puede expresarse
  de forma estable dentro de `tests/test_classify_publication.py`.
- Si aparece una dependencia no prevista de `_walk_repo_files()` en otra ruta
  semantica del script que no sea el tree-scan.
-> emitir `CG-WOT-2026-014c.md` y PARAR.

## DoD (binario, comandos exactos)
- [x] `python -m pytest tests/test_classify_publication.py -q` pasa.
- [x] Existe una barrera automatica en `tests/test_classify_publication.py`
  donde un archivo git-ignored con `API_KEY=...` NO activa
  `tree_secret_scan`; al reintroducir un universo basado en disco, esa barrera
  FALLA.
- [x] La misma suite confirma que un archivo tracked con `API_KEY=...` SI se
  detecta.
- [x] La misma suite confirma que un archivo untracked pero no ignorado con
  `API_KEY=...` SI se detecta.
- [x] `python -m ruff check scripts/classify_publication.py tests/test_classify_publication.py`
  -> `All checks passed`.
- [x] `python scripts/run_pytest_safe.py --level all` -> `last-run.json` con
  `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [x] `python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
  -> `0 errors / 0 warnings`.
- [x] La evidencia de cierre cita el SHA del commit del `repo_motor` que
  contiene el fix.
  SHA verificado: `0c412f08f053ca34518433820017d31b277de0cf`.

## Handoff
Commit productivo en `repo_motor` (mensaje con `WOT-2026-014c`), suite
canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. No hacer push
hasta OK humano.
