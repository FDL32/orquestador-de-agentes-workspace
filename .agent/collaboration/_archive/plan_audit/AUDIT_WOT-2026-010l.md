# AUDIT_WOT-2026-010l -- Criterios de auditoria

## Contrato estructural

- [ ] El diff productivo se limita a runner/selector, tests focales y una nota
      documental puntual.
- [ ] No cambia el contrato canonico de handoff de `010c`/`010q`.
- [ ] No introduce cache pytest, xdist/sharding, CI ni servicios externos.

## Evidencia minima

- [ ] Test de barrera: `git diff` fallido -> repliegue a suite canonica.
- [ ] Test de barrera: archivo troncal (`pyproject.toml`, `pytest.ini`,
      `.agent/**`) -> repliegue a suite canonica.
- [ ] Test de barrera: resolucion vacia o insegura -> repliegue a suite canonica.
- [ ] Test positivo: caso seguro produce subset reproducible y auditable.
- [ ] El handoff sigue bloqueando corridas focales para `--mark-ready` via `010q`.
- [ ] `ruff check` sobre Python tocado pasa.
- [ ] Tests focales derivados del diff pasan.
- [ ] `check_encoding_guard.py` pasa sobre archivos tocados.
- [ ] `validate --json --project-root <repo_destino>` termina 0/0.

## Anti-patrones a rechazar

- Parser git nuevo cuando ya existe un seam canonico.
- Pass-open silencioso cuando el selector no sabe.
- Mezclar este ticket con cache, xdist, CI o cambio de politica de handoff.
- Heuristicas no auditables sin tests de barrera.
