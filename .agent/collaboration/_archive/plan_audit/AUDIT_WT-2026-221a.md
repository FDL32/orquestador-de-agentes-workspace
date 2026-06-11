# AUDIT WT-2026-221a - Relaunch CEM

Alias: Relaunch Topology Gate / Builder Continuity Capsule

## Objetivo del audit
Verificar que `WT-2026-221a` corrige una falla real de relaunch y deja una
barrera proporcional, en lugar de solo adornar el prompt o maquillar la salida
del launcher.

## Reglas de revision
- No aprobar un cambio que solo haga mas largo el prompt.
- Exigir evidencia de que la topologia se valida antes del relaunch.
- Exigir una capsula derivada de artefactos canonicos, no de texto libre.
- Exigir test que reproduzca la familia de fallo tipo seq 578.

## Hallazgos bloqueantes tipicos
1. **Relaunch sigue ocurriendo sin root verificado**
   - El sistema sigue abriendo Builder aunque no haya `repo_destino` canonico o
     el bus no sea legible.

2. **Capsula narrativa**
   - La capsula es solo un resumen libre sin enlaces claros a `TURN.md`,
     `work_plan.md`, `execution_log.md`, feedback o eventos.

3. **Estado stale reciclado**
   - La capsula se reutiliza entre requeues o se acumula como estado vivo.

4. **Test sin reproduccion real**
   - Hay tests del texto del prompt, pero no del bloqueo por topologia ni del
     caso equivalente al seq 578.

5. **Scope creep**
   - El cambio invade gates del Manager o scope-watch temprano sin necesidad
     contractual.

## Evidencia minima esperada
- seam real de relaunch documentado;
- test del fallo tipo seq 578;
- test del camino valido;
- prueba o artefacto de capsula fresh;
- `ruff` y subset de tests verdes.

## TP Check
- TP-01: el seam real de relaunch queda identificado y documentado.
- TP-02: existe barrera observable para root/topologia invalidos.
- TP-03: un relaunch valido genera capsula fresh evidence-linked.
- TP-04: la capsula separa hechos, blockers, hipotesis y siguiente accion.
- TP-05: existe reproduccion verificable de la familia seq 578.
- TP-06: el cambio minimiza superficie y no mezcla `WT-2026-221b` o `WT-2026-221c` sin justificacion explicita.

## Criterio de rechazo inmediato
- relaunch con root invalido que aun retorna exito operativo;
- capsula sin fuentes canonicas identificables;
- ausencia de reproduccion del fallo original;
- mezcla de cambios fuera de `WT-2026-221a` sin justificacion.
