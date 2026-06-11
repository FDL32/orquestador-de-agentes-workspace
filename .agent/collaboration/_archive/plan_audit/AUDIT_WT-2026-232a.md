# AUDIT_WT-2026-232a

## Tipo
Scope gate / evidence gate / multi-repo closeout. Tier 3.

## Evidencia Minima Requerida
- Commit en `repo_motor` con `WT-2026-232a`.
- Test que reproduce el falso positivo de `WT-2026-231a`: commit motor dentro de FLT
  y `mark-ready` sin override.
- Tests negativos: fuera de FLT y sin evidencia.
- Evidencia de que superficies operativas ya no usan `Modelo B` salvo menciones legacy.
- Evidencia funcional de que el Builder recibe `repo_motor_root`,
  `repo_destino_root` y `workspace_activo_root` como valores efimeros resueltos
  dinamicamente, mientras los artefactos persistentes conservan paths relativos.
- Ruff limpio.
- `validate --json` 0/0 desde `repo_destino`.

## TP Check
TP-01: `mark-ready` con commit real en `repo_motor` dentro de FLT pasa sin
`--scope-override`.
TP-02: commit motor fuera de FLT bloquea con paths motor-relative.
TP-03: ronda sin evidencia productiva sigue bloqueando.
TP-04: FLT motor-aware no se resuelve contra `PROJECT_ROOT`.
TP-05: no se relaja `mark-ready` ni se acepta collaboration-only.
TP-06: `WT-2026-231a` no regresa: `pre-handoff` sigue commiteando y tageando.
TP-07: no se crean tags ni commits en `repo_destino`.
TP-08: referencias operativas a `Modelo B` migradas a `topologia motor/destino`.
TP-09: las tres raices se resuelven con la precedencia documentada y se inyectan
como valores no vacios en prompt/runtime, no como contrato persistente.
TP-10: no queda `WT-2026-232b` ni `WT-2026-209` como deuda diferida viva.

## Blockers Esperados
- CRITICO: resolver el falso positivo usando `--scope-override` automatico o aceptando
  ausencia de evidencia.
- CRITICO: seguir usando `parse_files_likely_touched()` para comparar contra paths de
  `repo_motor`.
- CRITICO: seguir usando `get_changed_files()` como fuente unica cuando `repo_destino`
  tiene `.git`.
- CRITICO: comparar paths absolutos de `repo_destino` contra paths relativos de
  `repo_motor`.
- CRITICO: aceptar como evidencia cualquier commit historico con el ID sin verificar
  el checkpoint `checkpoint/review-<ticket>` de la ronda actual.
- CRITICO: crear una funcion nueva duplicada en vez de reusar `_parse_raw_flt_paths()`.
- CRITICO: modificar `check_scope_gate()` globalmente en vez de insertar rama
  motor-aware localizada en `_handle_mark_ready()`.
- CRITICO: llamar a `resolve_evidence()` para resolver el scope motor-aware o
  modificar `bus/evidence.py`.
- CRITICO: usar fallback legacy cuando existe topologia motor/destino pero el
  checkpoint falta, no es ancestro de `HEAD` o no pertenece al ticket activo.
- ALTO: cambiar `Files Likely Touched` a rutas absolutas locales.
- ALTO: crear tags/checkpoints en `repo_destino`.
- ALTO: tests con mocks de git en vez de repos reales en `tmp_path`.
- ALTO: validar la inyeccion buscando solo el nombre de una variable sin comprobar
  los tres valores resueltos.
- ALTO: permitir que el launcher continue con alguna raiz vacia o hardcodeada.
- ALTO: duplicar en PowerShell la resolucion de raices en vez de consumir
  `--resolve-launcher-roots --json`.
- ALTO: implementar `_resolve_launcher_roots()` en `runtime/motor_link.py` o cualquier
  path fuera de FLT.
- ALTO: dejar `Modelo B` como termino operativo vigente en prompts/launcher/tests.
- ALTO: diferir la portabilidad del arranque Builder a otro ticket.
- MEDIO: mensajes de bloqueo sin lista concreta de paths motor-relative.

## Revision Manager
El Manager debe verificar mecanicamente:
- `git -C <repo_motor> log --oneline -5` contiene commit `WT-2026-232a`.
- `git -C <repo_motor> rev-parse checkpoint/review-WT-2026-232a` apunta al commit
  revisado y este es alcanzable desde `HEAD`.
- `_resolve_launcher_roots()` y `--resolve-launcher-roots --json` producen las mismas
  tres claves y valores para repos temporales.
- `git show --stat <commit>` toca solo FLT declarados o paths justificados.
- `python -m pytest tests/test_mark_ready_motor_scope.py -v` -> exit code 0.
- `python -m pytest tests/test_builder_prompt_context.py -v` -> exit code 0.
- `python -m pytest tests/test_pre_handoff_multirepo.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py -q`
  -> sin regresiones.
- `ruff check .agent/agent_controller.py tests/test_mark_ready_motor_scope.py tests/test_pre_handoff_multirepo.py`
  -> limpio.
- `ruff check tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py tests/test_builder_prompt_context.py`
  -> limpio.
- Parse check de `scripts/launch_agent_terminals.ps1`:
  `pwsh -NoProfile -NonInteractive -Command "$tokens=$null; $errors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path 'scripts/launch_agent_terminals.ps1'), [ref]$tokens, [ref]$errors); if ($errors.Count -gt 0) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }"`
  -> exit code 0, sin errores de sintaxis.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  -> 0/0 desde `repo_destino`.
- No hay nuevo uso obligatorio de `--scope-override` para el caso correcto.
- `PLAN_WT-2026-232b.md` no existe como plan diferido; el alcance esta absorbido por
  `WT-2026-232a`.
