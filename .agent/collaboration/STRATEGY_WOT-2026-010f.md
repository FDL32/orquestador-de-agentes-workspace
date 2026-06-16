# STRATEGY_WOT-2026-010f -- Limpieza/investigacion de checkpoint/review-none

> Estrategia tecnica del ticket. El scope/FLT/criterios canonicos viven en
> `work_plan.md`; aqui se detalla el COMO sin divergir.

## Hechos verificados (no asumir)

Verificado en `.agent/agent_controller.py`:
- Linea 1780: UNICO guard fuerte; rechaza
  `ticket_id.lower() in ("n/a", "none", "unknown", "")`.
- **17 guards DEBILES** con `(plan_id|ticket_id|current_plan_id) == "N/A"`
  (9 `plan_id`/`current_plan_id` + 8 `ticket_id`). El de `_handle_pre_handoff`
  (3314) es el que crea el tag `review-none`; los demas afectan mark-ready,
  bootstrap, manager-approve, pause/resume/abort, request-changes, queries.
- Linea ~3659: `tag_name = f"checkpoint/review-{plan_id}"`.
- Linea ~3767: `git tag -a {tag_name} -m {tag_msg}` crea el tag.
- Tag `review-none` -> objeto `8352c64` -> commit `eda918f`.

Verificado en `.agent/state_validation.py`:
- `get_plan_id(content) -> str` (linea 62): devuelve texto tras `**ID:**` o
  `"N/A"`.
- `is_seed_neutral_state` (linea 91-105): documenta que el seed neutro del motor
  usa `ID=none` con proyecciones `READY_TO_START`.

Verificado en git:
- `checkpoint/review-none` existe y apunta a commit reciente del ciclo de 010d
  (ruta viva, no artefacto historico unico).
- No hay evidencia de push del tag (es local).

## Cadena causal exacta

1. `work_plan.md` con `**ID:** none` (seed neutro o residual de bootstrap).
2. `get_plan_id` -> `"none"`.
3. `_handle_pre_handoff`: `plan_id="none"` no es `""` ni `"N/A"` -> pasa guard.
4. `tag_name = "checkpoint/review-none"`.
5. `git tag -a checkpoint/review-none` -> ruido operativo.

## Diseno del fix

### Paso 1 - Constante compartida (state_validation.py)

```python
# IDs de plan que NO designan un ticket real; ningun artefacto canonico
# (checkpoint, bus, review packet) debe materializarse para ellos.
INVALID_PLAN_IDS = frozenset({"", "n/a", "none", "unknown"})


def is_invalid_plan_id(plan_id: str) -> bool:
    return plan_id.strip().lower() in INVALID_PLAN_IDS
```

### Paso 2 - Migrar los 17 guards debiles + el fuerte (1780)

Sustituir cada `if not X or X == "N/A":` por `if is_invalid_plan_id(X):`,
preservando el cuerpo (mensaje y return) de cada guard. El de
`_handle_pre_handoff` (3314) queda, por ejemplo:
```python
if is_invalid_plan_id(plan_id):
    print(
        f"[ERROR] Invalid plan_id '{plan_id}': cannot create checkpoint M3 "
        f"without a real ticket. Fix: set a valid **ID:** in work_plan.md.",
        file=sys.stderr, flush=True,
    )
    return 1
```
El guard fuerte de 1780 tambien pasa a `is_invalid_plan_id(ticket_id)`
(comportamiento identico, elimina el literal). Tras migrar, `grep -nE
'(plan_id|ticket_id|current_plan_id) == "N/A"' agent_controller.py` debe dar 0.

IMPORTANTE: localizar las ubicaciones por grep al implementar, NO por numero de
linea fijo: cada edicion desplaza las lineas siguientes.

### Paso 3 - Limpieza del tag existente

```
# Verificar cero referencias vivas
git tag -l "checkpoint/review-none"          # confirma que existe
grep -rn "review-none" .agent/runtime/events .agent/collaboration  # debe ser 0
git tag -d checkpoint/review-none            # borrado local
```
Solo borrar tras confirmar grep vacio. No usar `git push --delete` (no hay
evidencia de que el tag se publicara).

## Testing (TDD)

Archivo: `tests/unit/test_pre_handoff_checkpoint.py`. Usar repo git real en
`tmp_path` (patron `init_git_repo` de `tests/test_pre_handoff_guard.py`), NO
mockear git.

- `test_pre_handoff_blocks_plan_id_none`: work_plan con `**ID:** none` ->
  `_handle_pre_handoff` retorna != 0 y `git tag -l checkpoint/review-none` vacio.
  FALLA sin el fix (hoy crearia el tag).
- `test_pre_handoff_blocks_na_unknown_empty`: parametrizado sobre N/A, "", unknown.
- `test_pre_handoff_allows_valid_ticket`: `**ID:** WOT-2026-999z` -> tag creado.
- `test_mark_ready_blocks_plan_id_none`: `_handle_mark_ready` con `plan_id="none"`
  no emite eventos de bus (2da ruta de creacion de alto riesgo; sugerencia
  Manager). Observar el bus real (events.jsonl) antes/despues, no mockear emit.
- `test_invalid_plan_ids_single_source`: importar `INVALID_PLAN_IDS` /
  `is_invalid_plan_id` y verificar tabla de verdad + normalizacion; el literal
  `== "N/A"` ya no aparece inline en agent_controller (grep == 0).

Anti-patron a evitar: no mockear `_handle_pre_handoff` ni `_handle_mark_ready`
internamente; ejercer la funcion real con un work_plan fixture y observar el
efecto en `git tag` / el bus.

## Relacion con otros tickets

- 010c protege el cierre (suite-green); 010f limpia ruido de checkpoint que
  podria enmascarar drift. Independiente de la cascada de pausa (010d).
- 010i (hardening de packaging/forbidden surfaces) es complementario pero
  SEPARADO: 010f corrige una ruta concreta de creacion de tag; 010i endurece
  gates de review en general. No mezclar.
