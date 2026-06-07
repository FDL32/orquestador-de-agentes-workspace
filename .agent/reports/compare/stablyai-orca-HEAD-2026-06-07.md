# Repo Compare: stablyai/orca vs orquestador_de_agentes

**Fecha:** 2026-06-07
**Repo target:** https://github.com/stablyai/orca
**SHA target:** `9c92e3d47b3ccb3d8300f9dc59b63716bed22712` (obtenido via GitHub API publica; commit del 2026-06-07T16:59:55Z)
**AUDIT.md:** [AUSENTE] â€” `.agent/runtime/audit/AUDIT.md` no existe en este `repo_destino`. No se pudo regenerar porque `scripts/local_audit.py` no esta instalado en el destino. Fallback local: `scripts/audit_codebase.py` existe pero requiere `deadcode` y `vulture` â€” no genera el snapshot `AUDIT.md` requerido por repo-compare.
**Archivos leidos:** 10 (max 12) â€” README.md, AGENTS.md, package.json, LICENSE, .github/workflows/ (11 workflows listados), git tree via API, commit SHA via API
**Superficies remotas consultadas:**
  - README.md (via GitHub raw y web)
  - AGENTS.md (via GitHub raw)
  - package.json (via GitHub raw)
  - LICENSE (via GitHub raw â€” MIT)
  - .github/workflows/ (via GitHub API â€” 11 workflows)
  - Full git tree (via GitHub API â€” estructura completa)
  - Commit HEAD (via GitHub API â€” SHA, author, fecha)
  - Reddit SOUL.md (post de patron conceptual â€” via web)
**Oportunidades detectadas:** 4 (3-5 target)
**Fuente del acceso remoto:** GitHub API publica (web fallback). MCP GitHub: `Authentication Failed`. `gh` CLI: no autenticado.

---

## Nota sobre el contexto local

Este reporte se genera SIN AUDIT.md. El contrato repo-compare exige AUDIT.md como
Fase 0 autoritativa; su ausencia implica que toda comparacion contra "lo que ya
existe" usa inspeccion manual de directorios y archivos del repo_motor, no un
snapshot verificable. Marcar cada oportunidad con el nivel de evidencia real.

---

## Filtro rapido: Score 4/5 âœ…

| Dimension | Puntos | Justificacion |
|-----------|--------|---------------|
| README claro | 1 | README explica proposito, instalacion, 12+ features con GIFs. "The AI Orchestrator for 100x builders" â€” claro en < 3 frases. |
| Tests/CI | 1 | `tests/` con e2e (Playwright) y unit (vitest). 11 workflows CI: e2e, pr, release-cut, mobile, homebrew, etc. |
| Mantenimiento | 1 | Ultimo commit: 2026-06-07 (hoy). Version 1.4.51-rc.4. Issues con templates. Releases activos. |
| Encaje tecnico | 0 | TypeScript/Electron (Node 24, pnpm). Motor es Python 3.10+. Portar codigo directo no es viable. Los patrones de orquestacion, worktrees, source-control review y SSH si son evaluables como inspiracion arquitectonica. |
| Claridad estructural | 1 | Directorios claros: `src/`, `config/`, `docs/`, `tests/`, `.github/`. Naming consistente. `AGENTS.md` propio con reglas compactas. |

**Total:** 4/5 â†’ Continuar a Fase 2 (exploracion)

---

## OPORTUNIDAD #1: Worktree-native agent orchestration (tablero de flota)

**Ubicacion en repo target:** README + `docs/` (feature-wall/parallel-worktrees.gif, orca CLI)
**Fuente:** GitHub: stablyai/orca README + git tree docs/

**Que hace?**
Orca ejecuta multiples agentes CLI (Claude Code, Codex, OpenCode, Goose, etc.) lado a
lado, cada uno en su propio git worktree aislado. Muestra estado activo por agente en
tabs/paneles. Permite cambiar de contexto instantaneamente sin stashing ni branch
juggling.

