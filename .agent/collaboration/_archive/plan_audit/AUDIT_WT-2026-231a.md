# AUDIT_WT-2026-231a

## Tipo
Pre-handoff / packaging / commit evidence. Tier 3 con impacto en cierre canonico.

## Evidencia minima requerida
- Diff productivo revisable en `repo_motor` con commit `WT-2026-231a`.
- Tests multi-repo con repos git reales en `tmp_path`.
- Prueba de que `pre-handoff` commitea en `repo_motor`, no en `repo_destino`.
- Prueba de bloqueo fuera de FLT.
- Prueba de retry ante hook que modifica staged files.
- `mark-ready` no se relaja.

## TP Check
TP-01: el guard de motor sucio ya no hace `return 1` antes de evaluar commit-o-bloquea.
TP-02: cambios productivos dentro de FLT generan commit en `repo_motor` con ID del ticket.
TP-03: cambios productivos fuera de FLT bloquean mostrando los paths motor-relative
  fuera de FLT y no commitean.
TP-04: ronda vacia sin productivo mantiene bloqueo de `no implementation evidence`.
TP-05: `checkpoint/review-<ticket>` apunta al commit de entrega en `repo_motor`.
TP-06: paths FLT y paths de git se normalizan a `motor-relative` con `/`.
TP-07: hook/formatter que modifica staged files provoca re-add solo de paths incluidos
  en FLT y segundo commit, o bloqueo con stdout/stderr si falla de nuevo.
TP-08: no se crea tag en `repo_destino`; el tag dual queda fuera de WT-2026-231a.
TP-09: `mark-ready` mantiene su gate actual y pasa solo porque existe commit real.
TP-10: la decision commit-o-bloquea del motor no usa `get_changed_files()` ni el output
  absoluto de `parse_files_likely_touched()`; usa cambios y FLT normalizados a
  `motor-relative`.
TP-11: `motor_root` queda declarado antes del guard y no produce `NameError` cuando el
  destino tambien tiene `.git`.
TP-12: el bloque de tag `checkpoint/review-<ticket>` usa `cwd=motor_root`.

## Blockers esperados
- CRITICO: Builder resuelve `.agent/agent_controller.py` contra `repo_destino`
  en vez de contra `repo_motor`.
- CRITICO: Builder intenta leer estos paths del `repo_destino`: `PROJECT.md`,
  `.agent/collaboration/work_plan.md`, `.agent/config/` o
  `.agent/agent_controller.py`; el prompt ya contiene el contrato necesario y no debe
  pedir permisos extra.
- CRITICO: anadir logica de commit despues de un `return 1` del guard de WT-2026-228a
  sin reestructurar la barrera.
- CRITICO: commitear paths del motor que no estan incluidos en FLT.
- CRITICO: comparar paths absolutos contra FLT relativos y producir `files_to_stage=[]`.
- CRITICO: usar `get_changed_files()` como fuente de `delivery_changes` del motor en
  Modelo B.
- CRITICO: usar directamente `parse_files_likely_touched()` para la interseccion del
  motor sin normalizar desde las lineas raw de `## Files Likely Touched`.
- CRITICO: commitear o tagear `repo_destino` como parte del fix principal.
- ALTO: relajar `mark-ready` para aceptar ausencia de commit.
- ALTO: tests con mocks de git en vez de repos git reales.
- ALTO: re-add tras hook incluye paths fuera de FLT.
- ALTO: `motor_root` solo se declara en la rama donde `project_root` no tiene `.git`,
  dejando la rama Modelo B con riesgo de `NameError`.
- ALTO: cambiar `cwd` del commit pero olvidar el `cwd` del tag checkpoint.
- MEDIO: mensaje de bloqueo no incluye los paths motor-relative fuera de FLT.

## Revision Manager
El Manager debe verificar mecanicamente:
- `git -C <repo_motor> log --oneline -5`
  contiene commit con `WT-2026-231a`.
- `git show --stat <commit>` toca `.agent/agent_controller.py` y tests esperados.
- `git show --stat <commit>` no toca paths bajo `repo_destino`.
- `python -m pytest tests/test_pre_handoff_multirepo.py -v` -> exit code 0.
- `python -m pytest tests/test_pre_handoff_guard.py tests/test_agent_controller.py -q`
  -> sin regresiones.
- `ruff check .agent/agent_controller.py tests/test_pre_handoff_guard.py tests/test_pre_handoff_multirepo.py`
  -> limpio.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  -> 0/0, ejecutado por Manager desde `repo_destino`.
- `mark-ready` no contiene bypass nuevo para falta de commit.
- No existe nuevo tag `checkpoint/review-<ticket>` en `repo_destino` creado por este flujo.
- La implementacion no usa `get_changed_files()` ni paths absolutos de
  `parse_files_likely_touched()` para decidir el commit de `repo_motor`.
- El tag `checkpoint/review-<ticket>` se crea/refresca con `cwd=motor_root`.
