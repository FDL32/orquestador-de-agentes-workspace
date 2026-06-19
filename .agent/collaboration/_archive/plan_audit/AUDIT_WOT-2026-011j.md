# AUDIT_WOT-2026-011j.md

## Preguntas binarias de auditoria
- El diff de 011j elimina o encapsula de forma BOM-safe las escrituras PowerShell BOM-prone declaradas in-scope en `scripts/launch_agent_terminals.ps1`?
- Existe una prueba o barrera de regresion que falla sin el fix y pasa con el fix para la ruta cambiada?
- `tests/test_opencode_config_stability.py` sigue pasando y protege el patron BOM-safe ya aceptado?
- El ticket evita editar manualmente `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md`, dejando ese saneado para el relanzamiento posterior de 012a?
- `python scripts/check_encoding_guard.py` sobre las superficies propias de 011j queda verde?
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` queda en 0 errors / 0 warnings?

## Hallazgos a rechazar
- Cualquier fix que solo ponga verde el ticket manipulando manualmente archivos historicos de 012a.
- Cualquier cambio que mueva el problema a `agent_controller.py`, `check_encoding_guard.py` o a superficies fuera del FLT sin reabrir contrato.
- Cualquier handoff que no deje explicitado en `execution_log.md` que 012a debe regenerar su historico despues del fix de fuente.
