# AUDIT_WOT-2026-010x

## Checklist binario
- [ ] El workflow ya no referencia `gitleaks/gitleaks-action@v2`.
- [ ] El paso de gitleaks usa CLI OSS y no depende de `GITLEAKS_LICENSE` ni de token dedicado para ese paso.
- [ ] La invocacion sigue siendo fail-closed y no reabre la politica/config portable de gitleaks.
- [ ] `tests/unit/test_hook_ci_alignment.py` incorpora una barrera que falla si reaparece el action licenciado.
- [ ] El Builder demuestra FAIL-sin/PASS-con de esa barrera.
- [ ] `python -m pytest tests/unit/test_hook_ci_alignment.py -v` pasa.
- [ ] `ruff check tests/unit/test_hook_ci_alignment.py` pasa.
- [ ] `uv run ruff format --check tests/unit/test_hook_ci_alignment.py` pasa.
- [ ] `python scripts/run_pytest_safe.py --level all` pasa en HEAD.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` devuelve 0 errores y 0 warnings.

