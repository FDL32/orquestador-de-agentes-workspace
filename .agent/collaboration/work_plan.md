# Work Plan: WOT-2026-010h

> Origen: la regla "el `<PREFIX>` de ticket es per-project, no universal" esta
> fijada en codigo (`bus/ticket_id.py`: `(?:WP|WT|[A-Z]{3})`) y parcialmente en
> `session_bootstrap.md` (lineas 59,88), pero NO es explicita ni consistente en
> los prompts de arranque/auditoria. Un agente en otro `repo_destino` podria
> asumir `WOT-` erroneamente. Este ticket propaga la regla a esos prompts.

## Metadata

- **ID:** WOT-2026-010h
- **Contract ID:** T-010H-001
- **Estado:** APPROVED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010a (completed)

## Objetivo

Propagar la regla de prefijo de ticket per-project a los prompts de arranque y
auditoria del motor, de modo que ningun agente asuma `WOT-` como prefijo
universal. `WOT-` debe describirse SOLO como el prefijo del motor/dogfooding; el
prefijo real de cada `repo_destino` se lee de su propio contrato
(`AGENTS.md`/`CLAUDE.md` autocargado) y se verifica via
`agent_controller --validate`.

## Hechos verificados (premise re-check read-only, 2026-06-17)

- `bus/ticket_id.py` define el prefijo per-project en codigo:
  `TICKET_ID_PATTERN = r"(?:WP|WT|[A-Z]{3})-\d{4}-[A-Za-z0-9]+"` (lineas 21,64,68).
  La regla per-project YA es verdad en runtime; falta hacerla explicita en docs.
- `prompts/session_bootstrap.md` lineas 59,88 ya describen parcialmente la regla
  (motor `WOT-YYYY-NNNx` canonical/legacy `WP-`/`WT-`; destino `XXX-YYYY-NNN`
  con `Ticket prefix: XXX` en `PROJECT.md`). Es la fuente a la que alinear.
- Gap confirmado con evidencia (`grep -ciE "prefix|prefijo|per-project"`):
  - `prompts/destination_bootstrap.md`: 1 mencion (parcial).
  - `prompts/audit_complete_motor_destination.md`: **0 menciones** (gap).
  - `prompts/audit_post_change_system_health.md`: **0 menciones** (gap).
- `scripts/check_ticket_nomenclature.py` existe y es el gate de cierre que
  clasifica generador/ejemplo-vivo vs historia.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar:

- la redaccion exacta de la regla per-project en `session_bootstrap.md`
  (lineas 59,62,88) para no contradecirla;
- el orden de fuente canonico: primario = `AGENTS.md`/`CLAUDE.md` autocargado del
  destino; verificacion = `agent_controller --validate` (no fiarse de una linea
  suelta de `PROJECT.md`);
- que ninguno de los 4 prompts ya contradiga la regla antes de tocarlos;
- que no se introduzcan ejemplos vivos nuevos con `WP-`/`WT-` (los romperia el
  gate de nomenclatura).

Registrar en `execution_log.md`: redaccion de referencia, gap por prompt y
cualquier contradiccion preexistente detectada.

## Files Likely Touched

### repo_motor
- `prompts/session_bootstrap.md`
- `prompts/destination_bootstrap.md`
- `prompts/audit_complete_motor_destination.md`
- `prompts/audit_post_change_system_health.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only

- `bus/ticket_id.py`
- `AGENTS.md`
- `scripts/check_ticket_nomenclature.py`
- `.agent/planning/ticket_contracts.md`

## Manager-only

- verificar que los 4 prompts no se contradicen entre si tras el cambio;
- verificar que `WOT-` queda descrito como prefijo del motor/dogfooding, no
  universal, en cada prompt tocado;
- `check_ticket_nomenclature.py` + encoding guard + `validate --json` en 0/0.

## Decision Arquitectonica

- La regla per-project es fuente unica: los prompts la REFERENCIAN y alinean con
  `session_bootstrap.md`; no se redefine en paralelo en cada prompt.
- `WOT-` es ejemplo del motor, nunca plantilla universal. Cualquier ejemplo de ID
  en estos prompts debe dejar claro que el prefijo se lee del repo activo.
- Cambio minimo y documental: no se toca codigo, runtime, bus ni gates.

## Criterios Binarios

- [ ] Cada uno de los 4 prompts dice explicitamente que el `<PREFIX>` se lee del
      contrato del repo activo, con ORDEN DE FUENTE: primario =
      `AGENTS.md`/`CLAUDE.md` autocargado del destino; cuando el sistema exige
      `Ticket prefix: XXX`, verificar via `agent_controller --validate` (no
      fiarse de una linea suelta de `PROJECT.md`).
- [ ] `WOT-` se describe SOLO como prefijo del motor/dogfooding, no universal.
- [ ] Los 4 prompts no se contradicen entre si.
- [ ] No se generan ejemplos vivos nuevos con `WP-`/`WT-`.
- [ ] `python scripts/check_ticket_nomenclature.py` pasa.
- [ ] `python scripts/check_encoding_guard.py <md tocados>` exit 0.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
      termina 0 errors / 0 warnings.

## Non-goals

- NO mezclar con `WOT-2026-010g` (010g = clasificacion/retirada de legacy;
  010h = endurecer nomenclatura de prefijo).
- NO tocar codigo, runtime, bus, gates ejecutables ni el regex de
  `bus/ticket_id.py`.
- NO reescribir historia de commits ni ejemplos legacy etiquetados.
- NO tocar documentacion general (`QUICKSTART.md`, `INTERACTION_MODES.md`) en
  esta ronda.

## Forbidden Surfaces

- `bus/ticket_id.py` (codigo del regex; solo lectura)
- `privada/`
- `.env`
- `.agent/runtime/memory/`
- bus editado manualmente
- `QUICKSTART.md`, `INTERACTION_MODES.md`
- codigo/tests/CLI ejecutable
