# AUDIT_WT-2026-230a

## Tipo
Devx / instalador / bootstrap de destino. Tier 3.

## Evidencia minima requerida
- Diff productivo revisable en `repo_motor` con commit `WT-2026-230a`.
- `scripts/destination_context.py` presente y probado.
- `prompts/destination_bootstrap.md` presente.
- Provisionado nuevo integrado en `install_agent_system.py` para `install` y `sync`.
- Tests focales de destino virgen, truncamiento y ausencia de git.
- `ruff` limpio y `validate --json` 0/0.

## TP Check
TP-01: `destination_context.py` vive en `repo_motor`; el destino no recibe wrappers
  ejecutables duplicados.
TP-02: `destination_bootstrap.md` ordena leer
  `.agent/config/motor_destination_link.json` antes de invocar el script.
TP-03: un destino sin `graphify-out/` genera `destination_map.md` util igualmente.
TP-04: git ausente o repo no versionado no hace crash.
TP-05: el mapa respeta `max_bytes`; truncamiento preserve identidad + estado operativo.
TP-06: `install` y `sync` crean `.agent/context/` y `destination_context.json`
  sin pisar customizaciones locales; el mecanismo concreto evita imitar el overwrite
  de `copy_repomix_config`.
TP-07: `session_bootstrap.md` documenta correctamente el desvio a modo destino.
TP-08: no se introducen Repomix en arranque, skill, cache ni cambios a `--validate`.

## Blockers esperados
- CRITICO: copiar `destination_context.py` o wrappers equivalentes al destino
  (rompe el contrato de logica-en-motor).
- CRITICO: depender de Graphify, Node o Repomix para el primer arranque.
- CRITICO: truncar el mapa de forma que se pierda identidad, ticket activo o estado operativo.
- CRITICO: Builder lee o escribe un path real bajo `repo_destino` / `workspace_activo`
  durante la implementacion, incluido `.agent/config/motor_destination_link.json`.
- ALTO: reutilizar `_get_canonical_files()` por import acoplado desde `ReviewBridge`
  en vez de usar una lista propia o helper extraido explicitamente.
- ALTO: crear cache o perfiles por capas dentro de este ticket.
- ALTO: modificar `agent_controller --validate` para meter descubrimiento/topologia.
- MEDIO: `install`/`sync` pisan `destination_context.json` si el destino ya lo personalizo.
- MEDIO: ausencia de git lanza traceback en vez de degradar limpio.
- ALTO: Builder toca `.agent/collaboration/`, `.agent/runtime/` o `backlog.md`
  durante la implementacion de este ticket.

## Revision Manager
El Manager debe verificar mecanicamente:
- `git -C C:\Users\fdl\Proyectos_Python\orquestador_de_agentes log --oneline -3`
  contiene commit con `WT-2026-230a`.
- `git show --stat <commit>` toca `scripts/destination_context.py`,
  `scripts/install_agent_system.py`, prompts y tests esperados.
- `python -m pytest tests/test_destination_context.py -v` -> todos pasan.
- `python -m pytest tests/test_install_agent_system.py -q` -> sin regresiones.
- `ruff check scripts/install_agent_system.py scripts/destination_context.py`
  -> All checks passed.
- `python ../orquestador_de_agentes/.agent/agent_controller.py --validate --json --project-root .`
  -> 0/0.
- `destination_bootstrap.md` resuelve `motor_root` via link local antes de invocar el script.
- No hay wrappers `destination_context.ps1/.bat/.sh` nuevos en el destino.
- No hay cambios a Repomix ni a `agent_controller --validate` salvo evidencia nueva
  y justificacion CEM explicita.
- El diff productivo del Builder se limita a `scripts/`, `prompts/` y `tests/` del
  `repo_motor`; no hay escritura de Builder en `.agent/collaboration/`.
- La Fase 0 del Builder no accede a `repo_destino/.agent/config/`; confirma el contrato
  leyendo `scripts/install_agent_system.py` y `runtime/motor_link.py` en `repo_motor`.
