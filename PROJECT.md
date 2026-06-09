# PROJECT.md - Project Manifest

Este archivo define el contrato canonico del `repo_destino` de dogfooding para
`orquestador_de_agentes`. El motor lo usa como referencia de prefijo de
tickets, stack y reglas locales.

## Identidad del Proyecto

- **Nombre:** `orquestador_de_agentes_workspace`
- **Proposito:** repo destino de dogfooding para validar en ciclo real el
  motor `orquestador_de_agentes`, sus tickets, su bus y su protocolo de
  cierre multiagente.
Ticket prefix: WT

## Stack Tecnologico

- **Runtime:** Python 3.10+
- **Package manager:** `uv`
- **Testing:** `pytest`
- **Linter:** `ruff`

## Rutas Criticas

- `scripts/` - utilidades locales del `repo_destino` y runners seguros
- `tests/` - suite local y regresiones del workspace
- `.agent/` - collaboration, runtime, memoria y estado operativo local

## Reglas y Non-Goals

- Las operaciones git de tooling se validan contra `repo_motor`, pero el estado
  operativo canonico vive en este `repo_destino`.
- No mezclar cambios de `repo_motor` con cierres documentales del
  `repo_destino`; cada repo se empaqueta y valida por separado.

## CHANGELOG.md

Companero de este manifiesto. Registra decisiones arquitectonicas, cierres de
sesion y handoffs documentales del `repo_destino`. Mantenlo actualizado junto
con `PROJECT.md`.
