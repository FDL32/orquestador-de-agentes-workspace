# PLAN WOT-2026-005a - memory_upload: decision de destino de memoria

## Pasos
1. `prompts/memory_upload.md`: insertar tras "### Wings de memoria" (antes de "## Formato
   de la propuesta") una seccion `## Decisión de destino de memoria (obligatoria antes de
   escribir)`:
   - tabla de los tres destinos (Claude privada / portable motor / portable destino) con
     portabilidad/validabilidad y cuando usar cada uno;
   - reglas: declarar destino antes de escribir; evidencia requerida por destino; promocion
     a `observations.jsonl` solo con schema + consumidor real, si no `NO PROMOVIBLE` con
     motivo; decision explicita de promover-o-no lo guardado en privada.
   - subseccion `### Drift de schema en observations.jsonl`: si hay drift, prohibido añadir
     entradas portables nuevas sin ticket de migracion.
2. Verificar encoding UTF-8 limpio.

## Evidencia esperada
- Diff del prompt; encoding guard exit 0; validate destino 0; motor solo este archivo.

## STOP
- No tocar schema ni codigo. Si hace falta, follow-up code.
