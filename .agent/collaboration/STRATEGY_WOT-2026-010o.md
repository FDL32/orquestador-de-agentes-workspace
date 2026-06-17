# STRATEGY_WOT-2026-010o -- Determinismo del evidence-gate en tests

## Hechos verificados

- La flakiness observada en `010k` no nacio en el diff productivo del ticket,
  sino en el entorno de ejecucion del `repo_destino` real.
- El valor del ticket no es "hacer pasar tests" a base de mocks, sino
  conservar la logica real del evidence-gate con una fuente de estado git
  controlada.

## Plan tecnico

1. Confirmar el seam exacto entre los tests de review bridge y la resolucion
   del `repo_destino` vivo.
2. Identificar la superficie minima donde puede inyectarse un repo temporal o
   una fixture controlada sin cambiar la politica del evidence-gate.
3. Preparar un repo git temporal reproducible con dos escenarios:
   `APPROVE` (cambios solo collaboration-only) y `CHANGES` (cambios
   productivos).
4. Reescribir los tests afectados para usar esa fuente controlada y demostrar
   que dejan de depender del estado git del destino vivo.
5. Correr focales y suite canonica para verificar que el desacoplamiento no
   degrada cobertura ni introduce mock drift.

## Riesgos

- **Mock drift:** parchear un seam equivocado y dejar de ejercer el codigo real
  de produccion.
- **Sobre-anchura:** tener que tocar API publica del evidence-gate en vez de la
  capa de fixture/test.
- **Fixture irreal:** crear un repo temporal demasiado sintetico que no emita la
  misma senal que el evidence-gate usa en produccion.

## No hacer

- No tocar `motor_destination_link.json` en produccion.
- No cambiar la politica funcional de `APPROVE` vs `CHANGES`.
- No mezclar con optimizacion de suite, selector focal o CI.
