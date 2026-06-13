# Work Plan: WOT-2026-002a - A2c demo de clone limpio + install --sync sin copias legacy

## Metadata
- **ID:** WOT-2026-002a
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_destino
- **Repo de autoridad:** repo_destino
- **Alias historico:** WOT-AUDIT-A2c
- **Titulo:** Demostrar sobre clone limpio que el destino opera con el motor externo sin las copias legacy
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (validacion sobre clone desechable; no toca arbol productivo del destino ni el motor)
- **Origen:** WOT-AUDIT-A2 / triage_manifest.md (host-extends / motor-provides)

## Objetivo
Demostrar, sobre un clone limpio del destino en una ruta temporal, que tras
simular el estado post-A2d (sin las copias `motor-provides` de
`scripts/`/`skills/`/`agent_system/` + los 7 scripts comunes) el destino sigue
operando usando el motor EXTERNO: `install_agent_system.py --sync` regenera
`motor_destination_link.json`, y las herramientas del motor (`discover_skills`,
`run_pytest_safe`, `agent_controller --validate`) corren contra el clone via
`AGENT_PROJECT_ROOT`. El entregable es un reporte con exit codes reales que
des-riesga WOT-2026-002c (A2d) o, si el installer o una herramienta falla,
documenta la dependencia real.

## Decision Arquitectonica
El demo prueba CAPACIDAD, no solo no-uso. Por eso el clone se "desnuda" de las
copias legacy ANTES de invocar las herramientas, simulando el estado que dejara
A2d. Toda invocacion usa el motor externo (`<MOTOR_ROOT>/scripts/install_agent_system.py`,
`discover_skills.py`, `run_pytest_safe.py` o `<MOTOR_ROOT>/.agent/agent_controller.py`)
con `AGENT_PROJECT_ROOT=<clone>`,
nunca las copias del clone. El clone vive en una ruta temporal desechable: mover
o borrar archivos ahi NO toca el arbol real del destino. El motor permanece
read-only (verificado por snapshot/check).

## Files Likely Touched
- `orchestrator_pipeline/reports/closeout_WOT-2026-002a.md` (reporte del demo, entregable)
- `orchestrator_pipeline/reports/` (artefactos de evidencia del demo: logs/exit codes)
- `.agent/collaboration/execution_log.md` (bitacora)

## Superficies
- **Builder (crea/modifica):** reporte y evidencia bajo `orchestrator_pipeline/reports/`;
  `execution_log.md`. Opera sobre un clone temporal del destino (fuera del arbol real).
- **Read/inspect only:** `triage_manifest.md`, `MANIFEST.workspace`, scripts del motor.
  NO editar el motor. NO editar el arbol legacy real del destino.
- **Manager-only:** review doble adversarial + verificacion de exit codes reales y de
  que el destino real / el motor quedaron intactos.

## Non-goals
- NO eliminar ni mover copias legacy del destino REAL (eso es WOT-2026-002c / A2d).
- NO tocar el motor (read-only; verificado por `check_motor_pristine`).
- NO modificar superficies productivas del destino para "pasar" el demo.
- NO cerrar A2d ni adelantar sus decisiones.

## Criterios binarios de cierre
- [ ] Clone limpio del destino creado en ruta temporal; `git status` del destino REAL
      sin cambios salvo los artefactos nuevos bajo `orchestrator_pipeline/reports/`.
- [ ] En el clone (NO en el destino real), las copias legacy `motor-provides`
      (`scripts/`, `skills/`, `agent_system/`, `tests/`, `.agent/README.md`) retiradas
      para simular post-A2d; queda registro de que se retiro.
- [ ] `install_agent_system.py --sync` del motor externo sobre el clone stripped:
      exit code capturado; si exit 0, `motor_destination_link.json` regenerado/valido.
- [ ] `discover_skills.py` (motor externo, `AGENT_PROJECT_ROOT=<clone>`): exit code
      capturado; las skills del motor resuelven sin las copias del clone.
- [ ] `run_pytest_safe.py` (motor externo, `AGENT_PROJECT_ROOT=<clone>`): exit code
      capturado (coleccion real, no vacua).
- [ ] `agent_controller --validate --project-root <clone>`: exit code + errors/warnings
      capturados.
- [ ] Reporte `closeout_WOT-2026-002a.md` con cada comando exacto y su exit code
      real (no relato); etiqueta de evidencia por claim.
- [ ] `agent_controller --validate --project-root <destino real>` = 0/0 al cerrar.
- [ ] Motor intacto: `check_motor_pristine --check` contra el snapshot = limpio.

## STOP / escalado
1. Si `install --sync` REQUIERE las copias legacy para regenerar el link (falla sin
   ellas): NO forzar. Documentar el fallo con exit code -> cambia el alcance de A2d
   (esas copias serian dependencia del instalador, no vestigios). Marcar el criterio
   afectado como bloqueante y reportar en el cierre.
2. Si una herramienta del motor FALLA contra el clone stripped por buscar una copia
   local concreta: registrar exit code + traza, identificar la copia y marcarla como
   dependencia viva (input directo para la barrera de A2d). No maquillar.
3. Si el demo fuese a mutar el destino REAL o el motor: parar. El clone temporal es la
   unica superficie de escritura ejecutable; el destino real solo recibe el reporte.
4. Si no se puede crear el clone temporal (permiso/espacio): BLOCKED con diagnostico.

## Gates (deliverable_type: mixed; evidencia ejecutable + reporte)
La naturaleza `mixed` se cumple asi: el lado "code" se valida ejecutando installer
y herramientas del motor contra el clone (exit codes reales); el lado documental es
el reporte. Mapeo de gates a trabajo real:
- Demo install: `python <MOTOR_ROOT>/scripts/install_agent_system.py --sync` apuntando al clone (segun --help) -> exit code.
- Demo pytest: `python <MOTOR_ROOT>/scripts/run_pytest_safe.py` con `AGENT_PROJECT_ROOT=<clone>` -> exit code (este ES el gate pytest del ticket, ejercido sobre el clone).
- Demo validate: `python <MOTOR_ROOT>/.agent/agent_controller.py --validate --json --project-root <clone>` -> errors/warnings.
- Demo discovery: `python <MOTOR_ROOT>/scripts/discover_skills.py --json` con `AGENT_PROJECT_ROOT=<clone>` -> exit code.
- Estado destino real: `agent_controller --validate --project-root <destino>` 0/0.
- Integridad motor: `check_motor_pristine --check` vs snapshot.
- Deliverable existence: reporte presente bajo `orchestrator_pipeline/reports/`.
- ruff: N/A (no se toca Python productivo del destino; el entregable es markdown +
  evidencia). Salto auditable.

## Riesgos
- Bajo. El demo opera sobre un clone desechable; el destino real y el motor son
  read-only salvo el reporte. Mitigacion: snapshot del motor + validate del destino
  antes/despues; toda mutacion ejecutable confinada al tmp clone.
- Residual: el demo podria revelar una dependencia real de una copia legacy. Eso NO
  es un fallo del demo: es exactamente la senal que A2d necesita (se documenta y se
  escala, no se oculta).

## Entregables
- `orchestrator_pipeline/reports/closeout_WOT-2026-002a.md`: reporte del demo con
  comandos, exit codes reales, decision (A2d des-riesgado o dependencia detectada),
  y etiquetas de evidencia.
