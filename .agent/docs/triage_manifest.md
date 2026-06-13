# Triage Manifest - host-extends / motor-provides (WOT-AUDIT-A2b)

Date verified: 2026-06-13
Destination HEAD: `13ee7e1` (+ uncommitted A2b ticket surfaces)
Motor HEAD: `704939f`
Deliverable type: analysis. This document inventories and classifies; it moves,
deletes and repoints NOTHING. Execution lives in later tickets (CI portability,
A2c clone-clean, A2d removal).

## Buckets
- **motor-provides:** reusable tooling / framework / shared scripts-skills-prompts.
  A verified FUNCTIONAL equivalent is (or must be) the motor's; the destino must
  not version the copy. Some rows carry a `stale-diverged` flag: the destino copy
  differs from the motor and the motor coverage must be reconciled before removal.
- **destino-keep:** operational state, local integration, host config, authentic
  host overrides, or repo_destino domain functionality.
- **huerfano-needs-decision:** no functional equivalent in the motor AND does not
  implement destino domain. Decide promote-to-motor vs archive.
- **ci-portability-blocker:** machine-executed CI surface that depends on local
  copies and cannot reference a sibling motor in GitHub Actions.

## Classification criterion (frozen, from work_plan)
Axis: development/creation of the system -> motor; operational state / integration
/ host config / host overrides / domain functionality -> destino. "Particular by
domain" counts as destino-keep ONLY if it implements repo_destino behavior, not
because it is system tooling that merely happens to exist only in the destino.
Equivalence is judged FUNCTIONALLY (diff/behavior), never by basename.

---

## 1. `scripts/` (12 tracked) -- all dev/creation tooling

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `scripts/run_pytest_safe.py` | motor-provides (stale-diverged) | dev test-runner; motor tiene `scripts/run_pytest_safe.py` v2.0; diff=601 lineas (copia muy vieja) | `.claude/settings.local.json` (personal), `agent_system/scripts/install_agent_system.py`, `agent_system/tests/test_hooks.py`, `scripts/audit_codebase.py` | referenciar motor; reconciliar cobertura antes de A2d |
| `scripts/discover_skills.py` | motor-provides (stale-diverged) | indexador de skills; motor lo tiene; diff=304 | CI `.github/workflows/quality-gates.yml`, `.claude/settings.local.json`, `agent_system/scripts/orquestador.py` | referenciar motor; CI ver bucket 8 |
| `scripts/upgrade_agent_system.py` | motor-provides (stale-diverged) | instalador/upgrade del sistema; motor lo tiene; diff=485 | `agent_system/scripts/*` (cadena interna) | referenciar motor; reconciliar antes de A2d |
| `scripts/detect_agent_system_version.py` | motor-provides (stale-diverged) | deteccion de version del sistema; motor lo tiene; diff=230; menciona `z_scripts` (nombre viejo) | `rollback`/`upgrade_agent_system` (cadena interna) | referenciar motor; reconciliar antes de A2d |
| `scripts/test_refactoring_impact.py` | motor-provides (stale-diverged) | suite de impacto refactor; motor `tests/` lo tiene; diff=64 | nadie vivo (solo docs) | referenciar motor (test corre en suite) |
| `scripts/test_refactor_kit_portable.py` | motor-provides | suite refactor-kit; motor `tests/` lo tiene; diff=3 (equivalente) | nadie vivo (solo docs) | referenciar motor (suite) |
| `scripts/test_refactor_kit_performance.py` | motor-provides | motor `tests/` lo tiene; diff=2 (equivalente, confirmado A2a) | `.claude/settings.local.json` (personal) | referenciar motor (suite); ya corregido en A2a |
| `scripts/artifact_graph.py` | huerfano-needs-decision | grafo de artefactos; NO existe en el motor | solo `scripts/audit_codebase.py` (cluster) | promover al motor vs archivar |
| `scripts/audit_codebase.py` | huerfano-needs-decision | orquestador de auditoria; NO en el motor; sin entrypoint vivo a nivel destino | nadie vivo (invoca a otros) | promover vs archivar |
| `scripts/rollback_agent_system.py` | huerfano-needs-decision | rollback del sistema; NO en el motor | `upgrade_agent_system` (cluster) | promover vs archivar |
| `scripts/state_drift.py` | huerfano-needs-decision | detector de drift de sesion; NO en el motor (su rol vive hoy en `agent_controller --validate`) | solo `scripts/audit_codebase.py` (cluster) | archivar (superado por validate) vs promover |
| `scripts/test_refactor_manager_skill.py` | huerfano-needs-decision | suite del refactor manager; NO en el motor | nadie vivo | promover vs archivar |

