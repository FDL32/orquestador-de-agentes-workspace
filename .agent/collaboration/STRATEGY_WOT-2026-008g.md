# STRATEGY_WOT-2026-008g.md

## Enfoque

1. Reconfirmar inventario: 20 prompts fisicos, 29 skills y estado de WOT-2026-008f.
2. Escribir una DEC unica en repo_motor: `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`.
3. Actualizar solo la cabecera de AGENTS.md para separar backend IA, rol, artefacto y supervisor runtime.
4. No tocar prompts, skills, frontmatter, discovery ni bus.
5. Verificar que la DEC usa lenguaje preciso: formaliza mecanismo implicito en `_PIPELINE_ACTIONS`, no extiende una regla escrita inexistente.
6. Registrar en execution_log.md los comandos y gates.

## Gates esperados

- `python scripts/discover_skills.py --check-naming`
- `python scripts/check_encoding_guard.py docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md AGENTS.md`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Riesgos

- Convertir un ticket documental en rename real: bloquear.
- Forzar audit_* a auditor_* y mentir sobre consumidores multi-rol: bloquear.
- Redefinir supervisor en vez de documentar el actor runtime existente: bloquear.
- Tocar frontmatter o discovery sin contrato de implementacion: bloquear.