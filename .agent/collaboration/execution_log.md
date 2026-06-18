# execution_log.md -- WOT-2026-008i

## Metadata

- **Ticket:** WOT-2026-008i
- **Estado:** IN_PROGRESS
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-008i`.
- Motivo: `DEC-008G-001` serializa este lote antes de `008j`; `008k` ya dejo el
  catalogo con `role` limpio y `008e/008h` ya fijaron la capa de prompts.
- Premisa verificada: `008g`, `008e`, `008h` y `008k` cerrados canonicamente.
- Decision de alcance: migracion atomica de skill dirs `man-*` -> `manager-*`
  sin aliases runtime nuevos. La compatibilidad se mide sobre triggers,
  bindings prompt<->skill y referencias operativas vivas.
- Pendiente de Builder: baseline de discovery, rename de los cuatro directorios,
  migracion de consumidores vivos, barrera anti-prose-viva y suite canonica
  contra HEAD.