**Que valor aporta al motor?**
El motor actual orquesta agentes secuencialmente via `scripts/orquestador.py` y
tickets secuenciales. Un tablero de flota multi-agente paralelo con worktrees
aislados permitiria:
- Comparar resultados de diferentes agentes en el mismo problema
- Ejecutar reviews paralelas
- Aislar riesgos por worktree (un agente no contamina el trabajo de otro)
- Escalar a N agentes sin colision de estado

**Ya existe en local?**
- **Estado:** Parcial
- **Evidencia (sin AUDIT.md, por inspeccion manual):**
  - `scripts/orquestador.py` en repo_motor: orquesta agentes pero secuencial, no paralelo.
  - `skills/repo-compare/` y `skills/test-driven-development/`: skills individuales, no
    hay un panel de flota ni worktree manager.
  - `bus/event_bus.py` en repo_motor: podria servir como base para eventos de estado
    de agentes, pero no hay consumidor de "flota".
  - No existe mecanismo de worktree nativo en el motor.

**Dependencias nuevas:**
- [x] Ninguna (patron arquitectonico, no codigo portado)
- [ ] `lib1`, `lib2`
- [ ] Requiere `uv add <lib>`

**Encaje tecnico:**
- **Python:** 3.10+ â€” compatible
- **Arquitectura:** Medio â€” el bus de eventos existe pero no hay concepto de "sesion de agente paralela"
- **Deps:** Ligeras â€” stdlib (`subprocess`, `pathlib`) + `git` CLI para worktrees

**Plan de incorporacion:**
1. Disenar contrato de "sesion de agente" con worktree, estado, cola de eventos
2. Implementar lanzador paralelo con aislamiento de directorio (worktrees git o tempdirs)
3. Integrar con bus de eventos existente
4. Anadir skill de "flota" o extension de orquestador

**Dificultad estimada:** L (>4h)
- **Razon:** Cambio arquitectonico: requiere disenar contrato de sesion paralela,
  integracion con bus, manejo de errores en paralelo y limpieza de worktrees.

**Prioridad:** Media
- **Razon:** Alto valor para escalar capacidad de orquestacion, pero esfuerzo grande.
  No urgente porque el flujo secuencial actual cubre el caso basico.

**Decision:** INCORPORAR DESPUES
- **Razon:** El patron es valioso pero requiere diseno arquitectonico. Mejor como
  follow-up con prototipo primero.

---

## OPORTUNIDAD #2: Reglas AGENTS.md compactas y prescriptivas

**Ubicacion en repo target:** `AGENTS.md` (raiz, 3824 bytes, ~90 lineas)
**Lineas clave:**
```markdown
## Worktree Safety
Always use the primary working directory (the worktree) for all file reads and edits.
Never follow absolute paths from subagent results that point to the main repo.

## Cross-Platform Support
Orca targets macOS, Linux, and Windows. Keep all platform-dependent behavior behind runtime checks.

## SSH Use Case
All changes must consider the SSH use case. Don't assume local-only execution.

## Git Provider Compatibility
Source-control and review changes must consider GitLab and other supported git providers...
```
**Fuente:** GitHub: stablyai/orca/AGENTS.md (raw)

**Que hace?**
Define ~12 reglas operativas cortas (1-3 parrafos cada una) sobre: design system, code
comments, lint rules, naming, worktree safety, cross-platform, SSH, git provider
compatibility, GitHub CLI, type declarations. Son prescriptivas, no descriptivas.

**Que valor aporta al motor?**
El motor tiene `AGENTS.md` general que describe el sistema, no reglas para agentes que
trabajan EN el motor. Una seccion compacta de "reglas de operacion" similar permitiria:
- Que agentes terceros (Goose, Codex) sigan las mismas reglas que Claude Code
- Reducir "sorpresas" cross-platform
- Forzar consideraciones de SSH/remoto desde el diseno
- Estandarizar naming y estructura

