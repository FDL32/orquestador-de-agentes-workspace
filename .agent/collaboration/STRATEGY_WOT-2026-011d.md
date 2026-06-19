# STRATEGY_WOT-2026-011d.md

## Enfoque

Ticket mixto de retirada auditada. El riesgo no esta en borrar archivos sino en
falsificar la conclusion: hoy el catalogo publicado trata
`audit_plan.md`, `destination_bootstrap.md`, `launch_builder.md`,
`refactor_bootstrap.md`, `review_manager.md`, `session_bootstrap.md` y
`session_close_chat.md` como `active`, y `MANIFEST.distribute`,
`.claude/rules/00-startup.md`, `PROJECT.md`, `CLOSURE_MODEL.md`, `AGENTS.md`
y `tests/test_migration_bootstrap.py` todavia nombran stubs legacy.
La estrategia correcta es cerrar primero la fuente real del catalogo, luego
reapuntar consumidores y solo despues decidir deletes por evidencia.

## Fase 0 - Baseline y clasificacion

1. Confirmar los 7 stubs legacy en `prompts/`.
2. Construir una matriz por stub con `rg` separando:
   - consumidores operativos vivos;
   - proyecciones generadas;
   - historia / DEC / changelog / memoria.
3. Confirmar en codigo que `INDEX.md` se genera desde `discover_skills.py` y
   que `build_catalog()` no deriva todavia `status` para `prompts/`.
4. Registrar en `execution_log.md` la baseline por stub antes de cualquier edit
   o delete.

## Fase 1 - Fuente de verdad del catalogo

1. Ajustar `scripts/discover_skills.py` para que el catalogo de `prompts/`
   pueda derivar lifecycle desde metadata real del archivo reutilizando el
   parser existente cuando sea posible.
2. Usar solo el vocabulario ya soportado por el motor:
   `active`, `deprecated`, `draft`.
3. Marcar los stubs legacy como `deprecated` en la fuente de verdad elegida.
4. Regenerar `docs/registry/INDEX.md` con
   `python scripts/discover_skills.py --generate-index`.

## Fase 2 - Repoint de consumidores vivos

1. Reapuntar consumidores operativos documentales a los nombres canonicos:
   `.claude/rules/00-startup.md`, `PROJECT.md`, `CLOSURE_MODEL.md` y cualquier
   otra superficie viva que la baseline detecte.
2. Decidir el papel final de `MANIFEST.distribute`:
   - si el stub sigue siendo compat necesario, se conserva como compat explicita;
   - si ya no es necesario, se retira del manifiesto.
3. Actualizar tests de barrera afectados, especialmente catalogo/index y la
   migracion 008h/010a si el contrato de stubs cambia.

## Fase 3 - Retirada condicional por stub

1. Reejecutar `rg` por cada stub despues del repoint y de regenerar `INDEX.md`.
2. Borrar solo los stubs con `0` consumidores no-historicos verificados.
3. Mantener en disco, ya `deprecated`, cualquier stub que siga justificadamente
   requerido por compatibilidad viva.
4. Registrar por stub la decision final: `deleted` o `deprecated-kept`, con
   evidencia literal.

## Barreras

Deben existir barreras que prueben:

- el catalogo/index ya no publica los stubs como `active`;
- las rutas operativas usan nombres canonicos;
- cualquier delete estuvo precedido por `rg` con `0` consumidores vivos;
- las referencias historicas no se reescriben;
- `--check-index`, tests focales, `ruff`, `pytest-safe` y `validate` quedan
  verdes.

## Riesgos a vigilar

- Intentar "resolver" el ticket editando `INDEX.md` a mano.
- Suponer que `status` de prompts ya existe y hacer un frontmatter que el motor
  ignora.
- Borrar stubs por intuicion aunque `MANIFEST` o tests aun los consuman.
- Convertir historia o DEC en scope productivo cuando solo son trazabilidad.
