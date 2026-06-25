# Plan de Trabajo: WOT-2026-013k

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013k
- **Estado:** APPROVED
- **Titulo:** Extender retention local opt-in a notifications_*.md gitignored en collaboration/archive
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** WOT-2026-013l
- **Objective-Link:** OBJ-013K-001
- **Plan-Link:** PLAN-013K-001
- **Builder clarification budget:** 0 (el ticket fija la premisa gitignored, la superficie real a extender, el FLT y la prohibicion expresa de tocar controller/closeout)

## Objetivo
Extender `scripts/prune_runtime_retention.py` para incluir `repo_destino/.agent/collaboration/archive/notifications_*.md` como cuarta superficie local gitignored de retencion opt-in, con `--dry-run` y `--apply` explicitos, conservando solo los N mas recientes de esa familia y sin tocar ningun otro artefacto de `collaboration/archive/` ni la superficie viva `notifications.md`.

## Premise
La auditoria contractual de 2026-06-25 corrigio la premisa inicial de `013k`: `notifications_*.md` NO vive en historico versionado. Verificacion por bytes: `git ls-files` devuelve 0 hits, `git check-ignore -v` resuelve a `.gitignore:72` (`.agent/collaboration/archive/`), y `git log -- .agent/collaboration/archive/notifications_*.md` no muestra historial trackeado. Por tanto, `013k` no es un ticket del seam del controller ni de closeout; es una laguna de la utilidad local ya entregada por `013l`. Hoy `prune_runtime_retention.py` cubre `reviews/`, `review_packets/` y `observations.jsonl.bak.*`, pero deja fuera `collaboration/archive/notifications_*.md` aunque comparte la misma naturaleza: superficie local, gitignored y de retencion opt-in.

