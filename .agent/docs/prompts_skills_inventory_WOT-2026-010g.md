# Inventory Report: prompts/ + skills/ - WOT-2026-010g

> **Fase:** ANALYSIS (read-only)
> **Motor HEAD:** 8dbfcda (WOT-2026-010h)
> **Destino:** orquestador_de_agentes_workspace
> **Fecha:** 2026-06-17
> **Taxonomia:** canonical / alias-compat / legacy-retained / deprecated-removable / destination-only

---

## 1. Prompts (`prompts/*.md`) - 20 archivos

| # | Archivo | Etiqueta | Consumidores vivos (rg) | Notas |
|---|---------|----------|------------------------|-------|
| 1 | `audit_agent_output.md` | **canonical** | Consumido por `skills/orchestrate-pipeline/SKILL.md`, `skills/audit-pipeline/SKILL.md` | Prompt base de auditoria adversarial |
| 2 | `audit_bus.md` | **canonical** | Prompt independiente, referenciado en docs | Bus event audit |
| 3 | `audit_cf_plan_graph.md` | **canonical** | Contrato formation pipeline | CF audit: plan graph |
| 4 | `audit_cf_repo_charter.md` | **canonical** | Contrato formation pipeline | CF audit: repo charter |
| 5 | `audit_cf_ticket_contract.md` | **canonical** | Contrato formation pipeline | CF audit: ticket contract |
| 6 | `audit_complete_motor_destination.md` | **canonical** | Referenciado en `prompts/audit_post_change_system_health.md` (hereda dimensiones) | Auditoria completa motor+destino |
| 7 | `audit_git_publication.md` | **canonical** | Referenciado en `prompts/destination_bootstrap.md`, `skills/orchestrate-pipeline/SKILL.md` | Auditoria de publicacion Git |
| 8 | `audit_pipeline.md` | **canonical** | Consumido por `skills/audit-pipeline/SKILL.md` | Meta-auditoria de pipeline |
| 9 | `audit_plan.md` | **alias-compat** | Consumido por: `AGENTS.md` (lo menciona como alias canonico), `MANIFEST.distribute` (lo lista como parte del motor), `docs/registry/INDEX.md` (registro activo), `.agent/context/project-map.json` (mapa de proyecto), `graphify-out/graph.json` (grafo de dependencias) | **Stub alias** de `audit_ticket_contract.md` (renombrado en WOT-2026-010a). Contenido: solo `# Legacy alias: audit_plan.md -> audit_ticket_contract.md`. Se conserva para compatibilidad de referencias externas. |
| 10 | `audit_post_change_system_health.md` | **canonical** | Referenciado en `prompts/destination_bootstrap.md` (paso de salud post-cambio) | Auditoria de salud post-cambio |
| 11 | `audit_ticket_contract.md` | **canonical** | Destino real del alias `audit_plan.md`. Consumido por `AGENTS.md`, `prompts/orchestrator_pipeline.md` | Prompt de auditoria de contrato de ticket |
| 12 | `contract_formation_pipeline.md` | **canonical** | Consumido por `prompts/orchestrator_pipeline.md` | Pipeline de formacion de contrato |
| 13 | `destination_bootstrap.md` | **canonical** | Consumido por `skills/orchestrate-pipeline/SKILL.md` | Bootstrap para repos destino |
| 14 | `launch_builder.md` | **canonical** | Consumido por `prompts/audit_complete_motor_destination.md`, `prompts/orchestrator_pipeline.md` | Prompt de lanzamiento de Builder |
| 15 | `memory_upload.md` | **canonical** | Consumido por `AGENTS.md` (referencia de memoria) | Upload de memoria portable |
| 16 | `orchestrator_pipeline.md` | **canonical** | Consumido por `skills/orchestrate-pipeline/SKILL.md`, `prompts/destination_bootstrap.md` | Pipeline central de orquestacion |
| 17 | `refactor_bootstrap.md` | **canonical** | Consumido por `skills/refactor-manager/SKILL.md` (referencia), `scripts/build_llms.py` (incluido en LLM), `docs/registry/INDEX.md` (registro) | Bootstrap para sesiones de refactor |
| 18 | `review_manager.md` | **canonical** | Consumido por `skills/orchestrate-pipeline/SKILL.md`, `skills/audit-pipeline/SKILL.md` | Prompt de revision del Manager |
| 19 | `session_bootstrap.md` | **canonical** | Consumido por `prompts/audit_complete_motor_destination.md` (fuente minima) | Bootstrap canonico de sesion |
| 20 | `session_close_chat.md` | **canonical** | Consumido por `prompts/orchestrator_pipeline.md` (2 referencias), `skills/orchestrate-pipeline/SKILL.md` (2 referencias) | Cierre de sesion por chat |

