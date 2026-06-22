# AUDIT_WOT-2026-013i -- Criterios de auditoria del ticket

> Checklist verificable que el Manager debe cruzar en review.
> Espejo de los criterios binarios de `work_plan.md`.

## Contrato estructural

- [ ] El ticket sigue acotado a harness/tests y no deriva a producto, runner, CI o xdist.
- [ ] El diff productivo se limita a `tests/conftest.py` y barreras declaradas.
- [ ] `tests/unit/test_detect_version.py`, `tests/unit/test_no_inline_ticket_regex.py`, `scripts/project_scanner.py` y `agent_system/scripts/project_paths.py` permanecen read-only.

## Evidencia minima

- [ ] Existe una medicion before/after comparable en el mismo host con comandos exactos.
- [ ] `execution_log.md` separa claramente coste de setup/purge frente a coste del cuerpo del test.
- [ ] Existe evidencia de que no quedan residuos operativos peligrosos en `tests/sandbox/test_runtime/`.

## Calidad del fix

- [ ] El cambio reduce o acota la latencia del purge sin mover la deuda a una limpieza manual o externa.
- [ ] Hay al menos una barrera de regresion sobre la nueva semantica de `tests/conftest.py`.
- [ ] La cura de producto de `013d` y la politica xdist/default siguen intactas.

## Gates de cierre

- [ ] `python -m pytest tests/unit/test_project_scanner.py tests/unit/test_windows_safe_temp_runtime.py -q -p no:cacheprovider` termina verde.
- [ ] El triple xdist heredado termina verde en 3 corridas consecutivas.
- [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
- [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.

## Anti-patrones a rechazar (Manager)

- Fix que solo parece rapido porque mide con sandbox ya limpio y no registra el estado previo.
- Cambio que deja residuos y confia en limpieza manual fuera del harness.
- "Mejora" que en realidad reabre producto, runner, CI o la politica xdist/default.
