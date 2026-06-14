# AUDIT WOT-2026-003f - CI destino gate de portabilidad de settings

## Objetivo
Verificar que el workflow del destino corre el gate canonico del motor contra su
`.claude/settings.json`, que `paths:` dispara en cambios de `.claude/**`, y que el gate
pasa localmente (settings del destino portable, post-003b).

## Reglas de revision
- Revisar el diff real del workflow.
- Confirmar que el step usa el script del motor (`_motor/scripts/...`), no logica duplicada.
- Confirmar `.claude/**` en ambos filtros `paths:`.
- Ejecutar el gate localmente contra `.claude/settings.json` (exit 0).
- Confirmar YAML valido y motor intacto.

## Hallazgos bloqueantes tipicos
- CRITICO: el step maquilla un fallo del gate (settings con regresion).
- ALTO: se duplica la logica del gate en el YAML en vez de invocar el script del motor.
- ALTO: `paths:` no incluye `.claude/**` (el paso nunca dispararia en cambios de settings).
- MEDIO: YAML invalido.

## TP Check
TP-01: step corre `check_claude_settings_portability.py` del motor contra `.claude/settings.json`. (diff)
TP-02: `paths:` push y pull_request incluyen `.claude/**`. (diff)
TP-03: gate pasa localmente contra el settings del destino (exit 0). (command)
TP-04: YAML valido (safe_load). (command)
TP-05: validate destino 0; motor intacto; commit con WOT-2026-003f en repo_destino. (command/git)

## Rechazo inmediato
- Gate maquillado, logica duplicada, o `.claude/**` ausente de paths.
