# AUDIT WT-2026-249a - Hardening minimo del contrato CLI: stderr vs returncode

## Estado
PENDING

## Objetivo de auditoria
Verificar que el ticket corrige dos inconsistencias concretas del contrato CLI
sin degradar el diagnostico legitimo ni abrir un refactor global no planificado.

## TP Check
- TP-01: verificado - existe un problema real de contrato observable, no solo
  una preferencia de estilo.
- TP-02: verificado - el deliverable es de codigo; la evidencia valida es diff,
  tests de contrato y validate.
- TP-03: verificado - el principal riesgo es scope creep: querer arreglar todo
  `stderr` del controlador en un solo ticket.
- TP-04: verificado - hay que separar `stderr + returncode 1` (valido) de
  `stderr + returncode 0` (inconsistente).
- TP-05: verificado - el wrapper de subproceso debe clasificar por
  `returncode`, no por texto.
- TP-06: verificado - el TP Check no sustituye quality gates ni evidencia de
  commit visible.

## Fases de revision

### Fase 1 - Confirmacion del problema real
- Verificar que el commit `eacde60` no toca controller ni introduce la deuda.
- Verificar en codigo que el caso stale orphan hoy retorna `0` y escribe a
  `stderr`.
- Verificar en codigo que el wrapper de `session close` hoy reenvia
  `result.stderr` sin discriminar `result.returncode`.

### Fase 2 - Fix 1: stale orphan
- Verificar que la rama stale orphan deja de escribir a `stderr` cuando retorna
  `0`.
- Verificar el destino exacto del warning tras el fix:
  - si `json_output=False`: warning visible en `stdout`;
  - si `json_output=True`: sin warning textual libre; salida limpia con `exit 0`.
- Verificar que el comportamiento semantico del comando no cambia: sigue
  saliendo limpio, no emite `HANDOFF_BLOCKED` y no contamina el bus.
- Verificar que no se rompe la via real de error cuando el stale round si debe
  bloquear.

### Fase 3 - Fix 2: wrapper de session close
- Verificar que el wrapper usa `result.returncode` como clasificador.
- Verificar que con `returncode == 0` no reenvia `stderr` como error del padre.
- Verificar que con `returncode != 0` sigue reenviando `stderr`.
- Verificar que no se introduce parseo heuristico de texto.

### Fase 4 - No regresion de alcance
- Verificar que el ticket no intenta reescribir todo el contrato CLI del
  controlador.
- Verificar que no se tocan rutas `stderr + returncode 1` ajenas al problema
  salvo evidencia adicional fuerte.
- Verificar que no aparecen helpers globales `_emit_cli_*` ni refactor amplio
  fuera de scope.

### Fase 5 - Tests focales
- Verificar tests para:
  - barrera de regresion explicita del contrato roto previo en stale orphan;
  - stale orphan => `returncode 0`, `stderr` vacio;
  - session close exitoso => `stderr` no propagado;
  - session close fallido => `stderr` propagado.
- Verificar que el test del wrapper distingue padre e hijo y no es cosmetico.
- Verificar que `tests/test_agent_controller.py` completo sigue verde tras el
  fix, no solo los tests nuevos.

### Fase 6 - Quality gates
- Verificar exit code 0 de:
  - `pytest tests/test_agent_controller.py -v`
  - `ruff check .agent/agent_controller.py tests/test_agent_controller.py`
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers
- El stale orphan sigue devolviendo `0` con escritura a `stderr`.
- El stale orphan retorna `0` pero sigue emitiendo `HANDOFF_BLOCKED` o cualquier
  otro evento al bus.
- No existe barrera de regresion explicita para el contrato roto previo.
- El fix rompe `tests/test_agent_controller.py` fuera de los tests nuevos.
- El wrapper de session close sigue reenviando `stderr` del hijo cuando el hijo
  retorna `0`.
- El fix depende de parsear texto libre en vez de `returncode`.
- El ticket deriva hacia un refactor general del controlador fuera de FLT.
- Faltan tests de contrato observables o son cosmeticos.
- Ruff, pytest focal o validate fallan.
