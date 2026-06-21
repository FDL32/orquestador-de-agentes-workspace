# Execution Log -- WOT-2026-013c

**Estado:** IN_PROGRESS

## MANAGER - WOT-2026-013c - Bootstrap operativo

Ticket abierto tras el cierre honesto de `011i` / `013b`: la politica de runner quedo fuera de juego y la deuda real siguiente son 3 tests global-state-bound.

Packet congelado y commiteado en repo_destino:
- backlog vivo + ficha `013c`
- `T-013C-001` en `ticket_contracts.md`
- `PLAN-013C-001` en `plan_graph.md`

Premisa operativa del Builder:
- serial del triple debe seguir verde
- xdist del triple (`-n 8 --dist load`) debe reproducir el rojo actual o confirmar que ya no pertenece a esta familia
- cualquier necesidad de tocar runner/CI/producto dispara STOP + `CG-WOT-2026-013c.md`
## BUILDER - WOT-2026-013c - Aislamiento de 3 tests global-state bajo xdist

### Fase 0 - Diagnostico (read-only)
Comandos exactos:
- Serial: `python -m pytest tests/unit/test_detect_version.py tests/unit/test_project_scanner.py tests/unit/test_no_inline_ticket_regex.py -q`
  -> 52 passed in 362s (VERDE).
- Paralelo: `uv run python -m pytest <triple> -q -n 8 --dist load`
  -> 3 failed, 49 passed. Rojo anclado EXACTAMENTE en los 3 tests del contrato.

Firma del rojo (identica en los 3):
`FileNotFoundError: [WinError 3] ...tests/sandbox/test_runtime/session_<PID>` durante `rglob`.

Tracebacks:
- test_scan_current_project: scan_project -> _collect_local_modules -> project_root.rglob("*.py").
- test_upgrade_path_suggestion: AgentSystemDetector(".") -> ProjectPathsResolver.resolve_paths -> project_root.rglob(".agent").
- test_no_inline_ticket_regex: _collect_violations -> directory.rglob("*.py") sobre tests/.

### Hallazgo de shared state (DIFERENTE de la hipotesis del contrato)
El contrato presumia cwd/git/escaneo del proyecto como estado global. La causa raiz REAL
es mas concreta: los 3 tests recorren el ARBOL VIVO del repo con rglob. Ese arbol contiene
`tests/sandbox/test_runtime/session_<PID>/`, que el conftest crea por-worker (PID) y BORRA
en teardown (`_project_temp_environment` -> shutil.rmtree; pytest_sessionfinish). Bajo xdist
cada worker (gw0..gw7) tiene su propio session_<PID>; cuando un worker borra el suyo mientras
otro worker esta a mitad de un rglob del arbol, scandir encuentra un dir a medio borrar ->
FileNotFoundError. No es defecto de los 3 tests: es que escanean un arbol que otros workers mutan.

La cura de raiz en superficie permitida (conftest, NO producto): situar SESSION_RUNTIME_ROOT
fuera del arbol escaneado del repo, de modo que ningun rglob del proyecto recorra los sandbox
volatiles de los workers. No cambia ninguna asercion de los tests (siguen escaneando el repo real;
solo desaparece el ruido concurrente de los tmp dirs dentro del arbol).

### Fase 1 - Implementacion
Cambio minimo en superficie permitida (conftest):
- `tests/conftest.py`: `SESSION_RUNTIME_ROOT` reubicado de `tests/sandbox/test_runtime/session_<PID>`
  a `tempfile.gettempdir()/oda_test_runtime/session_<PID>` (FUERA del arbol del repo). Asi ningun
  rglob del proyecto recorre los sandbox volatiles por-worker. `TEST_RUNTIME_ROOT` se conserva por
  compat con otros tests que lo referencian por nombre. tmp_path mantiene su semantica via factory.
- NO se toco producto, runner, CI, controller ni runtime. Scope honesto: solo 2 de las 4 superficies
  permitidas fueron necesarias (conftest + project_scanner para la barrera); detect_version y
  no_inline_ticket_regex NO requirieron edicion porque el fix de raiz en conftest los cura a los tres.

### Fase 2 - Tests + barrera
- `tests/unit/test_project_scanner.py`: nueva barrera `test_session_sandbox_lives_outside_scanned_repo_tree`
  que afirma la invariante de raiz (sandbox de sesion fuera del arbol escaneado).
- FAIL-sin/PASS-con (determinista): con fix -> 1 passed; revirtiendo conftest a HEAD -> AssertionError.
- Triple bajo `-n 8 --dist load`: VERDE y ESTABLE en 3 corridas seguidas (52/53/53 passed, 0 failed).
  Antes del fix: 3 failed reproducibles. Serial sigue verde.

### Gates focales
- ruff check (4 archivos): All checks passed!
- ruff format --check (4 archivos): already formatted
- encoding guard: exit 0
- diff acotado a tests/conftest.py + tests/unit/test_project_scanner.py (ambos en FLT).

### CONTRACT_GAP -- CG-WOT-2026-013c.md emitido
La cura de raiz cae en superficie prohibida:
- 2 de los 3 tests ejecutan el rglob DENTRO de producto (project_scanner / project_paths); el test solo
  pasa el root. La exclusion de tests/sandbox YA existe en producto pero es POST-rglob: el scandir crudo
  explota antes de filtrar. Hacerlo robusto = tocar codigo de producto (Forbidden Surface).
- La alternativa solo-conftest (sandbox fuera del arbol) volvia verde el triple xdist (estable x3) PERO
  rompio test_windows_safe_temp_runtime::test_tmp_path_stays_under_runtime_root (exige sandbox DENTRO).
  Suite --level all con ese cambio: 10 failed. Conflicto de invariantes irreducible sin tocar producto.
- Decision: emitir CG-WOT-2026-013c.md y bloquear, conforme al CONTRACT_GAP behavior del contrato.
  Commit experimental revertido (reset --soft + restore a cd74667). Working tree limpio, runner intacto.
