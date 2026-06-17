# Work Plan: WOT-2026-010i

> Origen: la review de `WOT-2026-010e` detecto fallos de proceso que el sistema
> solo encontro tarde: packet sin commit visible, Forbidden Surfaces protegidas
> solo por contrato, test de fallback con falso verde y una regresion semantica
> que debe quedar blindada aunque el bug vivo ya este corregido.

## Metadata

- **ID:** WOT-2026-010i
- **Contract ID:** T-010I-001
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010e (cerrado), WOT-2026-010q (cerrado)

## Objetivo

Endurecer el pre-handoff y la evidencia de review para que tres fallos queden
bloqueados mecanicamente antes del Manager: diff que toca una Forbidden Surface
del `work_plan.md`, packet code/mixed sin commit visible del ticket, y test
semantico que no demuestra el campo leido frente al campo retornado. El cambio
debe producir barreras reutilizables con diagnostico self-service y tests que
fallen sin la proteccion correspondiente.

## Hechos verificados

- `WOT-2026-010e` esta cerrado canonicamente: bus seq 1103-1108.
- El bug de `_resolve_destino()` ya esta corregido: la lectura debe usar
  `destination_root`; `010i` lo blinda con test de regresion, no lo reabre.
- `WOT-2026-010q` ya exige suite canonica real al handoff; `010i` no relaja esa
  barrera ni cambia `run_pytest_safe.py`.
- `WOT-2026-010l` depende de este hardening antes de introducir selector focal.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar codigo:

- funcion o script que valida scope en `--pre-handoff` y `--mark-ready`;
- parser canonico de `Forbidden Surfaces` en `work_plan.md`, o ausencia de uno;
- fuente actual de commits visibles del ticket en repo_motor y como se compara
  contra el packet de review;
- tests existentes para `pre_handoff_guard`, `check_deliverables_exist`,
  `encoding_post_write_hook` y parsers FLT/contract;
- estado actual de `_resolve_destino()` y fixture minimo que demuestra que
  `destination_root` es el valor retornado.

Registrar en `execution_log.md`:

- seams exactos confirmados;
- decision de implementacion para cada barrera;
- cualquier superficie fuera del FLT antes de tocarla.

## Files Likely Touched

### repo_motor
- `scripts/pre_handoff_guard.py`
- `.agent/scope_gate.py`
- `scripts/check_deliverables_exist.py`
- `scripts/encoding_post_write_hook.py`
- `tests/test_pre_handoff_guard.py`
- `tests/unit/test_scope_gate.py`
- `tests/unit/test_check_deliverables_exist.py`
- `tests/unit/test_encoding_post_write_hook.py`
- `docs/protocol/review_packet_hardening_WOT-2026-010i.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010i.md`
- `.agent/collaboration/AUDIT_WOT-2026-010i.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only

- `prompts/launch_builder.md`
- `prompts/review_manager.md`
- `prompts/audit_ticket_contract.md`
- `docs/test_performance/test_performance_variance_WOT-2026-010p.md`
- `.agent/runtime/pytest-safe/last-run.json`

## Manager-only

- revisar que el diff real no toca Forbidden Surfaces declaradas;
- verificar que el commit productivo contiene `WOT-2026-010i`;
- `validate --json --project-root <repo_destino>` final en 0/0.

## Decision Arquitectonica

- Forbidden Surfaces se tratan como contrato ejecutable en handoff, no solo como
  texto de auditoria.
- Packet visible significa commit del repo_motor con el ticket en el mensaje o
  una razon CEM explicita; un dirty tree code/mixed no puede pasar a review.
- Tests semanticos deben observar el valor de salida o efecto real, no solo que
  una rama parezca cubierta por entorno.
- `010i` no cambia politica de suite canonica, no introduce selector focal y no
  modifica el schema de `last-run.json`.

## Criterios Binarios

- [ ] Un diff que toque una ruta listada en `Forbidden Surfaces` bloquea
      `--pre-handoff` o `--mark-ready` con diagnostico que nombre la ruta.
- [ ] Un ticket `code` o `mixed` sin commit visible del ticket bloquea handoff
      con remediacion accionable.
- [ ] Un ticket `documentation`, `research` o `analysis` conserva el flujo
      documental existente y no exige commit de codigo si no toca codigo.
- [ ] Existe test semantico que prueba que `_resolve_destino()` retorna
      `destination_root` desde `motor_destination_link.json`, no `motor_root`.
- [ ] Existe test negativo que demuestra que un test de fallback no puede pasar
      sin observar el fallback real o su efecto de subprocess.
- [ ] El diagnostico de cada barrera es self-service: incluye que fallo, ruta o
      campo implicado y comando o accion de remediacion.
- [ ] No toca `scripts/run_pytest_safe.py`, cache, xdist, sharding ni politica
      Builder/Manager fuera del handoff.
- [ ] Tests focales del area tocada pasan, `ruff check` aplica sobre Python
      tocado, encoding guard pasa sobre artefactos Markdown/Python tocados y
      `validate --json --project-root <repo_destino>` termina 0/0.

## Non-goals

- NO reabrir funcionalmente `WOT-2026-010e`.
- NO implementar selector focal de tests.
- NO cambiar `run_pytest_safe.py` ni el schema de `last-run.json`.
- NO convertir cualquier dirty tree en bloqueo continuo durante iteracion.
- NO relajar gates existentes para pasar handoff.

## Forbidden Surfaces

- `scripts/run_pytest_safe.py`
- cache pytest
- xdist/sharding
- politica de cierre Manager fuera del handoff
- bus editado manualmente
- `privada/`
- `.env`