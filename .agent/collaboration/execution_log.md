# Execution Log -- WOT-2026-013k

**Estado:** READY_FOR_REVIEW

## Re-encuadre contractual -- WOT-2026-013k

La auditoria contractual de 2026-06-25 detecto que la premisa inicial de `013k` era falsa: `repo_destino/.agent/collaboration/archive/notifications_*.md` NO esta versionado; es una superficie LOCAL gitignored.

Evidencia verificada por bytes:
- `git ls-files ".agent/collaboration/archive/notifications_*.md"` -> 0 hits.
- `git check-ignore -v .agent/collaboration/archive/notifications_20200101_000000.md` -> `.gitignore:72` (`.agent/collaboration/archive/`).
- `git log -- .agent/collaboration/archive/notifications_*.md` -> sin historial trackeado.

Decision aplicada:
- `013k` deja de apuntar al seam del controller.
- El fix correcto es extender `scripts/prune_runtime_retention.py` como follow-up directo de `013l`.
- `PLAN-013K-001`, `OBJ-013K-001`, `T-013K-001` y el packet activo quedaron resincronizados con esa premisa.

Guardrails del ciclo:
- No tocar `.agent/agent_controller.py`, `session_closeout`, `bus/**` ni `runtime/**`.
- No seleccionar nada en `collaboration/archive/` salvo `notifications_*.md`.
- Si la nueva superficie no cabe en la utilidad opt-in sin wiring automatico, emitir `CG-WOT-2026-013k.md` y parar.

## Fase 0 - Diagnostico read-only (Builder, 2026-06-25, cwd=repo_motor, HEAD=9ddfe5d)

Premisa CONFIRMADA (VERIFICABLE POR BYTES):
- `git ls-files ".agent/collaboration/archive/notifications_*.md"` -> 0 hits
  (NO versionado).
- `git check-ignore -v .agent/collaboration/archive/notifications_20200101_000000.md`
  -> `.gitignore:72: .agent/collaboration/archive/` (gitignored, local-only).
- 97 archivos `notifications_*.md` reales en el archive del workspace -> deuda real.
- Productor read-only: `archive_old_notifications()` (agent_controller.py:1923) escribe
  `ARCHIVE_DIR / f"notifications_{timestamp}.md"` (l.1948, strftime %Y%m%d_%H%M%S).
  NO se toca (solo lectura).
- Otros archivos en `collaboration/archive/` que JAMAS deben seleccionarse:
  `execution_log_legacy_*`, `manager_feedback/`, `recovered_*`, `relaunch_capsules/`,
  `review_queue_*.md`, etc.
- validate del workspace verde antes de tocar.

TENSION RESUELTA (clave): en 013l/013v, `collaboration/archive/` figura como
superficie PROHIBIDA (el test de safety puebla `collaboration/archive/ancient.md`
y verifica que NUNCA se selecciona). 013k anade `notifications_*.md` DENTRO de esa
carpeta. Se resuelve con un FILTRO DE PATRON estricto (como observation_baks filtra
por prefijo dentro de runtime/memory/): predicado
`name.startswith("notifications_") and name.endswith(".md")`. Verificado que
distingue: notifications_<ts>.md=True; notifications.md=False; review_queue_*.md=False;
manager_feedback=False. El test de safety existente (ancient.md, review_queue, etc.)
DEBE seguir verde porque ninguno matchea el patron.

NO es CONTRACT_GAP: el selector SI distingue notifications_*.md de otros archive
files, y no requiere tocar controller/closeout. Diseno: 4a Surface
("notification_archives", rel_root "collaboration/archive", entry_is_dir=False,
keep_arg "keep_notification_archives") + rama de filtro por patron en
_list_surface_entries (analoga a observation_baks). Cambio minimo, sin refactor del
modelo ni de las 3 superficies existentes. FLT: prune_runtime_retention.py + test.

## Fase 1 + Fase 2 - Implementacion, barreras y gates (Builder, 2026-06-25)

Cambios en `scripts/prune_runtime_retention.py` (FLT):
- 4a Surface "notification_archives" (rel_root "collaboration/archive",
  entry_is_dir=False, keep_arg "keep_notification_archives") con filtro de patron
  `name.startswith("notifications_") and name.endswith(".md")`. Excluye
  notifications.md (vivo), review_queue_*.md, manager_feedback, recovered_*,
  relaunch_capsules y cualquier otro archivo de collaboration/archive/.
- Flag `--keep-notification-archives <N>` (default conservador 20).
- Refactor: extraje `_entry_is_candidate(surface, entry)` para centralizar el
  filtro por superficie y bajar la complejidad de `_list_surface_entries`
  (C901 12->ok). No cambia comportamiento de las 3 superficies previas.
- `select_all` ahora tolerante: una keep-key ausente => keep-all (NUNCA poda por
  accidente; defensa para herramienta destructiva).
- Docstring + invariante de seguridad actualizados: collaboration/archive/ es
  reachable SOLO para la familia notifications_; el resto sigue prohibido.
- Salida: "retention over 4 gitignored local surfaces".

Tests en `tests/unit/test_prune_runtime_retention.py` (FLT, extendidos, no familia
paralela):
- Fixture ampliado: 5 notifications_<ts>.md + decoys de archive (review_queue,
  manager_feedback, recovered_work_plan, ancient.md).
