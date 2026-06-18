# AUDIT_WOT-2026-008k.md

## Checklist de aceptacion

- [ ] Las cinco skills auditoras de FLT tienen ole: auditor.
- [ ] skills/bui-self-audit/SKILL.md sigue en ole: builder.
- [ ] No hay renames de prompts ni skills.
- [ ] discover_skills.py --check-naming pasa.
- [ ] discover_skills.py --check-contract pasa.
- [ ] check_skill_collisions.py pasa.
- [ ] discover_skills.py --check-index pasa tras regenerar INDEX.md.
- [ ] La salida JSON/catalogo evidencia el ownership coherente de las skills auditoras.
- [ ] Tests focales cubren ole: auditor, exclusion de ui-self-audit y no regresion de manager/builder.
- [ ] alidate --json --project-root <repo_destino> termina en 0/0.

## Anti-patrones a rechazar

- Tratar prompts udit_* como si el ticket obligara a renombrarlos.
- Reclasificar ui-self-audit a uditor por el nombre.
- Romper --check-contract y justificarlo como "scope futuro".
- Cambiar mas ownership del catalogo del que exige el contrato.
- Introducir gates paralelos cuando discovery ya ofrece la autoridad suficiente.