**Ya existe en local?**
- **Estado:** No (como formato compacto de reglas)
- **Evidencia (sin AUDIT.md):**
  - `AGENTS.md` del repo_destino (leido): es documentacion general/operacional, no
    conjunto de reglas prescriptivas.
  - `.agent/rules/` en repo_motor: contiene reglas de ingenieria sostenible y
    formato, pero no cubre worktree safety, SSH, cross-platform.
  - No hay equivalente a "Worktree Safety" o "SSH Use Case" en el motor.

**Dependencias nuevas:**
- [x] Ninguna

**Encaje tecnico:**
- **Python:** N/A (es Markdown)
- **Arquitectura:** Alto â€” solo requiere agregar/reorganizar secciones en `AGENTS.md`
- **Deps:** Ligeras

**Plan de incorporacion:**
1. Extraer reglas aplicables: worktree safety, cross-platform, SSH, provider compat
2. Adaptar lenguaje al contexto del motor Python
3. Agregar como seccion nueva en `AGENTS.md` o como archivo separado
4. Revisar que no duplique `.agent/rules/` ni memoria L2

**Dificultad estimada:** S (â‰¤1h)
- **Razon:** Solo editar Markdown, sin codigo nuevo.

**Prioridad:** Alta
- **Razon:** Bajo esfuerzo, impacto medio-alto en calidad de contribuciones de agentes.

**Decision:** INCORPORAR AHORA
- **Razon:** Bajo esfuerzo, impacto inmediato en consistencia de agentes que trabajan
  en el motor. Se puede hacer como ticket documental separado.

---

## OPORTUNIDAD #3: Source-control integrado con revision de diffs AI

**Ubicacion en repo target:** README (Built-in source control) + `docs/review/annotate-ai-diff`
**Fuente:** GitHub: stablyai/orca README

**Que hace?**
Permite revisar, anotar y commitear diffs generados por IA sin salir de Orca.
Integra PRs, issues y Actions checks vinculados a cada worktree automaticamente.

**Que valor aporta al motor?**
El motor actual usa `git` CLI directamente y flujo manual de PR. Una integracion
source-control que automaticamente:
- Cree ramas por ticket
- Asocie PRs a worktrees
- Valide que los diffs AI no toquen archivos prohibidos
- Genere resumen de cambios por agente

**Ya existe en local?**
- **Estado:** No (como flujo integrado)
- **Evidencia (sin AUDIT.md):**
  - `scripts/orquestador.py`: usa git pero no tiene integracion PR/worktree.
  - `skills/test-driven-development/`: asume git pero no automatiza ramas/PRs.
  - No existe "review de diff AI" como skill.

**Dependencias nuevas:**
- [x] Ninguna (patron de flujo, no codigo portado)
- [ ] Requiere `gh` CLI, pero ya es dependencia opcional del motor

**Encaje tecnico:**
- **Python:** 3.10+ â€” compatible
- **Arquitectura:** Medio â€” requiere nuevas abstracciones (BranchContext, DiffReview)
- **Deps:** Ligeras â€” `subprocess` + `gh` CLI existente

**Plan de incorporacion:**
1. Disenar skill `git-workflow` que automatice ramaâ†’ticketâ†’PR
2. Implementar helper de diff-review que marque archivos fuera de alcance
3. Integrar con `--mark-ready` para crear PRs automaticos
4. Anadir a quality gates: verificar que diff solo toca Files Likely Touched

**Dificultad estimada:** M (1-4h)
- **Razon:** Logica de flujo git mas validacion de alcance; requiere pruebas.

**Prioridad:** Media
- **Razon:** Mejora la automatizacion pero el flujo manual actual funciona.

**Decision:** INCORPORAR DESPUES
- **Razon:** Valor claro pero no bloqueante. Mejor como follow-up despues de
  estabilizar el flujo secuencial actual.

---

## OPORTUNIDAD #4: Patron SOUL.md â€” perfil operativo compacto de agente

