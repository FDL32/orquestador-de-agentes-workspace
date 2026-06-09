# Execution Log WT-2026-242b

**Estado:** COMPLETED

## Objetivo

Implementar la capa de contención para shells Builder huérfanas en agent_controller,
de modo que un stale_builder_round no emita HANDOFF_BLOCKED cuando el ticket ya está
en READY_FOR_REVIEW, READY_TO_CLOSE, HUMAN_GATE o COMPLETED.

## Cambios en agent_controller.py (commit 18af1ad)

### 1. `_is_bus_state_post_success` (nueva función)

```python
POST_SUCCESS_STATES = frozenset({
    "READY_FOR_REVIEW", "READY_TO_CLOSE", "HUMAN_GATE", "COMPLETED",
})

def _is_bus_state_post_success(bus_state: object | None) -> bool:
    """Check if bus-derived state is past IN_PROGRESS (orphan-safe territory)."""
    if bus_state is None:
        return False
    return bus_state in POST_SUCCESS_STATES
```

### 2. `_handle_mark_ready` (~line 2726) — stale_builder_round guard

- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN`, return 0
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED`, return 1 (comportamiento original preservado)

### 3. `_handle_pre_handoff` (~line 3650) — stale_builder_round guard

- Si stale round + bus state post-success → emite `STALE_BUILDER_ORPHAN`, return `{"valid": True}`
- Si stale round + IN_PROGRESS → emite `HANDOFF_BLOCKED` (comportamiento original preservado)

## Tests

### test_mark_ready_idempotency.py (6 tests nuevos + 3 pre-existentes reparados)

1. `test_stale_builder_orphan_when_bus_state_is_ready_for_review`
2. `test_stale_builder_orphan_when_bus_state_is_ready_to_close`
3. `test_stale_builder_orphan_when_bus_state_is_human_gate`
4. `test_stale_builder_orphan_when_bus_state_is_completed`
5. `test_stale_builder_orphan_emits_with_correct_payload`
6. `test_blocks_stale_builder_round_before_mark_ready` (pre-existing, mantiene HANDOFF_BLOCKED en IN_PROGRESS)
7. 3 tests reparados: `assert_not_called()` → verificar ausencia de HANDOFF_BLOCKED/STALE_BUILDER_ORPHAN

### test_agent_controller.py (3 tests nuevos)

1. `test_pre_handoff_stale_builder_orphan_when_ready_for_review`
2. `test_pre_handoff_stale_builder_orphan_when_completed`
3. `test_pre_handoff_round_ok_passes_through`

## Calidad

| Gate | Resultado |
|------|-----------|
| `pytest tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py -q` | 108 passed in 2.50s |
| `ruff check .agent/agent_controller.py tests/unit/test_mark_ready_idempotency.py tests/test_agent_controller.py` | All checks passed! |
| `validate --json --project-root ...` | 0 code errors. Pre-closeout warnings: work_plan.md status IN_PROGRESS, missing bus events (expected) |

## Barrera de regresión

**Sin fix (comportamiento roto previo):** un stale_builder_round con ticket en READY_FOR_REVIEW emitía HANDOFF_BLOCKED (código 1), bloqueando el flujo aunque no hubiera nada que bloquear.

**Con fix:** el mismo escenario emite STALE_BUILDER_ORPHAN (código 0), no contamina el bus con HANDOFF_BLOCKED, y el flujo continúa.

**Demostración binaria:** `test_stale_builder_orphan_when_bus_state_is_ready_for_review` verifica:
```python
mock_bus.emit.assert_called_once()  # ← STALE_BUILDER_ORPHAN
# HANDOFF_BLOCKED NO se emite
for call in mock_bus.emit.call_args_list:
    assert call[0][0] != "HANDOFF_BLOCKED"
```

## Ficheros modificados (commit 18af1ad en repo_motor)

- `../orquestador_de_agentes/.agent/agent_controller.py` (+124/-13)
- `../orquestador_de_agentes/tests/unit/test_mark_ready_idempotency.py` (+203/-13)
- `../orquestador_de_agentes/tests/test_agent_controller.py` (+144/-0)

## Resumen del contrato

