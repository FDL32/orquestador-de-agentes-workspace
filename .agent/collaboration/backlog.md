# Backlog

> Tickets candidatos y planes futuros del workspace.
> No es estado activo: el ticket activo vive en `work_plan.md`.
> Al arrancar un item, se convierte en `work_plan.md`; al cerrarlo, pasa a `CHANGELOG.md`.
> Historico de tickets completados/absortos: ver `CHANGELOG.md` del motor.

## Politica
- **Workspace (dogfooding):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -- repo destino real.
- **Motor (fuente canonica):** `C:\Users\fdl\Proyectos_Python\orquestador_de_agentes` -- repo portable con `.git` propio.
- **Contrato:** mejoras globales se portan explicitamente al motor; nunca se asume sincronizacion implicita.
- **Escritura:** humano o Manager; Builder solo lo toca si el plan lo pide explicitamente.
- **Destino:** cada proyecto destino tendra su propio `.agent/collaboration/backlog.md`.

## Vista rapida

| Prioridad | Ticket | Titulo | Scope | Estado | Depende de | Origen |
|-----------|--------|--------|-------|--------|------------|--------|
| Media | WT-2026-250c | Poda documental de backlog y saneo de mojibake en superficies vivas | system/collab-hygiene | active | - | session-2026-06-11-system-audit |
| Alta | WT-2026-251b | Migrar el dogfooding al prefijo WOT como validacion viva | system/ticket-prefix-portability | done | WT-2026-251a, WT-2026-250a | session-2026-06-11-system-audit |  <!-- verificado: absorbido: backfill 9d97df7 + pipeline canonico 961f210 -->
| Alta | WT-2026-252a | Decision-artifact estructurado del Manager con fallback a parser NDJSON | system/review-decision-contract | done | WT-2026-248b | session-2026-06-11-system-audit |  <!-- verificado: 2dda386 + 886652b (decision artifact canal primario) -->
| Media | WT-2026-253a | Reescribir skill code-audit sobre CLIs directas | system/skills-product | done | - | session-2026-06-11-system-audit |  <!-- verificado: 02fdf81 -->
| Media | WT-2026-253b | Des-localizar repo-compare y graphify del entorno del autor | system/skills-product | done | - | session-2026-06-11-system-audit |  <!-- verificado: d19ff6b -->
| Media | WT-2026-253c | local_audit veraz y AUDIT.md autogenerado en el launcher | system/bootstrap-observability | done | - | session-2026-06-11-system-audit |  <!-- verificado: bd3f3a0 -->
| Media | WT-2026-254a | Deprecacion formal Goose/Claw fase 1 (docs y tests) | system/legacy-deprecation | done | - | session-2026-06-11-system-audit |  <!-- verificado: 3f6aad3 -->
| Media | WT-2026-254b | Regenerar .claude/rules del destino desde el estado real | system/docs-coherence | done | WT-2026-254a | session-2026-06-11-system-audit |  <!-- verificado: 3f6aad3 -->
| Media | WT-2026-255a | Extraer parser de decisiones de review_bridge a modulo propio | system/seam-extraction | done | WT-2026-252a | session-2026-06-11-system-audit |  <!-- verificado: 2dda386 + 886652b (decision artifact canal primario) -->
| Baja | WT-2026-256a | Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2 | system/security-dependencies | blocked-external | - | session-2026-06-11-security-followup |  <!-- 2026-06-12: uv sigue resolviendo pip<=26.1.1; excepcion legitima -->

## Completados en sesion 2026-06-11 (audit integral)

| Ticket | Titulo | Commit(s) |
|--------|--------|-----------|
| WT-2026-248b | Alinear prompts wrapper y skills canonicas | 568f6a0 |
| WT-2026-249c | Review bridge: normalizar parseo de CHANGES | repo_motor |
| WT-2026-250a | Archivador reconoce sufijos de letra | d6d4461 |
| WT-2026-250b | Rotacion review_queue y split feedback digest/raw | 89ee4ac |
| WT-2026-250d | manager-approve resuelve repo git correcto | 31336f1 |
| WT-2026-251a | Centralizar ticket-ID regex + prefijos 2-3 letras | edbad61 |

> Nota: para historial previo ver `CHANGELOG.md` del motor (git conserva todo).

## WOT-2026-001x - Resolucion formal en closeout 2026-06-12

