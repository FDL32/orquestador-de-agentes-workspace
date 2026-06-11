# AUDIT_WT-2026-242a

## Riesgos Bloqueantes

### CRITICO - el bridge sigue decidiendo JSON/no-JSON desde PATH en vez del ejecutable real
Si el fix mantiene una deteccion global basada en `opencode.cmd` o en un probe
stale de `__init__`, el bug observado en `WT-2026-241a` puede repetirse.

### CRITICO - fallback sin JSON se activa por cualquier exit_code
Si el bridge hace fallback por cualquier `exit_code != 0`, enmascara timeouts,
auth failures o corrupcion de transporte como si fueran solo "flag no
soportado".

### ALTO - APPROVE textual deja de degradarse
Si el cambio abre `APPROVE` desde texto plano o desde una ruta no autoritativa,
se relaja una barrera deliberadamente conservadora del cierre canonico.

### ALTO - tests no fijan el caso real de PATH vacio
Si no existe una prueba donde `PATH` este vacio pero el `manager_executable` sea
valido, el bug exacto observado no queda barrado.

## TP Check

TP-01: la review OpenCode intenta `--format json` con el ejecutable real.

TP-02: el fallback sin JSON solo ocurre ante stderr/help compatibles con flag no
soportado.

TP-03: un ejecutable valido fuera de `PATH` sigue usando JSON.

TP-04: `APPROVE` textual tras fallback sigue degradando a `INSPECT`.

TP-05: `validate --json` del `repo_destino` queda sin errores.

## Veredicto Previo

`APPROVED`