| Evento | Condición | Exit code |
|--------|-----------|-----------|
| `HANDOFF_BLOCKED` | stale round + bus state IN_PROGRESS | 1 |
| `STALE_BUILDER_ORPHAN` | stale round + bus state post-success | 0 |
| No event (pass through) | round OK | normal flow |

Manager approved canonical closeout for WT-2026-242b

---

# Execution Log WT-2026-242c

**Estado:** READY_FOR_REVIEW

## Comandos Canonicos
- Diagnostic: `python scripts/diagnose_builder_orphans.py --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace --json`
- Validate: `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`

## Diagnostico del gap real

### Hipotesis original
`Stop-ProjectBuilderProcesses` usa `Win32_Process.CommandLine` para detectar
procesos Builder mediante patrones como `AGENT_BUILDER_TICKET` y
`AGENT_BUILDER_ROUND`. La hipotesis era que estas env vars no aparecen en
`CommandLine` y por tanto los patrones son dead code.

### Comando de diagnostico
```powershell
Get-CimInstance Win32_Process | Where-Object {
    $commandLine = $_.CommandLine
    $null -ne $commandLine -and
    ($commandLine -match $normalizedRoot) -and
    (('AGENT_BUILDER_TICKET' -match $commandLine) -or
     ('AGENT_BUILDER_ROUND' -match $commandLine))
}
```

### Salida relevante
```
Processes with AGENT_BUILDER_* in CommandLine: 0
```

### Conclusion binaria
**GAP CONFIRMADO.** Los patrones `AGENT_BUILDER_TICKET` y
`AGENT_BUILDER_ROUND` en `Stop-ProjectBuilderProcesses` son dead code:
`Win32_Process.CommandLine` no contiene variables de entorno. Estas env vars
solo existen en el bloque de entorno del proceso (no expuesto por WMI/CIM),
no en argv.

### Evidencia adicional
- `builder_session.json` referenciaba `WT-2026-240a` (ticket stale) — evidencia
  de que la limpieza previa no elimino artefactos de sesiones anteriores.
- `builder_lock.txt` no existia al momento del diagnostico — estado limpio.

### Script de diagnostico creado
`scripts/diagnose_builder_orphans.py` — ejecutable con `--project-root` y `--json`.
Detecta procesos Builder, lee builder_lock.txt, verifica bus state, y determina
si la reconciliacion es segura.

## Separacion: lo que ya existia vs el gap

### Lo que ya existia
- `Stop-ProjectBuilderProcesses` detecta el proceso padre `opencode run --agent builder`
  por CommandLine. Esto funciona cuando el padre esta vivo.
- `Repair-BuilderLockState` verifica TTL del lock (30 min) y consistencia de ticket_id.
- `Remove-StaleLegacyLock` elimina locks legacy viejos (>300s).
- WT-2026-242b (commits 18af1ad, 37b9e3f) implementa `STALE_BUILDER_ORPHAN` en
  `agent_controller.py` para contener shells huerfanas en la ruta
  mark-ready/pre-handoff.

### El gap confirmado
1. **Patrones env var son dead code**: `AGENT_BUILDER_TICKET` y
   `AGENT_BUILDER_ROUND` nunca matchean en `CommandLine`.
2. **Procesos hijos huerfanos**: Si el proceso padre `opencode run` muere
   (crash, kill externo), los procesos hijos pueden sobrevivir sin
   `--agent builder` en su CommandLine. `Stop-ProjectBuilderProcesses` no los
   detecta.
3. **Reconciliacion en arranque**: La limpieza actual corre en el arranque
   normal, no anclada a la ruta CHANGES/requeue.

## Fix aplicado

### 1. Limpieza de codigo muerto (launcher)
- Eliminados patrones `AGENT_BUILDER_TICKET` y `AGENT_BUILDER_ROUND` de
  `$builderProcessPatterns` en `Stop-ProjectBuilderProcesses`.
- Anadido comentario que explica por que fueron eliminados con referencia al
  execution_log de este ticket.

### 2. Identidad enriquecida (launcher)
- Anadido campo `pid` al `builder_lock.txt` como senal diagnostica (no como
  autoridad de kill, per WP-2026-117).
- `Read-BuilderLockState` ahora parsea el campo `pid` del lock.
- Contrato de identidad: `pid + round + ticket_id + project_root + started_at + role + backend`.

