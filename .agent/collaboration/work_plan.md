# Work Plan: WOT-2026-009g

> Origen: incidente de handoff de WOT-2026-008b (cerrado/publicado, motor 869b920).

## Metadata

- **ID:** WOT-2026-009g
- **Contract ID:** T-009G-001
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-008b (handoff incident origin), WOT-2026-009b (scope gate runtime)

## Objetivo

Cerrar el falso verde de handoff detectado en WOT-2026-008b: el `work_plan.md`
del ticket activo pudo llegar a READY_FOR_REVIEW sin estar commiteado, porque
ambas verificaciones de árbol limpio lo excluyen deliberadamente.

`work_plan.md` debe estar commiteado en el instante del handoff (HEAD == working
tree para esa ruta). NO es dirty genérico: es commit-state obligatorio del
contrato activo. Sin sacar `work_plan.md` de las live surfaces generales.

**Causa raíz verificada en código (2026-06-16):**
- `scripts/pre_handoff_guard.py:39` incluye `.agent/collaboration/work_plan.md`
  en `LIVE_SURFACES_REL` → excluido del dirty check.
- `.agent/motor_checkpoint.py:35` incluye la misma ruta en su propia
  `LIVE_SURFACES_REL` (lista duplicada en otro módulo).
- `_handle_mark_ready` (agent_controller.py:3006) invoca `_run_pre_handoff_guard`
  → usa la lista de `pre_handoff_guard.py`.
- `_handle_pre_handoff` (agent_controller.py:3411) verifica con
  `_build_live_surface_sets` ← `motor_checkpoint.LIVE_SURFACES_REL`.
- Resultado: DOS puertas (`--mark-ready` y `--pre-handoff` standalone), ambas
  excluyen `work_plan.md`. Cerrar solo una deja la otra como falso verde latente.

## Decision Arquitectonica

Helper compartido en `.agent/motor_checkpoint.py` (módulo común a ambas rutas):

```
assert_work_plan_committed(project_root, motor_root) -> tuple[bool, dict]
```

**El helper NO parsea git. Delega en la fuente canónica existente**
`scope_gate.get_changed_files(project_root=..., motor_root=...)`
(VERIFICADO en código, .agent/scope_gate.py:295):

- `get_changed_files` ya usa `git status --porcelain -z` y ya cubre la semántica
  completa requerida: staged, unstaged, untracked, rename (rama `R`) y deletion
  (rama genérica `changed.add(path)`). Devuelve **rutas absolutas resueltas**.
- El helper resuelve la ruta absoluta de `.agent/collaboration/work_plan.md`
  contra el git root activo y comprueba si está en el set devuelto por
  `get_changed_files`. Si está → no commiteado → `committed = False`.
- PROHIBIDO crear un parser de `git status` nuevo en `motor_checkpoint.py`.
  Existen ya dos (`scope_gate.get_changed_files`, `pre_handoff_guard
  .get_changed_files`); añadir un tercero reabre el patrón de drift que este
  ticket combate. Reutilizar `scope_gate.get_changed_files` es obligatorio.
- Retorna `(committed, diag)` con diagnóstico accionable. `diag` DEBE incluir:
  - campo `uncommitted_work_plan: true` cuando bloquea.
  - mensaje con la ruta literal `.agent/collaboration/work_plan.md`.
  - remediación: `git add .agent/collaboration/work_plan.md && git commit -m "..."`.
- `work_plan.md` PERMANECE en ambas `LIVE_SURFACES_REL` (sigue exento del
  dirty-tree genérico). El helper es una regla ADICIONAL y separada: "exento del
  dirty genérico" + "obligatoriamente commiteado al handoff" conviven en planos
  distintos.

Invocaciones (ambas puertas, sin dejar rama descubierta):
- `scripts/pre_handoff_guard.py`: llama al helper; si no commiteado → bloquea
  `--mark-ready` con exit 1 + JSON `uncommitted_work_plan: true`.
- `.agent/agent_controller.py::_handle_pre_handoff`: el check debe ejecutarse
  **una vez, después de resolver `project_root`/git_root y ANTES de estos tres
  retornos exitosos** de la función: (1) rama documentation/research/analysis,
  (2) rama motor auto-commit, (3) rama idempotent no-op. El check NO puede
  colocarse dentro de una sola rama, o la cobertura vuelve a ser parcial.
  Colocarlo en el punto común previo a los tres `return 0` listados.

