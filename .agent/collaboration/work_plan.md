# Work Ticket - WT-2026-236a

## Metadata
- **ID:** WT-2026-236a
- **Title:** Smoke repo-compare con Orca y SOUL.md para validar flujo externo
- **Scope:** system/research-devx
- **Priority:** Media
- **Estado:** APPROVED
- **deliverable_type:** documentation
- **Asignado a:** BUILDER
- **Depende de:** WT-2026-182, WT-2026-227a, WT-2026-235a

## Objetivo
Validar de punta a punta que el protocolo `repo-compare` sigue siendo operable en
la topologia `repo_motor` + `repo_destino`, usando `stablyai/orca` como repo target
y el post de `SOUL.md` como referencia secundaria de patrones de operador.

El resultado esperado no es adoptar codigo todavia, sino producir un reporte
evidence-linked que diga que oportunidades merecen ticket propio, que debe
ignorarse, y que partes del tooling externo fallan hoy.

## Contexto externo verificado
- `stablyai/orca`: IDE/orquestador para flotas de agentes CLI en worktrees
  paralelos. README publico declara soporte para Claude Code, Codex, OpenCode,
  Goose y otros agentes; features relevantes: worktree-native, terminales
  multi-agente, source control integrado, GitHub integration, SSH y companion
  mobile. Repo publico MIT, TypeScript dominante, con tests y CI visibles.
- Reddit `SOUL.md`: template de identidad operativa para agentes. La idea util no
  es copiar el texto, sino evaluar si el motor necesita un documento compacto de
  stance/autonomia/mision que no duplique `AGENTS.md`, memoria ni prompts.
- Intento MCP GitHub: `mcp__github.get_file_contents(stablyai/orca/README.md)`
  fallo con `Authentication Failed: Bad credentials`.
- Intento `gh` CLI: `gh repo view stablyai/orca ...` fallo porque `gh` no esta
  autenticado (`gh auth login` o `GH_TOKEN` requerido).
- Preflight local: falta `.agent/runtime/audit/AUDIT.md`; ademas este
  `repo_destino` no tiene `scripts/local_audit.py`, aunque la skill repo-compare
  lo espera como primer fallback.

## Problema
El protocolo `repo-compare` promete comparar un repositorio GitHub contra el
contexto local usando AUDIT.md, Repomix y MCP GitHub. En esta sesion ya aparecieron
tres fricciones reales: credenciales MCP invalidas, `gh` CLI sin auth y ausencia
del AUDIT.md local/fallback `local_audit.py` en el `repo_destino`.

Si estas fricciones no quedan explicitadas, el equipo puede creer que
repo-compare esta sano porque el analisis manual con navegador funciona. Este
ticket debe separar el valor de las ideas externas de la salud real del tooling
canonico.

## Contrato
- Ejecutar el protocolo repo-compare con estos pasos concretos: preflight de
  AUDIT.md, scoring 0-5, exploracion remota acotada, reporte persistido y validate
  final. No inventar evidencia si una herramienta falla.
- Si MCP GitHub o `gh` CLI no estan disponibles, documentar el fallo exacto y usar
  solo fuentes publicas como fallback diagnostico.
- No escribir `CREDITS.md`; solo emitir candidate row si hay oportunidad `AHORA`
  o `DESPUES`.
- No copiar texto largo de Reddit ni incorporar SOUL.md como archivo operativo.
  Tratarlo como patron conceptual y revisar privacidad/token budget.
- No introducir dependencias nuevas ni instalar tooling externo sin aprobacion.

## Decision Arquitectonica
El ticket trata `repo-compare` como protocolo observable, no como simple informe
manual. Por eso el reporte debe conservar dos canales separados: oportunidades de
producto inspiradas por Orca/SOUL.md y diagnostico del tooling que deberia haber
soportado la comparacion (`AUDIT.md`, Repomix, MCP GitHub y `gh` CLI).

Esta separacion evita un falso verde: si el navegador publico permite investigar,
eso solo demuestra que existe un fallback humano, no que la ruta canonica este
sana para agentes.

## Non-goals
- No portar codigo de Orca ni crear integraciones Electron/TypeScript.
- No crear un `SOUL.md` operativo ni reescribir `AGENTS.md`.
- No corregir autenticacion MCP/`gh` ni ejecutar `gh auth login`.
- No instalar Repomix, clonar repos remotos ni anadir dependencias.
- No tocar `CREDITS.md`; solo proponer candidate row si procede.

## Fases

### Fase 0 - Preflight canonico
- Verificar `repo_motor`, `repo_destino`, ticket activo y estado del bus.
- Comprobar existencia/frescura de `.agent/runtime/audit/AUDIT.md`.
- Si falta AUDIT.md, buscar fallback local equivalente (`scripts/audit_codebase.py`
  o script del motor) y documentar si el contrato de repo-compare esta roto.
