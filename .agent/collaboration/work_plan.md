# Plan de Trabajo: WOT-2026-014a

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014a
- **Estado:** APPROVED
- **Titulo:** closeout self-dirty: prepush deja de bloquear por su propio reporte (Opcion A congelada)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014A-001
- **Plan-Link:** PLAN-014A-001
- **Builder clarification budget:** 0 (Opcion A congelada; B y C descartadas)

## Objetivo
Eliminar la circularidad del cierre: que el reporte de cierre (session_close_report.md, tracked) no
haga fallar prepush_check->check_git_tree_clean cuando una corrida previa lo dejo sin commitear,
SIN debilitar el gate pre-push general frente a cambios productivos no esperados.
Verificacion del objetivo (que comando/test lo demuestra): un test de barrera mutation-verified que
reproduce el bloqueo (reporte sucio -> prepush falla SIN el fix) y verifica que CON el fix el reporte
esperado se perdona en la ruta del cierre, mientras un cambio productivo sin commitear SIGUE fallando.

## Premise (VERIFICADO en codigo + en vivo)
- session_closeout.py:115 REPORT_REL = .agent/runtime/memory/session_close_report.md (tracked, se commitea en cada cierre).
- delivery_hygiene_check.py:260 check_git_tree_clean corre git status --porcelain (L271) SIN allowlist -> marca el reporte como arbol sucio (exit 1, bloqueante).
- closeout_steps/rotation.py:389 step_git_clean SI tiene expected_patterns (incluye session_close_report.md, L390) y lo perdona (L398).
La asimetria hace el cierre circular. Premisa falsa descartada: el reporte NO esta gitignored (git ls-files lo confirma tracked).

## Premise Re-check (cwd=repo_motor, solo lectura)
grep -nE "REPORT_REL|check_git_tree_clean|expected_patterns" scripts/session_closeout.py scripts/delivery_hygiene_check.py scripts/closeout_steps/rotation.py
git ls-files .agent/runtime/memory/session_close_report.md
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
Condicion de arranque: check_git_tree_clean sigue sin allowlist; expected_patterns sigue local en step_git_clean.

## Decision Arquitectonica (Opcion A CONGELADA)
- Extraer la allowlist de artefactos runtime esperados del closeout (hoy expected_patterns local en
  step_git_clean) a una CONSTANTE COMPARTIDA importable (hogar: scripts/delivery_hygiene_check.py, p.ej.
  EXPECTED_CLOSEOUT_RUNTIME_ARTIFACTS), y que closeout_steps/rotation.py la importe en vez de redefinirla.
- check_git_tree_clean gana un parametro OPCIONAL de allowlist (p.ej. expected_artifacts: list[str] | None = None).
  Default None == comportamiento ACTUAL (gate pre-push general SIN cambios). El consumidor del CLOSEOUT
  (la invocacion de prepush_check dentro del pipeline de cierre) pasa la constante compartida; los usos
  de check_git_tree_clean FUERA del closeout NO pasan allowlist y quedan IDENTICOS.
- La allowlist solo perdona el match exacto del/los artefacto(s) runtime esperado(s); un cambio
  productivo sin commitear (cualquier otra ruta) SIGUE marcando arbol sucio.
- Opcion B (auto-commit del reporte) y Opcion C (mover a gitignored) quedan DESCARTADAS.

## Plan - secuencia minima fija
1. Confirmar el call-chain exacto: closeout -> prepush_check -> check_git_tree_clean (localizar el call-site
   del closeout que invoca prepush_check, para pasar ahi la allowlist).
2. Extraer la constante compartida; rewire de step_git_clean para importarla.
3. Anadir el parametro opcional a check_git_tree_clean (default = comportamiento general intacto) y pasar la
   constante SOLO desde el contexto del cierre.
4. Barrera mutation-verified + gates + commit productivo con WOT-2026-014a.

## Files Likely Touched (relativos a repo_motor)
- scripts/delivery_hygiene_check.py
- scripts/closeout_steps/rotation.py
- scripts/prepush_check.py
- tests/unit/test_closeout_self_dirty_allowlist.py

Aclaraciones: el call-site exacto del threading (prepush_check vs su invocacion en el closeout) se
confirma en Fase 0; si el threading toca session_closeout.py de forma minima y derivada, es aceptable
declararlo, pero NO se cambia el contrato general de check_git_tree_clean.

## Read/inspect only
- scripts/session_closeout.py
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- El comportamiento DEFAULT de check_git_tree_clean (sin allowlist) usado por el pre-push GENERAL: no se
  toca; debe seguir marcando sucio cualquier cambio no esperado.
- Auto-commit del reporte (Opcion B) y mover el reporte a ruta gitignored (Opcion C): PROHIBIDOS.
- El contrato de prepush_check para usos fuera del closeout: no se altera.
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal
python -m pytest tests/unit/test_closeout_self_dirty_allowlist.py -q
python -m ruff check scripts/delivery_hygiene_check.py scripts/closeout_steps/rotation.py scripts/prepush_check.py tests/unit/test_closeout_self_dirty_allowlist.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO debilitar delivery_hygiene_check para artefactos NO esperados.
- NO tocar el contrato de prepush_check para usos fuera del closeout.
- NO adoptar Opcion B ni C.

## CONTRACT_GAP / STOP
- Si aplicar la allowlist SOLO se puede haciendo que el comportamiento general de check_git_tree_clean
  cambie (no via parametro opt-in), escalar a decision humana (STOP).
- Si el call-chain del closeout no permite pasar la allowlist sin tocar el contrato de prepush_check usado fuera del cierre.
-> emitir CG-WOT-2026-014a.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] BARRERA mutation-verified: un test reproduce el bloqueo (reporte runtime esperado sin commitear ->
  check_git_tree_clean SIN allowlist FALLA); con la allowlist del cierre, ese mismo reporte se perdona.
- [ ] El MISMO test (o uno hermano) confirma que un cambio PRODUCTIVO sin commitear SIGUE marcando sucio
  (la allowlist no se traga trabajo real).
- [ ] check_git_tree_clean SIN allowlist (default) conserva su comportamiento exacto (test que lo fija).
- [ ] expected_patterns vive en una constante compartida importada por step_git_clean (no duplicada).
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD.
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014a), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.
