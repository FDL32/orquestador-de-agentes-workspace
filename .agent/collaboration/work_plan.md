# Work Plan: WOT-2026-010f

> Origen: durante la review final de WOT-2026-010c se detecto que HEAD tenia un
> tag extra `checkpoint/review-none` junto al M3 correcto. No bloqueo 010c
> porque la gate valida el tag del ticket correcto, pero `review-none` indica una
> ruta que crea checkpoints con `plan_id="none"`. Investigacion 2026-06-17
> confirma que la ruta SIGUE VIVA: el tag se recreo durante el handoff de 010d.

## Metadata

- **ID:** WOT-2026-010f
- **Contract ID:** T-010F-001
- **Estado:** READY_TO_START
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010c (cerrado/COMPLETED)

## Pre-launch note

- `STATE.md` mostrara `WOT-2026-010d / COMPLETED` hasta que 010f emita
  `STATE_CHANGED` al bus. El arranque canonico ocurre tras esta auditoria.
- `TURN.md` debe leerse como preparacion de packet, no como ticket activo.

## Objetivo

Eliminar la creacion de tags `checkpoint/review-none` cerrando la ruta viva que
los produce, sin tocar checkpoints validos. Dejar barrera que falle si un
checkpoint M3 se intenta crear con un `plan_id` no valido (`none`, `n/a`,
`unknown`, vacio).

Frase guia: "Un checkpoint con ticket `none` es ruido operativo que puede
ocultar drift de bus o bootstrap; el handoff debe fallar fail-closed antes de
crear un tag sin ticket valido."

## Root cause (VERIFICADO en codigo 2026-06-17, ampliado tras Manager CHANGES B1)

Patron de guard DEBIL duplicado a lo largo de `.agent/agent_controller.py`. Solo
**un** guard es fuerte; el resto son debiles.

- **Guard FUERTE (unico):** linea 1780 (validacion CONTRACT_GAP) rechaza
  `ticket_id.lower() in ("n/a", "none", "unknown", "")`.
- **Guards DEBILES: 17 ubicaciones** (verificado por grep `== "N/A"`, no 2 ni 9).
  Dos formas equivalentes del mismo defecto:
  - `plan_id == "N/A"` / `current_plan_id == "N/A"` (9 ocurrencias).
  - `ticket_id == "N/A"` (8 ocurrencias).
  Las 17 dejan pasar `"none"` y `"unknown"` (solo bloquean `""` y `"N/A"`).
  Conteo verificado: `grep -c 'plan_id == "N/A"'` = 9, `grep -c 'ticket_id ==
  "N/A"'` = 8 -> 17 debiles + 1 fuerte (linea 1780) = 18 sitios de validacion.
  El Builder debe localizar las 17 por grep en el momento de implementar (los
  numeros de linea se desplazan al editar) y migrar las 17.

`get_plan_id` (`.agent/state_validation.py:62`) devuelve el texto tras `**ID:**`
o `"N/A"`. El seed neutro del motor documenta `ID=none` (state_validation.py:95,
`is_seed_neutral_state`). Por tanto, con un work_plan `**ID:** none`,
`plan_id="none"` pasa el guard debil. En `_handle_pre_handoff` (3314) eso llega a
la creacion de tag (`tag_name = f"checkpoint/review-{plan_id}"`, linea 3659;
creado en 3767) y materializa `checkpoint/review-none`.

Clasificacion de riesgo de los 18 guards debiles por tipo de efecto:

| Linea | Funcion | Tipo | Riesgo si plan_id="none" pasa |
|------|---------|------|-------------------------------|
| 2778 | `_handle_mark_ready` | Creacion (eventos/artefactos) | Alto |
| 3173 | `_handle_bootstrap_ticket` | Creacion (bus events) | Alto |
| 3314 | `_handle_pre_handoff` | Creacion (checkpoint tag) | Alto (este ticket) |
| 3879 | `_check_bus_drift` | Query | Bajo |
| 3988 | `_check_invariants` | Query | Bajo |
| 4273/4287 | `_handle_manager_approve` | Mutacion/cierre | Alto |
| 4499/4509 | `_handle_escalate_human_gate` | Mutacion | Medio |
| 4566 | `_handle_resume_human_gate` | Mutacion | Medio |
| 4636 | `_handle_pause_ticket` | Mutacion | Medio |
| 4819 | `_handle_resume_ticket` | Mutacion | Medio |
| 4949 | `_handle_abort_paused_ticket` | Mutacion | Medio |
| 5035 | `_handle_reopen_terminal_ticket` | Mutacion | Medio |
| 5189/5201 | `_handle_request_changes` | Mutacion | Medio |
| 5755 | `_handle_get_closeout_skip` | Query | Bajo |

