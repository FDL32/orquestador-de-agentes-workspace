# AUDIT_WOT-2026-010k -- Criterios de auditoria

## Contrato estructural

- [ ] El diff se limita a tests/fixtures del hotspot real y al reporte de
      follow-up.
- [ ] No se tocaron runner, CI, cache ni políticas de cierre.

## Evidencia minima

- [ ] Existe una barrera roja->verde del hotspot elegido.
- [ ] Existe una medición before/after comparable.
- [ ] Existe al menos un smoke test sin shortcut cuando el fix sustituye setup
      real por helper/fixture.
- [ ] `validate --json` termina 0/0.

## Anti-patrones a rechazar

- Cambiar el objetivo real a `git/subprocess` sin evidencia nueva.
- Mejorar tiempo borrando comportamiento observable.
- Declarar mejora sin before/after medido.
