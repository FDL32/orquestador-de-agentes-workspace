# AUDIT WT-2026-221b - Manager evidence gate

## Alias
Manager Evidence Gate / Review Packet Diff Authority.

## Objetivo del audit
Verificar que el cambio impide reviews sin evidencia minima verificable del
ticket activo, especialmente cuando el packet solo contiene docs o artefactos de
colaboracion.

El auditor debe separar claims verificados, inferencias razonables y gaps no
verificados. Ningun auto-reporte del Builder cuenta como evidencia por si solo.

## Reglas de revision
- Revisar el archivo real y el test real antes de emitir hallazgos criticos.
- Confirmar que el gate opera sobre el camino real de review, no sobre un wrapper
  documental paralelo.
- Confirmar que la evidencia del `repo_motor` no se confunde con estado del
  `repo_destino`.
- Confirmar que docs-only/collaboration-only no puede pasar como implementacion.
- Confirmar que el mensaje de rechazo es accionable para Builder.

## Hallazgos bloqueantes tipicos
### CRITICO - Review packet sin diff/commit productivo aceptado
Si el caso docs-only/collaboration-only puede llegar a review como valido, el
ticket no cumple su objetivo.

### CRITICO - Gate mira el repo equivocado
Si el gate calcula diff solo en el `repo_destino` o ignora el `repo_motor`, puede
repetir el fallo de `seq 602/606/617`.

### ALTO - Bus/estado activo no requerido
Si el review puede ejecutarse sin ticket activo consistente, falta la autoridad
minima de estado.

### ALTO - Evidencia de tests sustituida por relato
Si el cierre solo lista tests en texto sin artefacto o salida verificable, queda
un gap CEM.

### MEDIO - Mensaje de rechazo no accionable
Si el gate falla pero no explica que falta, el Builder queda bloqueado sin ruta
de correccion.

### MEDIO - Scope creep hacia tickets hermanos
Cambios de parser central (`WT-2026-223a`) o scope-watch temprano
(`WT-2026-221c`) deben rechazarse salvo justificacion explicita y minima.

## Evidencia minima esperada
- Test de reproduccion docs-only/collaboration-only.
- Test de rechazo por bus/estado activo ausente o inconsistente.
- Test de aceptacion con evidencia minima del `repo_motor`.
- Salida de tests focales.
- Salida de `ruff`.
- Validacion del `repo_destino` sin errores ni warnings.
- Muestra del blocker estructurado o salida equivalente.

## TP Check
TP-01: seam real de review packet confirmado en codigo.

TP-02: review sin bus/estado activo queda rechazado.

TP-03: review docs-only/collaboration-only queda rechazado.

TP-04: review con evidencia minima del `repo_motor` pasa el gate.

TP-05: familia `seq 602/606/617` reproducida por test.

TP-06: rechazo accionable, no solo fallo generico.

TP-07: no hay scope creep hacia `WT-2026-221c` o `WT-2026-223a`.

## Criterio de rechazo inmediato
- No hay test que falle sin el gate.
- El gate no distingue `repo_motor` de `repo_destino`.
- El packet docs-only/collaboration-only pasa.
- El cierre reclama evidencia que no aparece en artefactos verificables.
- Builder marca ready con cambios productivos sin commit/diff visible.
