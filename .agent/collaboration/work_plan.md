# work_plan.md -- WOT-2026-008k

## Metadata

- **ID:** WOT-2026-008k
- **Contract ID:** T-008K-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Formalizar `role: auditor` en las skills que son propiedad real del rol auditor,
sin renombrar directorios ni prompts. Esta pasada usa **opcion B**:
`discover_skills.py` y el catalogo exponen `role` como campo separado de
`owner`, sin cambiar la semantica actual de `owner`. Cumplimiento medible: las
cinco skills auditoras declaradas quedan con `role: auditor`, el catalogo/INDEX
reflejan `role` en columna separada, `bui-self-audit` permanece en `builder`,
las tres skills que hoy son contract-validated conservan `source_prompt` y
`contract_id`, y `validate --json --project-root <repo_destino>` cierra en
0 errors / 0 warnings.

## Non-goals

- No renombrar prompts `audit_*` ni skills.
- No tocar `skills/bui-self-audit/SKILL.md`.
- No migrar `man-*` o `bui-*`.
- No tocar bus, runtime o eventos.
- No cambiar dependencias ni launcher.
- No desenlazar `owner` de `author`/`role`.

## Premisas verificadas antes de Builder

- `WOT-2026-008g` y `WOT-2026-008h` estan COMPLETED.
- `DEC-008G-001` congelo que `audit_*` en prompts es familia transversal y que
  `008k` formaliza solo el rol de ciertas skills auditoras.
- `WOT-2026-008i` y `WOT-2026-008j` quedan diferidos segun `DEC-008G-001`; este
  ticket es independiente de la expansion `man-*`/`bui-*`.
- Las cinco skills candidatas se dividen hoy en dos grupos relevantes: tres con
  contrato vivo (`audit-git-publication`, `audit-pipeline`,
  `system-health-audit`) y dos sin `source_prompt` (`code-audit`,
  `local-audit`).
- `skills/bui-self-audit/SKILL.md` usa `role: builder` y queda fuera por
  propiedad real del artefacto.
- `repo_motor` ya no esta limpio: existe WIP parcial en
  `scripts/discover_skills.py`, cinco `SKILL.md` y `docs/registry/INDEX.md`.
  El Builder debe partir de ese estado real y documentar si continua sobre el
  WIP o si lo reajusta.
- `_derive_owner()` hoy deriva `owner` desde `("author", "role")`. Opcion B no
  cambia eso: anade `role` como campo separado del catalogo/INDEX y acepta que
  `owner` y `role` coincidan cuando no exista `author`.

## Decision Arquitectonica

La taxonomia se apoya en propiedad real del artefacto, no en el prefijo del
nombre. Por eso los prompts `audit_*` siguen como familia transversal, mientras
que estas cinco skills pasan a `role: auditor`. `bui-self-audit` no migra: es
una skill del builder para auto-auditar su propio trabajo, no una skill del rol
auditor.

Decision de contrato para evitar falso verde: `auditor` entra en el opt-in de
`_check_contract()` para que `audit-git-publication`, `audit-pipeline` y
`system-health-audit` conserven validacion de `source_prompt` y `contract_id`.
La ruta de exclusion silenciosa no esta permitida.

Decision de catalogo para opcion B: `role` se expone como columna/campo nuevo y
separado de `owner`. Este ticket no cambia la semantica de `_derive_owner()` ni
intenta desenlazar `owner` de `author/role`; si eso hiciera falta, es
`CONTRACT_GAP`.

## Files Likely Touched

### repo_motor

- `skills/audit-git-publication/SKILL.md`
- `skills/audit-pipeline/SKILL.md`
- `skills/code-audit/SKILL.md`
- `skills/local-audit/SKILL.md`
- `skills/system-health-audit/SKILL.md`
- `scripts/discover_skills.py`
- `docs/registry/INDEX.md`
- `docs/registry/README.md`
- `tests/test_discover_skills.py`
- `tests/test_check_naming.py`
- `tests/test_registry_catalog.py`

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
- `skills/bui-self-audit/SKILL.md`
- `prompts/audit_*.md`
- `scripts/check_skill_collisions.py`
- `scripts/run_gates_dispatch.py`
- `bus/runtime/events`

## Forbidden Surfaces

- Renombrar skills o prompts.
- Tocar `skills/bui-self-audit/SKILL.md`.
- Mover `audit_*` prompts a `auditor_*`.
- Tocar bus/runtime/events manualmente.
- Tocar dependencias.
- Expandir `man-*`/`bui-*`.
- Cambiar la semantica de `owner` mas alla de anadir `role`.

## Criterios binarios

- Las cinco skills auditoras declaradas en FLT usan `role: auditor`.
- `skills/bui-self-audit/SKILL.md` sigue con `role: builder`.
- `scripts/discover_skills.py` acepta y proyecta `role: auditor`, mantiene
  `auditor` en el opt-in de `_check_contract()` y expone `role` como campo
  separado de `owner`.
- `audit-git-publication`, `audit-pipeline` y `system-health-audit` conservan
  validacion de `source_prompt` y `contract_id` despues del cambio.
- El catalogo derivado y `docs/registry/INDEX.md` exponen `role` como campo
  separado de `owner`; el orden de columnas queda estable y probado.
- `docs/registry/README.md` queda alineado si documenta ownership/roles/catalog
  fields.
- `discover_skills.py --check-naming`, `--check-contract`, `--check-index` y
  `check_skill_collisions.py` quedan verdes.
- La evidencia de discovery demuestra que las cinco skills auditoras salen
  clasificadas coherentemente, con `role` visible y `bui-self-audit` fuera.
- `tests/test_registry_catalog.py` verifica el nuevo campo `role` y conserva
  los required fields previos.
- Tests focales cubren aceptacion de `role: auditor`, exclusion de
  `bui-self-audit`, no regresion de `manager|builder` y la nueva proyeccion
  `role` del catalogo.
- `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all`
  y `validate --json` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008k.md` y parar si formalizar `auditor` exige renombrar
prompts `audit_*`, ampliar el ticket a `man-*`/`bui-*`, reescribir
`source_prompt`/`contract_id` fuera de las tres skills contract-validated, o
cambiar la semantica de `owner` mas alla de anadir `role` como campo separado.