- Tests existentes actualizados a 4 superficies (test_collects, safety,
  _forbidden_snapshot ya no incluye collaboration/archive; nuevo helper
  _archive_decoys_snapshot).
- 3 barreras nominales NUEVAS (node-ids exactos del DoD):
  TestRuntimeRetentionSelection::test_notification_archives_are_collected_as_gitignored_local_surface
  TestRuntimeRetentionSelection::test_keep_count_prunes_only_old_notification_archives
  TestRuntimeRetentionSafety::test_non_notification_collaboration_archive_files_are_never_selected

Evidencia mutation-verified (fail-sin-fix / pass-con-fix, con backup en scratchpad):
- MUTACION A: ampliar el filtro a todo `.md` ->
  test_non_notification_collaboration_archive_files_are_never_selected FALLA.
- MUTACION B: quitar la 4a Surface ->
  test_notification_archives_are_collected_as_gitignored_local_surface FALLA.
- Restaurado -> 15 passed.

Gates (comandos exactos + exit):
- `pytest tests/unit/test_prune_runtime_retention.py -q` -> 15 passed (exit 0).
- 5 node-ids del DoD -> 5 passed.
- `ruff check` (2 archivos) -> All checks passed (tras refactor C901). `ruff format` OK.
- `validate --json --force --project-root <workspace>` -> 0 errors / 0 warnings.
- dry-run real: 77 notification_archives candidatos; 97->97 (no borra).
- Suite canonica `run_pytest_safe --level all`: al HEAD post-commit (last-run.json).

Scope: sin creep. Solo los 2 archivos del FLT. agent_controller/closeout/bus/
runtime/gitignore/manifests/notifications.md NO tocados. archive_old_notifications
solo leido. CONTRACT_GAP NO aplica (premisa reprodujo; selector distingue la familia).

## Cierre canonico - suite + falso-verde descartado (Builder, 2026-06-25)

IMPORTANTE (evidencia, no relato; redaccion alineada LITERALMENTE con el artefacto):
la primera corrida de la suite canonica con `AGENT_PROJECT_ROOT=<workspace>` (como
sugeria la seccion cross-repo del prompt) NO produjo una suite valida. El runner
eligio el interprete del workspace (`<workspace>/.venv`), que NO tiene pytest
instalado -> stdout literal "No module named pytest". La suite NO corrio.

Distincion exacta de exit codes (VERIFICADA POR ARTEFACTO, sin contradiccion):
- El `last-run.json` del workspace (el ARTEFACTO canonico del gate) registro
  `exit_code: 1`, status=finished. Es decir, el gate canonico SI capturo el fallo;
  un cierre que lea el artefacto NO se deja enganar.
- La unica senal "0" fue el exit del PROCESO WRAPPER de fondo (el shell que lanzo
  run_pytest_safe.py, reportado por la task-notification del entorno), NO el del
  gate. Ese 0 del wrapper NO es evidencia de suite verde.
- Leccion: la evidencia de cierre es el `last-run.json` (exit_code/sha/N passed),
  nunca el exit del wrapper que orquesta la corrida. El riesgo es fiarse del exit
  del wrapper, no que el artefacto mienta.

Razon: WOT-2026-013k es `delivery_authority: repo_motor`; el codigo entregado vive
en el motor (`scripts/prune_runtime_retention.py`) y la suite que lo prueba es la
del motor. La regla cross-repo (CTL-2026-007b) aplica a `delivery_authority:
repo_destino`, no aqui. La corrida canonica correcta usa el INTERPRETE DEL MOTOR,
sin AGENT_PROJECT_ROOT apuntando al workspace.

Corrida autoritativa correcta (last-run.json del MOTOR, VERIFICADO):
- status=finished, exit_code=0, level=all, args_mode=default_discovery,
  tested_commit_sha=8454c96 == HEAD, cwd=repo_motor.
- 3197 passed, 20 skipped.

## Correccion tras CHANGES del Manager (Builder, 2026-06-25)

CHANGES del Manager: 1 BLOCKER (redaccion del execution_log) + 1 sugerencia no
bloqueante (help). Codigo aprobado, sin defectos de implementacion.

- BLOCKER (contradiccion exit 0 vs exit_code=1 en la narrativa del falso-verde):
  reescrito el bloque "Cierre canonico - suite + falso-verde descartado" arriba
  para que coincida LITERALMENTE con el artefacto. Distincion exacta: el
  `last-run.json` del workspace = `exit_code: 1` (el gate SI capturo el fallo); el
  "0" era SOLO el exit del proceso WRAPPER de fondo (task-notification del entorno),
  NO del gate. Eliminada la frase "el proceso devolvio exit 0 ... la suite NO corrio"
  que mezclaba ambos. Mismo error que el Manager ya me corrigio en la memoria
  Claude; aplicado aqui.
- Sugerencia no bloqueante (help description listaba 3 superficies): corregido el
  `description` del argparse en `prune_runtime_retention.py` para listar tambien
  `collaboration/archive/notifications_*.md`. Help-only, sin cambio de comportamiento;
  15 focal passed (barreras de help de 013v intactas), ruff limpio. Commit motor
  `84726ad`.

Re-cierre: suite canonica re-ejecutada al nuevo HEAD `84726ad` con el INTERPRETE
DEL MOTOR (delivery_authority repo_motor); ver last-run.json del motor.
