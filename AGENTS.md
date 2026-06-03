# AGENTS.md - Instrucciones Transversales del Repositorio

## Vocabulario canonico (leer antes de actuar)

Este repo es `repo_destino` de dogfooding del motor. No usar "workspace" a secas.

| Termino | Descripcion |
|---------|-------------|
| `repo_motor` | `orquestador_de_agentes/` — motor portable, fuente canonica |
| `repo_destino` | Este repositorio (`orquestador_de_agentes_workspace/`) — donde viven tickets y estado |
| `workspace_activo` | Raiz operativa con `.agent/` desde la que corre el ticket actual (= este repo) |
| `entorno_multi_root` | IDE con `repo_motor` + `repo_destino` abiertos a la vez |

**Regla de repos:** operaciones git del tooling corren en `repo_motor`. Estado operativo (tickets, memoria) vive aqui en `repo_destino`.

**Regla de nomenclatura de tickets:** este `repo_destino` usa el prefijo `WT-YYYY-NNN` por ser dogfooding del motor. Un proyecto destino normal declara su prefijo en `PROJECT.md` como `Ticket prefix: XXX`.

## Agentes disponibles

- Claude Code: agente principal y supervisor.
- Codex / GitHub Copilot: agentes soportados si leen este archivo dentro del arbol.
- OpenCode: backend del Builder con contrato local en `.opencode/`.
- Goose / Claw: motores orquestados por `scripts/orquestador.py`.

## Resumen del entorno

- Runtime: Python 3.10+, `pathlib`, `typing`.
- Package manager: `uv` (`uv add <lib>`, nunca `pip` directo).
- Testing y calidad: `pytest`, `ruff`.
- Seguridad: `gitleaks`, `pip-audit`.
- Motor externo: `orquestador_de_agentes/` — enlazado via `.agent/config/motor_destination_link.json`.

## Rutas importantes

- `agent_system/`: copia instalada del framework del motor en este destino.
- `scripts/`: utilidades instaladas del motor para este destino.
- `skills/`: micro-habilidades instaladas del motor para este destino.
- `.agent/collaboration/`: estado operacional canonico de este destino.
- `.agent/runtime/memory/`: memoria persistente de este proyecto.
- `.agent/config/motor_destination_link.json`: enlace motor<->destino (gitignored, local).
- `REPOSITORY_STRUCTURE.md`: mapa interno del repositorio.

## Comandos principales

- Sincronizar desde motor: `python scripts/install_agent_system.py --sync`
- Vista previa sync: `python scripts/install_agent_system.py --sync --dry-run`
- Estado del sistema: `python orquestador_de_agentes/.agent/agent_controller.py --validate --project-root .`
- Tests: `python scripts/run_pytest_safe.py`
- Calidad: `ruff check . && ruff format .`
- Auditoria de dependencias: `python scripts/pip_audit_project.py` (via `repo_motor`)

## Convenciones

- Lee `PROJECT.md` antes de tocar arquitectura o estado.
- Usa `pathlib` y `try/except` explicito para I/O.
- El estado canonico vive en `.agent/collaboration/work_plan.md` y `execution_log.md`.
- No mezcles contenido del `repo_motor` con estado del `repo_destino`.

### Anti-patrones de testing

- Platform-attribute stub sin `raising=False`: al parchear atributos opcionales de modulos stdlib
  que no existen en todas las plataformas (como `subprocess.DETACHED_PROCESS` en POSIX), usa
  `monkeypatch.setattr(..., raising=False)`. Sin ese flag, `monkeypatch` puede lanzar
  `AttributeError` en CI aunque el atributo sea un stub intencional.

## Memoria por proyecto

- `.agent/runtime/memory/observations.jsonl`: observaciones persistentes de este destino (wing `project`).
- `.agent/runtime/memory/MEMORY.md`: indice humano acotado (tope 80 lineas).
- Wings `engine` y `meta`: se reciben del `repo_motor` via sync; para promocion upstream ver `prompts/memory_upload.md` en el motor.
- Regenera el indice solo de forma explicita.

## Secretos y seguridad

- No guardes credenciales, tokens ni rutas sensibles.
- No toques `privada/`.
- No desactives `guard_paths` para trabajar mas rapido.
- No pidas dependencias nuevas sin aprobacion.

## Criterio de cierre

Considera una tarea cerrada solo cuando:
1. `ruff`, `pytest` y `pip-audit` pasan.
2. El codigo nuevo usa rutas y manejo de errores correctos.
3. Las decisiones importantes quedan consolidadas en `PROJECT.md` o `CHANGELOG.md`.
