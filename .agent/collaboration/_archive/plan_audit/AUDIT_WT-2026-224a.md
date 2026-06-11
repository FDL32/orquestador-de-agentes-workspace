# AUDIT WT-2026-224a - Supervisor relaunch overlap guard

## Alias
No-overlap Builder relaunch / active Builder relaunch suppression.

## Objetivo del audit
Verificar que el supervisor ya no abre un Builder nuevo cuando el round activo
sigue protegido por el mecanismo canonico de `_builder_alive()`.

## Reglas de revision
- Revisar el archivo real y el test real antes de emitir hallazgos criticos.
- Confirmar que la barrera vive en `_relaunch_builder()` o helper inmediato.
- Confirmar que `_builder_alive()` suprime relaunch.
- Confirmar que el camino con `_builder_alive() == False` sigue relanzando.
- Confirmar que el bloqueo deja razon accionable y observable.

## Hallazgos bloqueantes tipicos
### CRITICO - Relaunch sigue ocurriendo cuando `_builder_alive()` devuelve True
Si el supervisor sigue spawneando en ese caso, el ticket no cumple su objetivo.

### CRITICO - El check ignora el criterio canonico de `_builder_alive()`
Si solo mira mtime del lock sin consultar `BUILDER_EXIT` posterior al
`lock_started_at`, la barrera puede producir falsos Builder vivos.

### ALTO - La barrera vive fuera del camino real de relaunch
Si se implementa en un wrapper o en docs, no resuelve el overlap operativo.

### MEDIO - Mensaje de supresion no accionable
Si el bloqueo no explica ticket/round y razon de `_builder_alive()`, el
diagnostico posterior empeora.

### MEDIO - Scope creep hacia heartbeats o parser central
Cambios de `WT-2026-221c` o `WT-2026-223a` deben rechazarse.

## Evidencia minima esperada
- Test de supresion con `_builder_alive() == True`.
- Test de camino valido con `_builder_alive() == False`.
- Salida de tests focales.
- Salida de `ruff`.
- Validacion del `repo_destino` sin errores ni warnings.

## TP Check
TP-01: seam real confirmado en `_relaunch_builder()`.
TP-02: `_builder_alive()` devuelve `True` y suprime relaunch.
TP-03: `_builder_alive()` devuelve `False` y permite relaunch.
TP-04: el bloqueo deja razon estructurada observable.
TP-05: existe reproduccion automatizada del overlap.
TP-06: no hay scope creep hacia `WT-2026-221c` o `WT-2026-223a`.

## Criterio de rechazo inmediato
- No hay test que suprima relaunch con Builder vivo.
- El check no usa `_builder_alive()` ni un criterio equivalente basado en
  `BUILDER_EXIT` posterior al lock y mtime fresco.
- El cierre reclama evidencia que no aparece en artefactos verificables.
- Se mezclan cambios de parser, scope watch o rediseno de protocolo.
