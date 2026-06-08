# Work Ticket - WT-2026-242a

## Metadata
- **ID:** WT-2026-242a
- **Title:** Hacer try-first con JSON real en el review bridge de OpenCode
- **Scope:** system/review-bridge-json-transport
- **Priority:** Alta
- **Estado:** COMPLETED
- **deliverable_type:** code
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-241a

## Objetivo
Endurecer el `review_bridge` para que, cuando el backend del Manager sea
OpenCode, la review intente `--format json` usando el `manager_executable` real
de esa ejecucion, sin depender de `opencode.cmd` en `PATH` ni de una deteccion
stale calculada en `__init__`.

## Contexto verificado
- `WT-2026-241a` entro en `HUMAN_GATE` con `parse_method: text_regex` aunque el
  review del Manager terminaba en `DECISION: CHANGES`.
- La auditoria de codigo confirmo la causa raiz:
  - `ReviewBridge.__init__()` calcula una sola vez
    `self._supports_json_format`.
  - `_detect_json_format_support()` prueba `opencode.cmd run --help` por `PATH`
    e ignora el `manager_executable` real que el launcher resolvio.
  - Si ese lookup falla, el bridge no anade `--format json` y cae en
    `text_regex`, que degrada `CHANGES` a `INSPECT`.
- El problema afecta el estado canonico del ticket y debe corregirse antes de
  relanzar el sistema multiagente.

## Problema
El bridge puede inferir falsamente que OpenCode no soporta JSON aunque el
ejecutable real si lo soporte. Eso desvía la review a texto plano, cambia la
decision operativa del Manager y puede empujar tickets validos a `HUMAN_GATE`.

## Contrato
- El ticket es `code`: el cambio vive en `repo_motor` y requiere evidencia
  real.
- La ruta OpenCode del bridge debe usar enfoque `try-first`:
  - intentar `--format json` con el `manager_executable` real;
  - hacer fallback sin JSON solo si el stderr indica de forma concreta que el
    flag no es soportado;
  - no usar `exit_code != 0` por si solo como criterio de fallback.
- `_supports_json_format` como campo de instancia calculado en `__init__` debe
  dejar de gobernar la decision JSON/no-JSON. Si el Builder elige eliminarlo,
  debe eliminar las referencias restantes. Si el Builder prefiere mantener una
  cache local dentro de `_run_opencode_review`, `__init__` ya no puede llamar a
  `_detect_json_format_support()`.
- Los patrones de fallback permitidos deben ser explicitos y acotados, por
  ejemplo:
  - `unknown flag`
  - `invalid option`
  - help banner / salida de ayuda del CLI
- `APPROVE` sigue siendo fuerte solo desde `json_final_answer`.
- El output del intento fallido por flag no soportado se descarta por completo;
  el fallback debe arrancar como proceso nuevo con output limpio.
- Este ticket no abre todavia `CHANGES` desde `text_regex`.

## Files Likely Touched
- `bus/review_bridge.py`
- `tests/test_review_bridge.py`

## Decision Arquitectonica
- El seam correcto es la ruta OpenCode del `review_bridge`, no el launcher ni el
  `agent_controller`.
- El sistema debe preferir verdad operacional sobre capability detection
  cacheada.
- El fallback sin JSON debe estar gobernado por senales observables del
  ejecutable real, no por heuristicas de entorno en `PATH`.

## Non-goals
- No cambiar todavia la politica de `text_regex` para aceptar `CHANGES`.
- No tocar la logica de `STALE_BUILDER_ORPHAN`; eso va en un ticket separado.
- No rehacer la arquitectura general del bridge; solo endurecer la decision
  JSON/no-JSON y su trazabilidad.

## Plan de ejecucion
1. Reemplazar la deteccion stale de soporte JSON por una ruta `try-first`
   dentro de la review OpenCode.
2. Intentar la ejecucion con `--format json` usando el `manager_executable`
   real y hacer fallback solo ante patrones concretos de flag no soportado.
3. Mantener la regla conservadora: `APPROVE` solo desde `json_final_answer`.
4. Anadir tests gobernantes y registrar comandos/resultados exactos en
   `execution_log.md`.

## Quality Gates
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m pytest tests/test_review_bridge.py -q`
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe -m ruff check bus/review_bridge.py tests/test_review_bridge.py`
- `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.venv\Scripts\python.exe C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\.agent\agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace`

## Handoff al Builder
- Mantente dentro de `bus/review_bridge.py` y `tests/test_review_bridge.py`
  salvo evidencia nueva fuerte.
- El bug observado no es "OpenCode no soporta JSON", sino "el bridge decide mal
  si intentarlo". No tapes el problema relajando `text_regex`.
- Registra evidencia de:
  - intento JSON con ejecutable real fuera de `PATH`;
  - fallback solo ante flag no soportado;
  - `APPROVE` textual sigue degradando a `INSPECT`.
- El gate `pytest tests/test_review_bridge.py -q` debe cubrir tanto los tests
  nuevos como regresion sobre los casos ya existentes en ese archivo.
