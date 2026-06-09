# Work Ticket - WT-2026-244a

## Metadata
- **ID:** WT-2026-244a
- **Title:** Formalizar policy de mergeabilidad y review inspirada por FrontierCode
- **Scope:** system/review-quality-policy
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** documentation
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-243a

## Objetivo
Convertir `AUDIT_FRONTIERCODE_LEARNINGS.md` en politica operativa local para
Builder y Manager, sin introducir un gate nuevo ni tocar codigo productivo. El
ticket se considera cumplido cuando:
- `PROJECT.md` anade una seccion durable que dice explicitamente que
  `APROBADO` exige `validate --json` con `0 errors` y `0 warnings
  estructurales`, y que la implementacion correcta es `allowlist ->
  endurecer gate`.
- `AGENTS.md` anade una regla builder-facing con la etiqueta literal
  `[NON-REVERSE-CLASSICAL: <razon breve>]` para tests de contrato o cobertura
  cuando no aplique reverse-classical.
- `PROJECT.md` o `AGENTS.md` definen `BLOCKERS` con al menos estos casos:
  errores en `validate --json`, bugfix sin evidencia suficiente del bug o sin
  etiqueta `[NON-REVERSE-CLASSICAL: ...]`, y `scope creep`. Tambien definen
  `NITS` con al menos estos casos: legibilidad, refactors no necesarios y
  mejoras de estilo no bloqueantes.
- `PROJECT.md` o `AGENTS.md` reconocen explicitamente `Files Likely Touched`,
  `non-goals` y la regla "seguir patrones existentes del codebase o justificar
  cualquier patron nuevo" como parte del criterio de mergeabilidad.
- El diff queda limitado a `PROJECT.md`, `AGENTS.md` y
  `.agent/collaboration/AUDIT_FRONTIERCODE_LEARNINGS.md`.
- `validate --json` del `repo_destino` termina con `errors: {}`.

## Contexto verificado
- `AUDIT_FRONTIERCODE_LEARNINGS.md` ya consolida los aprendizajes de
  FrontierCode y rondas sucesivas de auditoria esceptica.
- El riesgo principal no es "falta de benchmark", sino dejar la politica en
  terminos abstractos o duplicar gates ya existentes.
- El sistema ya tiene barreras parciales equivalentes a `scope discipline`
  (`Files Likely Touched`, `non-goals`, review de diff) que deben reconocerse y
  mantenerse como barreras auditables, no reemplazarse.

## Contrato
- Ticket documental puro: no tocar codigo productivo ni schemas del bus.
- Convertir en regla explicita el gate de cierre existente (`validate --json`
  con `0 errors` y `0 warnings estructurales`); no inventar un "mergeability
  gate" nuevo.
- Reverse-classical solo para bugfixes; tests de contrato o cobertura nueva
  requieren justificacion trazable.
- La politica debe distinguir `BLOCKERS` de `NITS`.
- La politica debe dejar claro que la implementacion correcta es:
  `allowlist de warnings no bloqueantes -> gate 0 warnings estructurales`.
- La politica debe vivir unicamente en `PROJECT.md`, `AGENTS.md` y, si hace
  falta, ajustes menores del audit consolidado.

## Files Likely Touched
- `PROJECT.md`
- `AGENTS.md`

## Non-goals
- No cambiar `validate --json` en este ticket.
- No tocar `agent_controller.py`, `review_bridge.py` ni tests del motor.
- No introducir severidades complejas si una allowlist corta basta.
- No acortar `work_plan.md` por decreto.

## Quality Gates
```powershell
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Decision Arquitectonica

**Problema:** El audit sobre FrontierCode ya destilo una politica plausible,
pero todavia vive como analisis, no como contrato operativo builder-facing.

**Decision:** Formalizar primero la politica en documentacion local del
`repo_destino`, usando `PROJECT.md` y `AGENTS.md` como superficies durables.
La politica debe endurecer lo existente (`validate --json`, review packet,
scope discipline) sin crear un gate paralelo.

**Alternativa descartada:** implementar de inmediato un cambio de codigo en
`validate --json` o un sistema de severidades completo. Se descarta porque el
audit concluye que primero hace falta fijar la politica, la allowlist y la
distincion entre warnings estructurales y advisories.

**Impacto:** Builder y Manager tendran una regla explicita y auditable sobre:
- cuando `validate --json` bloquea el cierre;
- cuando reverse-classical aplica y cuando debe dejarse la etiqueta
  `[NON-REVERSE-CLASSICAL: ...]`;
- como se separan `BLOCKERS` y `NITS`;
- como `Files Likely Touched`, `non-goals` y convenciones del codebase cuentan
  como mergeabilidad.

## Nota de artefactos

- `AUDIT_FRONTIERCODE_LEARNINGS.md` vive en `repo_destino` y actua como
  referencia argumental, no como entregable principal del diff del
  `repo_motor`.
- Builder puede citarlo o ajustarlo si hace falta para coherencia documental,
  pero el entregable gobernante del ticket es la policy formalizada en
  `PROJECT.md` y `AGENTS.md`.
