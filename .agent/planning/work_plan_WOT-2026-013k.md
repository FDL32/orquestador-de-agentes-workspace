# Plan de Trabajo: WOT-2026-013k

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013k
- **Estado:** APPROVED
- **Titulo:** Acotar el historico versionado de notifications_*.md sin perder trazabilidad util
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-013K-001
- **Plan-Link:** PLAN-013K-001
- **Builder clarification budget:** 0 (el ticket fija el seam real, la via conservadora de consolidacion y las superficies prohibidas; no deja abierta una poda ciega ni un rediseno del closeout)

## Objetivo
Introducir una politica conservadora y verificable para `repo_destino/.agent/collaboration/archive/notifications_*.md`: conservar visibles solo los snapshots recientes como archivos individuales y compactar el historico frio en un archivo determinista con contenido integro y rango temporal verificable, sin romper la rotacion viva de `notifications.md`, sin tocar otros archivos de `archive/` y sin mover esta superficie al circuito gitignored de `013l/013v`.

## Premise
`013l` y `013v` resolvieron el problema de crecimiento local gitignored (`reviews/`, `review_packets/`, `observations.jsonl.bak.*`) con una utilidad opt-in y con semantica explicita. `013k` es distinto: el crecimiento vive en un historico VERSIONADO del repo de dogfooding. `.agent/agent_controller.py::archive_old_notifications()` crea hoy un nuevo `notifications_<timestamp>.md` cada vez que `notifications.md` supera el umbral, pero no aplica retencion sobre snapshots previos. Eso deja un historico util, pero tambien un crecimiento sin techo en cada clone. La solucion honesta no es borrar sin mas: hay que compactar el historico frio en un artefacto verificable que conserve el texto integro y el rango temporal de los snapshots absorbidos, y mantener solo una ventana reciente como archivos sueltos.

