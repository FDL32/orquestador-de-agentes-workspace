# AUDIT_WT-2026-237a

## Riesgos Bloqueantes

### CRITICO - ticket code sin diff productivo real
Bloquear si `WT-2026-237a` intenta cerrar solo con narrativa o validaciones
documentales. Un ticket `code` necesita diff revisable en `repo_motor`.

### CRITICO - scope incompleto
Bloquear si Builder toca archivos de `repo_motor` fuera de `Files Likely Touched`
o si falta algun test/config/wrapper que razonablemente vaya a cambiar.

### ALTO - gates irreales o incompletos
Bloquear si `pytest`/`ruff` apuntan a rutas genericas o inexistentes, o si falta
evidencia funcional cuando se toca `scripts/launch_agent_terminals.ps1`.

### ALTO - recontaminacion del smoke
Bloquear si el ticket reabre `WT-2026-236a`, modifica su reporte o mezcla codigo
de motor con artefactos documentales previos.

### ALTO - closeout sin higiene de packaging
Bloquear si `execution_log.md` no deja evidencia de gates reales, si el commit no
referencia `WT-2026-237a` exacto o si `--pre-handoff` ve drift transitorio de
`.opencode/opencode.json`.

### MEDIO - fixture irreal en PowerShell
Si se toca el launcher, el test debe reproducir el runtime con `Set-StrictMode`
y un fixture JSON realista; no basta un parse textual del `.ps1`.

## TP Check

TP-01: leer el codigo real de `bus/review_bridge.py`,
`.agent/agent_controller.py`, `scripts/state_projection_sync.py`,
`scripts/state_projection_probe.py` y `scripts/launch_agent_terminals.ps1`
antes de proponer nuevos cambios.

TP-02: verificar que `Files Likely Touched` cubre codigo, tests y wrappers
que Builder vaya a tocar.

TP-03: cualquier gap residual se demuestra con test o evidencia directa de
runtime; no basta una referencia conversacional al smoke.

TP-04: `pytest` focal pasa y queda registrado con exit code real.

TP-05: `ruff` focal pasa y queda registrado con exit code real.

TP-06: `validate` canonico pasa o deja blocker exacto documentado.

TP-07: el commit final referencia `WT-2026-237a` exacto y el review packet ya no
mezcla fixes de motor con un ticket documental.

## Comandos de Revision

```powershell
git -C C:\Users\fdl\Proyectos_Python\orquestador_de_agentes show --stat HEAD
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py -q
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check bus/review_bridge.py .agent/agent_controller.py scripts/state_projection_sync.py scripts/state_projection_probe.py tests/test_manager_review_bridge.py tests/test_agent_controller.py tests/test_launch_agent_terminals_script.py
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

## Veredicto Previo

`APPROVED`: el ticket es la via correcta para separar codigo de motor del smoke
documental. El Builder debe demostrar primero si quedan gaps reales y luego
cerrarlos con gates de codigo y packaging limpio.
