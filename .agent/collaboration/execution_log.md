# Execution Log -- WOT-2026-013f

**Estado:** IN_PROGRESS

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
