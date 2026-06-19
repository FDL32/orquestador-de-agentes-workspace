# AUDIT_WOT-2026-010w.md

## Checklist de aceptacion

- [ ] Los tres call sites de `closeout_steps` fijan `encoding="utf-8",
      errors="replace"`.
- [ ] Existe test de regresion real en `tests/test_session_closeout.py` para
      salida UTF-8 alta sin `UnicodeDecodeError`.
- [ ] `--session-close --dry-run --force` deja de romper por decode en Windows.
- [ ] El fix se queda en `closeout_steps`; no migra al controller.
- [ ] `pytest` focal, `ruff`, `format`, suite canonica y `validate 0/0` verdes.

## Anti-patrones a rechazar

- Corregir solo `run_script()` dejando vivos los otros dos call sites.
- Mover la correccion al controller o a un wrapper global no pedido.
- Simular el caso solo con mocks y no con una salida UTF-8 real.
- Mezclar el fix con otros cambios del closeout o de naming/higiene.
