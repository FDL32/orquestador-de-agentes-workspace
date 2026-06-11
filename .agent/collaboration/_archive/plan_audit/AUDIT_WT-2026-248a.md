# AUDIT WT-2026-248a - Stabilize .opencode/opencode.json: exact launcher restore and integrity guard in pre-handoff

## Estado
PENDING

## Objetivo de auditoria
Verificar que el ticket elimina el drift recurrente de `.opencode/opencode.json` sin introducir un cleanup silencioso peligroso, manteniendo autoridad clara sobre que cambios pueden autocorregirse y cuales deben bloquearse explicitamente.

## TP Check
- TP-01: verificado - existe un problema real, repetido y evidence-linked en tickets recientes.
- TP-02: verificado - el deliverable es de codigo; la evidencia valida es diff real, tests y validate.
- TP-03: verificado - el mayor riesgo no es tecnico sino de autoridad: borrar cambios legitimos por exceso de automatismo.
- TP-04: verificado - el ticket necesita un contrato explicito de que residuos son launcher-owned y cuales no.
- TP-05: verificado - la barrera debe probar tanto camino feliz como camino de fallo.
- TP-06: verificado - el TP Check no sustituye quality gates ni evidencia de git limpio.

## Fases de revision

### Fase 1 - Reproduccion y causa raiz
- Verificar que el drift inicial esta reproducido o documentado con evidencia equivalente nueva.
- Verificar que la causa raiz queda localizada en la restauracion del launcher y no en un cambio legitimo del archivo.
- Verificar que el ticket no se lanza hasta que `work_plan.md` activo del `repo_destino` se actualice canonicamente a `WT-2026-248a`; el scope gate de `--mark-ready` no lee `PLAN_WT-2026-248a.md`.

### Fase 2 - Capa 1: restauracion del launcher
- Verificar que `scripts/launch_agent_terminals.ps1` restaura `.opencode/opencode.json` de forma byte-exacta o equivalente verificable.
- Verificar que el fix se hace en el bloque `finally` embebido como template string y no en una ruta incidental distinta.
- Verificar que el fix cubre salida exitosa y salida por fallo/abort del Builder, y que el Builder deja en `execution_log.md` la estrategia elegida para validar ese camino, junto con evidencia reproducible real y no solo una descripcion narrativa.
- Verificar que `Set-OpenCodeExternalPermission` no se modifica en esta pasada.
- Verificar que el archivo trackeado no conserva permisos runtime ni rutas absolutas del `repo_destino`.

### Fase 3 - Capa 2: guard de integridad en pre-handoff
- Verificar que la autocorreccion se inserta en el bloque commit-or-block de `_handle_pre_handoff`, antes de la evaluacion de `motor_uncommitted_productive`.
- Verificar que `--pre-handoff` no hace cleanup generico de archivos dirty fuera de FLT.
- Verificar que la deteccion del residuo permitido es determinista por bytes:
  - `bytes_actuales == BOM_UTF8 + bytes_head`
  - donde `BOM_UTF8 = 0xEF 0xBB 0xBF`
- Verificar que cualquier autocorreccion se limita a `.opencode/opencode.json` y a ese residuo exacto, y que la autocorreccion emite un mensaje visible en stderr.
- Verificar que si el diff contiene cualquier cambio semantico adicional o ambiguo, el sistema bloquea en vez de hacer `git checkout` silencioso.

### Fase 4 - No regresion de autoridad
- Verificar que el ticket no convierte `--pre-handoff` en una segunda fuente de verdad sobre configuracion legitima.
- Verificar que si `.opencode/opencode.json` aparece en `Files Likely Touched`, no se aplica autocorreccion especial y gobiernan las reglas normales de scope/evidence.
- Verificar que no se usa `.gitignore` como forma de esconder el problema.
- Verificar que la categoria "runtime-owned" no queda abierta: en `WT-2026-248a` aplica solo a `.opencode/opencode.json` y al residuo BOM exacto descrito.

### Fase 5 - Tests focales
- Verificar pruebas para:
  - drift feliz => diff vacio tras restauracion;
  - drift en camino de fallo => diff vacio tras restauracion;
  - residuo exacto permitido => autocorreccion;
  - cambio semantico adicional => bloqueo.
- Verificar que no hay tests cosmeticos ni mocks drift.

### Fase 6 - Quality gates
- Verificar exit code 0 de:
  - `pytest tests/test_opencode_config_stability.py -v`
  - `ruff check .agent/agent_controller.py tests/test_opencode_config_stability.py`
  - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers
- `work_plan.md` sigue apuntando a otro ticket al lanzar Builder.
- Cualquier solucion que haga `git checkout` generico de `.opencode/opencode.json` sin discriminar el diff exacto.
- Cualquier solucion que pueda borrar cambios legitimos de configuracion sin fallo explicito.
- Falta de cobertura del camino de fallo/abort del launcher, o ausencia en `execution_log.md` de la estrategia elegida para validarlo.
- Persistencia de permisos runtime o rutas del `repo_destino` en el archivo trackeado.
- `git diff HEAD -- .opencode/opencode.json` sigue mostrando drift tras el ciclo.
- Ruff, pytest focal o validate fallan.