## Premise Re-check (cwd=repo_motor salvo cuando se indica; solo lectura)
```
git -C <workspace_activo> ls-files ".agent/collaboration/archive/notifications_*.md"
git -C <workspace_activo> check-ignore -v .agent/collaboration/archive/notifications_20200101_000000.md
rg -n "collaboration/archive|notifications|keep_observation_baks|keep_packets|keep_reviews" scripts/prune_runtime_retention.py tests/unit/test_prune_runtime_retention.py
rg -n "archive_old_notifications|notifications_\{timestamp\}\.md|ARCHIVE_DIR" .agent/agent_controller.py
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- `notifications_*.md` no esta trackeado y queda cubierto por `.gitignore` del workspace;
- la utilidad actual de retencion local cubre solo tres superficies y deja fuera `notifications_*.md`;
- `.agent/agent_controller.py::archive_old_notifications()` es solo el productor read-only de esos snapshots, no la superficie correcta del fix;
- `validate` del workspace sigue en `0 errors / 0 warnings` antes de tocar nada.
Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
La via de menor riesgo es extender la utilidad local ya existente, no tocar el controller. `013k` es un follow-up directo de `013l`: misma CLI opt-in, misma politica de `--dry-run|--apply`, misma barrera de no spillover, y una cuarta superficie localizada con patron estricto (`collaboration/archive/notifications_*.md`). Este ticket NO modifica `archive_old_notifications()`, NO se integra al closeout, y NO autoriza seleccionar otros archivos de `collaboration/archive/`.

## Plan - secuencia minima FIJA
### Paso 1 - ampliar la superficie del selector
- Extender `scripts/prune_runtime_retention.py` para reconocer `repo_destino/.agent/collaboration/archive/notifications_*.md` como cuarta superficie local opt-in.
- Exponer un flag explicito `--keep-notification-archives <N>` con default conservador y semantica consistente con el resto de keep-counts.
- Mantener `notifications.md` completamente fuera de la seleccion; solo se toca la familia `notifications_*.md` dentro de `collaboration/archive/`.

### Paso 2 - barreras de regresion en la familia existente
- Extender `tests/unit/test_prune_runtime_retention.py` en vez de abrir una familia paralela.
- Anadir barreras para probar tres invariantes concretas:
  1. `notifications_*.md` entra en la seleccion como cuarta superficie gitignored;
  2. el keep-count conserva exactamente los N mas recientes de esa familia;
  3. ningun otro archivo de `collaboration/archive/` puede ser candidato.
- Las barreras deben fallar sin el fix y pasar con el fix. No usar el workspace vivo como fixture.

### Paso 3 - no derivar el alcance
- Confirmar que `.agent/agent_controller.py`, `session_closeout`, `bus/**`, `runtime/**`, manifests y `.gitignore` permanecen read-only.
- No tocar `013v`; el ticket se apoya en `013l`, no reabre la semantica de `reviews/`.
- Si la nueva superficie no puede modelarse con la utilidad actual sin tocar closeout/controller, eso es CONTRACT_GAP.

## Files Likely Touched (relativos a repo_motor)
- `scripts/prune_runtime_retention.py`
- `tests/unit/test_prune_runtime_retention.py`

Aclaraciones (no parte de las rutas):
- `scripts/prune_runtime_retention.py`: nueva cuarta superficie `collaboration/archive/notifications_*.md`, nuevo keep-count explicito y salida coherente con el resto de la CLI.
- `tests/unit/test_prune_runtime_retention.py`: extender la familia existente con barreras nominales para notifications archivadas; no crear tests del controller.

## Forbidden Surfaces
- `repo_motor/.agent/agent_controller.py`, `repo_motor/scripts/session_closeout.py`, `repo_motor/bus/**`, `repo_motor/runtime/**`: fuera de scope; `013k` no toca productores ni closeout.
- `repo_motor/.gitignore`, `repo_motor/MANIFEST.distribute`, `repo_motor/MANIFEST.workspace`: read-only; la premisa gitignored ya esta fijada.
- cualquier archivo de `repo_destino/.agent/collaboration/archive/` que no coincida con `notifications_*.md`.
- `repo_destino/.agent/collaboration/notifications.md`: superficie viva, prohibido.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/unit/test_prune_runtime_retention.py -q
python scripts/prune_runtime_retention.py --project-root <workspace_activo> --dry-run --keep-reviews 20 --keep-packets 20 --keep-observation-baks 10 --keep-notification-archives 20
python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO tocar `.agent/agent_controller.py` ni mover la retencion al seam del controller.
- NO integrar esta superficie en `session-close`, `mark-ready`, `manager-approve` ni otro wiring automatico.
- NO seleccionar archivos de `collaboration/archive/` que no sean `notifications_*.md`.
- NO cambiar `.gitignore`, manifests ni la naturaleza local gitignored de esta superficie.

## CONTRACT_GAP / STOP
- Si la unica forma de cubrir `notifications_*.md` exige tocar `.agent/agent_controller.py`, `session_closeout` o closeout/bus.
- Si el selector no puede distinguir `notifications_*.md` de otros artefactos de `collaboration/archive/`.
- Si `notifications_*.md` deja de estar gitignored y el problema vuelve a ser de historico versionado.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013k.md` y PARA.

## DoD (binario, comandos exactos)
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_notification_archives_are_collected_as_gitignored_local_surface -q` pasa y demuestra que `notifications_*.md` entra como cuarta superficie local del selector.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_keep_count_prunes_only_old_notification_archives -q` pasa; el selector conserva exactamente los N mas recientes de `notifications_*.md` y poda solo el resto.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSafety::test_non_notification_collaboration_archive_files_are_never_selected -q` pasa; si la utilidad intenta incluir `review_queue`, `manager_feedback` u otros archivos de `collaboration/archive/`, FALLA.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_dry_run_reports_without_deleting tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_apply_deletes_only_selected_candidates -q` sigue pasando con cobertura de la nueva superficie.
- [ ] `python -m ruff check scripts/prune_runtime_retention.py tests/unit/test_prune_runtime_retention.py` -> `All checks passed`.
- [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --force --project-root <workspace_activo>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013k`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.