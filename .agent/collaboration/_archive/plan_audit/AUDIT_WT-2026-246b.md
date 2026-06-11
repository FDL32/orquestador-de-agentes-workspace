# AUDIT WT-2026-246b - Idempotencia del closeout del launcher y guard autoritativo post-success

## Estado
PENDING

## Objetivo de auditoria
Verificar que el launcher deja de ejecutar closeout post-success sobre rounds ya entregados, que la consulta previa usa estado autoritativo real del ticket, que el stale guard del controller no se debilita y que los residuos de runtime del launcher no vuelven a ensuciar el `repo_motor`.

## TP Check
- TP-01: verificado - el problema esta acotado y tiene secuencia observable en bus (`BUILDER_EXIT` correcto seguido de closeout tardio/orphan).
- TP-02: verificado - el fix necesita contrato binario: o el launcher hace skip temprano en estado post-entrega o sigue emitiendo ruido.
- TP-03: verificado - el scope mezcla codigo y documentacion operativa de forma legitima, por eso `deliverable_type` debe ser `mixed`.
- TP-04: verificado - la autoridad debe seguir siendo el bus/controller, no `STATE.md`.
- TP-05: verificado - el ticket incluye dos residuos de entorno (`.opencode/opencode.json`, `nul`) que deben tratarse como observables verificables, no como anecdota.
- TP-06: verificado - el TP Check no sustituye pruebas de no-regresion ni gates funcionales.

## Fases de revision

### Fase 1 - Reproduccion del fallo real
- Verificar en `.agent/runtime/events/events.jsonl` de `WT-2026-246a` que el handoff correcto ocurrio antes del ruido del launcher.
- Verificar que los eventos tardios son `STALE_BUILDER_ORPHAN` o equivalentes post-success, no fallo primario del ticket.
- Verificar que el problema de autenticacion del Manager queda explicitamente fuera de alcance.

### Fase 2 - Guardia temprana del launcher
- Verificar en `scripts/launch_agent_terminals.ps1` que el launcher consulta estado autoritativo antes de relanzar closeout desde `finally`.
- Verificar que el skip se aplica para `READY_FOR_REVIEW`, `READY_TO_CLOSE`, `HUMAN_GATE` y `COMPLETED`.
- Verificar que el logging del skip incluye contexto suficiente (`ticket_id`, `round`, `bus_state`).
- Verificar que, si la consulta CLI falla o devuelve salida no parseable, el launcher procede con closeout (no skip).

### Fase 3 - Fuente de autoridad
- Verificar que la consulta del launcher no depende de `STATE.md` como autoridad primaria.
- Verificar que `.agent/agent_controller.py` expone una salida CLI estable y minima para este consumo.
- Verificar que la nueva salida no rompe contratos existentes del controller.
- Verificar que el parseado del output del nuevo flag funciona bajo `Set-StrictMode -Version Latest` con un fixture JSON minimo real.

### Fase 4 - No regresion del controller
- Verificar que el stale guard sigue bloqueando rounds viejos cuando el ticket aun esta en `IN_PROGRESS`.
- Verificar que no se debilita el contrato de `builder_lock.txt` ni la semantica de `--mark-ready`.
- Verificar que no reaparecen eventos duplicados de closeout en el camino exitoso.

### Fase 5 - Higiene runtime
- Verificar que `.opencode/opencode.json` no queda dirty tras el flujo.
- Verificar que `nul` no vuelve a aparecer como untracked tras la reproduccion o los tests del ticket.
- Verificar que cualquier salvaguarda adicional en `.gitignore` se trata como contencion de entorno, no como sustituto del fix raiz.

### Fase 6 - Quality gates
- Verificar exit code 0 de:
  - `ruff check .agent/agent_controller.py tests/test_mark_ready_motor_scope.py`
  - `pytest tests/test_mark_ready_motor_scope.py -q`
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers
- El launcher sigue ejecutando `--pre-handoff` o `--mark-ready` post-success sin consultar estado autoritativo.
- La nueva guardia usa `STATE.md` o cualquier proyeccion no autoritativa como fuente primaria.
- El fix debilita o bypassa el stale guard del controller cuando el ticket sigue en `IN_PROGRESS`.
- Siguen apareciendo `STALE_BUILDER_ORPHAN`, `HANDOFF_BLOCKED` o `BUILDER_EXIT` duplicados tras un closeout exitoso del mismo round.
- `.opencode/opencode.json` queda dirty al terminar el flujo o `nul` reaparece como untracked.
- Ruff, pytest focal o validate fallan.