### Resumen prompts

| Etiqueta | Cantidad |
|----------|----------|
| canonical | 19 |
| alias-compat | 1 (`audit_plan.md`) |
| legacy-retained | 0 |
| deprecated-removable | 0 |
| destination-only | 0 |

---

## 2. Skills (`skills/*/`) - 29 skills + 2 support dirs

Total directories: 31. Breakdown: 29 **skills** (tienen `SKILL.md`), 1 **support** (`_shared/`, sin `SKILL.md`), 1 **cache** (`__pycache__/`).

### 2a. Skills con SKILL.md (canonical salvo excepciones)

| # | Skill | Archivos clave | Etiqueta | Notas |
|---|-------|---------------|----------|-------|
| 1 | `audit-git-publication` | SKILL.md | **canonical** | Git publication audit |
| 2 | `audit-pipeline` | SKILL.md | **canonical** | Pipeline meta-audit |
| 3 | `bui-implement-from-plan` | SKILL.md | **canonical** | Builder implementa desde plan |
| 4 | `bui-run-quality-gates` | SKILL.md | **canonical** | Builder gates |
| 5 | `bui-self-audit` | SKILL.md | **canonical** | Builder self-audit |
| 6 | `bui-write-deliverable` | SKILL.md | **canonical** | Builder deliverable writing |
| 7 | `code-audit` | SKILL.md | **canonical** | Code audit |
| 8 | `create-agent-skill` | SKILL.md | **canonical** | Skill creation |
| 9 | `deep-research` | SKILL.md | **canonical** | Deep research |
| 10 | `graphify` | SKILL.md | **canonical** | Dependency grapher |
| 11 | `grill-work-plan` | SKILL.md | **canonical** | Work plan critique |
| 12 | `local-audit` | SKILL.md | **canonical** | Local audit |
| 13 | `man-create-work-plan` | SKILL.md | **canonical** | Manager creates work plan |
| 14 | `man-resolve-escalation` | SKILL.md | **canonical** | Manager escalation |
| 15 | `man-review-implementation` | SKILL.md | **canonical** | Manager review |
| 16 | `man-session-closeout` | SKILL.md | **canonical** | Manager session close |
| 17 | `memory-consolidate` | SKILL.md | **canonical** | Memory consolidation |
| 18 | `orchestrate-pipeline` | SKILL.md | **canonical** | Pipeline orchestration |
| 19 | `project-finalize` | SKILL.md | **canonical** | Project finalization |
| 20 | `refactor-manager` | SKILL.md, PROMPT_TEMPLATE.md, EXECUTION_PROMPT.md, goose-skill.json, goose_integration.py | **canonical** (skill core) + **deprecated-removable** (goose-skill.json) + **legacy-retained** (goose_integration.py) | Skill central de refactor. Contiene 2 artefactos Goose que requieren atencion (ver seccion 2c). |
| 21 | `repo-compare` | SKILL.md | **canonical** | Repo comparison |
| 22 | `scaffold-python-project` | SKILL.md | **canonical** | Python project scaffolding |
| 23 | `secure-existing-project` | SKILL.md | **canonical** | Security audit |
| 24 | `session-close-observations` | SKILL.md + references/ | **canonical** | Session observations |
| 25 | `setup-agent-system` | SKILL.md + references/quickstart-checklist.md | **canonical** (skill) + **legacy-retained** (references/quickstart-checklist.md) | Setup del sistema agente. Contiene 1 legacy reference (ver seccion 2c). |
| 26 | `system-health-audit` | SKILL.md | **canonical** | System health audit |
| 27 | `systematic-debugging` | SKILL.md | **canonical** | Systematic debugging |
| 28 | `test-driven-development` | SKILL.md | **canonical** | TDD |
| 29 | `version-changelog` | SKILL.md + references/ | **canonical** | Version & changelog |