| Ticket | Estado | Resolucion formal |
|--------|--------|-------------------|
| WOT-2026-001a | absorbed | Absorbido por el endurecimiento ya entregado en pipeline + prompt (`WT-2026-248b` y contrato canonico derivado). |
| WOT-2026-001b | completed | Cerrado documentalmente en este closeout: el patron Manager -> Builder por chat queda validado y registrado como recovery canonico en memoria/changelog. |
| WOT-2026-001c | completed | Cerrado documentalmente en este closeout: se consolida la leccion de mojibake/BOM recurrente y la correccion del propio Manager como superficie legitima. |
| WOT-2026-001d | completed | Cumplido de facto: `review_bridge.py` ya esta por debajo del umbral (`2618 < 2700`). |

> Serie 001x resuelta sin abrir trabajo activo nuevo en `repo_destino`.

---

## WT-2026-250c - Poda documental de backlog y saneo de mojibake en superficies vivas
- **Prioridad:** Media
- **Scope:** system/collab-hygiene
- **Estado:** active
- **deliverable_type:** documentation
- **Criterio:** backlog <200 lineas; 0 mojibake en superficies vivas; PYSEC-196 tiene ficha con criterio de salida; validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-251b - Migrar el dogfooding al prefijo WOT como validacion viva
- **Prioridad:** Alta
- **Scope:** system/ticket-prefix-portability
- **Estado:** pending
- **deliverable_type:** mixed
- **Objetivo:** correr el proximo ticket bajo prefijo `WOT-`. Actualizar `PROJECT.md` del destino con `Ticket prefix: WOT`.
- **Criterio:** un ticket `WOT-2026-001a` completa el ciclo bus con validate 0/0 y archivado correcto.
- **STOP:** no-match silencioso de `WOT-*` en logs -> reabrir WT-2026-251a.
- **Depende de:** WT-2026-251a, WT-2026-250a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-252a - Decision-artifact estructurado del Manager con fallback a parser NDJSON
- **Prioridad:** Alta
- **Scope:** system/review-decision-contract
- **Estado:** pending
- **deliverable_type:** code
- **Objetivo:** el prompt/skill de review instruye al Manager a escribir `.agent/runtime/reviews/decision_<ticket>.json`; el bridge lo lee como canal primario; el parser NDJSON queda como fallback.
- **Files Likely Touched:** `prompts/review_manager.md`, `skills/man-review-implementation/SKILL.md`, `bus/review_bridge.py`, tests (repo_motor).
- **Criterio:** con artifact presente el bridge decide sin leer el transcript (test); `discover_skills.py --check-contract` pasa; ruff + pytest-safe + validate 0/0.
- **STOP:** si el backend no puede garantizar escritura del archivo, degradar a artifact opcional + telemetria.
- **Depende de:** WT-2026-248b.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253a - Reescribir skill code-audit sobre CLIs directas
- **Prioridad:** Media
- **Scope:** system/skills-product
- **Estado:** pending
- **deliverable_type:** documentation
- **Problema:** `skills/code-audit/SKILL.md` instruye ejecutar `python scripts/audit_codebase.py`, que no existe. La skill es inejecutable.
- **Objetivo:** reescribir el Workflow a `uv run vulture`, `uv run deadcode`, `ruff check --select C90,ERA,SIM`; corregir version.
- **Files Likely Touched:** `skills/code-audit/SKILL.md` (repo_motor).
- **Criterio:** cada comando del Workflow ejecuta en el motor real; validate 0/0.
- **STOP:** si vulture/deadcode no corren en Windows, anotar la limitacion en la skill.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253b - Des-localizar repo-compare y graphify del entorno del autor
- **Prioridad:** Media
- **Scope:** system/skills-product
- **Estado:** pending
- **deliverable_type:** documentation
- **Problema:** `skills/repo-compare/SKILL.md` define el proyecto local como `z_scripts/`; `skills/graphify/SKILL.md` usa bash en runtime Windows.
- **Objetivo:** parametrizar proyecto local en repo-compare; pasos agnosticos de shell en graphify; declarar o reescribir networkx.
- **Criterio:** `rg z_scripts skills/` devuelve 0; pasos de graphify ejecutables en PowerShell 5.1; validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-253c - local_audit veraz y AUDIT.md autogenerado en el launcher
- **Prioridad:** Media
- **Scope:** system/bootstrap-observability
- **Estado:** pending
- **deliverable_type:** code
- **Problema:** `scripts/local_audit.py:44` busca `- Version:` pero `PROJECT.md:2` usa `**Version:**`, reportando Unknown. El launcher nunca invoca `local_audit.py`.
- **Objetivo:** alinear parsers; invocar `local_audit.py` en el launcher con timeout best-effort.
- **Criterio:** AUDIT.md reporta la version real; tras lanzar sesion existe AUDIT.md fresco; ruff + pytest-safe + validate 0/0.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-254a - Deprecacion formal Goose/Claw fase 1 (docs y tests)
- **Prioridad:** Media
- **Scope:** system/legacy-deprecation
- **Estado:** pending
- **deliverable_type:** mixed
- **Objetivo:** fase 1 sin borrar codigo: marcar DEPRECATED en docs, mover `test_goose_*.py` fuera de `scripts/`.
- **Files Likely Touched:** `AGENTS.md`, `README.md`, `QUICKSTART.md`, `.goosehints`, scripts de test (repo_motor).
- **Criterio:** ninguna doc del motor presenta Goose/Claw como via oficial; test_goose ya no viven en `scripts/`; suite verde; validate 0/0.
- **STOP:** si el instalador copia superficies Goose a destinos, documentar antes de mover nada.
- **Depende de:** -.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-254b - Regenerar .claude/rules del destino desde el estado real
- **Prioridad:** Media
- **Scope:** system/docs-coherence
- **Estado:** pending
- **deliverable_type:** documentation
- **Problema:** las reglas del destino son plantilla sin adaptar: rutas erroneas (`src/`, `orquestacion_agentes/`, `z_scripts`, `publica/`), `work_plan.md` en `.session/` (el canonico es `.agent/collaboration/`).
- **Objetivo:** reglas regeneradas desde el estado real del destino y del motor.
- **Criterio:** cada comando en las reglas existe en el destino; 0 referencias a rutas inexistentes; validate 0/0.
- **Depende de:** WT-2026-254a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-255a - Extraer parser de decisiones de review_bridge a modulo propio
- **Prioridad:** Media
- **Scope:** system/seam-extraction
- **Estado:** pending
- **deliverable_type:** code
- **Problema:** `bus/review_bridge.py` (3266 lineas) mezcla transporte, parseo y requeue. El parseo tiene mayor churn.
- **Objetivo:** extraer parseo NDJSON + decision-artifact a `bus/review_decision.py`; `review_bridge.py` queda como orquestacion. Sin cambios de comportamiento.
- **Files Likely Touched:** `bus/review_bridge.py`, `bus/review_decision.py` (nuevo), tests (repo_motor).
- **Criterio:** suite review verde; `review_bridge.py` reduce >=600 lineas; ruff + pytest-safe + validate 0/0.
- **STOP:** si la extraccion exige cambiar firmas consumidas por supervisor, replantear el corte.
- **Depende de:** WT-2026-252a.
- **Origen:** session-2026-06-11-system-audit.