## 2. `skills/` (41 tracked) -- skills de proceso/sistema

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `skills/<15 dirs de skill>/` (bui-*, man-*, project-finalize, graphify, refactor-manager, etc.) | motor-provides | mismos dirs existen en `motor/skills/`; skills compartidas del framework | discovery del motor (host-first) | referenciar motor; verificar paridad por skill antes de A2d |
| `skills/validate_all.py` | motor-provides | existe `motor/skills/validate_all.py`; tooling de validacion de skills | runtime/discovery | referenciar motor |
| `skills/README.md`, `skills/_shared/` | motor-provides | doc/util compartida del framework | solo-docs / util interna | referenciar motor |

Nota: ninguna skill identificada como autoria de dominio del destino. Pendiente
de confirmar paridad funcional por skill en A2d (no por nombre de dir).

## 3. `agent_system/` (113 tracked) -- bundle del framework

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `agent_system/**` (docs, scripts, skills, tests, refactor_kit, templates) | motor-provides | es el arbol del framework; el motor tiene `agent_system/`. Marcado en AGENTS.md como "NO copiar/editar en proyectos derivados" | cadena interna del propio bundle | referenciar motor; eliminar del destino en A2d |

## 4. `tests/` (2 tracked)

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `tests/test_event_bus_hygiene.py` | motor-provides | existe en `motor/tests/`; test del bus compartido | suite | referenciar motor |
| `tests/test_ticket_007_context_recovery.py` | huerfano-needs-decision | "Selective Context Recovery Lite"; NI el test NI el feature existen en el motor | nadie vivo | confirmar si es experimento del destino (domain) o legacy -> promover/archivar |

## 5. `.agent/` (125 tracked) -- mayoritariamente estado del destino

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `.agent/collaboration/**` (96) | destino-keep | estado operativo de tickets (work_plan, TURN, STATE, execution_log, backlog, review_queue, audits, archive); contrato MANIFEST.workspace | controller del motor (lee estado) | conservar |
| `.agent/audits/**` (12) | destino-keep | auditorias del destino (system_health); MANIFEST.workspace `.agent/audits/system_health/` | health-audit | conservar |
| `.agent/runtime/**` (8: events, memory) | destino-keep | bus y memoria del destino; MANIFEST.workspace `runtime/events`, `runtime/memory` | controller/memory_loader | conservar |
| `.agent/config/**` (3: agents.json, hooks_config.json, destination_context.json) | destino-keep | config de integracion del host; MANIFEST.workspace los lista | controller/launcher | conservar |
| `.agent/.version_manifest.json` | destino-keep | estado tecnico de version del destino; MANIFEST.workspace lo lista | doctor/upgrade | conservar |
| `.agent/docs/resource_precedence.md`, `.agent/docs/triage_manifest.md` | destino-keep | docs de autoria del destino (A2a/A2b) | solo-docs | conservar |
| `.agent/README.md` | motor-provides | el motor tiene `.agent/README.md`; doc de framework | solo-docs | referenciar motor (verificar si esta customizado) |
| `.agent/hooks/pre_compact_hook.py` | huerfano-needs-decision | hook de framework; el motor `.agent/hooks/` tiene `guard_paths.py`/`__init__.py` pero NO este; ambiguo (framework generico vs hook de integracion del host) | wiring de pre-compact | decidir promover al motor vs conservar como hook del host |
| `.agent/microagents/onboarding.md` | huerfano-needs-decision | NO existe en el motor; onboarding (posible host-specific o stale) | solo-docs | confirmar host-specific (keep) vs legacy (archivar) |
| `.agent/glossary.md` | huerfano-needs-decision | NO existe en el motor; glosario (posible host vs stale) | solo-docs | confirmar keep vs archivar |

