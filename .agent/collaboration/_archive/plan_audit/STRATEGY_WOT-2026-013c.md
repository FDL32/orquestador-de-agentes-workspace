# STRATEGY_WOT-2026-013c.md

## Objetivo
Aislar los 3 tests global-state-bound para que el triple quede verde tanto en serial como bajo xdist `--dist load`, sin tocar runner ni politica de cierre.

## Fases
1. Baseline read-only
   - Reproducir serial verde y xdist rojo del triple exacto.
   - Registrar firma del rojo y confirmar que sigue anclado en estos 3 tests.
2. Aislamiento de estado
   - Inspeccionar fixtures y shared state (`cwd`, git, escaneo de proyecto vivo, tmp roots).
   - Introducir aislamiento minimo en `tests/conftest.py` o fixtures locales.
3. Barrera
   - Demostrar FAIL-sin/PASS-con sobre el rojo real; no aceptar verde cosmético.
4. Gates
   - Triple serial + triple xdist + ruff + `--level all` + `validate`.
5. Handoff
   - Solo si el diff queda acotado a tests/fixtures y toda la evidencia es literal.

## Riesgos
- Que el rojo se desplace a otra familia y el ticket deje de ser honesto.
- Que el fix tentador sea tocar runner/politica: eso es STOP, no atajo.
- Que aparezca mock drift o floor assertions: review debe rechazarlo.