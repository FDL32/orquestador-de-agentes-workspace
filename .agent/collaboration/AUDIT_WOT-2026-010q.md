# AUDIT_WOT-2026-010q -- Criterios de auditoria

## Contrato estructural

- [ ] El diff se limita al guard de pre-handoff, tests y documentacion minima
      declarada.
- [ ] No se modifica `scripts/run_pytest_safe.py`.
- [ ] No se cambia la politica de runner, cache, xdist, sharding ni Manager.

## Evidencia minima

- [ ] Test rojo->verde: `level="unit"` fresco y verde bloquea.
- [ ] Test rojo->verde: `level="all"` + `args_mode="explicit_args"` bloquea.
- [ ] Test positivo: `level="all"` + `args_mode="default_discovery"` permite
      continuar si el resto de condiciones estan verdes.
- [ ] El diagnostico del bloqueo incluye causa y remediacion.
- [ ] `ruff check` sobre Python tocado pasa.
- [ ] Tests focales de pre-handoff pasan.
- [ ] `validate --json` termina 0/0.

## Anti-patrones a rechazar

- Validar solo `level` e ignorar `args_mode`.
- Cambiar el runner para escribir campos nuevos innecesarios.
- Relajar el requisito de suite canonica completa al handoff.
- Mezclar este ticket con `010l`.
