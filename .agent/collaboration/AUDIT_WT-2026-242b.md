# AUDIT_WT-2026-242b

## Riesgos Bloqueantes

### CRITICO - la shell huerfana sigue emitiendo HANDOFF_BLOCKED en READY_FOR_REVIEW+
Si el cambio deja intacta la emision de `HANDOFF_BLOCKED` para
`stale_builder_round` cuando el ticket ya esta fuera de `IN_PROGRESS`, el bug
observado sigue vivo aunque cambie el texto del log.

### CRITICO - la contencion rompe el bloqueo legitimo en IN_PROGRESS
Si el filtro se vuelve demasiado amplio y deja pasar una Builder realmente
invalida mientras el ticket aun esta en `IN_PROGRESS`, se relaja un gate real
del sistema.

### ALTO - el nuevo evento no tiene contrato claro
Si se introduce `STALE_BUILDER_ORPHAN` (o equivalente) sin definir dondese
consume o ignora, el sistema puede tratarlo como ruido desconocido o, peor,
como trigger operativo no previsto.

### ALTO - el test solo comprueba logs y no el bus
Si la prueba valida solo stderr/stdout pero no confirma que el bus ya no recibe
`HANDOFF_BLOCKED`, el bug queda sin barrera real.

## TP Check

TP-01: `stale_builder_round` en `READY_FOR_REVIEW+` no emite
`HANDOFF_BLOCKED`.

TP-02: la contencion deja rastro diagnostico trazable sin modificar el estado
canonico del ticket.

TP-03: `stale_builder_round` en `IN_PROGRESS` mantiene el bloqueo actual.

TP-04: `validate --json` del `repo_destino` queda sin errores.

## Veredicto Previo

`APPROVED`