Evidencia de ruta viva: `checkpoint/review-none` (objeto tag `8352c64`) apunta al
commit `eda918f` ("WOT-2026-010d: Final formatting and linting"), del ciclo de
010d. Es ruta viva recreada en este ciclo, no artefacto historico unico.

## Decision de alcance (Manager CHANGES B1 -> opcion (a))

Se adopta la **opcion (a)**: este ticket reemplaza las **18** ocurrencias del
guard debil con `is_invalid_plan_id()`, consumiendo la constante compartida
`INVALID_PLAN_IDS`. Es un refactor mecanico que NO cambia el comportamiento de
las rutas con ticket valido (un ticket real nunca esta en `INVALID_PLAN_IDS`),
pero blinda como efecto colateral beneficioso las rutas de creacion/mutacion
(mark-ready, bootstrap, manager-approve, pause/resume/abort, request-changes).
La barrera de test PRINCIPAL sigue siendo la ruta de checkpoint (pre-handoff);
se anade ademas un test de no-regresion para `_handle_mark_ready` con
`plan_id="none"`. Se descarta la opcion (b) porque importar la constante y
usarla en 1 de 18 sitios dejaria el codigo en estado peor (inconsistente).

## Decision Arquitectonica

- **Fuente unica de verdad:** extraer el conjunto de IDs invalidos a una
  constante compartida `INVALID_PLAN_IDS = frozenset({"", "n/a", "none",
  "unknown"})` en `state_validation.py`, con helper `is_invalid_plan_id(pid)`
  que normaliza (`pid.strip().lower()`). La duplicacion del literal fue la causa
  raiz; la constante la elimina.
- **Fail-closed en los 18 guards:** reemplazar cada guard debil
  (`if not X or X == "N/A":`) por `if is_invalid_plan_id(X):`. En las rutas de
  creacion/mutacion, salir con error ANTES de cualquier efecto (tag, evento,
  mutacion de estado). En las rutas query, el cambio solo refuerza el early-return
  sin cambiar el resultado para tickets validos.
- **No tocar checkpoints validos:** un ticket real nunca esta en
  `INVALID_PLAN_IDS`; `checkpoint/review-<ticket>` y cada ruta con ticket
  valido conserva su comportamiento exacto.
- **Limpieza del tag existente:** `checkpoint/review-none` se elimina SOLO tras
  verificar que no es referenciado por bus, backlog ni archive. Es un tag local
  (no hay evidencia de push); borrado con `git tag -d checkpoint/review-none`.
- **NO confundir con:** la gate de suite-green (010c), el scope gate, ni la
  barrera work_plan-committed (009g). Esta es una correccion de la ruta de
  creacion de checkpoint, independiente de esas gates.

## Orden de ejecucion (obligatorio, TDD)

1. **Tests de barrera PRIMERO:** (a) con work_plan `**ID:** none`,
   `_handle_pre_handoff` debe FALLAR fail-closed y NO crear tag; (b)
   `_handle_mark_ready` con `plan_id="none"` no emite eventos de bus. Ambos deben
   fallar sin el fix.
2. Extraer `INVALID_PLAN_IDS` + `is_invalid_plan_id` en `state_validation.py`.
3. Refactorizar el guard fuerte de linea 1780 para consumir el helper (sin
   cambiar comportamiento).
4. Reemplazar las 17 ocurrencias del guard debil por `is_invalid_plan_id(...)`.
   Mecanico: 9 con `plan_id`/`current_plan_id` + 8 con `ticket_id`. Localizar por
   grep `== "N/A"` en el momento de editar; migrar las 17 (grep final == 0).
5. Limpiar el tag `checkpoint/review-none` tras verificar cero referencias vivas.
6. Gates + cierre canonico.

## Files Likely Touched

### repo_motor
- `.agent/agent_controller.py`
- `.agent/state_validation.py`
- `tests/unit/test_pre_handoff_checkpoint.py`
- `tests/test_get_closeout_skip.py`

Notas (no son parte del FLT parseable):
- `tests/test_get_closeout_skip.py`: test colateral. _handle_get_closeout_skip
  (linea ~5756) es uno de los 17 guards migrados; sus tests dependian de que el
  seed neutro "none" llegara a la logica del bus. Se actualizan para inyectar un
  plan_id valido (su intencion es testear la derivacion del bus, no el guard) y
  se parametriza el caso de id invalido. Tocar este test es consecuencia directa
  del fix, no scope creep.
- `.agent/agent_controller.py`: migrar los 17 guards debiles
  `(plan_id|ticket_id|current_plan_id) == "N/A"` a `is_invalid_plan_id()`
  (localizar por grep, NO por numero de linea; son 17 + el fuerte de 1780). No
  tocar la logica de creacion de tag/eventos mas alla del guard previo.
