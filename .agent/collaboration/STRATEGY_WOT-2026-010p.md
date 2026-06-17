# STRATEGY_WOT-2026-010p -- Varianza de suite y foreground/background

## Hechos verificados

- La diferencia `43min` vs `~6min` observada en `010o` se explica mejor como
  espera operativa del agente que como tiempo real de pytest.
- Aun asi, conviene capturar durations sobre HEAD actual antes de abrir
  optimizaciones como `010l`.

## Plan tecnico

1. Revisar reportes previos de performance (`010j`, `010k`) y `last-run.json`.
2. Ejecutar al menos una corrida:
   `python scripts/run_pytest_safe.py --level all -- --durations=50`.
3. Guardar wall-clock total y top durations en
   `docs/test_performance/test_performance_variance_WOT-2026-010p.md`.
4. Repetir una segunda corrida comparable solo si la primera termina en menos
   de 10 minutos wall-clock; si tarda 10 minutos o mas, documentar STOP
   `segunda_corrida_omitida_por_coste`.
5. Documentar en `INTERACTION_MODES.md` la regla operacional:
   foreground para suites esperadas <10 min; background solo con progreso
   verificable.

## Riesgos

- **Medicion no comparable:** mezclar background/polling con tiempo real.
- **Sobre-scope:** convertir un ticket de analisis en optimizacion.
- **Cristalizacion:** tratar un numero aislado como verdad permanente.

## No hacer

- No cambiar runner/gates/cache.
- No implementar selector focal.
- No tocar xdist/sharding.
