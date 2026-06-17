# STRATEGY_WOT-2026-010n -- Gate de deliverables namespaced

## Hechos verificados

- El bug aparece cuando un deliverable Builder valido vive en `repo_motor`.
- `scope_gate.py` ya conoce FLT namespaced; el gate de deliverables debe
  converger con esa semantica, no inventar otra.
- El caso de `010j` es una reproduccion viva, no una hipotesis.

## Plan tecnico

1. Reproducir el caso real de `010j` con una barrera roja.
2. Inspeccionar como el gate resuelve paths Builder hoy.
3. Introducir resolucion determinista por namespace y/o `delivery_authority`.
4. Verificar que `repo_destino` no regresa.
5. Reintentar el cierre de `010j` solo despues del fix.

## Riesgos a vigilar

- **Pass-open accidental:** arreglar el bug aceptando cualquier path seria peor
  que el bloqueo actual.
- **Drift entre consumidores:** si `scope_gate` y `check_deliverables_exist`
  divergen, reapareceran falsos bloqueos.
- **Sobreparseo:** notas libres o secciones informativas no deben convertirse en
  deliverables obligatorios.

## No hacer

- No copiar el deliverable de `010j` a `repo_destino`.
- No tocar el runner de pytest ni el flujo de performance.
- No cerrar `010j` por narrativa sin pasar por el gate corregido.
