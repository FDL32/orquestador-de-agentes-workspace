# Work Ticket - WT-2026-228a

## Metadata
- **ID:** WT-2026-228a
- **Title:** Pre-handoff bloquea cambios productivos sin commit en repo_motor
- **Scope:** system/pre-handoff-evidence
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-226a, WT-2026-227a

## Problema
`--pre-handoff` puede dar una senal falsa en entorno multi-root.

Bug 1 verificado en codigo: en Modelo B, `_handle_pre_handoff` elige
`git_root = project_root` cuando el `repo_destino` tiene `.git`. Eso deja fuera
los cambios productivos sin commit del `repo_motor` (`_MOTOR_ROOT`). Resultado:
el Builder puede tener implementacion real en el motor y aun asi recibir una
ruta de cierre que no ve esos archivos.

Bug 2 verificado en codigo: si `--pre-handoff` detecta cambios y los
auto-commitea, usa el mensaje `chore(<ticket>): pre-handoff checkpoint`.
Ese mensaje contiene terminos incluidos en `_CHECKPOINT_KEYWORDS`
(`checkpoint`, `pre-handoff`, `wip`, `interim`), por lo que `--mark-ready`
rechaza despues ese commit como evidencia no significativa.

La correccion correcta es bloquear con mensaje accionable, no auto-commitear.

## Objetivo
Antes de handoff, detectar cambios productivos sin commit en `repo_motor` usando
el seam compartido `bus/evidence.py`. Si existen, bloquear con lista de archivos
y pedir commit manual con el ticket ID. Si no existen cambios productivos sin
commit, `--pre-handoff` no debe asumir responsabilidad del gate de commits:
`--mark-ready` sigue siendo quien bloquea la ausencia de commit del ticket.

Resultados esperados:
1. `repo_motor` con cambios productivos sin commit bloquea `--pre-handoff`.
2. El bloqueo muestra el texto:
   `Uncommitted productive changes in repo_motor: commit with ticket ID before handoff.`
   y lista los archivos productivos.
3. `repo_motor` con cambios solo docs/collaboration no activa esta barrera.
4. `repo_motor` limpio con commit reciente que contiene `WT-2026-228a` pasa
   `--pre-handoff`.
5. `repo_motor` limpio sin commit del ticket tambien pasa `--pre-handoff`; esa
   ausencia queda para `--mark-ready`.
6. `--pre-handoff` no auto-commitea cambios productivos del `repo_motor`.

## Contrato CEM v0
- Contrato antes que fix.
- Evidencia antes que relato.
- Rigor proporcional: toca handoff, evidence seam y flujo multi-root.
- Ninguna afirmacion sin artefacto verificable.
- No crear otro detector paralelo de evidencia productiva.
- Cambios fuera de scope: detenerse, clasificarlos y registrarlos antes de tocar.

## Decision Arquitectonica
- Reutilizar `bus/evidence.py` como unica fuente para separar cambios
  productivos de docs/collaboration.
- No inferir dirty files desde `resolve_evidence()["motor_productive"]`, porque
  ese campo tambien puede incluir archivos de commits recientes.
- Si hace falta, extender `bus/evidence.py` con un campo explicito como
  `motor_uncommitted_productive` construido solo desde `git diff --name-only` y
  `git diff --cached --name-only`.
- La barrera vive en `--pre-handoff`, antes de cualquier commit/tag de
  checkpoint.
- La barrera solo comprueba cambios productivos sin commit en `repo_motor`.
- No convertir `--pre-handoff` en sustituto de `--mark-ready`.
- No auto-commitear cambios del motor con mensajes genericos.

## Decision de implementacion minima
- Confirmar en codigo:
  - `.agent/agent_controller.py:_handle_pre_handoff`;
  - `.agent/agent_controller.py:_MOTOR_ROOT`;
  - `.agent/agent_controller.py:_CHECKPOINT_KEYWORDS`;
  - `bus/evidence.py:resolve_evidence`.
- Insertar el check antes del bloque que calcula `needs_commit` o ejecuta
  `git commit`.
- Usar `bus/evidence.py` para obtener o clasificar un conjunto explicitamente
  uncommitted del motor; no usar `motor_productive` como proxy de dirty files.
- Bloquear solo cuando el conjunto uncommitted productivo del motor contenga
  archivos reales. Los cambios ya presentes en commits recientes del
  ticket no deben confundirse con dirty changes.
- Mantener el comportamiento existente para tag de checkpoint cuando no haya
  cambios productivos sin commit en `repo_motor`.

