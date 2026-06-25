# Plan de Trabajo: WOT-2026-013v

> Fuente canonica unica del ticket (packet oficial). El backlog del workspace
> debe REFERENCIAR este archivo, no reproducir su cuerpo.

## Metadata
- **ID:** WOT-2026-013v
- **Estado:** APPROVED
- **Titulo:** Documentar semantica de recencia en reviews/ para prune_runtime_retention
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Baja
- **Depende de:** WOT-2026-013l
- **Objective-Link:** OBJ-013V-001
- **Plan-Link:** PLAN-013V-001
- **Builder clarification budget:** 0 (el ticket ya decide la via conservadora: documentar la semantica actual de `reviews/`, no cambiar el algoritmo ni tocar closeout)

## Objetivo
Hacer explicita y verificable la semantica actual de `reviews/` en `scripts/prune_runtime_retention.py`: "reciente" significa `mtime` del DIRECTORIO del ticket, no "ultimo intento logico" dentro del dir. El ticket deja esa decision visible en help/docstring/salida y la blinda con tests, sin cambiar el algoritmo de orden ni ampliar blast radius sobre borrado.

## Premise
La review de `013l` detecto una ambiguedad real en una utilidad ya aprobada: para `reviews/`, el script ordena por `mtime` del directorio del ticket, mientras que el operador puede leer "mas reciente" como "ultimo intento logico" (el archivo mas nuevo dentro del dir). La medicion local del workspace de dogfooding demostro que el `mtime` del directorio y el `mtime` del archivo mas reciente dentro del directorio divergen con frecuencia (23 de 38 dirs; hasta ~38883 s, unas 11 h). Como la CLI es opt-in, conservadora y exige `--dry-run` antes de `--apply`, el camino de menor riesgo para `013v` es hacer explicita la semantica real y dejar barreras que impidan volver a vender otra distinta por accidente.

## Premise Re-check (cwd=repo_motor, solo lectura)
```
python scripts/prune_runtime_retention.py --help
rg -n "st_mtime|Keep the newest N review dirs|reviews/|review_packets|observations\.jsonl\.bak|dry-run" scripts/prune_runtime_retention.py
rg -n "TestRuntimeRetentionSelection|TestRuntimeRetentionCLI|TestRuntimeRetentionSafety|review_directories_are_ranked|help_makes_directory_mtime_semantics_explicit" tests/unit/test_prune_runtime_retention.py
python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>
```
Condicion de arranque (read-only, VERIFICABLE POR BYTES):
- `reviews/` se ordena hoy por `p.stat().st_mtime` del directorio por ticket;
- `review_packets/` y `observations.jsonl.bak.*` siguen siendo superficies por archivo y no forman parte de la ambiguedad detectada;
- la ayuda/docstring actual no deja suficientemente explicito que `reviews/` usa `mtime` de directorio;
- `validate` del workspace sigue en `0 errors / 0 warnings` antes de tocar nada.
Si esta premisa no reproduce, PARA y documenta el drift antes de tocar codigo.

## Decision Arquitectonica
`013v` sigue la via de MENOR RIESGO: documentar la semantica actual de `reviews/` y blindarla con barreras. Este ticket NO reordena `reviews/` por el archivo mas reciente dentro del dir, NO cambia la politica de `review_packets` o `observations.jsonl.bak.*`, y NO integra nada al closeout. Si mas adelante se quisiera cambiar el algoritmo, eso iria en otro follow-up con aprobacion explicita.

## Plan - secuencia minima FIJA
### Paso 1 - explicitar la semantica actual
- Ajustar el docstring/help y, si hace falta, la salida de `--dry-run` para que `reviews/` diga sin ambiguedad que su recencia se mide por `mtime` del DIRECTORIO del ticket.
- Mantener la explicacion de `review_packets` y `observations.jsonl.bak.*` como superficies por archivo.

### Paso 2 - barrera de regresion semantica
- Anadir/ajustar tests en `tests/unit/test_prune_runtime_retention.py` para bloquear dos regresiones:
  1. que el texto vuelva a sugerir "ultimo intento logico" para `reviews/`;
  2. que alguien cambie silenciosamente la semantica de orden de `reviews/` sin decision explicita.
- La barrera debe seguir siendo hermetica y no usar el workspace vivo como fixture.

