# AUDIT_WOT-2026-014c

## Scope
- Ticket: `WOT-2026-014c`
- deliverable_type: `code`
- delivery_authority: `repo_motor`
- Objetivo auditado: acotar el tree-scan de `classify_publication` al universo
  publicable de git y bloquear la regresion contra archivos git-ignored.

## TP Check
- TP-01: el packet debe fijar el seam real y evitar scope-creep hacia regex,
  buckets o history-scan.
  Verificacion esperada: FLT limitado a `scripts/classify_publication.py` y
  `tests/test_classify_publication.py`, con `history_scan` y politicas de
  secreto fuera de scope.
- TP-02: la barrera principal debe cubrir la matriz completa
  `ignored / tracked / untracked-no-ignored`, no solo el caso ignored.
  Verificacion esperada: una sola suite focal demuestra las tres filas.
- TP-03: el ticket debe distinguir correccion de alcance de correccion de
  deteccion.
  Verificacion esperada: no aparecen cambios de regex o allowlists de
  contenido para cerrar un falso positivo de scope.
- TP-04: el fail-sin-fix debe ser real.
  Verificacion esperada: al restaurar un universo basado en disco, el test del
  archivo git-ignored vuelve a fallar.
- TP-05: el cierre debe seguir exigiendo validate y suite canonica, no solo la
  suite focal.
  Verificacion esperada: `run_pytest_safe --level all` y
  `validate --json --project-root <workspace_activo>` citados en la evidencia.

## Regression Focus
- La regresion principal es que el tree-scan vuelva a leer archivos que git no
  publicaria.
- El falso verde a evitar es restringir el universo a solo tracked y perder la
  deteccion de `untracked` publicables.

## Closing Rule
- No aprobar si el diff toca `_scan_history_secrets()` o cambia la politica de
  secretos fuera del seam del universo publicable.
- No aprobar sin evidencia literal de los tres casos de la matriz y sin el SHA
  del commit del `repo_motor`.