## WT-2026-256a - Retirar excepcion PYSEC-2026-196 cuando uv resuelva pip>=26.1.2
- **Prioridad:** Baja
- **Scope:** system/security-dependencies
- **Estado:** pending
- **deliverable_type:** code
- **Problema:** `repo_motor` ignora temporalmente `PYSEC-2026-196` en `[tool.pip-audit].ignore-vuln`. La excepcion no tiene propietario ni caducidad.
- **Objetivo:** cuando `uv lock --upgrade-package pip` fije `pip>=26.1.2`, retirar la excepcion y verificar `python scripts/pip_audit_project.py` sin vulnerabilidades ignoradas.
- **Criterio:** pip-audit pasa sin ignorar PYSEC-2026-196; commit en repo_motor con evidencia de uv lock actualizado; ruff + pytest-safe verdes.
- **STOP:** si `uv` sigue resolviendo `pip<26.1.2`, documentar blocker y retrasar hasta nueva release.
- **Evidencia de origen:** commit `3601312` en repo_motor introdujo el wrapper.
- **Depende de:** -.
- **Origen:** session-2026-06-07-security-followup (reintroducida 2026-06-11).

## Nota de colision de IDs (2026-06-12)

Los tickets de chat de los giros 9-12 se asignaron manualmente como
WT-2026-256a..259a y COLISIONAN con WT-2026-256a (PYSEC-2026-196) de esta
tabla. Los IDs de los commits 8d385df (giro 9), 4970529 (giro 10),
827f96c (giro 11) y 929ca09 (giro 12) se refieren a los giros de
descomposicion, NO al ticket PYSEC. Leccion ya conocida: derivar IDs del
estado real del backlog antes de asignar. El ticket PYSEC conserva el ID
WT-2026-256a en esta tabla.
