# AUDIT_WOT-2026-014i

## Scope
- Ticket WOT-2026-014i, mixed (YAML/CI), delivery_authority repo_motor, cross-repo (motor + workspace).
- Objetivo auditado: bump de action-pins a primer major no-Node20 en 5 workflows (3 motor + 2 workspace), sin cambiar logica.

## TP Check
- TP-01: solo cambia el tag de version de cada uses: (checkout@v5, setup-python@v6, upload-artifact@v5, setup-uv@v6); steps/env/logica intactos.
- TP-02: regla cross-repo = 1 ticket / 2 commits (motor + workspace).
- TP-03: cada YAML parsea; validate del workspace 0/0; run_pytest_safe del motor verde.
- TP-04: gitleaks (CLI OSS) y FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 no se tocan (salvo confirmacion para el segundo).
- TP-05: EVIDENCIA PRIMARIA = workflow verde post-push sin anotacion Node-20 (Manager-only, gateada al push).

## Regression Focus
- Falso verde a evitar: dar el ticket por cerrado con solo gates locales (ruff/pytest vacuos) sin la evidencia
  CI-verde post-push. El cierre canonico de 014i REQUIERE la evidencia CI tras el push.
- No cambiar logica de jobs disfrazada de bump.

## Closing Rule
- No aprobar canonicamente 014i sin la evidencia CI-verde post-push (sin anotacion Node-20) en los workflows afectados,
  los DOS commits (motor + workspace) y sus SHA. Los gates locales solos NO bastan para mixed/CI.
