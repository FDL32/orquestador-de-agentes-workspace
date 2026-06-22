# Execution Log -- WOT-2026-013i

**Estado:** READY_FOR_REVIEW

## MANAGER - WOT-2026-013i - Bootstrap operativo

Ticket activado para atacar la latencia operacional del purge de sandboxes huerfanos detectada por `013g`, manteniendo intacta la barrera de higiene introducida por `013d`.

Packet activo en repo_destino:
- `OBJ-013I-001` en `repo_charter.md`
- `PLAN-013I-001` en `plan_graph.md`
- `T-013I-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013i.md` y `AUDIT_WOT-2026-013i.md` activos para Builder

Premisa operativa del Builder:
- releer `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` y `tests/conftest.py`
- medir en el mismo host antes de optimizar; separar setup/purge del cuerpo del test
- mantener el fix acotado a harness/tests o bloquear por `CG-WOT-2026-013i.md`
- preservar la higiene del sandbox y revalidar la barrera xdist heredada de `013d`

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `103849a`
- repo_destino HEAD = `06732f6`
- `validate --json --project-root <repo_destino>` = `0 errors / 0 warnings`
- evidencia disparadora: `013g` atribuyo el coste a `_purge_orphan_session_dirs()` con `historical_orphan_dirs=568`

## BUILDER - WOT-2026-013i - Fase 0 (diagnostico) + medicion BEFORE

Preflight: validate 0/0; STATE/TURN/work_plan=013i; bus seq 1337 IN_PROGRESS para 013i (013h COMPLETED seq 1335). Ambos repos sync con origin. No anclado a 013h.

Seam confirmado [V]: `tests/conftest.py::_purge_orphan_session_dirs` (l.57-78) corre en el fixture session-autouse `_project_temp_environment` (l.81-85) en sessionstart. Hace `shutil.rmtree(entry, ignore_errors=True)` secuencial de cada `session_*` huerfano.

Medicion BEFORE [V] (mismo host, perf_counter, sandbox real actual):
- Estado del sandbox: `ls -d tests/sandbox/test_runtime/session_* | wc -l` => 575 dirs huerfanos; `find tests/sandbox/test_runtime -mindepth 1 | wc -l` => 533168 entradas.
- `_purge_orphan_session_dirs(keep_pid=-1)` (purga todos): purged=0, n_after=575, en **38.99s**.

HALLAZGO CRITICO [V]: el purge tarda ~39s pero NO borra nada (purged=0, 575 dirs siguen). La higiene de 013d esta ROTA en silencio:
- Causa real (rmtree sin ignore_errors sobre un huerfano): `PermissionError [WinError 5] Acceso denegado` en `.../dest/.git/objects/f5/...`. Los huerfanos contienen repos git de fixtures; git marca los objects como read-only, y en Windows `shutil.rmtree` no puede borrar archivos read-only.
- Con `ignore_errors=True`, el helper traga el error, gasta 39s recorriendo 533k entradas y deja los 575 dirs intactos. Se acumulan indefinidamente, amplificando coste cada sesion (568 en 013g -> 575 ahora).

Decision tecnica: el fix correcto FORTALECE 013d (hoy roto) y acota la latencia futura en origen:
- Anadir un `onerror`/`onexc` handler a `shutil.rmtree` que limpie el bit read-only (`os.chmod(path, stat.S_IWRITE)`) y reintente el unlink -- patron estandar Windows para borrar arboles `.git`.
- Resultado: el purge BORRA de verdad => la acumulacion perpetua desaparece => las sesiones futuras arrancan con ~0-1 huerfanos en vez de 575, acotando la latencia de raiz.
- Esto NO debilita la barrera de 013d: la hace funcionar. No toca producto/runner/xdist. Frontera = `tests/conftest.py` + barreras.

Procedo a Fase 1 (handler read-only en el purge) + Fase 2 (barrera de regresion) + medicion AFTER.

## BUILDER - WOT-2026-013i - Fase 1 (fix) + Fase 2 (barreras) + medicion AFTER + gates

