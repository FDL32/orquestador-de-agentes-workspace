# AUDIT WT-2026-246a - Endurecer guard M3 y guiar recuperacion del Builder

## Estado
APPROVED

## Objetivo de auditoria
Verificar que el guard de `mark-ready` deja de aceptar checkpoints M3 obsoletos, que el Builder recibe instrucciones operativas precisas para recuperarse sin usar overrides incorrectos y que el ticket se trata como verificacion/commit de una implementacion ya precompletada en el arbol.

## TP Check
- TP-01: verificado - el flujo es lineal: verificar implementacion existente, endurecer guard, cubrir regresion, actualizar instrucciones del Builder.
- TP-02: verificado - los observables son binarios: bloqueo del stale checkpoint, tests verdes, validate verde y mensajes operativos concretos.
- TP-03: verificado - el scope mezcla codigo y documentacion operativa de forma legitima, por eso `deliverable_type` debe ser `mixed`.
- TP-04: verificado - el contrato objetivo es explicito: `checkpoint/review-<ticket>` debe coincidir con `HEAD`.
- TP-05: verificado - PLAN y AUDIT describen la misma ruta de recuperacion: `--pre-handoff --json --force`, no `--scope-override`.
- TP-06: verificado - el TP Check no sustituye gates funcionales.

## Fases de revision

### Fase 1 - Estado precompletado
- Verificar que la herencia operativa de `WT-2026-245c` (`STATE.md`, `TURN.md`, `execution_log.md`) se limpio o se aislo en un commit previo antes del commit productivo de `246a`.
- Verificar que la implementacion ya existe en el arbol de trabajo y que el Builder no rehace la solucion desde cero sin motivo.
- Verificar que el commit final del ticket contiene solo la superficie productiva declarada.

### Fase 2 - Guard canonico
- Verificar en `.agent/agent_controller.py` que `_resolve_motor_checkpoint_files()` ya no acepta como valido un tag que solo sea ancestro.
- Verificar que el mensaje distingue el caso stale del caso missing checkpoint.

### Fase 3 - Recuperacion Builder
- Verificar que el diagnostico recomienda reejecutar `--pre-handoff --json --force`.
- Verificar que el diagnostico prohbe explicitamente usar `--scope-override` para este caso.
- Verificar que `.opencode/agents/builder.md`, `prompts/launch_builder.md` y `skills/bui-implement-from-plan/SKILL.md` quedan alineados.

### Fase 4 - Regresion
- Verificar test automatizado para el caso "ancestor but not head".
- Verificar que los casos validos existentes del scope motor siguen pasando.

### Fase 5 - Quality gates
- Verificar exit code 0 de:
  - `ruff check .agent/agent_controller.py tests/test_mark_ready_motor_scope.py`
  - `pytest tests/test_mark_ready_motor_scope.py -q`
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers
- Los archivos canonicos de colaboracion heredados de `245c` siguen ensuciando el arbol y provocarian bloqueo del scope gate en `--mark-ready`.
- El guard sigue aceptando un checkpoint que no apunta a `HEAD`.
- El mensaje al Builder sigue siendo generico o sugiere `--scope-override` para un checkpoint stale.
- Falta cobertura automatica del caso stale ancestor.
- El Builder trata el ticket como implementacion desde cero y pisa la solucion ya presente en el arbol.
- Ruff, pytest focal o validate fallan.
