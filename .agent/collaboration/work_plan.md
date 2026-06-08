# Work Ticket - WT-2026-237a

## Metadata
- **ID:** WT-2026-237a
- **Title:** Formalizar fixes de motor emergentes del smoke repo-compare
- **Scope:** system/review-closeout-hardening
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-235a, WT-2026-236a

## Objetivo
Absorber de forma canonica los hardenings de `repo_motor` que salieron del smoke
`WT-2026-236a`, de modo que el siguiente review packet de codigo represente un
ticket de motor limpio, con scope explicito, quality gates reales y cierre
reproducible en topologia `repo_motor` + `repo_destino`.

El resultado no es reabrir el smoke documental ni volver a discutir Orca/SOUL.md.
El entregable es codigo y tests de `repo_motor` que conviertan los fixes de
sesion y los gaps residuales del review/closeout en una entrega revisable.

## Contexto verificado
- `WT-2026-236a` cerro como smoke/documentation valido, pero el relanzamiento real
  del Builder/Manager obligo a tocar codigo productivo del `repo_motor`.
- El Manager devolvio `CHANGES` legitimo cuando esos cambios de motor aparecieron
  en el review packet de un ticket documental con `Files Likely Touched`
  incompatibles con codigo.
- Durante la sesion ya se corrigieron rutas criticas del motor:
  closeout de non-code tickets, proyecciones de estado, resolucion del agente
  `manager`, parse NDJSON del bridge y permisos del launcher.
- Quedan huecos de hardening y, principalmente, falta empaquetar cualquier
  cambio dentro de un ticket de codigo limpio con evidencias revisables.

## Problema
Si seguimos mezclando fixes de motor con tickets documentales, el review loop hace
lo correcto al rechazar por scope, packaging o ausencia de gates de codigo.
Eso deja al sistema en un falso limbo: el hotfix existe en `main`, pero no queda
explicado ni auditado como entrega canonica del motor.

Este ticket debe convertir esa deuda de sesion en trabajo deliberado: declarar
el scope exacto del `repo_motor`, cerrar los gaps de codigo que sigan abiertos y
dejar una evidencia de quality gates que el Manager pueda revisar sin arrastrar
artefactos del smoke.

## Contrato
- El ticket es `code`: cualquier cierre debe tener diff productivo en
  `repo_motor`, commit referenciado con el ticket exacto y gates de codigo reales.
- El scope principal son review bridge, closeout, proyecciones de estado y
  launcher portable. No reabrir investigacion repo-compare ni producto Orca.
- Si algun fix ya esta correcto en `main`, no reimplementar por deporte: solo
  tocarlo si falta regression coverage, sigue teniendo un gap residual o necesita
  ajuste minimo para cumplir el contrato final del ticket.
- `WT-2026-236a` permanece como smoke/documentation ya cerrado; este ticket no
  debe reescribir su reporte ni su historico, solo referenciarlo.

## Decision Arquitectonica
El sistema necesita separar dos planos:

- tickets `documentation/research`, donde el gate canonico es artefacto +
  validate + review de contenido;
- tickets `code`, donde el gate canonico es diff productivo + tests/gates +
  review packet revisable.

`WT-2026-237a` existe para restaurar esa separacion. La implementacion no debe
inventar nuevas capacidades de producto; debe cerrar el contrato operativo que
permite a Builder, Supervisor y Manager sobrevivir a tickets documentales y de
codigo sin drift ni falsos negativos de transporte.

## Memoria aplicable
- `CL-10 auditor-skeptic-review`: cada fix debe verificarse en codigo real y con
  tests que reproduzcan el runtime, no solo por revision de texto.
- `CL-18 scope-gate-path-format`: los paths bajo `repo_motor` se listan relativos
  al root del motor, sin prefijo `orquestador_de_agentes/`.
- `CL-19 dual-contract-sync`: cualquier ajuste de paths, fases, TPs o criterios
  debe replicarse en `work_plan.md` y `PLAN_WT-2026-237a.md`.
- `obs-ps1-strictmode-dynamic-props`: scripts PowerShell con `ConvertFrom-Json`
  requieren test funcional bajo `Set-StrictMode`, no solo parseo.
- `obs-code-ticket-prehandoff-packaging`: para tickets `code`/`mixed`, el
  preflight debe cubrir FLT completo, arbol limpio antes de `--pre-handoff`,
  gates reales y commit evidence con ticket exacto.
- `review-decision-provenance-contract`: la decision del Manager debe venir de
  fuente autoritativa y cualquier degradacion de transporte debe quedar trazable.

## Non-goals
- No reabrir `WT-2026-236a` ni modificar su reporte repo-compare.
- No implementar nueva funcionalidad de producto inspirada por Orca.
- No redisenar toda la arquitectura del bus ni absorber backlog ajeno como
  `WT-2026-213` salvo evidencia nueva bloqueante.
- No introducir dependencias nuevas ni cambiar credenciales/OpenCode auth UX
  salvo que un test o el runtime actual demuestren un blocker directo.

## Fases

### Fase 0 - Preflight canonico de ticket code
- Confirmar que `WT-2026-236a` esta cerrado y que el ticket activo pasa a ser
  `WT-2026-237a`.
- Verificar arbol limpio en `repo_motor` antes de Builder y registrar cualquier
  mutacion runtime esperada de `.opencode/opencode.json`.
- Leer `PLAN_WT-2026-235a.md`, `PLAN_WT-2026-236a.md` y feedback relevante para
  delimitar exactamente que gaps ya fueron corregidos y cuales quedan abiertos.
