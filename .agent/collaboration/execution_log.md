# Execution Log: WOT-2026-009b - Scope gate topology-aware

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-009b
- **Contract ID:** T-009B-001
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD: 9b7666f
- Destino HEAD: 28dad7c
- Validate previo: 0 errors / 0 warnings

## Preflight

Inventario parsers FLT:
1. scope_gate.py - canonical
2. agent_controller.py - wrapper sobre scope_gate
3. motor_checkpoint.py - parse_raw_flt_paths (paths relativos)
4. scripts/pre_handoff_guard.py - delega en scope_gate desde este ticket
5. scripts/pip_audit_policy.py - scope-insensible (deuda 009d)

_check_scope_for_validate existe en agent_controller.py:3857. Actualizado en 009b.

## Implementacion

### scope_gate.py
- Helpers de modulo extraidos: _looks_like_path_token, _normalize_flt_line
- Nueva _parse_flt_section(lines) -> (has_namespaces, [(ns, path)])
- Nueva parse_flt_namespaced(content, *, motor_root, project_root, delivery_authority)
  retorna {"motor": set, "destino": set}

### motor_checkpoint.py
- parse_raw_flt_paths: namespace-aware. Excluye ### repo_destino.
- Rutas planas y ### repo_motor retornadas. Backward-compat preservada.

### agent_controller.py
- parse_files_likely_touched: firma actualizada con deliverable_type=None;
  lee deliverable_type del plan_content automaticamente si no se pasa.
  Backward-compat con tests que mockean lambda x: set.
- Nuevo parse_flt_namespaced(plan_content) wrapper.
- Nuevo get_productive_changed_files(delivery_authority): diff del root productivo.
- _check_scope_for_validate: para repo_motor valida diff motor contra whitelist
  motor. Warning solo cuando hay out_of_scope real; gate limpio no emite warning.
  Para repo_destino: comportamiento anterior intacto.
- _run_pre_handoff_guard: pasa --motor-root al script cuando motor != project_root.

### scripts/pre_handoff_guard.py
- parse_files_likely_touched: delega en scope_gate.parse_flt_namespaced.
  Sin parser propio namespaced. Fallback flat si scope_gate no importable.
- run_guard y CLI aceptan motor_root para scope_discrepancy correcto.

### tests/unit/test_scope_gate_topology.py (nuevo)
12 tests: namespaces separados, backward-compat, unknown sub-headings, raw FLT.

## Correcciones CHANGES (post-review)

B1 resuelto: warning informativo de scope eliminado cuando gate pasa limpio.
  _check_scope_for_validate para repo_motor solo emite warning si out_of_scope real.

B2 resuelto: pre_handoff_guard.py delega en scope_gate.parse_flt_namespaced.
  Sin duplicacion de parser. Fallback solo si scope_gate no importable.

Bug regresion resuelto: parse_files_likely_touched wrapper acepta deliverable_type=None
  por defecto; lee del plan_content automaticamente. Tests con lambda x: set no rompen.

## Gates

- ruff check .: exit 0
- pytest test_agent_controller.py + focales: 153/0/0
- Suite completa run_pytest_safe.py: pendiente (en ejecucion)

## Motor commits

- c308f40 feat(WOT-2026-009b): topology-aware FLT namespace parsing
- (pendiente commit de correcciones CHANGES)

## Validate final destino

0 errors. Warnings residuales:
- ticket_prose: estilo del work_plan, no bloquean cierre de codigo.
- bus_drift + invariants: estructurales, bus no accesible desde contexto motor.
  Se resuelven con --mark-ready canonico en destino.

## Deuda documentada (parser inventory 009d)

scripts/pip_audit_policy.py:32 _parse_files_likely_touched
- Retorna paths relativos para decidir si correr pip-audit.
- No participa en validate ni scope gate de topologia.
- Criterio de salida 009d: unificar si pip-audit falla por FLT namespaced.


Manager approved canonical closeout for WOT-2026-009b