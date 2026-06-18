# work_plan.md -- WOT-2026-008k

## Metadata

- **ID:** WOT-2026-008k
- **Contract ID:** T-008K-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Formalizar `role: auditor` en las skills que son propiedad real del rol auditor, sin renombrar directorios ni prompts. Cumplimiento medible: las cinco skills auditoras declaradas quedan con `role: auditor`, discovery/index siguen verdes, `bui-self-audit` permanece en `builder`, las tres skills que hoy son `manager` conservan validación de `source_prompt` y `contract_id`, y `validate --json --project-root <repo_destino>` cierra en 0 errors / 0 warnings.

## Non-goals

- No renombrar prompts `audit_*` ni skills.
- No tocar `skills/bui-self-audit/SKILL.md`.
- No migrar `man-*` o `bui-*`.
- No tocar bus, runtime o eventos.
- No cambiar dependencias ni launcher.

## Premisas verificadas antes de Builder

- `WOT-2026-008g` y `WOT-2026-008h` estan COMPLETED.
- `DEC-008G-001` congelo que `audit_*` en prompts es familia transversal y que `008k` formaliza solo el rol de ciertas skills auditoras.
- `WOT-2026-008i` y `WOT-2026-008j` quedan diferidos segun `DEC-008G-001`; este ticket es independiente de la expansion `man-*`/`bui-*`.
- Las cinco skills candidatas se dividen hoy en dos grupos relevantes: tres con `role: manager` y contrato vivo (`audit-git-publication`, `audit-pipeline`, `system-health-audit`) y dos con `role: shared` sin `source_prompt` (`code-audit`, `local-audit`).
- `skills/bui-self-audit/SKILL.md` usa `role: builder` y queda fuera por propiedad real del artefacto.
- `scripts/discover_skills.py` hoy endurece `_check_contract()` solo para `manager|builder`; el ticket debe decidirlo explicitamente y preservar enforcement para las tres skills que hoy ya estan contract-validated.

## Decision Arquitectonica

La taxonomia se apoya en propiedad real del artefacto, no en el prefijo del nombre. Por eso los prompts `audit_*` siguen como familia transversal, mientras que estas cinco skills pasan a `role: auditor`. `bui-self-audit` no migra: es una skill del builder para auto-auditar su propio trabajo, no una skill del rol auditor.

Decision de contrato para evitar falso verde: `auditor` entra en el opt-in de `_check_contract()` para que `audit-git-publication`, `audit-pipeline` y `system-health-audit` conserven validación de `source_prompt` y `contract_id`. La ruta de exclusión silenciosa no está permitida.

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

## Criterios binarios

- Las cinco skills auditoras declaradas en FLT usan `role: auditor`.
- `skills/bui-self-audit/SKILL.md` sigue con `role: builder`.
- `scripts/discover_skills.py` acepta y proyecta `role: auditor` y añade `auditor` al opt-in de `_check_contract()` sin romper el contrato actual de `manager|builder`.
- `audit-git-publication`, `audit-pipeline` y `system-health-audit` conservan validación de `source_prompt` y `contract_id` después del cambio.
- `docs/registry/INDEX.md` refleja el ownership actualizado de las skills auditoras.
- `docs/registry/README.md` queda alineado si documenta ownership/roles.
- `discover_skills.py --check-naming`, `--check-contract`, `--check-index` y `check_skill_collisions.py` quedan verdes.
- La evidencia de discovery demuestra que las cinco skills auditoras salen clasificadas coherentemente y que `bui-self-audit` sigue fuera.
- Tests focales cubren aceptación de `role: auditor`, exclusión de `bui-self-audit` y no regresión de `manager|builder`.
- `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all` y `validate --json` quedan verdes.

## CONTRACT_GAP

Emitir `CG-WOT-2026-008k.md` y parar si formalizar `auditor` exige renombrar prompts `audit_*`, ampliar el ticket a `man-*`/`bui-*`, reescribir `source_prompt`/`contract_id` fuera de las tres skills contract-validated, o cambia el meaning de `owner` más allá de las cinco skills auditoras.