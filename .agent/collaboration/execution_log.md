# Execution Log WOT-2026-003d

**Estado:** IN_PROGRESS

## Metadata

- **ID:** WOT-2026-003d
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** EXECUTE

## Resumen

- Pipeline orquestado (FALLBACK_SIN_TASK_TOOL). RE-SCOPED tras verificacion de premisa:
  --sync ya NO re-vendoriza el bundle; el riesgo real es que el residue-prune strict borre
  `.agent/docs/` (deliverables destino-keep TRACKEADOS). Nuevo contrato: el prune nunca borra
  rutas git-trackeadas del destino; fail-safe ante incertidumbre.
- Alto blast radius + politica FALLBACK (WOT-2026-006a): cierre SOLO a READY_FOR_REVIEW.
  NO manager-approve, NO push, hasta revision independiente.

## Ejecucion Builder

- Implementacion en `repo_motor`: commit `ff05b8d` (`fix(WOT-2026-003d): never prune git-tracked destino residues`).
- `scripts/install_agent_system.py`: anadidos `_git_tracked_relpaths()` y `_filter_git_tracked_residues()`; `prune_residues()` filtra residuos git-trackeados antes del prune (strict e interactivo), con fail-safe si el estado tracked no es determinable.
- `tests/unit/test_install_agent_system.py`: anadidos tests barrera con repo git real para `.agent/docs/` trackeado + residuo untracked, y test fail-safe cuando tracked status no puede determinarse.

## Gates y evidencia real

- `python -m pytest tests/unit/test_install_agent_system.py -q -p no:cacheprovider` -> exit 0, `45 passed in 0.46s`.
- `python -m ruff check scripts/install_agent_system.py tests/unit/test_install_agent_system.py` -> exit 0, `All checks passed!`.
- `python scripts/check_encoding_guard.py scripts/install_agent_system.py tests/unit/test_install_agent_system.py` -> exit 0.
- `python scripts/run_pytest_safe.py --force-unlock` -> exit 0, `2633 passed, 19 skipped, 5 deselected in 221.81s (0:03:41)`.
- `python scripts/install_agent_system.py --sync --dry-run --dest C:\Users\fdl\Proyectos_Python\orquestador_de_agentes_workspace` -> exit 0.
  Evidencia relevante:
  - `[WARN] Destination residues detected: 1` -> `docs`
  - `[SKIP] residue is git-tracked (destino-keep), not pruning: .agent/docs`
  - ya NO aparece `Residues selected for cleanup (automatic (strict)): 1 -> docs`

## Resultado

- Riesgo original corregido: `--sync` strict sigue detectando `.agent/docs/` como residuo, pero ya no lo selecciona ni lo prunea si esta trackeado.
- El prune de residuos untracked sigue activo; el fail-safe bloquea el borrado si no se puede determinar el estado tracked.
- Ticket listo para `READY_FOR_REVIEW`, pendiente de revision independiente adversarial.