## 6. `.claude/` (11 tracked) -- integracion del host

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `.claude/settings.json` | destino-keep | config de integracion versionada del host (portable) | Claude Code | conservar |
| `.claude/rules/**`, `.claude/commands/**`, `.claude/README.md` | destino-keep | reglas/commands de integracion de ESTE repo | Claude Code (contexto) | conservar (actualizar referencias stale a comandos en doc-pass aparte) |

Nota: `.claude/settings.local.json` (untracked, gitignored) = machine-executed
local PERSONAL; fuera del contrato de portabilidad; no se versiona ni migra.

## 7. root (13 tracked) + CI

| ruta | bucket | por que (funcional) | quien la invoca hoy | accion posterior |
| --- | --- | --- | --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `PROJECT.md`, `README.md`, `CHANGELOG.md`, `EXECUTIVE_SUMMARY.md`, `RUNTIME_EXCLUSIONS.md` | destino-keep | docs de identidad/instruccion operativa de ESTE repo (Claude/agentes las leen) | agentes (contexto) | conservar (contenido espeja templates del motor; no migrar el archivo) |
| `.gitignore`, `.gitignore_global`, `ruff.toml`, `repomix.config.json`, `workspace_orquestador_de_agentes.code-workspace` | destino-keep | config del host | tooling local | conservar |
| `.goosehints` | huerfano-needs-decision | integracion de Goose, DEPRECADO (WT-2026-254a); historial de mojibake | Goose (deprecado) | archivar |
| `.github/workflows/quality-gates.yml` | ci-portability-blocker | CI corre `compileall scripts tests` + `discover_skills.py` (guarded); GitHub Actions hace checkout SOLO del destino, no hay motor sibling | GitHub Actions (push/PR) | ticket CI portability: checkout/instalar motor o saltar; gate de A2d |

---

## Resumen por bucket (conteo aproximado, grupos contados por su volumen)
- **motor-provides:** `scripts/` 7, `skills/` ~41, `agent_system/` 113, `tests/` 1,
  `.agent/README.md` 1 -> el grueso del arbol de tooling/framework.
- **destino-keep:** `.agent/` estado (~120: collaboration/audits/runtime/config/docs/
  version), `.claude/` 11, root docs/config 12.
- **huerfano-needs-decision:** `scripts/` 5, `tests/` 1, `.agent/` 3
  (pre_compact_hook, onboarding, glossary), root 1 (`.goosehints`) = 10 rutas.
- **ci-portability-blocker:** 1 (`.github/workflows/quality-gates.yml`).

## Conclusion (vacio-hasta-prueba, NO cerrada)
No se ha encontrado ninguna herramienta claramente de DOMINIO del repo_destino: el
conjunto `destino-keep por dominio` se declara **vacio-hasta-prueba**. Lo que el
destino conserva legitimamente hoy es estado operativo, integracion y config del
host (coherente con MANIFEST.workspace, que restringe el workspace a `.agent/`).

Avisos para los tickets de ejecucion (NO resueltos aqui):
1. Las copias "comunes" de `scripts/` estan STALE/divergidas (hasta 601 lineas):
   A2d debe reconciliar cobertura funcional del motor antes de eliminar, no asumir
   equivalencia por nombre.
2. 10 rutas huerfanas requieren decision explicita promover-vs-archivar (incluye
   posibles host-specific reales: `pre_compact_hook`, `onboarding`, `glossary`,
   y `test_ticket_007` que podria ser dominio del destino).
3. El CI es el unico bloqueante machine-executed de A2d y necesita su propio ticket.
