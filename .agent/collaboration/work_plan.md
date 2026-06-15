# Work Plan: WOT-2026-009b

## Metadata

- **ID:** WOT-2026-009b
- **Contract ID:** T-009B-001
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-009a (COMPLETED)

## Objetivo

Hacer que validate/pre-handoff/mark-ready resuelvan el root productivo correcto
segun `delivery_authority`, usando `## Files Likely Touched` con subsecciones
opcionales `### repo_motor` / `### repo_destino`.

Root cause: `_parse_raw_flt_paths` en motor_checkpoint.py y los parsers de
pre_handoff_guard.py mezclan todas las rutas bajo `## Files Likely Touched` sin
distinguir namespace. En tickets `delivery_authority: repo_motor`, el diff
productivo esta en motor pero el validate corre desde el destino, generando
warnings falsos o bloqueando cuando las rutas del motor no se resuelven contra
PROJECT_ROOT del destino.

## Non-goals

- No introducir guardias reciprocas amplias (eso es 009c).
- No crear secciones `External Scope` ni `Operational Surfaces`.
- No reemplazar `delivery_authority` por `target_repository`.
- No invertir globalmente `get_changed_files`.
- No implementar 009d (consolidacion de parsers) mas alla del inventario.
- No tocar state machine ni TicketState.

## Inventario de parsers FLT (pre-implementacion)

Resultado del grep preflight:

1. `scope_gate.py:98` — `parse_files_likely_touched` (canonical, deliverable-aware
   desde 009a). Recibe project_root. Retorna paths resueltos absolutos.
2. `agent_controller.py:318` — wrapper que delega en scope_gate con PROJECT_ROOT.
3. `motor_checkpoint.py:130` — `parse_raw_flt_paths`: retorna paths relativos raw
   sin resolver (para comparar con motor_uncommitted_productive). NO acepta namespace.
4. `scripts/pre_handoff_guard.py:272` — parser propio independiente. Lee work_plan
   desde project_root. NO delega en scope_gate. NO acepta namespace.
5. `scripts/pip_audit_policy.py:32` — `_parse_files_likely_touched`: retorna paths
   relativos sin resolver. Solo usado para decidir si correr pip-audit.

Parsers que necesitan actualizacion en 009b: (3) y (4).
Parser (5) pip_audit_policy es scope-insensible por diseno; inventariado como
deuda 009d con criterio: unificar solo si pip-audit comienza a fallar por topologia.

`_check_scope_for_validate` existe en agent_controller.py:3857 — llama a
`check_scope_gate` que delega en scope_gate. Se actualiza via cambios en (2).

## Diseno

### Contrato de FLT namespaced

```markdown
## Files Likely Touched

### repo_motor
- .agent/scope_gate.py
- .agent/agent_controller.py

### repo_destino
- .agent/docs/foo.md
```

- Rutas planas (sin subseccion) son backward-compatible: se resuelven contra
  el root de autoridad del ticket (motor o destino).
- Rutas bajo `### repo_motor` se resuelven SIEMPRE contra motor_root.
- Rutas bajo `### repo_destino` se resuelven SIEMPRE contra project_root (destino).
- Un namespace desconocido emite warning; no bloquea.

### Cambios por modulo

**scope_gate.py** — funcion nueva `parse_flt_namespaced`:
- Recibe `work_plan_content`, `motor_root`, `project_root`, `delivery_authority`.
- Retorna `dict[str, set[str]]` con claves `"motor"` y `"destino"`.
- Backward-compat: rutas planas van al bucket de la autoridad del ticket.
- `parse_files_likely_touched` NO cambia de firma (backward compat con tests).
- Nueva funcion separada para no romper callers existentes.

**agent_controller.py** wrappers:
- Nuevo wrapper `parse_flt_namespaced(plan_content)` que llama a scope_gate.
- `_check_scope_for_validate` actualiza para usar diff correcto segun autoridad:
  si `delivery_authority == repo_motor`, diff viene de motor_root; si destino,
  del destino. Usa `get_productive_changed_files(delivery_authority)` nuevo.
- `get_productive_changed_files(delivery_authority)`: wrapper nuevo sobre
  `scope_gate.get_changed_files` que elige el root segun autoridad.

**motor_checkpoint.py** — `parse_raw_flt_paths`:
- Extender para que reconozca `### repo_motor` / `### repo_destino`.
- Cuando hay namespace: rutas bajo `### repo_motor` van al set de retorno;
  rutas bajo `### repo_destino` se ignoran (no son paths del motor).
- Cuando no hay namespace: comportamiento actual (backward compat).

**scripts/pre_handoff_guard.py** — `parse_files_likely_touched`:
- Actualizar para delegar en `scope_gate.parse_files_likely_touched` con
  project_root correcto segun delivery_authority.
- Si delivery_authority == repo_motor: resolver rutas motor contra motor_root.
- Recibe `delivery_authority` y `motor_root` como parametros opcionales.

### Resolucion de diff en validate

`_check_scope_for_validate` actualmente siempre llama `get_changed_files()`
que usa PROJECT_ROOT (destino). Para tickets motor:
- Diff productivo: `get_changed_files(project_root=motor_root, motor_root=None)`
- Las superficies operativas del destino siguen excluidas por excludelist.
- El gate valida el diff motor contra la whitelist de rutas motor.

## Files Likely Touched

### repo_motor
- `.agent/scope_gate.py`
- `.agent/agent_controller.py`
- `.agent/motor_checkpoint.py`
- `scripts/pre_handoff_guard.py`
- `tests/unit/test_scope_gate_topology.py`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/execution_log.md`

## Criterios Binarios

- [ ] Test positivo: ticket `delivery_authority: repo_motor` con `### repo_motor`
      valida 0/0 con diff motor dentro de scope.
- [ ] Test/parser: `parse_flt_namespaced` retorna paths motor y destino en sets
      separados; no mezcla.
- [ ] Test negativo: diff motor fuera de `### repo_motor` emite warning accionable.
- [ ] Test negativo: ticket motor sin namespace FLT valido con diff productivo
      en motor NO pasa limpio (emite warning de scope).
- [ ] Test negativo: solo `### repo_destino` no cubre diff productivo del motor.
- [ ] Test legacy: FLT plano sin namespace conserva comportamiento actual.
- [ ] `ruff check .` exit 0.
- [ ] `python scripts/run_pytest_safe.py` exit 0.
- [ ] Validate destino final 0/0.
- [ ] Commit en motor referencia WOT-2026-009b.

## STOP conditions

- Si tocar state machine es necesario, parar y escalar.
- No crear External Scope ni Operational Surfaces.
- No invertir get_changed_files globalmente.
- No implementar 009c ni 009d (solo inventario de deuda).
- Si unificar pip_audit_policy parser requiere cambio mayor, solo inventariar.

## Forbidden Surfaces

- `.agent/collaboration/` del motor (seed neutro).
- `privada/` y `.env`.
- `bus/state_machine.py` (no tocar TicketState).
- `events.jsonl` editado a mano.
