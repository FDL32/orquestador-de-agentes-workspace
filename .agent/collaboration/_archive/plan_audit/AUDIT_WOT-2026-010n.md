# AUDIT_WOT-2026-010n -- Criterios de auditoria

## Contrato estructural

- [ ] El scope productivo se limita al gate de deliverables y sus tests.
- [ ] No se duplico el artefacto de `010j` entre repos.
- [ ] No se relajaron gates a modo pass-open.

## Evidencia minima

- [ ] Existe reproduccion roja del caso real de `010j`.
- [ ] Existe evidencia verde para deliverable en `repo_motor`.
- [ ] Existe evidencia verde para deliverable en `repo_destino`.
- [ ] Existe evidencia de fallo cerrado para namespace/ruta invalida.

## Anti-patrones a rechazar

- Arreglar el bug copiando archivos al `repo_destino`.
- Parsear notas o secciones `Read/inspect only` como deliverables Builder.
- Cambiar politicas de cierre o de runner fuera del scope del ticket.
