# AUDIT_WOT-2026-014e

## Scope
- Ticket: `WOT-2026-014e`
- deliverable_type: `code`
- delivery_authority: `repo_motor`
- Objetivo auditado: unificar la resolucion de `motor_root` sobre
  `runtime.motor_link.resolve_motor_root` y bloquear la reaparicion del drift
  `.resolve()` entre consumidores.

## TP Check
- TP-01: el packet debe fijar el seam real a dos consumidores concretos y dejar
  `runtime/motor_link.py` como autoridad, no como tercer lugar a redisenar.
  Verificacion esperada: FLT limitado a
  `scripts/run_gates_dispatch.py`, `scripts/check_destino_publish_ready.py` y
  sus tests unitarios naturales.
- TP-02: el ticket debe preservar la precedencia `arg > env > link` sin volver
  a abrir el JSON en cada consumidor.
  Verificacion esperada: wrappers locales minimos, sin parser duplicado.
- TP-03: la barrera principal debe probar normalizacion real del path, no solo
  un grep cosmetico de imports.
  Verificacion esperada: test regression que falla al reintroducir una copia
  local con ruta sin `.resolve()`.
- TP-04: el ticket debe distinguir `motor_root` de `destination_root`.
  Verificacion esperada: `destination_root` y sus consumidores quedan en
  `Forbidden Surfaces` / `Non-goals`.
- TP-05: el cierre debe seguir exigiendo validate y suite canonica, no solo la
  bateria focal.
  Verificacion esperada: `run_pytest_safe --level all` y
  `validate --json --project-root <workspace_activo>` citados en la evidencia.

## Regression Focus
- La regresion principal es que reaparezca una copia local que reabra
  `motor_destination_link.json` y devuelva `motor_root` sin normalizar.
- El falso verde a evitar es un diff que solo cambie imports o nombres pero no
  demuestre paridad semantica entre helper canonico y consumidores.

## Closing Rule
- No aprobar si el diff toca `destination_root`, `encoding_post_write_hook`,
  `check_motor_destination_integration` o crea un segundo helper para leer el
  mismo JSON.
- No aprobar sin evidencia literal del fail-sin-fix de la barrera y sin el SHA
  del commit del `repo_motor`.