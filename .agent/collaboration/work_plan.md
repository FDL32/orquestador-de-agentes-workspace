# Work Ticket - WT-2026-239a

## Metadata
- **ID:** WT-2026-239a
- **Title:** Separar protocolo de cierre para tickets documentation vs code
- **Scope:** system/documentation-closeout-protocol
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-238a

## Objetivo
Separar el protocolo de cierre de tickets `documentation` frente a tickets
`code`, empezando por una solucion minima en el `repo_motor`: bypass condicional
del `pre-handoff` existente cuando el deliverable real es documental.

## Contexto verificado
- `WT-2026-237a` quedo cerrado como ticket de codigo.
- `WT-2026-238a` quedo cerrado como ticket documental/handoff.
- El backlog y el handoff ya registran que el siguiente gap real es la
  asimetria entre tickets documentales y la ruta actual de `pre-handoff`.
- En el codigo actual, `mark-ready` ya trata tickets no-code de forma distinta,
  pero `pre-handoff` sigue heredando comportamiento de ticket `code`.

## Problema
El motor sigue tratando parte del cierre de tickets `documentation` como si
fuera cierre de tickets `code` con menos diff. Eso provoca `HANDOFF_BLOCKED`
por checkpoint, commit gates o `pre-handoff` no adecuados al deliverable real.

## Contrato
- El ticket es `code`: el fix vive en `repo_motor` y debe venir con tests
  focales y gates reales.
- El output minimo era:
  - bypass condicional en `pre-handoff` para tickets documentales;
  - cierre Builder -> Manager -> Supervisor sin checkpoint/commit manual para
    esa rama;
  - tests de ciclo real para el branch documental;
  - `validate --json` del `repo_destino` sin errores.

## Decision Arquitectonica
- Este cierre no reescribe el resultado tecnico del ticket ni lo maquilla como
  `COMPLETED`.
- La decision es conservar `WT-2026-239a` como ticket revisado con resultado
  `CHANGES`, dejando el hallazgo y la evidencia en un artefacto canonico de
  Manager.
- Asi evitamos mezclar el cierre de `239a` con la activacion prematura de un
  ticket siguiente.

## Non-goals
- No activar todavia un ticket sucesor.
- No reescribir el bus para forzar un `COMPLETED` artificial.
- No mezclar el cierre de revision de `239a` con cambios de `repo_motor`.

## Estado de revision
- **Resultado Manager:** `CHANGES`
- **Cierre del ticket:** no aprobado como `COMPLETED`
- **Motivo principal:** el bypass documental implementado no detecta
  `repo_motor` sucio y el test nuevo cementa ese comportamiento.
- **Artefacto canonico de revision:** `MANAGER_REVIEW_WT-2026-239a.md`

## Cierre documental
- El seam real quedo identificado.
- La implementacion no cumplio aceptacion.
- No hay siguiente ticket activo todavia en este cierre.
- Cualquier follow-up posterior debe arrancar como ticket nuevo, no como cierre
  implicito de `WT-2026-239a`.
