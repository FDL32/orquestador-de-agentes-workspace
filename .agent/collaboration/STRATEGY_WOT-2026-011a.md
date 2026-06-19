# STRATEGY_WOT-2026-011a.md

## Enfoque

`WOT-2026-010u` ya introdujo una barrera valida para detectar
`archive_rename_uncommitted`, pero esa barrera vive en `delivery_hygiene` /
`pre_handoff` y llega tarde para el operador: el `--session-close` puede
terminar dejando el rename en limbo y la contaminacion aparece en el siguiente
ticket. `011a` no reabre la politica del archivador; mueve la deteccion al
closeout real, en el punto donde ocurre la mutacion.

## Fase 0 - Baseline

1. Confirmar en codigo que `step_archive_collaboration()` devuelve `PASS` si el
   script sale `0`, sin verificar la post-condicion del rename.
2. Confirmar que `check_archive_rename_complete()` ya existe y expone la razon
   estable `archive_rename_uncommitted` con remediacion self-service.
3. Registrar en `execution_log.md` la recurrencia verificada: `010w` y `011d`
   necesitaron reconcile manual post-closeout.

## Fase 1 - Barrera en closeout

1. Reutilizar la deteccion canonica de `delivery_hygiene_check.py` desde
   `scripts/closeout_steps/archival.py` o, si hace falta por propagacion de
   bloqueo, desde `scripts/session_closeout.py`.
2. Si el archivado deja `D old` + `?? _archive/plan_audit/new`, devolver
   `FAIL` bloqueante en el propio closeout.
3. Conservar el mensaje accionable con origen, destino y comando exacto de
   reconcile. Sin auto-commit.

## Fase 2 - Barreras de regresion

1. Anadir un test de `session_closeout` o del step de archivado que reproduzca
   el limbo y demuestre `FAIL` sin el fix / `PASS` con el fix.
2. Mantener el caso limpio en `PASS`.
3. Si se toca la helper de higiene, cubrir que el reason estable no cambia.

## Riesgos a vigilar

- Duplicar la logica de deteccion en vez de reutilizar la barrera existente.
- Dejar el closeout en `WARN`, trasladando otra vez el problema al ticket
  siguiente.
- Introducir auto-commit encubierto "para ahorrar un commit manual".
- Expandir el ticket a rediseño de archivado, manifest o bus.
