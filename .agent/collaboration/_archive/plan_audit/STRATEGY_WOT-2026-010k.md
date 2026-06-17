# STRATEGY_WOT-2026-010k -- Hotspots reales de suite

## Hechos verificados

- `010j` ya midio la suite completa; no hace falta reabrir la discusión de
  hipótesis generales.
- El ticket debe elegir uno o muy pocos hotspots reales, no “mejorar la suite”
  en abstracto.

## Plan tecnico

1. Releer el reporte de `010j` y escoger el hotspot con mejor relación
   señal/riesgo.
2. Confirmar si el tiempo viene de scan, setup repetido o fixture cara.
3. Diseñar un cambio local que preserve el contrato observable del test.
4. Añadir barrera roja->verde y smoke test cuando el shortcut sustituya un
   setup real.
5. Medir before/after en condiciones comparables y documentarlo.

## Riesgos

- **Falso verde:** acortar un test eliminando justo el comportamiento que debía
  validar.
- **Re-scope espurio:** terminar cambiando política de runner en vez de un test
  o fixture local.
- **Optimización ornamental:** ahorrar poco o nada sin mover el hotspot real.

## No hacer

- No perseguir `git/subprocess` por inercia.
- No tocar CI, cache, xdist o selector focal.
- No aceptar mejoras sin medición comparable.
