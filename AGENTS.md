# AGENTS.md - Instrucciones Transversales del Repositorio

## Agentes disponibles

- Claude Code: agente principal y supervisor.
- Codex / GitHub Copilot: agentes soportados si leen este archivo dentro del arbol.
- OpenCode: backend soportado para Builder con contrato local en `orquestacion_agentes/.opencode/`.
- Goose / Claw: motores orquestados por `scripts/orquestador.py`.

## Resumen del entorno

- Runtime: Python 3.10+, `pathlib`, `typing`.
- Package manager: `uv` (`uv add <lib>`, nunca `pip` directo).
- Testing y calidad: `pytest`, `ruff`.
- Seguridad: `gitleaks`, `pip-audit`.

## Rutas importantes

- `agent_system/`: codigo base de apoyo incluido con la plantilla.
- `scripts/`: utilidades de instalacion, upgrade, rollback y validacion.
- `skills/`: micro-habilidades reutilizables.
- `.agent/collaboration/`: estado operacional canonico.
- `.agent/runtime/memory/`: memoria persistente por proyecto.
- `.agent/council/`: broker de consejo y auditoria paralela.
- `REPOSITORY_STRUCTURE.md`: mapa interno publicable del repositorio.

## Contrato de version y portabilidad

- `pyproject.toml` define la version del paquete portable.
- `.agent/.version_manifest.json` define la version tecnica del core.
- Los comandos canonical y legacy se documentan por separado.
- Estado actual: `v9.5.0` terminal-driven closeout completado, plantilla lista para copiar al siguiente proyecto.
- Este repositorio se trata como autonomo al publicar; evita depender de rutas o metadatos del workspace padre en la documentacion publica.

## Comandos principales

- Instalacion inicial: `python scripts/install_agent_system.py --install`
- Sincronizacion estricta: `python scripts/install_agent_system.py --sync`
- Sincronizacion interactiva: `python scripts/install_agent_system.py --sync --prune`
- Vista previa: `python scripts/install_agent_system.py --sync --dry-run`
- Estado del sistema: `python .agent/agent_controller.py`
- Interaccion por terminal: `python scripts/ticket_supervisor.py --reactive`
- Tests: `python scripts/run_pytest_safe.py`
- Calidad: `ruff check . && ruff format .`
- Auditoria de dependencias: `uv run pip-audit .`

## Convenciones

- Lee `PROJECT.md` antes de tocar arquitectura o estado.
- Lee `INTERACTION_MODES.md` antes de operar por chat o por terminal.
- Usa `pathlib` y `try/except` explicito para I/O.
- Mantiene la raiz limpia: no metas basura temporal en el arbol portable.
- Usa `.agent/collaboration/work_plan.md` y `.agent/collaboration/execution_log.md` para el estado canonico.

### Anti-patrones de testing

- Platform-attribute stub sin `raising=False`: al parchear atributos opcionales de modulos stdlib que no existen en todas las plataformas, como `subprocess.DETACHED_PROCESS` en POSIX, usa `monkeypatch.setattr(..., raising=False)`. Sin ese flag, `monkeypatch` puede lanzar `AttributeError` en CI aunque el atributo sea un stub intencional.

## Ticket namespaces

- Este motor usa `WP-YYYY-NNN`.
- Los proyectos destino declaran su prefijo local en `PROJECT.md` como `Ticket prefix: XXX` y usan `XXX-YYYY-NNN`.
- El prefijo es documental; el bus, `work_plan.md`, `execution_log.md`, `TURN.md` y `STATE.md` funcionan igual.

## Memoria por proyecto

- `.agent/runtime/memory/observations.jsonl` guarda observaciones persistentes.
- `.agent/runtime/memory/MEMORY.md` es un indice humano acotado, con tope de 80 lineas.
- La historia completa y la busqueda profunda viven en `observations.jsonl`, no en `MEMORY.md`.
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