Razón de no reusar solo `get_changed_files()` del guard: `_handle_pre_handoff`
no pasa por el script, usa `motor_checkpoint`. El helper debe vivir en el módulo
común y delegar en `scope_gate` para cubrir ambas puertas con una sola regla y
una sola fuente git.

## Non-goals

- NO sacar `work_plan.md` de `LIVE_SURFACES_REL` (re-rompería ciclos donde el
  runtime reescribe el plan legítimamente).
- NO unificar las dos copias de `LIVE_SURFACES_REL` (pre_handoff_guard vs
  motor_checkpoint). Es deuda real pero abre blast radius; queda anotada para
  ticket posterior, fuera de 009g.
- NO añadir el mismo check duro para STATE.md, TURN.md, execution_log.md,
  notifications.md, backlog.md (el runtime los reescribe; no son el contrato).
- NO automatizar la barrera de regresión "pre-fix falla / post-fix pasa" como
  gate. Eso es refuerzo manual del Manager en review_manager.md, posible
  follow-up doc, no parte de 009g.
- NO tocar scope de otros tickets.
- NO corregir nomenclatura WP/WT/PLAN_*; queda para WOT-2026-010a.
- El borrador `PLAN_WOT-2026-009g.md` es artefacto transicional (se renombrara
  a STRATEGY_WOT en 010a); NO es precedente canonico de nombre.

## Files Likely Touched

### repo_motor
- `.agent/motor_checkpoint.py` (helper `assert_work_plan_committed`)
- `scripts/pre_handoff_guard.py` (invocar helper, bloquear mark-ready)
- `.agent/agent_controller.py` (invocar helper en `_handle_pre_handoff`)
- `tests/test_pre_handoff_guard.py` (existente — no duplicar en tests/unit/)
- `tests/unit/test_motor_checkpoint.py` (nuevo o existente)

### Read/inspect only
- `.agent/scope_gate.py::get_changed_files` (FUENTE A REUSAR; no reimplementar)
- `.agent/agent_controller.py::_handle_mark_ready` / `_run_pre_handoff_guard`
  (confirmar ruta de invocación — VERIFICADO: mark-ready pasa por el guard)

### Manager-only
- Reproducir barrera: caso 008b (work_plan.md dirty + READY_FOR_REVIEW) →
  gate actual pasa / gate nuevo falla. Verificar en worktree, no por relato.
- Ejecutar `validate --json` final.

## Criterios Binarios

- [ ] Preflight antes de Builder: AGENT_PROJECT_ROOT, repo_motor, repo_destino,
      ticket activo y árbol destino limpio salvo artefactos esperados verificados.
- [ ] Helper `assert_work_plan_committed` existe en `motor_checkpoint.py` y
      **delega en `scope_gate.get_changed_files`** (NO parsea git directamente,
      NO crea un tercer parser de `git status`).
- [ ] `pre_handoff_guard.py` invoca el helper y bloquea `--mark-ready` con
      `uncommitted_work_plan: true` + ruta literal
      `.agent/collaboration/work_plan.md` + remediación accionable.
- [ ] `_handle_pre_handoff` invoca el helper en el punto común previo a los tres
      `return 0` (después de resolver project_root/git_root): rama
      documentation/research/analysis, rama motor auto-commit, rama idempotent
      no-op.
- [ ] `work_plan.md` SIGUE en ambas `LIVE_SURFACES_REL` (sin regresión de
      runtime: STATE/TURN/execution_log dirty NO bloquean).
- [ ] Barrera de regresión, demostrada de forma NO destructiva (fixture de repo
      git temporal o worktree; NO manipular el árbol principal): con la
      condición 008b reproducida (work_plan.md modificado vs HEAD + resto
      limpio), el comportamiento PRE-helper pasa (falso verde) y el
      POST-helper falla con `uncommitted_work_plan: true`.
- [ ] Tests del helper sobre fixture git: detecta unstaged, staged, untracked
      y deletion de `work_plan.md` (4 estados porcelain).
- [ ] Test control: work_plan.md commiteado + STATE/TURN/execution_log dirty
      → NO falla por work_plan (no-regresión de runtime).
- [ ] `ruff check .` exit 0 en repo_motor.
- [ ] Tests focales pasan con exit 0.
- [ ] `validate --json` destino 0/0 al cierre.

## Forbidden Surfaces

- `.agent/collaboration/` del motor (seed neutro).
- `privada/` y `.env`.
- `bus/state_machine.py`.
- `scripts/validate_ticket_prose.py`.
- Las dos `LIVE_SURFACES_REL` NO se fusionan ni se les quita `work_plan.md`.
- Scope de cualquier otro ticket.
