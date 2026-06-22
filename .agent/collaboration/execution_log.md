# Execution Log -- WOT-2026-013f

**Estado:** READY_FOR_REVIEW

## MANAGER - WOT-2026-013f - Bootstrap operativo

Ticket activado para podar `tests/deprecated/` sin tocar runner, producto ni familias legacy adyacentes.

Packet activo en repo_destino:
- backlog alineado con follow-up FU-013E-2 y FLT estrecho
- `OBJ-013F-001` en `repo_charter.md`
- `PLAN-013F-001` en `plan_graph.md`
- `T-013F-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013f.md` y `AUDIT_WOT-2026-013f.md` activos para Builder

Premisa operativa del Builder:
- releer `pytest.ini`, `tests/deprecated/test_goose_triggers.py`, `tests/deprecated/test_goose_realworld.py`, `scripts/cleanup_legacy.py` y `tests/integration/RETIRED_TESTS.md`
- registrar collect-only pre y post (`python -m pytest tests --collect-only -q -p no:cacheprovider`) y exigir 3111 en ambos lados
- retirar solo `tests/deprecated/` y documentar el retiro en `tests/integration/RETIRED_TESTS.md`
- si aparece consumidor vivo o el conteo cambia, parar y emitir `CG-WOT-2026-013f.md`

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `4eb0fbb`
- repo_destino HEAD = `b722c1b`
- `git status -sb` limpio en ambos repos (`main...origin/main`)
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings

## BUILDER - WOT-2026-013f - Fase 0 (diagnostico read-only)

Preflight de bootstrap verificado: STATE.md=WOT-2026-013f/IN_PROGRESS, TURN.md Plan ID=WOT-2026-013f, work_plan.md ID=WOT-2026-013f, bus seq 1304 STATE_CHANGED->IN_PROGRESS para 013f (013e cerrado seq 1303). No anclado a ticket anterior.

Seams y premisas confirmados en codigo (motor HEAD 4eb0fbb):
- `pytest.ini` linea 13: `norecursedirs` incluye `tests/deprecated` => el directorio NO se recolecta hoy.
- `tests/deprecated/` contiene: `__init__.py` (vacio), `test_goose_triggers.py`, `test_goose_realworld.py`, `__pycache__/`. Ambos .py llevan cabecera `# DEPRECATED (WT-2026-254a): Goose integration deprecated. Moved from scripts/ to tests/deprecated/.`
- `scripts/cleanup_legacy.py`: `OLD_SCRIPT_NAMES` lista el basename `test_goose_realworld.py`, pero `_find_old_scripts()` (l.87-90) lo resuelve SOLO contra `self.scripts_dir` (`scripts/`), no contra `tests/deprecated/`. `LEGACY_DIRS` (l.44-49) NO incluye `tests/deprecated`. => NO es consumidor vivo del directorio.
- `tests/integration/RETIRED_TESTS.md` existe (35 lineas) como ledger canonico de retiros (WP-2026-061/066).

Consumidores vivos de `tests/deprecated/`: NINGUNO.
- `.py`: 0 hits fuera del propio dir.
- config (.toml/.cfg/.ini/.json/.yml): 0 hits canonicos.
- Unicos hits: `graphify-out/` (cache sha256/graph), que esta GITIGNORED y es generado, no canonico.
- Referencia en `.claude/rules/03-skills-discovery.md` es documental historica (ya tachada DEPRECATED), no consumidor de codigo.

Baseline PRE-poda:
- `python -m pytest tests --collect-only -q -p no:cacheprovider` => `3111 tests collected`.

Desviaciones de scope: ninguna. No procede CG-WOT-2026-013f. Procedo a Fase 1 (poda + ledger).

## BUILDER - WOT-2026-013f - Fase 1 + gates + entrega

Fase 1 (poda + ledger):
- `git rm -r tests/deprecated/` => removidos `__init__.py`, `test_goose_realworld.py`, `test_goose_triggers.py`. Borrado fisico del `__pycache__/` residual (gitignored).
- `tests/integration/RETIRED_TESTS.md` actualizado: nueva seccion "Retired: tests/deprecated/ (Goose integration suite)" documentando que cubrian Goose (deprecado WT-2026-254a), que ya estaban excluidos del runner (norecursedirs), que el collect-only se mantiene en 3111, ausencia de consumidores vivos, y origen FU-013E-2. Seccion "Known Debt" actualizada a WOT-2026-013f.

Commit del entregable (repo_motor):
- HEAD = `bc658f8` "WOT-2026-013f prune tests/deprecated (Goose, already runner-excluded)".
- `git show --stat HEAD`: 4 files changed, 16 insertions(+), 410 deletions(-): 3 deletes de tests/deprecated/ + tests/integration/RETIRED_TESTS.md. Diff = exactamente el contrato. Arbol limpio.
- Pre-commit hooks: encoding guard, history truncation, claude settings portability => Passed; ruff/ast Skipped (no .py modificado, solo borrados + markdown).

Gates (comandos exactos + exit codes):
- Collect-only PRE: `python -m pytest tests --collect-only -q -p no:cacheprovider` => `3111 tests collected`.
- Collect-only POST: `python -m pytest tests --collect-only -q -p no:cacheprovider` => `3111 tests collected`. Sin cambio (poda no reduce recoleccion canonica).
- Ruff / ruff format: NO APLICA (no se toco ningun .py; solo borrados de archivos y edicion de markdown).
- Encoding guard: `python scripts/check_encoding_guard.py tests/integration/RETIRED_TESTS.md` => exit 0.
- Suite canonica: `python scripts/run_pytest_safe.py --level all` => `3091 passed, 20 skipped in 709.27s`, exit_code 0. last-run.json: status=finished, level=all, args_mode=default_discovery, tested_commit_sha=bc658f8 == HEAD. (3091 passed + 20 skipped = 3111 recolectados.)
- State-leak: silencioso (runner barrier exit 0; solo execution_log.md modificado en destino, que es entregable Builder esperado).
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` => 0 errors, 0 warnings.

Desviaciones y justificaciones CEM: ninguna. Diff acotado a las superficies FLT. Procedo a --pre-handoff + --mark-ready.


Scope override: Los 3 archivos borrados son hijos de tests/deprecated/, ruta explicitamente listada en Files Likely Touched del work_plan WOT-2026-013f. El scope gate compara rutas de archivo exactas y no expande el prefijo de directorio del FLT. Entrega en repo_motor commit bc658f8 (git rm -r tests/deprecated/ + ledger RETIRED_TESTS.md).. Affected files: tests/deprecated/__init__.py, tests/deprecated/test_goose_realworld.py, tests/deprecated/test_goose_triggers.py

Scope override: Los 3 archivos borrados son hijos de tests/deprecated/, ruta explicitamente en Files Likely Touched de WOT-2026-013f; el scope gate no expande el prefijo de directorio. Entrega repo_motor commit bc658f8.. Affected files: tests/deprecated/__init__.py, tests/deprecated/test_goose_realworld.py, tests/deprecated/test_goose_triggers.py