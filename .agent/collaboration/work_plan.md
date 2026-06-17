# Work Plan: WOT-2026-010l

> Origen: `run_pytest_safe.py` ya acepta subsets manuales, `010j` midio los
> hotspots reales, `010i` endurecio el packet de review y `010q` cerro el gap
> de handoff full-suite. Toca introducir iteracion focal rapida sin reabrir
> falsos verdes.

## Metadata

- **ID:** WOT-2026-010l
- **Contract ID:** T-010L-001
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010j (completed-via-010n), WOT-2026-010i (completed), WOT-2026-010q (completed)

## Objetivo

Crear un selector focal por diff para `run_pytest_safe.py` que proponga un
subset reproducible de tests para iteracion local del Builder y falle abierto a
la suite canonica completa cuando no pueda demostrar cobertura segura. El cambio
no debe alterar la politica de handoff: `010q` sigue exigiendo `level=all` +
`args_mode=default_discovery` para `--mark-ready`.

## Hechos verificados

- `scripts/run_pytest_safe.py` ya distingue `default_discovery` frente a
  `explicit_args` y registra ambos en `last-run.json`.
- `010q` ya bloquea handoff si la ultima corrida no fue `level=all` con
  `args_mode=default_discovery`; `010l` no debe duplicar ni relajar esa barrera.
- `010i` ya endurecio Forbidden Surfaces y commit-visible; el ticket puede
  concentrarse en seleccion focal y fail-open.
- `010j` ya produjo baseline durable y `010k` ya redujo hotspots reales; este
  ticket es de ergonomia de iteracion, no de performance base.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar codigo:

- donde vive hoy el parsing de args y el target por defecto en
  `scripts/run_pytest_safe.py`;
- que seam reutilizar para diff real (`scope_gate.get_changed_files()` o helper
  equivalente) sin abrir un parser git paralelo;
- que tests existentes cubren `args_mode`, fallback a suite canonica y runner
  dispatch;
- que archivos deben considerarse `troncales` para fail-open inmediato;
- como dejar un reporte corto y durable del selector en
  `docs/test_performance/test_selection_WOT-2026-010l.md`.

Registrar en `execution_log.md`:

- seams confirmados;
- decision de mapeo archivo->tests o razon de helper nuevo;
- cualquier desviacion de scope detectada antes de tocar codigo.

## Files Likely Touched

### repo_motor
- `scripts/run_pytest_safe.py`
- `scripts/test_selection.py`
- `tests/unit/test_run_pytest_safe.py`
- `tests/test_pre_handoff_guard.py`
- `tests/unit/test_run_gates_dispatch.py`
- `docs/test_performance/test_selection_WOT-2026-010l.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010l.md`
- `.agent/collaboration/AUDIT_WOT-2026-010l.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`

## Read/inspect only

- `pytest.ini`
- `pyproject.toml`
- `.agent/agent_controller.py`
- `scripts/run_gates_dispatch.py`
- `.agent/scope_gate.py`
- `scripts/pre_handoff_guard.py`
- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
- `docs/test_performance/test_performance_followup_WOT-2026-010k.md`

## Manager-only

- verificar que el diff no relaja `010q` ni el contrato de cierre canonico;
- verificar que el selector replega a suite canonica cuando el mapeo es vacio,
  inseguro o estructural;
- `validate --json --project-root <repo_destino>` final en 0/0.

## Decision Arquitectonica

- El selector focal es ergonomia local de iteracion; no es evidencia valida de
  handoff canonico por si mismo.
- El diff real debe consumirse desde seams existentes del motor, no desde un
  parser git paralelo improvisado.
- Los casos inseguros fallan abierto a la suite canonica completa con razon
  auditable.
- Si el selector necesita heuristicas nuevas, deben ser explicables en codigo y
  cubiertas por tests de barrera.

## Criterios Binarios

- [ ] Consume diff real y produce una lista reproducible de tests candidatos.
- [ ] Si `git diff` falla, si hay cambios en archivos troncales
      (`pyproject.toml`, `pytest.ini`, `.agent/**`), si el mapeo seguro no
      existe o si el set resuelto es vacio, falla abierto a la suite canonica
      completa con razon auditable.
- [ ] No cambia el contrato de cierre de `010c` ni debilita `010q`: el handoff
      sigue exigiendo `level=all` y `args_mode=default_discovery`.
- [ ] Incluye tests de barrera para diff fallido, archivo troncal,
      resolucion vacia y mapeo parcial/inseguro.
- [ ] Documenta como invocar el selector y como detectar cuando replega a suite
      canonica.
- [ ] No introduce cache pytest, xdist/sharding, servicios externos ni cambios
      de CI.
- [ ] Tests focales del area tocada pasan, `ruff check` aplica sobre Python
      tocado, encoding guard pasa sobre artefactos Markdown/Python tocados y
      `validate --json --project-root <repo_destino>` termina 0/0.

## Non-goals

- NO cambiar el contrato de cierre de WOT-2026-010c.
- NO relajar `010q` ni el schema de `last-run.json`.
- NO activar cache de resultados, xdist, sharding ni SaaS externos.
- NO convertir el selector focal en requisito de Manager o de closeout.
- NO mezclar este ticket con optimizaciones de performance adicionales.

## Forbidden Surfaces

- cache pytest
- xdist/sharding
- politica Manager/Builder de handoff
- schema de `last-run.json`
- pass-open silencioso
- herramientas IA externas o SaaS
- bus editado manualmente
- `privada/`
- `.env`
