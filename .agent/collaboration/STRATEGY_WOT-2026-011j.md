# STRATEGY_WOT-2026-011j.md

## Objetivo tecnico
Eliminar la fuente BOM in-scope detectada por WOT-2026-011c en el runtime PowerShell del repo_motor y dejar a WOT-2026-012a listo para una regeneracion limpia posterior de su historico, sin absorber ese ticket dentro de 011j.

## Secuencia propuesta
1. Reconfirmar la premisa de partida: `backlog.md` vivo en verde, `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` en rojo solo por control chars historicos, sin mutarlos.
2. Localizar en `scripts/launch_agent_terminals.ps1` las escrituras PowerShell BOM-prone todavia in-scope para 011j.
3. Sustituirlas por el patron BOM-safe ya aceptado por WT-2026-248a o por uno equivalente, manteniendo el comportamiento funcional del launcher.
4. AÃ±adir o ajustar barreras de regresion para que la ruta BOM-prone falle sin el fix y la ruta BOM-safe pase con el fix.
5. Registrar en `execution_log.md` que 011j corrige la fuente viva y que el saneado de `_archive/backlog_*` llegara al relanzar 012a, no por edicion manual aqui.

## Riesgos a vigilar
- Cambiar un writer equivocado y dejar el BOM real intacto.
- Introducir una ruta BOM-safe que rompa `tests/test_opencode_config_stability.py` o el launcher en Windows.
- Invadir el scope de 012a editando historico o regenerando backlog archives dentro de 011j.

## Criterio de salida
El ticket solo puede declararse listo si el writer BOM-prone in-scope queda corregido, la barrera de regresion es verde, el encoding guard sobre superficies propias pasa y `execution_log.md` deja explicitado el follow-up de regeneracion para 012a.
