# Execution Log: WOT-2026-010p - Varianza de suite y foreground/background

## Metadata

**Estado:** IN_PROGRESS
- **ID:** WOT-2026-010p
- **Contract ID:** T-010P-001
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- `WOT-2026-010o` cerro canonico y mostro confusion entre espera de herramienta
  y tiempo real de pytest.
- `WOT-2026-010q` cerro canonico y blindo el handoff para exigir suite real.

## Fase 0 - COMPLETADA

### Seams confirmados

- `docs/test_performance/` existe con `010j` y `010k` como antecedentes.
- Comando exacto: `python scripts/run_pytest_safe.py --level all -- --durations=50`
- `INTERACTION_MODES.md`: no tenia regla foreground/background — se anade.
- `last-run.json` de 010q (HEAD 849e7d52): corrida sin `--durations`, duracion
  observable `15:18:00 -> 15:24:09` = 6m09s confirma el rango esperado.

## Fase 1 - COMPLETADA

### Corridas ejecutadas

**Corrida 1** — `python scripts/run_pytest_safe.py --level all -- --durations=50`
- Wall-clock: **5m34s** (334.29s pytest)
- exit_code: 0 | level: all | args_mode: default_discovery
- tested_commit_sha: `849e7d52d4153a4904beb812f171c3281acccabb`
- Resultado: 2913 passed, 20 skipped

**Decision:** 5m34s < 10 min → se ejecuta segunda corrida.

**Corrida 2** — mismo comando
- Wall-clock: **5m29s** (329.30s pytest)
- exit_code: 0 | level: all | args_mode: default_discovery
- tested_commit_sha: `849e7d52d4153a4904beb812f171c3281acccabb`
- Resultado: 2913 passed, 20 skipped
- Delta vs C1: -4.99s absoluto / -1.5%

### Artefactos creados

- `docs/test_performance/test_performance_variance_WOT-2026-010p.md` (nuevo)
- `INTERACTION_MODES.md` actualizado con regla foreground/background

### Clasificacion

**Categoria: `entorno/I-O`** — outliers estables entre corridas (delta <5%),
varianza total de 1.5%, no hay hotspot nuevo ni test inestable. Suite estable.

## Gates

- Artefacto existe: `docs/test_performance/test_performance_variance_WOT-2026-010p.md` — SI
- Validate: `python .agent/agent_controller.py --validate --json --project-root repo_destino` -> 0 errors / 0 warnings
- Commit repo_motor: `e5d4a9d` docs(WOT-2026-010p): artefacto creado y regla documentada

## Estado actual

- Current state: WOT-2026-010p READY_FOR_REVIEW
