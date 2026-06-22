# 05 - Archive Plan

## Bloque de cabecera

- **Scope:** KEEP/ARCHIVE/DELETE para artefactos observados en esta pasada
- **Repo motor (HEAD):** `f48191f6983f58ceeeef75b1401acf66d5620fc3`
- **Repo destino (HEAD):** `935907c38cd6456ba42e6e63a1462c82c4e77647`
- **Fecha:** `2026-06-22 16:49`
- **Comandos ejecutados:** ver `00_scope.md`
- **Cobertura declarada:** solo plan; no se ejecutan borrados en esta auditoria
- **Limitaciones:** v0 read-only para saneos

| Ruta | Decision | Evidencia | Riesgo | Rollback |
|------|----------|-----------|--------|----------|
| `.agent/runtime/memory/session_close_report.md` | KEEP | artefacto canonico del cierre recien ejecutado | bajo | git restore / historial |
| `.agent/runtime/memory/MEMORY.md` | KEEP | consolidacion automatica post-close | bajo | git restore / regenerar consolidate |
| `.agent/runtime/memory/memory_profile.md` | KEEP | consolidacion automatica post-close | bajo | git restore / regenerar consolidate |
| `.agent/audits/system_health/general_audit_20260622_1449/` | KEEP | evidencia nueva de salud post-cambio | bajo | git restore / borrar carpeta en ticket posterior |
| `.agent/audits/system_health/general_audit_20260622_1449/raw/` | KEEP gitignored | evidencia bruta no publicable por defecto | bajo | regenerar recolector |

## Conclusiones

- No se propone `DELETE` en esta pasada.
- No hay deuda de archivado nueva generada por esta auditoria.
