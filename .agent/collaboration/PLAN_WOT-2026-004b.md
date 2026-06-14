# PLAN WOT-2026-004b - Motor: gitleaks seed + politica SHA + fix guard \.git

## Objetivo
Espejo tecnico del `work_plan.md`. Tres deliverables independientes en el repo_motor,
commiteables por separado o juntos con `WOT-2026-004b` en el mensaje.

## Pasos de ejecucion

### Paso A - Fix guard \.git over-match (`.agent/hooks/guard_paths.py`)
1. En `_is_protected_path`, normalizar el path antes de matchear patrones de ruta:
   `path_str = _normalize(str(path_obj))` (forward slashes + lower; `_normalize` ya existe).
2. En `PROTECTED_PATH_PATTERNS`, reemplazar `r"\.git"` por un patron anclado a
   segmento de ruta que matchee el directorio `.git` interno pero NO `.github`,
   `.gitignore`, `.gitleaks.toml`, `.gitattributes`, `.gitmodules`.
   Candidato: `r"(^|/)\.git(/|$)"`. Justificar la eleccion en el commit/log.
3. Verificar que el resto de patrones (`privada`, `secrets?`, `\.env`, etc.) siguen
   matcheando sobre el path normalizado (son substrings; siguen funcionando).

### Paso B - Seed portable (`agent_system/templates/gitleaks.config.toml`)
1. Crear el template generico:
   - `[extend] useDefault = true`.
   - Bloque `[allowlist]` que implemente la politica generic-api-key-on-SHA para
     logs operativos: preferir `paths` (regex de PATH) que cubran superficies de log
     del workspace donde aparecen SHAs git de 40 hex (p.ej. `\.agent/collaboration/`,
     `execution_log\.md`, `orchestrator_pipeline/`, `CHANGELOG\.md`), en vez de un
     regex amplio de 40-hex que ocultaria claves reales en cualquier sitio.
   - Comentario que explique: el seed es generico; los falsos positivos por VALOR
     especifico (placeholders didacticos, SHAs concretos) se añaden por destino, no aqui.
   - NO incluir `sk_live_1234567890` ni el SHA `9c92e3d4...` del destino.
2. Encoding UTF-8 limpio (pasar `check_encoding_guard.py`).

### Paso C - Installer no-clobber (`scripts/install_agent_system.py`)
1. Añadir `copy_gitleaks_config(template_root, destination_root, dry_run)` analoga a
   `copy_repomix_config`: origen
   `template_root/agent_system/templates/gitleaks.config.toml`, destino
   `destination_root/.gitleaks.toml`.
2. **No-clobber:** si `destination_root/.gitleaks.toml` ya existe, NO sobreescribir;
   loggear `[SKIP] .gitleaks.toml ya existe (no-clobber)` y devolver False/True segun
   convencion del modulo. Solo copiar cuando ausente.
3. Wirear la llamada en el flujo install/sync donde se invoca `copy_repomix_config`
   (misma fase de provisioning de templates root-level).

### Paso D - MANIFEST.distribute
1. Añadir `agent_system/templates/gitleaks.config.toml` bajo la seccion de templates
   (junto a repomix.config.json / PROJECT_TEMPLATE.md si estan listadas).

### Paso E - Tests (barrera real)
1. Test del guard: con el patron viejo `\.git` un Write a `.gitleaks.toml`/`.github/...`
   se bloquea; con el fix se permite, y `.git/config` sigue bloqueado. El test debe
   ejercitar `evaluate_tool_request` o `_is_protected_path` con repo_root controlado
   (tmp_path) y payloads reales (no mocks de la API equivocada).
2. Test del installer: copia seed cuando ausente; NO clobber cuando presente
   (crear un `.gitleaks.toml` previo en tmp dest y verificar que no cambia).

### Paso F - Gates + commit
1. `ruff check` + `ruff format --check` sobre `.py` tocados.
2. `python scripts/run_pytest_safe.py` con cwd=repo_motor.
3. Commit(s) en repo_motor: `fix(WOT-2026-004b): ...` y/o `feat(WOT-2026-004b): ...`.
4. `agent_controller --validate --project-root .` (destino) 0/0.

## Seams / invariantes
- El guard sigue fail-closed ante link/motor ausente y ante `.git/` interno.
- El installer es idempotente y no-clobber para `.gitleaks.toml`.
- El seed es generico: la separacion "falso positivo generico (path) vs especifico
  (valor por destino)" es el invariante de seguridad.

## Evidencia esperada
- Diff de `guard_paths.py`; salida del test que falla con patron viejo / pasa con fix.
- `cat` del seed mostrando useDefault + politica por path + ausencia de regexes de destino.
- Test de installer no-clobber (exit codes).
- `git -C <motor> log/show` del/los commit(s).
- `run_pytest_safe` exit 0; ruff exit 0; validate destino 0/0.
- `check_motor_pristine --check`: motor_status muestra solo los archivos del ticket.

## STOP
- Ver STOP del work_plan. Cualquier cambio que amplie la superficie de seguridad
  (ocultar 40-hex globalmente, tocar otros patrones, romper fail-closed) -> escalar.
