# AUDIT_WOT-2026-010j -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] `deliverable_type` sigue siendo `analysis`; no hubo drift a ticket code.
- [ ] El diff productivo del motor se limita al reporte durable del ticket.
- [ ] No se tocaron `scripts/run_pytest_safe.py`, `scripts/run_gates_dispatch.py`,
      `pytest.ini`, `pyproject.toml` ni otros modulos productivos.

## Evidencia minima

- [ ] Existe evidencia del comando de medicion:
      `python scripts/run_pytest_safe.py --level all -- --durations=50`
- [ ] El reporte durable existe en
      `repo_motor/docs/test_performance/test_performance_baseline_WOT-2026-010j.md`.
- [ ] La existencia del reporte se verifico por lectura o check compatible con
      el entorno, no solo por encoding guard.
- [ ] `check_encoding_guard.py` pasa sobre el reporte y el packet tocado.

## Calidad del reporte

- [ ] Incluye tiempo total, top tests lentos y top modulos/familias lentas.
- [ ] Incluye conteos de `subprocess`, `git`, filesystem real, controller/bus,
      `integration` y `slow`.
- [ ] Distingue hechos verificados de inferencias.
- [ ] La hipotesis `subprocess`/`git` queda confirmada o refutada
      explicitamente; no queda cristalizada por repeticion.
- [ ] La recomendacion del siguiente ticket ejecutable se apoya en los datos
      del reporte.

## Gates de cierre

- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- [ ] No se introdujeron warnings de scope o drift por preparar el packet.

## Anti-patrones a rechazar (Manager)

- Reporte guardado solo en `repo_destino` o en memoria runtime.
- Medicion hecha con `unit` o con filtros que impidan ver la suite completa.
- Conclusiones de optimizacion presentadas como hechos sin medicion.
- Claim "reporte creado" sostenido solo por exit code o encoding.
