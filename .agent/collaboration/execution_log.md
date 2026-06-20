# execution_log.md -- WOT-2026-011f
## Metadata
- **Ticket:** WOT-2026-011f
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-011f.
- Motivo: `011i` queda bloqueado por los 3 tests no parallel-safe destapados en `011e`; el siguiente paso real es cerrar la deuda de contrato/encoding para `*.ps1` y el launcher.
- Contrato congelado: `T-011F-001`.
- Frontera fijada antes de Builder: `011f` = contrato de fuente/line endings/guard para PowerShell; NO reabre `011j` funcional ni toca handoff/CI.
- Runtime bootstrap esperado para Builder: `STATE=IN_PROGRESS`, `TURN=BUILDER/IMPLEMENT`, `work_plan.md` activo en `011f`.
## Premise Re-check requerido al Builder
- Confirmar que `.gitattributes` no cubre aun `*.ps1`.
- Confirmar por bytes que `launch_agent_terminals.ps1` sigue con BOM y CRLF.
- Releer `encoding_guard.py` y verificar que `.ps1` esta en `TEXT_EXTENSIONS` pero no en el barrido repo-wide.
- Releer `bom_source_audit_WOT-2026-011c.md` y las barreras de launcher/encoding ya existentes.
## Restriccion cross-ticket
- `011f` no reabre writers BOM-safe de `011j`, no toca `pre_handoff_guard.py`, no toca CI y no corrige historicos congelados.
- Si el launcher necesita una reparacion funcional ajena a encoding/line endings, el ticket para con `CG-WOT-2026-011f.md`.

## BUILDER - WOT-2026-011f - Encoding .ps1 multiplataforma

### Fase 0 - Baseline (VERIFICADO por bytes)
- scripts/launch_agent_terminals.ps1: BOM UTF-8 SI, 1921 CRLF (0 bare LF), 4 secuencias mojibake doble-encoding (Ã³->o canonico/proximo, Ãº->u aun, Ã­->i asi) + 2 em-dash mojibake (â€->-)  + 1 em-dash legitimo U+2014 que el guard tambien rechaza.
- scripts/test_manager_smoke.ps1: sin BOM; 2 bytes c2b7 (·, U+00B7, middle-dot LEGITIMO en regex de parseo, NO mojibake; guard exit 0). Acota blast radius a 2 .ps1.
- .gitattributes: sin regla *.ps1.
- scripts/encoding_guard.py: .ps1 en TEXT_EXTENSIONS (L21) pero NO en GLOB_PATTERNS (solo scripts/**/*.py). Ese es el seam.

### Fase 1 - Implementacion
- .gitattributes: anadida regla `*.ps1 text eol=crlf` (coherente con CRLF del launcher en Windows).
- launcher normalizado: BOM removido; 7 secuencias mojibake reconstruidas DIRIGIDO (no replace ciego; 0 acentos legitimos en el archivo, sin riesgo). CRLF preservados (1921). 0 non-ascii restantes. Diff = 7 lineas, TODAS encoding (6 comentarios + 1 string de mensaje de error), 0 logica funcional. PARSE OK (AST PowerShell).
- encoding_guard.py: GLOB_PATTERNS + "scripts/**/*.ps1".
- Ambos .ps1 limpios bajo el guard repo-wide (exit 0); test_manager_smoke con · legitimo no se marca -> sin deuda nueva, sin CONTRACT_GAP.

### Fase 2 - Barreras (tests/test_encoding_integrity.py, 3 nuevos)
- test_launcher_ps1_is_in_guard_scope: launcher en GLOB + collect_files_to_check.
- test_launcher_ps1_is_clean_no_bom_no_mojibake: launcher sin BOM ni mojibake.
- test_dirty_ps1_would_be_blocked: un .ps1 con BOM+mojibake es detectado (scope real, no cosmetico).
- Verificacion FAIL-sin/PASS-con: revertido guard+launcher a HEAD -> test_launcher_ps1_is_in_guard_scope + is_clean FAIL (2 failed); restaurado -> 2 passed.

### Gates
- Tests focales: `python -m pytest tests/test_encoding_integrity.py tests/test_launch_agent_terminals_script.py -q` -> 304 passed, 15 skipped.
- Ruff: All checks passed! | Ruff format: 3 files already formatted.
- Encoding launcher: `python scripts/check_encoding_guard.py scripts/launch_agent_terminals.ps1` -> exit 0.
- PowerShell parse (AST): PARSE OK.
