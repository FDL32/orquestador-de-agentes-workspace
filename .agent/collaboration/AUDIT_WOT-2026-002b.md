# AUDIT WOT-2026-002b - Decision de los 10 huerfanos

## Objetivo del audit
Verificar que cada una de las 10 decisiones se apoya en evidencia real (grep citado
en motor + destino, determinacion de dominio), no en el relato; y que NO se movio ni
borro ningun huerfano (eso es A2d).

## Reglas de revision
- Cada decision debe citar grep concreto (archivo:linea) o "sin hits en motor ni destino".
- "archive-legacy" exige evidencia de muerte: sin invocacion viva Y (superado o deprecado).
- "promote-to-motor" exige que sea tooling del sistema sin equivalente funcional en motor.
- "destino-keep" exige que implemente dominio/integracion real del destino, no solo
  "existe solo aqui".
- Confirmar que el arbol real no cambio: ningun huerfano movido/borrado.

## Hallazgos bloqueantes tipicos
- CRITICO: una decision sin evidencia (relato "parece legacy" sin grep).
- CRITICO: se movio/borro un huerfano en este ticket (es A2d, no 002b).
- ALTO: "archive" de algo con invocacion viva (rompe un flujo en A2d).
- ALTO: "destino-keep" justificado solo por basename/ubicacion, no por dominio.
- MEDIO: huerfano "dudoso" cerrado como decision firme sin evidencia suficiente.

## Evidencia minima esperada
- 10 filas, cada una con: ruta, grep motor, grep destino, dominio, decision, barrera-A2d (si).
- 0 huerfanos sin resolver.
- validate 0/0; encoding guard OK.

## TP Check
TP-01: los 10 huerfanos tienen decision; 0 sin resolver. (doc)
TP-02: cada decision cita grep real (motor + destino) o "sin hits" verificable. (doc/grep)
TP-03: ningun huerfano fue movido/borrado (git status destino sin renames/deletes). (git)
TP-04: las decisiones "archive" tienen evidencia de muerte (sin invocacion + superado/deprecado). (doc)
TP-05: barreras para A2d listadas (huerfanos no-archivables sin reconciliar). (doc)
TP-06: validate 0/0; encoding limpio. (command)

## Criterio de rechazo inmediato
- Alguna decision sin evidencia citable.
- Se movio o borro un huerfano (scope de A2d invadido).
- Se archivo algo con invocacion viva demostrable.