### Paso 3 - no derivar el alcance
- Verificar que packets/baks siguen con su contrato existente y que el ticket no se convierte en un rediseno del algoritmo general ni del closeout.
- Si la unica forma de hacer la semantica honesta exige cambiar el algoritmo, eso es CONTRACT_GAP, no scope creep.

## Files Likely Touched (relativos a repo_motor)
- `scripts/prune_runtime_retention.py`
- `tests/unit/test_prune_runtime_retention.py`

Aclaraciones (no parte de las rutas):
- `scripts/prune_runtime_retention.py`: solo help/docstring/salida y, si hace falta, comentarios o nombres locales para hacer visible la semantica actual de `reviews/`.
- `tests/unit/test_prune_runtime_retention.py`: nuevas barreras nominales para ayuda/semantica de `reviews/`; no abrir una segunda familia de tests ni tocar suites ajenas.

## Forbidden Surfaces
- `repo_motor/.agent/agent_controller.py`, `repo_motor/bus/**`, `repo_motor/runtime/**`: fuera de scope; `013v` no toca lifecycle, bus ni estado operativo.
- `repo_motor/scripts/run_pytest_safe.py`: gate canonico read-only.
- `repo_motor/scripts/memory_consolidate.py`, `repo_motor/scripts/migrate_observations.py`, `repo_motor/bus/review_bridge.py`, `repo_motor/bus/review_report.py`: productores read-only; no mover la semantica ahi.
- `review_packets` / `observations.jsonl.bak.*` mas alla de texto compartido indispensable: este ticket no redisena su orden.
- wiring automatico con `session-close`, `mark-ready`, `manager-approve` o launcher: prohibido.
- `privada/`, `.env*`, credenciales, tokens y configuraciones sensibles: fuera de scope absoluto.

## Bateria focal (primer loop; NO la suite canonica completa hasta el cierre)
```
python -m pytest tests/unit/test_prune_runtime_retention.py -q
python scripts/prune_runtime_retention.py --help
python scripts/prune_runtime_retention.py --project-root <repo_destino> --dry-run --keep-reviews 20 --keep-packets 20 --keep-observation-baks 10
# Cierre canonico:
python scripts/run_pytest_safe.py --level all
```

## Non-goals
- NO cambiar el algoritmo de orden de `reviews/` a "archivo mas reciente dentro del dir" en esta ronda.
- NO tocar la politica de `review_packets` ni de `observations.jsonl.bak.*` mas alla de mantener una explicacion coherente.
- NO cablear la utilidad al closeout, al controller ni a productores de runtime.
- NO reabrir `013l`, `013k` o `013t`.

## CONTRACT_GAP / STOP
- Si hacer honesta la semantica exige cambiar el algoritmo de orden de `reviews/` en lugar de documentarlo.
- Si aparece una dependencia no prevista con `review_packets`, `observations.jsonl.bak.*`, historico versionado o closeout.
- Si el codigo real no usa `mtime` de directorio y la premisa del ticket resulta falsa.
-> emite `.agent/planning/contract_gaps/CG-WOT-2026-013v.md` y PARA.

## DoD (binario, comandos exactos)
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionDocs::test_help_makes_directory_mtime_semantics_explicit -q` pasa y el help deja claro que `reviews/` se ordena por el `mtime` del DIRECTORIO del ticket.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionDocs::test_reviews_semantics_do_not_claim_last_logical_attempt -q` pasa; si el texto vuelve a sugerir "ultimo intento logico" o una semantica por archivo interno, FALLA.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_review_directories_are_ranked_by_directory_mtime_not_nested_file_mtime -q` pasa; si alguien reinterpreta `reviews/` por archivo interno sin decision explicita, FALLA.
- [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_keep_count_prunes_old_review_and_packet_entries -q` sigue pasando para confirmar que packets/baks conservan su politica existente y el ticket no deriva el algoritmo general.
- [ ] `python -m ruff check scripts/prune_runtime_retention.py tests/unit/test_prune_runtime_retention.py` -> `All checks passed`.
- [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>` -> `0 errors / 0 warnings`.

## Handoff
Commit productivo en repo_motor (mensaje con `WOT-2026-013v`), suite canonica fresca al HEAD, luego `--pre-handoff` + `--mark-ready`. NO push hasta OK humano.
