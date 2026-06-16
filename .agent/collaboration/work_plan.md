# Work Plan: WOT-2026-008c

> Origen: familia 008 tras cierre verificado de WOT-2026-008b y WOT-2026-010a (2026-06-16).
> Resolucion de blocker (2026-06-16): 008c se alinea con `DEC-008B-001`.
> NO introduce `registry.json` como fuente de verdad. La autoridad sigue siendo
> discovery recursivo + frontmatter; `INDEX.md` es proyeccion generada.

## Metadata

- **ID:** WOT-2026-008c
- **Contract ID:** T-008C-001
- **Estado:** COMPLETED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-008b

## Objetivo

Endurecer el catalogo logico de prompts y skills sin crear una segunda fuente de
verdad. La autoridad sigue siendo el discovery recursivo sobre frontmatter y
layout vivo; 008c anade proyeccion generada (`INDEX.md`), metadata de estado
(`active`/`deprecated`/`draft`) y gates de paridad/stale derivadas del discovery.

Root cause viva: hoy el discovery y el dispatch dependen de frontmatter aislado,
globs, nombres humanos y memoria local, pero no exponen de forma canonica estado,
aliases, owner/canonical_source ni una proyeccion auditable para humanos.

## Decision Arquitectonica

- **DEC mandataria:** `docs/decisions/DEC-008B-001-registry-model.md` adopta
  `Discovery recursivo sin manifest` y rechaza `registry.json` como autoridad.
- **Fuente de verdad:** frontmatter + layout en disco + `discover_skills.py`.
  No se crea `registry.json` en 008c.
- **Proyeccion humana:** `docs/registry/INDEX.md` se genera desde
  `discover_skills --json` y debe fallar si queda stale.
- **Metadata logica derivada:** `discover_skills.py` puede exponer `status`,
  `owner`, `canonical_source`, `kind` y `aliases`, pero derivadas de fuentes
  vivas, no de un manifest manual.
- **Paridad con frontmatter:** cualquier metadata nueva debe derivarse de
  frontmatter o reglas vivas verificables. No inventar semantica manual.
- **Sin deuda fisica:** no mover carpetas, no renombrar archivos, no crear
  shims fisicos en 008c.
- **Integracion minima:** tocar discovery/dispatch solo donde haga falta para
  que `active`/`deprecated`/`draft`/`aliases` tengan efecto real.

## Orden de ejecucion (obligatorio)

1. Inventario de fuentes vivas y callers de discovery/dispatch.
2. Disenar metadata derivada compatible con DEC-008B-001.
3. Extender `discover_skills.py --json` con catalogo enriquecido.
4. Generar `docs/registry/INDEX.md` desde discovery.
5. Anadir gate stale/paridad para discovery -> INDEX.
6. Integracion minima en dispatch para `active`/`deprecated`/`draft`/`aliases`.
7. Tests de paridad, stale y consumer path.

## Files Likely Touched

### repo_motor
- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/validate_agent_config.py`
- `scripts/run_gates_dispatch.py`
- `bus/skill_resolver.py`
- `docs/registry/README.md`
- `docs/registry/INDEX.md`
- `tests/test_discover_skills.py`
- `tests/test_check_skill_collisions.py`
- `tests/test_approval_state_revision_and_skill_access.py`
- `tests/test_refactoring_impact.py`
- `tests/test_registry_catalog.py`

Notas (no son parte del FLT parseable):
- NO crear `docs/registry/registry.json` ni otro manifest autoritativo.
- El catalogo derivado debe cubrir `prompts/*.md`, `skills/*/SKILL.md`,
  `skills/*/references/*.md`, `skills/_shared/*.md` y los consumidores
  `scripts/discover_skills.py`, `scripts/check_skill_collisions.py`,
  `scripts/validate_agent_config.py`, `scripts/run_gates_dispatch.py`,
  `bus/skill_resolver.py`.
- Si aparece necesidad de renames, aliases publicos o shims fisicos, detener y
  remitir a 008d.

### Read/inspect only
- `AGENTS.md`
- `docs/decisions/DEC-008B-001-registry-model.md`
- `prompts/orchestrator_pipeline.md`
- `prompts/session_bootstrap.md`
- `prompts/audit_ticket_contract.md`
- `skills/man-create-work-plan/SKILL.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `skills/_shared/ticket-anti-patterns.md`

### Manager-only
- Ejecutar stale gate de `INDEX.md`.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <destino>` final.

## Criterios Binarios

- [ ] `discover_skills.py --json` expone un catalogo enriquecido derivado del discovery, sin `registry.json` manual.
- [ ] `docs/registry/INDEX.md` es proyeccion generada del discovery y falla si queda stale.
- [ ] La metadata derivada cubre al menos `kind`, `path`, `status`, `owner`, `canonical_source` y `aliases` cuando aplique.
- [ ] `status` soporta al menos `active`, `deprecated` y `draft`, con default retrocompatible `active` cuando el frontmatter no lo declare.
- [ ] El discovery/dispatch tocado usa esa metadata derivada para `active`/`deprecated`/`draft`/`aliases`, sin depender solo de presencia en disco.
- [ ] El catalogo derivado cubre `prompts/*.md`, `skills/*/SKILL.md`, `skills/*/references/*.md`, `skills/_shared/*.md` y los consumidores `scripts/discover_skills.py`, `scripts/check_skill_collisions.py`, `scripts/validate_agent_config.py`, `scripts/run_gates_dispatch.py`, `bus/skill_resolver.py`.
- [ ] Existe gate local o de test que falla si `INDEX.md` queda stale respecto a `discover_skills --json`.
- [ ] No se crean manifests manuales, no se mueven carpetas y no se renombran archivos.
- [ ] `ruff check .` exit 0 sobre Python tocado.
- [ ] Tests focales del discovery/dispatch/INDEX exit 0.
- [ ] `validate --json` destino 0/0 al cierre.

## Non-goals

- NO introducir `registry.json` ni otro manifest autoritativo en disco.
- NO ejecutar renames de prompts/skills ni aliases publicos: eso es 008d.
- NO retirar compat legacy: eso es 008e.
- NO crear el gate de integracion destino-motor: eso es 008f.
- NO reimplementar scanners ya existentes si basta con delegar.
- NO convertir `INDEX.md` en documento manual.

## Forbidden Surfaces

- `_archive/`
- `privada/` y `.env`
- Cualquier manifest manual tipo `registry.json`
- Cualquier rename fisico de prompts/skills
- Scope de 008d, 008e o 008f
