# execution_log.md -- WOT-2026-012b
## Metadata
- **Ticket:** WOT-2026-012b
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-012b.
- Motivo: `012a` ya fijo el contrato de cola viva; ahora toca convertirlo en barrera automatica antes de seguir acumulando deuda sobre el backlog.
- Contrato congelado: `T-012B-001`.
- Ajuste previo de cola viva: `012a` se reconcilia fuera del backlog activo porque ya esta `COMPLETED`; su traza historica ya vive en `_archive/backlog_done.md`.
- Runtime bootstrap esperado para Builder: `STATE=IN_PROGRESS`, `TURN=BUILDER/IMPLEMENT`, `work_plan.md` activo en `012b`.
## Premise Re-check requerido al Builder
- Releer `.agent/collaboration/backlog.md` y confirmar que la tabla activa expone `Reactivation` y que `012a` ya no aparece como ticket vivo.
- Verificar que `scripts/run_gates_dispatch.py`, `scripts/check_deliverables_exist.py` y `scripts/validate_ticket_prose.py` no ofrecen ya una barrera equivalente.
- Confirmar que la resolucion de proyecto para leer `repo_destino` falla cerrada sin `--project-root` ni `AGENT_PROJECT_ROOT`.
## Restriccion cross-ticket
- `012b` no reabre `012a`, no toca el archivador del closeout y no cambia la politica de cierre canonico.
- `011f` permanece como ticket separado de encoding/line endings; no mezclarlo con este gate.

## BUILDER - WOT-2026-012b - Gate check_backlog_contract.py

### Fase 0 - Diagnostico (VERIFICADO)
- backlog migrado por 012a: tabla 'Vista rapida' con 8 columnas (Prioridad|Ticket|Titulo|Scope|Estado|Depende de|Origen|Reactivation); 012a ya no es fila viva.
- Estados vivos presentes: pending (react=-), blocked/deferred/completed-partial (react=condition:<slug>).
- NO existe gate equivalente (scripts/check_backlog_contract.py ausente; run_gates_dispatch/check_deliverables/validate_ticket_prose no validan la tabla del backlog).
- Patron de resolucion: runtime.project_root.resolve_project_root() usa AGENT_PROJECT_ROOT con fallback a __file__. Para 012b se requiere resolucion ESTRICTA sin fallback (leer backlog relativo al cwd = motor seed, incorrecto).

### Fase 1 - Implementacion
- scripts/check_backlog_contract.py: resuelve destino via --project-root o AGENT_PROJECT_ROOT, fail-closed (exit 2) sin root. Parsea SOLO la tabla bajo '## Vista rapida' (nunca HTML/prose). Valida: 8 columnas, header exacto, Status en vocabulario cerrado (pending|blocked|deferred|ready-for-review|awaiting-manager|completed-partial), semantica Reactivation (- solo activos sin trigger; condition:/commit:/external:/ticket-id para blocked/deferred/completed-partial; rechaza N/A/prosa vaga), encabezados ### WOT-/WT-/WP- bien formados. Sin mutacion.
- Integrado en scripts/run_gates_dispatch.py como barrera independiente de deliverable_type (mismo patron que --check-contract/--check-naming), pasando --project-root PROJECT_ROOT.

### Fase 2 - Tests (tests/unit/test_check_backlog_contract.py, 11 tests)
- PASS valido; fail-closed sin root (exit 2); via AGENT_PROJECT_ROOT; terminal en cola viva bloquea; deferred sin trigger bloquea; Reactivation vaga (N/A) bloquea; Reactivation no estructurada (prosa) bloquea; conteo de columnas; ficha malformada; falta 'Vista rapida'; header de columnas mismatch.
- Verificacion FAIL-sin/PASS-con: sin el gate -> error de coleccion (FileNotFoundError); con el gate -> 11 passed.

### Gates (comandos + resultado literal)
- Tests focales: `python -m pytest tests/unit/test_check_backlog_contract.py -v` -> 11 passed in 0.15s
- Ruff: `uv run ruff check scripts/check_backlog_contract.py tests/unit/test_check_backlog_contract.py scripts/run_gates_dispatch.py` -> All checks passed!
- Ruff format: `uv run ruff format --check <mismos>` -> 3 files already formatted
- Encoding: `python scripts/check_encoding_guard.py <3 archivos>` -> exit 0 (todos no-BOM, ASCII, 0 ctrl chars)
- (suite canonica --level all + validate: al completar)

