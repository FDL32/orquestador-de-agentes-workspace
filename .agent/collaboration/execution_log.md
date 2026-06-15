# Execution Log: WOT-2026-008a - Taxonomia prompts/skills

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-008a
- **Contract ID:** T-008A-001
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Rol activo:** BUILDER
- **Accion:** PREMISE_RECHECK_THEN_ANALYZE

## Contract Formation baseline

- repo_charter.md: OBJ-001 navegacion, OBJ-002 compatibilidad, OBJ-003 migracion.
- plan_graph.md: PLAN-001 no paralelizable con cambios de prompts/skills.
- ticket_contracts.md: T-008A-001 frozen.
- work_plan.md: derivado del contrato; cero implementacion en motor.

## Evidencia inicial del Manager

- Motor HEAD: ece7524.
- Destino HEAD: 28b24ce.
- `prompts/*.md`: 19 archivos.
- `skills/` top-level excluyendo `_shared`: 30 directorios.
- `discover_skills.py`: usa `directory.iterdir()` y `<dir>/SKILL.md`.
- `check_skill_collisions.py`: usa globs `skills/*/SKILL.md` y `.agent/skills/*/SKILL.md`.

## Pendiente del Builder

Ejecutar Premise Re-check, crear el manifiesto declarado y registrar evidencia
literal de cada gate. No modificar el repo_motor.
## Launch readiness (Manager)

- Contract validator: `OK: 3 file(s) validated, 0 errors`.
- Skill discovery contract: exit 0.
- Skill collision check: `OK: no skill name or trigger collisions`.
- Bootstrap: `STATE_CHANGED BOOTSTRAP -> IN_PROGRESS` emitido para WOT-2026-008a.
- STATE.md: `ACTIVE_TICKET: WOT-2026-008a`, `STATUS: IN_PROGRESS`.
- TURN.md: `ROL=BUILDER`, `Accion=IMPLEMENT`.
- Controller validate: exit 0, 0 errors, 0 warnings.
- Encoding guard: exit 0.
- repo_motor git status: limpio.
## CHANGES remediation before relaunch

- Motor root contamination detected from prior Builder attempt: repo_motor `.agent/docs/taxonomy_migration_WOT-2026-008a.md` and runtime events were removed/restored by Manager before relaunch.
- Contract count reconciled: prompts=19, SKILL.md=29, PROMPT_TEMPLATE.md=2, skill references=33, shared docs=3.
- DoD expanded beyond `prompts/*.md` and `skills/*/SKILL.md` to include templates, references, `_shared`, manifests, llms and tool consumers.
- Added DEC-008-004: explicit manifest/registry vs glob discovery, informed by mattpocock/skills plugin manifest pattern.
- Folder depth is now an evaluated hypothesis, not a frozen decision.
- Relaunch requirement: verify `AGENT_PROJECT_ROOT` points to repo_destino before any write.


## Builder execution (analysis) -- 2026-06-15

### Root verification (lesson from prior contaminated attempt)
- AGENT_PROJECT_ROOT: UNSET at run. Did NOT trust env; targeted repo_destino
  explicitly for the deliverable; ran validate with --project-root <destino>.
- repo_motor HEAD ece7524, git status --short EMPTY before and after (no motor
  contamination; the deliverable lives ONLY in repo_destino/.agent/docs/).

### Premise Re-check (read-only, evidence)
- Counts: prompts=19, SKILL.md=29, PROMPT_TEMPLATE.md=2, references=33, _shared=3,
  llms*.txt=2, MANIFEST.*=2.
- Flatness in code: discover_skills.py:99/297 iterdir(); check_skill_collisions.py:54
  glob("skills/*/SKILL.md"). Premise (flat) CONFIRMED; no CONTRACT_GAP.
- Runs: discover_skills --json -> total_skills=28, total_triggers=87; collision ->
  "OK: no skill name or trigger collisions".
- DISCOVERY-GAP-1: 28 discovered vs 29 on disk; man-review-implementation (name:
  code-review) is absent from discovery and trigger_map. Documented, owner=008b.
- External (gh authenticated): mattpocock/skills plugin.json (manifest-first, one
  category level, deprecated/ excluded) + OKF SPEC (markdown+frontmatter, index
  router). Pattern taken, not copied.

### Deliverable
- .agent/docs/taxonomy_migration_WOT-2026-008a.md created in repo_destino.
- Full inventory classified (sec.3), surface separation (sec.2), depth as
  hypothesis (sec.4), registry manifest-first vs glob (sec.5), single canonical
  source + shims (sec.6), DEC-008-001..006 (sec.7), follow-up tickets 008b-e
  (sec.8), risks/STOP/rollback/gates (sec.9), completeness statement (sec.10).

### Gates
- encoding guard del entregable: exit 0.
- repo_motor git status --short: EMPTY (clean).
- Reporte .agent/docs/taxonomy_migration_WOT-2026-008a.md creado. Validate destino:
  ver linea final.

