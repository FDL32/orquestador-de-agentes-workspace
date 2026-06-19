# AUDIT_WOT-2026-011d.md

## Checklist de aceptacion

- [ ] `discover_skills.py` trata el lifecycle de prompts stub desde una fuente
      real del archivo y sin ampliar el vocabulario de status.
- [ ] `docs/registry/INDEX.md` se regenera con `--generate-index` y los 7 stubs
      ya no aparecen como `active`.
- [ ] Los consumidores operativos vivos fuera de historia apuntan a nombres
      canonicos o justifican explicitamente la compatibilidad residual.
- [ ] Todo stub borrado tiene evidencia `rg` pre/post delete con `0`
      consumidores no-historicos.
- [ ] Todo stub que no llegue a `0` consumidores queda `deprecated` y no se
      fuerza su borrado.
- [ ] `pytest` focal de catalogo/migracion, `ruff`, `pytest-safe`,
      `--check-index` y `validate` quedan verdes.

## TP Check

- TP-01: verificado - la secuencia es lineal: baseline, fuente de verdad,
  repoint, delete condicional; no pide borrar antes de medir consumidores.
- TP-02: verificado - cada criterio nombra un verificador literal:
  `rg`, `--generate-index`, `--check-index`, `pytest`, `ruff`, `validate`.
- TP-03: verificado - `Files Likely Touched` enumera rutas concretas del
  `repo_motor` y una unica ruta operativa en `repo_destino`, sin comodines.
- TP-04: verificado - no hay lenguaje blando en el flujo critico; el delete es
  condicional a `0 consumidores no-historicos verificados`.
- TP-05: verificado - `work_plan`, `STRATEGY` y `AUDIT` describen la misma
  secuencia: catalogo fuente real -> repoint -> delete condicional.

## Anti-patrones a rechazar

- Editar `docs/registry/INDEX.md` manualmente para "ganar tiempo".
- Anadir `legacy-retained` u otro status nuevo solo para sortear el catalogo.
- Marcar un stub como retirado sin `rg` pre-delete con `0` consumidores vivos.
- Reescribir referencias historicas en DEC/changelog para reducir el conteo.
- Declarar exito porque el stub sigue en disco pero el indice ya no lo muestra,
  sin resolver consumidores operativos reales.
