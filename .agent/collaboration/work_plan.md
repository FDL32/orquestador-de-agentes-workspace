# Plan de Trabajo: WOT-2026-014h

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014h
- **Estado:** APPROVED
- **Titulo:** Extraer la logica viva de scope-verification fuera de scripts/orquestador.py (DEPRECATED)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Baja
- **Depende de:** -
- **Objective-Link:** OBJ-014H-001
- **Plan-Link:** PLAN-014H-001
- **Builder clarification budget:** 0 (consumidores transversales resueltos; shim no necesario)

## Objetivo
Mover la logica VIVA de scope-verification desde scripts/orquestador.py (marcado DEPRECATED y lleno de
adapters Goose/Claw muertos) a un modulo NO-deprecado nuevo scripts/scope_verification.py, y reapuntar el
unico consumidor (tests/test_orquestador_scope.py). Verificacion del objetivo: el test importa del modulo
nuevo y pasa; busqueda transversal confirma 0 consumidores live restantes de esas funciones en orquestador.
Ver DoD.

## Funciones a mover (5, no 4 -- VERIFICADO por busqueda transversal)
El test importa CINCO simbolos de scripts.orquestador, no cuatro: ademas de snapshot_paths,
detect_changed_files, classify_scope y generate_scope_report, importa snapshot_file_info (lineas 40 y 54
de tests/test_orquestador_scope.py). Las 5 se mueven juntas (snapshot_file_info es dependencia de snapshot_paths
y se importa directo en el test).

## Premise (VERIFICADO por busqueda transversal)
- scripts/orquestador.py lleva banner DEPRECATED (L6-8) + adapters Goose/Claw muertos, pero contiene logica
  viva: snapshot_file_info, snapshot_paths, detect_changed_files, classify_scope, generate_scope_report.
- UNICO consumidor LIVE: tests/test_orquestador_scope.py (motor). Ningun codigo de produccion las importa.
- Workspace: solo copias MUERTAS en _backups/ y _legacy/goose_claw_deprecated/ (no importadas por codigo vivo).
- orquestador.py NO esta en MANIFEST.distribute/workspace (no vendorizado a destinos; Extractor no lo tiene).
- => NO se necesita re-export shim (no aparece consumidor live mas alla del test).

## Premise Re-check (cwd=repo_motor, solo lectura)
grep -rnE "from scripts.orquestador import|snapshot_file_info|snapshot_paths|detect_changed_files|classify_scope|generate_scope_report" . --include="*.py" | grep -v "__pycache__"
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
Condicion de arranque: las 5 funciones siguen en scripts/orquestador.py; el unico import live es el test.

## Decision Arquitectonica
- Crear scripts/scope_verification.py (NO deprecado) con las 5 funciones movidas tal cual (sin reescribir logica).
- tests/test_orquestador_scope.py reapunta sus imports: from scripts.orquestador import X -> from scripts.scope_verification import X. Se conserva el nombre del archivo de test (no se renombra; minimiza churn).
- scripts/orquestador.py queda como cascaron Goose/Claw SIN esas 5 funciones; NO se borra; NO se anade shim (busqueda transversal = 0 consumidores live).
- NO se tocan los adapters Goose/Claw ni el banner DEPRECATED.

## Files Likely Touched (relativos a repo_motor)
- scripts/scope_verification.py
- scripts/orquestador.py
- tests/test_orquestador_scope.py

Aclaraciones: mover las 5 funciones (incluyendo helpers internos que solo ellas usan); reapuntar imports del test; no renombrar el test.

## Read/inspect only
- MANIFEST.distribute, MANIFEST.workspace
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- Los adapters Goose/Claw y el banner DEPRECATED de orquestador.py: read-only, no se tocan.
- NO borrar scripts/orquestador.py (retirada total = follow-up posterior).
- El modo --skill de orquestador (delega via subprocess a discover_skills.py): no se toca.
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal
python -m pytest tests/test_orquestador_scope.py -q
python -m ruff check scripts/scope_verification.py scripts/orquestador.py tests/test_orquestador_scope.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO borrar orquestador.py.
- NO tocar adapters Goose/Claw.
- NO renombrar el archivo de test.
- NO anadir shim (busqueda transversal confirma 0 consumidores live; un shim seria codigo muerto).

## CONTRACT_GAP / STOP
- Si al mover las funciones aparece un consumidor live no inventariado (que obligue a un shim).
- Si alguna de las 5 funciones depende de estado/import del cascaron Goose/Claw que no se pueda mover limpio.
-> emitir CG-WOT-2026-014h.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] Las 5 funciones (snapshot_file_info, snapshot_paths, detect_changed_files, classify_scope, generate_scope_report) residen en scripts/scope_verification.py.
- [ ] tests/test_orquestador_scope.py importa esas funciones desde scripts.scope_verification (ya no desde scripts.orquestador) y pasa en verde.
- [ ] BUSQUEDA TRANSVERSAL post-extraccion: ningun consumidor live importa esas funciones desde scripts.orquestador (grep en motor + workspace de dogfooding, excluyendo _backups/_legacy/__pycache__).
- [ ] scripts/orquestador.py ya no define esas 5 funciones; el cascaron Goose/Claw y el banner DEPRECATED quedan intactos.
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD.
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014h), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.
