# execution_log.md -- WOT-2026-008h

**Estado:** IN_PROGRESS

## Manager Preflight

- WOT-2026-008g cerrado canonicamente antes de abrir 008h.
- T-008H-001 materializado como contrato frozen.
- Objetivo: rename versionado de cinco prompts de orchestrator con stubs, sin tocar `orchestrator_pipeline.md` ni migrar skills `man-*`/`bui-*`.
- Riesgo clave declarado: los nombres viejos siguen siendo lexicalmente validos; la prueba de migracion debe apoyarse en consumers/stubs/source_prompt, no solo en `--check-naming`.
- Pendiente de Builder: baseline, rename, actualizacion de consumidores, gates y handoff canonico.