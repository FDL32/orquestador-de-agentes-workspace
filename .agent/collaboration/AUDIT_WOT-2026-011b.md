# AUDIT_WOT-2026-011b

## Preguntas binarias de auditoria
- [ ] El diff mantiene `_BUILDER_START_VERIFY_TIMEOUT_DEFAULT = 20.0` y el env var canonico salvo refactor semantico neutro.
- [ ] Existe evidencia literal de que las pruebas temporizadas fijan explicitamente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` o una costura equivalente determinista.
- [ ] Hay al menos una barrera FAIL-sin/PASS-con que demuestra que la ruta temporizada deja de depender del timeout default del host.
- [ ] Las rutas `builder_started_verified` y `builder_launch_unverified` siguen cubiertas y su semantica observable no cambia.
- [ ] `ruff`, tests focales, `python scripts/run_pytest_safe.py --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- [ ] No se tocaron `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py`, CI/workflows ni el bus manualmente.

## Evidencia minima esperada
- Diff de `bus/builder_relaunch.py` y/o `tests/test_supervisor.py`.
- Salida literal de las gates ejecutadas.
- Nota en `execution_log.md` indicando seam usado y barrera FAIL-sin/PASS-con.
- Si aplica, `CG-WOT-2026-011b.md` con causa exacta y superficies que fuerzan el bloqueo.
