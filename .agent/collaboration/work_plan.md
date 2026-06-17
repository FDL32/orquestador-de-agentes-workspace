# Work Plan: WOT-2026-010n

> Origen: `WOT-2026-010j` quedo bloqueado canonicamente porque el gate de
> deliverables no sabe resolver artefactos Builder que viven en `repo_motor`
> cuando el contrato los declara via `delivery_authority` y FLT namespaced.

## Metadata

- **ID:** WOT-2026-010n
- **Contract ID:** T-010N-001
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010j (CONTRACT_GAP confirmado)

## Objetivo

Corregir `scripts/check_deliverables_exist.py` para que resuelva deliverables
Builder segun su namespace (`repo_motor`/`repo_destino`) y/o
`delivery_authority`, sin relajar el gate a pass-open y sin obligar a duplicar
artefactos entre repos.

## Hechos verificados

- `WOT-2026-010j` produjo un deliverable real en
  `repo_motor/docs/test_performance/test_performance_baseline_WOT-2026-010j.md`.
- El cierre de `010j` quedo bloqueado por el gate no-bypassable de existencia
  de deliverables.
- El workaround de duplicar el artefacto en `repo_destino` contradice la
  Decision Arquitectonica del propio `010j`.
- Existe follow-up contractual congelado en `T-010N-001`.

## Fase 0: Diagnostico antes del cambio

Confirmar en codigo antes de editar:

- como `scripts/check_deliverables_exist.py` interpreta hoy `Files Likely Touched`
- si cada path declarado se resuelve relativo a `--project-root` sin distinguir namespace de FLT
- como `scripts/scope_gate.py` resuelve namespaces FLT
- que `Read/inspect only`, `Manager-only` y notas libres no deben contarse como
  deliverables Builder

Registrar en `execution_log.md`:
- seams confirmados
- reproduccion del caso real de `010j` indicando comando, path del deliverable
  en `repo_motor`, resultado del gate y codigo de salida
- desvio de scope detectado, si existe, con path exacto y justificacion CEM

## Files Likely Touched

### repo_motor
- `scripts/check_deliverables_exist.py`
- `tests/test_pre_handoff_guard.py`
- `tests/unit/test_check_deliverables_exist.py`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/scope_gate.py`
- `.agent/agent_controller.py`
- `scripts/pre_handoff_guard.py`
- `.agent/planning/ticket_contracts.md`
- `.agent/planning/contract_gaps/CG-WOT-2026-010j.md`
- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`

## Manager-only

- `validate --json --project-root <repo_destino>` final en 0/0
- verificar que `010j` puede cerrar tras el fix sin duplicar el reporte en
  `repo_destino`

## Decision Arquitectonica

- El fix debe vivir en el gate de deliverables, no en `010j`, porque la causa
  raiz es una resolucion incorrecta del namespace FLT/delivery_authority.
- `scope_gate.py` ya distingue `repo_motor` y `repo_destino`; el gate de
  existencia debe converger con esa misma semantica para evitar contratos
  divergentes.
- Duplicar artefactos entre repos para satisfacer el gate rompería la
  arquitectura host-extends y falsearia el contrato de tickets `analysis` o
  `documentation` con entrega legitima en `repo_motor`.

## Criterios Binarios

- [ ] Existe una barrera de regresion que reproduce el caso real de `010j` y
      falla sin el fix.
- [ ] Un deliverable Builder existente en `repo_motor` pasa el gate cuando el
      FLT o el contrato lo resuelven a `repo_motor`.
- [ ] Un deliverable Builder existente en `repo_destino` sigue pasando sin
      regresion.
- [ ] Una ruta namespaced invalida, ambigua o fuera de root falla cerrado con
      diagnostico que menciona el path leido, el namespace esperado y el root
      resuelto por el gate.
- [ ] El gate ignora `Read/inspect only`, `Manager-only` y notas no parseables
      como entregables Builder.
- [ ] `WOT-2026-010j` puede cerrar canonicamente sin duplicar el reporte en
      `repo_destino`.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors /
      0 warnings al handoff.

## Non-goals

- NO duplicar artefactos entre `repo_motor` y `repo_destino` para satisfacer el gate.
- NO convertir el gate en pass-open.
- NO mezclar optimizaciones de runner ni cambios de politica fuera de
  `scripts/check_deliverables_exist.py`, sus tests y la documentacion del gate
  si el fix cambia la regla operativa visible.

## Forbidden Surfaces

- `privada/`
- `.env`
- bus editado manualmente
- el reporte productivo de `WOT-2026-010j`
- cambios de politica de closeout fuera del gate de deliverables