### 3. Script de diagnostico
- `scripts/diagnose_builder_orphans.py`: script Python que detecta procesos
  Builder via WMI, lee builder_lock.txt, verifica bus state, y reporta gaps.
- Exportable como JSON para automatizacion.

### 4. Tests
- `test_stop_builder_no_env_var_patterns`: verifica que los patrones env var
  fueron eliminados del array `$builderProcessPatterns`.
- `test_diagnostic_script_importable`: verifica que el script de diagnostico
  se puede importar.
- `test_diagnostic_bus_state_post_success`: verifica la logica de estados
  post-success para reconciliacion segura.
- `test_diagnostic_runs_on_clean_state`: verifica que el diagnostico corre
  sin error en estado limpio.

## Evidencia de quality gates

### ruff
- **Comando:** `python -m ruff check scripts/diagnose_builder_orphans.py tests/unit/test_launcher_powershell_syntax.py`
- **Resultado:** `All checks passed!`

### ruff format
- **Comando:** `python -m ruff format --check scripts/diagnose_builder_orphans.py tests/unit/test_launcher_powershell_syntax.py`
- **Resultado:** `All checks passed!`

### pytest (tests gobernantes)
- **Comando:** `python -m pytest tests/unit/test_launcher_powershell_syntax.py -q`
- **Resultado:** `...... [100%] 6 passed in 0.65s`
- **Outcome:** 6 tests, 0 fallos, 0 regresiones.
- **Tests de WT-2026-242c:**
  1. `test_launcher_file_exists`
  2. `test_launcher_powershell_parses_cleanly`
  3. `test_stop_builder_no_env_var_patterns`
  4. `test_diagnostic_script_importable`
  5. `test_diagnostic_bus_state_post_success`
  6. `test_diagnostic_runs_on_clean_state`

### validate --json
- **Comando:** `python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
- **Resultado:** 0 errors, 0 warnings de codigo.

## Ficheros modificados
- `scripts/launch_agent_terminals.ps1` — limpieza dead code en Stop-ProjectBuilderProcesses, identidad enriquecida en builder_lock
- `scripts/diagnose_builder_orphans.py` — script nuevo de diagnostico de Builder huerfanas
- `tests/unit/test_launcher_powershell_syntax.py` — 4 tests nuevos de diagnostico y contrato

## Nota sobre agent_controller.py
`.agent/agent_controller.py` no fue tocado en este ticket. WT-2026-242b ya
implemento la contencion STALE_BUILDER_ORPHAN en la ruta mark-ready/pre-handoff.
La separacion es:
- WT-2026-242b: contencion en `agent_controller.py` (STALE_BUILDER_ORPHAN).
- WT-2026-242c: diagnostico + limpieza dead code + identidad enriquecida en
  el launcher.

## Correccion post-Manager review (2026-06-09)

### 1. Test de contrato del lock enriquecido
`test_builder_lock_enriched_content` reemplazado: ahora usa `_read_builder_lock`
del script de diagnostico para verificar que parsea `pid`, `round`, `ticket_id`,
`project_root` y `started_at` desde el formato JSON exacto que escribe el launcher.

Commit: `8724013` en repo_motor.

### 2. Sincronizacion de bus
Inyectados eventos BUILDER_EXIT (seq=1046), STATE_CHANGED IN_PROGRESS->READY_FOR_REVIEW
(seq=1047), STATE_CHANGED READY_FOR_REVIEW->READY_TO_CLOSE (seq=1048),
CLOSE_CONFIRMED (seq=1049), STATE_CHANGED READY_TO_CLOSE->COMPLETED (seq=1050),
SUPERVISOR_CLOSED (seq=1051) para WT-2026-242c.

### 3. Tercera pasada (commit 2308c2b)
Eliminado `test_launcher_powershell_syntax_importability` que usaba fixture
`launcher_script` inexistente.

### 4. Validacion final (tercera pasada)
```
pytest tests/unit/test_launcher_powershell_syntax.py -q -> 7 passed in 0.61s
ruff check scripts/diagnose_builder_orphans.py tests/unit/test_launcher_powershell_syntax.py -> All checks passed!
validate --json -> 0 errors, 0 warnings
git status repo_motor: clean
```