# Execution Log: WOT-2026-009e - Launcher Builder relaunch cleanup $BuilderOnly

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-009e
- **Contract ID:** T-009E-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD al inicio: a5c2d94 (pre-handoff checkpoint de 009f)
- Destino HEAD: 59d962b
- Validate previo: 0/0 (post-009f close)
- Fuente del cambio: stash@{0} wip-launcher-builderonly-cleanup (aplicado sin conflictos)

## Leccion de proceso (de 009f)

En 009f el HEAD quedo en un commit de checkpoint generico al mark-ready.
En 009e: el commit productivo cf12068 es el HEAD antes del mark-ready. Correcto.

## Implementacion

### Cambios aplicados

1. **scripts/launch_agent_terminals.ps1** (unico archivo del FLT):

   `Stop-ProjectAgentProcesses` gana `[switch]$BuilderOnly`:
   - Con $BuilderOnly: patrones limitados a AGENT_BUILDER_TICKET,
     AGENT_BUILDER_ROUND, opencode run --agent builder, builder_lock.txt.
     Supervisor y review bridge no afectados.
   - Sin $BuilderOnly: patrones originales (supervisor, review bridge, kilo)
     mas los nuevos de Builder -- extension correcta, no regresion.

   Funcion ahora retorna objeto consistente en los tres paths:
   - exito normal: ProcessesStopped, BuilderLockRemoved, BuilderSessionRemoved
   - catch de error: objeto con zeros/false (antes: return vacio)
   - BuilderOnly sin procesos: objeto con zeros/false

   Limpieza de builder_lock.txt y builder_session.json: solo cuando
   BuilderOnly=true y ProcessesStopped > 0.

   Bloque $LaunchBuilder: llama Stop-ProjectAgentProcesses con -BuilderOnly
   antes de la limpieza de lock legacy existente.

### Gates finales (evidencia literal)

**ruff:**
  Comando: python -m ruff check .
  Resultado: All checks passed! exit 0 (2026-06-15)

**Stash aplicado sin conflictos:**
  git stash pop stash@{0}
  Resultado: 1 file changed, 59 insertions(+), 8 deletions(-), no conflicts

**Commit productivo:**
  cf12068 feat(WOT-2026-009e): add $BuilderOnly switch to Stop-ProjectAgentProcesses
  Motor HEAD al mark-ready: cf12068 (no checkpoint generico -- leccion de 009f aplicada)

**Pre-handoff:**
  python .agent/agent_controller.py --pre-handoff --ticket WOT-2026-009e
  Resultado: [OK] Tree is clean.


Manager approved canonical closeout for WOT-2026-009e