# work_plan.md -- WOT-2026-008i

## Metadata

- **ID:** WOT-2026-008i
- **Contract ID:** T-008I-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Renombrar atomicamente las cuatro skills `man-*` a `manager-*` y migrar sus
consumidores vivos operativos sin tocar `bui-*`, sin cambiar `triggers`, sin
romper `manager_review.md` ni `--check-contract`, y preservando la paridad
funcional del discovery. El nombre de directorio de skill se trata como
superficie interna del bundle; la compatibilidad se garantiza actualizando los
consumidores vivos y manteniendo los mismos triggers, no inventando un segundo
resolver de aliases.

## Non-goals

- No tocar `bui-*` ni abrir `008j` antes de tiempo.
- No cambiar `triggers`.
- No cambiar `contract_id`.
- No tocar prompts `audit_*`.
- No tocar bus, runtime o eventos.
- No introducir dependencias nuevas.
- No redisenar discovery salvo ajustes estrictamente necesarios para el rename.

## Premisas verificadas antes de Builder

- `WOT-2026-008g`, `008e`, `008h` y `008k` estan COMPLETED.
- `DEC-008G-001` serializa `008i` como el lote de expansion `man-*` ->
  `manager-*`.
- `manager_review.md` ya es el prompt canonico desde `008e`; el binding de
  `man-review-implementation` sigue apuntando a ese prompt y debe migrarse sin
  romper `--check-contract`.
- Los cuatro directorios candidatos son hoy:
  - `skills/man-create-work-plan/`
  - `skills/man-resolve-escalation/`
  - `skills/man-review-implementation/`
  - `skills/man-session-closeout/`
- Hay consumidores vivos operativos de esos nombres en prompts, skills,
  registro y tests; no basta con pasar `--check-naming`.
- `008i` NO depende de stubs ejecutables de skill: la compatibilidad viva se
  mide sobre `triggers`, `source_prompt` y referencias operativas.

## Decision Arquitectonica

Esta pasada usa migracion atomica de nombres de skill, no stubs de skill.
Motivo: a diferencia de los prompts, discovery no tiene hoy un mecanismo
canonico y declarativo de alias para skills equivalente a `legacy_aliases:`.
Crear uno dentro de `008i` seria ampliar el scope y el grafo de compatibilidad.

Regla de compatibilidad del ticket:
- conservar triggers y semantica de dispatch;
- actualizar bindings y consumidores vivos a `manager-*`;
- tolerar restos `man-*` solo en historia, DEC, changelog, backlog o tests de
  compatibilidad explicitamente justificados.

Si aparece un consumidor runtime real del path legacy `skills/man-*`, eso es
`CONTRACT_GAP`, no una invitacion a improvisar un resolver paralelo.

## Files Likely Touched

### repo_motor

- `skills/man-create-work-plan/`
- `skills/man-resolve-escalation/`
- `skills/man-review-implementation/`
- `skills/man-session-closeout/`
- `prompts/manager_review.md`
- `prompts/orchestrator_pipeline.md`
- `prompts/orchestrator_session_close_chat.md`
- `skills/orchestrate-pipeline/SKILL.md`
- `skills/project-finalize/SKILL.md`
- `skills/audit-pipeline/SKILL.md`
- `skills/grill-work-plan/SKILL.md`
- `skills/session-close-observations/SKILL.md`
- `skills/README.md`
- `skills/validate_all.py`
- `skills/create-agent-skill/references/frontmatter-template.md`
- `skills/create-agent-skill/references/skill-anatomy.md`
- `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`
- `docs/registry/INDEX.md`
- `tests/test_discover_skills.py`
- `tests/test_check_naming.py`
- `tests/test_agent_readme_references.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
- `docs/decisions/DEC-008D-001-naming-convention.md`
- `prompts/review_manager.md`
- `CHANGELOG.md`
- `backlog.md`
- `ticket_contracts.md`
- `tests/sandbox/**`
- `bus/runtime/events`

## Forbidden Surfaces

- Tocar `bui-*`.
- Tocar `audit_*` fuera de consumidores prose explicitamente declarados.
- Cambiar `triggers`.
- Cambiar `contract_id`.
- Introducir alias runtime nuevos para skills.
- Tocar bus/runtime/events manualmente.
- Tocar dependencias.

## Criterios binarios

- Existen los cuatro directorios canonicos `skills/manager-create-work-plan/`,
  `skills/manager-resolve-escalation/`,
  `skills/manager-review-implementation/` y
  `skills/manager-session-closeout/`.
- `prompts/manager_review.md` referencia
  `skills/manager-review-implementation/SKILL.md` y conserva
  `contract_id: cid-man-review-v2`.
- Los consumidores vivos declarados en FLT usan `manager-*` al cierre.
- `rg` de `man-create-work-plan|man-resolve-escalation|man-review-implementation|man-session-closeout`
  sobre superficies operativas solo deja historia/DEC/changelog/backlog/tests de
  compatibilidad justificadas.
- `python scripts/discover_skills.py --check-contract` queda verde.
- `python scripts/discover_skills.py --check-naming` queda verde.
- `python scripts/check_skill_collisions.py` queda verde.
- `python scripts/discover_skills.py --check-index` queda verde tras regenerar
  `docs/registry/INDEX.md`.
- La paridad pre/post de discovery conserva los mismos triggers funcionales; el
  diff del JSON queda limitado a rutas/nombres derivados por el rename.
- Existe una barrera que detecta referencias prose vivas a los nombres `man-*`
  en consumidores operativos del lote.
- `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all`
  y `validate --json --project-root <repo_destino>` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008i.md` y parar si aparece un consumidor runtime real del
path `skills/man-*`, si preservar compatibilidad exige un alias de skill no
soportado limpiamente por discovery, o si el rename deriva a `bui-*` o a
cambios de trigger/dispatch.