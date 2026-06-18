# execution_log.md -- WOT-2026-008d

**Estado:** READY_FOR_REVIEW

## Fase 0 -- Preflight Manager

- work_plan.md creado para WOT-2026-008d desde T-008D-001.
- STRATEGY_WOT-2026-008d.md y AUDIT_WOT-2026-008d.md creados.
- Criterio de baseline de paridad anadido al contrato: --check-contract, check_skill_collisions.py y discover_skills.py --json antes/despues del piloto.
- STATE.md ya apunta a WOT-2026-008d / IN_PROGRESS por bootstrap previo; no re-ejecutar bootstrap.
- Pendiente de Builder: diagnostico Fase 0, DEC primero, gate --check-naming, integracion run_gates_dispatch y piloto reversible si la DEC lo autoriza.
## Builder Fase 0 - Diagnostico + baseline (2026-06-18)

- Preflight verde: validate --json 0 errors / 0 warnings; STATE=008d/IN_PROGRESS; TURN=BUILDER/IMPLEMENT.
- Baseline pre-cambio (comandos + exit codes):
  - discover_skills.py --check-contract -> EXIT 0.
  - check_skill_collisions.py -> EXIT 0 ("OK: no skill name or trigger collisions").
  - discover_skills.py --json -> 29 skills, 90 triggers, trigger_map 90 keys (snapshot capturado, luego limpiado).
  - discover_skills.py --check-naming -> flag NO existe aun (corre discovery default). Confirmado deliverable, no premisa.
- Seams: run_gates_dispatch.py ya invoca --check-contract como barrera incondicional (L157-165); --check-naming se integra con el mismo patron justo despues. discover_skills.py es dueno de discovery+frontmatter.
- Estado real en disco: 20 prompts snake_case, 29 skills kebab-case (bui-/man-), scripts CLI verbo-primero. Unica excepcion noun_verb: prompts/review_manager.md con 6 consumidores source_prompt/prose vivos (audit-pipeline, man-review-implementation, orchestrate-pipeline SKILLs + audit_complete_motor_destination, audit_pipeline, orchestrator_pipeline prompts).
- Decision CEM: renombrar review_manager excede el piloto minimo reversible (6 updates atomicas). Diferido a 008e; piloto de 008d = validacion-only. Documentado en DEC.

## Builder Fase 1 - Implementacion (DEC primero)

1. DEC creada antes de cualquier codigo: docs/decisions/DEC-008D-001-naming-convention.md (DECIDED). Fija prompts snake_case, skills kebab-case, scripts CLI verbo-primero; prefijos de rol actor-primero (manager_review no review_manager); contrato shim/frontmatter via legacy_aliases: sin sidecar/manifest (coherente con DEC-008B-001 Opcion 4); canonical_name derivado del filename, naming_status derivado; ortogonalidad total con disable-model-invocation (010s); autoridad = discover_skills.py --check-naming; check_skill_collisions.py READ-ONLY; piloto validacion-only con review_manager como excepcion legacy y rename atomico asignado a 008e.
2. scripts/discover_skills.py: anadido check_naming() + helpers _check_prompt_names/_check_skill_names, _check_naming() CLI, regex _PROMPT_NAME_RE/_SKILL_NAME_RE, KNOWN_LEGACY_NAMES={"review_manager"}. Dispatch --check-naming en main() junto a --check-contract.
3. scripts/run_gates_dispatch.py: anadida barrera --check-naming tras --check-contract, fail-closed, independiente de deliverable_type.
4. NO se toca check_skill_collisions.py (read-only por DEC), NO pre_handoff_guard.py (Forbidden), NO renames, NO registry.json, NO bus.

## Builder Fase 2 - Tests + Gates

