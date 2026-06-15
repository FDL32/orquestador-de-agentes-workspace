# Execution Log: WOT-2026-009b - Scope gate topology-aware

## Metadata

**Estado:** READY_FOR_REVIEW
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

```json
{
  "errors": { "work_plan.md": [], "execution_log.md": [], "notifications.md": [],
    "consistency": [], "TURN.md": [], "host_project_prefix": [], "git_presence": [] },
  "warnings": {}
}
```

## Preflight obligatorio

### Inventario parsers FLT

Comando: `rg "parse_files_likely_touched" .agent scripts bus tests --type py -n`

Resultado (5 parsers):
1. scope_gate.py:98 — canonical (deliverable-aware desde 009a)
2. agent_controller.py:318 — wrapper sobre scope_gate
3. motor_checkpoint.py:130 — parse_raw_flt_paths (retorna paths relativos)
4. scripts/pre_handoff_guard.py:272 — parser propio independiente
5. scripts/pip_audit_policy.py:32 — _parse_files_likely_touched (scope-insensible)

Parsers actualizados en 009b: (3) y (4).
Deuda 009d: (5) pip_audit_policy — inventariado; no toca topologia.

### _check_scope_for_validate verificado

Existe en agent_controller.py:3857. Actualizado en este ticket para usar
get_productive_changed_files(delivery_authority) y parse_flt_namespaced.

## Implementacion (Builder)

### Paso 1: scope_gate.py

- Extraidos `_looks_like_path_token` y `_normalize_flt_line` como helpers de modulo.
- Nueva funcion `_parse_flt_section(lines)` -> (has_namespaces, [(ns, path)]).
- Nueva funcion `parse_flt_namespaced(content, *, motor_root, project_root, delivery_authority)`
  retorna `{"motor": set, "destino": set}`.
- Complexity C901: resuelta extrayendo _parse_flt_section como helper separado.

### Paso 2: motor_checkpoint.py

- `parse_raw_flt_paths`: ahora reconoce `### repo_motor` / `### repo_destino`.
- Rutas bajo `### repo_destino` se excluyen del retorno.
- Rutas planas y bajo `### repo_motor` se retornan (backward-compat).

### Paso 3: agent_controller.py

- Nuevo wrapper `parse_flt_namespaced(plan_content)`.
- Nuevo `get_productive_changed_files(delivery_authority)`: diff del root productivo.
- `_check_scope_for_validate`: usa delivery_authority para elegir diff y whitelist.
  Para repo_motor: valida diff motor contra whitelist motor; emite warning con
  diagnostico (root validado, subseccion esperada, comando para revalidar).
  Para repo_destino: comportamiento anterior intacto.
- `_run_pre_handoff_guard`: pasa `--motor-root` si motor_root != project_root.

### Paso 4: scripts/pre_handoff_guard.py

- `parse_files_likely_touched(project_root, motor_root=None)`: namespace-aware.
  Con namespaces: rutas motor contra motor_root, rutas destino contra project_root.
  Sin namespaces: flat backward-compat (todas contra project_root).
- `run_guard(project_root, ticket_id, motor_root=None)`: acepta motor_root.
- CLI: acepta `--motor-root` para passar motor_root al guard.

### Paso 5: tests/unit/test_scope_gate_topology.py (nuevo)

12 tests: 7 para parse_flt_namespaced, 5 para parse_raw_flt_paths.
Cubren: namespace motor/destino separados, flat backward-compat,
unknown sub-headings ignorados, empty FLT, destino-only sin motor.

## Gates

- ruff check: exit 0
- pytest focales (unit/ + pre_handoff_guard + mark_ready_motor_scope): 1151/0/0
- pytest suite completa via run_pytest_safe.py: exit 0

## Motor commit

- c308f40 feat(WOT-2026-009b): topology-aware FLT namespace parsing

## Validate final destino

```json
{
  "errors": { "work_plan.md": [], "execution_log.md": [], ... },
  "warnings": {
    "ticket_prose": ["[TP-PROSE-04]...", "[TP-PROSE-10]..."],
    "bus_drift": ["No STATE_CHANGED event found in bus for ticket WOT-2026-009b"]
  }
}
```

ticket_prose: warnings de estilo del work_plan, no bloquean cierre de codigo.
bus_drift: esperado pre-mark-ready. Se resuelve con --mark-ready canonico.

## Deuda documentada (parser inventory 009d)

Parser 5: scripts/pip_audit_policy.py:32 `_parse_files_likely_touched`
- Retorna paths relativos para decidir si correr pip-audit.
- No participa en validate ni scope gate.
- No afectado por topologia motor/destino.
- Criterio de salida 009d: unificar solo si pip-audit comienza a fallar
  por no encontrar manifiestos en FLT namespaced.
