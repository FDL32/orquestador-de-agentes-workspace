# AUDIT_WOT-2026-011c.md

## Checklist de aceptacion

- [ ] Existe `bom_source_audit_WOT-2026-011c.md` en `.agent/runtime/audit/`.
- [ ] El reporte nombra con evidencia reproducible la fuente del BOM y, si es
      posible, el origen de los control chars.
- [ ] El reporte separa `VERIFICADO` de `INFERENCIA RAZONABLE`.
- [ ] El reporte no aplica fix; solo recomienda follow-up.
- [ ] `python scripts/check_encoding_guard.py <reporte> <execution_log>` queda verde.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
      queda en 0 errors / 0 warnings.

## TP Check

- TP-01: verificado - el ticket ataca una sola brecha: la fuente del BOM/control-char.
- TP-02: verificado - el resultado es un artefacto research, no una mutacion de runtime.
- TP-03: verificado - `delivery_authority` es `repo_destino`; `repo_motor` solo se lee.
- TP-04: verificado - si para demostrar la hipotesis hace falta modificar un escritor,
  el contrato exige `CONTRACT_GAP`.
- TP-05: verificado - `work_plan`, `STRATEGY` y `AUDIT` convergen en "identificar y parar".

## Anti-patrones a rechazar

- Arreglar BOM/control chars durante el spike.
- Presentar correlacion como causalidad verificada.
- Editar `backlog.md` o `execution_log.md` solo para borrar el sintoma.
- Tocar `repo_motor` porque "es mas facil probarlo cambiando el launcher".
