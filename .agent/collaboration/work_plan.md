# Work Plan: WOT-2026-010k

> Origen: `WOT-2026-010j` midio la suite real y refuto la premisa vieja de
> `git/subprocess` como hotspot dominante. El siguiente paso no es atacar a
> ciegas un tiempo arbitrario, sino reducir el tiempo wall-clock medido (en
> segundos) de hotspots reales de filesystem/scan y setup repetido.

## Metadata

- **ID:** WOT-2026-010k
- **Contract ID:** T-010K-001
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010j, WOT-2026-010n (cerrados)

## Objetivo

Reducir tiempo de suite atacando dos hotspots reales de filesystem/scan:
`tests/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project`
y `tests/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms`,
sin relajar la suite canonica, sin cambiar politica de gates y sin convertir
tests utiles en atajos cosmeticos. La mejora debe quedar medida como delta de
tiempo wall-clock de esos dos tests y de su suite focal directa, comparando
before/after en el mismo entorno y con el mismo comando.

## Hechos verificados

- `010j` identifico que el coste dominante no era `git/subprocess`.
- Los dos hotspots priorizados por este ticket son:
  - `tests/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project`
  - `tests/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms`
- `010n` ya resolvio el gate que bloqueaba tickets con artefactos en
  `repo_motor`; no hay que mezclar ese problema aqui.

## Fase 0: Diagnostico antes del cambio

Confirmar en codigo antes de editar:

- que esos dos tests aparecen en el reporte de `010j` con tiempos
  `162.29s` y `61.99s`
- que el cambio propuesto no elimina como API observable el scan real o la
  lectura real que esos tests deben seguir validando
- que existe una barrera roja->verde viable y una medicion before/after
  comparable con el mismo comando, mismo entorno y mismo subset focal

Registrar en `execution_log.md`:
- tiempo before de `test_scan_current_project`
- tiempo before de `test_repo_has_no_live_retired_topology_terms`
- razon de no tocar otros outliers en esta ronda

## Files Likely Touched

### repo_motor
- `tests/test_project_scanner.py`
- `tests/test_no_legacy_topology_terms.py`
- helper o fixture compartida nueva solo si elimina setup repetido de esos dos
  tests concretos
- `docs/test_performance/test_performance_followup_WOT-2026-010k.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
- `scripts/run_pytest_safe.py`
- `pytest.ini`
- `.agent/agent_controller.py`
- tests relacionados no modificados

## Manager-only

- `validate --json --project-root <repo_destino>` final en 0/0
- verificar que el before y el after se midieron con el mismo comando focal,
  mismo entorno local y mismo commit del codigo bajo prueba

## Decision Arquitectonica

- El ticket se re-scopea explicitamente: no persigue ya `git/subprocess` como
  blanco principal, porque `010j` lo refuto con medicion real.
- La optimizacion debe ser local y semanticamente conservadora: reducir el
  tiempo (segundos wall-clock) de setup o scan donde el comportamiento
  completo no sea la API observable del test.
- Si para ganar tiempo hace falta cambiar politica de runner, cache, selector
  focal o paralelizacion, eso ya no es `010k` y debe bloquearse.

## Criterios Binarios

- [ ] Solo optimiza `test_scan_current_project`,
      `test_repo_has_no_live_retired_topology_terms` o sus fixtures directas.
- [ ] La optimizacion se centra en filesystem/scan o setup repetido de esos dos
      tests; no reabre la hipotesis `git/subprocess` sin evidencia nueva.
- [ ] Mantiene tests de contrato que validan comportamiento real del subsistema
      optimizado cuando ese comportamiento es la API observable.
- [ ] Cada helper/fixture nueva que sustituya setup caro queda cubierta por al
      menos un smoke test sin el shortcut correspondiente.
- [ ] Demuestra mejora con medicion before/after bajo condiciones comparables
      del mismo entorno, indicando comando exacto, tiempo before, tiempo after
      y delta wall-clock de esos dos tests o de su suite focal directa; el
      before y el after usan el mismo comando focal, mismo entorno local y
      mismo commit del codigo bajo prueba salvo el diff del ticket.
- [ ] No reduce cobertura semantica ni introduce falso-verde.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors /
      0 warnings al handoff.

## Non-goals

- NO tocar `run_gates_dispatch.py` ni politica Builder/Manager.
- NO introducir cache de resultados pytest.
- NO paralelizar la suite.
- NO mezclar selector focal, sharding o cambios de CI.

## Forbidden Surfaces

- `run_gates_dispatch.py`
- politica Builder/Manager
- cache de pytest
- paralelizacion/xdist
- `privada/`
- `.env`
- bus editado manualmente