**Ubicacion en repo target:** Reddit post (patron conceptual, no archivo operativo en Orca)
**Fuente:** Reddit (web publica â€” post individual)

**Que hace?**
Define un documento compacto de identidad operativa para agentes: stance (como
interactua con el usuario), autonomia (que puede decidir solo), mision (prioridades de
alto nivel), accountability (como reporta errores), delegation rules (que puede delegar
y a quien), lookup protocol (como buscar informacion), escalation (cuando y como escalar).

**Que valor aporta al motor?**
El motor actual tiene:
- `AGENTS.md` â€” documentacion operativa del sistema
- `.agent/rules/` â€” reglas de ingenieria
- Memoria L2 (`memory_rules.md`) â€” reglas de dominio
- Prompts â€” instrucciones de sesion

Un perfil SOUL.md compacto (< 50 lineas) podria complementar sin duplicar:
- Dar a CADA agente (no solo al Builder actual) un stance consistente
- Reducir tokens de prompt porque ya no haria falta repetir "como comportarse"
- Ser portable entre agentes (Claude Code, Codex, Goose, OpenCode)

**Ya existe en local?**
- **Estado:** No (como documento compacto de stance)
- **Evidencia (sin AUDIT.md):**
  - `AGENTS.md` del repo_motor: describe el sistema, no la identidad del agente.
  - `.agent/rules/common/sustainable_engineering.md`: reglas tecnicas, no stance.
  - Memoria L3 (`memory_profile.md`): perfil del proyecto, no del agente.
  - No existe "perfil de agente" en el motor.

**Riesgos:**
- Riesgo ALTO de duplicar AGENTS.md si no se disena con cuidado
- Token budget: debe ser < 50 lineas / < 3KB para que valga la pena
- Podria confundir a agentes que ya reciben instrucciones via prompt

**Dependencias nuevas:**
- [x] Ninguna (es documento, no codigo)

**Encaje tecnico:**
- **Python:** N/A (documento)
- **Arquitectura:** Alto â€” solo crear/linker un archivo markdown
- **Deps:** Ligeras

**Plan de incorporacion (si se decide adoptar):**
1. Redactar borrador de < 50 lineas con stance/autonomia/mision/accountability
2. Verificar que no duplica AGENTS.md, memoria L2 ni prompts existentes
3. Colocar en `.agent/runtime/identity/` o raiz del motor
4. Referenciar desde `session_bootstrap.md` y memoria L3
5. Probar con 3 agentes distintos (Claude Code, Codex, Goose) que el stance es
   consistente

**Dificultad estimada:** S (â‰¤1h)
- **Razon:** Solo redaccion y validacion de no-duplicacion.

**Prioridad:** Baja
- **Razon:** Valor especulativo hasta que se pruebe con multiples agentes. Riesgo de
  duplicacion con AGENTS.md.

**Decision:** IGNORAR (por ahora)
- **Razon:** El concepto es interesante pero el motor no tiene suficiente diversidad de
  agentes como para justificar un perfil separado. AGENTS.md + memoria L3 cubren el
  caso actual. Revisar cuando se integre un tercer tipo de agente.

---

## Matriz Final

| Oportunidad | Impacto (1-10) | Esfuerzo (h) | Encaje (%) | Decision |
|-------------|----------------|--------------|------------|----------|
| #1: Worktree-native orchestration | 8 | >4h | 60% | DESPUES |
| #2: Reglas AGENTS compactas | 6 | â‰¤1h | 90% | AHORA |
| #3: Source-control integrado | 7 | 1-4h | 70% | DESPUES |
| #4: Patron SOUL.md | 4 | â‰¤1h | 85% | IGNORAR |

---

## Que Ignorar

