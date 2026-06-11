# PROJECT.md - Project Manifest

Este archivo define el contrato canonico del `repo_destino` de dogfooding para
`orquestador_de_agentes`. El motor lo usa como referencia de prefijo de
tickets, stack y reglas locales.

## Identidad del Proyecto

- **Nombre:** `orquestador_de_agentes_workspace`
- **Proposito:** repo destino de dogfooding para validar en ciclo real el
  motor `orquestador_de_agentes`, sus tickets, su bus y su protocolo de
  cierre multiagente.
Ticket prefix: WOT

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

## Sistema de Tickets

- Todo plan nuevo arranca con un ticket base terminado en `a`.
- No existe plan canonico sin ticket `...a`; ese ticket fija el objetivo base y
  el primer cierre esperado del ciclo.
- Los tickets `...b`, `...c`, `...d` y siguientes se usan para:
  - dividir planes largos en entregas mas pequenas;
  - formalizar fixes surgidos despues de cerrar un `...a`;
  - absorber hardening o follow-ups detectados en auditoria.
- Cuando un ticket `...a` descubre problemas estructurales del bus o del
  launcher, el `...a` se cierra primero de forma limpia y los arreglos salen a
  tickets derivados, sin mezclar commits de investigacion y remediacion.

## Regla de Recovery del Bus

- Si el Builder lanzado por shell no lleva el bus a cierre canonico, la
  prioridad no es "forzar el cierre", sino analizar la causa raiz para que no
  se repita.
- El flujo recomendado es:
  1. diagnosticar por que el bus no llego a termino;
  2. cerrar por chat el ticket `...a` correspondiente para no ensuciar commits;
  3. abrir tickets `...b`, `...c`, `...d` con los fixes concretos;
  4. implementar esos fixes por chat, no a traves del propio bus averiado.
- Regla operativa explicita: no arreglar el bus "a traves del bus" salvo que el
  propio ticket trate exactamente del mecanismo de recovery y la evidencia lo
  justifique.

## Politica de Cierre y Review

### Gate de cierre: `validate --json`

El unico gate de cierre operativo es `validate --json` del `repo_motor`. Un
ticket se considera `APROBADO` solo cuando `validate --json` produce `0 errors`
y `0 warnings estructurales`.

La secuencia correcta de endurecimiento es:

1. **Allowlist** — documentar en el ticket que warnings especificos son no
   bloqueantes (advisories externos, warnings no estructurales).
2. **Gate** — una vez acordada la allowlist, el gate exige
   `0 warnings estructurales` sin excepcion.

Los warnings documentados en la allowlist se consideran `NITS` (ver seccion
siguiente). Cualquier otro warning estructural es bloqueante.

### BLOCKERS vs NITS

| Categoria | Criterio | Ejemplos |
|-----------|----------|----------|
| **BLOCKER** | Impide el cierre. Requiere correccion o justificacion trazable antes de aprobar. | Errores en `validate --json`; tests que no pasan; bugfix sin evidencia suficiente del bug o sin etiqueta `[NON-REVERSE-CLASSICAL: ...]`; `scope creep`; evidencia insuficiente del cambio productivo. |
| **NIT** | No bloquea el cierre. Se documenta pero no detiene la aprobacion. | Legibilidad; refactors no necesarios; estilo o claridad que no rompe gates; warnings documentados en la allowlist del ticket. |

### Criterio de mergeabilidad

Ademas del gate tecnico, el revisor evalua:

- **Scope discipline:** el diff respeta `Files Likely Touched` y `non-goals`
  declarados en el plan. Cualquier archivo fuera de esa lista requiere
  justificacion explicita.
- **Code quality / conventions:** el codigo nuevo sigue los patrones existentes
  del codebase. Si introduce un patron nuevo, debe justificarlo en el plan o en
  un comentario en el codigo.

Estos criterios no son un gate autonomo, sino la formalizacion de practicas que
ya existen en el flujo de trabajo actual.

## CHANGELOG.md

Companero de este manifiesto. Registra decisiones arquitectonicas, cierres de
sesion y handoffs documentales del `repo_destino`. Mantenlo actualizado junto
con `PROJECT.md`.
