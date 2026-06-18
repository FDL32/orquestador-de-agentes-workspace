# work_plan.md -- WOT-2026-008d

## Metadata

- **ID:** WOT-2026-008d
- **Contract ID:** T-008D-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **repo_motor:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes
- **repo_destino:** C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace

## Objetivo

Crear `docs/decisions/DEC-008D-001-naming-convention.md`, implementar `python scripts/discover_skills.py --check-naming`, conectarlo en `scripts/run_gates_dispatch.py`, demostrar paridad pre/post con `--check-contract`, `check_skill_collisions.py` y `discover_skills.py --json`, y cerrar con `validate --json` en 0 errors.

## Premisas verificadas antes de Builder

- `WOT-2026-008c` esta completado y formaliza `docs/registry/INDEX.md` como proyeccion generada, sin `registry.json`.
- `T-008D-001` existe y esta frozen.
- `discover_skills.py --check-naming` no existe aun: es entregable de este ticket.
- Naming lexico es ortogonal a la taxonomia `disable-model-invocation` de `010s`; la DEC debe confirmarlo.
- `pre_handoff_guard` no debe implementar logica de naming; solo valida handoff, gates frescos y barrera 010u.

## Decision Arquitectonica

La primera entrega del Builder debe ser `docs/decisions/DEC-008D-001-naming-convention.md`. La DEC decide la convencion antes de cualquier rename: patrones por tipo, prefijos de rol, contrato de shim/frontmatter, fuente de `canonical_name`/`legacy_aliases`/`naming_status`, y si `check_skill_collisions.py` permanece read-only o se modifica con justificacion explicita. Si no hay DEC, no hay rename.

## Non-goals

- No crear `registry.json` ni manifest central.
- No renombrar mas de un piloto prompt+skill en este ticket.
- No mover carpetas completas de `prompts/` o `skills/`.
- No retirar shims ni compat legacy; eso queda para `008e`.
- No tocar bus runtime/events manualmente.
- No tocar dependencias, `pyproject.toml` ni `uv.lock`.
- No poner logica de naming en `pre_handoff_guard`.

## Files Likely Touched

### repo_motor

- `docs/decisions/DEC-008D-001-naming-convention.md`
- `docs/registry/README.md`
- `docs/registry/INDEX.md`
- `scripts/discover_skills.py`
- `scripts/run_gates_dispatch.py`
- `tests/test_discover_skills.py`
- `tests/unit/test_run_gates_dispatch.py`
- `tests/test_check_naming.py`
- `tests/test_discover_skills.py`
- `tests/unit/test_run_gates_dispatch.py`



Nota: la DEC declarara las rutas concretas de prompts piloto, stubs legacy y skills piloto antes de tocarlas; no son FLT editable hasta que la DEC las nombre explicitamente.

### repo_destino

- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/check_skill_collisions.py` (no editar salvo que la DEC descarte explicitamente `discover_skills.py --check-naming` como autoridad)
- `scripts/check_ticket_nomenclature.py`
- `scripts/validate_ticket_prose.py`
- `skills/`
- `prompts/`
- `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`
- `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
- `skills/man-review-implementation/SKILL.md` y prompt relacionado son solo candidatos; si la DEC elige ese piloto, el Builder debe registrar CEM y mantener el cambio dentro de FLT antes de tocarlo

## Manager-only

- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/AUDIT_WOT-2026-008d.md`
- `.agent/collaboration/STRATEGY_WOT-2026-008d.md`
- `.agent/planning/ticket_contracts.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

## Forbidden Surfaces

- `registry.json` o manifest central.
- Migracion masiva.
- Borrado de prompts/skills o carpetas completas.
- Retirada de shims sin scan reproducible.
- Romper `source_prompt` o `contract_id`.
- Logica de naming en `pre_handoff_guard`.
- Bus runtime/events editado manualmente.
- `privada/`, `.env`, dependencias.

## Fase 0 obligatoria

1. Confirmar `T-008D-001` frozen y `008c` completed.
2. Capturar baseline antes de cualquier rename:
   - `python scripts/discover_skills.py --check-contract`
   - `python scripts/check_skill_collisions.py`
   - `python scripts/discover_skills.py --json`
3. Localizar consumidores vivos de `source_prompt` y referencias prose del piloto candidato.
4. Confirmar si `audit_plan.md` sigue siendo stub-alias vivo y documentar el patron de shim.
5. Registrar en `execution_log.md` seams, baseline y cualquier desviacion CEM antes de tocar codigo.

## Criterios binarios

- Existe DEC congelada como primer entregable y antes de cualquier rename.
- La DEC fija prompts `snake_case`, skills `kebab-case`, scripts CLI verbo primero, shims/stubs versionados, prefijos de rol y ortogonalidad con `disable-model-invocation`.
- Si hay piloto de rename, el prompt, su frontmatter `source_prompt` y cada referencia prose viva en prompts/skills operativos se actualizan atomicamente.
- Existe shim/stub legacy para cada nombre publico antiguo tocado, con retirada asignada a `008e`; la DEC define si es alias documental o prompt ejecutable y como conserva `source_prompt`/`contract_id` sin romper `--check-contract`.
- `python scripts/discover_skills.py --check-contract` queda verde.
- `python scripts/check_skill_collisions.py` queda verde.
- Baseline pre/post de `--check-contract`, `check_skill_collisions.py` y `discover_skills.py --json` demuestra paridad salvo renames/aliases declarados en la DEC.
- `docs/registry/INDEX.md` expone `canonical_name`, `legacy_aliases` y `naming_status` o campos equivalentes; fuente: frontmatter (`legacy_aliases:`) o derivacion por filename en `discover_skills.py`, sin sidecar JSON ni manifest central.
- `rg` de nombres antiguos solo aparece en shims, docs historicas/deprecacion, changelog/backlog o tests de compatibilidad.
- Existe `discover_skills.py --check-naming` antes del cierre, con test fail-closed para un nombre fuera de convencion; si se crea script separado o se extiende `check_skill_collisions.py`, la DEC lo justifica.
- `scripts/run_gates_dispatch.py` invoca `discover_skills.py --check-naming` o equivalente decidido por la DEC en los perfiles aplicables.
- Tests focales, ruff/format si toca Python, encoding guard, handoff verde incluida barrera 010u, suite canonica y `validate --json --project-root <repo_destino>` terminan en verde.

## CONTRACT_GAP behavior

Emitir `CG-WOT-2026-008d.md` y bloquear si la convencion requiere redisenar discovery, crear manifest central, tocar bus/runtime, no puede mantener `--check-contract` verde con shims, o exige meter naming dentro de `pre_handoff_guard`.

## STOP conditions

Parar si no hay DEC; si el rename elegido no tiene shim seguro; si quedan referencias legacy vivas fuera de superficies permitidas; si `discover_skills.py` queda read-only mientras se exige modificarlo; si no se revalida 010s; si la DEC no fija prefijos de rol; si el piloto exige scope masivo.