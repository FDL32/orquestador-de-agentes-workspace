# Execution Log WT-2026-242a

**Estado:** READY_FOR_REVIEW
**Commit final:** `a76a28b` - `feat(WT-2026-242a): harden review bridge JSON try-first fallback`

## Comandos Canonicos
- Launch script: `powershell -ExecutionPolicy Bypass -File C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\scripts\launch_agent_terminals.ps1 -ProjectRoot C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
- Validate: `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`

## Preflight de activacion
- `WT-2026-241a` dejo una causa raiz confirmada en el `review_bridge`: la
  decision JSON/no-JSON depende de un probe por `PATH`, no del ejecutable real.
- `WT-2026-241a` queda superseded por `WT-2026-242a` por
  `root cause in review_bridge JSON capability path`.
- El siguiente trabajo se separa como ticket nuevo para no mezclar el
  `HUMAN_GATE` operativo del ticket anterior con el fix de transporte.
- El scope queda concentrado en la ruta OpenCode del `repo_motor`.

## Hipotesis operativa
- El bridge debe dejar de inferir capacidades desde un estado cacheado y pasar a
  probar `--format json` con el `manager_executable` real.
- El fallback sin JSON debe dispararse solo cuando el stderr o la ayuda del CLI
  indiquen de forma concreta que el flag no es soportado.

## Tareas ejecutadas por el Builder
- [x] Implementar la ruta `try-first` en `bus/review_bridge.py`.
- [x] Mantener la asimetria conservadora: `APPROVE` textual sigue siendo `INSPECT`.
- [x] Anadir y ejecutar los tests gobernantes del bridge (4 tests en `TestTryFirstJsonTransport`).
- [x] Corregir RUF059 en `test_review_bridge.py` (lineas 1486 y 1513).
- [x] Committear entrega final en `repo_motor` (`a76a28b`, arbol limpio).

## Evidencia de quality gates

### ruff
- **Comando:** `python -m ruff check bus/review_bridge.py tests/test_review_bridge.py`
- **Resultado:** `All checks passed!`
- **Outcome:** 0 errores, 0 warnings.

### pytest (tests gobernantes + regresion)
- **Comando:** `python -m pytest tests/test_review_bridge.py -q`
- **Resultado:** `...................................................... [100%] 54 passed in 2.34s`
- **Outcome:** 54 tests, 0 fallos, 0 regresiones.
- **Tests de WT-2026-242a (TestTryFirstJsonTransport):** 4 passed:
  1. `test_opencode_review_uses_json_when_executable_off_path`
  2. `test_opencode_review_falls_back_without_json_on_unsupported_flag_error`
  3. `test_opencode_review_degrades_textual_approve_to_inspect_after_fallback`
  4. `test_opencode_review_does_not_fallback_on_generic_failure`

### validate --json
- **Comando:** `python .agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`
- **Resultado:**
```json
{
  "errors": {},
  "warnings": {}
}
```
- **Outcome:** 0 errors, 0 warnings.

## Ficheros modificados
- `bus/review_bridge.py` - ruta try-first con `--format json` usando `manager_executable` real
- `tests/test_review_bridge.py` - 4 tests gobernantes + correccion RUF059
