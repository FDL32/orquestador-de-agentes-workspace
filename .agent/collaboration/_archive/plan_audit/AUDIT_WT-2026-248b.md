# AUDIT_WT-2026-248b - Prompt/Skill contract hardening

## Tipo de auditoria
- **Ticket:** WT-2026-248b
- **deliverable_type:** mixed
- **Objetivo de auditoria:** verificar que el contrato bidireccional
  `prompt <-> skill` queda alineado, ejecutable y protegido por una barrera de
  regresion integrada en gates.

## TP Check
- **TP-01: Contradiccion secuencial** - PASS esperado si las fases son
  commitables e independientes (Manager -> Builder -> barrera/docs).
- **TP-02: Criterio no verificable** - FAIL si algun cierre usa lenguaje como
  "alineado", "limpio" o "correcto" sin comando literal.
- **TP-03: Deriva de ambito implicita** - FAIL si aparece una superficie fuera
  de `Files Likely Touched` o si se intenta meter `.opencode/opencode.json`.
- **TP-04: Semantica blanda** - FAIL si el checker no distingue YAML invalido,
  ruta ausente, ruta no portable y falta de ancla inversa.
- **TP-05: Paridad PLAN/AUDIT rota** - FAIL si este audit no replica las tres
  fases y los mismos criterios binarios del plan.
- **TP-07: Alcance condicional** - FAIL si la integracion en gates queda como
  "si aplica" sin comando o punto de integracion concreto.

## Criterios binarios de aprobacion

### Fase 1 - Manager
- `skills/man-review-implementation/SKILL.md` contiene `source_prompt:`
  valido en frontmatter y `contract_id` no vacio.
- `prompts/review_manager.md` contiene
  `Skill canonica: skills/man-review-implementation/SKILL.md`.
- `prompts/review_manager.md` contiene el mismo `contract_id` que la skill.
- `rg "CAMBIOS_REQUERIDOS|RECHAZADO|ÃÂ³ PENDING" skills/man-review-implementation/SKILL.md`
  devuelve 0 coincidencias.
- El workflow del Manager usa veredicto binario `APROBADO` / `CHANGES` y no
  reintroduce gates legacy fuera del contrato actual.

### Fase 2 - Builder
- `skills/bui-implement-from-plan/SKILL.md` contiene `source_prompt:` valido y
  `contract_id` no vacio.
- `prompts/launch_builder.md` contiene
  `Skill canonica: skills/bui-implement-from-plan/SKILL.md`.
- `prompts/launch_builder.md` contiene el mismo `contract_id` que la skill.
- `rg "Regla de 2 Acciones" skills/bui-implement-from-plan/SKILL.md`
  devuelve 0 coincidencias.
- El workflow del Builder queda alineado con `--pre-handoff` +
  `--mark-ready` y con `deliverable_type`.

### Fase 3 - Barrera y docs
- `python scripts/discover_skills.py --check-contract` termina con exit 0 y
  sin warnings en estado final.
- El checker falla con exit no cero si:
  - el frontmatter YAML es invalido;
  - falta `source_prompt:`;
  - falta `contract_id`;
  - la ruta referida no existe;
  - la ruta no se resuelve de forma portable contra `repo_motor`;
  - el prompt no contiene el ancla inversa `Skill canonica: <ruta_skill>`.
- `python -m pytest tests/test_discover_skills.py -v` pasa.
- `ruff check scripts/discover_skills.py scripts/run_gates_dispatch.py tests/test_discover_skills.py` pasa.
- `scripts/run_gates_dispatch.py` ejecuta el checker desde `main()` como paso
  final e independiente del `deliverable_type`.
- `PROJECT.md` y `CHANGELOG.md` describen `248b` como follow-up estructural de
  prompt/skill; no lo mezclan con runtime/config de OpenCode.

## Riesgos a vigilar durante review
- **ALTO:** checker unidireccional que solo valida existencia.
- **ALTO:** `source_prompt:` valido solo en el entorno local del Builder y no
  portable contra `repo_motor`.
- **ALTO:** barrera no integrada en gates reales.
- **ALTO:** fases 1 y 2 reportadas como cerradas usando `--check-contract`
  antes de que el flag exista.
- **MEDIO:** `grep` usado como contrato principal en vez de evidencia auxiliar.
- **MEDIO:** cambio parcial en prompt o skill sin reflejo en la contraparte.
- **MEDIO:** `extract_frontmatter()` sigue colapsando YAML invalido a `{}` y
  no permite distinguir sintaxis rota de contrato ausente.
- **BAJO:** docs correctas pero script sin mensajes de error accionables.

## Evidencia minima requerida en execution_log.md
- comando exacto de `discover_skills.py --check-contract`
- salida exacta de `pytest` focal
- salida exacta de `ruff`
- evidencia de `grep` para terminos heredados como limpieza auxiliar, no como
  prueba principal del contrato
- referencia al commit aislado de cada fase si hubo 3 commits

## Blockers de no-aprobacion
- falta `source_prompt:` en cualquier skill de rol tocada
- falta `contract_id` o mismatch entre skill y prompt
- falta la linea `Skill canonica: ...` en cualquier prompt wrapper tocado
- checker no valida ancla inversa
- checker no valida portabilidad de `source_prompt:` contra `repo_motor`
- checker existe pero no esta conectado al flujo de gates
- quedan terminos contradictorios en superficies del ticket
- docs venden `248b` como runtime/config OpenCode o como algo mas amplio que el
  contrato prompt/skill