- Registrar estado de MCP GitHub, `gh auth status`, Repomix y acceso web fallback.

### Fase 1 - Filtro rapido Orca
- Aplicar scoring repo-compare 0-5:
  README claro, tests/CI, mantenimiento, encaje tecnico, claridad estructural.
- Usar evidencia publica ya verificada y, si el acceso GitHub queda reparado,
  preferir MCP/`gh` para SHA, LICENSE, workflows y estructura.
- Si score < 3, cerrar como bajo valor con razon. Si score >= 3, continuar.

### Fase 2 - Exploracion acotada
- Leer maximo 8-12 superficies remotas:
  README, AGENTS.md, package.json, orca.yaml, docs relevantes, CLI, tests,
  workflows y superficies de worktree/source-control si se localizan.
- Para SOUL.md, extraer solo patrones: stance, autonomia, accountability,
  mission map, delegation rules, lookup protocol, escalation.
- Comparar contra capacidades locales citando rutas del `repo_motor` o AUDIT.md
  cuando exista.

### Fase 3 - Reporte persistido
- Crear reporte en `.agent/runtime/compare/stablyai-orca-HEAD-2026-06-07.md`
  o con SHA real si se obtiene.
- Incluir oportunidades con la plantilla repo-compare:
  fuente verificada, valor, si ya existe, dependencias, encaje, plan y decision.
  Objetivo: minimo 3 y maximo 5; si hay menos de 3, justificar cada descarte.
- Incluir matriz final, "Que Ignorar", "Accion Inmediata" y bloque candidato
  `CREDITS.md` solo si procede.

### Fase 4 - Diagnostico del protocolo
- Separar hallazgos de producto de hallazgos de tooling.
- Si el bloqueo principal es autenticacion/ausencia AUDIT.md, proponer follow-up
  concreto en backlog sin arreglarlo dentro de este ticket salvo que sea un cambio
  documental minimo.

## Files Likely Touched

### repo_destino - Builder
- `.agent/runtime/compare/stablyai-orca-HEAD-2026-06-07.md`
- `.agent/collaboration/execution_log.md`

### repo_destino - Manager only
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WT-2026-236a.md`
- `.agent/collaboration/AUDIT_WT-2026-236a.md`
- `.agent/collaboration/backlog.md`
- `.agent/collaboration/STATE.md`
- `.agent/collaboration/TURN.md`

### repo_motor - Read/inspect only by default
- `skills/repo-compare/SKILL.md`
- `skills/repo-compare/references/output-format.md`
- `skills/repo-compare/references/filter-criteria.md`
- `prompts/audit_plan.md`
- `.agent/agent_controller.py`
- `scripts/local_audit.py` or equivalent, if present

## Superficies prohibidas para Builder
- No modificar codigo productivo del `repo_motor` en este ticket.
- No tocar `CREDITS.md`; emitir solo bloque candidato.
- No tocar `privada/`.
- No instalar paquetes ni ejecutar `gh auth login`.
- No escribir memoria persistente sin propuesta humana explicita.

## Criterios de aceptacion
- El reporte repo-compare queda persistido en `.agent/runtime/compare/`.
- El reporte indica el estado de AUDIT.md, MCP GitHub, `gh` CLI y Repomix.
- Orca recibe scoring 0-5 con evidencia verificable.
- Se documentan 3-5 oportunidades o, si no hay suficientes, se explica por que.
- SOUL.md se evalua como patron conceptual, sin copiar plantilla extensa ni
  introducir secretos/rutas privadas.
- Hay seccion explicita "Que Ignorar".
- Hay accion inmediata recomendada: adoptar, abrir follow-up, o no invertir mas.
- Si hay oportunidad `AHORA`/`DESPUES`, el reporte incluye candidate row para
  `CREDITS.md`.
- `agent_controller.py --validate --json --project-root <repo_destino>` pasa o
  deja blocker exacto documentado.

## TP Check
TP-01: `repo-compare` no se considera sano si AUDIT.md falta y no hay fallback.
TP-02: fallos MCP/`gh` quedan registrados como diagnostico, no ocultos por web.
TP-03: cada oportunidad cita fuente externa y estado local.
TP-04: no se propone portar UI/Electron/Node de Orca al motor Python sin justificar
  esfuerzo/deps.
TP-05: SOUL.md no duplica AGENTS.md/memoria; se reduce a patrones accionables.
TP-06: no se escribe `CREDITS.md` ni memoria.
TP-07: cierre con validate o blocker verificable.
