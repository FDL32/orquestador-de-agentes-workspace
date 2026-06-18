# Work Plan: WOT-2026-010t

> Origen: `WOT-2026-010r` recomendo adaptar el vocabulario de `codebase-design` al review del Manager. Este ticket convierte esa recomendacion en checklist y anti-patron local, sin tocar codigo ni importar el bundle externo.

## Metadata

- **ID:** WOT-2026-010t
- **Contract ID:** T-010T-001
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010r (completed)

## Objetivo

Adaptar conceptualmente el vocabulario de diseno profundo (`deep module`, `interface`, `seam`, `adapter`, `deletion test`, `interface is the test surface`) al review del Manager. El resultado debe ayudar a detectar sobreingenieria, wrappers superficiales y seams inventados, usando un ejemplo real del motor como referencia.

## Hechos verificados de arranque

- `010r` esta cerrado canonicamente y `validate --json` esta 0/0.
- El reporte `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md` existe en `repo_motor` y recomienda `010t` para vocabulario de review.
- `review-checklist.md` y `anti-patterns.md` existen como superficies vivas del Manager.
- El ticket es `documentation`: no requiere pytest/ruff salvo que el Builder toque codigo, lo cual esta prohibido.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar:

- que `v1.0.1` no cambia de forma material `codebase-design` o `diagnosing-bugs`; si cambia, documentar diferencia o emitir CONTRACT_GAP;
- que `skills/man-review-implementation/references/review-checklist.md` es el checklist activo;
- que `skills/_shared/anti-patterns.md` es la fuente canonica AP;
- que `skills/systematic-debugging/SKILL.md` conserva el limite local de 3 intentos;
- que existe un artefacto real para el ejemplo, preferentemente `WOT-2026-009b scope_gate` o un decision artifact equivalente.

Registrar en `execution_log.md`:

- fuentes externas verificadas y SHA/tag usados;
- artefacto real elegido como ejemplo;
- cualquier normalizacion de encoding necesaria en archivos tocados.

## Files Likely Touched

### repo_motor
- `skills/man-review-implementation/references/review-checklist.md`
- `skills/_shared/anti-patterns.md`
- `CREDITS.md`
- `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010t.md`
- `.agent/collaboration/AUDIT_WOT-2026-010t.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`
- `.agent/planning/ticket_contracts.md`

## Read/inspect only

- `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
- `skills/_shared/ticket-anti-patterns.md`
- `skills/systematic-debugging/SKILL.md`
- `skills/man-review-implementation/SKILL.md`
- `.agent/runtime/reviews/`
- `.agent/collaboration/_archive/plan_audit/`

## Manager-only

- verificar que el vocabulario describe seams/adapters existentes, no exige abstracciones nuevas;
- verificar que `CREDITS.md` usa source pinneado y `Adapted`;
- verificar que no se toca codigo ni discovery;
- verificar que encoding guard no oculta una reescritura masiva no revisable.

## Decision Arquitectonica

- El vocabulario es una herramienta de review, no una regla para crear capas nuevas.
- `interface is the test surface` debe usarse para preguntar que contrato observable se prueba, no para exigir mas mocks.
- `deletion test` se usa como heuristica de valor: si borrar el wrapper no cambia comportamiento ni claridad, probablemente es AP-03 o sobreingenieria.
- `diagnosing-bugs` puede enriquecer el lenguaje de causa raiz, pero NO reemplaza `systematic-debugging` ni su limite de 3 intentos.

## Criterios Binarios

- [ ] `review-checklist.md` incluye preguntas accionables para `deep module`, `interface`, `seam`, `adapter`, `deletion test` y `interface is the test surface`.
- [ ] `anti-patterns.md` incluye anti-patron o refinamiento sobre seam/adapter inventado y sobreingenieria por vocabulario.
- [ ] Existe `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md` con ejemplo real aplicado a un artefacto existente.
- [ ] El documento contrasta `diagnosing-bugs` con `systematic-debugging` y conserva el limite de 3 intentos.
- [ ] `CREDITS.md` incluye fila `WOT-2026-010t` con fuente pinneada, licencia MIT verificada y `Adapted`.
- [ ] No se toca codigo, discovery, resolver, bus, prompts ni dependencias.
- [ ] Encoding guard pasa sobre todos los archivos tocados.
- [ ] `validate --json --project-root <repo_destino>` termina 0 errors / 0 warnings.

## Non-goals

- NO migrar taxonomia `user/model-invoked` (`010s`).
- NO tocar `triggers`, discovery, resolver ni bus.
- NO copiar archivos del bundle externo.
- NO introducir nuevas abstracciones productivas.
- NO modificar prompts generales fuera del review checklist.
- NO cambiar el limite de 3 intentos de `systematic-debugging`.

## Forbidden Surfaces

- codigo Python
- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/local_audit.py`
- `scripts/orquestador.py`
- `scripts/validate_agent_config.py`
- `bus/skill_resolver.py`
- `skills/` fuera de `skills/man-review-implementation/references/review-checklist.md` y `skills/_shared/anti-patterns.md`
- `prompts/`
- `pyproject.toml`
- `uv.lock`
- bundle externo copiado
- bus editado manualmente
- `privada/`
- `.env`