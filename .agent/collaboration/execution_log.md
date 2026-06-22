# Execution Log -- WOT-2026-013h

**Estado:** READY_FOR_REVIEW

## MANAGER - WOT-2026-013h - Bootstrap operativo

Ticket activado para eliminar la herencia recurrente de `archive_rename_uncommitted` en el archivado canonico, sin auto-commit y sin reabrir familias cerradas.

Packet activo en repo_destino:
- backlog alineado: `013h` pasa a ser el primer ticket accionable; `013i` queda pendiente posterior
- `OBJ-013H-001` en `repo_charter.md`
- `PLAN-013H-001` en `plan_graph.md`
- `T-013H-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013h.md` y `AUDIT_WOT-2026-013h.md` activos para Builder

Premisa operativa del Builder:
- releer `scripts/archive_collaboration_artifacts.py`, `scripts/closeout_steps/archival.py`, `scripts/session_closeout.py` y las barreras actuales
- reproducir el patron real con repo git en `tmp_path`, no con mocks blandos
- mantener el fix acotado a archivado/cierre o bloquear por `CG-WOT-2026-013h.md`
- preservar una sola razon estable: `archive_rename_uncommitted`

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `cf5a4bc`
- repo_destino HEAD = `cd8e33b`
- `013g` cerro canonicamente y el follow-up correcto es de closeout/archivado, no de runner

## BUILDER - WOT-2026-013h - Fase 0 (diagnostico read-only)

Preflight verificado: validate 0/0; STATE=013h/IN_PROGRESS; TURN BUILDER/013h/IMPLEMENT; bus seq 1328 STATE_CHANGED->IN_PROGRESS para 013h (013g COMPLETED seq 1326). No anclado a 013g.

Causa raiz [V] (rastreada por codigo):
- El archivador `scripts/archive_collaboration_artifacts.py::archive_collaboration_artifacts()` (l.144-156) mueve STRATEGY_/AUDIT_ cerrados con `shutil.move` y NO hace `git add` ni commit.
- El detector canonico `scripts/delivery_hygiene_check.py::check_archive_rename_complete` (l.373-391) define el limbo como un par `D <origen>` + `?? _archive/plan_audit/<basename>` (delete sin stage + untracked). Un `git add` de ambos lados colapsa el par a rename staged `R` y el detector PASA.
- Quien dispara el archivado en cierre canonico: `.agent/agent_controller.py::_auto_archive_closed_artifacts()` (l.1013-1040) en `_handle_mark_ready` (l.3198), seguido de `_check_mark_ready_archive_rename()` (l.3207) que BLOQUEA fail-closed si hay limbo.
- `_handle_manager_approve` (l.4334+) NO archiva: solo `_sync_markdowns_to_completed`. => los STRATEGY/AUDIT del ticket N-1 quedan VIVOS en collaboration/ tras su cierre, y el `_auto_archive` del mark-ready del ticket N los mueve, generando el limbo HEREDADO que vivieron 013e->013f->013g.
- 011a (closeout) y 011h (mark-ready) ya FALLAN-CERRADO ante el limbo, pero ninguno lo PREVIENE en origen: el archivador deja el limbo y la barrera solo lo detecta despues. El reconcile manual era la unica salida.

Seam elegido (dentro de FLT): el fix correcto y minimo es que `archive_collaboration_artifacts()` haga `git add` de cada rename (origen+destino) tras el `shutil.move`, cuando opera dentro de un repo git. Esto:
- elimina el limbo en ORIGEN (rename queda staged, no `D`+`??`),
- NO commitea (preserva "no auto-commit opaco"; el rename staged entra en el commit de cierre natural),
- mantiene `archive_rename_uncommitted` como unica fuente de verdad (no crea segundo guard ni segunda razon),
- es best-effort: si no hay repo git o git falla, el archivado no rompe y la barrera fail-closed sigue como red de seguridad.

