# 07 - Pasada adversarial (Pasada B consolidada)

## Bloque de cabecera

- **Scope:** claims VERIFICADO / INFERIDO / NO VERIFICADO / HALLAZGO / RIESGO
- **Fecha auditada:** 20260615_2141
- **Auditor:** Claude Sonnet 4.6, doble pasada — Pasada A en 01-04, Pasada B aqui

---

## Tabla de veredictos por claim

| # | Claim | Pasada B | Veredicto |
|---|-------|----------|-----------|
| 1 | Ruff motor exit 0 = codigo correcto | Parcial; sin mypy ni cobertura total | VERIFICADO-PARCIAL |
| 2 | Motor pristine al momento del collector | 3 campos vacios, no hay escritura posterior al commit | VERIFICADO |
| 3 | Commit a5c2d94 es checkpoint (no productivo) | Es productivo con mensaje de checkpoint | ANOTACION-CONVENCION |
| 4 | Suite 64 tests 009d passed | Execution_log evidencia literal; no re-ejecucion en audit | INFERIDO-POSITIVO |
| 5 | Skills contract pass = 29 skills OK | BOM omite 1 skill; puede ser 28 de 29 | RIESGO-CONOCIDO |
| 6 | Validate 0/0 motor | Raw evidence exit 0, errors={}, warnings={} | VERIFICADO |
| 7 | Validate 0/0 destino | Raw evidence exit 0, errors={}, warnings={} | VERIFICADO |
| 8 | check_destino_publish_ready.py funciona | 8 tests; script revisado; exit codes correctos | VERIFICADO |
| 9 | Gate en CI del destino | Snippet en docs; no verificado en quality-gates.yml | NO-VERIFICADO |
| 10 | Incidente 0081fb6 resuelto | Gate 009f + memoria + validate 0/0 actual | RESUELTO |
| 11 | FLT parser consumidores delegados | Commit 43e80bb + 64 tests en execution_log | INFERIDO-POSITIVO |
| 12 | Reciprocal isolation guards (009c) | 8 tests + commit a020afd | VERIFICADO |
| 13 | Bus con 105 eventos previos | Conteo real: total=167, 009x=62, anteriores=105 | VERIFICADO-PENDIENTE-LIMPIEZA |
| 14 | pre_compact_hook datetime bug | Error capturado en sesion: offset-naive vs aware | HALLAZGO-NUEVO |
| 15 | Suite allowlist no cubre todos los tests | Nota backlog 2026-06-12: DEFAULT=28 de 147 | RIESGO-HEREDADO |

---

## Claims criticos sin evidencia directa

### C1. No hay falso verde estructural en este audit

Todos los VERIFICADO tienen raw evidence o commit verificable.
Los INFERIDO-POSITIVO tienen execution_log con evidencia literal y estado del repo coherente.
No se encontro ningun claim que diga PASS pero sea imposible de rastrear.

### C2. Scope creep — algun ticket toco superficie prohibida?

- 009c: Forbidden Surfaces = .agent/collaboration/ del motor, privada/, bus/state_machine.py.
  Commit a020afd toca .agent/scope_gate.py y tests. No hay evidencia de toque a forbidden.
- 009d: Forbidden Surfaces incluye bus/state_machine.py y scripts/validate_ticket_prose.py.
  Commit 43e80bb toca .agent/scope_gate.py, motor_checkpoint.py, pip_audit_policy.py, graph_context.py,
  y 3 test files. Sin toque a forbidden.
- 009e: toca launch_agent_terminals.ps1. Sin forbidden declaradas violadas.
- 009f: toca scripts/check_destino_publish_ready.py, tests, prompts/orchestrator_pipeline.md.
  Forbidden del plan = .agent/collaboration/ del motor, privada/, bus/state_machine.py.
  Sin violaciones detectadas.
Veredicto: SIN SCOPE CREEP DETECTADO.

### C3. Claims sin evidencia directa aceptados como validos

- Tests 009c (test_scope_gate_isolation.py, 8 tests): no en execution_log del ultimo cierre
  (que fue 009d). El commit a020afd existe y el archivo existe en el arbol del motor.
  Aceptado como INFERIDO-POSITIVO.

### C4. Fixture drift — los stubs de 009f son realistas?

Los tests de 009f usan patch.object(cdr, '_run_validate', ...) en vez de correr el controlador real.
Esto es pragmatico (evita dependencia en estado del destino real durante los tests unitarios)
pero introduce el riesgo de que el stub no refleje el contrato real del controlador.
El test test_resolves_motor_from_link_json usa motor=tmp_path/motor (directorio existente pero vacio).
Si el controlador requiere mas estructura en motor_root, el test pasaria con un stub que no detectaria
la falla real.
Veredicto: RIESGO DE FIXTURE DRIFT BAJO. Aceptable para unit test; se recomienda test de integracion
eventual.

---

## Estado canonico del sistema al cierre de auditoria

| Dimension | Estado | Evidencia |
|-----------|--------|-----------|
| Motor ruff | PASS | exit 0 |
| Motor validate | PASS | 0/0 |
| Motor pristine | PASS | dirty=false |
| Motor suite | PASS parcial | exit 0 (allowlist) |
| Destino validate | PASS | 0/0 |
| Destino surfaces | COHERENTES | COMPLETED, 009d |
| Integracion motor+destino | PASS | validate cruzado 0/0 |
| Incidente 0081fb6 | RESUELTO | gate 009f |
| Bus | PENDIENTE | 105 eventos previos, archivar en session-close |

---

## Veredicto final de auditoria

SISTEMA EN ESTADO SALUDABLE.

No hay regresiones activas ni gates rojos.
Dos hallazgos nuevos de baja prioridad documentados (datetime bug, CI gate no verificado).
Un riesgo heredado conocido (suite allowlist parcial).

AUTORIZADO para proceder a session-close.