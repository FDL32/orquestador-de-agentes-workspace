# BUILDER BRIEF WT-2026-249c

## Mision
Implementar un fix minimo en `bus/review_bridge.py` para impedir que una review valida del Manager con `DECISION: CHANGES` termine convertida en `INSPECT` y derive a `HUMAN_GATE` por fallo de parser.

## Scope productivo
- `bus/review_bridge.py`
- `tests/test_review_bridge.py`

## Read first
1. `work_plan.md`
2. `PLAN_WT-2026-249c.md`
3. `AUDIT_WT-2026-249c.md`
4. `.agent/runtime/reviews/WT-2026-249b/attempt-2.md`
5. `.agent/runtime/review_packets/WT-2026-249b_attempt-2.md`
6. `.agent/runtime/events/events.jsonl`

## Contrato duro
- No tocar `agent_controller.py`, `supervisor.py`, state machine ni schema del bus.
- No introducir payload estructurado de `CHANGES`.
- No crear `REWORK_*` ni artefactos equivalentes.
- Mantener el fix en parser-only.

## Barreras minimas esperadas
- `test_early_inspect_later_changes_returns_changes`
- test del canal realmente observado en `249b`
- si aplica, `test_no_final_answer_text_with_changes_returns_changes`
- `test_final_answer_phase_wins_as_regression`

## Gates
- `python -m pytest tests/test_review_bridge.py -v`
- `python scripts/run_pytest_safe.py`
- `python -m ruff check bus/review_bridge.py tests/test_review_bridge.py`
- `python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`

## Cierre esperado
Antes de `--mark-ready`, registra en `execution_log.md`:
- evidencia del canal real usado en `249b`;
- si el fix fue solo Bug #1 o Bug #1 + residual `json_last_text`;
- nombre de la prueba barrera que fallaba antes y pasa despues.
