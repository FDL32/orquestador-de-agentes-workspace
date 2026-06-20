# execution_log.md -- WOT-2026-011e
## Metadata
- **Ticket:** WOT-2026-011e
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-011e.
- Motivo: tras cerrar `012b`, el siguiente paso real pendiente es habilitar un camino local y medido de xdist sin tocar CI ni el default del runner.
- Contrato congelado: `T-011E-001`.
- Frontera fijada antes de Builder: `011e` = local opt-in; `010m` = CI; `011i` = posible default futuro solo si este ticket sale estable.
- Runtime bootstrap esperado para Builder: `STATE=IN_PROGRESS`, `TURN=BUILDER/IMPLEMENT`, `work_plan.md` activo en `011e`.
## Premise Re-check requerido al Builder
- Confirmar que `pyproject.toml` aun no declara `pytest-xdist` y que `run_pytest_safe.py` no expone hoy un flag de paralelizacion.
- Releer `scripts/pre_handoff_guard.py` y preservar intacta la exigencia de `level=all` + `args_mode=default_discovery` para handoff.
- Confirmar la frontera `011e <-> 010m <-> 011i` antes de tocar el runner.
- Elegir un subset unitario explicito y reproducible para la medicion serial-vs-xdist en este host.
## Restriccion cross-ticket
- `011e` no toca CI, no toca `run_gates_dispatch.py`, no toca `pre_handoff_guard.py` y no cambia el default del runner.
- Si el opt-in local no puede mantenerse dentro de esa frontera, el ticket para con `CG-WOT-2026-011e.md`.
## BUILDER - WOT-2026-011e - pytest-xdist opt-in con medicion

### Fase 0 - Diagnostico (VERIFICADO)
- pytest-xdist ausente de pyproject/uv.lock antes del ticket.
- run_pytest_safe.py soporta --level unit|integration|all + --select-from-diff, sin flag xdist.
- pre_handoff_guard.py exige level=all + args_mode=default_discovery (NO tocado).
- Frontera 011e(local opt-in) / 010m(CI) / 011i(default futuro) respetada.

### Fase 1 - Implementacion
- pytest-xdist>=3.6 anadido a [dependency-groups].dev via `uv add --dev`; instalado 3.8.0 (+execnet 2.1.2); uv.lock actualizado.
- Flag opt-in --xdist-workers <N|auto> en run_pytest_safe.py. resolve_xdist() habilita xdist SOLO si level==unit AND args_mode==default_discovery; auto = min(8, max(2, cpu//2)). Fuera de ese contrato -> serial con fallback_reason auditable. Inyecta `-n <N>` solo cuando habilitado.
- Metadata en last-run.json: xdist={requested,requested_value,enabled,workers,fallback_reason}.
- Rutas verificadas (--dry-run): sin flag->serial(not_requested); auto+unit->-n 8 enabled; auto+--level all->serial fallback "xdist only for level=unit"; valor invalido->serial fallback. El camino canonico (--level all) NUNCA paraleliza.

### Fase 2 - Tests (tests/unit/test_run_pytest_safe.py, 7 nuevos)
- enabled unit subset; explicit worker count; not-requested backward-compat; fallback level=all; fallback non-default-discovery; fallback invalid value; fallback <2 workers.
- FAIL-sin/PASS-con: revertido run_pytest_safe a HEAD -> 7 failed (resolve_xdist ausente); restaurado -> 7 passed.

### MEDICION serial vs xdist (mismo subset tests/unit, mismo host)
- NOTA entorno: xdist vive en .venv del proyecto; sys.executable bajo `uv run` = .venv/python (lo carga). Con python global, `-n` da "unrecognized arguments" (xdist no instalado ahi). El runner usa sys.executable, correcto bajo el launcher/uv.
- SERIAL (uv run, sin -n): 1276 passed, 1 skipped, 138.20s.
- XDIST -n 8: 1273 passed, **3 failed**, 16.34s (~8.5x mas rapido).
- HALLAZGO CRITICO: xdist introduce 3 flakes por estado compartido entre workers (no aislados con tmp_path):
  test_detect_version.py::test_upgrade_path_suggestion, test_project_scanner.py::test_scan_current_project,
  test_no_inline_ticket_regex.py::test_no_inline_ticket_regex. Pasan en serial, fallan en paralelo.
- CONCLUSION: la velocidad (8.5x) es real pero la suite NO es paralelo-segura aun. Esto JUSTIFICA el diseno opt-in del contrato: 011e entrega la herramienta + la medicion que DEMUESTRA que xdist NO debe ser default todavia. Activar por defecto (011i) o en CI (010m) requiere antes aislar esos 3 (y verificar 0 flakes en varias corridas) -> follow-up para 011i/010m, fuera de scope de 011e.
