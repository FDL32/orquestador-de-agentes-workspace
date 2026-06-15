# 06 - Tickets propuestos

## Bloque de cabecera

- **Scope:** hallazgos nuevos que merecen ticket
- **Fecha auditada:** 20260615_2141

---

## Hallazgos nuevos — tickets recomendados

### T1 — Bug datetime comparison en pre_compact_hook.py (BAJA PRIORIDAD)

- **Descripcion:** pre_compact_hook.py falla con 'can't compare offset-naive and offset-aware datetimes'
  al intentar actualizar STATE.md durante una compactacion.
- **Impacto:** STATE.md puede quedar desactualizado. No bloquea operacion; error capturado.
- **Scope sugerido:** motor/hooks
- **Deliverable:** fix de una linea (astimezone() o similar para hacer aware ambos datetimes).
- **Prioridad:** Baja.
- **Nombre sugerido:** WOT-2026-010a o similar.

### T2 — Verificar integracion de check_destino_publish_ready.py en quality-gates.yml (BAJA)

- **Descripcion:** El gate existe (scripts/, tests/), documentado en orchestrator_pipeline.md,
  pero no se verifico si ya esta en .github/workflows/quality-gates.yml del destino.
- **Impacto:** Si falta, el gate solo protege manualmente, no en CI.
- **Scope sugerido:** system/ci-portability (destino)
- **Deliverable:** verificar workflow, anadir paso si falta.
- **Prioridad:** Baja.

## Hallazgos heredados con tickets ya existentes

| Hallazgo | Ticket existente | Estado |
|----------|-----------------|--------|
| Suite allowlist parcial | backlog nota 2026-06-12 | pendiente candidato |
| BOM en man-review-implementation SKILL.md | WOT-2026-008b | pending |
| PYSEC-2026-196 excepcion pip-audit | WT-2026-256a | blocked-external |

## Tickets NO recomendados

- Commit a5c2d94 con mensaje checkpoint: no merece ticket; es nota de convencion en docs.
- Incidente 0081fb6: ya resuelto con 009f + memoria. No reabrir.