# AUDIT_WT-2026-234a

## Riesgos bloqueantes

### CRITICO - borrado por regex sin clasificacion
Bloquear cualquier implementacion que borre o mueva archivos solo porque el nombre
contiene un ID.

### ALTO - Builder cruza al repo_destino
El Builder solo modifica `scripts/session_closeout.py` y su test en `repo_motor`.
Archivo, memoria, collaboration y limpieza local son Manager-only.

### ALTO - archivo sin prueba de integridad
No retirar `BUS_ARCHITECTURE_WT-2026-210.md` hasta copiarlo al destino y comparar
checksum.

### ALTO - limpieza destructiva sin human gate
No borrar `.agent/backups/` ni `tests/sandbox/test_runtime/` sin autorizacion
explicita y comprobacion de que Git los ignora.

### MEDIO - falso positivo por contenido
La barrera analiza basename de paths versionados; mencionar `WT-2026-...` dentro de
un archivo portable es valido.

### MEDIO - regex incompleta
Debe cubrir IDs legacy sin sufijo, nuevos con sufijo alfabetico y nombres con
underscore tipo `test_wt_*`.

### MEDIO - memoria duplicada
La propuesta debe fusionarse conceptualmente con `repo-motor-portable-root`, no
repetirla sin valor incremental.

### MEDIO - documentacion root solapada u obsoleta
Revisar `UPGRADE_GUIDE.md`, `DISTRIBUTION_GUIDE.md` y `UPGRADE_CLEANUP_GUIDE.md`
contra comandos reales. No mantener tres guias que describen contratos distintos
para la misma operacion.

### MEDIO - monitor con parser legacy
`ticket_activity_monitor.py` debe reconocer el formato canonico del `work_plan.md`
(`**ID:**` / `**Plan ID:**`) y no depender solo de `Ticket activo`.

## TP Check

TP-01: verificar que la fuente sea `git ls-files`.
TP-02: probar legacy, sufijado, PLAN y underscore `test_wt_*`.
TP-03: revisar diff y confirmar cero paths del destino en entrega Builder.
TP-04: comparar hash origen/destino antes del git rm.
TP-05: exigir confirmacion humana para 834 MB ignorados.
TP-06: comprobar que no se escribio memoria upstream sin confirmacion.
TP-07: revisar report final, validate y git status de ambos repos.
TP-08: cada markdown root auditado queda clasificado y las guias obsoletas quedan
actualizadas, fusionadas o archivadas.
TP-09: monitor probado con formato canonico y formato legacy.

## Comandos de revision

```powershell
git -C <repo_motor> ls-files
git -C <repo_motor> diff --name-status
python -m pytest tests/test_session_closeout.py -q
python -m pytest tests/test_ticket_activity_monitor.py -q
python -m ruff check scripts/session_closeout.py scripts/ticket_activity_monitor.py tests/test_session_closeout.py tests/test_ticket_activity_monitor.py
python scripts/session_closeout.py --project-root <repo_destino> --dry-run
```

## Veredicto previo

`APPROVED`: plan auditado y listo para Builder. Las decisiones humanas sobre
memoria, archivo y limpieza quedan como gates Manager-only dentro del ticket.
