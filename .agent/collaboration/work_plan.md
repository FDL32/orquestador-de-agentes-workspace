# Work Plan: WOT-2026-010u

> Origen: patron repetido de archivado en limbo: `archive_collaboration_artifacts.py` mueve `STRATEGY_/AUDIT_` cerrados a `_archive/plan_audit/`, pero si el rename no queda commiteado, el siguiente ticket queda bloqueado por `contaminacion_productiva`.

## Metadata

- **ID:** WOT-2026-010u
- **Contract ID:** T-010U-001
- **Estado:** COMPLETED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010s (completed)

## Objetivo

Convertir el archivado incompleto de `STRATEGY_/AUDIT_` en una barrera temprana y accionable. El ticket debe detectar el estado `delete+untracked` que representa un rename no commiteado hacia `_archive/plan_audit/` y bloquear cierre/handoff con un diagnostico self-service. No debe hacer commits automaticos.

## Hechos verificados de arranque

- `scripts/archive_collaboration_artifacts.py` mueve archivos con `shutil.move`, sin `git add` ni commit.
- La deteccion actual existe, pero llega tarde como `contaminacion_productiva` en el siguiente validate/handoff.
- Patron repetido en la sesion: archivado previo dejo delete+untracked y bloqueo tickets posteriores.
- Decision de alcance: implementar opcion B. Guard fail-closed + remediacion explicita. NO auto-commit.

## Fase 0: Diagnostico antes del cambio

Confirmar antes de editar:

- punto exacto donde se invoca `_auto_archive_closed_artifacts()` en `agent_controller.py`;
- como `pre_handoff_guard.py` clasifica `_archive/plan_audit/` y superficies vivas;
- donde `delivery_hygiene_check.py` reporta arbol sucio/contaminacion;
- si ya existe helper reutilizable para `git status --porcelain -z` o parser de renames;
- tests existentes que cubren archiver/pre-handoff/validate.

Registrar en `execution_log.md`:

- seam elegido para la barrera;
- por que no se implementa auto-commit;
- reproduccion roja del limbo delete+untracked.

## Files Likely Touched

### repo_motor
- `scripts/archive_collaboration_artifacts.py`
- `.agent/agent_controller.py`
- `scripts/pre_handoff_guard.py`
- `scripts/delivery_hygiene_check.py`
- `tests/test_pre_handoff_guard.py`
- `tests/test_archive_collaboration_artifacts.py`
- `tests/unit/test_delivery_hygiene_check.py`
- `docs/protocol/archive_rename_hygiene_WOT-2026-010u.md`

### repo_destino
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/STRATEGY_WOT-2026-010u.md`
- `.agent/collaboration/AUDIT_WOT-2026-010u.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/backlog.md`
- `.agent/planning/ticket_contracts.md`

## Read/inspect only

- `.agent/collaboration/_archive/plan_audit/`
- `.agent/runtime/events/`
- `docs/KNOWN_FAILURE_PATTERNS.md`
- `AGENTS.md`

## Manager-only

- verificar que el guard no auto-commitea;
- verificar que no borra artefactos historicos;
- verificar que el diagnostico contiene comandos de remediacion;
- verificar test rojo/verde contra repo git real o fixture con git real.

## Decision Arquitectonica

- La barrera debe fallar temprano si detecta rename incompleto de plan/audit cerrado.
- Remediacion preferida: stage ambos lados del rename y commitear, no borrar archivos.
- No auto-commit desde archivador: evita commits sorpresa y mezcla de estado vivo con cambios del usuario.
- El guard debe ser self-service: mostrar rutas y comando exacto de reconciliacion.

## Criterios Binarios

- [ ] Existe test que reproduce `D .agent/collaboration/AUDIT_*.md` + `?? .agent/collaboration/_archive/plan_audit/AUDIT_*.md` y falla sin el fix.
- [ ] El guard bloquea el cierre/handoff/validate correspondiente con razon `archive_rename_uncommitted` o equivalente estable.
- [ ] El diagnostico lista origen, destino y comando de remediacion (`git add <old> <new> && git commit ...`).
- [ ] El fix no ejecuta `git commit` automaticamente.
- [ ] No se borran artefactos historicos; el flujo esperado preserva rename 100%.
- [ ] Tests focales pasan.
- [ ] Ruff/format pasan sobre Python tocado.
- [ ] Encoding guard pasa sobre docs y codigo tocados.
- [ ] `validate --json --project-root <repo_destino>` termina 0 errors / 0 warnings.

## Non-goals

- NO auto-commit en `archive_collaboration_artifacts.py`.
- NO borrar artefactos en vez de renombrar.
- NO editar bus runtime ni fabricar eventos.
- NO cambiar politicas de archive para `archive/` vivo de notifications.
- NO mezclar limpieza Goose ni Plan 008.

## Forbidden Surfaces

- bus runtime/events
- `privada/`
- `.env`
- dependencias (`pyproject.toml`, `uv.lock`)
- borrado destructivo de `_archive/plan_audit/`
- auto-commit automatico dentro del archivador