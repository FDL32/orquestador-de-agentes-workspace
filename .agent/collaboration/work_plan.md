# Plan de Trabajo: WOT-2026-013l

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013l
- **Estado:** APPROVED
- **Titulo:** Retencion local opt-in para runtime gitignored (reviews, review_packets, observations.bak)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-013L-001
- **Plan-Link:** PLAN-013L-001
- **Builder clarification budget:** 0 (el ticket fija superficie, enfoque opt-in, rutas prohibidas, nombre de script/tests y el contrato exacto de la barrera; no deja decisiones abiertas de producto)

## Objetivo
Introducir una via pequena, opt-in y auditable para aplicar retencion por conteo/edad sobre las superficies locales gitignored `repo_destino/.agent/runtime/reviews/`, `repo_destino/.agent/runtime/review_packets/` y `repo_destino/.agent/runtime/memory/observations.jsonl.bak.*`, sin tocar historico versionado ni integrar la poda en `session-close` o en productores existentes.

## Premise
La deuda de `013l` es estrictamente LOCAL y de disco del operador: las tres superficies objetivo estan gitignored en `repo_motor` y `repo_destino`, y ademas figuran como excluidas del contrato portable en `MANIFEST.distribute` / `MANIFEST.workspace`. Los productores actuales (`review_bridge`/`review_report` para reviews y packets; `memory_consolidate`/`migrate_observations` para backups) crean artefactos legitimos, pero hoy no existe una herramienta auditable y de bajo riesgo para acotar su retencion. El camino de menor blast radius es una CLI independiente, explicitamente invocada, en vez de cablear poda automatica dentro del lifecycle de cierre.

