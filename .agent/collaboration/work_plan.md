# Work Ticket - WT-2026-240a

## Metadata
- **ID:** WT-2026-240a
- **Title:** Bloquear repo_motor sucio en pre-handoff documental
- **Scope:** system/documentation-prehandoff-hygiene
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-239a

## Objetivo
Corregir el bypass documental introducido en `WT-2026-239a` para que los
tickets `documentation/research/analysis` sigan bloqueando cuando el
`repo_motor` tiene cambios productivos sin commit, pero sin volver a exigir
auto-commit, tag o checkpoint en la rama documental.

## Contexto verificado
- `WT-2026-239a` dejo identificado el seam correcto en `_handle_pre_handoff()`,
  pero no cumplio aceptacion.
- La revision de Manager en `MANAGER_REVIEW_WT-2026-239a.md` confirma dos
  blockers:
  - el bypass documental no llama a `motor_uncommitted_productive()`;
  - el test nuevo especifica el comportamiento incorrecto.
- El siguiente trabajo debe ser un fix minimo en `repo_motor`, no una
  refactorizacion del protocolo completo.

## Problema
La rama documental de `--pre-handoff` permite pasar con `repo_motor` sucio
porque salta directo al chequeo de `git status` del repo activo. En topologia
motor/destino eso omite por completo cambios productivos no commiteados del
motor.

## Contrato
- El ticket es `code`: el cambio vive en `repo_motor` y requiere tests focales.
- La correccion minima debe:
  - llamar a `motor_uncommitted_productive()` al entrar en la rama documental;
  - emitir `HANDOFF_BLOCKED` y retornar `1` si `repo_motor` esta sucio;
  - conservar el bypass de auto-commit, tag y checkpoint cuando `repo_motor`
    este limpio;
  - invertir el test erroneo de `WT-2026-239a` y anadir regresion para tickets
    `code`.

## Files Likely Touched
- `.agent/agent_controller.py`
- `tests/test_pre_handoff_multirepo.py`

## Decision Arquitectonica
- Mantener el fix concentrado en `_handle_pre_handoff()`.
- No tocar `manager-approve`, `review_bridge` ni `EventBus` en este ticket.
- El bypass documental debe saltar solo el auto-commit, tag y checkpoint, no la
  higiene productiva del `repo_motor`.

## Non-goals
- No resolver en este ticket la deuda de `event_bus.py` sobre eventos no
  canonicos.
- No duplicar funciones de pre-handoff para tickets `documentation` vs `code`.
- No reabrir `WT-2026-239a`; este ticket corrige el bug detectado por su review.

## Plan de ejecucion
1. Insertar el chequeo de `motor_uncommitted_productive()` al inicio de la rama
   documental.
2. Ajustar la salida de error documental para bloquear con `HANDOFF_BLOCKED`
   cuando haya cambios productivos en `repo_motor`.
3. Invertir el test documental existente y anadir la regresion focal para
   tickets `code` si falta cobertura explicita.
4. Ejecutar `pytest`, `ruff` y `validate --json`, y registrar evidencia exacta
   en `execution_log.md`.

## Handoff al Builder
- `WT-2026-239a` dejo el seam identificado pero no cumplio aceptacion.
- El fix esperado es minimo: `agent_controller.py` +
  `test_pre_handoff_multirepo.py`.
- Antes de editar, compara tu diff previsto contra `Files Likely Touched`.
- No mezcles este ticket con deuda posterior de `WT-2026-241a`.
