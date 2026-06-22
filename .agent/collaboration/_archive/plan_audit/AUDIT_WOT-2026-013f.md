# AUDIT_WOT-2026-013f -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] `deliverable_type` sigue siendo `code`; no hubo drift a ticket documental o de runner.
- [ ] El diff productivo del motor se limita a borrar `tests/deprecated/` y actualizar `tests/integration/RETIRED_TESTS.md`.
- [ ] No se tocaron `pytest.ini`, `scripts/run_pytest_safe.py`, `scripts/cleanup_legacy.py`, `tests/test_goose_native_skill.py`, `tests/unit/test_ejemplo.py`, CI/workflows ni producto fuera del scope declarado.
- [ ] No se mezclo `013f` con `013g` ni con FU-013E-1.

## Evidencia minima

- [ ] `execution_log.md` registra el collect-only pre y post con el mismo conteo (3111).
- [ ] `tests/integration/RETIRED_TESTS.md` documenta explicitamente que los tests retirados cubrian Goose y ya estaban excluidos del runner.
- [ ] La ausencia de consumidores vivos de `tests/deprecated/` se justifico con lectura/codigo, no por intuicion.
- [ ] El packet deja claro que `scripts/cleanup_legacy.py` apunta al antiguo `scripts/test_goose_realworld.py`, no al directorio retirado.

## Gates de cierre

- [ ] `python scripts/run_pytest_safe.py --level all` termina verde y la evidencia canonica reconcilia `tested_commit_sha == HEAD`.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- [ ] No se introdujeron drift o warnings por bootstrappear el packet de `013f`.

## Anti-patrones a rechazar (Manager)

- Borrado del directorio sin dejar trazabilidad en `tests/integration/RETIRED_TESTS.md`.
- Claims de "no afecta al runner" sin collect-only pre/post registrado.
- Ensanchamiento de scope hacia `pytest.ini`, Goose legacy vecino o producto vivo.
- Cualquier borrado ejecutado pese a encontrar un consumidor canonico de `tests/deprecated/`.
