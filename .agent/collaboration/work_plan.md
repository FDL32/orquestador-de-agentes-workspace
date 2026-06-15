# Work Plan: WOT-2026-009a

## Metadata

- **ID:** WOT-2026-009a
- **Contract ID:** T-009A-001
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-008a (COMPLETED)

## Objetivo

Bloquear mecanicamente el arranque de Builder si el contrato del ticket no valida
limpio en modo equivalente al handoff. El gate debe respetar `deliverable_type` y
aceptar las superficies documentales canonicas (`Builder`, `Read/inspect only`,
`Manager-only`) en tickets `analysis`, `documentation` y `research` sin producir
warnings spurios.

Root cause del WOT-2026-008a: `scope_gate.parse_files_likely_touched` busca
`## Files Likely Touched` literalmente; tickets documentales usan `## Builder` /
`## Read/inspect only` / `## Manager-only` en su lugar, devolviendo whitelist vacia
-> warning `No Files Likely Touched section in work_plan.md` solo visible en
handoff, cuando ya es tarde.

## Non-goals

- No introducir el estado `READY_FOR_BUILDER` en la state machine (statechange
  amplia; diferida a ticket posterior si se necesita).
- No relajar warnings globalmente.
- No crear override Markdown; el override es evento auditable del bus.

## Files Likely Touched

> Nota: delivery_authority=repo_motor. Los archivos a continuacion son rutas del
> repo_motor (commit 440e878). El scope gate del destino no puede resolver estas
> rutas; el validate del motor pasa 0/0 y es el gate autoritativo para este ticket.

- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/work_plan.md`

## Decision Arquitectonica

El cambio mas localizado y fail-safe es extender `parse_files_likely_touched` para
aceptar un `deliverable_type` opcional: cuando vale `analysis/documentation/research`
y no existe `## Files Likely Touched`, parsear `## Builder` como la lista de archivos
declarados del Builder. Esto hace que `check_scope_gate` reciba una whitelist real,
no vacia, y pueda verificar cobertura real en lugar de emitir el warning spurio.

El preflight en el pipeline (documentado en `orchestrator_pipeline.md`) debe correr
`--validate --json --project-root <destino>` antes de lanzar Builder y fallar si hay
errors o warnings no aceptados por el contrato del ticket.

## Implementacion

### Paso 1: `.agent/scope_gate.py`

Extender la firma de `parse_files_likely_touched`:

```python
def parse_files_likely_touched(
    work_plan_content: str,
    *,
    project_root: Path,
    deliverable_type: str = "code",
) -> set[str]:
```

Logica adicional: si `deliverable_type in {"analysis", "documentation", "research"}`
y la busqueda de `## Files Likely Touched` devuelve conjunto vacio, intentar parsear
`## Builder` con la misma logica de extraccion de paths. La seccion `## Builder`
termina en el siguiente heading `## ` igual que `## Files Likely Touched`.

Extender `check_scope_gate` para aceptar y pasar `deliverable_type`:

```python
def check_scope_gate(
    work_plan_content: str,
    changed_files: set[str] | None,
    exclude_files: set[str],
    *,
    parse_files_likely_touched_fn,
    deliverable_type: str = "code",
) -> dict:
```

### Paso 2: `.agent/agent_controller.py`

En los wrappers `parse_files_likely_touched` y `check_scope_gate`, leer
`deliverable_type` del `work_plan_content` y pasarlo a scope_gate.

### Paso 3: `prompts/orchestrator_pipeline.md`

Anadir seccion de preflight gate antes de lanzar Builder. El orquestador debe
correr `--validate --json --project-root <destino>` y verificar `errors == 0` y
`warnings == {}` antes de materializar TURN.md con `ROL=BUILDER`. Si falla, el
pipeline se detiene con `PIPELINE_BLOCKED` y el plan necesita correccion.

### Paso 4: `prompts/launch_builder.md`

Anadir nota: el Builder arranca solo si el preflight de validate paso 0/0; si
llego aqui con warnings pendientes, detener y reportar al Orquestador.

## Tests (tests/unit/test_scope_gate_deliverable_aware.py)

- **Negativo A:** `analysis` sin `## Files Likely Touched` ni `## Builder` ->
  warning `No Files Likely Touched section`, no bloqueo (backward compat).
- **Positivo A:** `analysis` con `## Builder` que lista `.agent/docs/foo.md` ->
  whitelist contiene la ruta; sin warning cuando esa ruta aparece en diff.
- **Positivo B:** `code` con `## Builder` pero sin `## Files Likely Touched` ->
  NO parsea `## Builder` (solo para doc types); sigue devolviendo vacio y warning.
- **Positivo C:** `analysis` con `## Files Likely Touched` (legacy) ->
  comportamiento sin cambio, usa FLT.

## Criterios Binarios

- [ ] Test negativo: `analysis` sin superficies Builder falla con warning backward compat.
- [ ] Test positivo A: `analysis` con `## Builder: - .agent/docs/foo.md` -> whitelist
      contiene la ruta y check_scope_gate no emite warning si el archivo esta en diff.
- [ ] Test positivo B: `code` con `## Builder` NO parsea la seccion.
- [ ] Test positivo C: `analysis` con `## Files Likely Touched` -> comportamiento intacto.
- [ ] `ruff check .` exit 0.
- [ ] `python scripts/run_pytest_safe.py` exit 0.
- [ ] `python .agent/agent_controller.py --validate --json --project-root
      C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` exit 0, 0/0.
- [ ] `orchestrator_pipeline.md` documenta el preflight gate con comando ejecutable.
- [ ] Motor `git status --short` vacio despues del commit.
- [ ] Commit referencia WOT-2026-009a en el motor.

## STOP conditions

- Si cambiar la firma de `parse_files_likely_touched` rompe tests existentes de
  forma no trivial, parar y reevaluar alcance.
- No tocar state machine ni `TicketState` en este ticket.
- No crear archivo de override Markdown.
- No relajar el warning para `code/mixed`.

## Forbidden Surfaces

- `.agent/collaboration/` del motor (seed neutro).
- `privada/` y `.env`.
- `bus/state_machine.py` (no tocar TicketState en este ticket).
- `events.jsonl` editado a mano.
