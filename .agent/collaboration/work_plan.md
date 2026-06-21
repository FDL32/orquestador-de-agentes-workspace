# work_plan.md -- WOT-2026-010x
## Metadata
- **ID:** WOT-2026-010x
- **Contract ID:** T-010X-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Sustituir `gitleaks/gitleaks-action@v2` por una invocacion CLI OSS de gitleaks en `.github/workflows/security-audit.yml`, manteniendo el escaneo fail-closed y una barrera de regresion en `tests/unit/test_hook_ci_alignment.py`, sin reabrir la politica portable de allowlists.
## Non-goals
- No tocar `agent_system/templates/gitleaks.config.toml`, `.pre-commit-config.yaml`, `scripts/install_agent_system.py`, `scripts/pip_audit_project.py` ni otros workflows.
- No cambiar la politica de allowlists, ignores de seguridad o semantica general del `security-audit` mas alla del paso de gitleaks.
- No mezclar `010x` con `011g`, `011i`, `WT-2026-256a` ni follow-ups de dependencias.
## Premisas verificadas antes de Builder
- `.github/workflows/security-audit.yml` sigue usando `gitleaks/gitleaks-action@v2`.
- El motor ya dispone de semilla portable de configuracion en `agent_system/templates/gitleaks.config.toml`.
- `tests/unit/test_hook_ci_alignment.py` ya es la barrera natural para evitar drift entre CI y la politica de seguridad del workflow.
- El ticket debe resolverse dentro del workflow y su barrera; si requiere tocar politica/config de gitleaks fuera de esas superficies, el resultado correcto es `CONTRACT_GAP`.
## Decision Arquitectonica
`010x` se mantiene acotado a la invocacion de CI: el workflow deja de depender del action licenciado y la regresion se fija en `tests/unit/test_hook_ci_alignment.py`. La politica portable de gitleaks ya fijada por `004a/004b` queda read-only.
## Files Likely Touched
### repo_motor
- .github/workflows/security-audit.yml
- tests/unit/test_hook_ci_alignment.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- agent_system/templates/gitleaks.config.toml
- .pre-commit-config.yaml
- scripts/install_agent_system.py
- .agent/collaboration/_archive/backlog_done.md
- .agent/runtime/pytest-safe/last-run.json
## Forbidden Surfaces
- tocar la politica/config de gitleaks (`agent_system/templates/gitleaks.config.toml`)
- tocar `.pre-commit-config.yaml`, `scripts/install_agent_system.py`, `scripts/pip_audit_project.py` u otros workflows
- introducir otro action de terceros/licenciado para resolver el mismo paso
- mezclar el ticket con ignores de dependencias o deuda de `WT-2026-256a`
## Criterios binarios
- `.github/workflows/security-audit.yml` deja de referenciar `gitleaks/gitleaks-action@v2`.
- El paso de gitleaks usa CLI OSS directa y no requiere `GITLEAKS_LICENSE` ni `GITHUB_TOKEN` para ese paso.
- La invocacion conserva semantica fail-closed y usa una fuente de configuracion ya existente en el repo, sin reabrir la politica de allowlists.
- `tests/unit/test_hook_ci_alignment.py` gana una barrera FAIL-sin/PASS-con que falle si reaparece el action licenciado y pase con la invocacion CLI.
- `python -m pytest tests/unit/test_hook_ci_alignment.py -v`, `ruff check tests/unit/test_hook_ci_alignment.py`, `uv run ruff format --check tests/unit/test_hook_ci_alignment.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si la sustitucion exige tocar politica/config de gitleaks fuera de las superficies declaradas.
- Parar si la unica via OSS viable introduce otro action de terceros/licenciado o redisenia el workflow completo.
- Parar si la barrera de `tests/unit/test_hook_ci_alignment.py` no puede expresar la regresion sin mezclar otras familias de workflow/security.
## CONTRACT_GAP
Emitir `CG-WOT-2026-010x.md` si la sustitucion OSS solo puede hacerse tocando politica/config de gitleaks fuera del workflow y la barrera declarada, si el unico camino verde relaja el fail-closed del escaneo, o si la solucion exige un action de terceros/licenciado diferente.

