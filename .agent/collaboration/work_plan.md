# Work Ticket - WT-2026-215

## Metadata
- **ID:** WT-2026-215
- **Title:** Gates Modelo B: operaciones git de evidencia/provenance resuelven motor_root
- **Scope:** system/gates-motor-root
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-210 (completado), WT-2026-187 (completado)

## Problema
Varias funciones git de evidencia en `bus/review_bridge.py`, `scripts/prepush_check.py`
y `scripts/session_closeout.py` corren con `cwd=project_root` (el workspace, repo_destino)
en vez de `motor_root` (orquestador_de_agentes, donde viven los commits).

Consecuencia real verificada en sesion actual: el review packet del Manager refleja
artefactos de colaboracion del workspace, no codigo del motor. Cada cierre ha
necesitado un "Scope override" manual para que el Manager no rechazara por diff vacio.

`_resolve_motor_root` y `_resolve_motor_controller` ya migran a `motor_link` (WT-2026-187),
pero las funciones git de evidencia quedaron sin migrar. Es deuda quirurgica con causa
raiz verificada en codigo.

## Objetivo
Hacer que todas las operaciones git de evidencia/provenance del tooling de review y gates
resuelvan `motor_root` via `motor_link`, de forma que el review packet refleje el codigo
real del motor y el Manager no necesite overrides manuales de scope.

Criterio verificable: `check_review_packet_diff_empty` devuelve `False` cuando el Builder
commiteo codigo real en el motor; `python -m pytest tests/test_motor_root_gates.py -v`
pasa; `ruff` limpio; `validate --json` 0/0.

## Contrato CEM v0
- Contrato antes que fix: clasificar cada call site (git-de-codigo vs git-de-estado-workspace)
  antes de tocar.
- Evidencia antes que relato: test con repos git reales (no mocks de git).
- Rigor proporcional: Tier 3 (tooling de review/gates), no Tier 1 (bus core).
- No-cambio-ciego: el principio no es "reemplazar todos los cwd=self.project_root",
  sino corregir exactamente la superficie de evidencia/provenance.

## Decision Arquitectonica
Introducir un helper privado `_motor_root_or_raise()` en `review_bridge.py` que devuelve
`motor_root` resuelto via `_resolve_motor_root()` o lanza excepcion controlada si no hay
link. Todos los call sites de evidencia/provenance lo usan. El helper hace la intencion
explicita y la decision auditable.

En `prepush_check.py` y `session_closeout.py`, separar la operacion git del motor como
check bloqueante (usa `motor_root`) y dejar cualquier informacion del workspace como
informativa (usa `project_root` si aporta algo, o se elimina si es redundante).

El caso ambiguo `_get_untracked_files` (L1096 `review_bridge.py`) se resuelve
explicitamente en `PLAN_WT-2026-215.md` antes de tocar: motor_root si es evidencia de
codigo no commiteado, project_root si son deliverables locales del destino.

## Non-goals
- No tocar cwd de repomix (L483), review transport (L1907, 2011, 3222, 3280) ni
  `_run_script()` de session_closeout.
- No cambiar el contrato de `_resolve_motor_root()` ni de `motor_link.py`.
- No modificar bus/state_machine, supervisor, controller ni relaunch.
- No automatizar la emision de CHANGES ni tocar WT-2026-217.
- No reescribir historico de git.
- No refactorizar funciones mas alla de lo necesario para pasar cwd correcto.

## Fases

### Fase 0: Diagnostico y clasificacion
- Confirmar los call sites exactos (linea por linea) contra el codigo real del motor
  en la sesion de implementacion (el codigo puede haber cambiado desde este plan).
- Confirmar en el codigo real que `_get_untracked_files` mantiene semantica de
  archivos de codigo no commiteados. La decision ya fue registrada por Manager
  en `execution_log.md`: usar `motor_root`. Builder no escribe en
  `.agent/collaboration/`.
- Verificar que no existe ya un helper equivalente en `review_bridge.py`.

### Fase 1: Helper en review_bridge.py
- Introducir `_motor_root_or_raise()` como metodo privado de `ReviewBridge`
  (o nombre equivalente si el contexto lo pide).
- Migrar los call sites de evidencia/provenance clasificados en Fase 0:
  `_git_diff_stat` (L578), `_build_diff_for_files_likely_touched` (L599),
  `_git_provenance` (L985), `_resolve_review_base` y sus ramas (L1014, 1040, 1072, 1096
  segun decision de Fase 0), `_get_current_git_head` (L1444),
  `_compute_changed_files` y diffs (L1495, 1510, 1525).
- Cada funcion del grupo llama `_motor_root_or_raise()` internamente; no se pasa
  `motor_root` como parametro encadenado entre funciones.
- Confirmar que call sites fuera de scope no se tocan.

### Fase 2: prepush_check.py y session_closeout.py
- `prepush_check.py`: migrar `run_git_status_check` (L250 aprox) a motor_root.
- `session_closeout.py`: migrar `_step_git_clean` (L1524 aprox) a motor_root.
- En ambos casos, resolver via `runtime.motor_link.resolve_motor_root(project_root)`
  y usar fallback explicito de warning si no hay link de motor.

### Fase 3: Tests y quality gates
- `tests/test_motor_root_gates.py` (nuevo):
  - workspace no-repo (o repo distinto) + motor con commits reales:
    `check_review_packet_diff_empty` devuelve False.
  - pre-check no emite CHANGES espurio con motor con commits.
  - `prepush_check` / `session_closeout` resuelven motor_root.
  - fallback si no hay link: comportamiento documentado y sin crash.
  - test de regresion: sin el fix, el caso principal falla.
- Ruff limpio en todos los archivos tocados.
- `pip-audit` limpio.
- `validate --json --project-root <repo_destino>` con 0/0.

## Files Likely Touched
- `bus/review_bridge.py`
- `scripts/prepush_check.py`
- `scripts/session_closeout.py`
- `tests/test_motor_root_gates.py`
- `tests/test_manager_review_bridge.py`

## TP Check
TP-01: `_motor_root_or_raise()` (o equivalente) es el seam unico; no se crean ramas
  paralelas de resolucion de motor_root en las funciones de evidencia.
TP-02: con workspace repo y motor repo hermano, `check_review_packet_diff_empty`
  devuelve False si el motor tiene commits reales.
TP-03: la decision Manager sobre `_get_untracked_files` esta documentada en
  `execution_log.md` antes del handoff y el test cubre el caso elegido.
TP-04: `prepush_check.py` y `session_closeout.py` ejecutan git sobre motor_root.
TP-05: call sites fuera de scope (repomix, review transport, `_run_script`) sin cambios.
TP-06: fallback si no hay `motor_destination_link.json`: no crash, comportamiento
  documentado.
TP-07: test de regresion demuestra fallo sin el fix via revert parcial seguro.
TP-08: `ruff` limpio, `validate --json` 0/0.

## Criterio binario de salida
- `git -C C:\Users\fdl\Proyectos_Python\orquestador_de_agentes log --oneline -3`
  contiene commit con `WT-2026-215`.
- `python -m pytest tests/test_motor_root_gates.py -v` -> todos pasan.
- `python -m pytest tests/test_manager_review_bridge.py -q` -> sin regresiones.
- `ruff check bus/review_bridge.py scripts/prepush_check.py scripts/session_closeout.py`
  -> All checks passed.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  -> 0 errores, 0 warnings.
