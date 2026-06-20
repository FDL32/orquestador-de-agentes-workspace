# work_plan.md -- WOT-2026-011f
## Metadata
- **ID:** WOT-2026-011f
- **Contract ID:** T-011F-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Normalizar el contrato multiplataforma de `*.ps1`: declarar line endings explicitamente en `.gitattributes`, sanear `scripts/launch_agent_terminals.ps1` para que quede sin BOM ni mojibake y meter los `.ps1` reales de `scripts/` bajo la barrera canonica de encoding, sin reabrir la logica funcional del launcher.
## Non-goals
- No cambiar el comportamiento funcional del launcher salvo lo estrictamente necesario para normalizar su fuente.
- No reabrir `011j` ni volver a tocar writers BOM-safe ya corregidos.
- No tocar `pre_handoff_guard.py`, CI/workflows ni historicos de backlog/control-chars de `012a`.
- No ampliar el alcance fuera de `scripts/launch_agent_terminals.ps1`, `scripts/test_manager_smoke.ps1`, `.gitattributes` y `scripts/encoding_guard.py`.
## Premisas verificadas antes de Builder
- `.gitattributes` no declara aun `*.ps1`.
- `scripts/launch_agent_terminals.ps1` sigue con BOM UTF-8 en origen, usa CRLF y contiene secuencias mojibake verificadas (`???` en lineas 91/100).
- `scripts/encoding_guard.py` incluye `.ps1` en `TEXT_EXTENSIONS`, pero su barrido repo-wide omite `scripts/**/*.ps1`.
- `scripts/test_manager_smoke.ps1` ya esta limpio, por lo que el blast radius actual de la cobertura `.ps1` es acotable.
## Decision Arquitectonica
`011f` cierra la deuda de fuente, no la de writers: el launcher se normaliza como artefacto versionado y el guard pasa a cubrir los `.ps1` reales del motor. El contrato objetivo es `*.ps1` versionados con line endings explicitamente declarados, UTF-8 sin BOM y barrera automatica repo-wide. El fix debe reconstruir el mojibake desde contexto confiable, no por reemplazo ciego.
## Files Likely Touched
### repo_motor
- .gitattributes
- scripts/launch_agent_terminals.ps1
- scripts/encoding_guard.py
- tests/test_encoding_integrity.py
- tests/test_launch_agent_terminals_script.py
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- tests/test_opencode_config_stability.py
- tests/unit/test_launcher_powershell_syntax.py
- scripts/test_manager_smoke.ps1
- .agent/runtime/audit/bom_source_audit_WOT-2026-011c.md
- scripts/check_encoding_guard.py
## Forbidden Surfaces
- reabrir la logica funcional del launcher fuera de normalizacion de fuente
- broad-strip de BOM/mojibake fuera de las superficies declaradas
- tocar pre_handoff_guard.py o workflows de CI
- editar historicos de backlog/control-chars congelados
## Criterios binarios
- `.gitattributes` declara explicitamente el contrato de `*.ps1`.
- `scripts/launch_agent_terminals.ps1` queda sin BOM y con line endings coherentes con el contrato fijado.
- Las secuencias mojibake verificadas del launcher se reconstruyen desde contexto confiable.
- `scripts/encoding_guard.py` incorpora `scripts/**/*.ps1` (o cobertura repo-wide equivalente) al scope real del guard.
- Existe al menos una barrera FAIL-sin/PASS-con para demostrar que el launcher entra en scope del guard y que el estado previo habria fallado.
- `python scripts/check_encoding_guard.py scripts/launch_agent_terminals.ps1`, tests focales, `ruff` y `validate --json --project-root <repo_destino>` quedan verdes.
## STOP conditions
- Parar si el target de line endings no puede verificarse en este host Windows.
- Parar si arreglar el mojibake exige adivinar contenido sin contexto confiable.
- Parar si ampliar el guard a `.ps1` saca deuda nueva fuera de `scripts/launch_agent_terminals.ps1` y `scripts/test_manager_smoke.ps1`.
## CONTRACT_GAP
Emitir `CG-WOT-2026-011f.md` si normalizar el launcher exige tocar logica funcional ajena al contrato de fuente, si el mojibake no puede reconstruirse con evidencia, o si la cobertura repo-wide de `.ps1` revela deuda adicional no acotable dentro del scope declarado.
