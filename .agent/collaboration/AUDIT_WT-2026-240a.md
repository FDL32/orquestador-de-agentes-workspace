# AUDIT_WT-2026-240a

## Riesgos Bloqueantes

### CRITICO - bypass sigue sin detectar motor sucio
Si el fix no inserta `motor_uncommitted_productive()` antes del
`git status --porcelain`, el bug de `WT-2026-239a` persiste. Verificar que la
llamada ocurre al inicio de la rama documental, antes de cualquier otra
operacion.

### CRITICO - test invertido de forma incompleta
Si el test documental sigue aceptando `result == 0` con motor sucio, el ticket
no protege el bugfix. La inversion debe ser exacta: mismo setup, assert
cambiado a `1`.

### ALTO - regresion en tickets code
Si el fix rompe la rama `code`, el ticket no puede cerrarse. Verificar que la
ruta actual de tickets `code` siga bloqueando como antes.

### ALTO - bypass documental vuelve a crear commit o tag
El objetivo no es eliminar el bypass, sino endurecerlo. Si el caso documental
limpio vuelve a crear commit/tag/checkpoint en `repo_motor`, el fix reabre el
problema original.

## TP Check

TP-01: la rama documental llama a `motor_uncommitted_productive(motor_root)`
antes de cualquier otra operacion.

TP-02: si `repo_motor` esta sucio, se emite `HANDOFF_BLOCKED` y retorna `1`.

TP-03: si `repo_motor` esta limpio, el bypass prosigue sin commit ni tag.

TP-04: `test_docs_ticket_dirty_motor_blocks` verifica `result == 1` con motor
sucio.

TP-05: `test_docs_ticket_clean_motor_bypass` verifica `result == 0` sin commit
ni tag en motor.

TP-06: `test_code_ticket_still_blocks_on_dirty_motor` verifica que `code` sigue
bloqueando sin regresion.

TP-07: `pytest`, `ruff` y `validate --json` ejecutados sin errores.

## Veredicto Previo

`APPROVED`
