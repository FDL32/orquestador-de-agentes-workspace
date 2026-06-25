# Execution Log -- WOT-2026-013t

**Estado:** IN_PROGRESS

## Preparacion

- Ticket reactivado y packet canonico copiado a `work_plan.md`.
- Pendiente: bootstrap canonico del bus + arranque Builder.

## Implementacion + barreras + gates (Builder, 2026-06-25)

Decision de contrato (ya congelada en work_plan l.39): owner unico =
scripts/upgrade_agent_system.py; scripts/upgrade.py = entrypoint publico que
re-exporta. Esto resolvio los 2 BLOCKERs de la auditoria adversarial (owner
decidido + DoD item 1 coherente), asi clarification=0 es honesto.

Cambios (FLT, repo_motor):
- `scripts/upgrade.py`: reescrito como RE-EXPORT delgado del owner. Elimina su 2a
  clase editable (365 -> ~45 lineas). Re-exporta UpgradeManager, shutil, datetime,
  main del owner; conserva el CLI (`python scripts/upgrade.py` via main del owner)
  y `from scripts.upgrade import UpgradeManager`. VERIFICADO: public.UpgradeManager
  IS owner.UpgradeManager; __module__ == scripts.upgrade_agent_system; shutil/
  datetime/main re-exportados (seam de copia inequivoco, Paso 2).
- `scripts/upgrade_agent_system.py`: owner unico, sin cambios de logica (ya era el
  fork moderno con ProjectPathsResolver/DoctorAgentSystem).
- `tests/integration/test_lifecycle_integration.py`: ALINEADO al owner (Paso 3,
  FLT modificable). (a) los 2 tests COMPLETED creaban proyectos legacy sin
  manifest; el owner es manifest-first -> el de upgrade_then_rollback recibe
  manifest canonico (como los unit tests del owner) -> COMPLETED; (b)
  test_full_lifecycle_chain mantiene deteccion legacy v9.2 pero ahora asierta el
  contrato REAL del owner: upgrade legacy sin manifest -> BLOCKED ("Run migration
  first", detection_mode=legacy_markers). El viejo upgrade.py upgradeaba legacy
  laxamente; consolidar al owner elimina esa via insegura. (c)
  test_concurrent_upgrade_safety: patches repuntados de scripts.upgrade.* a
  scripts.upgrade_agent_system.* (el owner que ejecuta las copias).
- `tests/unit/test_upgrade.py`: nueva clase TestUpgradeSingleOwner (3 barreras):
  scripts.upgrade.UpgradeManager IS owner; seam re-export; upgrade.py no define
  clase propia. DoD item 4.
- `README.md`: l.104 alineado: upgrade.py = entrypoint publico, owner =
  upgrade_agent_system.py (re-export), sin 2a clase editable.

Evidencia mutation-verified:
- Reintroducir `class UpgradeManager` en upgrade.py -> 2 de 3 barreras
  TestUpgradeSingleOwner FALLAN; restaurado -> 3 passed. (DoD item 4: la barrera
  de owner unico FALLA si reaparece una 2a clase editable divergente).
- Las barreras de copia de 013r (test_backup_propagates_real_copytree_failure,
  test_backup_invokes_real_copies_count) siguen verdes sobre el owner real.

Gates:
- `ruff check` (4 archivos) -> All checks passed; `ruff format` OK.
- `check_encoding_guard.py README.md` -> exit 0.
- focal: test_upgrade.py (24) + test_lifecycle_integration.py (4) = 28 passed.
- validate + suite canonica: ver abajo. delivery_authority=repo_motor -> suite con
  INTERPRETE DEL MOTOR, sin AGENT_PROJECT_ROOT al workspace (ver
  docs/RUNNER_INTERPRETER_SEMANTICS.md).

Scope: solo los 5 archivos del FLT. Forbidden surfaces (rollback/detect_version/
doctor/project_paths, .agent/**, bus, runtime) NO tocadas. CONTRACT_GAP no aplica:
la compat publica de upgrade.py se preservo via re-export sin migracion amplia.
