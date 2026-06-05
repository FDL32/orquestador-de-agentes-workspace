# Work Ticket - WT-2026-231a

## Metadata
- **ID:** WT-2026-231a
- **Title:** Pre-handoff commitea repo_motor en Modelo B con scope FLT
- **Scope:** system/pre-handoff-commit
- **Priority:** Alta
- **Estado:** APPROVED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-228a (completado), WT-2026-215 (completado)

## Problema
En Modelo B, el codigo productivo vive en `repo_motor`, pero el cierre canonico exige
un commit visible con el ID del ticket antes de `mark-ready`. El flujo actual ha
fallado repetidamente porque el Builder puede implementar, pero el harness no genera
de forma determinista el commit del motor.

El guard de WT-2026-228a detecta motor sucio y bloquea, pero no convierte ese estado
en la decision correcta commit-o-bloquea. El resultado recurrente es `mark-ready`
bloqueado por `No commit evidence`, incluso cuando hay trabajo productivo real.

## Objetivo
Reestructurar `--pre-handoff` para que, en Modelo B:
- detecte cambios productivos del `repo_motor`;
- compare esos cambios contra `Files Likely Touched` con paths normalizados;
- commitee automaticamente en `repo_motor` si todo esta dentro de scope;
- bloquee con lista exacta si hay productivo fuera de scope;
- mantenga el bloqueo de `no implementation evidence` en rondas vacias;
- cree/refresque `checkpoint/review-<ticket>` en `repo_motor`.

Este ticket no relaja `mark-ready`: lo alimenta con el commit real que hoy falta.

## Contrato CEM v0
- Contrato antes que fix: `mark-ready` sigue exigiendo commit real; el cambio vive aguas
  arriba en `pre-handoff`.
- Evidencia antes que relato: tests con repos git reales en `tmp_path`, no mocks de git.
- Rigor proporcional: commit automatico solo para cambios productivos dentro de FLT.
- Root/topologia antes de ejecucion: git de entrega productiva corre en `repo_motor`,
  no en `repo_destino`.

## Decision Arquitectonica
Convertir el guard de motor sucio en una decision determinista:
- motor sucio dentro de FLT -> `git add` + `git commit` en `repo_motor`;
- motor sucio fuera de FLT -> bloqueo con paths exactos;
- sin productivo -> mantiene bloqueo de evidencia.

No se crea tag en `repo_destino`. El tag load-bearing es el de `repo_motor`, porque ahi
vive la entrega revisable. El estado operativo del destino sigue gobernado por bus y
markdowns canonicos.

## Non-goals
- No crear tag en `repo_destino`.
- No relajar `mark-ready`.
- No cambiar el contrato de `Files Likely Touched`.
- No dar permisos extra al Builder.
- No cambiar review Manager.
- No mezclar con `WT-2026-230a`.

## Fases

### Fase 0: Diagnostico en codigo real
- Confirmar en `.agent/agent_controller.py` el orden actual de:
  - guard de motor sucio de WT-2026-228a;
  - logica de commit/pre-handoff;
  - creacion/refresco de `checkpoint/review-<ticket>`.
- Confirmar como se leen hoy `Files Likely Touched`.
- Confirmar como se detectan cambios productivos del motor.
- Confirmar que la logica actual no debe tocar `repo_destino` para el commit productivo.

### Fase 1: Commit-o-bloquea en repo_motor
- Resolver `motor_root`.
- Obtener cambios productivos del motor.
- Normalizar FLT y paths git a `motor-relative` con `/`.
- Si todos los cambios productivos estan dentro de FLT:
  - hacer `git add <paths>` con `cwd=motor_root`;
  - hacer `git commit` con mensaje que incluya `WT-2026-231a`;
  - crear/refrescar `checkpoint/review-<ticket>` en `repo_motor`.
- Si hay cambios fuera de FLT:
  - no commitear;
  - bloquear con lista exacta de paths.
- Si no hay cambios productivos:
  - mantener bloqueo de `no implementation evidence`.

### Fase 2: Hooks que modifican staged files
- Manejar el caso en que un hook/formatter modifica un archivo staged:
  - intento 1: add + commit;
  - si falla y quedan cambios dentro de FLT, re-add solo esos paths;
  - intento 2: commit;
  - si vuelve a fallar, bloquear con stdout/stderr claro;
  - nunca re-add fuera de FLT.

### Fase 3: Tests y quality gates
- Crear o ajustar tests multi-repo con repos git reales.
- Cubrir normalizacion de paths.
- Cubrir retry por hook que modifica staged files.
- Verificar que `mark-ready` no se relaja.

## Files Likely Touched
- `.agent/agent_controller.py`
- `tests/test_agent_controller.py`
- `tests/test_pre_handoff_guard.py`
- `tests/test_pre_handoff_multirepo.py`

## Builder Access Surface

### Puede leer/escribir
- `.agent/agent_controller.py`
- `tests/test_agent_controller.py`
- `tests/test_pre_handoff_guard.py`
- `tests/test_pre_handoff_multirepo.py`

### No puede leer/escribir
- Ningun path real bajo `repo_destino` / `workspace_activo`.
- `.agent/collaboration/**` del destino.
- `.agent/runtime/**` del destino.
- `.agent/config/**` del destino.
- `backlog.md`.

### Si necesita datos del destino
- Crear fixtures temporales con `tmp_path`.
- Leer el codigo del motor que genera esos artefactos.

## TP Check
TP-01: el guard de motor sucio ya no hace `return 1` antes de evaluar commit-o-bloquea.
TP-02: cambios productivos dentro de FLT generan commit en `repo_motor` con ID del ticket.
TP-03: cambios productivos fuera de FLT bloquean con lista exacta y no commitean.
TP-04: ronda vacia sin productivo mantiene bloqueo de `no implementation evidence`.
TP-05: `checkpoint/review-<ticket>` apunta al commit de entrega en `repo_motor`.
TP-06: paths FLT y paths de git se normalizan a `motor-relative` con `/`.
TP-07: hook/formatter que modifica staged files provoca re-add solo de paths en scope
  y segundo commit, o bloqueo claro si falla de nuevo.
TP-08: no se crea tag en `repo_destino`.
TP-09: `mark-ready` mantiene su gate actual y pasa solo porque existe commit real.

## Criterio binario de salida
- Existe commit en `repo_motor` con `WT-2026-231a`.
- `python -m pytest tests/test_pre_handoff_multirepo.py -v` -> todos pasan.
- `python -m pytest tests/test_pre_handoff_guard.py tests/test_agent_controller.py -q`
  -> sin regresiones.
- `ruff check .agent/agent_controller.py tests/test_pre_handoff_guard.py tests/test_pre_handoff_multirepo.py`
  -> limpio.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  (Manager gate: ejecutar desde `repo_destino`, no desde `repo_motor`)
  -> 0 errores, 0 warnings.
