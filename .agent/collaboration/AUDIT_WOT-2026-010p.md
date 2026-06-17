# AUDIT_WOT-2026-010p -- Criterios de auditoria

## Contrato estructural

- [ ] El ticket produce reporte de analisis, no cambios de runner.
- [ ] La regla foreground/background queda documentada en una superficie
      operacional canonica.
- [ ] No se tocan forbidden surfaces.

## Evidencia minima

- [ ] Existe `docs/test_performance/test_performance_variance_WOT-2026-010p.md`.
- [ ] El reporte contiene comando exacto, wall-clock, `exit_code`,
      `tested_commit_sha`, `level`, `args_mode` y top durations.
- [ ] Si solo hay una corrida, el STOP de segunda corrida esta justificado.
- [ ] La conclusion esta clasificada como una de las categorias del contrato.
- [ ] `validate --json` termina 0/0.

## Anti-patrones a rechazar

- Optimizar tests dentro de este ticket.
- Usar tiempo de espera del agente como tiempo de pytest.
- Proponer `010l` sin reconocer que `010q` ya blindo el handoff.
