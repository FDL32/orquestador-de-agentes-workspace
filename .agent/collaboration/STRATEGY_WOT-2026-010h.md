# STRATEGY_WOT-2026-010h -- Propagar prefijo per-project a prompts

## Hechos verificados

- El prefijo per-project ya es verdad en codigo (`bus/ticket_id.py`,
  `(?:WP|WT|[A-Z]{3})`). No hay que cambiar runtime; hay que alinear docs.
- `session_bootstrap.md` (59,88) es la fuente de redaccion canonica; el resto de
  prompts debe REFERENCIARLA, no redefinir la regla en paralelo.
- Gate de cierre disponible: `check_ticket_nomenclature.py` (falla ante
  generador/ejemplo vivo con prefijo legacy sin etiqueta).

## Plan tecnico

1. Releer la redaccion de referencia en `session_bootstrap.md` y fijar una
   formulacion unica de la regla (orden de fuente + `WOT-` = motor only).
2. En cada uno de los 4 prompts, anadir/ajustar una nota breve y consistente:
   - el `<PREFIX>` se lee del contrato del repo activo
     (`AGENTS.md`/`CLAUDE.md` autocargado);
   - verificacion via `agent_controller --validate`, no por una linea suelta de
     `PROJECT.md`;
   - `WOT-` es prefijo del motor/dogfooding, no universal.
3. Donde haya ejemplos de ID, asegurarse de que no introducen `WP-`/`WT-` vivos
   nuevos y que dejan claro el origen per-project.
4. Pasar `check_ticket_nomenclature.py`, encoding guard y `validate` 0/0.

## Riesgos

- **Redefinicion en paralelo:** que cada prompt diga la regla con palabras
  distintas y se contradigan. Mitigacion: una sola formulacion, referenciada.
- **Ejemplo vivo legacy:** introducir `WP-`/`WT-` como plantilla -> rompe el
  gate de nomenclatura. Mitigacion: usar `XXX-YYYY-NNN` o `WOT-` etiquetado como
  motor.
- **Scope creep documental:** tocar `QUICKSTART.md`/`INTERACTION_MODES.md` o
  010g. Mitigacion: Forbidden Surfaces explicitas.

## No hacer

- No tocar `bus/ticket_id.py` ni ningun codigo/gate ejecutable.
- No reescribir historia de commits ni ejemplos legacy etiquetados.
- No mezclar con 010g.
