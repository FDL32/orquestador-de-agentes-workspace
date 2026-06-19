# STRATEGY_WOT-2026-012a.md

## Objetivo tecnico
Separar la cola viva del historico en `backlog.md`, regenerar los artefactos historicos desde una fuente viva ya limpia tras `011j` y fijar el formato parseable que `012b` convertira luego en gate.

## Secuencia propuesta
1. Releer `backlog.md`, `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` como baseline.
2. Materializar snapshot pre-corte portable antes de mover terminales.
3. Mover por bloques logicos los tickets terminales al historico, preservando integra la seccion `### WOT-2026-012a`.
4. Dejar la tabla activa como cola viva parseable con `Reactivation` estructurado.
5. Registrar conteos y evidencia mecanica del movimiento en `execution_log.md`.
6. Cerrar con `check_encoding_guard.py` + `validate --json` en verde.

## Restriccion deliberada
El BOM/mojibake preexistente del propio `scripts/launch_agent_terminals.ps1` queda fuera de `012a`. Esa correccion pertenece a `011f` y no debe contaminar el corte documental de backlog.
