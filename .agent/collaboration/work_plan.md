# Work Plan: WOT-2026-010o

> Origen: durante `WOT-2026-010k` aparecio una flakiness real en
> `tests/test_manager_review_bridge.py` y `tests/test_review_bridge.py` que no
> provenia del diff del ticket, sino del acoplamiento de esos tests al estado
> git vivo del `repo_destino` resuelto via `motor_destination_link.json`.

## Metadata

- **ID:** WOT-2026-010o
- **Contract ID:** T-010O-001
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010k (cerrado)

## Objetivo

Hacer deterministas los tests de evidence-gate en
`tests/test_manager_review_bridge.py` y `tests/test_review_bridge.py` sin
debilitar la logica real de produccion. El fix debe desacoplar la fuente del
estado git inspeccionado por el evidence-gate de modo que la suite ya no
dependa del estado vivo y mutable del `repo_destino` real de esta maquina.

## Hechos verificados

- El hallazgo nace en una corrida intermedia de `run_pytest_safe --level all`
  durante `010k`, con 6 fallos transitorios en los tests de review bridge.
- El diff productivo de `010k` no tocaba `bus/review_bridge.py`,
  `bus/manager_review_bridge.py` ni esos tests de review.
- El comportamiento observado varia con el estado git del `repo_destino` real
  apuntado por `.agent/config/motor_destination_link.json`.
- `010o` es follow-up de determinismo de tests; no cambia la politica real del
  evidence-gate ni reabre el scope de `010k`.

## Fase 0: Diagnostico antes del cambio

Confirmar en codigo antes de editar:

- que los tests nombrados siguen ejercitando el evidence-gate real de
  produccion, directa o indirectamente
- que el acoplamiento al `repo_destino` real entra por una ruta verificable
  (resolver, config o helper), no por una sospecha narrativa
- que existe una via de fixture/repo temporal que mantenga la semantica
  observable (`APPROVE` vs `CHANGES`) sin leer el estado git del destino vivo
- que el FLT incluye todos los tests/helpers que el Builder necesitara tocar

Registrar en `execution_log.md`:

- seam exacto por el que el test llega al `repo_destino` real
- por que el diff de `010k` quedo descartado como causa raiz
- la estrategia elegida para desacoplar el entorno sin mock drift

## Files Likely Touched

### repo_motor
- `tests/test_manager_review_bridge.py`
- `tests/test_review_bridge.py`
- fixture/helper nuevo de repo git temporal solo si elimina la dependencia del
  `repo_destino` vivo y sigue ejerciendo el codigo real de produccion
- `tests/conftest.py` o modulo de fixtures compartido equivalente, solo si es
  la ubicacion minima necesaria

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010o.md`
- `.agent/collaboration/AUDIT_WOT-2026-010o.md`
- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `bus/review_bridge.py`
- `bus/manager_review_bridge.py`
- `.agent/config/motor_destination_link.json`
- `tests/test_pre_handoff_guard.py` si reutiliza helpers de repos git reales
- `docs/test_performance/test_performance_followup_WOT-2026-010k.md`

## Manager-only

- `validate --json --project-root <repo_destino>` final en 0/0
- verificar que el ticket no cambia la politica del evidence-gate, solo el
  aislamiento del entorno de test

## Decision Arquitectonica

- El evidence-gate de produccion se conserva; lo que cambia es la fuente del
  estado git observado por los tests.
- La prueba debe seguir pasando por codigo real de produccion, evitando mocks
  vacios que solo congelen el resultado esperado.
- Si hace falta cambiar la API publica del evidence-gate para poder testearlo,
  el Builder debe detenerse y elevar `CONTRACT_GAP` en vez de forzar un fix mas
  ancho.

## Criterios Binarios

- [ ] Los tests de evidence-gate en ambos archivos pasan de forma reproducible
      sin depender del estado git real del `repo_destino` vivo.
- [ ] Existe al menos un caso `APPROVE` y al menos un caso `CHANGES` contra un
      repo controlado/temporal, no contra el `repo_destino` real.
- [ ] La suite se corre dos veces con estados distintos del `repo_destino` real
      entre medias y estos tests mantienen el mismo resultado.
- [ ] El fix sigue ejerciendo el codigo real del evidence-gate; no degrada el
      test a un mock que solo fije la decision.
- [ ] `ruff check` pasa sobre los Python tocados.
- [ ] `python scripts/run_pytest_safe.py --level all` termina en verde.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors /
      0 warnings al handoff.

## Non-goals

- NO cambiar la politica funcional del evidence-gate.
- NO tocar `.agent/config/motor_destination_link.json` en produccion.
- NO mezclar con optimizaciones de `010k`, selector focal (`010l`) o xdist
  (`010m`).
- NO tocar bus editado manualmente.

## Forbidden Surfaces

- `.agent/config/motor_destination_link.json`
- logica de negocio del evidence-gate fuera de lo estrictamente necesario para
  inyectar o fixturizar el estado de repo si la firma publica se mantiene
- `run_gates_dispatch.py`
- `scripts/run_pytest_safe.py`
- `privada/`
- `.env`
- bus editado manualmente