- tests/test_check_naming.py (NUEVO): fixtures de arbol aislado en disco (sin mocks). Cubre arbol conforme limpio, _shared/no-.md skipped, fail-closed nombre skill malo, fail-closed prompt malo, multiples violaciones, excepcion legacy tolerada, CLI exit 0 en arbol real, dirs ausentes = limpio.
- tests/unit/test_run_gates_dispatch.py: test_dispatch_wires_check_naming_barrier (source-level) + test_dispatch_propagates_naming_failure (behavioral: naming falla -> main()==1; orden naming > contract verificado).
- Focal: pytest test_check_naming.py test_run_gates_dispatch.py test_discover_skills.py test_registry_catalog.py -q -> 67 passed.
- Fail-closed en vivo: inyectado skills/Bad_Name/ -> --check-naming EXIT 1 con diagnostico; retirado -> EXIT 0.
- ruff All checks passed (tras refactor C901: check_naming dividido en 2 helpers); ruff format unchanged; encoding guard EXIT 0.

## Paridad pre/post (criterio binario)

- discover_skills.py --json: byte-identico pre vs post (diff -> PARITY OK). El gate no introduce side-effects en discovery.
- --check-contract EXIT 0; check_skill_collisions.py EXIT 0 (archivo intacto); --check-index en sync.

## INDEX / naming metadata

- Criterio "INDEX expone canonical_name/legacy_aliases/naming_status SI APLICA": NO aplica en 008d. Piloto validacion-only, sin renames ni legacy_aliases: en frontmatter -> sin metadata de naming nueva que proyectar. La proyeccion se materializa en 008e con el primer rename. Deuda con criterio de salida en la DEC.

## Builder - Manager CHANGES resueltos (2026-06-18)

Manager review veredicto CHANGES, 2 blockers. Ambos corregidos:

### Blocker 1 (ALTO) - suite stale contra HEAD
- Causa raiz: la primera suite corrio ANTES del commit productivo, asi que
  last-run.json registraba 67c2dcc (commit de 008c), no el de 008d.
- Fix: commit del CHANGES-fix primero (af1359f), luego re-run.
- Evidencia: `run_pytest_safe --level all` -> **2965 passed, 20 skipped, 0 failed**
  (333s); last-run.json tested_commit_sha = af1359f == HEAD. Verificado.

### Blocker 2 (ALTO) - --check-naming no enforzaba actor-first
- Causa raiz: el gate solo validaba forma lexica (snake/kebab). review_manager
  ES snake_case valido, asi que devolvia [] y la regla central de la DEC
  (actor-first) nunca se aplicaba; KNOWN_LEGACY_NAMES enmascaraba una regla
  inexistente.
- Fix: anadido `_actor_order_violation` en discover_skills.py. Dispara SOLO
  cuando coexisten un actor de pipeline (manager/builder) y una accion de
  pipeline (review/implement/create/plan/audit/resolve/approve) en orden
  actor-ultimo. review_manager ahora se DETECTA como violacion y se tolera via
  KNOWN_LEGACY_NAMES como deuda declarada (no como conformidad silenciosa).
- Barrera verificada: test `test_legacy_tolerance_masks_a_real_detection`
  vacia el set legacy y confirma que la violacion re-emerge. Test fail-closed
  para nuevo caso actor-ultimo (review_builder/approve_manager).
- Anti over-matching (AP-16): durante el fix se detecto que `refactor-manager`
  (manager = sustantivo nucleo, sin accion de pipeline) y `launch_builder`
  (launch = verbo del orquestador, no accion del actor) NO deben marcarse. La
  regla se acoto a acciones de pipeline para no tocarlos. Live tree verde.

### Sugerencia no bloqueante - aplicada
- DEC seccion 2 aclarada: `launch_builder` queda conforme porque `launch` no es
  accion de pipeline, NO como excepcion historica a actor-first. Alcance preciso
  de la regla documentado (head-noun y verbo-orquestador excluidos).

### Gates post-fix
- Focal: 74 passed (+7 actor-first). ruff/format/encoding limpios.
- Paridad: discover --json 29 skills / 90 triggers (sin cambio). --check-contract,
  --check-naming, --check-index, check_skill_collisions todos EXIT 0.
- Commit productivo: af1359f. Re-handoff abajo.
