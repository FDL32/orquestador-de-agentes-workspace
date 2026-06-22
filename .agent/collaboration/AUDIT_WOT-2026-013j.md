# AUDIT_WOT-2026-013j -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] El ticket sigue acotado a gate del backlog + regla de pipeline, sin derivar a scope gate, handoff o controller.
- [ ] El diff productivo se limita a `scripts/check_backlog_contract.py`, su test y la instruccion de pipeline declarada.
- [ ] `backlog.md` no se convierte en una autoridad paralela del FLT.

## Evidencia minima

- [ ] Existe una reproduccion del caso con ficha detallada que re-declara `Files Likely Touched`.
- [ ] Existe evidencia FAIL-sin/PASS-con de la barrera del gate.
- [ ] `execution_log.md` registra comandos exactos, resultados y decision CEM si hubo desviacion.

## Calidad del fix

- [ ] El backlog deja de poder divergir silenciosamente del contrato frozen respecto al FLT.
- [ ] La autoridad del contrato/work_plan queda explicita en el flujo si el pipeline sigue leyendo la ficha detallada.
- [ ] `scope_gate` y `pre_handoff_guard` permanecen intactos.

## Gates de cierre

- [ ] `python -m pytest tests/unit/test_check_backlog_contract.py -q -p no:cacheprovider` termina verde.
- [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.

## Anti-patrones a rechazar (Manager)

- Solucion que conserva dos fuentes de verdad “sincronizadas a mano”.
- Test verde que no reproduce una ficha real con FLT duplicado/divergente.
- Fix que se apoya en tocar `scope_gate`, `pre_handoff_guard` o `agent_controller` fuera del scope declarado.
