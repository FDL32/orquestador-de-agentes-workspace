# STRATEGY_WOT-2026-010x

## Objetivo tecnico
Reemplazar el uso de `gitleaks/gitleaks-action@v2` en el workflow de seguridad por una invocacion CLI OSS acotada al mismo workflow y endurecida por una barrera en `tests/unit/test_hook_ci_alignment.py`, sin tocar la politica portable de gitleaks.

## Fase 0 - Baseline y lectura obligatoria
1. Releer `.github/workflows/security-audit.yml`, `tests/unit/test_hook_ci_alignment.py`, `agent_system/templates/gitleaks.config.toml` y `.pre-commit-config.yaml`.
2. Confirmar en codigo que el workflow aun usa `gitleaks/gitleaks-action@v2` y que la semilla portable ya existe.
3. Registrar en `execution_log.md` el baseline y por que la politica/config queda fuera de scope.

## Fase 1 - Cambio minimo en CI
1. Sustituir solo el paso de gitleaks en `.github/workflows/security-audit.yml`.
2. Mantener el resto del workflow intacto salvo ajustes estrictamente necesarios para la invocacion CLI OSS.
3. Evitar cualquier dependencia en `GITLEAKS_LICENSE` o token dedicado para ese paso.

## Fase 2 - Barrera de regresion
1. Extender `tests/unit/test_hook_ci_alignment.py` con una barrera que detecte la reaparicion del action licenciado.
2. La barrera debe anclar tambien que el workflow conserva una invocacion CLI explicita en vez de caer en una superficie opaca.
3. Demostrar FAIL-sin/PASS-con para esa barrera en `execution_log.md`.

## Fase 3 - Gates y handoff
1. Ejecutar `python -m pytest tests/unit/test_hook_ci_alignment.py -v`.
2. Ejecutar `ruff check tests/unit/test_hook_ci_alignment.py`.
3. Ejecutar `uv run ruff format --check tests/unit/test_hook_ci_alignment.py`.
4. Ejecutar `python scripts/run_pytest_safe.py --level all`.
5. Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`.
6. Hacer handoff canonico solo si todos los gates y el bus quedan verdes.

## Riesgos conocidos
- Si la CLI OSS no puede invocarse sin abrir nueva superficie de config/politica, el ticket debe parar con `CONTRACT_GAP`.
- Si el workflow necesita redisenarse mas alla del paso de gitleaks, el scope deja de ser el aprobado.
- `WT-2026-256a` y cualquier ignore de dependencias permanecen fuera de este ticket.

