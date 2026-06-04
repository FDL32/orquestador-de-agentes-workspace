# AUDIT_WT-2026-228a

## Tipo
Codigo de orquestacion / pre-handoff. Tier 3.

## Evidencia minima requerida
- Diff productivo revisable en `repo_motor`.
- Tests focales con repos git reales.
- Test de regresion que falla sin el fix.
- `ruff` limpio.
- `validate --json` con 0 errores y 0 warnings.

## TP Check
TP-01: `_handle_pre_handoff` es el seam tocado y no se crea ruta paralela.
TP-02: `repo_motor` con cambios productivos sin commit bloquea
`--pre-handoff`.
TP-03: el bloqueo incluye:
`Uncommitted productive changes in repo_motor: commit with ticket ID before handoff.`
y lista de archivos.
TP-04: cambios docs/collaboration-only no activan la barrera.
TP-05: `repo_motor` limpio con commit `WT-2026-228a` pasa.
TP-06: `repo_motor` limpio sin commit del ticket pasa en `--pre-handoff`.
TP-07: no hay auto-commit de cambios productivos del motor.
TP-08: se reutiliza `bus/evidence.py` sin usar `motor_productive` como proxy de
uncommitted files.
TP-09: sin scope creep hacia permisos, review packet, relaunch, locks o
`--mark-ready`.
TP-10: un commit reciente del ticket no se interpreta como dirty file.

## Blockers esperados
- CRITICO: implementacion que auto-commitea cambios productivos del motor.
- CRITICO: detector nuevo que duplica `bus/evidence.py`.
- CRITICO: bloqueo basado en `motor_productive` que confunde commits recientes
  con cambios sin commit.
- ALTO: test que mockea `git` en vez de usar repos reales.
- ALTO: test de regresion no demuestra fallo sin el fix.
- MEDIO: mensaje de bloqueo sin lista de archivos productivos.
- MEDIO: cambios fuera de `Files Likely Touched` sin justificacion CEM.

## Revision Manager
El Manager debe verificar mecanicamente:
- `git log --oneline -5` contiene commit con `WT-2026-228a`.
- `git show --stat <commit>` toca solo la whitelist o trae justificacion.
- `python -m pytest <tests_focales> -v` pasa.
- `ruff check <archivos_python_tocados>` pasa.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  devuelve 0/0.
- El test de regresion falla sin el fix mediante revert parcial seguro del
  archivo central, y pasa restaurado.