- **Interfaz grafica Electron/React**: Todo el frontend de Orca (terminales visuales,
  paneles, tabs, drag-and-drop, markdown preview, design mode, file explorer). El motor
  es Python CLI-first. Portar UI Electron a Python no tiene sentido. Si se necesita
  visualizacion, mejor como web dashboard ligero con `rich` o `textual`.
  - **Ubicacion:** `src/renderer/`, `src/main/`
  - **Por que ignorar:** Stack completamente diferente (React/Electron/Node vs Python CLI)

- **Mobile companion app (iOS/Android)**: Requiere desarrollo nativo, push notifications,
  App Store distribution. No es viable para un motor Python open-source sin equipo
  movil dedicado.
  - **Ubicacion:** `docs/assets/feature-wall/mobile-companion-app-showcase.gif`
  - **Por que ignorar:** Esfuerzo desproporcionado para el valor actual del motor.

- **Real-time terminal rendering (xterm.js, node-pty)**: Orca usa un terminal embebido
  de alta fidelidad. El motor actual invoca subprocesos y captura stdout. No hay
  necesidad de emulacion de terminal en tiempo real.
  - **Ubicacion:** package.json (`@xterm/*`, `node-pty`)
  - **Por que ignorar:** Overkill para un motor de orquestacion que no necesita
    presentar terminales interactivas.

- **Account switcher y usage tracking (PostHog)**: Orca permite cambiar cuentas de
  agente (Claude Code, Codex) y trackear uso. El motor no maneja cuentas de agentes
  externos â€” cada agente tiene su propia autenticacion.
  - **Ubicacion:** package.json (`posthog-node`), docs/ `codex-accounts.gif`
  - **Por que ignorar:** No aplica al modelo de orquestacion del motor.

- **Componentes UI especificos (shadcn, radix, dnd-kit, monaco-editor, tiptap)**: Todo
  el ecosistema React de Orca para edicion de texto, markdown, tablas, drag-and-drop.
  No es portable a Python.
  - **Ubicacion:** package.json devDependencies
  - **Por que ignorar:** Stack UI no portable.

---

## Diagnostico del Protocolo repo-compare

### Estado del tooling canonico

| Herramienta | Estado | Detalle |
|-------------|--------|---------|
| **AUDIT.md** | AUSENTE | `.agent/runtime/audit/AUDIT.md` no existe. `scripts/local_audit.py` no esta instalado en repo_destino. `scripts/audit_codebase.py` existe pero no genera AUDIT.md (genera `.session/audit_report.md` con analisis de deadcode, no snapshot de capacidades). El contrato repo-compare requiere AUDIT.md como Fase 0 â€” esta roto. |
| **MCP GitHub** | FALLA | `mcp__github__get_file_contents(stablyai/orca/README.md)` devolvio `Authentication Failed: Bad credentials`. Las credenciales MCP no estan configuradas o expiraron. |
| **gh CLI** | FALLA | `gh repo view stablyai/orca` falla porque `gh` no esta autenticado. Se requiere `gh auth login` o `GH_TOKEN`. |
| **Repomix** | NO VERIFICADO | No se intento ejecutar `npx repomix` porque: (a) no hay AUDIT.md que comprimir, (b) el ticket prohibe instalar tooling nuevo, (c) no hay repos remotos clonados. |
| **Fallback web publico** | FUNCIONA PARCIALMENTE | GitHub API publica (no autenticada) permite leer README, AGENTS.md, package.json, LICENSE, tree, commits, workflows. Reddit web permite leer post SOUL.md. NO permite: search code, list PRs/issues privados, leer archivos > 1MB via raw. |

### Fuente real de datos para este reporte

Este reporte se construyo usando:
1. **GitHub API publica** (REST, no autenticada): README, AGENTS.md, package.json,
   LICENSE, git tree, commits, workflows
2. **GitHub raw content**: README.md, AGENTS.md, package.json, LICENSE
3. **Reddit web**: post SOUL.md (patron conceptual)

**Ninguna fuente fue MCP GitHub, gh CLI, AUDIT.md ni Repomix.**

### Hallazgos clave del protocolo

