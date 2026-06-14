# AUDIT WOT-2026-005a - memory_upload: decision de destino de memoria

## Objetivo
Verificar que el prompt obliga a decidir destino de memoria con contrato (privada vs
portable), exige schema/NO PROMOVIBLE para portables, y bloquea entradas portables sobre
schema en drift. Documental: foco en claridad e integridad, sin codigo.

## Reglas de revision
- Leer el diff real del prompt.
- Confirmar los 3 criterios binarios del work_plan textualmente presentes.
- Confirmar que NO se toco schema ni codigo (solo el prompt).
- Encoding limpio.

## TP Check
TP-01: el prompt distingue 3 memorias y exige declarar destino antes de escribir. (texto)
TP-02: portable -> schema OK o etiqueta `NO PROMOVIBLE` con motivo. (texto)
TP-03: schema en drift -> prohibido añadir portables sin ticket de migracion. (texto)
TP-04: encoding guard exit 0; solo `prompts/memory_upload.md` cambia en el motor. (command/git)
TP-05: commit en repo_motor con WOT-2026-005a. (git)

## Rechazo inmediato
- Falta alguno de los 3 criterios; o se toco schema/codigo; o encoding sucio.