## Premise Re-check (cwd=repo_motor, solo lectura)
```
rg -n "\.agent/runtime/reviews/|\.agent/runtime/review_packets/|observations\.jsonl\.bak\.\*" .gitignore MANIFEST.distribute MANIFEST.workspace
rg -n "review_packets|runtime/reviews|observations\.jsonl\.bak" bus scripts tests
python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- las tres superficies objetivo aparecen como gitignored/local-only;
- existen productores vivos para esas rutas, pero no una politica de retencion dedicada;
- `validate` del workspace sigue verde antes de tocar nada, confirmando que esto es higiene local y no una reparacion de estado roto.
Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
La solucion debe ser una utilidad opt-in, separada del closeout y de los productores. Este ticket NO cambia el contrato de `session-close`, `mark-ready`, `manager-review`, `memory_consolidate` ni `migrate_observations`. Solo introduce una CLI enfocada a seleccionar/listar/borrar candidatos de las tres superficies objetivo con `--dry-run` y `--apply` explicitos, manteniendo la poda fuera de las rutas versionadas y del historico util.

## Plan - secuencia minima FIJA
### Paso 1 - seleccion de candidatos
- Crear una utilidad nueva en `scripts/prune_runtime_retention.py` que resuelva `--project-root`, detecte solo las tres superficies objetivo y seleccione candidatos por conteo/edad de forma determinista.
- El criterio por defecto debe ser conservador y auditable; no asumir que cada artefacto antiguo se puede borrar por edad si no cae dentro de las tres superficies fijadas.

### Paso 2 - dry-run y apply explicitos
- Exponer un `--dry-run` legible y un `--apply` explicito; el script no debe borrar nada si el modo no queda declarado con claridad.
- Declarar explicitamente los flags de retencion `--keep-reviews <N>`, `--keep-packets <N>` y `--keep-observation-baks <N>` para que el contrato de conteo quede autocontenido en este work plan.
- La salida debe permitir verificar que solo se tocarian/tocaron archivos de `reviews`, `review_packets` y `observations.jsonl.bak.*`.

### Paso 3 - barreras de regresion
- Anadir una familia nueva de tests focales en `tests/unit/test_prune_runtime_retention.py`.
- La barrera debe FALLAR si el selector intenta incluir historico versionado (`events/archive`, `collaboration/archive`, `_archive/plan_audit`, `audits/system_health`) o si la CLI degrada `dry-run` a borrado real.

## Files Likely Touched (relativos a repo_motor)
- `scripts/prune_runtime_retention.py`
- `tests/unit/test_prune_runtime_retention.py`

Aclaraciones (no parte de las rutas):
- `scripts/prune_runtime_retention.py`: utilidad nueva, standalone y opt-in; no se cablea a `session-close`, `mark-ready` ni al controller.
- `tests/unit/test_prune_runtime_retention.py`: pruebas de seleccion segura, `dry-run`, `apply` y barrera contra spillover a superficies versionadas.

## Forbidden Surfaces
- `repo_motor/.agent/agent_controller.py`, `repo_motor/bus/**`, `repo_motor/runtime/**`: fuera de scope; este ticket no cambia semantica de cierre, review ni estado de bus.
- `repo_motor/scripts/memory_consolidate.py`, `repo_motor/scripts/migrate_observations.py`, `repo_motor/bus/review_bridge.py`, `repo_motor/bus/review_report.py`: productores read-only en esta ronda; no integrar la retencion ahi.
- `repo_motor/.gitignore`, `repo_motor/MANIFEST.distribute`, `repo_motor/MANIFEST.workspace`: read-only; la premisa local-only ya esta fijada.
- `repo_destino/.agent/runtime/events/archive/**`, `repo_destino/.agent/audits/system_health/**`, `repo_destino/.agent/collaboration/archive/**`, `repo_destino/.agent/collaboration/_archive/**`: historico versionado/util, prohibido absoluto.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/unit/test_prune_runtime_retention.py -q
python scripts/prune_runtime_retention.py --project-root <repo_destino> --dry-run --keep-reviews <N> --keep-packets <N> --keep-observation-baks <N>
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO tocar `013k` ni introducir retencion para `notifications_*.md` versionado en esta ronda.
- NO cablear la poda dentro de `session-close`, `mark-ready`, `manager-approve` ni del launcher.
- NO cambiar productores de reviews/packets/backups; solo consumir sus artefactos desde una utilidad aparte.
- NO cambiar `gitignore`, manifests, ni la politica de archivado/versionado del workspace.

## CONTRACT_GAP / STOP
- Si la unica solucion segura exige tocar `session-close`, `mark-ready`, `review_bridge`, `memory_consolidate` o cualquier productor de runtime en vez de una CLI independiente.
- Si la retencion necesita inspeccionar o borrar superficies versionadas/historico util para cumplir el objetivo.
- Si el selector no puede distinguir de forma determinista entre artefactos locales podables y artefactos utiles que deban preservarse.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013l.md` y PARA.

## DoD (binario, comandos exactos)
- [x] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_collects_only_gitignored_runtime_targets -q` pasa y demuestra que el selector solo considera `reviews`, `review_packets` y `observations.jsonl.bak.*`.
- [x] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_keep_count_prunes_old_review_and_packet_entries -q` pasa; si se reintroduce spillover hacia otra ruta o se rompe el orden determinista, FALLA.
- [x] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_observation_backups_follow_the_same_retention_policy -q` pasa y cubre `observations.jsonl.bak.*` sin crear una politica separada opaca.
- [x] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_dry_run_reports_without_deleting tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_apply_deletes_only_selected_candidates -q` pasa; `dry-run` no borra nada y `apply` elimina solo los candidatos seleccionados.
- [x] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSafety::test_versioned_history_surfaces_are_never_selected -q` pasa; si se intenta incluir `events/archive`, `collaboration/archive`, `_archive/plan_audit` o `audits/system_health`, FALLA.
- [x] `python -m ruff check scripts/prune_runtime_retention.py tests/unit/test_prune_runtime_retention.py` -> `All checks passed`.
- [x] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [x] `python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013l`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano. Ejemplo focal portable: `python scripts/prune_runtime_retention.py --project-root <repo_destino> --dry-run --keep-reviews 20 --keep-packets 20 --keep-observation-baks 10`.
