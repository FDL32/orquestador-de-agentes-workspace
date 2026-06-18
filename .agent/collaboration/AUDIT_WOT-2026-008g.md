# AUDIT_WOT-2026-008g.md

## Checklist Manager

- Confirmar que WOT-2026-008f esta COMPLETED antes de arrancar 008g.
- Confirmar que el diff del repo_motor contiene solo `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md` y `AGENTS.md`.
- Confirmar que no hay renames/moves de prompts o skills.
- Confirmar que no hay cambios de frontmatter.
- Confirmar que la DEC contiene los 7 bloques exigidos por el work_plan.
- Confirmar que `audit_*` queda como familia transversal y que `auditor_*` no se fuerza para prompts multi-rol.
- Confirmar que AGENTS.md distingue backend IA, rol, artefacto y supervisor runtime.
- Confirmar `discover_skills.py --check-naming`, encoding guard y validate 0/0.

## Anti-patrones a rechazar

- Renombrar `launch_builder.md` u otros prompts en este ticket.
- Expandir `man-`/`bui-` dentro de 008g.
- Cambiar `discover_skills.py`, `_PIPELINE_ACTIONS`, bus o pre_handoff_guard.
- Decir que DEC-008D-001 ya tenia una regla textual family-wins.
- Convertir supervisor en rol de prompt.

## Criterio de aprobacion

Aprobar si la DEC y AGENTS.md dejan el vocabulario canonico listo para los tickets 008h-008k, con gates documentales verdes y sin cambios productivos fuera del alcance.