# AUDIT_WOT-2026-013a

## Preguntas binarias de auditoria
- [ ] `python -m pytest tests/test_controller_integration.py -k approved_pending -q` pasa en aislamiento.
- [ ] El diff toca solo `tests/test_controller_integration.py` y `execution_log.md`.
- [ ] Existe evidencia FAIL-sin/PASS-con para el mismo test aislado.
- [ ] `python -m pytest tests/test_controller_integration.py -q`, `ruff`, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- [ ] No se tocaron `.agent/agent_controller.py`, `runtime/`, `bus/`, `scripts/run_pytest_safe.py`, `pre_handoff_guard.py` ni CI/workflows.
- [ ] `execution_log.md` documenta explicitamente que el fix fue test-only.

## Evidencia minima esperada
- Diff de `tests/test_controller_integration.py`.
- Salida literal del rojo aislado y del verde posterior.
- Gates ejecutadas y registradas en `execution_log.md`.
- Si aplica, `CG-WOT-2026-013a.md` con causa exacta del bloqueo.
