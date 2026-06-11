# AUDIT WT-2026-225a

## Veredicto esperado
No aprobar si el fix solo lee `TURN.md` o `STATE.md` sin contrastar el bus.

## Hallazgos bloqueantes a vigilar

### CRITICO - La decision de launch sigue dependiendo de una proyeccion stale
- Bloquea si el launcher puede seguir arrancando Builder o Manager sin derivar
  primero el estado canonico del bus.

### ALTO - No hay prueba de drift reproducible
- Bloquea si no existe un test que reproduzca `bus=READY_FOR_REVIEW` con
  `STATE.md=IN_PROGRESS`.

### ALTO - Catch-up sin evidencia estructurada
- Bloquea si la reconciliacion ocurre pero no deja rastro verificable.

### MEDIO - Scope creep hacia rounds o locks
- Marcar cambios innecesarios en `builder_lock`, `_builder_alive()` o
  `stale_builder_round`.

## TP Check
TP-01: seam real confirmado en launcher/bus read.
TP-02: drift detectado cuando `last_processed_sequence < max(bus seq)` antes
del launch.
TP-03: `STATE.md` y `TURN.md` se reproyectan desde el ultimo estado derivado
del bus.
TP-04: evidencia verificable del catch-up en archivos proyectados y salida
estructurada o evento asociado.
TP-05: test que reproduce `READY_FOR_REVIEW` en bus vs `IN_PROGRESS` en
`STATE.md` y falla sin el fix.
TP-06: sin scope creep hacia rounds, locks o nomenclatura.
