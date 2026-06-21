# AUDIT_WOT-2026-010m.md

## Preguntas binarias de auditoria
- `quality-gates.yml` gana un piloto CI xdist aditivo y explicitamente acotado, sin eliminar ni alterar la corrida serial canonica existente?
- El piloto usa `scripts/run_pytest_safe.py` con `--xdist-workers <N>` solo en la superficie permitida del ticket y el camino canonico en CI sigue sin xdist?
- Existe una barrera FAIL-sin/PASS-con que falle si desaparece el piloto o si la corrida canonica adopta xdist por accidente?
- `execution_log.md` deja evidencia auditable de la separacion entre piloto CI y cierre canonico, con resultado o medicion del piloto?
- `python -m pytest tests/unit/test_quality_gates_workflow.py -q`, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes?

## Hallazgos a rechazar
- Cualquier cambio que toque `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `scripts/pre_handoff_guard.py` o `scripts/run_gates_dispatch.py`.
- Cualquier implementacion que convierta xdist en default implicito o lo meta en la corrida canonica `--level all`.
- Cualquier piloto que dependa de pass-open silencioso o de otros workflows fuera de `quality-gates.yml`.
- Cualquier solucion que derive en redisenar el selector/runner por los tests no parallel-safe en vez de dejar un piloto CI acotado.