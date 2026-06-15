# Work Plan: WOT-2026-009e

## Metadata

- **ID:** WOT-2026-009e
- **Contract ID:** T-009E-001
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-009b (COMPLETED)
- **Fuente:** stash wip-launcher-builderonly-cleanup (stash@{0} en repo_motor)

## Objetivo

Integrar el switch `$BuilderOnly` en `Stop-ProjectAgentProcesses` del launcher
para que el relanzamiento de Builder mate solo procesos Builder (no supervisor ni
review bridge), y limpie `builder_lock.txt` y `builder_session.json` cuando
corresponde.

Verificacion: dado un relanzamiento con `-LaunchBuilder`, `Stop-ProjectAgentProcesses`
se invoca con `-BuilderOnly` y solo termina procesos que coinciden con patrones
`AGENT_BUILDER_TICKET`, `AGENT_BUILDER_ROUND` u `opencode run --agent builder`.
El supervisor (`ticket_supervisor.py`) y el review bridge (`manager_review_bridge.py`)
no se ven afectados.

## Leccion de proceso (de 009f)

El ultimo commit antes de `--mark-ready` debe ser productivo y referenciar el ticket,
no un commit de checkpoint generico. En 009f, el HEAD del motor quedo en
`chore(WOT-2026-009f): pre-handoff checkpoint` y el Manager tuvo que cerrar con
`--force`. En 009e: el commit productivo va primero, el checkpoint (si existe) no
debe quedar como HEAD al momento del mark-ready.

## Decision Arquitectonica

El cambio vive enteramente en `scripts/launch_agent_terminals.ps1`:

  1. `Stop-ProjectAgentProcesses` gana parametro `[switch]$BuilderOnly`.
     - Si $BuilderOnly: patrones limitados a Builder (AGENT_BUILDER_TICKET,
       AGENT_BUILDER_ROUND, opencode run --agent builder, builder_lock.txt).
     - Si no: patrones completos actuales (supervisor, review bridge, kilo, builder).
     - La funcion ahora devuelve un objeto con ProcessesStopped, BuilderLockRemoved,
       BuilderSessionRemoved en todos los paths (incluyendo el catch de error).

  2. En el bloque `if ($LaunchBuilder)`:
     - Llama `Stop-ProjectAgentProcesses -ProjectRoot $ProjectRoot -BuilderOnly`
       antes de la limpieza de lock legacy existente.
     - Loguea el resumen de cleanup si se cerraron procesos.

  3. No se toca la logica de arranque, liveness check, ni el path `-ResumeBuilder`.

## Non-goals

- No cambiar la semantica funcional fuera del flujo de relanzamiento Builder.
- No tocar `Is-BuilderRunningInProject`, `Remove-StaleLegacyLock` ni el path supervisor.
- No introducir nuevos parametros en el launcher fuera de lo ya en el stash.
- No mezclar con 009f ni 009d.

## Files Likely Touched

### repo_motor
- scripts/launch_agent_terminals.ps1
- prompts/launch_builder.md

## Criterios Binarios

- [ ] `Stop-ProjectAgentProcesses` acepta `[switch]$BuilderOnly`.
- [ ] Con $BuilderOnly: solo mata procesos Builder; no toca supervisor ni review bridge.
- [ ] Sin $BuilderOnly: comportamiento identico al actual (no regresion).
- [ ] La funcion retorna objeto consistente (ProcessesStopped, BuilderLockRemoved,
      BuilderSessionRemoved) en los tres paths: exito normal, catch de error, y BuilderOnly sin procesos.
- [ ] El bloque $LaunchBuilder llama Stop-ProjectAgentProcesses con -BuilderOnly.
- [ ] builder_lock.txt y builder_session.json se limpian solo cuando BuilderOnly y
      ProcessesStopped > 0.
- [ ] ruff check . exit 0.
- [ ] validate destino 0/0 al cerrar.
- [ ] El contrato Builder deja explicito que tickets launcher/PowerShell deben reportar tests focales reales del launcher y no presentar ruff como gate principal si no hubo Python tocado.
- [ ] HEAD del motor al momento de --mark-ready es un commit productivo de 009e,
      no un checkpoint generico.

## STOP conditions

- Si el stash introduce cambios fuera de launch_agent_terminals.ps1: no aplicar;
  abrir ticket separado para esa superficie.
- Si $BuilderOnly mata el supervisor en algun path no cubierto: revertir y
  redisenar el filtro de patrones.
- Si el stash tiene conflictos con HEAD actual del motor: resolver conservando
  la intencion del switch, no forzar merge automatico.

## Forbidden Surfaces

- .agent/collaboration/ del motor (seed neutro).
- privada/ y .env.
- bus/state_machine.py.
- scripts/ticket_supervisor.py.
- Cualquier script fuera de launch_agent_terminals.ps1.
