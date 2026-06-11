# BUILDER BRIEF WT-2026-249a

## Mision
Endurecer el contrato CLI minimo del controlador sin convertir este ticket en
una reescritura de `agent_controller.py`.

Hay dos fixes obligatorios y solo dos:
1. eliminar `stderr + returncode 0` en la rama stale orphan;
2. evitar que el wrapper de `session close` propague `stderr` del hijo cuando
   el hijo termina con `returncode == 0`.

No lances Builder hasta que el `work_plan.md` activo del `repo_destino` apunte
canonicamente a `WT-2026-249a`; si sigue apuntando a `248a`, `--mark-ready`
bloqueara por FLT incorrecto.

## Objetivo binario
Al final del ticket deben cumplirse estas tres condiciones:
1. stale orphan termina limpio: `returncode 0`, sin `stderr` contaminante;
2. session close exitoso no propaga `stderr` del subproceso al padre;
3. session close fallido si sigue propagando `stderr` y conserva returncode no
   cero.

## Superficie autorizada
### Files Likely Touched
- `.agent/agent_controller.py`
- `tests/test_agent_controller.py`

### Read/inspect only
- `.agent/collaboration/PLAN_WT-2026-249a.md`
- `.agent/collaboration/AUDIT_WT-2026-249a.md`
- `.agent/collaboration/execution_log.md`
- `scripts/session_closeout.py`
- `prompts/audit_agent_output.md`

## Reglas duras
- No arregles "todo stderr"; arregla solo los dos contratos verificados.
- No toques rutas `stderr + returncode 1` solo por limpieza visual.
- No metas helpers globales `_emit_cli_*` en esta pasada.
- No uses parseo de strings para clasificar severidad; usa `returncode`.
- No cierres sin tests de contrato observables.

## Implementacion esperada

### Fix 1 - stale orphan
- Localiza la rama en `_handle_pre_handoff`.
- Si el comando retorna `0`, no debe escribir warning en `stderr`.
- Destino exacto del warning:
  - `json_output=False` => warning a `stdout`;
  - `json_output=True` => sin warning textual libre.
- Mantener el comportamiento funcional: salida limpia, sin pollution del bus.

### Fix 2 - session close wrapper
- Localiza la rama que hoy hace:
  - imprimir `result.stdout`;
  - reenviar siempre `result.stderr`.
- Cambia el criterio:
  - `result.returncode == 0` => no propagar `stderr` como error del padre;
  - `result.returncode != 0` => si propagar `stderr`.

## Evidencia obligatoria en execution_log.md
Debes dejar estas tres piezas de evidencia con comando exacto y resultado:
1. stale orphan:
   - barrera de regresion explicita del comportamiento roto previo;
   - prueba que confirme `returncode 0`;
   - prueba que confirme `stderr` vacio.
   - prueba que confirme ausencia de eventos al bus en esta rama.
2. session close exitoso:
   - prueba que confirme ausencia de `stderr` propagado por el padre.
3. session close fallido:
   - prueba que confirme propagacion de `stderr` y returncode no cero.

## Quality gates
```powershell
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests/test_agent_controller.py -v
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check .agent/agent_controller.py tests/test_agent_controller.py
C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe .agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
```

El `pytest` de arriba no es solo para los tests nuevos: debe servir tambien
como comprobacion de que `tests/test_agent_controller.py` completo sigue verde
tras el fix.

## Cierre esperado
No intentes `--mark-ready` hasta tener:
- fix minimo en controller;
- tests focales verdes;
- quality gates verdes;
- commit visible con `WT-2026-249a`;
- evidencia registrada de los tres contratos observables.
