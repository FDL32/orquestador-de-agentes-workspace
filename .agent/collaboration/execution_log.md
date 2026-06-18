# execution_log.md -- WOT-2026-008i

## Metadata

- **Ticket:** WOT-2026-008i
**Estado:** READY_FOR_REVIEW
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-008i`.
- Motivo: `DEC-008G-001` serializa este lote antes de `008j`; `008k` ya dejo el
  catalogo con `role` limpio y `008e/008h` ya fijaron la capa de prompts.
- Premisa verificada: `008g`, `008e`, `008h` y `008k` cerrados canonicamente.
- Decision de alcance: migracion atomica de skill dirs `man-*` -> `manager-*`
  sin aliases runtime nuevos. La compatibilidad se mide sobre triggers,
  bindings prompt<->skill y referencias operativas vivas.
- Pendiente de Builder: baseline de discovery, rename de los cuatro directorios,
  migracion de consumidores vivos, barrera anti-prose-viva y suite canonica
  contra HEAD.
## Builder Fase 0 - Diagnostico + baseline (2026-06-18)

- Preflight verde: validate 0/0; STATE=008i/IN_PROGRESS; TURN=BUILDER/008i/IMPLEMENT.
- Baseline: --check-naming/--check-contract/--check-index/collisions EXIT 0. discover --json: 29 skills, 90 triggers.
- Seams: solo man-review-implementation tiene contrato bidireccional (source_prompt + contract_id). manager_review.md:9 anchor "Skill canonica: skills/man-review-implementation/SKILL.md" -> debe migrar a manager-review-implementation o --check-contract falla. Triggers NO cambian.
- Huella: 33 archivos. NO-FLT historia/runtime/memoria/changelog/cache no se tocan (tolerados por contrato).

### CEM: consumidores operativos vivos NO declarados en FLT
- .claude/agents/manager.md: frontmatter skills: lista 3 nombres man-* + cuerpo los invoca por accion. Tras rename -> agente Manager roto.
- skills/refactor-manager/PROMPT_TEMPLATE.md:219: ref prose viva a man-review-implementation.
- DECISION: incluir ambos en la migracion. NO es CONTRACT_GAP (no resolver paralelo, no runtime-bus, no toca bui-*/triggers). El contrato exige migrar consumidores vivos; el FLT los omitio. Registrado ANTES de tocar codigo.

## Builder Fase 1/2 - Implementacion + Tests

### Fase 1
- git mv 4 dirs man-* -> manager-* (historia preservada, incl. references/).
- Anchor migrado en prompts/manager_review.md:9 -> skills/manager-review-implementation/SKILL.md (--check-contract verde).
- Self-refs internas de los dirs renombrados migradas (name:, titulos #, cross-refs entre skills hermanas). name: man-session-closeout -> manager-session-closeout (los otros 3 ya tenian name logico sin prefijo).
- Consumidores operativos migrados (FLT + 3 CEM): .claude/agents/manager.md, skills/refactor-manager/PROMPT_TEMPLATE.md, scripts/closeout_steps/observations.py:156.
- INDEX regenerado. BOM preexistente en create-agent-skill/references/frontmatter-template.md retirado (encoding guard pre-commit lo cazo).

### Fase 2
- test_check_naming.py: BARRERA TestNoLiveManSkillRefs008i (falla si sobrevive ref man-* a skill en consumidor operativo; tolerada historia/memoria/DEC/changelog/tests). Cazo en vivo la ref de closeout_steps/observations.py:156 que yo habia clasificado como tolerada -> corregida.
- test_discover_skills.py: test_manager_review_binding_after_rename actualizado a manager-review-implementation + anchor.
- test_agent_readme_references.py: ref a SKILL real -> manager-review-implementation.
- Focal: 67 passed, 4 skipped.
- Paridad: trigger_map BYTE-IDENTICO (90 triggers, 29 skills); diff JSON solo en paths derivados del rename.
- Gates: naming/contract/index/collisions EXIT 0; ruff All checks passed; format clean; encoding EXIT 0.
- Commit productivo: b230b61.
- Pendiente: suite canonica level=all contra HEAD + handoff.

### Cierre de evidencia - suite
- run_pytest_safe --level all sobre b230b61: 3013 passed, 20 skipped, 0 failed (691.73s).
- last-run.json: finished, exit_code=0, tested_commit_sha=b230b61 == HEAD.


Scope override: commit b230b61: (1) references/ internos de los 4 dirs man-*/manager-* son parte atomica del git mv declarado en FLT (el FLT lista los dirs; el parser cuenta archivos); (2) 3 consumidores vivos no-FLT (.claude/agents/manager.md, scripts/closeout_steps/observations.py, skills/refactor-manager/PROMPT_TEMPLATE.md) justificados por CEM en execution_log Fase 0 ANTES de tocarlos: el contrato exige migrar consumidores vivos operativos. No CONTRACT_GAP. Triggers byte-identicos.. Affected files: .claude/agents/manager.md, scripts/closeout_steps/observations.py, skills/man-create-work-plan/SKILL.md, skills/man-create-work-plan/references/plan-quality-checklist.md, skills/man-create-work-plan/references/plan-template.md, skills/man-create-work-plan/references/risk-guide.md, skills/man-resolve-escalation/SKILL.md, skills/man-resolve-escalation/references/escalation-levels.md, skills/man-review-implementation/SKILL.md, skills/man-review-implementation/references/review-checklist.md, skills/man-review-implementation/references/verdict-format.md, skills/man-session-closeout/SKILL.md, skills/man-session-closeout/references/closeout-lessons-format.md, skills/man-session-closeout/references/scope-taxonomy.md, skills/man-session-closeout/references/upstream-learnings-format.md, skills/manager-create-work-plan/SKILL.md, skills/manager-create-work-plan/references/plan-quality-checklist.md, skills/manager-create-work-plan/references/plan-template.md, skills/manager-create-work-plan/references/risk-guide.md, skills/manager-resolve-escalation/SKILL.md, skills/manager-resolve-escalation/references/escalation-levels.md, skills/manager-review-implementation/SKILL.md, skills/manager-review-implementation/references/review-checklist.md, skills/manager-review-implementation/references/verdict-format.md, skills/manager-session-closeout/SKILL.md, skills/manager-session-closeout/references/closeout-lessons-format.md, skills/manager-session-closeout/references/scope-taxonomy.md, skills/manager-session-closeout/references/upstream-learnings-format.md, skills/refactor-manager/PROMPT_TEMPLATE.md