- `.agent/state_validation.py`: anadir constante `INVALID_PLAN_IDS` y helper
  `is_invalid_plan_id(pid)`. Nota de nomenclatura: el helper recibe tanto
  `plan_id` como `ticket_id`; el nombre mantiene la nomenclatura de la constante
  `INVALID_PLAN_IDS` ya establecida, su semantica real es "cualquier ID de
  ticket/plan que no designa un ticket real". No renombrar para no romper la
  convencion.
- `tests/unit/test_pre_handoff_checkpoint.py` (nuevo): barreras que demuestran
  que `plan_id` invalido no crea tag (pre-handoff) ni emite eventos (mark-ready).

## Read/inspect only

- `scripts/create_checkpoint.py` (`MILESTONE_TAGS["M3"]`; consumidor del
  ticket_id, NO reimplementar).
- `scripts/pre_handoff_guard.py` (valida M3 existente; no es quien lo crea con
  plan_id none).
- `git tag -l "checkpoint/review-*"` como inventario de referencia.

## Manager-only

- Ejecutar `python scripts/run_pytest_safe.py -- -m "not integration and not slow"`
  desde `repo_motor` y leer hasta `0 failed`.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  final 0/0.
- Verificar que `git tag -l "checkpoint/review-none"` no devuelve nada al cierre.

## Tests Esperados (en `tests/unit/test_pre_handoff_checkpoint.py`)

- Con `plan_id="none"`, `_handle_pre_handoff` NO crea tag y falla fail-closed
  (barrera principal: hoy crea `review-none`).
- Parametrizado: `plan_id` en `"N/A"`, `""`, `"unknown"` -> igualmente bloqueado.
- Con `plan_id` valido (`WOT-2026-999z`): `checkpoint/review-<ticket>` se crea
  normalmente (no-regresion).
- `_handle_mark_ready` con `plan_id="none"` NO emite eventos de bus (test de
  no-regresion de la 2da ruta de creacion de alto riesgo; sugerencia Manager).
- `is_invalid_plan_id`: tabla de verdad (`none/N/A/""/unknown/" None "` -> True;
  `WOT-2026-001a` -> False). Verifica normalizacion `strip().lower()`.
- `INVALID_PLAN_IDS` es la unica fuente: test que importa la constante y
  verifica contenido; el literal `== "N/A"` ya no aparece inline en
  `agent_controller.py` (grep == 0 ocurrencias del patron debil).

## Criterios Binarios

- [ ] Existe `INVALID_PLAN_IDS` + `is_invalid_plan_id` en `state_validation.py`.
- [ ] Las **17** ubicaciones del guard debil consumen `is_invalid_plan_id(...)`;
      el patron `(plan_id|ticket_id|current_plan_id) == "N/A"` ya no aparece
      inline en `agent_controller.py` (grep == 0). El guard fuerte (1780) tambien
      lo consume.
- [ ] `--pre-handoff` con `plan_id` invalido (`none/n/a/unknown/""`) falla
      fail-closed ANTES de crear ningun tag.
- [ ] `_handle_mark_ready` con `plan_id="none"` no emite eventos de bus.
- [ ] Test de barrera: con `plan_id="none"` no se crea tag; FALLA sin el fix.
- [ ] `checkpoint/review-<ticket>` con ticket valido sigue creandose (no-regresion).
- [ ] `checkpoint/review-none` eliminado tras verificar cero referencias en
      bus/backlog/archive.
- [ ] `git tag -l "checkpoint/review-none"` vacio al cierre.
- [ ] `ruff check .` exit 0.
- [ ] Tests focales exit 0.
- [ ] `run_pytest_safe -- -m "not integration and not slow"` leido hasta `0 failed`.
- [ ] `validate --json --project-root <repo_destino>` exit 0, 0 errors.

## Non-goals

- NO reescribir la politica M3 completa ni el resto de milestones (M0/M1/M2/M4).
- NO tocar la gate de suite-green (010c), scope gate ni work_plan-committed (009g).
- NO borrar otros tags `checkpoint/review-*` validos.
- NO tocar WOT-2026-010d, 010e, 010g, 010h, 010i ni 008d.
- NO normalizar `plan_id="none"` a otra cosa: el contrato es RECHAZARLO, no
  traducirlo.

## Forbidden Surfaces

- `scripts/create_checkpoint.py` salvo lectura (no reimplementar M3).
- `scripts/pre_handoff_guard.py` (valida, no crea; fuera de scope).
- `bus/state_machine.py`.
- `privada/` y `.env`.
- Scope de 010d, 010e, 010g, 010h, 010i, 008d.
