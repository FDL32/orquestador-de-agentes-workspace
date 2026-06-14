# Work Plan: WOT-2026-003f - CI destino: gate de portabilidad contra .claude/settings.json

## Metadata
- **ID:** WOT-2026-003f
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino (orquestador_de_agentes_workspace)
- **Titulo:** Paso de CI del destino que corre `check_claude_settings_portability.py` contra su `.claude/settings.json`
- **Asignado a:** Builder
- **Severidad:** Baja | **Riesgo:** Bajo (paso de CI nuevo; reversible via git)
- **Depende de:** WOT-2026-003c (completed)
- **Origen:** session-2026-06-14-post-a2d-hardening (follow-up de 003c)

## Decision Arquitectonica
El gate de portabilidad de settings (003c) ya existe y esta testeado en el motor, pero
solo corre en el pre-commit del MOTOR. Un fail-open o grants personales en el
`.claude/settings.json` del DESTINO no se detectarian hasta tocar el motor. Se añade un
paso al workflow `quality-gates.yml` del destino que corre el gate (del motor, ya
checkouteado en `_motor/`) contra el settings del destino, y se amplia el filtro `paths:`
con `.claude/**` para que cambios de settings disparen el workflow. No se duplica logica:
se reutiliza el script canonico del motor.

## Files Likely Touched (repo_destino)
.github/workflows/quality-gates.yml

## Read/inspect only
- `_motor/scripts/check_claude_settings_portability.py` (CLI: arg opcional path; default `.claude/settings.json`; exit 1 si viola).
- `.claude/settings.json` del destino (objeto del gate; NO editar aqui).

## Manager-only
- Revision: confirmar que el paso corre el gate del motor (no duplica logica), que el filtro
  `paths:` incluye `.claude/**`, y que el gate pasa localmente contra el settings actual del destino.

## Non-goals
- NO modificar `.claude/settings.json` del destino.
- NO duplicar la logica del gate en el workflow.
- NO tocar el motor (script ya existe).

## Criterios binarios de cierre
- [ ] `quality-gates.yml`: nuevo step que corre `python _motor/scripts/check_claude_settings_portability.py .claude/settings.json`.
- [ ] Filtros `paths:` (push y pull_request) incluyen `.claude/**`.
- [ ] El gate pasa localmente contra el `.claude/settings.json` del destino (exit 0).
- [ ] YAML valido (parsea sin error).
- [ ] `validate --project-root .` (destino) 0 errores; motor intacto (check_motor_pristine).
- [ ] Commit en repo_destino con WOT-2026-003f.

## STOP / escalado
- Si el gate falla localmente contra el settings del destino, NO maquillar el workflow:
  el settings del destino tendria una regresion (grants/fail-open) -> abrir ticket de seguridad.
- Si el gate requiere el motor no disponible en CI, revisar el checkout `_motor/` antes de añadir el paso.

## Gates (deliverable_type: code; cambio de CI/config)
- Parseo YAML del workflow (python yaml.safe_load).
- Run local del gate contra `.claude/settings.json` (exit 0) = barrera de comportamiento.
- `validate --project-root .` (destino) 0 errores.
- `check_motor_pristine --check` (motor no debe cambiar).
- Nota: sin pytest nuevo (no se añade logica Python; el gate ya esta testeado en el motor por 003c).

## Entregables
- `quality-gates.yml` con el paso del gate + `.claude/**` en paths.
- `orchestrator_pipeline/reports/closeout_WOT-2026-003f.md`.