## Premise Re-check (cwd=repo_motor salvo cuando se indica; solo lectura)
```
Get-ChildItem <workspace_activo>/.agent/collaboration/archive/notifications_*.md | Select-Object FullName,Length,LastWriteTime
rg -n "MAX_NOTIFICATION_ENTRIES|def archive_old_notifications|notifications_\{timestamp\}\.md|ARCHIVE_DIR|_handle_archive" .agent/agent_controller.py
rg -n "collaboration/archive|ARCHIVE_DIR|execution_log" scripts/check_no_history_truncation.py scripts/pre_handoff_guard.py
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- existe historico versionado `notifications_*.md` en `repo_destino/.agent/collaboration/archive/`;
- el seam real es `archive_old_notifications()` dentro del controller, no una utilidad externa ya existente;
- los guardrails actuales protegen `collaboration/archive/` como historico, pero no aplican politica especifica a `notifications_*.md`;
- `validate` del workspace sigue en `0 errors / 0 warnings` antes de tocar nada.
Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
La via de menor riesgo es resolver `013k` en el seam real del controller: la politica de retencion/consolidacion vive junto a `archive_old_notifications()`, que es quien conoce el momento exacto en que nace un nuevo snapshot. Este ticket NO crea una segunda utilidad generica de poda, NO mueve `notifications_*.md` a gitignored, y NO integra nada al closeout. La politica debe ser concreta: compactar primero el historico frio en un archivo determinista que preserve contenido y rango temporal, y solo despues retirar archivos individuales antiguos ya absorbidos, dejando visibles exactamente los N mas recientes como snapshots sueltos.

## Plan - secuencia minima FIJA
### Paso 1 - politica de consolidacion en el seam real
- Extender `.agent/agent_controller.py::archive_old_notifications()` (o helper inmediato del mismo modulo) para que, tras crear el snapshot nuevo de la rotacion actual, mantenga solo una ventana reciente de `notifications_*.md` como archivos individuales.
- Los snapshots mas antiguos deben compactarse en un artefacto determinista bajo el mismo `archive/`, con contenido integro y rango temporal verificable, antes de poder retirarlos como archivos individuales.
- Mantener intacta la semantica viva de `notifications.md`: el tail sigue siendo el ultimo `MAX_NOTIFICATION_ENTRIES` del log activo.

### Paso 2 - barreras de regresion
- Crear `tests/unit/test_notification_archive_retention.py` con barreras hermeticas contra tres regresiones:
  1. crecimiento versionado sin techo;
  2. borrado de historico frio sin compensacion verificable;
  3. contaminacion de `archive/` fuera de `notifications_*.md`.
- La barrera debe fallar sin el fix y pasar con el fix. No usar el workspace vivo como fixture.

### Paso 3 - no derivar el alcance
- Confirmar que `scripts/check_no_history_truncation.py` y `scripts/pre_handoff_guard.py` siguen siendo solo guardrails read-only y no se convierten en la implementacion de la politica.
- No tocar `013l/013v`, `session_closeout`, `bus/**`, `runtime/**`, manifests ni la naturaleza versionada del historico.
- Si la unica salida segura es sacar esta superficie del repo o redisenar closeout, eso es CONTRACT_GAP, no scope creep permitido.

## Files Likely Touched (relativos a repo_motor)
- `.agent/agent_controller.py`
- `tests/unit/test_notification_archive_retention.py`

Aclaraciones (no parte de las rutas):
- `.agent/agent_controller.py`: retencion/consolidacion de `notifications_*.md` en `archive_old_notifications()` o helper inmediato del mismo modulo; no tocar el lifecycle general del controller.
- `tests/unit/test_notification_archive_retention.py`: nueva barrera hermetica de regresion sobre el historico versionado de notifications; no abrir una segunda familia de tests sobre closeout.

## Forbidden Surfaces
- `repo_motor/scripts/prune_runtime_retention.py`: fuera de scope; ese flujo ya cubre solo superficies gitignored.
- `repo_motor/scripts/session_closeout.py`, `repo_motor/bus/**`, `repo_motor/runtime/**`: fuera de scope; `013k` no redisena lifecycle ni closeout.
- `repo_motor/scripts/check_no_history_truncation.py` y `repo_motor/scripts/pre_handoff_guard.py`: read-only; no convertir guardrails en implementacion de producto.
- cualquier archivo de `repo_destino/.agent/collaboration/archive/` que no sea `notifications_*.md`.
- `repo_motor/MANIFEST.distribute`, `repo_motor/MANIFEST.workspace`, `.gitignore`: este ticket no cambia la frontera portable ni la naturaleza versionada del historico.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/unit/test_notification_archive_retention.py -q
python -m pytest tests/test_completion_integration.py::test_approved_ready_for_review_handoff -q
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO reabrir `013l` ni `013v`, ni reutilizar su utilidad local opt-in para esta superficie versionada.
- NO convertir `notifications_*.md` en gitignored ni sacarlos del repo en esta ronda.
- NO tocar closeout, session-close, bus, runtime ni manifests.
- NO podar a ciegas historico util sin consolidacion verificable previa.

## CONTRACT_GAP / STOP
- Si la unica solucion segura exige mover `notifications_*.md` fuera del repo o cambiar su naturaleza versionada.
- Si compactar el historico obliga a tocar `archive/` fuera de `notifications_*.md` o a redisenar closeout/bus/lifecycle.
- Si el seam real no es `archive_old_notifications()` y el ticket queda sin punto de control localizable.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013k.md` y PARA.

## DoD (binario, comandos exactos)
- [ ] `python -m pytest tests/unit/test_notification_archive_retention.py::test_archive_old_notifications_consolidates_cold_archives_and_keeps_recent_snapshots -q` pasa; si los snapshots frios se borran sin consolidacion o si el crecimiento vuelve a quedar sin techo, FALLA.
- [ ] `python -m pytest tests/unit/test_notification_archive_retention.py::test_archive_old_notifications_preserves_notifications_tail_after_rotation -q` pasa; la rotacion viva mantiene el tail correcto de `notifications.md`.
- [ ] `python -m pytest tests/unit/test_notification_archive_retention.py::test_archive_old_notifications_leaves_non_notification_archive_files_untouched -q` pasa; si el fix toca `archive/` fuera de `notifications_*.md`, FALLA.
- [ ] `python -m pytest tests/test_completion_integration.py::test_approved_ready_for_review_handoff -q` sigue pasando para confirmar que el flujo principal del controller no regresa por la nueva politica de archivo.
- [ ] `python -m ruff check .agent/agent_controller.py tests/unit/test_notification_archive_retention.py` -> `All checks passed`.
- [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013k`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.