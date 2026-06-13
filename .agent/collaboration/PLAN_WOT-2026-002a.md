# PLAN WOT-2026-002a - Demo de clone limpio post-A2d (host-extends)

## Objetivo
Espejo tecnico de `work_plan.md`. Probar con evidencia ejecutable que un clone del
destino, despojado de las copias `motor-provides`, sigue operando mediante el motor
externo. Entregable: reporte con exit codes reales.

## Pasos de ejecucion
1. Preparacion (read-only sobre el destino real):
   - Confirmar `MOTOR_ROOT` y `AGENT_PROJECT_ROOT`.
   - `git -C <destino> status --short` (baseline; debe quedar igual salvo reportes).
   - Capturar snapshot del motor ya existe (`motor_before_WOT-2026-002a.json`).
2. Clone temporal:
   - `git clone <destino> <TMP>/clone_002a` (clone local, desechable).
   - Verificar que el clone trae las copias legacy (estado pre-A2d).
3. Inspeccionar el instalador antes de invocarlo:
   - `python <MOTOR_ROOT>/scripts/install_agent_system.py --help` para confirmar como
     se apunta al destino (target/cwd/flag) y que hace `--sync`.
4. Simular post-A2d en el CLONE (no en el destino real):
   - Mover a `<TMP>/clone_002a/_stripped/` (o `git rm` en el clone) las copias
     `motor-provides`: `scripts/`, `skills/`, `agent_system/`, `tests/`,
     `.agent/README.md`. Registrar exactamente que se retiro.
   - NO retirar `.agent/collaboration|runtime|config|audits|docs` (estado del destino).
5. Ejecutar el motor externo contra el clone stripped, capturando exit codes:
   - install: `python <MOTOR_ROOT>/scripts/install_agent_system.py --sync` apuntando
     al clone (segun --help). Capturar exit code + si regenera
     `motor_destination_link.json`.
   - discovery: `AGENT_PROJECT_ROOT=<clone>` + `python <MOTOR_ROOT>/scripts/discover_skills.py --json`.
   - pytest: `AGENT_PROJECT_ROOT=<clone>` + `python <MOTOR_ROOT>/scripts/run_pytest_safe.py`
     (desde `cwd=<clone>`).
   - validate: `python <MOTOR_ROOT>/.agent/agent_controller.py --validate --json --project-root <clone>`.
6. Redactar `orchestrator_pipeline/reports/closeout_WOT-2026-002a.md` con la tabla de
   comandos/exit codes y la decision (des-riesga A2d / dependencia detectada).
7. Cierre:
   - `agent_controller --validate --project-root <destino real>` 0/0.
   - `check_motor_pristine --check` vs snapshot = limpio.
   - `check_encoding_guard.py` sobre el reporte.
   - Commit del reporte en el repo_destino (mensaje incluye `WOT-2026-002a`).
   - `--pre-handoff` y `--mark-ready` (delivery_authority=repo_destino -> M3 en destino).

## Seams / invariantes
- El motor es la fuente de tooling; el clone solo provee estado via `AGENT_PROJECT_ROOT`.
- Algunos scripts del motor no exponen `--project-root` (discover_skills, run_pytest_safe,
  local_audit): se invocan desde `cwd=<clone>` con `AGENT_PROJECT_ROOT=<clone>`.
- El clone es desechable: cualquier `git rm`/move ahi es seguro y reversible.
- El destino real solo recibe el reporte; el motor permanece intacto.

## Evidencia esperada
- exit codes reales de install/discovery/pytest/validate contra el clone stripped.
- `motor_destination_link.json` regenerado en el clone (si install soporta el caso).
- validate del destino real 0/0.
- `check_motor_pristine --check` limpio.

## STOP
- install --sync falla sin las copias legacy -> documentar exit code; cambia alcance A2d.
- una herramienta del motor exige una copia local concreta -> registrar cual; input de A2d.
- imposibilidad de clonar (permiso/espacio) -> BLOCKED con diagnostico.
- No tocar el destino real (salvo reporte) ni el motor.
