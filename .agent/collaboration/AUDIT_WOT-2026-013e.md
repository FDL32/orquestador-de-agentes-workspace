# AUDIT_WOT-2026-013e -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] `deliverable_type` sigue siendo `analysis`; no hubo drift a ticket code.
- [ ] El diff productivo del motor se limita al reporte durable del ticket.
- [ ] No se tocaron `tests/`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml`, `uv.lock`, CI/workflows ni producto.
- [ ] No se reabrieron `011e`, `010m`, `011i` ni `013d`.

## Evidencia minima

- [ ] Existe el reporte durable en `repo_motor/docs/test_performance/test_suite_audit_WOT-2026-013e.md`.
- [ ] La existencia del reporte se verifico por lectura o check compatible con el entorno, no solo por encoding guard.
- [ ] `execution_log.md` contiene la linea final contractual de artefacto + validate.
- [ ] `python scripts/check_encoding_guard.py docs/test_performance/test_suite_audit_WOT-2026-013e.md` pasa.

## Calidad del reporte

- [ ] Inventaria la suite por familias o subsistemas con conteo auditable.
- [ ] Clasifica cada familia como `core regression`, `structural gate`, `legacy candidate`, `redundant candidate` o `unknown`.
- [ ] Distingue evidencia verificada de inferencia limitada.
- [ ] Lista tests o familias lentas, marks/skip estructurales, barreras canonicas del runner/handoff y debt legacy detectable.
- [ ] Los follow-ups propuestos son pequenos, verificables y con superficie acotada.
- [ ] El reporte deja explicito que `013e` no borra ni relaja tests.

## Gates de cierre

- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- [ ] No se introdujeron drift o warnings por bootstrappear el nuevo packet.

## Anti-patrones a rechazar (Manager)

- Clasificaciones presentadas como hechos sin evidencia suficiente.
- Recomendaciones de poda masiva o mezcla de runner, CI y producto en un solo follow-up.
- Claims de artefacto creados sostenidos solo por exit code o encoding.
- Cualquier ensanchamiento de scope que evite emitir `CG-WOT-2026-013e.md` cuando la premisa cae.
