# Work Ticket - WT-2026-242c

## Metadata
- **ID:** WT-2026-242c
- **Title:** Diagnosticar gap real de detección de Builders huérfanas y endurecer contrato de identidad
- **Scope:** system/orphan-builder-detection
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-242a, WT-2026-242b

## Objetivo
Diagnosticar el gap real de detección de Builders huérfanas en launcher y endurecer el contrato de identidad solo con evidencia confirmada.
El objetivo se considera cumplido cuando:
- `python -m pytest tests/unit/test_launcher_powershell_syntax.py -q` termina en verde.
- `python -m ruff check scripts/diagnose_builder_orphans.py tests/unit/test_launcher_powershell_syntax.py` termina sin errores.
- `python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` devuelve `errors: {}`.

## Contexto verificado
- `Stop-ProjectBuilderProcesses` usa `Win32_Process.CommandLine` con patrones
  `AGENT_BUILDER_TICKET` y `AGENT_BUILDER_ROUND` que son dead code: las env
  vars nunca aparecen en CommandLine.
- WT-2026-242b implemento `STALE_BUILDER_ORPHAN` en `agent_controller.py` para
  contener shells huérfanas en la ruta mark-ready/pre-handoff.
- Este ticket trabaja en el launcher (launcher-side), no en el controller.

## Contrato
- Gap confirmado con evidencia reproducible.
- Limpieza de código muerto en `Stop-ProjectBuilderProcesses`.
- Identidad enriquecida en `builder_lock.txt`: `pid + round + ticket_id + project_root + started_at`.
- Script de diagnóstico `scripts/diagnose_builder_orphans.py`.
- Tests que fijan el contrato de limpieza y diagnóstico.

## Files Likely Touched
- `scripts/launch_agent_terminals.ps1`
- `scripts/diagnose_builder_orphans.py`
- `tests/unit/test_launcher_powershell_syntax.py`

## Non-goals
- No tocar `.agent/agent_controller.py` (WT-2026-242b ya lo modifico).
- No cambiar la lógica de `STALE_BUILDER_ORPHAN` (eso es de WT-2026-242b).
- No añadir kills nuevos en caliente sin confirmar el gap.

## Quality Gates
```powershell
python -m pytest tests/unit/test_launcher_powershell_syntax.py -q
python -m ruff check scripts/diagnose_builder_orphans.py tests/unit/test_launcher_powershell_syntax.py
python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Decision Arquitectonica

**Problema:** `Stop-ProjectBuilderProcesses` usaba patrones `AGENT_BUILDER_TICKET` y
`AGENT_BUILDER_ROUND` contra `Win32_Process.CommandLine`. Las env vars nunca aparecen
en CommandLine, por lo que esos patrones eran dead code.

**Decision:** Eliminar los patrones env-var y confiar exclusivamente en patrones CLI-arg
(`opencode.*run.*--agent\s+builder`). Para compensar la perdida de senyal de identidad,
enriquecer `builder_lock.txt` con `pid + round + ticket_id + project_root + started_at`
como contrato de correlacion entre procesos y tickets.

**Alternativa descartada:** Inyectar env vars en el proceso hijo via `Start-Process -Environment`.
Se descarto porque el PID del lock ya permite correlacion via WMI sin contaminar el
CommandLine, y porque modificar el entorno de lanzamiento tendria efectos secundarios
en la sesion del agente.

**Impacto:** El script `diagnose_builder_orphans.py` usa el lock enriquecido para
detectar gaps (PID en lock pero sin proceso vivo), y `Read-BuilderLockState` en el
launcher parsea el JSON enriquecido manteniendo compatibilidad con formato legacy.
- `tests/unit/test_launcher_powershell_syntax.py`: tests concretos para fijar la limpieza del codigo muerto en `Stop-ProjectBuilderProcesses`, la identidad enriquecida del lock y el contrato del launcher bajo `Set-StrictMode`.
- `scripts/diagnose_builder_orphans.py`: script ejecutable y verificable que materializa el diagnostico del gap `CommandLine` vs env vars con salida reproducible.
- `validate --json`: comprobacion final de que el ajuste documental y operativo no introduce errores estructurales en `repo_destino`.