Fix (Fase 1, tests/conftest.py):
- `_force_remove_readonly(func, path, _exc)`: handler que hace `os.chmod(path, S_IWRITE)` + retry de func; OSError final swallowed (fail-open).
- `_rmtree_robust(target)`: rmtree con `onexc=` (Py>=3.12) / `onerror=` (Py<3.12) enrutado al handler; devuelve True si el path quedo borrado.
- `_purge_orphan_session_dirs` ahora usa `_rmtree_robust` y cuenta solo borrados reales. Tambien el finalizer de `_project_temp_environment` y `pytest_sessionfinish` usan `_rmtree_robust` para que la sesion actual no genere nuevos huerfanos read-only.
- import `stat` anadido. NO se toco producto, runner, pytest.ini ni xdist.

Medicion AFTER [V] (mismo host, perf_counter):
- Purge real de los 575 huerfanos acumulados: purged=575, n_after=0, en 141.81s (one-shot: hace el trabajo que el viejo se saltaba).
- Purge en ESTADO ESTABLE (sandbox limpio, lo que veran las sesiones futuras): purged=0 en 0.0001s.
- Comparativa: before recurrente ~38.99s/sesion sin borrar nada (creciente sin techo) => after estado estable ~0.0001s. El coste recurrente se elimina de raiz porque el purge ahora borra y no se acumula. La latencia queda acotada a un evento unico de limpieza del backlog historico.
- Suite canonica completa post-fix: 3096 passed, 20 skipped en 134.49s (vs ~350s en 013h, ~709s en 013f con sandbox sucio): evidencia en vivo de la latencia acotada.
- Residuos tras suite canonica: `ls -d tests/sandbox/test_runtime/session_* | wc -l` => 0. Sin residuos peores; higiene de 013d reforzada.

Barreras (Fase 2, tests/unit/test_windows_safe_temp_runtime.py, sandbox real sin mocks):
- test_rmtree_robust_deletes_readonly_tree
- test_purge_orphan_session_dirs_removes_readonly_orphan (purged==1; keep_pid preservado)
- test_force_remove_readonly_does_not_raise_on_locked (fail-open)
FAIL-sin/PASS-con [V]: el purge viejo (ignore_errors) deja el orphan read-only (purged=0, sigue existiendo); el nuevo lo borra (purged=1). Confirmado via one-off en tmp repo real.

Gates (comandos exactos + resultados literales):
- Focal: `python -m pytest tests/unit/test_project_scanner.py tests/unit/test_windows_safe_temp_runtime.py -q -p no:cacheprovider` => `46 passed`.
- Triple xdist x3 (via `uv run` porque pytest-xdist se resuelve por dependency group, no en el python del sistema): `uv run python -m pytest <triple> -q -n 8 --dist load -p no:cacheprovider` => `3 passed` en corridas 1, 2 y 3 (verde consecutivo). Nota: el `python -m pytest` directo no reconoce `-n` (xdist no instalado en el interprete base); es coherente con el default no-xdist del runner (011e opt-in). No se toco la politica xdist.
- Ruff check: `uv run ruff check tests/conftest.py tests/unit/test_project_scanner.py tests/unit/test_windows_safe_temp_runtime.py` => `All checks passed!`.
- Ruff format: `uv run ruff format --check <mismos>` => `3 files already formatted`.
- Suite canonica: `python scripts/run_pytest_safe.py --level all` => `3096 passed, 20 skipped in 134.49s`, exit 0. last-run.json: status=finished, level=all, args_mode=default_discovery, tested_commit_sha=07f9c69 == HEAD.
- State-leak: silencioso (runner barrier exit 0; cambios en collaboration/ son proyecciones del bootstrap del packet 013i, no mutacion de la suite; STATE sigue 013i/IN_PROGRESS).
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings.

Commit del entregable (repo_motor): HEAD `07f9c69` "WOT-2026-013i fix silent no-op sandbox purge (read-only .git on Windows)". Diff = 2 files (tests/conftest.py + tests/unit/test_windows_safe_temp_runtime.py), ambos en FLT. 150 insertions, 13 deletions. Pre-commit hooks (ast/ruff/encoding/history) verdes.

Desviaciones y justificaciones CEM: ninguna. No procede CG (el fix vive en harness/tests; no toco producto/runner/CI/xdist). Listo para --pre-handoff + --mark-ready.
