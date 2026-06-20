# STRATEGY_WOT-2026-011f.md

## Objetivo tecnico
Cerrar la deuda de contrato para PowerShell en el motor: declarar `*.ps1` en `.gitattributes`, dejar `launch_agent_terminals.ps1` como UTF-8 sin BOM con line endings explicitamente fijados y extender el encoding guard repo-wide a los `.ps1` reales de `scripts/`.

## Secuencia propuesta
1. Reconfirmar por bytes el baseline de `launch_agent_terminals.ps1` (BOM + CRLF + mojibake) y de `scripts/test_manager_smoke.ps1` (sin BOM).
2. Fijar en `.gitattributes` el contrato de `*.ps1`.
3. Normalizar `scripts/launch_agent_terminals.ps1` sin tocar semantica funcional: quitar BOM, conservar line endings del contrato y reconstruir solo las secuencias mojibake verificadas.
4. Extender `scripts/encoding_guard.py` para que el barrido repo-wide incluya `scripts/**/*.ps1`.
5. Anadir/ajustar barreras en `tests/test_encoding_integrity.py` y `tests/test_launch_agent_terminals_script.py` para demostrar FAIL-sin/PASS-con.
6. Reejecutar `check_encoding_guard.py` explicito sobre el launcher, tests focales, `ruff` y `validate --json`.
7. Cerrar sin tocar workflows, handoff guard ni otros historicos de encoding fuera del scope.

## Riesgos a vigilar
- El launcher es una superficie grande: cualquier cambio debe ser estrictamente de fuente/encoding, no de comportamiento.
- Meter `scripts/**/*.ps1` en el guard puede exponer deuda nueva; el contrato permite parar con CONTRACT_GAP si no se puede acotar a los dos `.ps1` actuales.
- La reconstruccion del mojibake debe apoyarse en contexto inequ?voco; si no, hay que escalar en vez de inventar texto.