Confirmacion de que NO requiere tocar agent_controller.py: el staging en el archivador resuelve el limbo aguas arriba de `_check_mark_ready_archive_rename`, que entonces pasa sin cambios. Fix acotado a `scripts/archive_collaboration_artifacts.py` + tests. No se toca agent_controller.py (fuera de FLT), ni se relaja el detector.

Patron real confirmado vigente: `D old + ?? new` / `archive_rename_uncommitted` (visto en 013e/013f/013g, reconciliado a mano cada vez).

Desviaciones de scope: ninguna. No procede CG. Procedo a Fase 1 (fix en archivador) + Fase 2 (tests con repo git real en tmp_path).

## BUILDER - WOT-2026-013h - Fase 1 (fix) + Fase 2 (tests) + gates + entrega

Fix (Fase 1, scripts/archive_collaboration_artifacts.py):
- Anadido helper `_find_git_root()` (walk up buscando .git) y `_stage_archival_rename(src, dest)` que corre `git add -- <src> <dest>` desde la raiz del work-tree tras el shutil.move. Stage, NO commit. Best-effort/fail-open: sin git o si git falla, no levanta; la barrera fail-closed sigue de red.
- Llamado tras cada shutil.move exitoso en `archive_collaboration_artifacts()`.
- import subprocess anadido. noqa S603/S607 en la llamada git (args fijos, sin input de usuario).
- NO se toco agent_controller.py: el staging en origen resuelve el limbo aguas arriba de _check_mark_ready_archive_rename, que pasa sin cambios. NO se relajo el detector. NO se creo segundo guard.

Tests (Fase 2, repo git real en tmp_path, sin mocks de subprocess para la barrera):
- tests/test_archive_collaboration_artifacts.py: + `test_archiver_stages_rename_so_no_limbo_inherited` (regresion FAIL-sin/PASS-con), `test_archiver_stages_but_does_not_commit` (HEAD intacto + rename staged), `test_archiver_no_git_tree_still_moves` (fail-open). Reemplaza el viejo helper `_seed_closed_pair`.
- tests/test_session_closeout.py: reescrito `test_uncommitted_rename_blocks_in_real_closeout` -> `test_real_archiver_stages_rename_and_step_passes` (el step real ahora PASA, staged, HEAD intacto). Las barreras `test_partial_move_then_*_fails_closed` (limbo sin staging) siguen verificando fail-closed: la barrera 011a queda intacta.

Evidencia FAIL-sin/PASS-con (registrada):
- FAIL-sin-fix: neutralizando `_stage_archival_rename` a no-op, el archivador deja el limbo y `check_archive_rename_complete().passed == False`. Verificado via script one-off en tmp repo git real.
- PASS-con-fix: con el staging, `guard.passed == True` sin reconcile manual; los 3 tests focales del archivador y el del closeout pasan.

Gates (comandos exactos + resultados literales):
- Focales: `python -m pytest tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py -q -p no:cacheprovider` => `224 passed`.
- Ruff check: `uv run ruff check <7 archivos del contrato>` => `All checks passed!`.
- Ruff format: `uv run ruff format --check <7 archivos>` => `7 files already formatted`.
- Suite canonica: `python scripts/run_pytest_safe.py --level all` => `3093 passed, 20 skipped in 349.56s`, exit_code 0. last-run.json: status=finished, level=all, args_mode=default_discovery, tested_commit_sha=103849a == HEAD.
- State-leak: silencioso (runner barrier exit 0; solo execution_log.md modificado en destino).
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings.

Commit del entregable (repo_motor): HEAD `103849a` "WOT-2026-013h stage archival rename to end inherited limbo". Diff = 3 files (scripts/archive_collaboration_artifacts.py + 2 test files), todos en FLT. 163 insertions, 26 deletions. Pre-commit hooks (ast/ruff/encoding/history) verdes. Arbol motor limpio.

Desviaciones y justificaciones CEM: ninguna. Procedo a pre-handoff + mark-ready.
