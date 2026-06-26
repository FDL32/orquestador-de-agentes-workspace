# AUDIT_WOT-2026-013t

## Scope
- Ticket: `WOT-2026-013t`
- deliverable_type: `code`
- delivery_authority: `repo_motor`
- Objetivo auditado: deduplicar el seam de upgrade y dejar un solo owner efectivo de `UpgradeManager` sin romper la via publica `scripts/upgrade.py`.

## TP Check
- TP-01: el packet nombra superficies concretas y no deja decisiones de arquitectura abiertas al Builder.
  Verificacion esperada: FLT de 5 rutas y surfaces prohibidas acotadas al seam de upgrade.
- TP-02: cada criterio binario cita comando exacto, archivo o barrera verificable.
  Verificacion esperada: DoD anclado a pytest focal, ruff, suite canonica y validate 0/0.
- TP-03: las non-goals y forbidden surfaces impiden derivar hacia closeout, bus, runner o refactors amplios del sistema.
  Verificacion esperada: `rollback.py`, `detect_version.py`, `doctor_agent_system.py`, `ProjectPathsResolver`, bus y runtime quedan read-only salvo CONTRACT_GAP.
- TP-04: el criterio de salida distingue owner unico real, compatibilidad publica y barrera fail-sin-fix del seam de copia.
  Verificacion esperada: owner unico + import publico `scripts.upgrade` + pruebas que fallan si reaparecen dos owners o si se rompe `copytree`/`copy2` en el owner real.
- TP-05: si aparece necesidad de tocar superficies no aprobadas, el ticket escala en vez de improvisar scope.
  Verificacion esperada: STOP explicito hacia `CG-WOT-2026-013t.md`.

## Regression Focus
- La barrera principal debe FALLAR si reaparecen dos `UpgradeManager` editables o si romper `copytree`/`copy2` en el owner real deja de derribar las pruebas focales.

## Closing Rule
- No aprobar sin `run_pytest_safe --level all`, `validate --json --force --project-root <workspace_activo>` en `0 errors / 0 warnings`, y evidencia de que README + imports + tests ya no apuntan a forks divergentes.
