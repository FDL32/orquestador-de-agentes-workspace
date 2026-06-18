# AUDIT_WOT-2026-008h.md

## Checklist Manager

- [ ] Los cinco prompts canonicos `orchestrator_*` existen.
- [ ] Los cinco nombres viejos siguen presentes como stubs/aliases.
- [ ] `prompts/orchestrator_pipeline.md` no se renombra.
- [ ] `skills/bui-implement-from-plan/SKILL.md` actualiza `source_prompt`.
- [ ] Los consumidores vivos declarados en FLT apuntan al canonico o documentan stub.
- [ ] `INDEX.md`, `MANIFEST.distribute`, `README.md`, `QUICKSTART.md`, `AGENTS.md`, `CLAUDE.md`, `llms*.txt` quedaron alineados.
- [ ] La prueba de migracion usa algo mas que `--check-naming`: `rg`, stubs presentes y `source_prompt`.
- [ ] Tests focales, suite segura, encoding guard y validate 0/0 pasan.

## Anti-patrones

- Declarar exito solo porque `--check-naming` sigue verde.
- Renombrar `orchestrator_pipeline.md` por arrastre.
- Borrar prompts viejos en vez de stubearlos.
- Dejar prose viva en skills/prompts apuntando al nombre antiguo.