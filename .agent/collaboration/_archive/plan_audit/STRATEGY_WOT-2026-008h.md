# STRATEGY_WOT-2026-008h.md

## Enfoque

Ejecutar un rename versionado tipo 008e, pero para cinco prompts del orchestrator. El riesgo principal no es sintactico: los nombres viejos siguen siendo lexicalmente validos, asi que la prueba de migracion debe apoyarse en stubs, `source_prompt`, consumidores vivos y registry.

## Pasos

1. Capturar baseline de consumers y gates: `--check-naming`, `--json`, `--check-index`, `rg` de nombres viejos/nuevos.
2. Crear los cinco prompts canonicos nuevos `orchestrator_*`.
3. Convertir los cinco nombres viejos en stubs de compatibilidad.
4. Actualizar `source_prompt` y prose viva declarada en FLT.
5. Regenerar/alinear `INDEX.md`, `MANIFEST.distribute`, `llms*.txt` y docs de onboarding.
6. Ejecutar tests focales + suite segura y cerrar con handoff canonico.

## Riesgos

- `launch_builder.md` no sirve como prueba de migracion por naming gate, porque ya era una excepcion lexical valida.
- `session_bootstrap.md` tiene tests dedicados y no puede quedar como stub vacio si esos tests leen contenido operativo.
- Mezclar este rename con migraciones `man-*`/`bui-*` expandiria el alcance de forma peligrosa.