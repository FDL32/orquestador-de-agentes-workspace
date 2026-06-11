# Execution Log WT-2026-248b

**Estado:** COMPLETED

## Metadata

- **ID:** WT-2026-248b
- **deliverable_type:** mixed
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT_WORK

## Fase 0: Diagnostico

### Seams confirmados

| Archivo | Estado | Hallazgo |
|---------|--------|----------|
| `prompts/review_manager.md` | Existe, 127 lines | Wrapper sin `Skill canonica:` ni `contract_id`. Usa veredicto tripartito `APROBADO`/`CHANGES` (binario correcto). Sin referencia a skill fuente. |
| `prompts/launch_builder.md` | Existe, 161 lines | Wrapper sin `Skill canonica:` ni `contract_id`. Usa `{{TEMPLATE_VARS}}`. Sin referencia a skill fuente. |
| `skills/man-review-implementation/SKILL.md` | Existe, 383 lines | Frontmatter sin `source_prompt:` ni `contract_id`. Contiene `CAMBIOS_REQUERIDOS`, `RECHAZADO`, `Ï³ PENDING` (mojibake). Veredicto tripartito. Gates legacy. |
| `skills/bui-implement-from-plan/SKILL.md` | Existe, 425 lines | Frontmatter sin `source_prompt:` ni `contract_id`. Contiene `Regla de 2 Acciones`. Sin contrato moderno de `deliverable_type`. |
| `scripts/discover_skills.py` | Existe, 164 lines | `extract_frontmatter()` colapsa YAML invalido a `{}` silenciosamente. No distingue "sin frontmatter", "YAML invalido" y "frontmatter valido sin campo". No existe `--check-contract`. |
| `scripts/run_gates_dispatch.py` | Existe, 134 lines | `main()` ejecuta code_gates + deliverable_gates segun dtype. No invoca ningun checker contractual. Punto de integracion: final de `main()` antes de `return 0`. |
| `tests/test_discover_skills.py` | NO existe | No hay tests focales para este ticket. Tests existentes en `tests/unit/test_skill_discovery.py` (292 lines) cubren descubrimiento basico, frontmatter parsing, host-precedence. |
| `PROJECT.md` | Existe, 92 lines | Menciona `248b` como pendiente. No describe el contrato prompt/skill hardening. |
| `CHANGELOG.md` | Existe | Ultima entrada: Git EOL hygiene. No menciona `248b`. |

### Hallazgos relevantes

1. **Parser de frontmatter existente**: `extract_frontmatter()` en `discover_skills.py` usa parsing manual linea-por-linea con `": "` split. No usa `yaml.safe_load`. Colapsa cualquier excepcion a `{}` silenciosamente. No distingue YAML invalido de frontmatter ausente.
2. **Parser alternativo**: `skills/validate_all.py` tiene `extract_frontmatter()` con regex y `yaml.safe_load`. No es reutilizable directamente porque esta en skills/.
3. **`discover_skills.py` resuelve rutas**: `bundle_root = Path(__file__).resolve().parent.parent` -> `skills_dir = bundle_root / "skills"`. Las rutas son siempre relativas al `repo_motor`.
4. **Punto de integracion en `run_gates_dispatch.py`**: `main()` lineas 119-130. Despues de code_gates y deliverable_gates, antes de `return 0`. Debe ser paso final e independiente de `deliverable_type`.
5. **No hay desviacion de scope**: todos los archivos estan dentro de `Files Likely Touched`.

### Evidencia de deuda heredada (pre-fix)

```powershell
rg "CAMBIOS_REQUERIDOS|RECHAZADO|Ã¯Â¿Â½ PENDING" skills/man-review-implementation/SKILL.md
# Resultado esperado: >0 coincidencias (deuda a limpiar)

rg "Regla de 2 Acciones" skills/bui-implement-from-plan/SKILL.md
# Resultado esperado: >0 coincidencias (deuda a limpiar)
```

## Registro de ejecucion

### Fase 1: Manager contract sync (COMPLETED)

**Archivos tocados:**
- `skills/man-review-implementation/SKILL.md`: anadido `source_prompt: prompts/review_manager.md`, `contract_id: cid-man-review-v1`. Veredicto tripartito reemplazado por binario (APROBADO/CHANGES). Eliminados `CAMBIOS_REQUERIDOS`, `RECHAZADO`, `Ã¯Â¿Â½ PENDING` (mojibake), gates legacy.
- `prompts/review_manager.md`: anadido `Skill canonica: skills/man-review-implementation/SKILL.md` y `contract_id: cid-man-review-v1`.

### Fase 2: Builder contract sync (COMPLETED)

**Archivos tocados:**
- `skills/bui-implement-from-plan/SKILL.md`: anadido `source_prompt: prompts/launch_builder.md`, `contract_id: cid-bui-implement-v1`. Eliminado `Regla de 2 Acciones` y vocabulario heredado. Workflow alineado con `--pre-handoff` + `--mark-ready`.
- `prompts/launch_builder.md`: anadido `Skill canonica: skills/bui-implement-from-plan/SKILL.md` y `contract_id: cid-bui-implement-v1`.

### Fase 3: Contract barrier and docs (COMPLETED)

**Archivos tocados:**
- `scripts/discover_skills.py`: anadido `parse_frontmatter()` con tri-state (data, error). Anadido `_validate_single_skill()` y `_check_contract()` para `--check-contract`. `extract_frontmatter()` preservado para backward compat.
- `scripts/run_gates_dispatch.py`: integrado `discover_skills.py --check-contract` como paso final en `main()`, independiente de `deliverable_type`.
- `tests/test_discover_skills.py`: 20 tests (nuevo archivo).
- `PROJECT.md`: estado actualizado a 248b completado.
- `CHANGELOG.md`: entrada anadida para 248b.

### Quality Gates

```powershell
# 1. pytest focal
python -m pytest tests/test_discover_skills.py -v
# Result: 20 passed in 0.16s

# 2. ruff check
ruff check scripts/discover_skills.py scripts/run_gates_dispatch.py tests/test_discover_skills.py
# Result: All checks passed!

# 3. --check-contract
python scripts/discover_skills.py --check-contract
# Result: exit 0
# skills/bui-implement-from-plan/SKILL.md: contrato valido (source_prompt=prompts/launch_builder.md, contract_id=cid-bui-implement-v1)
# skills/man-review-implementation/SKILL.md: contrato valido (source_prompt=prompts/review_manager.md, contract_id=cid-man-review-v1)

# 4. validate repo_destino
python .agent/agent_controller.py --validate --json --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Result: 0 errors, 0 warnings (ticket_prose warnings are non-blocking)
```

### Evidencia de limpieza auxiliar

```powershell
Select-String -Path "skills/man-review-implementation/SKILL.md" -Pattern "CAMBIOS_REQUERIDOS|RECHAZADO|Ã¯Â¿Â½ PENDING"
# Result: 0 matches (deuda limpiada)

Select-String -Path "skills/bui-implement-from-plan/SKILL.md" -Pattern "Regla de 2 Acciones"
# Result: 0 matches (deuda limpiada)
```

### Commit

```
28555a1 feat(WT-2026-248b): bidirectional prompt<->skill contract hardening
9 files changed, 607 insertions(+), 503 deletions(-)
create mode 100644 tests/test_discover_skills.py
```


Manager approved canonical closeout for WT-2026-248b

Manager approved canonical closeout for WT-2026-251a

Manager approved canonical closeout for WT-2026-251a