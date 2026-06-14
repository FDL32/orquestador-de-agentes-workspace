# Work Plan: WOT-2026-004b - Motor: seed .gitleaks.toml + politica generic-api-key-on-SHA + fix guard \.git over-match

## Metadata
- **ID:** WOT-2026-004b
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor (orquestador_de_agentes)
- **Titulo:** Seed `.gitleaks.toml` portable en el bundle + politica generic-api-key-on-SHA en logs operativos + fix del over-match `\.git` del guard
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Medio (toca hook de seguridad; reversible via git)
- **Depende de:** WOT-2026-004a (completed)
- **Origen:** session-2026-06-14-session-close (backlog destino, scope motor)

## Decision Arquitectonica
El motor es la fuente canonica de seguridad portable: el guard `\.git` y el seed de
gitleaks viven UNA vez en el motor y los destinos los heredan. Se elige (1) anclar el
patron `.git` a segmento de ruta (en vez de relajar el guard o moverlo a allowlist por
destino) porque el over-match es un bug de precision, no de politica: el contrato
fail-closed sobre `.git/` interno se preserva intacto. Se elige (2) un seed GENERICO en
`agent_system/templates/` con allowlist por PATH (no por valor) porque los falsos
positivos estructurales (SHA git de 40 hex en logs operativos) son comunes a todo
destino, mientras que los falsos positivos por valor concreto (placeholders, SHAs
puntuales) son especificos y deben añadirse por destino. Se elige (3) copia no-clobber
en el installer para no pisar la personalizacion del destino (p.ej. la de 004a). Esta
separacion generico-vs-especifico es deliberada: evita que el seed se convierta en un
agujero de seguridad que oculte secretos reales en cualquier ruta.

## Contrato canonico que protege el cambio
1. **Guard fail-closed pero preciso:** `guard_paths.py` debe seguir bloqueando el
   directorio interno `.git/` y rutas sensibles, pero NO debe bloquear escrituras
   legitimas a `.github/`, `.gitignore`, `.gitleaks.toml`, `.gitattributes`,
   `.gitmodules` (over-match actual del patron substring `\.git`).
2. **Portabilidad del bundle:** un destino nuevo debe recibir un `.gitleaks.toml`
   seed generico (useDefault) para que su CI con `fetch-depth: 0` no rompa por
   falsos positivos estructurales (SHA git en logs operativos), SIN heredar los
   falsos positivos especificos de ESTE destino (placeholder didactico, SHA concreto).
3. **No clobber:** el installer NO debe sobreescribir un `.gitleaks.toml` ya
   personalizado en el destino (p.ej. el de WOT-2026-004a).

## Bug confirmado (recon orquestador)
`guard_paths.py`:
- `PROTECTED_PATH_PATTERNS` incluye `r"\.git"` (linea ~24).
- `_is_protected_path` hace `path_str = str(path_obj)` y luego
  `_matches_any_pattern(path_str, PROTECTED_PATH_PATTERNS)` con `re.search`.
- `re.search(r"\.git", "...\\.github\\workflows\\ci.yml")` -> MATCH. Tambien
  `.gitignore`, `.gitleaks.toml`. Resultado: Write/Edit bloqueado como
  "ruta protegida por patron: \.git" (fail-closed sobre rutas legitimas).
- Nota Windows: `str(path_obj)` resuelve con backslashes; el fix debe normalizar
  separadores antes de anclar el patron (`_normalize` ya existe en el modulo).

## Files Likely Touched (repo_motor)
.agent/hooks/guard_paths.py
agent_system/templates/gitleaks.config.toml
scripts/install_agent_system.py
tests/test_guard_paths.py
tests/unit/test_install_agent_system.py
MANIFEST.distribute

Notas (fuera de la lista de rutas, para no romper el parser de scope):
- `guard_paths.py`: fix del patron `\.git` + normalizacion de path_str.
- `gitleaks.config.toml`: NUEVO seed generico portable.
- `install_agent_system.py`: `copy_gitleaks_config()` no-clobber + wiring install/sync.
- `tests/...`: barrera del guard + no-clobber del installer.
- `MANIFEST.distribute`: planificado, NO tocado (ver desviacion en execution_log).

