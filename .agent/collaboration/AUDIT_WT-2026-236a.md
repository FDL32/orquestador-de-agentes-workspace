# AUDIT_WT-2026-236a

## Riesgos Bloqueantes

### ALTO - falso verde de repo-compare
Bloquear si el cierre afirma que repo-compare esta sano sin haber tratado
explicitamente: AUDIT.md, MCP GitHub, `gh` CLI y Repomix.

### ALTO - evidencia externa no trazable
Cada oportunidad debe citar fuente verificable. Si se usa navegador por fallo de
MCP/`gh`, el reporte debe decirlo.

### ALTO - adopcion prematura de SOUL.md
Bloquear si se crea `SOUL.md` operativo o se copia la plantilla extensa. El valor
del post debe reducirse a patrones y tradeoffs.

### MEDIO - scope creep a codigo productivo
El ticket es documentation/research. Cualquier fix de repo-compare, auditoria o
auth debe quedar como follow-up salvo cambio documental minimo.

### MEDIO - credits prematuro
No modificar `CREDITS.md`. Solo emitir candidate row si hay oportunidad adoptable.

## TP Check

TP-01: el reporte existe en `.agent/runtime/compare/`.

TP-02: metadata del reporte incluye fecha, repo target, SHA o razon de ausencia,
estado de AUDIT.md y numero de archivos leidos.

TP-03: scoring 0-5 de Orca incluye justificacion por dimension.

TP-04: el reporte diferencia hallazgos de producto vs hallazgos de tooling.

TP-05: MCP GitHub y `gh` CLI quedan mencionados con resultado real.

TP-06: SOUL.md queda resumido como patron, no como texto a implantar;
`CREDITS.md` no fue modificado y solo existe candidate row en el reporte cuando
hay oportunidad `AHORA` o `DESPUES`.

TP-07: validate final pasa o el blocker queda documentado con comando y salida.

## Comandos de Revision

```powershell
Get-Content .agent\collaboration\work_plan.md
Get-Content .agent\runtime\compare\stablyai-orca-HEAD-2026-06-07.md
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Veredicto Previo

`APPROVED`: el ticket es apropiado como smoke porque prueba una ruta de alto valor
con fricciones reales ya observadas. La comparacion puede aportar ideas, pero el
hallazgo principal puede ser que el protocolo necesita endurecer preflight/auth.
