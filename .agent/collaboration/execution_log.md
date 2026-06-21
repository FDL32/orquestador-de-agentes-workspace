# execution_log.md -- WOT-2026-010x
## Metadata
- **Ticket:** WOT-2026-010x
- **Estado:** READY_FOR_REVIEW
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-010x.
- Motivo: `011g` ya cerro canonicamente; `011i` sigue condicionado por los 3 tests no paraleloseguros expuestos por `011e`; `011h` requiere antes normalizar la contradiccion backlog-vs-codigo. `010x` queda como ticket alto, independiente y con root cause ya verificado en CI.
- Contrato congelado: `T-010X-001`.
- Frontera fijada antes de Builder: solo workflow `.github/workflows/security-audit.yml` + barrera `tests/unit/test_hook_ci_alignment.py`; tocar politica/config de gitleaks o otros workflows dispara `CONTRACT_GAP`.
## Premise Re-check requerido al Builder
- Releer `.github/workflows/security-audit.yml`, `tests/unit/test_hook_ci_alignment.py`, `agent_system/templates/gitleaks.config.toml` y `.pre-commit-config.yaml`.
- Confirmar que el workflow aun usa `gitleaks/gitleaks-action@v2` y que la semilla portable ya existe.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de empezar la implementacion.
## Restriccion cross-ticket
- `010x` no reabre la politica de gitleaks de `004a/004b` ni mezcla `WT-2026-256a`, `011g`, `011i` o cambios en otros workflows.
- Si la sustitucion OSS exige tocar config/politica de gitleaks fuera del workflow y la barrera, el resultado correcto es `CG-WOT-2026-010x.md`.


## BUILDER - WOT-2026-010x - Gitleaks CLI OSS en security-audit.yml

### Fase 0 - Baseline (VERIFICADO)
- .github/workflows/security-audit.yml paso "Run Gitleaks" usaba `uses: gitleaks/gitleaks-action@v2` + `env: GITHUB_TOKEN` (action licenciado).
- Plantilla seed portable EXISTE: agent_system/templates/gitleaks.config.toml (useDefault + allowlist generic-api-key-on-SHA). No hay .gitleaks.toml vivo en raiz; el action@v2 corria sin --config (reglas default).
- tests/unit/test_hook_ci_alignment.py parsea el workflow (fixture ci_config) pero NO tenia barrera sobre gitleaks -> superficie natural a extender.
- Historico 004a (commit 3e23873) / 004b (9c7c91d): la politica/config de gitleaks queda FUERA de scope; 010x solo cambia el paso del workflow + barrera de test.

### Fase 1 - CLI OSS (cambio minimo)
- Paso "Run Gitleaks (OSS CLI)": descarga el binario release OSS de gitleaks v8.30.1 (curl + tar) y corre `./gitleaks detect --source . --config agent_system/templates/gitleaks.config.toml --redact --exit-code 1 --log-opts="--all"`.
- SIN gitleaks-action (uses eliminado), SIN GITLEAKS_LICENSE, SIN GITHUB_TOKEN para el paso (env solo GITLEAKS_VERSION). fail-closed via --exit-code 1. Reutiliza la config seed existente (no reabre allowlist). Resto del workflow intacto.
- YAML valido (yaml.safe_load); shell con set -euo pipefail; un comando por linea (sin continuaciones \ fragiles). encoding exit 0.

### Fase 2 - Barreras (tests/unit/test_hook_ci_alignment.py, 5 nuevas en TestHookCIAlignment)
- test_gitleaks_does_not_use_licensed_action: no `gitleaks-action` en uses.
- test_gitleaks_runs_oss_cli: `gitleaks detect` presente en run.
- test_gitleaks_is_fail_closed: `--exit-code 1` presente.
- test_gitleaks_reuses_existing_config: usa la plantilla seed.
- test_gitleaks_step_has_no_license_or_token: env sin GITLEAKS_LICENSE ni GITHUB_TOKEN.
- Verificacion FAIL-sin/PASS-con: revertido el workflow a HEAD (action@v2) -> 5 failed; restaurado fix -> 5 passed.

### Gates
- Tests focales: `python -m pytest tests/unit/test_hook_ci_alignment.py -q` -> 13 passed in 0.12s (8 pip-audit + 5 gitleaks).
- Ruff: All checks passed! | Ruff format: 1 file already formatted | Encoding (workflow+test): exit 0.