## Read/inspect only
- `<destino>/.gitleaks.toml` (artefacto 004a; referencia de que NO debe heredarse
  literalmente; NO editar desde este ticket)
- `scripts/install_agent_system.py::copy_repomix_config` (patron a imitar)
- `agent_system/templates/` (layout de templates existente)

## Manager-only
- Doble revision adversarial (deliverable_type=code).
- Verificar barrera: el test del guard DEBE fallar con el patron viejo `\.git` y
  pasar con el fix (demostrar que bloquea lo que promete bloquear y permite lo legitimo).
- Verificar no-clobber del installer con evidencia (destino con config previa no se pisa).
- `check_motor_pristine --check` (este ticket SI toca el motor: el head cambiara;
  la integridad se evalua como "solo los archivos del ticket", no "motor intacto").

## Non-goals
- NO tocar el `.gitleaks.toml` del destino (004a) ni sus regexes especificos.
- NO cambiar otros patrones del guard (`.env`, `privada`, etc.).
- NO cambiar el comportamiento fail-closed del guard ante link/motor ausente.
- NO añadir dependencias nuevas (stdlib + tooling existente).

## Criterios binarios de cierre
- [ ] Guard: Write/Edit a `.github/workflows/x.yml`, `.gitignore`, `.gitleaks.toml`,
      `.gitattributes` -> NO bloqueado (evaluate_tool_request devuelve 0).
- [ ] Guard: Write/Edit a `.git/config` o cualquier `.git/<interno>` -> bloqueado (exit 2).
- [ ] Test nuevo que falla con el patron viejo `\.git` y pasa con el fix (barrera real).
- [ ] Seed `agent_system/templates/gitleaks.config.toml` existe: useDefault=true,
      documenta la politica generic-api-key-on-SHA para logs operativos, y NO contiene
      los regexes especificos del destino (sk_live_1234567890 / el SHA concreto).
- [ ] `install_agent_system.py` copia el seed a `<destino>/.gitleaks.toml` SOLO si no
      existe (no-clobber), con test que lo demuestre.
- [ ] `MANIFEST.distribute` lista el template seed.
- [ ] `ruff check` limpio sobre archivos Python tocados; `run_pytest_safe.py` del motor verde.
- [ ] `agent_controller --validate --project-root .` (destino) 0/0 (no debe verse afectado).
- [ ] Commit(s) en repo_motor con `WOT-2026-004b` en el mensaje.

## STOP / escalado
- Si el fix del guard requiere cambiar la semantica de otros patrones para funcionar,
  parar y acotar: este ticket solo arregla `\.git`.
- Si seedear el `.gitleaks.toml` requiere cambiar el contrato del installer mas alla de
  una copia no-clobber (p.ej. tocar la maquinaria de allowlist/copytree), abrir follow-up.
- Si la politica generic-api-key-on-SHA no puede expresarse sin ocultar secretos reales
  (allowlist demasiado amplia), parar: preferir allowlist por PATH de superficies de log
  operativo, no por regex amplio de 40-hex.

## Gates (deliverable_type: code)
- `ruff check <archivos .py tocados>` y `ruff format --check`.
- `python scripts/run_pytest_safe.py` con cwd=repo_motor (target = motor; incluye tests nuevos).
- `agent_controller --validate --project-root .` (destino) 0/0.
- `check_motor_pristine --check` vs snapshot (espera: solo los archivos del ticket).

## Entregables
- `guard_paths.py` con patron `.git` anclado a segmento de ruta + normalizacion.
- `agent_system/templates/gitleaks.config.toml` seed portable generico.
- `copy_gitleaks_config()` no-clobber en el installer + wiring.
- `MANIFEST.distribute` actualizado.
- Tests de barrera (guard) y de copia (installer).
- `orchestrator_pipeline/reports/closeout_WOT-2026-004b.md`.
