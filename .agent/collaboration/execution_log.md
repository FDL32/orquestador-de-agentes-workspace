# execution_log.md -- WOT-2026-012a
## Metadata
- **Ticket:** WOT-2026-012a
**Estado:** IN_PROGRESS
- **deliverable_type:** mixed
- **delivery_authority:** repo_destino
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-012a.
- Motivo: `011j` ya cerro la fuente BOM del writer PowerShell y desbloquea la regeneracion limpia del historico de backlog.
- Contrato congelado: T-012A-001.
- Runtime bootstrap esperado para Builder: STATE=IN_PROGRESS, TURN=BUILDER/IMPLEMENT, work_plan.md activo en `012a`.
## Premise Re-check requerido al Builder
- `python scripts/check_encoding_guard.py .agent/collaboration/backlog.md` debe seguir verde o explicar cualquier rojo nuevo con evidencia.
- Releer `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` como baseline a regenerar, no a parchear ciegamente.
- Confirmar que la deuda del BOM/mojibake preexistente del propio `scripts/launch_agent_terminals.ps1` queda fuera de `012a` y se seguira por `011f`.
## Restriccion cross-ticket
- `012a` no toca el launcher PowerShell del motor ni sanea su encoding fuente.
- `011f` queda como follow-up explicito para `.gitattributes` / line endings / PS1 source encoding.


Terminal reopen requested by human for WOT-2026-012a
## BUILDER - WOT-2026-012a - Corte final + reconstruccion historica acotada

### Fase 0 - Diagnostico (VERIFICADO)
- backlog vivo: 234 lineas, no-BOM, 0 ctrl chars; ya con estructura cola-viva + columna Reactivation.
- Terminales mezclados a cortar: 011j (completed). 002c (completed-partial) PERMANECE (estado permitido en cola viva).
- _archive/backlog_done.md y _archive/backlog_pre_012a.md: 3 ctrl chars c/u, exactamente 0x07/0x0B/0x08, 0 inesperados (verificado: cualquier extra = CONTRACT_GAP, no aplico).
- Evidencia 011c: \x07udit->audit, \x0Balidate->validate, \x08ui-self->bui-self (reporte bom_source_audit_WOT-2026-011c.md lineas 57-68).

### Reconstrucciones puntuales (SOLO los 3 casos verificados por 011c)
- backlog_done.md  @179735: 0x07->'a' => 'audit_'
- backlog_done.md  @180069: 0x0B->'v' => 'valida(te)'
- backlog_done.md  @180101: 0x08->'b' => 'bui-se(lf)'
- backlog_pre_012a.md @176852/177183/177215: mismas 3 (a/v/b).
- Cada cambio = 1 byte; contexto post-cambio verificado contra el reporte 011c. 0 ctrl chars restantes en ambos archives. NINGUN strip masivo.

### Corte de 011j al historico
- Fila de tabla + ficha ### WOT-2026-011j (34 lineas) movidas de backlog.md vivo a _archive/backlog_done.md. La unica ref restante de 011j en vivo es 'Depende de' de 011f (correcto).
- ### WOT-2026-012a conservada integra: presente en vivo (1) Y en historico (1, anadida como traza del corte por exigencia del criterio binario).

### Evidencia mecanica antes/despues
- backlog vivo: 234 -> 199 lineas. Fichas ### vivas: 3 -> 2 (solo 012a, 012b). Terminales en cola: 1(011j) -> 0. 002c completed-partial permanece (permitido).

### Fuera de scope (confirmado)
- BOM/mojibake del propio scripts/launch_agent_terminals.ps1: NO tocado (deuda de WOT-2026-011f).
- launcher PowerShell, archivador, session_closeout, check_encoding_guard, .gitattributes: NO tocados.

### Gates
- Encoding guard (backlog.md + backlog_done.md + backlog_pre_012a.md + execution_log.md): exit 0.

### Linea de evidencia de cierre (ticket mixed/documental)
- Quality gate documental: `python scripts/check_encoding_guard.py <backlog.md, _archive/backlog_done.md, _archive/backlog_pre_012a.md, execution_log.md>` -> exit 0, all surfaces passed (sin BOM, sin control chars residuales).
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` -> exit code 0, 0 errors, 0 warnings, passed.
- Artefactos entregados y verificados en disco: backlog.md (cola viva, 199 lineas), _archive/backlog_done.md (historico + 011j + ### WOT-2026-012a), _archive/backlog_pre_012a.md (snapshot). Deliverable existence + encoding gate: passed.

### Handoff BLOQUEADO - CONTRACT_GAP (deliverable_type)
- pre-handoff guard como SCRIPT directo (flujo real): valid=False por UN subcheck:
  commit_visible=no_visible_commit. Resto OK (canonical_suite=fresh_green level=all
  sha=fb2c604, dirty_tree=False, missing_checkpoint=False, scope OK).
- Causa: T-012A-001 declara deliverable_type=mixed, pero la entrega es 100% documental
  en repo_destino (commit 9640511 toca solo .agent/collaboration/*.md). commit_visible
  (no bypassable por --force/--scope-override, agent_controller:1554) exige commit de
  codigo en motor para code/mixed -> incompatible con entrega documental en destino.
- El guard mismo recomienda: "the ticket type should not be code/mixed".
- Emitido CG-WOT-2026-012a.md: enmienda recomendada deliverable_type mixed->documentation.
- Falso positivo informativo: import de delivery_hygiene_check falla en modo-modulo
  pero NO en modo-script (flujo real); sin limbo de archivado real.
- NO se fuerza mark-ready ni se inventa commit. Trabajo staged y correcto en 9640511.
