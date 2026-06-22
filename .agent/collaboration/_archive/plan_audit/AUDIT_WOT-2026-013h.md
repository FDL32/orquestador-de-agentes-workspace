# AUDIT_WOT-2026-013h -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] El ticket sigue acotado a archivado/cierre y no deriva a runner, xdist, CI o producto.
- [ ] El diff productivo se limita a las superficies declaradas de archivado/cierre y sus tests.
- [ ] No hay auto-commit del archivador ni relajacion de `archive_rename_uncommitted`.

## Evidencia minima

- [ ] Existe una reproduccion con repo git real del patron `D old + ?? new`.
- [ ] Existe evidencia FAIL-sin/PASS-con sobre la ruta real corregida.
- [ ] `execution_log.md` registra comandos exactos, resultados y la decision CEM si hubo desviacion.

## Calidad del fix

- [ ] El siguiente ciclo no hereda limbo de archivado, o el mismo closeout falla cerrado antes de dejarlo.
- [ ] Se preserva la trazabilidad de `STRATEGY_` / `AUDIT_` archivados.
- [ ] `reconcile_ticket.py` sigue siendo recuperacion, no cierre normal.

## Gates de cierre

- [ ] `python -m pytest tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py -q` termina verde.
- [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.

## Anti-patrones a rechazar (Manager)

- Fix que mueve el problema a otra fase del closeout pero mantiene la herencia al ticket siguiente.
- Test verde con mocks de git/subprocess que no ejercen el limbo real.
- Solucion basada en auto-commit silencioso o en relajar el guard a pass-open.
