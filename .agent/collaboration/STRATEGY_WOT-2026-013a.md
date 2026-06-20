# STRATEGY_WOT-2026-013a

## Objetivo tecnico
Volver verde en aislamiento `test_approved_pending_returns_builder_implement` corrigiendo solo el fixture/driver de `tests/test_controller_integration.py` y preservando intacto el controller productivo.

## Fases
1. Baseline read-only.
   - Reejecutar `pytest -k approved_pending` y capturar el rojo exacto.
   - Releer `sandbox()`, `_run()`, `_REAL_CONTROLLER` y el uso de `cwd`/entorno.
2. Delimitar la solucion minima.
   - Preferir ejecutar el controller real apuntando al sandbox por `--project-root` o entorno, en vez de copiar el controller al sandbox.
   - Mantener `.agent/agent_controller.py` en read-only.
3. Barrera FAIL-sin/PASS-con.
   - Demostrar que el mismo test aislado falla sin el fix y pasa con el fix.
   - Mantener verde el resto del archivo de integracion.
4. Gates de cierre.
   - `pytest tests/test_controller_integration.py -q`.
   - `ruff` sobre Python tocado.
   - `python scripts/run_pytest_safe.py --level all`.
   - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`.
5. Evidencia en bitacora.
   - Registrar comando del rojo aislado, fix aplicado y barrera pre-fix/post-fix.

## Riesgos a vigilar
- Que el Builder derive a cambio productivo del controller para arreglar una deuda de test.
- Que el fix haga pasar el test aislado pero rompa los otros tests del mismo archivo.
- Que el sandbox necesite deuda arquitectonica mayor y deba salir `CONTRACT_GAP` legitimo.