### 2b. Support directories

| Directorio | Contenido | Etiqueta | Notas |
|------------|-----------|----------|-------|
| `_shared/` | `anti-patterns.md`, `ap-schema.md`, `ticket-anti-patterns.md` | **canonical** (support) | Recursos compartidos referenciados por skills. Sin SKILL.md propia. No requiere accion. |
| `__pycache__/` | Cache Python (auto-generado) | - | Gitignored. No es skill. No requiere accion. |

### 2c. Artefactos candidates a atencion dentro de skills

#### goose-skill.json (`skills/refactor-manager/`)
- **Etiqueta:** `legacy-retained`
- **Evidencia rg:** Consumido por `tests/test_goose_native_skill.py::test_skill_manifest` (assert exists sobre la ruta literal). Mismo test que consume `goose_integration.py`. Aunque la referencia es por ruta-string, un `assert exists()` falla igual que un import roto.
- **Justificacion:** Tiene un consumidor vivo ejecutable (test activo en suite canonica). No se puede declarar removable sin retirar el test primero. `legacy-retained` hasta que el test se deprecate en ticket de follow-up.
- **Rollback:** `git checkout 8dbfcda -- skills/refactor-manager/goose-skill.json`

#### goose_integration.py (`skills/refactor-manager/`)
- **Etiqueta:** `legacy-retained`
- **Evidencia rg:** Consumido por `tests/test_goose_native_skill.py` (test_goose_integration_import, test_refactor_manager_goose_context). Tambien importa de `agent_system.refactor_kit`.
- **Justificacion:** Tiene consumidores vivos (test legacy). No se puede declarar removable sin eliminar primero el test o marcarlo como deprecated. `legacy-retained` hasta que el test se retire en ticket de follow-up.
- **Nota:** `tests/deprecated/test_goose_realworld.py` y `test_goose_triggers.py` ya estan en `tests/deprecated/` - senial de que la migracion Goose->OpenCode esta en marcha.

#### quickstart-checklist.md (`skills/setup-agent-system/references/`)
- **Etiqueta:** `legacy-retained`
- **Evidencia rg:** Consumido solo por `docs/registry/INDEX.md` (line 74) como registro pasivo. Ningun script, prompt, skill o archivo operativo lo referencia.
- **Justificacion:** El unico consumidor es el indice de registro del motor, que lista archivos sin consumir su contenido. Al no existir consumidores operativos, es candidato a `deprecated-removable` tras actualizar el registro. Se mantiene `legacy-retained` por precaucion (principio: ante duda, no removable).
- **Rollback:** `git checkout 8dbfcda -- skills/setup-agent-system/references/quickstart-checklist.md`

---

## 3. Candidatos destination-only

Ningun prompt ni skill del motor califica como `destination-only`. Todos los `prompts/*.md` y las `skills/*/` con `SKILL.md` son tooling portable del motor, necesarios para que el motor funcione en cualquier destino.

El reporte actual (este archivo) es el unico artefacto `destination-only` de esta sesion, siguiendo el precedente de WOT-2026-008a (`.agent/docs/taxonomy_migration_WOT-2026-008a.md`).

