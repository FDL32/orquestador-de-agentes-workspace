# 01 - Auditoria del repo_motor

## Bloque de cabecera

- **Scope:** salud del motor (WOT-2026-009c / 009d / 009e / 009f)
- **Repo motor (HEAD):** 43e80bbb5e7bddae2f4366362d1bd76f893d45a8
- **Fecha auditada:** 20260615_2141 — completada post-compaction
- **Auditor:** Claude Sonnet 4.6, doble pasada adversarial

---

## Pasada A — Verificacion determinista

### A1. Ruff motor

- Evidencia: raw/ruff_motor.txt — exit_code=0, All checks passed!
- Veredicto: VERIFICADO.

### A2. Validate motor

- Evidencia: raw/validate_motor.txt — exit_code=0, errors={}, warnings={}
- Veredicto: VERIFICADO. 0 errores, 0 warnings.

### A3. Motor pristine

- Evidencia: raw/motor_pristine_snapshot.txt — exit_code=0, motor_dirty_before=false, status_before=[], diff_stat_before=[]
- Veredicto: VERIFICADO. Motor limpio al momento de recoleccion (21:41 UTC).

### A4. Skills contract

- Evidencia: raw/discover_skills_contract.txt — exit_code=0 (stdout vacio = contrato OK)
- Veredicto: VERIFICADO.

### A5. Commits de sesion en motor (HEAD 43e80bb)

| Commit  | Ticket | Descripcion |
|---------|--------|-------------|
| a020afd | 009c   | feat: reciprocal isolation guards motor/destino |
| ec6179b | 009c   | docs: harden builder bus handoff contract |
| a5c2d94 | 009f   | chore/productivo: pre-handoff checkpoint (check_destino_publish_ready.py + tests + orchestrator_pipeline) |
| cf12068 | 009e   | feat: add $BuilderOnly switch to Stop-ProjectAgentProcesses |
| 3806637 | 009e   | docs: clarify non-python gate evidence |
| 43e80bb | 009d   | feat: consolidate FLT parser consumers |

### A6. Suite pytest

- Evidencia: findings.json — pytest_safe_last_run.exit_code=0, finished_at=2026-06-15T21:27:40 UTC
- Caveat: suite canonica = allowlist parcial (DEFAULT_PYTEST_ARGS ~28 archivos, ~119 excluidos del directorio tests/).
  Tests focales de 009d (test_scope_gate_topology.py, test_pip_audit_policy.py, test_graph_context.py)
  se corrieron via argumento explicito en la evidencia del execution_log; no garantizados en DEFAULT.
- Veredicto: INFERIDO-PARCIAL. Exit code 0 real; cobertura total incierta.

---

## Pasada B — Refutacion adversarial

### B1. Ruff exit 0 = codigo correcto?

Ruff detecta errores de estilo y algunos patrones semanticos, no bugs logicos ni type errors.
Sin mypy ni cobertura total de tests, la correccion funcional no queda garantizada solo por ruff.
Veredicto: PARCIALMENTE VERDADERO. Complementar con tests.

### B2. Motor pristine — posible falso positivo?

El snapshot se tomo a 21:41:34 UTC, aprox. 10 min despues del ultimo commit (43e80bb, ~21:31 UTC segun bus).
Los tres campos son vacios (dirty=false, status=[], diff_stat=[]).
No hay evidencia de escritura posterior al commit en el arbol del motor.
Veredicto: VERIFICADO. Pristineza respaldada por los tres campos.

### B3. Commit a5c2d94 — inconsistencia de convencion

El mensaje dice 'pre-handoff checkpoint' pero los archivos son productivos de 009f:
scripts/check_destino_publish_ready.py (nuevo), tests/unit/test_check_destino_publish_ready.py (nuevo),
prompts/orchestrator_pipeline.md (modificado). Funcionalidad intacta; la convencion
'el ultimo commit antes de mark-ready debe ser productivo con referencia al ticket' fue violada.
Leccion documentada en sesion y en work_plan de 009e. No requiere accion retroactiva.
Veredicto: ANOTACION DE CONVENCION — no critico.

### B4. Skills contract — completitud?

Backlog WOT-2026-008b documenta BOM UTF-8 en skills/man-review-implementation/SKILL.md.
Ese BOM hace que parse_frontmatter devuelva NO_FRONTMATTER y omita la skill.
El check-contract puede pasar sobre 28 skills en vez de 29 en disco.
Veredicto: RIESGO CONOCIDO Y DOCUMENTADO. No nuevo; ticket 008b pendiente.

### B5. Bug datetime comparison en pre_compact_hook.py (HALLAZGO NUEVO)

Origen: nota de sesion capturada en PreCompact instruction:
'No se pudo actualizar STATE.md: can't compare offset-naive and offset-aware datetimes'.
Impacto: STATE.md puede quedar sin actualizar en compactaciones largas.
No bloquea operacion del sistema (error capturado y logeado).
Clasificacion: BUG MENOR, IMPACTO OPERATIVO BAJO.
Recomendacion: ticket motor/pre-compact-datetime-fix (baja prioridad).
Veredicto: HALLAZGO NUEVO.

### B6. Suite allowlist — riesgo sistemico heredado

Tests de 009c (test_scope_gate_isolation.py) y 009d corridos via argumento explicito.
Si DEFAULT_PYTEST_ARGS no los incluye, los gates canonicos futuros no los cubren automaticamente.
Veredicto: RIESGO ESTRUCTURAL HEREDADO. Ya en backlog (nota 2026-06-12). No nuevo.

---

## Resumen motor

| Area | Estado | Notas |
|------|--------|-------|
| Ruff | PASS | exit 0 |
| Validate | PASS | 0/0 |
| Motor pristine | PASS | dirty=false |
| Skills contract | PASS con caveat | BOM en 008b conocido |
| Suite (last-run) | PASS parcial | allowlist, no descubrimiento total |
| Commits de sesion | COHERENTES | 6 commits trazables |
| Bug pre-compact datetime | HALLAZGO NUEVO | Baja prioridad, ticket recomendado |
| Suite allowlist | RIESGO HEREDADO | Pendiente en backlog |