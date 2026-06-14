# PLAN WOT-2026-003f - CI destino gate de portabilidad de settings

## Pasos
1. `.github/workflows/quality-gates.yml`:
   - Añadir `- '.claude/**'` a `paths:` en push y pull_request.
   - Añadir step (tras "Validate destination .agent state"):
     `Claude settings portability gate` que corre
     `python _motor/scripts/check_claude_settings_portability.py .claude/settings.json`.
   - Añadir bullet al Summary.
2. Verificar: parseo YAML; run local del gate (exit 0); validate destino 0; motor intacto.

## Seams / invariantes
- Reutiliza el script canonico del motor (checkouteado en `_motor/`); sin duplicar logica.
- El paso falla la CI si el settings tracked del destino tiene grants personales o el
  entrypoint canonico es fail-open.

## Evidencia esperada
- Diff del workflow; `yaml.safe_load` OK; gate local exit 0; validate 0; motor pristine.

## STOP
- Gate local en rojo -> regresion de settings, no maquillar.
