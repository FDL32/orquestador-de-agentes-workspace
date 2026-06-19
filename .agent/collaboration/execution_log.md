# execution_log.md -- WOT-2026-011j
## Metadata
- **Ticket:** WOT-2026-011j
**Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-011j.
- Motivo: WOT-2026-011c ya identifico la fuente del BOM y el follow-up correcto es endurecer el writer PowerShell in-scope antes de relanzar 012a.
- Contrato congelado: T-011J-001.
- Runtime bootstrap esperado para Builder: STATE=IN_PROGRESS, TURN=BUILDER/IMPLEMENT, work_plan.md activo en 011j.
## Premise Re-check requerido al Builder
- `python scripts/check_encoding_guard.py .agent/collaboration/backlog.md` -> verde.
- `python scripts/check_encoding_guard.py .agent/collaboration/_archive/backlog_done.md .agent/collaboration/_archive/backlog_pre_012a.md` -> rojo por 3 control chars historicos.
- `scripts/launch_agent_terminals.ps1` conserva escrituras BOM-prone in-scope que justifican el fix.
## Restriccion cross-ticket
- 011j no edita manualmente `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md`.
- Si el rojo restante pertenece solo a la regeneracion de 012a, el Builder debe dejar evidencia y parar; no debe absorber 012a en este ticket.

## BUILDER - WOT-2026-011j - Fix fuente BOM en launcher PowerShell

### Fase 0 - Premise re-check (VERIFICADO)
- check_encoding_guard backlog.md vivo -> exit 0 (verde).
- check_encoding_guard _archive/backlog_done.md + backlog_pre_012a.md -> exit 1 SOLO por 3 control chars historicos (\x07udi/\x0Bali/\x08ui-). NO tocados (forbidden + scope 012a).
- Writes BOM-prone in-scope localizados en scripts/launch_agent_terminals.ps1:
  L1440 Set-Content -Encoding UTF8 ($ConfigPath, opencode.json) y L1904 Out-File -Encoding UTF8 ($lockPath, builder lock).
- Patron BOM-safe canonico ya existente (WT-2026-248a): [IO.File]::WriteAllBytes / UTF8Encoding($false). Reutilizado, no se invento politica nueva.

### Fase 1 - Implementacion
- L1440: $config|ConvertTo-Json -> [IO.File]::WriteAllText($ConfigPath,$configJson,(New-Object System.Text.UTF8Encoding $false)).
- L1904: $builderLockState|ConvertTo-Json -> [IO.File]::WriteAllText($lockPath,$builderLockJson,(UTF8Encoding $false)).
- 0 writes BOM-prone (no-comentario) restantes (grep verificado).
- Parser AST PowerShell: PARSE OK. Prueba funcional: WriteAllText UTF8($false) -> primeros bytes 7B 0D 0A (sin BOM).
- _archive/backlog_done.md y _archive/backlog_pre_012a.md NO editados (verificado: read-only, sin cambios).

### Fase 2 - Barrera de regresion
- tests/test_launch_agent_terminals_script.py::test_launcher_inscope_json_writes_are_bom_safe:
  afirma 0 writes Set-Content/Out-File -Encoding UTF8 in-scope + presencia del patron WriteAllText UTF8($false) para ConfigPath y lockPath.
- Verificacion FAIL-sin/PASS-con: revertido launcher a HEAD -> test FAIL (detecta los 2 writes BOM-prone); restaurado fix -> 1 passed.

### Hallazgo de scope (BOM/mojibake pre-existente del propio .ps1)
- El launcher en HEAD YA tiene BOM + 1 mojibake (pre-existente, no introducido por 011j; mis lineas anadidas son ASCII puro, verificado git diff).
- .ps1 NO esta en GLOB_PATTERNS del encoding guard (solo .md/.py); en staged-mode (commit normal) el guard NO lo chequea -> HEAD lo commitea con BOM sin bloqueo. El rojo solo aparece en modo explicito.
- DECISION: NO sanear el BOM/mojibake del propio launcher. Esta fuera del scope de 011j (writes que PRODUCE el launcher, no encoding DEL launcher), no lo cubre el gate de commit, y tocarlo seria "caza general de writers" (STOP condition del contrato). Se deja como deuda separada (candidato a follow-up de encoding de .ps1, dominio de 011f .gitattributes / encoding).

### Follow-up 012a (explicito)
- 011j corrige la FUENTE viva del BOM (writer PS). El saneado de _archive/backlog_done.md y _archive/backlog_pre_012a.md (3 control chars historicos) NO se hace aqui: WOT-2026-012a debera REGENERAR su historico limpio desde el backlog vivo al relanzarse, no por edicion manual de los archives.

### Gates finales (medicion canonica limpia sobre arbol 011j)
- NOTA proceso: la corrida previa que parecio "2h" fue una corrida interrumpida + probable suspension del host (status=started, lock stale, PID muerto, wall-clock inflado). NO era regresion de rendimiento. La medicion limpia se relanzo sin procesos huerfanos.
- Suite canonica: last-run.log -> "3027 passed, 20 skipped, 5 deselected in 339.67s (0:05:39)"; last-run.json status=finished exit=0 level=unit args_mode=default_discovery. 0 failed. 3027 = 3026 HEAD + 1 barrera nueva de 011j.
- Validate: errors=0 warnings=0.
- Encoding guard (superficies propias py+md): exit 0. El BOM/mojibake del propio .ps1 es pre-existente en HEAD y .ps1 NO esta en GLOB del guard (no bloquea commit); fuera de scope 011j (deuda separada).
- Diff: scripts/launch_agent_terminals.ps1 (+10/-2), tests/test_launch_agent_terminals_script.py (+30). Dentro de FLT motor.


Manager approved canonical closeout for WOT-2026-011j