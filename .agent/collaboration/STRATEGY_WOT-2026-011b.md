# STRATEGY_WOT-2026-011b

## Objetivo tecnico
Hacer determinista la familia de pruebas de relaunch que ejerce verificaciones temporizadas, reutilizando el seam existente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` y preservando el comportamiento productivo del relaunch.

## Fases
1. Baseline read-only.
   - Releer `bus/builder_relaunch.py` y `tests/test_supervisor.py`.
   - Confirmar donde vive el seam de timeout y que el default productivo sigue siendo `20.0`.
2. Delimitar el seam minimo.
   - Decidir si basta con fijar el env var dentro de los tests o si hace falta una micro-costura semantica neutra en `bus/builder_relaunch.py`.
   - Mantener `bus/supervisor.py` en read-only salvo evidencia contraria.
3. Barrera FAIL-sin/PASS-con.
   - Anadir o endurecer una prueba que falle sin fijar el timeout determinista y pase al usar la costura declarada.
   - Mantener cubiertas las rutas `builder_started_verified` y `builder_launch_unverified`.
4. Gates de cierre.
   - `pytest` focal sobre relaunch/supervisor.
   - `ruff` sobre Python tocado.
   - `python scripts/run_pytest_safe.py --level all`.
   - `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`.
5. Evidencia en bitacora.
   - Registrar en `execution_log.md` el seam usado, la barrera FAIL-sin/PASS-con y el resultado de las gates.

## Riesgos a vigilar
- Que el Builder resuelva la flaqueza con sleeps mas largos o timeouts wall-clock, en vez de con una costura determinista.
- Que el cambio derive en semantica productiva nueva o en tocar runner/handoff fuera de scope.
- Que el seam real este en otra superficie del relaunch y aparezca `CONTRACT_GAP` legitimo.
