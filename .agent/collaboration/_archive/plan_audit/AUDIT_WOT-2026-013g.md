# AUDIT_WOT-2026-013g -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] `deliverable_type` sigue siendo `analysis`; no hubo drift a ticket code.
- [ ] El diff productivo del motor se limita al reporte durable de `013g`.
- [ ] No se tocaron `tests/unit/test_detect_version.py`, producto Python, runner, `pytest.ini` ni CI.

## Evidencia minima

- [ ] Existe el reporte durable en `repo_motor/docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`.
- [ ] El reporte distingue [V] verificado de [I] inferencia.
- [ ] Las mediciones usadas para la conclusion son reproducibles y estan documentadas con comandos exactos.
- [ ] `execution_log.md` contiene la linea final contractual de artefacto + validate.

## Calidad del reporte

- [ ] Explica la mayor parte del coste observado o cierra explicitamente `sin optimizacion segura`.
- [ ] No presenta output historico no reconciliado como sustituto de medicion fresca.
- [ ] La recomendacion final no exige tocar test/producto dentro de este ticket.

## Gates de cierre

- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- [ ] No se introdujeron drift o warnings por bootstrappear el packet nuevo.

## Anti-patrones a rechazar (Manager)

- Causa presentada como hecho sin medicion comparable.
- Diff de codigo escondido en un ticket `analysis`.
- Recomendacion de optimizacion que en realidad requiere editar el test o producto en esta misma ronda.
