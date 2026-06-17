# Work Plan: WOT-2026-010r

> Origen: `WOT-2026-010g` dejo inventario de prompts/skills y el release externo `mattpocock/skills@1.0.0` introduce taxonomia y vocabulario que pueden afectar `008c/008d`. Este ticket mide impacto y decide ruta; no adopta cambios productivos.

## Metadata

- **ID:** WOT-2026-010r
- **Contract ID:** T-010R-001
- **Estado:** COMPLETED
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010g (completed), WOT-2026-008b (completed)

## Objetivo

Crear un reporte durable que evalua `mattpocock/skills@1.0.0` contra el inventario local de `010g` y la cadena Plan 008. El reporte debe decidir que ideas conviene adaptar, que riesgos tiene cada una y que tickets posteriores (`010s`, `010t`, `008c/008d`) quedan afectados.

## Hechos verificados de arranque

- `010g` esta cerrado canonicamente: `STATE.md` = `WOT-2026-010g / COMPLETED` y bus contiene `SUPERVISOR_CLOSED`.
- `validate --json --project-root <repo_destino>` previo al arranque dio 0 errors / 0 warnings.
- GitHub release verificado por fetch web: tag `mattpocock-skills@1.0.0`, release commit `00ff03c`, primary change commit listado `47bde84`, publicado 2026-06-17 14:45 UTC.
- `gh` puede no estar autenticado; si falla, conservar el error literal y usar fetch web como fuente alternativa.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de escribir el reporte:

- existencia y contenido relevante de `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md`;
- estado real de `010r`, `010s`, `010t`, `008c`, `008d` y `008e` en backlog;
- consumidores locales del campo `triggers` y del discovery de skills con comandos reproducibles;
- si `disable-model-invocation` existe o no en el repo;
- licencia del repo externo antes de recomendar adopcion en tickets posteriores.

Registrar en `execution_log.md`:

- fuente usada para el release (`gh` o fetch web) y resultado literal;
- seams/consumidores confirmados;
- limitaciones de evidencia.

## Files Likely Touched

### repo_motor
- `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010r.md`
- `.agent/collaboration/AUDIT_WOT-2026-010r.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`
- `.agent/planning/ticket_contracts.md`

## Read/inspect only

- `CREDITS.md`
- `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md`
- `skills/`
- `prompts/`
- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/local_audit.py`
- `scripts/orquestador.py`
- `scripts/validate_agent_config.py`
- `bus/skill_resolver.py`
- `.agent/collaboration/backlog.md`
- `.agent/planning/ticket_contracts.md`

## Manager-only

- verificar que el reporte separa evidencia e inferencia;
- verificar que no se adopta ni se porta codigo externo;
- verificar que `CREDITS.md` no se modifica en `010r` salvo CONTRACT_GAP aprobado;
- revisar impacto declarado sobre `008c/008d`, `010s` y `010t`.

## Decision Arquitectonica

- `010r` es un ticket de decision y evidencia, no de migracion.
- Las ideas externas se tratan como `Adapted`, no `Ported`, salvo ticket posterior con aprobacion explicita.
- La taxonomia `user-invoked/model-invoked` no puede sustituir `triggers` por decreto: primero debe mapear consumidores locales y compatibilidad.
- El vocabulario `codebase-design` puede alimentar review del Manager solo si se convierte en checklist concreta en ticket posterior.

## Criterios Binarios

- [ ] Existe `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`.
- [ ] El reporte separa `VERIFICADO` e `INFERENCIA` en claims del release y del repo local.
- [ ] El reporte cubre `ask-matt`, `codebase-design`, `domain-modeling`, `diagnosing-bugs`, `writing-great-skills`, `resolving-merge-conflicts` y `docs/invocation.md`.
- [ ] El reporte mapea impacto sobre `008c`, `008d`, `010s` y `010t` con accion propuesta por pieza.
- [ ] El reporte contiene inventario reproducible de consumidores locales de `triggers` y discovery.
- [ ] `CREDITS.md` queda read-only y cualquier fila se difiere a tickets de adopcion (`010s` o `010t`).
- [ ] No se copian archivos del bundle externo ni se instalan dependencias.
- [ ] Encoding guard pasa sobre reporte y packet tocado.
- [ ] `validate --json --project-root <repo_destino>` termina 0 errors / 0 warnings.

## Non-goals

- NO modificar discovery, resolver, bus, review Manager ni skills locales.
- NO instalar ni copiar el bundle externo.
- NO actualizar `CREDITS.md` en este ticket salvo que el contrato se reabra explicitamente.
- NO ejecutar `010s` ni `010t` dentro de `010r`.
- NO cambiar la ruta de `008c/008d`; solo informar impacto y riesgos.

## Forbidden Surfaces

- `skills/`
- `prompts/`
- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/local_audit.py`
- `scripts/orquestador.py`
- `scripts/validate_agent_config.py`
- `bus/skill_resolver.py`
- `CREDITS.md`
- `pyproject.toml`
- `uv.lock`
- bus editado manualmente
- `privada/`
- `.env`
