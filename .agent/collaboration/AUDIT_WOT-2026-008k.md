# AUDIT_WOT-2026-008k.md

## Checklist de aceptacion

- [ ] Las cinco skills auditoras de FLT tienen `role: auditor`.
- [ ] `skills/bui-self-audit/SKILL.md` sigue en `role: builder`.
- [ ] No hay renames de prompts ni skills.
- [ ] `discover_skills.py --check-naming` pasa.
- [ ] `discover_skills.py --check-contract` pasa.
- [ ] `check_skill_collisions.py` pasa como gate externo, sin tocar su test si no hace falta.
- [ ] `discover_skills.py --check-index` pasa tras regenerar `INDEX.md`.
- [ ] La salida JSON/catalogo evidencia el ownership coherente de las skills auditoras.
- [ ] Las tres skills que hoy son `manager` conservan validación de `source_prompt` y `contract_id` tras migrar a `auditor`.
- [ ] Tests focales cubren `role: auditor`, inclusión en opt-in, exclusión de `bui-self-audit` y no regresión de `manager|builder`.
- [ ] `validate --json --project-root <repo_destino>` termina en 0/0.

## Anti-patrones a rechazar

- Tratar prompts `audit_*` como si el ticket obligara a renombrarlos.
- Reclasificar `bui-self-audit` a `auditor` por el nombre.
- Dejar `auditor` fuera de `_check_contract()` y venderlo como green porque `--check-contract` sigue pasando.
- Cambiar más ownership del catalogo del que exige el contrato.
- Introducir gates paralelos cuando discovery ya ofrece la autoridad suficiente.