# AUDIT_WOT-2026-014a

## Scope
- Ticket WOT-2026-014a, code, repo_motor.
- Objetivo auditado: romper la circularidad del cierre (reporte tracked que bloquea su propio prepush)
  via Opcion A (allowlist compartida + parametro opt-in), sin debilitar el gate pre-push general.

## TP Check
- TP-01: Opcion A (allowlist opt-in). Opcion B (auto-commit) y C (gitignored) descartadas. No se cambia
  el comportamiento DEFAULT de check_git_tree_clean.
- TP-02: expected_patterns extraido a una constante compartida importada por step_git_clean (no duplicada).
- TP-03: barrera mutation-verified: reporte esperado sin commitear FALLA sin el fix; con la allowlist del
  cierre se perdona; un cambio PRODUCTIVO sin commitear SIGUE marcando sucio.
- TP-04: el pre-push general (sin allowlist) queda identico; prepush_check fuera del closeout intacto.
- TP-05: cierre con run_pytest_safe --level all + validate.

## Regression Focus
- Falso verde a evitar: una allowlist demasiado amplia que se trague trabajo productivo sin commitear
  (permitiria pushear con cambios reales). La barrera DEBE distinguir reporte-esperado de cambio-productivo.

## Closing Rule
- No aprobar si se cambia el comportamiento default de check_git_tree_clean, si la allowlist perdona algo
  fuera de los artefactos runtime esperados, si la barrera no distingue reporte-esperado de productivo, o
  sin el SHA del commit del repo_motor.
