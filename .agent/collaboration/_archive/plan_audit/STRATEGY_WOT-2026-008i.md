# STRATEGY_WOT-2026-008i.md

## Enfoque

Ticket de blast radius medio-alto: renombra cuatro skills manager desde el
prefijo corto `man-*` al canonico largo `manager-*`, preservando dispatch por
triggers y bindings prompt<->skill. El riesgo real no esta en el rename fisico,
si no en los consumidores prose/path vivos que aun apuntan al nombre legacy.

## Fase 0 - Baseline y seams

1. Releer `DEC-008G-001` y fijar que `008i` es lote de manager skills.
2. Capturar baseline de:
   - `python scripts/discover_skills.py --check-naming`
   - `python scripts/discover_skills.py --check-contract`
   - `python scripts/check_skill_collisions.py`
   - `python scripts/discover_skills.py --check-index`
   - `python scripts/discover_skills.py --json`
3. Inventariar referencias vivas a:
   - `man-create-work-plan`
   - `man-resolve-escalation`
   - `man-review-implementation`
   - `man-session-closeout`
4. Confirmar seams criticos:
   - `prompts/manager_review.md` -> anchor + `contract_id`
   - `prompts/orchestrator_pipeline.md` y `skills/orchestrate-pipeline/SKILL.md`
   - `skills/project-finalize/SKILL.md`
   - `docs/registry/INDEX.md`
5. Registrar en `execution_log.md` el baseline pre/post esperado y cualquier
   consumidor que parezca runtime real en vez de prose/documentacion.

## Fase 1 - Implementacion minima

1. Renombrar los cuatro directorios `man-*` a `manager-*`.
2. Actualizar dentro de cada skill:
   - heading/body si menciona el nombre legacy;
   - referencias cruzadas entre manager skills.
3. Actualizar `prompts/manager_review.md` para que el binding canonico apunte a
   `skills/manager-review-implementation/SKILL.md`, preservando
   `contract_id: cid-man-review-v2`.
4. Actualizar consumidores vivos declarados en FLT a `manager-*`.
5. Regenerar `docs/registry/INDEX.md` y alinear `skills/README.md`.
6. No tocar `triggers`, `contract_id` ni `bui-*`.

## Fase 2 - Barreras

Los tests deben cubrir al menos:
- binding `manager_review.md` -> `manager-review-implementation` sin romper
  `--check-contract`;
- ausencia de referencias prose vivas a `man-*` en consumidores operativos del
  lote;
- paridad funcional de triggers antes/despues del rename;
- referencias de README/registry alineadas con los nombres canonicos.

## Riesgos a vigilar

- Descubrir demasiado tarde un consumidor runtime real del path legacy.
- Probar solo `--check-naming` y venderlo como migracion completa.
- Romper `manager_review.md`/`contract_id` al cambiar el path canonico.
- Derivar a `bui-*` o a un sistema nuevo de aliases de skill.