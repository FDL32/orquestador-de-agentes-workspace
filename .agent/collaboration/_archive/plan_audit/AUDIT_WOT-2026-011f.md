# AUDIT_WOT-2026-011f.md

## Preguntas binarias de auditoria
- `.gitattributes` declara explicitamente el contrato de `*.ps1`?
- `scripts/launch_agent_terminals.ps1` quedo sin BOM y con line endings coherentes con ese contrato?
- Las secuencias mojibake verificadas del launcher fueron reconstruidas desde contexto confiable, sin sustituciones ciegas?
- El encoding guard repo-wide incluye ahora `scripts/**/*.ps1` o una cobertura equivalente sobre los `.ps1` reales del motor?
- Existe una barrera FAIL-sin/PASS-con que demuestra que el launcher entro en scope del guard?
- `python scripts/check_encoding_guard.py scripts/launch_agent_terminals.ps1`, tests focales, `ruff` y `validate --json --project-root <repo_destino>` terminan en verde?

## Hallazgos a rechazar
- Cualquier cambio que reabra logica funcional del launcher fuera de la normalizacion de fuente.
- Cualquier fix de mojibake basado en replace ciego o en perdida de informacion no justificada por contexto.
- Cualquier ampliacion del guard a `.ps1` que deje deuda nueva no acotada sin CONTRACT_GAP explicito.
- Cualquier intento de arreglar historicos congelados o superficies fuera de FLT bajo la excusa de "ya que tocamos encoding".
