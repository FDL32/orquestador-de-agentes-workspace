# AUDIT_WOT-2026-008i.md

## Checklist de aceptacion

- [ ] Existen los cuatro directorios canonicos `manager-*`.
- [ ] `manager_review.md` bindea a `skills/manager-review-implementation/SKILL.md`.
- [ ] `contract_id: cid-man-review-v2` sigue presente y `--check-contract` pasa.
- [ ] Los consumidores vivos declarados en FLT usan `manager-*`.
- [ ] El `rg` de `man-*` ya no deja consumidores operativos fuera de zonas
      historicas/compat justificadas.
- [ ] `discover_skills.py --check-naming` pasa.
- [ ] `discover_skills.py --check-contract` pasa.
- [ ] `check_skill_collisions.py` pasa.
- [ ] `discover_skills.py --check-index` pasa tras regenerar `INDEX.md`.
- [ ] La paridad de discovery conserva los mismos triggers funcionales.
- [ ] Existe un test que falla si reaparece una referencia prose viva a `man-*`.
- [ ] `validate --json --project-root <repo_destino>` termina en 0/0.

## Anti-patrones a rechazar

- Arreglar solo `--check-naming` y dejar prose/path viva legacy.
- Introducir alias runtime de skill no soportados por el contrato.
- Tocar `bui-*` o `audit_*` fuera del lote declarado.
- Cambiar `triggers` o `contract_id` para "facilitar" el rename.
- Presentar historial/DEC como si fueran consumidores vivos.