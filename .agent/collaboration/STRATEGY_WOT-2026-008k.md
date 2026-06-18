# STRATEGY_WOT-2026-008k.md

## Enfoque

Ticket de blast radius medio: toca frontmatter de cinco skills auditoras y el
discovery/catalogo derivado para que `role: auditor` sea canonico y visible
como campo separado de `owner`, sin romper `manager|builder`, sin contaminar
`bui-self-audit` y sin perder validacion de contrato en las tres skills que hoy
ya la tienen.

## Fase 0 - Baseline y seams

1. Confirmar `DEC-008G-001` y releer su fila de roadmap para `008k`.
2. Ejecutar `git status --short` en `repo_motor` y documentar el estado real:
   hoy existe WIP parcial en `scripts/discover_skills.py`, cinco `SKILL.md` y
   `docs/registry/INDEX.md`.
3. Capturar baseline de:
   - `python scripts/discover_skills.py --check-naming`
   - `python scripts/discover_skills.py --check-contract`
   - `python scripts/check_skill_collisions.py`
   - `python scripts/discover_skills.py --json`
4. Verificar `role:` actual en:
   - `audit-git-publication`
   - `audit-pipeline`
   - `system-health-audit`
   - `code-audit`
   - `local-audit`
   - `bui-self-audit`
5. Confirmar en `scripts/discover_skills.py`:
   - como deriva `owner`;
   - que `auditor` ya aparece en `CONTRACT_OPT_IN_ROLES`;
   - donde anadir `role` al catalogo/INDEX sin reescribir la semantica de
     `owner`.

## Fase 1 - Implementacion minima

1. Continuar sobre el WIP real si es coherente con el contrato; no revertir ni
   duplicar cambios sin documentarlo.
2. Actualizar/confirmar `role: auditor` solo en estas skills:
   - `audit-git-publication`
   - `audit-pipeline`
   - `system-health-audit`
   - `code-audit`
   - `local-audit`
3. Mantener `bui-self-audit` intacta en `builder`.
4. Ajustar `scripts/discover_skills.py` para:
   - aceptar y proyectar `auditor` coherentemente;
   - mantener `auditor` dentro del opt-in de `_check_contract()`;
   - anadir `role` como campo separado del catalogo derivado;
   - renderizar `INDEX.md` con columna `role` estable, sin cambiar la
     semantica de `owner`;
   - no reinterpretar prompts `audit_*` como propiedad del rol auditor.
5. Actualizar `tests/test_registry_catalog.py` para exigir el nuevo campo
   `role`.
6. Regenerar `docs/registry/INDEX.md` y alinear `docs/registry/README.md` si
   documenta ownership/roles/catalog fields.

## Fase 2 - Barreras

Tests focales deben probar:
- aceptacion de `role: auditor`;
- inclusion de `auditor` en `_check_contract()` para las tres skills que hoy
  son `manager`;
- exclusion explicita de `bui-self-audit`;
- no regresion de `manager|builder`;
- required fields del catalogo con `role` nuevo y `owner` preservado;
- proyeccion correcta en catalogo/index si el ticket toca discovery.

## Riesgos a vigilar

- Convertir este ticket en rename de familia `audit_*` -> fuera de scope.
- Romper `_check_contract()` al ampliar semantica de `role`.
- Cambiar `owner` de forma mas amplia de la necesaria o intentar desenlazarlo
  de `author/role`.
- Meter `bui-self-audit` por el nombre en vez de por propiedad real.