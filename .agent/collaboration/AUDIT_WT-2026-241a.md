# AUDIT_WT-2026-241a

## Riesgos Bloqueantes

### CRITICO - el launcher sigue dependiendo solo de builder_lock.txt
Si el cambio no inspecciona procesos Builder reales del `project_root`, el bug
operativo persiste aunque se limpien locks stale.

### CRITICO - limpieza mata procesos fuera del Builder o fuera del proyecto
La limpieza debe estar acotada al `project_root` activo y al rol Builder. Si
mata supervisor, review bridge o procesos ajenos, el fix no es aceptable.

### ALTO - resume path queda sin limpieza Builder
Si el hardening solo aplica al arranque fresco y no al launch efectivo del
Builder en la ruta relevante de resume/relaunch, el caso real observado en
`WT-2026-240a` persiste.

### ALTO - borra builder_session/lock sin haber cerrado procesos previos
La limpieza de artefactos debe estar condicionada a haber detectado/cerrado
Builders previos; no debe destruir sesion valida arbitrariamente.

## TP Check

TP-01: el launcher detecta procesos Builder previos del mismo `project_root`.

TP-02: antes del launch del nuevo Builder, esos procesos se cierran.

TP-03: si hubo procesos Builder previos, se limpian `builder_lock.txt` y
`builder_session.json`.

TP-04: la limpieza no apunta a supervisor ni manager bridge salvo en la ruta
que ya existia para arranque fresco.

TP-05: el hardening aplica en la ruta real donde se lanza Builder, no solo en
  preflight irrelevante.

TP-06: `validate --json` del `repo_destino` queda sin errores.

## Veredicto Previo

`APPROVED`
