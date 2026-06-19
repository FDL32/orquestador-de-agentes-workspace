# STRATEGY_WOT-2026-010w.md

## Enfoque

Ticket corto de hardening del closeout. La causa raiz ya esta verificada: tres
call sites en `closeout_steps` usan `subprocess.run(..., text=True)` sin
`encoding`, lo que en Windows decodifica con cp1252 y puede lanzar
`UnicodeDecodeError` al capturar salida UTF-8 de scripts o de git con paths
no-ASCII. El fix debe ser minimo, local y verificable.

## Fase 0 - Confirmacion de seams

1. Confirmar en codigo los tres call sites:
   - `scripts/closeout_steps/support.py:run_script`
   - `scripts/closeout_steps/support.py:check_versioned_filenames`
   - `scripts/closeout_steps/rotation.py:step_git_clean`
2. Reproducir el fallo real con:
   `python .agent/agent_controller.py --session-close --dry-run --force --project-root <repo_destino>`
   y registrar el `UnicodeDecodeError`.
3. Localizar la superficie de test viva en `tests/test_session_closeout.py`.
4. Confirmar que `scripts/session_closeout.py` y el controller quedan fuera del
   fix: el problema vive en `closeout_steps`.

## Fase 1 - Implementacion minima

1. Anadir `encoding="utf-8", errors="replace"` a los tres `subprocess.run`
   del FLT.
2. No tocar la logica funcional de los steps ni su semantica de PASS/WARN/FAIL.
3. Si algun test existente se apoya implicitamente en el decode por defecto,
   ajustarlo solo en lo necesario para reflejar el contrato nuevo.

## Fase 2 - Barreras

Deben existir barreras que prueben:
- PASS de `run_script()` al ejecutar un script temporal que imprima un em dash
  u otra salida UTF-8 alta.
- No `UnicodeDecodeError` al capturar esa salida.
- El dry-run real de `--session-close` deja de romper por decode.
- Los dos call sites latentes quedan cubiertos al menos por verificacion
  directa de codigo o por tests ya existentes del closeout.

## Riesgos a vigilar

- Corregir solo `run_script()` y dejar los otros dos decode-paths latentes.
- Mover el fix al controller por comodidad, ampliando el blast radius.
- Hacer un test demasiado mockeado que no ejerza la decodificacion real.
