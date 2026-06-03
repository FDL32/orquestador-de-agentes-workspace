# orquestador_de_agentes_workspace — Claude Code Guide

@AGENTS.md

## Identidad de este repositorio

Este repo es el `repo_destino` de dogfooding del motor `orquestador_de_agentes`.
Funciona como cualquier proyecto destino del motor, pero su carga principal son
tickets para mejorar el propio motor.

- `repo_motor`: `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes\`
- `repo_destino` (este repo): `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\`
- Estado canonico: `.agent/collaboration/` de este repo.
- Enlace motor<->destino: `.agent/config/motor_destination_link.json` (gitignored).

## Rol y Alcance de Claude Code

Eres el agente principal y supervisor (orquestador de alto nivel) para este repositorio.
Trabaja sobre decisiones ya reflejadas en el codigo y en la documentacion.
No redefinas arquitectura sin confirmacion explicita.

## Flujo Especifico de Claude

Para cambios no triviales:
1. Lee primero los archivos relevantes (`PROJECT.md`, `CHANGELOG.md`).
2. Usa plan mode para proponer un plan breve si el cambio afecta a varias capas o es complejo.
3. Implementa el minimo cambio util iterativamente.
4. Ejecuta verificaciones usando `/quality-gates`.

Para operar por terminal en vez de por chat, lee el `QUICKSTART.md` del motor:
`..\orquestador_de_agentes\QUICKSTART.md` y `..\orquestador_de_agentes\INTERACTION_MODES.md`.

## Extensiones de Claude Code

- `/agent-status`: Muestra el estado del sistema multi-agente (turno, fases).
- `/quality-gates`: Ejecuta pip-audit + ruff + pytest-safe y muestra resultado.

## Reglas Modulares

Las reglas especificas por subsistema se cargan bajo demanda.
Lee `.claude/rules/README.md` para entender que modulos de contexto estan disponibles.
Si una regla entra en conflicto con el codigo real, prioriza el codigo y senala la discrepancia.
Si repites una correccion por segunda vez, propone anadirla a `AGENTS.md` o a un modulo en `.claude/rules/`.
