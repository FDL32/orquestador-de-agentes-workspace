# Plan de Trabajo: WOT-2026-014g

> Fuente canonica unica del ticket (packet oficial).

## Metadata
- **ID:** WOT-2026-014g
- **Estado:** COMPLETED
- **Titulo:** Alinear name frontmatter == nombre de carpeta en 6 skills y anadir gate name==dir en discovery
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Prioridad:** Media
- **Depende de:** -
- **Objective-Link:** OBJ-014G-001
- **Plan-Link:** PLAN-014G-001
- **Builder clarification budget:** 0

## Objetivo
Hacer que el campo name del frontmatter sea identico al nombre de la carpeta (kebab largo) en las 6
skills desalineadas, verificar que el titulo del cuerpo ya coincide (no cambiarlo si ya coincide), y
anadir en scripts/discover_skills.py (_check_skill_names) una regla de gate que falle cuando
name != skill_dir.name.
Verificacion del objetivo (que comando/test lo demuestra): el gate name==dir nuevo en discover_skills,
mas un test fixture mutation-verified en tests/ (skill con name != carpeta hace FALLAR el gate; al
retirar el gate ese caso pasa silenciosamente). Ver DoD.

## Premise (VERIFICADO en codigo)
6 skills con name distinto de su carpeta (verificado leyendo cada SKILL.md):
- manager-create-work-plan -> name: create-work-plan
- manager-review-implementation -> name: code-review
- manager-resolve-escalation -> name: resolve-escalation
- builder-run-quality-gates -> name: run-quality-gates
- builder-self-audit -> name: self-audit
- builder-write-deliverable -> name: write-deliverable
La resolucion NO se rompe (discover_skills keya por skill_dir.name, no por name). El dano es de
consistencia/observabilidad. No existe gate que compare name con skill_dir.name (_check_skill_names en
discover_skills.py:501 solo valida kebab-case/actor-first).

## Premise Re-check (cwd=repo_motor, solo lectura)
for d in builder-self-audit manager-review-implementation; do grep -m1 "name:" skills/$d/SKILL.md; done
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
Condicion de arranque: las 6 siguen con name distinto de carpeta; _check_skill_names no compara name con dir.

## Nota de charter (resolucion de scope, documentada)
El charter (repo_charter.md, Plan WOT-2026-008) lista el Non-Goal "No modificar scripts de discovery,
manifests, tests o documentacion del motor". Resolucion de orquestacion: ese Non-Goal se interpreta
SCOPED al plan WOT-2026-008 (convive con constraints 008a explicitas); el lote 014x es mantenimiento
posterior fuera del plan 008. Por tanto NO bloquea a 014g. Follow-up abierto: clarificar en el charter
el alcance de ese Non-Goal (deuda documental, no de este ticket).

## Decision Arquitectonica
- name del frontmatter pasa a ser igual al nombre de la carpeta en las 6 skills (kebab largo).
- El titulo H1 del cuerpo ya usa el nombre largo: VERIFICAR y NO tocar si ya coincide.
- El gate name==dir se anade en scripts/discover_skills.py dentro de _check_skill_names (donde ya vive
  la autoridad de naming), comparando el name del frontmatter con skill_dir.name y devolviendo error si difieren.
- NO se hace canonico el name corto (no se renombran carpetas, triggers ni referencias de orchestrate-pipeline).

## Files Likely Touched (relativos a repo_motor)
- skills/manager-create-work-plan/SKILL.md
- skills/manager-review-implementation/SKILL.md
- skills/manager-resolve-escalation/SKILL.md
- skills/builder-run-quality-gates/SKILL.md
- skills/builder-self-audit/SKILL.md
- skills/builder-write-deliverable/SKILL.md
- scripts/discover_skills.py
- tests/unit/test_discover_skills_name_dir.py

Aclaraciones: solo el frontmatter name cambia en las 6 skills (y el titulo solo si NO coincidiera ya).
No abrir suite paralela: un unico archivo de test nuevo para el gate.

## Read/inspect only
- scripts/check_skill_collisions.py
- bus/skill_resolver.py
- C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace\.agent\collaboration\backlog.md

## Forbidden Surfaces
- Reglas de kebab-case / actor-first (DEC-008D-001): read-only, no se tocan.
- Carpetas de las skills, triggers, y referencias cruzadas de orchestrate-pipeline: no se renombran.
- El conflicto nominal con el builtin code-review: fuera de scope (no es dispatch real).
- bus/**, runtime/**, repo_destino/.agent/** (salvo execution_log.md): prohibidos.
- nuevas dependencias: prohibidas.

## Bateria focal
python -m pytest tests/unit/test_discover_skills_name_dir.py -q
python scripts/discover_skills.py --json
python -m ruff check scripts/discover_skills.py tests/unit/test_discover_skills_name_dir.py
python .agent/agent_controller.py --validate --json --force --project-root C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace
# Cierre canonico:
python scripts/run_pytest_safe.py --level all

## Non-goals
- NO hacer canonico el name corto.
- NO tocar las reglas kebab-case / actor-first.
- NO abordar el conflicto nominal con code-review.

## CONTRACT_GAP / STOP
- Si alinear name==dir rompe alguna referencia real de dispatch (no deberia: el dispatch usa carpeta+triggers).
- Si el gate name==dir entra en conflicto con una regla existente de _check_skill_names.
- Si el titulo del cuerpo de alguna skill NO coincide ya y cambiarlo toca contenido sustantivo.
-> emitir CG-WOT-2026-014g.md y PARAR.

## DoD (binario, comandos exactos)
- [ ] las 6 skills tienen name identico al nombre de su carpeta.
- [ ] el titulo H1 del cuerpo coincide con la carpeta (verificado; sin cambios si ya coincidia).
- [ ] existe en scripts/discover_skills.py una regla (en _check_skill_names) que falla cuando name != skill_dir.name.
- [ ] BARRERA mutation-verified: un test fixture con una skill cuyo name != carpeta hace FALLAR el gate; al
  retirar el gate ese mismo caso pasa silenciosamente.
- [ ] python scripts/discover_skills.py --json -> sin errores de naming para las 6 skills alineadas.
- [ ] python -m ruff check (FLT py) -> All checks passed.
- [ ] python scripts/run_pytest_safe.py --level all -> last-run.json exit_code 0, level all, tested_commit_sha == HEAD.
- [ ] python .agent/agent_controller.py --validate --json --force --project-root <repo_destino> -> 0 errors / 0 warnings.
- [ ] la evidencia cita el SHA del commit del repo_motor.

## Handoff
Commit productivo en repo_motor (mensaje con WOT-2026-014g), suite canonica fresca al HEAD, luego
--pre-handoff + --mark-ready. No push hasta OK humano.
