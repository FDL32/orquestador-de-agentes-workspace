# AUDIT_WOT-2026-012a.md

## Preguntas binarias de auditoria
- `backlog.md` activo quedo como cola viva sin tickets terminales mezclados?
- Existe historico separado y auditable para los tickets movidos?
- La tabla activa es la unica fuente parseable y expone `Reactivation` con el vocabulario acordado?
- La seccion `### WOT-2026-012a` se conserva integra en el historico?
- `python scripts/check_encoding_guard.py` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes?
- El ticket evita tocar `--session-close` / `--mark-ready` y evita absorber la deuda de encoding del `.ps1` del motor?

## Hallazgos a rechazar
- Cualquier corte que pierda historico o requiera reconstruccion no auditable.
- Cualquier solucion que vuelva a depender de comentarios HTML como semantica obligatoria.
- Cualquier intento de arreglar aqui el BOM/mojibake preexistente de `scripts/launch_agent_terminals.ps1`.
