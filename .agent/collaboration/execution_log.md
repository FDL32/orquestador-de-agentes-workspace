# Execution Log -- WOT-2026-013v

**Estado:** COMPLETED

## Bootstrap operativo -- WOT-2026-013v

Ticket activado para documentar la semantica operativa de `reviews/` en `scripts/prune_runtime_retention.py` sin cambiar el algoritmo de orden ni ampliar el blast radius del borrado local.

Procedencia verificada (2026-06-25):
- `WOT-2026-013l` ya cerro canonico en `COMPLETED` y deja como follow-up vivo `013v`.
- El packet canonico de este ciclo vive en `.agent/planning/work_plan_WOT-2026-013v.md`.
- El bus ya registra `STATE_CHANGED -> IN_PROGRESS` para `WOT-2026-013v`.
- `STATE.md` y `TURN.md` se resincronizaron desde la ruta canonica del supervisor para abrir el siguiente Builder loop sin drift.

Premisa activa:
- `reviews/` se ordena hoy por `mtime` del DIRECTORIO del ticket.
- `review_packets/` y `observations.jsonl.bak.*` siguen siendo superficies por archivo y no forman parte del cambio.
- La tarea de `013v` es volver explicita esa semantica en help/docstring/salida y blindarla con tests nominales.

Guardrails del ciclo:
- No cambiar el algoritmo de orden de `reviews/` en esta ronda.
- No tocar `review_packets`, `observations.jsonl.bak.*`, closeout, launcher ni productores de runtime fuera del texto compartido imprescindible.
- Si hacer honesta la semantica exige cambiar el algoritmo real, emitir `CG-WOT-2026-013v.md` y parar.

## Fase 0 - Diagnostico read-only (Builder, 2026-06-25, cwd=repo_motor, HEAD=cf689eb)

Premisa CONFIRMADA (VERIFICABLE POR BYTES):
- `reviews/` se ordena por `p.stat().st_mtime` (_sort_newest_first, l.144) y sus
  entradas son DIRECTORIOS por ticket (Surface "reviews" entry_is_dir=True, l.70).
- El help actual dice "Keep the newest N review dirs" (l.18 del --help) pero NO
  explicita que "newest" = mtime del DIRECTORIO, no "ultimo intento logico" /
  archivo mas reciente dentro del dir. El docstring (l.29-30) dice generico
  "newest kept; deterministic by mtime then name" sin aclarar reviews.
- `review_packets/` y `observations.jsonl.bak.*` son superficies por ARCHIVO; su
  mtime ES el del propio artefacto, asi que NO sufren la ambiguedad. Fuera de scope.
- validate del workspace verde antes de tocar -> es documentacion de semantica, no
  reparacion.

Evidencia de la ambiguedad (medida en 013l, ya en backlog 013v): en el workspace,
23 de 38 dirs de reviews/ tienen mtime de dir divergente del archivo mas reciente
dentro (hasta ~38883 s ~= 11 h), porque el FS bumpa el mtime del dir al anadir/
quitar entradas directas, no al editar archivos anidados.

Hallazgos legacy/portabilidad: ninguno. No se detectaron stubs ni destino-only en
la superficie tocada.

Decision: NO es CONTRACT_GAP (la premisa reproduce, el codigo SI usa mtime de dir).
Via conservadora del contrato: explicitar la semantica en docstring/help/salida +
3 barreras nominales nuevas, SIN cambiar el algoritmo de orden. FLT:
scripts/prune_runtime_retention.py + tests/unit/test_prune_runtime_retention.py.
Sin desviaciones de scope.

## Fase 1 + Fase 2 - Implementacion, barreras y gates (Builder, 2026-06-25)

Cambios en `scripts/prune_runtime_retention.py` (FLT, solo texto/semantica, SIN
tocar el algoritmo de orden):
- Docstring: parrafo "Recency semantics (WOT-2026-013v)" que explicita que para
  reviews/ la recencia es el mtime del DIRECTORIO del ticket, NO el archivo mas
  reciente dentro ("last logical attempt"); packets/baks son superficies por
  archivo. Nota de que cambiar el orden seria un follow-up con aprobacion.
- Help de `--keep-reviews`: "ranked by DIRECTORY mtime (not the newest file
  inside the dir)".
- Salida de prune(): linea "(reviews recency = DIRECTORY mtime, not the newest
  file inside the dir)" en dry-run y apply.

Barreras (Fase 2) en `tests/unit/test_prune_runtime_retention.py` (los 4 node-ids
del DoD, en sus clases exactas):
- TestRuntimeRetentionDocs::test_help_makes_directory_mtime_semantics_explicit (NUEVO)
- TestRuntimeRetentionDocs::test_reviews_semantics_do_not_claim_last_logical_attempt (NUEVO)
- TestRuntimeRetentionSelection::test_review_directories_are_ranked_by_directory_mtime_not_nested_file_mtime
  (NUEVO; barrera COMPORTAMENTAL: 2 dirs donde el mtime de dir y el del archivo
  interno DIVERGEN; keep=1 conserva el de dir-mtime mas nuevo aunque su archivo
  interno sea viejo. Si alguien reordena por archivo nested, el set se invierte
  y FALLA.)
- TestRuntimeRetentionSelection::test_keep_count_prunes_old_review_and_packet_entries
  (EXISTENTE, sigue pasando -> packets/baks conservan su politica).
Hermeticas: usan tmp_path / subprocess --help, sin el workspace vivo.

Evidencia mutation-verified (worktree-equivalente con backup en scratchpad):
- MUTACION A: revertir el help/docstring a wording ambiguo ->
  test_help_makes_directory_mtime_semantics_explicit FALLA.
- MUTACION B: reordenar reviews/ por mtime del archivo NESTED ->
  test_review_directories_are_ranked_by_directory_mtime_not_nested_file_mtime FALLA.
- Restaurado -> 12 passed.

Gates (comandos exactos + exit):
- `pytest tests/unit/test_prune_runtime_retention.py -q` -> 12 passed (exit 0).
- 4 node-ids del DoD -> 4 passed.
- `ruff check` (2 archivos) -> All checks passed; `ruff format` -> formatted.
- `validate --json --force --project-root <workspace>` -> 0 errors / 0 warnings.
- `prune --help` y `--dry-run` reales: semantica de reviews ahora inequivoca.
- Suite canonica `run_pytest_safe --level all`: al HEAD post-commit (last-run.json).

Scope: sin creep. Solo los 2 archivos del FLT, solo texto+tests. Algoritmo de
orden INTACTO (sigue mtime de dir). Forbidden surfaces no tocadas. CONTRACT_GAP
NO aplica (la premisa reprodujo; el codigo usa mtime de dir).

## Manager review - trazabilidad adicional (2026-06-25)

Decision de review: APROBADO.

Nota de trazabilidad:
- El Manager reverifico diff, scope, `ruff`, los 4 node-ids del DoD, `validate 0/0`,
  la suite canonica via `last-run.json` y el bus canonico `BUILDER_EXIT + STATE_CHANGED -> READY_FOR_REVIEW`.
- El claim de mutacion adversarial del Builder NO se reejecuto de forma independiente
  en esta pasada del Manager; queda aceptado como evidencia reportada por Builder,
  no como reproduccion adversarial propia del Manager.



Manager approved canonical closeout for WOT-2026-013v