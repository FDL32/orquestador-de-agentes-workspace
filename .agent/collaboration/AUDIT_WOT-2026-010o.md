# AUDIT_WOT-2026-010o -- Criterios de auditoria

## Contrato estructural

- [ ] El diff se limita a tests/fixtures del review bridge y, como mucho, a la
      capa minima necesaria para inyectar un repo controlado.
- [ ] No se toca la politica funcional del evidence-gate en produccion.
- [ ] No se edita `.agent/config/motor_destination_link.json`.

## Evidencia minima

- [ ] Existe un caso reproducible `APPROVE` contra repo controlado.
- [ ] Existe un caso reproducible `CHANGES` contra repo controlado.
- [ ] Existe evidencia de que el resultado ya no depende del estado git vivo del
      `repo_destino` real.
- [ ] `run_pytest_safe --level all` termina en verde.
- [ ] `validate --json` termina 0/0.

## Anti-patrones a rechazar

- Resolver la flakiness mockeando la decision final en vez del estado de repo.
- Introducir una fixture que no pase por el codigo real del evidence-gate.
- Mezclar este ticket con cambios de politica de runner, `010l` o `010m`.
