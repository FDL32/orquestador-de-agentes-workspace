# Execution Log -- WOT-2026-013v

**Estado:** IN_PROGRESS

## Bootstrap operativo -- WOT-2026-013v

Ticket activado para documentar la semantica operativa de `reviews/` en `scripts/prune_runtime_retention.py` sin cambiar el algoritmo de orden ni ampliar el blast radius del borrado local.

Procedencia verificada (2026-06-25):
- `WOT-2026-013l` ya cerro canonico en `COMPLETED` y deja como follow-up vivo `013v`.
- El packet canonico de este ciclo vive en `.agent/planning/work_plan_WOT-2026-013v.md`.
- El bus ya registra `STATE_CHANGED -> IN_PROGRESS` para `WOT-2026-013v`.
- `STATE.md` y `TURN.md` se resincronizaron desde la ruta canonica del supervisor para abrir el siguiente Builder loop sin drift.

Premisa activa:
- `reviews/` se ordena hoy por `mtime` del DIRECTORIO del ticket.
- `review_packets/` y `observations.jsonl.bak.*` siguen siendo superficies por archivo y no forman parte del cambio.
- La tarea de `013v` es volver explicita esa semantica en help/docstring/salida y blindarla con tests nominales.

Guardrails del ciclo:
- No cambiar el algoritmo de orden de `reviews/` en esta ronda.
- No tocar `review_packets`, `observations.jsonl.bak.*`, closeout, launcher ni productores de runtime fuera del texto compartido imprescindible.
- Si hacer honesta la semantica exige cambiar el algoritmo real, emitir `CG-WOT-2026-013v.md` y parar.
