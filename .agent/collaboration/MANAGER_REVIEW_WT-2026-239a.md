# MANAGER REVIEW — WT-2026-239a

**Fecha:** 2026-06-08
**Status:** CHANGES (no aprobado)

---

## Resumen

El Builder implementó el bypass condicional en `_handle_pre_handoff()` y añadió un test focal. Sin embargo, la implementación contiene un defecto de seguridad crítico que contradice el objetivo del sistema: el bypass documental no verifica `motor_uncommitted_productive()`, permitiendo que cambios productivos no commiteados en `repo_motor` pasen el handoff sin bloqueo.

---

## Hallazgos

### CRÍTICO — Bypass documental no detecta motor sucio

**Localización:** `agent_controller.py:3693-3752`

El bypass para `documentation/research/analysis` salta directamente a `git status --porcelain` sobre `git_root` sin llamar a `motor_uncommitted_productive()`. Si `git_root` apunta a `repo_destino` (Model B), los cambios productivos en `repo_motor` no se detectan en absoluto.

**El test lo confirma como bug:**
`test_pre_handoff_multirepo.py:463` (`test_docs_ticket_skips_motor_commit`) crea un cambio productivo real en motor (`def new_handler(): pass` sobre un archivo en FLT) y verifica que `result == 0`. El test *especifica* el comportamiento incorrecto.

**Corrección requerida:**
La rama documental debe:
1. Llamar a `motor_uncommitted_productive()` **antes** del bypass.
2. Si hay cambios productivos en motor, emitir `HANDOFF_BLOCKED` y retornar 1.
3. Solo saltar el auto-commit/tag/checkpoint, no la verificación de higiene del motor.

### CRÍTICO — Test cementa el bug

`test_docs_ticket_skips_motor_commit` debe **invertirse**: motor sucio bajo ticket documental debe retornar 1, no 0.

### ALTO — execution_log.md desactualizado

El log muestra items `[ ]` sin marcar para las fases 1-3, aunque el código está implementado. Esto indica que el Builder no actualizó el log durante la ejecución.

### ALTO — Sin verificación de ciclo real

No hay evidencia de ejecución end-to-end:
- `--pre-handoff` documental real
- `--mark-ready` post-bypass
- `--manager-approve` documental
- `pytest`, `ruff`, `validate --json`

---

## Veredicto

**No apruebo el cierre de WT-2026-239a.**

El ticket queda como **no aceptado / superseded** por los siguientes tickets hijos:

1. **WT-2026-240a**: Corregir pre-handoff documental para bloquear `repo_motor` sucio e invertir el test.
2. **WT-2026-241a**: Hardening de `EventBus` para rechazar/normalizar eventos no canónicos y evitar reset de `sequence_number`.

---

## Próximos pasos

1. No cerrar 239a como COMPLETED.
2. Preparar work_plan, PLAN y AUDIT de WT-2026-240a comenzando por el bug de pre-handoff documental.
3. El handoff debe decir explícitamente: "239a dejó el seam identificado pero no cumplió aceptación."