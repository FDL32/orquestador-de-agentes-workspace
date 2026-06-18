# STRATEGY_WOT-2026-008g.md

## Enfoque

Ticket documental DEC-only. El Builder no debe renombrar archivos ni tocar frontmatter. El valor es congelar vocabulario antes de los lotes de migracion.

## Pasos

1. Verificar premisas: 008f COMPLETED, 21 prompts fisicos, supervisor como runtime, audit_* como familia transversal.
2. Revisar la DEC preparada en repo_motor y ajustar solo si el inventario vivo la contradice.
3. Confirmar AGENTS.md con la seccion "Backends y roles".
4. Ejecutar gates documentales:
   - `python scripts/discover_skills.py --check-naming`
   - `python scripts/check_encoding_guard.py docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md AGENTS.md`
   - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
5. Registrar evidencia final en execution_log.md y hacer handoff canonico.

## Riesgos

- Convertir audit_* en auditor_* falsea propiedad multi-rol.
- Tocar renames en 008g rompe el alcance DEC-only.
- Redefinir supervisor rompe runtime/bus; solo documentarlo.