## Evidencia minima esperada
El cierre debe dejar, con artefactos verificables:
- seam real confirmado en `.agent/agent_controller.py`;
- prueba de bloqueo con `repo_motor` dirty en archivo productivo;
- prueba de no bloqueo con cambios docs/collaboration;
- prueba de paso con `repo_motor` limpio y commit del ticket;
- prueba de paso con `repo_motor` limpio sin commit del ticket;
- prueba de que `--pre-handoff` no crea commit automatico en `repo_motor`;
- salida de tests focales;
- salida de `ruff`;
- `agent_controller.py --validate --json --project-root .` sin errores ni
  warnings.

## Non-goals
- No implementar Manager commit.
- No auto-commitear cambios del `repo_motor`.
- No tocar permisos `external_directory`.
- No recuperar manualmente `WT-2026-227a`.
- No modificar el review packet de `WT-2026-227a`.
- No tocar rounds, locks ni relaunch.
- No relajar `--mark-ready`.

## Fases
### Fase 0: Diagnostico del camino real
- Confirmar que `_handle_pre_handoff` decide `git_root` con `project_root` antes
  que `_MOTOR_ROOT`.
- Confirmar que el commit automatico usa `pre-handoff checkpoint`.
- Confirmar que `_CHECKPOINT_KEYWORDS` rechazaria ese mensaje.
- Confirmar que `resolve_evidence` mezcla fuentes de working tree, staged y
  commits recientes, por lo que el fix necesita un conjunto uncommitted
  explicito.

### Fase 1: Barrera de pre-handoff
- Detectar cambios productivos sin commit en `repo_motor`.
- Bloquear con mensaje accionable y lista de archivos.
- Mantener docs/collaboration fuera de la barrera.
- No ejecutar auto-commit para esos cambios.

### Fase 2: Pruebas
- Usar repos git reales en `tmp_path`; no mockear subprocess de git.
- El test de regresion debe fallar sin el fix y pasar con el fix.
- Verificar la regresion con revert parcial del archivo central pre-fix, ejecutar
  el test esperado en rojo, restaurar y registrar el resultado en
  `execution_log.md`.

## Files Likely Touched
- `.agent/agent_controller.py`
- `bus/evidence.py`
- `tests/test_pre_handoff_guard.py`
- `tests/test_agent_controller.py`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-228a.md`
- `.agent/collaboration/AUDIT_WT-2026-228a.md`
- `.agent/collaboration/execution_log.md`

## Seams confirmados
- `.agent/agent_controller.py:_handle_pre_handoff`: ruta real de
  `--pre-handoff`.
- `.agent/agent_controller.py:_MOTOR_ROOT`: raiz del `repo_motor`.
- `.agent/agent_controller.py:_CHECKPOINT_KEYWORDS`: filtro que rechaza commits
  genericos.
- `bus/evidence.py:resolve_evidence`: seam compartido de evidencia productiva;
  si se extiende, debe exponer dirty files productivos sin mezclar commits.

## Calidad
- Ejecutar tests focales del pre-handoff/evidence.
- Ejecutar al menos un test nuevo que falle sin el fix.
- Ejecutar `ruff check` sobre archivos Python modificados.
- Ejecutar `agent_controller.py --validate --json --project-root .` en el
  `repo_destino` antes de marcar ready.

## TP Check
TP-01: seam real `_handle_pre_handoff` confirmado.
TP-02: `repo_motor` con cambios productivos sin commit bloquea
`--pre-handoff`.
TP-03: el mensaje de bloqueo incluye el texto canonico y la lista de archivos.
TP-04: cambios docs/collaboration-only no activan esta barrera.
TP-05: `repo_motor` limpio con commit del ticket pasa `--pre-handoff`.
TP-06: `repo_motor` limpio sin commit del ticket pasa `--pre-handoff`.
TP-07: `--pre-handoff` no auto-commitea cambios productivos del motor.
TP-08: la implementacion reutiliza `bus/evidence.py` y no usa
`motor_productive` como proxy de uncommitted files.
TP-09: sin scope creep hacia permisos, review packet, relaunch, locks o
`--mark-ready`.
TP-10: un commit reciente del ticket no se interpreta como dirty file.

## Criterio binario de salida
- `agent_controller.py --validate --json --project-root .` devuelve 0 errores y
  0 warnings.
- Existe un test de regresion que falla sin el fix y pasa con el fix.
- Existe un test negativo docs/collaboration-only.
- Existe un test de no auto-commit.
- No se crea un detector paralelo de evidencia productiva.
- No se bloquea un `repo_motor` limpio solo porque tenga commits recientes del
  ticket.
- Los cambios no salen de la whitelist.
