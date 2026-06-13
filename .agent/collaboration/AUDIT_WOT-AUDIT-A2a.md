# AUDIT WOT-AUDIT-A2a - Manager review (resource precedence doc)

## Alias
Host-extends/motor-provides resource precedence mapping (A2a, documentation).

## Objetivo del audit
Verificar que el entregable documenta de forma correcta y verificable (1) la
regla de precedencia host .agent -> motor read-only -> nunca legacy y (2) el
mapeo de los comandos del destino que apuntan a copias locales hacia su forma
invocable real del motor externo, sin mover, borrar ni reapuntar nada (A2a).

El auditor separa claims verificados de inferencias. Ningun auto-reporte del
Builder cuenta como evidencia por si solo.

## Reglas de revision
- Revisar el doc real y la interfaz real de los scripts del motor, no el report.
- Confirmar que A2a no movio, borro ni reapunto archivos.
- Confirmar que la forma invocable documentada es la que el motor soporta hoy.
- Confirmar que los 2 STOP de A2b quedan explicitos y accionables.

## Evidencia verificada (Manager, independiente)
- Interfaz de scripts inspeccionada en `repo_motor`:
  - `scripts/run_pytest_safe.py`, `scripts/discover_skills.py`,
    `scripts/local_audit.py`: ninguno expone `--project-root`
    (`grep -l "project-root"` -> vacio).
  - `local_audit.py` solo acepta `--json` y `--quick` (argparse confirmado).
  - `runtime/project_root.py:resolve_project_root` resuelve via
    `os.environ["AGENT_PROJECT_ROOT"]`. La forma `AGENT_PROJECT_ROOT` del
    entregable es correcta; la forma `--project-root` del work_plan original era
    factualmente erronea y quedo corregida en la tabla y en la Decision
    Arquitectonica del work_plan.
- Entregable `.agent/docs/resource_precedence.md`: 3 niveles de precedencia +
  tabla de 5 comandos + 2 STOP + fecha y HEADs (`13ee7e1` / `704939f`).
- Encoding: `resource_precedence.md`, `execution_log.md` y `work_plan.md`
  ascii-only, sin BOM (verificado por conteo de bytes >127 = 0).
- `agent_controller.py --validate --json --project-root <destino>` ->
  0 errors, 1 warning (TP-STRUCT-01, resuelto por este AUDIT).
- Working tree del destino: sin commit ni push (checkpoint-gating respetado).

## Desviacion encontrada y resuelta
El work_plan original mapeaba 3 scripts con `--project-root`, flag inexistente
hoy. El Builder no toco el ticket y documento la forma real en el entregable; el
Manager verifico la interfaz y propago la correccion al work_plan (tabla +
Decision Arquitectonica) para coherencia interna del ticket. A2b hereda la
forma correcta.

## TP Check
TP-01: existe `.agent/docs/resource_precedence.md` con precedencia de 3 niveles
y tabla completa de 5 comandos. VERIFICADO.

TP-02: la forma invocable documentada coincide con la interfaz real del motor
(`AGENT_PROJECT_ROOT`, sin `--project-root`). VERIFICADO contra el codigo.

TP-03: los STOP de A2b quedan explicitos y accionables. VERIFICADO, con
CORRECCION posterior (2026-06-13): el supuesto STOP del
`test_refactor_kit_performance.py` era un gap de verificacion; el motor SI tiene
el test en `tests/` (lo corre la suite). Solo queda como limpieza la allowlist
muerta `refactor-kit` hyphen. Ningun STOP real bloquea A2b.

TP-04: A2a no movio, borro ni reapunto archivos ni toco
`.claude/settings.local.json` ni el motor. VERIFICADO por git status + scope.

TP-05: validate exit 0 / 0 errors; artefactos ascii-only sin BOM; cierre con
linea artefacto+gate en `execution_log.md`. VERIFICADO.

## Criterio de rechazo inmediato
- El doc afirma una forma invocable que el motor no soporta hoy.
- A2a movio, borro o reapunto algo fuera de scope.
- Un STOP real de A2b queda sin documentar.
- Se reclama evidencia ausente de artefactos verificables.

## Decision
DECISION: APPROVE

El cambio mejora la salud del sistema (documenta el contrato de precedencia y
corrige una forma invocable erronea con evidencia real). El unico warning era el
propio requisito de este AUDIT. Pendiente humano: aprobar checkpoint para
commit; A2b/A2c/A2d quedan como fases posteriores con sus STOP registrados.