- Confirmar que `Files Likely Touched` cubre codigo, tests y wrappers esperados.

### Fase 1 - Consolidacion del scope real
- Revisar en `repo_motor` las superficies que la sesion ya toco:
  `bus/review_bridge.py`, `.agent/agent_controller.py`,
  `scripts/state_projection_sync.py`, `scripts/state_projection_probe.py`,
  `scripts/launch_agent_terminals.ps1` y sus tests.
- Marcar cuales comportamientos ya estan correctos y solo requieren evidencia,
  y cuales aun necesitan ajuste de codigo para cerrar el contrato completo.

### Fase 2 - Hardening residual
- Implementar solo los gaps que sigan abiertos tras Fase 1, con preferencia por:
  clasificacion de fallos de transporte/autenticacion,
  timing de restauracion de `.opencode/opencode.json`,
  gates de closeout para tickets `documentation`/`research` y
  tests funcionales de launcher bajo restricciones reales.
- Si un gap pertenece mejor a otro ticket existente del backlog, documentarlo y
  dejarlo fuera explicitamente en vez de absorberlo por inercia.

### Fase 3 - Tests y gates
- Asegurar regression coverage focal para cada cambio nuevo o endurecido.
- Ejecutar `pytest` focal y `ruff` sobre las superficies del ticket.
- Registrar evidencia exacta de gates en `execution_log.md` con exit code real.

### Fase 4 - Packaging y closeout
- Preparar un review packet donde cada cambio del diff productivo pertenezca al scope de
  este ticket y no arrastre runtime del smoke.
- Verificar `--pre-handoff`, `--mark-ready` y `--validate` en la ruta canonica
  del `repo_motor`.

## Files Likely Touched

### repo_motor - Builder
- `bus/review_bridge.py`
- `.agent/agent_controller.py`
- `scripts/state_projection_sync.py`
- `scripts/state_projection_probe.py`
- `scripts/launch_agent_terminals.ps1`
- `tests/test_manager_review_bridge.py`
- `tests/test_agent_controller.py`
- `tests/test_launch_agent_terminals_script.py`

### repo_destino - Manager only / estado canonico
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-237a.md`
- `.agent/collaboration/AUDIT_WT-2026-237a.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

### repo_motor - Read/inspect only si no se tocan
- `.opencode/agents/manager.md`
- `tests/test_state_projection_probe.py`
- `tests/test_state_projection_sync.py`
- `tests/unit/test_closeout_failures.py`

## Superficies prohibidas para Builder
- No reabrir artefactos de `WT-2026-236a` salvo lectura.
- No tocar `bus/supervisor.py` ni `bus/event_bus.py` sin evidencia nueva.
- No tocar `privada/`.
- No introducir dependencias nuevas.
- No escribir memoria persistente sin propuesta humana explicita.

## Tests Esperados
- **Tests nuevos o reforzados esperados:**
  - `tests/test_manager_review_bridge.py`
  - `tests/test_agent_controller.py`
  - `tests/test_launch_agent_terminals_script.py`
- **Checks de no-regresion:**
  - `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py -q`
  - `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check bus/review_bridge.py .agent/agent_controller.py scripts/state_projection_sync.py scripts/state_projection_probe.py tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py`
  - `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
- **Checks funcionales:** si se toca `scripts/launch_agent_terminals.ps1`, debe
  existir prueba funcional bajo `Set-StrictMode -Version Latest` con fixture JSON
  realista.

## Quality Gates ejecutables
```powershell
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py -q
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check bus/review_bridge.py .agent/agent_controller.py scripts/state_projection_sync.py scripts/state_projection_probe.py tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

Si el ticket termina sin diff productivo en `repo_motor`, no debe cerrarse como
ticket `code`: hay que documentar el motivo y reencuadrar el alcance.

## Packaging y handoff
- `execution_log.md` debe registrar gates de codigo con exit code real.
- El commit final debe referenciar exactamente `WT-2026-237a`.
- `--pre-handoff` debe ver arbol limpio en `repo_motor`, sin drift transitorio de
  `.opencode/opencode.json` en el momento del closeout.
- El review packet debe mostrar diff revisable del `repo_motor`, no solo runtime
  del `repo_destino`.

## Criterios de aceptacion
- Cualquier cambio nuevo del `repo_motor` queda dentro de `Files Likely Touched`.
- El review/closeout del motor no vuelve a fallar por clasificacion de transporte,
  proyeccion stale o contrato incorrecto para tickets no-code.
- Si se toca launcher PowerShell, el comportamiento queda cubierto por test
  funcional bajo entorno comparable al real.
- `pytest`, `ruff` y `--validate` pasan con rutas reales del ticket.
- El review packet ya no mezcla fixes de motor con un ticket documental.
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
  pasa sin drift nuevo o deja blocker exacto documentado con evidencia.

## TP Check
TP-01: leer codigo real de `bus/review_bridge.py`, `.agent/agent_controller.py`,
`scripts/state_projection_sync.py`, `scripts/state_projection_probe.py` y
`scripts/launch_agent_terminals.ps1` antes de proponer cambios adicionales.
TP-02: `Files Likely Touched` cubre codigo, tests y wrappers que Builder tocara.
TP-03: cualquier gap residual se demuestra con test o con evidencia directa de
runtime, no solo con narrativa de sesion.
TP-04: el cierre registra `pytest`, `ruff` y `validate` con exit code real.
TP-05: el commit final referencia `WT-2026-237a` exacto.
TP-06: `WT-2026-236a` no se reabre ni se contamina con nuevos cambios de motor.
TP-07: el ticket termina con review packet revisable o con blocker exacto de
closeout.
