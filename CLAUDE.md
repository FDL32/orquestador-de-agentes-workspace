sh
bootst# z_scripts - Claude Code Guide

@AGENTS.md

## Router: donde se trabaja

> **Esta raiz (`z_scripts/`) es un contenedor meta, NO el producto.** No es repo
> git, duplica estructura heredada (`_legacy/`, `_backups/`, copias de `.agent/`,
> `scripts/`, `skills/`). No trabajes aqui salvo mantenimiento meta explicito.
>
> **El proyecto operativo es `orquestacion_agentes/`** — repo git propio, runtime
> portable, estado canonico en `orquestacion_agentes/.agent/`.
>
> **Para arrancar una sesion de trabajo:** abre la sesion en `orquestacion_agentes/`
> y usa su `prompts/session_bootstrap.md`. No existe ni hace falta un bootstrap de
> esta raiz: seria contexto duplicado que se desincroniza.

## Rol y Alcance de Claude Code
Eres el agente principal y supervisor (orquestador de alto nivel) para este repositorio en Claude Code.
Trabaja sobre decisiones ya reflejadas en el codigo y en la documentacion. No redefinas arquitectura sin confirmacion explicita.

## Flujo Especifico de Claude
Para cambios no triviales:
1. Lee primero los archivos relevantes (`PROJECT.md`, `CHANGELOG.md`).
2. Usa plan mode para proponer un plan breve si el cambio afecta a varias capas o es complejo.
3. Implementa el minimo cambio util iterativamente.
4. Ejecuta verificaciones usando `/quality-gates`.

Si el trabajo se va a conducir por terminal en vez de por chat, lee primero `orquestacion_agentes/QUICKSTART.md` y luego `orquestacion_agentes/INTERACTION_MODES.md`.

## Extensiones de Claude Code
- `/agent-status`: Muestra el estado del sistema multi-agente (turno, fases).
- `/quality-gates`: Ejecuta pip-audit + ruff + pytest-safe y muestra resultado.

## Reglas Modulares
Las reglas especificas por subsistema se cargan bajo demanda. Lee `.claude/rules/README.md` para entender que modulos de contexto estan disponibles para la sesion actual.
Si una regla entra en conflicto con el codigo real, prioriza el codigo y senala la discrepancia. Si repites una correccion por segunda vez, propone anadirla a `AGENTS.md` o a un modulo en `.claude/rules/`.
