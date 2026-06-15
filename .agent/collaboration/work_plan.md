# Work Plan: WOT-2026-008a

## Metadata

- **ID:** WOT-2026-008a
- **Contract ID:** T-008A-001
- **Estado:** APPROVED
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Depends on:** WOT-2026-007d (COMPLETED 11e7ad8)
- **Contract source:** .agent/planning/ticket_contracts.md (T-008A-001, status: frozen)

## Objetivo

Crear `.agent/docs/taxonomy_migration_WOT-2026-008a.md`: inventario verificable,
taxonomia objetivo y plan de compatibilidad para prompts/skills. Este ticket no
implanta la migracion ni modifica el repo_motor.

## Non-goals

- No mover, renombrar, borrar ni editar prompts o skills.
- No modificar discovery, collision checks, manifests, tests o docs del motor.
- No renombrar triggers, contract_id ni nombres publicos.
- No crear shims o aliases.

## Decision Arquitectonica

008a es analysis con autoridad en repo_destino porque el motor no conserva
historico operativo. Separar analisis de migracion evita un commit masivo y
permite probar primero las limitaciones reales de discovery y contratos.

## Builder

- Crear `.agent/docs/taxonomy_migration_WOT-2026-008a.md`.
- Registrar comandos, resultados y decisiones en `execution_log.md`.

## Read/inspect only

- `repo_motor/prompts/`
- `repo_motor/skills/`
- `repo_motor/scripts/discover_skills.py`
- `repo_motor/scripts/check_skill_collisions.py`
- `repo_motor/MANIFEST.distribute`, `MANIFEST.workspace`
- `repo_motor/skills/**/PROMPT_TEMPLATE.md`, `repo_motor/skills/**/references/`, `repo_motor/skills/_shared/`
- `repo_motor/scripts/build_llms.py` y otros consumidores de prompts/skills
- referencias en docs, tests, AGENTS.md, PROJECT.md, QUICKSTART.md y llms*.txt

## Manager-only

- Re-derivar el inventario y muestrear consumidores.
- Verificar que el motor sigue pristine.
- Ejecutar validate final y revisar que no hay implementacion encubierta.

## Criterios Binarios

- [ ] Inventario completo de prompts, skills, prompt templates, references, `_shared`, scripts/manifests/llms consumidores, sin rutas sin clasificar.
- [ ] Cada fila contiene ruta, API publica, consumidores, destino, compatibilidad,
      riesgo y fase propietaria.
- [ ] Superficies machine-executed, contratos y docs estan separadas.
- [ ] Limitacion de discovery/collision demostrada con evidencia de codigo.
- [ ] Profundidad de carpetas evaluada como hipotesis; no se precongela `maximo un nivel` sin evidencia.
- [ ] Comparativa manifest-first vs discovery por glob/recursivo, incluyendo referencia mattpocock/skills si se puede verificar; si `gh` no esta autenticado, registrarlo como limitacion.
- [ ] Una sola fuente canonica; shims temporales con retirada versionada.
- [ ] Fases posteriores y dependencias definidas sin ejecutar ninguna.
- [ ] Riesgos, STOP, rollback y gates exactos documentados.
- [ ] repo_motor `git status --short` vacio al handoff.
- [ ] encoding guard del entregable exit 0.
- [ ] validate destino exit 0, 0 errors, 0 warnings al handoff.

## Premise Re-check

- Contar prompts, SKILL.md, PROMPT_TEMPLATE.md, references y `_shared`.
- Inspeccionar loops/globs de discovery y collision check.
- Ejecutar `discover_skills.py --check-contract` y `check_skill_collisions.py`.
- Ejecutar busqueda actual de referencias excluyendo caches y reportes generados.
- Verificar que el entregable se escribe en repo_destino/.agent/docs, no en repo_motor/.agent/docs.
- Confirmar HEAD motor y destino; si cambia motor durante el ticket, STOP.

## Forbidden Surfaces

- Todo archivo del repo_motor.
- `.agent/planning/`, `work_plan.md`, backlog y STATE salvo controller/Manager.
- Bus `events.jsonl` editado manualmente.
- `privada/`, secretos y rutas personales.

## STOP conditions

- Cualquier accion que mueva, borre, renombre o edite el repo_motor.
- Inventario incompleto o consumidor no clasificable.
- Necesidad de decidir una API publica no cubierta por DEC-008-*.
- Cambio concurrente del HEAD del motor.
- Entregable o runtime escrito en repo_motor por root equivocado.
- Scope que derive hacia implementacion: abrir ticket posterior, no improvisar.
