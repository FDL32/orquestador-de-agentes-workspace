# Plan de Trabajo: WOT-2026-014f

> Fuente canonica unica del ticket (packet oficial). El backlog REFERENCIA este archivo.

## Metadata
- **ID:** WOT-2026-014f
- **Estado:** COMPLETED
- **Titulo:** Unificar helpers de descubrimiento/parseo de manager_feedback en un modulo canonico
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014F-001
- **Plan-Link:** PLAN-014F-001
- **Builder clarification budget:** 0 (firma canonica, modulo canonico, FLT y barrera ya fijados)

## Objetivo
Extraer las definiciones REALES de descubrimiento y parseo de manager_feedback a UN modulo neutro
e importable nuevo (scripts/manager_feedback_helpers.py) y que los tres consumidores
(scripts/archive_collaboration_artifacts.py, scripts/closeout_steps/archival.py,
scripts/session_closeout.py) consuman esa unica definicion canonica. Conservar wrappers delgados
de compatibilidad donde haya que preservar una firma publica existente, sin introducir una tercera
implementacion real.

Verificacion del objetivo (que comando/test lo demuestra): el test de arquitectura AST (exactamente 1 implementacion real por helper, en scripts/manager_feedback_helpers.py) y la barrera import-identity de tests/unit/test_manager_feedback_helpers.py; ver DoD para los exit-codes exactos.

## Premise (VERIFICADO en codigo)
2 implementaciones reales + 1 wrapper (la premisa "3 copias" quedo stale):
- archive_collaboration_artifacts.py:248 find_manager_feedback_files(collaboration_dir) y
  :268 extract_ticket_id_from_feedback(filename: str) -> CLI/base, firma sin pattern.
- closeout_steps/archival.py:211 _find_manager_feedback_files(...) y :228
  _extract_ticket_id_from_feedback(filename, *, ticket_id_pattern: str) -> copia real del closeout.
- session_closeout.py:489-499 YA delega (wrappers de compatibilidad a _archival_*).
Las dos firmas reales difieren: (filename) vs (filename, *, ticket_id_pattern).

## Premise Re-check (cwd=repo_motor, solo lectura)
rg -n "find_manager_feedback_files|extract_ticket_id_from_feedback" scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
Condicion de arranque: 2 firmas reales aun divergentes; session_closeout sigue delegando; NO existe
aun scripts/manager_feedback_helpers.py. Si no reproduce, PARA y documenta drift.

## Decision Arquitectonica
- Firma canonica = la del closeout:
  extract_ticket_id_from_feedback(filename: str, *, ticket_id_pattern: str) -> str | None
  y find_manager_feedback_files(collaboration_dir: Path) -> list[Path].
- Hogar canonico = NUEVO modulo neutro scripts/manager_feedback_helpers.py
  (NO session_closeout.py, NO archival.py como canonico final implicito).
- Los 3 consumidores importan de ahi:
  - archive_collaboration_artifacts.py: conserva su API publica extract_ticket_id_from_feedback(filename)
    como WRAPPER delgado que llama al canonico con ticket_id_pattern=TICKET_ID_PATTERN
    (preserva callers/tests existentes); find_manager_feedback_files reexporta/wrappea el canonico.
  - closeout_steps/archival.py: _find_manager_feedback_files / _extract_ticket_id_from_feedback
    pasan a importar el canonico, sin cuerpo logico propio.
  - session_closeout.py: sus wrappers de compatibilidad repuntan al canonico, sin reintroducir logica.
- Path | None y el comportamiento observable se conservan.

## Files Likely Touched (relativos a repo_motor)
- scripts/manager_feedback_helpers.py
- scripts/archive_collaboration_artifacts.py
- scripts/closeout_steps/archival.py
- scripts/session_closeout.py
- tests/unit/test_manager_feedback_helpers.py

Aclaraciones: ajustar tests existentes que importan de archive_collaboration_artifacts solo si el
rewire lo exige; no abrir una suite paralela redundante.

## Read/inspect only
- bus/ticket_id.py (TICKET_ID_PATTERN)
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\AUDIT_WOT-2026-014f.md

## Forbidden Surfaces
- Politica de SELECCION de tickets: _can_prove_close (bus events) del closeout y la lista ticket_ids
  del CLI quedan separadas y read-only. step_archive_manager_feedback y su contrato de seleccion/movimiento NO se unifican.
- El sub-bloque de mover/unlink de cada consumidor: read-only salvo el cambio estrictamente derivado del rewire de import.
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal (primer loop; NO la suite canonica hasta el cierre)
python -m pytest tests/unit/test_manager_feedback_helpers.py -q
python -m ruff check scripts/manager_feedback_helpers.py scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py tests/unit/test_manager_feedback_helpers.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO unificar la politica de seleccion de tickets.
- NO cambiar el comportamiento observable del archivado.
- NO introducir una tercera implementacion real.

## CONTRACT_GAP / STOP
- Si preservar la API publica extract_ticket_id_from_feedback(filename) del CLI no es posible sin romper
  callers (deberia serlo via wrapper con default pattern).
- Si el rewire obliga a tocar la politica de seleccion o el contrato de step_archive_manager_feedback.
- Si la barrera de import-identity solo puede expresarse creando una suite paralela nueva.
-> emitir CG-WOT-2026-014f.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] python -m pytest tests/unit/test_manager_feedback_helpers.py -q pasa.
- [ ] existe scripts/manager_feedback_helpers.py con exactamente 1 definicion real de cada helper (firma del closeout).
- [ ] los 3 consumidores importan el canonico; ninguno conserva un cuerpo logico real duplicado.
- [ ] test de arquitectura (AST) afirma exactamente 1 implementacion real de discovery y 1 de parse, en el modulo canonico.
- [ ] BARRERA mutation-verified (import-identity): mutar el canonico cambia el comportamiento en CLI + archival + wrapper de session_closeout; revertir un consumidor a copia propia hace FALLAR el test.
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD.
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014f), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.
