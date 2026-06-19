# AUDIT_WOT-2026-010v.md

## Checklist de aceptacion

- [ ] `scripts/check_encoding_guard.py` bloquea control chars ASCII `<32`
      no-whitespace en archivo textual.
- [ ] `\t`, `\n`, `\r` y CRLF legitimos no bloquean.
- [ ] El hook post-write hereda la deteccion desde la fuente compartida.
- [ ] Hay test de regresion del CLI guard por ruta explicita.
- [ ] Hay test de regresion del hook post-write.
- [ ] Los tests previos de BOM/mojibake/question-mark siguen pasando.
- [ ] `pytest` focal, `ruff`, `format`, suite canonica y `validate 0/0` verdes.

## Anti-patrones a rechazar

- Arreglar solo `check_encoding_guard.py` dejando el hook fuera.
- Introducir un detector paralelo en vez de reutilizar `scripts.encoding_guard`.
- Marcar CRLF o tabs validos como corrupcion.
- Expandir el ticket a Bash/heredoc, binarios o allowlists nuevas.