---

## 4. Candidatos a archivar en motor

| Artefacto | Accion propuesta | Pre-requisito | Rollback |
|-----------|-----------------|---------------|----------|
| `skills/refactor-manager/goose-skill.json` | DELETE (remover del motor) | Ticket de follow-up que: 1) deprecate/remueva `tests/test_goose_native_skill.py::test_skill_manifest`, 2) confirme que `scripts/discover_skills.py` no genera trigger_map desde el JSON | `git checkout <pre-commit-sha> -- skills/refactor-manager/goose-skill.json` |
| `skills/setup-agent-system/references/quickstart-checklist.md` | DELETE (remover del motor) | Ticket de follow-up que: 1) elimine la fila de `docs/registry/INDEX.md`, 2) actualice `MANIFEST.distribute` si listaba el archivo | `git checkout <pre-commit-sha> -- skills/setup-agent-system/references/quickstart-checklist.md` |
| `skills/refactor-manager/goose_integration.py` | DELETE (remover del motor) | Ticket de follow-up que: 1) deprecate/remueva tests que lo importan, 2) verifique que `agent_system.refactor_kit` sigue funcionando sin el | `git checkout <pre-commit-sha> -- skills/refactor-manager/goose_integration.py` |

> **Importante:** Ninguna accion destructiva se ejecuta en este ticket. Las propuestas arriba son diagnosticos para tickets de follow-up.

---

## 5. Taxonomia completa (resumen)

| Taxonomia | Prompts | Skills (carpetas) | Skills (artefactos internos) | Total |
|-----------|---------|-------------------|------------------------------|-------|
| canonical | 19 | 29 | 2 (propiamente: `_shared/` support) | 50 |
| alias-compat | 1 (`audit_plan.md`) | 0 | 0 | 1 |
| legacy-retained | 0 | 0 | 3 (`goose_integration.py`, `goose-skill.json`, `quickstart-checklist.md`) | 3 |
| deprecated-removable | 0 | 0 | 0 | 0 |
| destination-only | 0 | 0 | 0 | 0 |
| cache (no clasificar) | - | 1 (`__pycache__/`) | - | 1 |

---

## 6. Seam de busqueda usado

Para cada candidato a move/delete se ejecuto:

```
Select-String -Pattern "<basename>" -Path @(
  <motor>/prompts/*,
  <motor>/scripts/*,
  <motor>/skills/*,
  <motor>/tests/*,
  <motor>/.agent/*,
  <motor>/AGENTS.md,
  <motor>/docs/registry/INDEX.md,
  <motor>/MANIFEST.distribute
)
```

Se buscaron referencias literales al nombre del archivo/directorio candidato. Exclusiones: `__pycache__/`, `.git/`, `.venv/`, `node_modules/`, archivos de cache y backups.

---

## 7. Observaciones adicionales

1. **Goose/Claw en AGENTS.md** (line 7): Referencia historica marcada `[DEPRECATED - WT-2026-254a]`. No se cambia en este ticket (historia fiel). Tickets de follow-up pueden retirar la referencia tras confirmar que `scripts/orquestador.py` tambien se depreca.

2. **`scripts/orquestador.py`**: Contiene `GooseAdapter` y `--engine goose` (lineas 167-204, 660). Es un consumidor vivo del patron Goose en scripts/. Pendiente de deprecacion formal.

3. **`scripts/discover_skills.py`**: Lineas 5, 557-558 mencionan Goose. Es el script que genera trigger_map. Pendiente de revision en ticket de follow-up.

4. **`tests/deprecated/test_goose_realworld.py` y `test_goose_triggers.py`**: Ya movidos a `tests/deprecated/`. Senial positiva de migracion.

5. **`tests/test_goose_native_skill.py`**: Test activo que importa `goose_integration.py`. Bloquea la declaracion de `goose_integration.py` como removable.