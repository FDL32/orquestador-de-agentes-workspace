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
TP-03: cambios productivos fuera de FLT bloquean con lista exacta y no commitean.
TP-04: ronda vacia sin productivo mantiene bloqueo de `no implementation evidence`.
TP-05: `checkpoint/review-<ticket>` apunta al commit de entrega en `repo_motor`.
TP-06: paths FLT y paths de git se normalizan a `motor-relative` con `/`.
TP-07: hook/formatter que modifica staged files provoca re-add solo de paths en scope
  y segundo commit, o bloqueo claro si falla de nuevo.
TP-08: no se crea tag en `repo_destino`; el tag dual queda fuera de scope.
TP-09: `mark-ready` mantiene su gate actual y pasa solo porque existe commit real.

## Blockers esperados
- CRITICO: anadir logica de commit despues de un `return 1` del guard de WT-2026-228a
  sin reestructurar la barrera.
- CRITICO: commitear todo lo sucio del motor sin validar FLT.
- CRITICO: comparar paths absolutos contra FLT relativos y producir `files_to_stage=[]`.
- CRITICO: commitear o tagear `repo_destino` como parte del fix principal.
- ALTO: relajar `mark-ready` para aceptar ausencia de commit.
- ALTO: tests con mocks de git en vez de repos git reales.
- ALTO: re-add tras hook incluye paths fuera de FLT.
- MEDIO: mensaje de bloqueo no lista paths fuera de scope.

## Revision Manager
El Manager debe verificar mecanicamente:
- `git -C C:\Users\fdl\Proyectos_Python\orquestador_de_agentes log --oneline -5`
  contiene commit con `WT-2026-231a`.
- `git show --stat <commit>` toca `.agent/agent_controller.py` y tests esperados.
- `python -m pytest tests/test_pre_handoff_multirepo.py -v` -> todos pasan.
- `python -m pytest tests/test_pre_handoff_guard.py tests/test_agent_controller.py -q`
  -> sin regresiones.
- `ruff check .agent/agent_controller.py tests/test_pre_handoff_guard.py tests/test_pre_handoff_multirepo.py`
  -> limpio.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  -> 0/0, ejecutado por Manager desde `repo_destino`.
- `mark-ready` no contiene bypass nuevo para falta de commit.
- No existe nuevo tag `checkpoint/review-<ticket>` en `repo_destino` creado por este flujo.