### Suite canonica --level all: 1 failed AJENO a 012b (bloqueo externo)
- Resultado: 1 failed, 3047 passed, 20 skipped (level=all, sha=1a04ec9).
- Test que falla: tests/unit/test_no_legacy_topology_terms.py::test_repo_has_no_live_retired_topology_terms.
- Causa: tests/test_hermes_build_context_bundle.py:79 contiene `assert "Model B" not in context`. El guard LEGACY_PATTERN (Model B / Modelo B / model_b) lo detecta como reintroduccion del termino retirado -> FALSO POSITIVO (un test anti-"Model B" contiene el literal por construccion).
- VERIFICADO ajeno a 012b: (1) el archivo hermes NO esta en mi working set ni FLT; (2) entro en commit 2ab3b42 'feat: add Hermes context bundle generator' (trabajo paralelo, no de mi pipeline); (3) stash de mi diff -> el test SIGUE fallando en HEAD limpio (1a04ec9). Mi diff no influye.
- Mi trabajo 012b es correcto y verde en aislamiento (11 focales passed, ruff/format/encoding OK).
- DECISION: no hago handoff con suite roja (gate fail-closed correcto), pero NO arreglo un archivo ajeno (hermes) fuera de mi FLT (scope creep). HANDOFF bloqueado por causa externa. Requiere decision de Manager/Orquestador: (a) hotfix separado del falso positivo (excluir el archivo de test del guard, o ajustar el patron para no auto-detectarse), o (b) revertir/corregir el commit hermes 2ab3b42.

### Ronda 2 - Fix del CHANGES del Manager (BLOCKER integracion)
- BLOCKER confirmado y reproducido: run_gates_dispatch invocaba "scripts/check_backlog_contract.py" (relativo) con cwd=PROJECT_ROOT=repo_destino -> "can't open file ...workspace\scripts\check_backlog_contract.py". El script vive solo en el motor.
- FIX: anadido MOTOR_SCRIPTS_DIR = Path(__file__).resolve().parent (siempre el motor); la invocacion del backlog gate usa ruta absoluta del motor + cwd=motor, manteniendo --project-root=destino. Verificado end-to-end desde cwd=destino -> exit 0 ejecutando el gate real contra el backlog del destino.
- Barrera de integracion anadida (2 tests): test_gate_invocable_by_absolute_path_from_foreign_cwd (PASS: ruta absoluta corre desde cwd ajeno) + test_relative_path_from_destino_cwd_is_the_bug (documenta el BLOCKER: relativo desde destino -> can't open file). Verificacion FAIL-sin/PASS-con del dispatcher: revertido a relativo -> el gate falla 'can't open file' desde destino; restaurado -> exit 0.
- Gates: ruff All checks passed; format 3 files clean; 13 focales passed; encoding exit 0.

### HALLAZGO sistemico (PRE-EXISTENTE, ajeno a 012b -> follow-up)
- Al ejercer run_gates_dispatch end-to-end desde el destino, falla ANTES de mi gate en discover_skills.py: "can't open file ...workspace\scripts\discover_skills.py". Las invocaciones de check_deliverables_exist.py (L144), discover_skills.py --check-contract (L164) y --check-naming (L176) usan TODAS ruta relativa con cwd=PROJECT_ROOT(destino) -> rotas en topologia destino-motor. VERIFICADO pre-existente (no en mi git diff). NO las arreglo en 012b (scope creep, fuera de FLT). Follow-up recomendado: dispatcher debe invocar TODOS los gates por ruta absoluta del motor.

### Bloqueo restante para handoff (externo, no 012b)
- Suite --level all sigue con 1 failed por hermes Model B (commit 2ab3b42, ajeno). Requiere hotfix del falso positivo o decision sobre el commit hermes ANTES de commit+handoff de 012b.### Ronda 3 - Cierre canonico tras fix sistemico del dispatcher
- Se cerró el hallazgo sistemico del Manager: un_gates_dispatch.py ya no invoca solo un gate por ruta absoluta, sino TODA la cadena de gates del motor con cwd=repo_motor, manteniendo AGENT_PROJECT_ROOT/--project-root para leer el runtime del destino. Ademas se eliminó la dependencia fragile a untime.* importable por nombre: el dispatcher resuelve localmente PROJECT_ROOT y MOTOR_ROOT, evitando colision con .agent/runtime.
- Ajuste adicional para permitir el cierre real del ticket: 	ests/unit/test_no_legacy_topology_terms.py ahora ignora asserts negativos del tipo ssert "Model B" not in ..., de modo que el guard no se auto-dispare contra un test anti-regresion de Hermes. Este unblocker de suite quedó incorporado al FLT del ticket.
- Commit productivo repo_motor: 2e0de38 (ix(WOT-2026-012b): harden topology-safe gate dispatch).
- Suite canonica sobre el SHA final: python scripts/run_gates_dispatch.py con AGENT_PROJECT_ROOT=<repo_destino> -> 3051 passed, 20 skipped, 5 deselected in 449.14s (0:07:29); uff check y uff format --check verdes; discover_skills --check-contract/--check-naming verdes; check_backlog_contract.py OK contra el backlog vivo del destino.
- Validate final: python .agent/agent_controller.py --validate --json --project-root <repo_destino> -> errors=0 warnings=0.
- Resultado: el bloqueo externo de Hermes quedó absorbido por la corrección del guard de terminología; 012b queda cerrable sin CONTRACT_GAP restante.