### DoD
- [x] Inventario completo, ninguna ruta sin clasificar (sec.3 + sec.10).
- [x] Cada fila: ruta/API/consumidores/destino/compat/riesgo/owner.
- [x] Separadas machine-executed / contract / documentation (sec.2).
- [x] discovery/collision planos demostrado con lineas de codigo.
- [x] Profundidad como hipotesis + tradeoffs + DEC-008-004 (sec.4).
- [x] Registry manifest-first vs glob, distinguiendo API/layout/indice (sec.5).
- [x] Fuente canonica unica + shims read-only con ticket de retirada (sec.6).
- [x] Descomposicion 008b-e con dependencias (sec.8).
- [x] Riesgos/STOP/rollback/gates por fase (sec.9).
- [x] git status motor vacio.
- [x] encoding guard exit 0.
- [ ] validate destino 0/0 -> ver linea final.

**Estado:** READY_FOR_REVIEW (pendiente validate 0/0 + re-review independiente).


## Manager review #1 -> CHANGES + remediacion -- 2026-06-15

Tres hallazgos, los tres VERIFICADOS independientemente:

1. Handoff canonico incompleto: bus 008a derivaba IN_PROGRESS; no habia
   BUILDER_EXIT ni STATE_CHANGED -> READY_FOR_REVIEW. (Yo habia escrito
   "READY_FOR_REVIEW" solo en texto del log, sin evento canonico.)
   -> FIX: ejecutado --mark-ready canonico (emite BUILDER_EXIT + STATE_CHANGED);
   no se edito events.jsonl a mano.
2. Claim gh impreciso: el manifiesto decia "gh authenticated" sin mecanismo.
   Verificado: gh SI autenticado via GITHUB_TOKEN (api calls reales: mattpocock
   plugin.json, OKF SPEC). No fue falso, pero estaba under-specified.
   -> FIX: manifiesto declara el mecanismo (GITHUB_TOKEN, no gh auth login) y que
   un reviewer sin el token vera "no login" (diferencia de entorno).
3. DISCOVERY-GAP-1 causa raiz erronea: yo dije "dir != name" (hipotesis hedged).
   Causa real VERIFICADA: BOM UTF-8 en man-review-implementation/SKILL.md
   (primeros bytes EF BB BF; primer char U+FEFF). parse_frontmatter ve <BOM>---
   != --- -> NO_FRONTMATTER -> discovery omite la skill. Hipotesis dir!=name
   FALSIFICADA. Secundario: encoding_guard cubre skills/**/*.md pero el BOM paso.
   -> FIX: seccion DISCOVERY-GAP-1 corregida con causa real + scope a 008b.

Gates tras remediacion: encoding guard del entregable exit 0; repo_motor git
status --short EMPTY; validate destino 0/0 (ver linea final).

**Estado:** READY_FOR_REVIEW (handoff canonico emitido al bus; pendiente re-review).


## Validate post-handoff: 0 errors / 1 warning (clasificado)

- validate destino: errors=0, warnings=1.
- Warning unico: scope -> "No Files Likely Touched section in work_plan.md".
- Naturaleza: FALSO POSITIVO para deliverable_type=analysis. El work_plan usa la
  convencion documental de CLAUDE.md (secciones ## Builder / ## Read/inspect only /
  ## Manager-only) en vez de "Files Likely Touched" (heading propio de tickets code).
  Evidencia: work_plan.md headings = Builder(L32), Read/inspect only(L37),
  Manager-only(L48); el contrato declara superficies via esas secciones.
- Clasificacion: accepted_health_exception. Propietario: scope-gate del validador
  (no respeta deliverable_type para esta seccion) + materializacion del Manager.
- NO se edita work_plan.md (Forbidden Surface del Builder). NO se hackea para
  forzar 0/0. Se surfacea a la re-review para decision: (a) el Manager anade
  "Files Likely Touched" al work_plan, o (b) se acepta el exception documentado,
  o (c) se corrige el scope-gate para honrar analysis (ticket motor aparte).

**Estado:** READY_FOR_REVIEW (handoff canonico en bus; 1 warning clasificado).


## Manager patch: pre-review contract cleanup -- 2026-06-15

- Decision: no cerrar 008a con `accepted_health_exception` para un warning
  reparable. Se anadio una seccion minima `Files Likely Touched` al work_plan
  con las superficies reales del ticket analysis.
- Razon: el Builder debe recibir contratos que pueden cerrar 0/0; las
  excepciones quedan para warnings no reparables, no para gaps documentales.
- Follow-up registrado en backlog: WOT-2026-009a para hacer el pre-Builder
  contract gate deliverable-aware, fail-closed y auditable.


Manager approved canonical closeout for WOT-2026-008a

## Post-close audit correction -- 2026-06-15

- Una auditoria externa inicial marco 008a como `NO ACEPTAR` porque audito solo
  `repo_motor` seed. Ese veredicto queda invalidado por error de topologia:
  los claims de 008a pertenecen a `repo_destino`.
- Evidencia re-derivada en `repo_destino`: entregable presente, bus con
  `BUILDER_EXIT -> READY_FOR_REVIEW -> REVIEW_DECISION -> COMPLETED ->
  SUPERVISOR_CLOSED`, backlog con WOT-2026-009a y validate 0/0.
- Leccion CEM: antes de auditar un cierre, declarar repo auditado, HEAD, acceso
  a `repo_destino` y claims fuera de alcance. Si no hay acceso al destino, el
  veredicto correcto es `NO AUDITABLE`, no `NO ACEPTAR`.
