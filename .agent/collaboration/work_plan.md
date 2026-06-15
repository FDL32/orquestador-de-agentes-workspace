# Work Plan: WOT-2026-009d

## Metadata

- **ID:** WOT-2026-009d
- **Contract ID:** T-009D-001
- **Estado:** COMPLETED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-009b (COMPLETED)

## Objetivo

Reducir los parsers activos de `Files Likely Touched` a una fuente canonica
(`scope_gate.parse_flt_raw_buckets`) con wrappers delgados en los consumidores,
para evitar que nueva semantica FLT amplifique deriva entre implementaciones.

Verificacion: `parse_raw_flt_paths` en `motor_checkpoint.py`, `pip_audit_policy.py`
y `graph_context.py` delegan a `scope_gate.parse_flt_raw_buckets`; `ruff check .`
exit 0; 64 tests focales passed.

## Decision Arquitectonica

El parser canonico vive en `scope_gate.parse_flt_raw_buckets`: recibe el contenido
del work_plan y retorna buckets `{motor: set[str], destino: set[str]}` con rutas
relativas normalizadas. Los consumidores (motor_checkpoint, pip_audit_policy,
graph_context) llaman al canonico y resuelven rutas absolutas contra su propia raiz.

Esto elimina tres implementaciones paralelas del mismo algoritmo y centraliza en
un unico punto cualquier futura extension de semantica FLT (nuevos namespaces,
wildcards, exclusiones).

## Non-goals

- No centralizar parsers de prosa o lint (validate_ticket_prose).
- No cambiar semantica observable del scope gate.
- No mezclar con 009e ni 009f.

## Files Likely Touched

### repo_motor
- .agent/scope_gate.py
- .agent/motor_checkpoint.py
- scripts/pip_audit_policy.py
- scripts/graph_context.py
- tests/unit/test_scope_gate_topology.py
- tests/unit/test_pip_audit_policy.py
- tests/unit/test_graph_context.py

## Criterios Binarios

- [ ] `parse_flt_raw_buckets` existe en scope_gate.py como funcion canonica.
- [ ] motor_checkpoint.py, pip_audit_policy.py y graph_context.py delegan al canonico.
- [ ] Tests cubren FLT plano y namespaced para cada consumidor.
- [ ] `ruff check .` exit 0.
- [ ] 64 tests focales passed.
- [ ] validate destino 0/0 al cerrar.

## Forbidden Surfaces

- .agent/collaboration/ del motor (seed neutro).
- privada/ y .env.
- bus/state_machine.py.
- scripts/validate_ticket_prose.py.
