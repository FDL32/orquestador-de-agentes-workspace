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

## Fase 0 - Pendiente

El Builder debe confirmar:

- fuentes de performance previas
- comando exacto de durations
- superficie canonica para la regla foreground/background

## Gates esperados

- existencia del reporte `docs/test_performance/test_performance_variance_WOT-2026-010p.md`
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
