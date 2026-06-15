# Work Plan: WOT-2026-007c - Validador stdlib-only de contratos de ticket y planning docs

## Metadata
- **ID:** WOT-2026-007c
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Validador de contratos de ticket y planning docs
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (nuevo script stdlib-only; no toca runtime/bus/controller).
- **Depende de:** WOT-2026-007a (COMPLETED 7bf57f8), WOT-2026-007b (COMPLETED bb60532)
- **Origen:** session-2026-06-14-contract-formation

## Objetivo
Implementar scripts/validate_contract_formation.py (stdlib-only) que valide
repo_charter, plan_graph, ticket_contracts y CONTRACT_GAP contra el contrato
de 007a. Incluye fixtures positivos y negativos; el negativo debe fallar por
contrato malformado real. Gate self-service: error indica archivo, campo, razon
y como revalidar.

## Non-goals

- No duplicar la logica de validate_ticket_prose.py (que ya valida work_plan.md).
  Este validador cubre los artefactos de planning (repo_charter, plan_graph,
  ticket_contracts), no el work_plan de ejecucion.
- No introducir dependencias externas (stdlib-only obligatorio).
- No validar el runtime bus ni el controller en este ticket.
- No implementar auto-fix: el validador es read-only y reporta; no muta artefactos.

## Decision Arquitectonica
- **Script:** scripts/validate_contract_formation.py
- **Tests:** tests/unit/test_validate_contract_formation.py
- **Fixtures:** tests/fixtures/contract_formation/ (positivo: ejemplo de 007b; negativo: variante malformada)
- **Alcance de validacion v1:**
  - ticket_contract: status, Premise Re-check, Objective-Link, Forbidden Surfaces, DoD, STOP, CONTRACT_GAP behavior, failure_modes en OBJ-*.
  - repo_charter: OBJ-*, failure_modes, Negative Audit Checklist, Non-Goals.
  - plan_graph: PLAN-*, Impact Simulation, Forbidden Surfaces.
  - CONTRACT_GAP: campos obligatorios.
- **Gate self-service:** cada error indica (archivo, campo, razon, comando de revalidacion).

## Files Likely Touched
- Builder: scripts/validate_contract_formation.py (nuevo)
- Builder: tests/unit/test_validate_contract_formation.py (nuevo)
- Builder: tests/fixtures/contract_formation/valid/ (fixture positivo de 007b)
- Builder: tests/fixtures/contract_formation/invalid/ (fixture negativo malformado)
- Builder: prompts/contract_formation_pipeline.md (anadir referencia al validador)
- Read/inspect only: docs/contract_formation/templates/, docs/contract_formation/examples/python_service_minimal/, scripts/validate_ticket_prose.py (patron de referencia)

## Criterios Binarios (DoD)
1. scripts/validate_contract_formation.py existe y es stdlib-only (0 imports no-stdlib).
2. Falla con error descriptivo si falta status, Premise Re-check, Objective-Link,
   Forbidden Surfaces, DoD, STOP, CONTRACT_GAP behavior en ticket_contract.
3. Falla si faltan failure_modes, Negative Audit Checklist o baseline evidence cuando existe validate.
4. Falla si una DEC-T1a no tiene evidencia corroborada.
5. Falla si un ticket documental declara criterios que dependen de Builder sin marcar mixed.
6. Incluye fixture positivo (pasa) y negativo (falla por contrato malformado: sin status frozen,
   sin failure_modes o sin checklist negativa).
7. Gate self-service: error indica archivo, campo, razon y como revalidar.
8. ruff check scripts/validate_contract_formation.py exit 0.
9. pytest tests/unit/test_validate_contract_formation.py verde (incluye test que falla sin la feature).
10. check_encoding_guard.py exit 0.
11. validate destino 0/0.

## STOP conditions
- Si validar Markdown requiere parser fragil o dependencia externa: limitar v1 a
  estructura simple (regex/split) y abrir follow-up; no introducir dependencia.
- Si la logica del validador duplica validate_ticket_prose.py: refactorizar para
  reutilizar, no duplicar.
- Si un test pasa sin la feature que pretende proteger (floor assertion): rechazar.

## Context Baseline
- repo_motor git_head: bb60532 (007b vertical validation)
- repo_destino validate_result: OK 0 errors (2 warnings bus-absent aceptados)
- generated_at: 2026-06-15

## Historial de Ejecucion
- 2026-06-15: Orquestador crea work_plan. Builder inicia implementacion del validador.

## Cierre Builder y Gates (READY_FOR_REVIEW)
- **Fecha:** 2026-06-15
- **ruff check + format:** scripts/validate_contract_formation.py exit 0
- **pytest-safe (suite canonica completa):** 2666 passed, 19 skipped, 0 failed
- **pytest test del ticket:** tests/unit/test_validate_contract_formation.py 29 passed
- **Barrera verificada:** el fixture negativo repo_charter_missing_failure_modes.md
  fallaba 2 tests cuando contenia el substring failure_modes (fixture irreal);
  corregido a omision genuina; ahora reporta OBJ-001:failure_modes real.
- **encoding guard:** 6 md tocados exit 0
- **pip-audit:** skip auditable (no se tocaron manifiestos de dependencias; WP-2026-092)
- **validate destino:** 0 errors (2 warnings bus-absent host-extends, accepted_health_exception)
- **AUTORIDAD DE CIERRE:** code/mixed requiere revision independiente real.
  El orquestador implemento como Builder; NO auto-aprueba. Estado READY_FOR_REVIEW
  hasta revision Manager independiente.
- **Entregables motor:** scripts/validate_contract_formation.py,
  tests/unit/test_validate_contract_formation.py,
  tests/fixtures/contract_formation/{valid,invalid}/,
  prompts/contract_formation_pipeline.md (seccion 11 actualizada).


## Respuesta a Revision Independiente (Manager subagente, CHANGES)
- **Veredicto recibido:** CHANGES, 3 blockers (verificados de forma independiente por el orquestador).
- **B1 (resuelto, motor 5dafbc7):** GAP_REQUIRED exigia `action`; la plantilla canonica
  contract_gap.md publica `requested_resolution`. Alineado. Test de regresion contra la plantilla real.
- **B2 (resuelto, motor 5dafbc7):** TICKET_REQUIRED no exigia `Premise Re-check` ni
  `Context Baseline Evidence`. Anadidos + 2 tests negativos barrera. Fixture valida y ejemplo 007b
  sincronizados para llevar Context Baseline.
- **B3 (diferido por decision de usuario):** drift bus/STATE.md/execution_log (siguen en 007a).
  Se reconcilia en el cierre canonico de 007c (mark-ready -> manager-approve) tras aprobacion,
  no por cirugia separada del bus. Warnings de validate documentados como pendientes de cierre.
- **Gates tras fix:** ruff 0; suite canonica 2676 passed / 19 skipped; encoding 0; tests del ticket 36 passed.
- **Estado:** COMPLETED, a la espera de aprobacion del usuario sobre los fixes para cierre canonico.