1. **El contrato repo-compare requiere AUDIT.md, pero no hay generador canonico en el destino.**
   - `scripts/local_audit.py` del motor produce AUDIT.md, pero no esta instalado en el destino.
   - `scripts/audit_codebase.py` del destino hace analisis de deadcode/ruff, no snapshot de capacidades.
   - **Follow-up necesario:** Instalar `scripts/local_audit.py` via sync, o adaptar `audit_codebase.py`.
2. **MCP GitHub y gh CLI son los dos unicos caminos para search code.**
   - La API publica sin autenticar solo permite leer archivos individuales si se conoce la ruta exacta.
   - Sin search code, no se puede encontrar "funcionalidades similares" en el repo target.
3. **Web fallback no es sustituto de MCP/gh.**
   - Permite leer archivos conocidos pero no descubrir patrones no evidentes.
   - El reporte se beneficio de la API REST publica que no requirio autenticacion,
     pero esto no esta en el contrato de repo-compare.
4. **Repomix no se evaluo pero no habria sido util sin AUDIT.md.**
   - Repomix comprime el contexto local contra el qual comparar; sin AUDIT.md, no hay
     baseline autoritativo.

---

## Accion Inmediata

**Proximo paso:** Abrir ticket documental para incorporar reglas operativas compactas
tipo Orca en `AGENTS.md` del motor (OPORTUNIDAD #2).

**Recomendacion de follow-ups:**
1. **WT-2026-XXX** (ALTA prioridad): Agregar seccion de reglas operativas a `AGENTS.md`
   inspirada en Orca: worktree safety, cross-platform, SSH, git provider compatibility.
   Esfuerzo: â‰¤1h.
2. **WT-2026-XXX** (MEDIA prioridad): Instalar `scripts/local_audit.py` en repo_destino
   para que el flujo repo-compare funcione con AUDIT.md.
3. **WT-2026-XXX** (MEDIA prioridad): Evaluar diseno de skill de orquestacion paralela
   con worktrees (OPORTUNIDAD #1). Requiere diseno arquitectonico primero.
4. **WT-2026-XXX** (BAJA prioridad): Reparar autenticacion MCP GitHub o gh CLI para
   que repo-compare pueda hacer search code en futuros compares.

**Comando sugerido:**
```bash
python scripts/ticket_supervisor.py --create --title "Agregar reglas operativas AGENTS.md inspiradas en Orca" --priority alta --type documentation
```

**Criterio de aceptacion:**
- [ ] `AGENTS.md` tiene seccion "Reglas Operativas" con minimo: worktree safety,
      cross-platform, SSH, git provider compatibility
- [ ] No duplica `.agent/rules/` ni memoria existente
- [ ] `python .agent/agent_controller.py --validate --json` PASS

---

## Credits â€” Candidate row for `CREDITS.md`

Si decides adoptar la OPORTUNIDAD #2 (reglas AGENTS.md compactas), anade esta fila a `CREDITS.md`:

| WP | Source | Pattern | License | Adapted vs Ported |
|----|--------|---------|---------|-------------------|
| WT-2026-XXX (TBD) | [stablyai/orca@9c92e3d](https://github.com/stablyai/orca/tree/9c92e3d47b3ccb3d8300f9dc59b63716bed22712) | AGENTS.md compact-prescriptive rules | MIT, [verify] | Inspiration |

**Notas:**
- `WP`: rellenar al abrir el ticket que adopta la oportunidad #2.
- `License`: Orca LICENSE es MIT. Verificar que el archivo actual sigue siendo MIT.
- `Adapted vs Ported`: Inspiration â€” el patron de tener reglas prescriptivas compactas
  se toma como inspiracion, no se copia texto de Orca.

---

*Reporte generado por Builder para WT-2026-236a. Fuentes: GitHub API publica + web fallback. AUDIT.md ausente â€” evidencia por inspeccion manual de directorios del repo_motor.*
