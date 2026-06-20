# execution_log.md -- WOT-2026-011b
## Metadata
- **Ticket:** WOT-2026-011b
- **Estado:** IN_PROGRESS
- **deliverable_type:** code
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-011b.
- Motivo: `011h` no se relanza porque la barrera de archivado que pedia ya existe en `scripts/pre_handoff_guard.py` y su test de regresion; `011b` sigue siendo deuda viva y no tiene contrato congelado aun.
- Contrato congelado: `T-011B-001`.
- Frontera fijada antes de Builder: `011b` endurece determinismo de tests de relaunch sobre la costura `BUILDER_START_VERIFY_TIMEOUT_SECONDS`; NO cambia semantica productiva, runner, handoff ni CI.
- Runtime bootstrap esperado para Builder: `STATE=IN_PROGRESS`, `TURN=BUILDER/IMPLEMENT`, `work_plan.md` activo en `011b`.
## Premise Re-check requerido al Builder
- Releer `bus/builder_relaunch.py` y confirmar que el env var canonico y el default `20.0` siguen presentes.
- Releer `tests/test_supervisor.py` y `tests/test_relaunch_evidence_capsule.py` para identificar la familia de relaunch afectada.
- Confirmar que `bus/supervisor.py` permanece read-only salvo evidencia contraria.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de empezar la implementacion.
## Restriccion cross-ticket
- `011b` no reabre `011e`, `011i` ni `010m`; no toca `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` ni la politica de cierre canonico.
- Si el seam real del timeout cae fuera de `bus/builder_relaunch.py` / `tests/test_supervisor.py`, el ticket para con `CG-WOT-2026-011b.md`.

## BUILDER - WOT-2026-011b - Relaunch timeout determinism

### Fase 0 - Premisa VERIFICADA
- Seam confirmado en bus/builder_relaunch.py: _BUILDER_START_VERIFY_TIMEOUT_ENV (L29), _BUILDER_START_VERIFY_TIMEOUT_DEFAULT=20.0 (L30), _get_verify_timeout() (L168), _verify_builder_start() (L180, bucle while time.time()<deadline + sleep(0.5)).
- Causa raiz medida (durations): EXACTAMENTE 2 tests pagan ~20s c/u via _verify_builder_start sin fijar el env:
  test_relaunch_uses_resume_flag (20.41s) y test_relaunch_seam_allows_monkeypatch_without_pytest_check (20.25s).
  El resto del subset relaunch corre en ms. Subset completo: 41s. Coincide con la premisa del contrato ("2 tests x 20s").
- bus/supervisor.py read-only confirmado (no requiere cambio).

### Fase 1 - Seam determinista (cambio minimo)
- monkeypatch.setenv("BUILDER_START_VERIFY_TIMEOUT_SECONDS","0.5") anadido a los 2 tests lentos. Reutiliza el seam canonico; NO toca el default productivo (sigue 20.0) ni bus/builder_relaunch.py.
- Efecto medido: cada test 20.4s -> 0.52s. Subset relaunch completo 41s -> 1.48s (28x).
- DECISION CEM: builder_relaunch.py NO se toca pese a estar en FLT. El seam ya existe y funciona; el contrato dice "reutilizar, no inventar segundo mecanismo". Tocar el productivo seria cambio innecesario. Cambio acotado a tests/test_supervisor.py.

### Fase 2 - Barreras (4 nuevas en test_supervisor.py)
- test_verify_timeout_seam_reads_env_var: el env override funciona.
- test_verify_timeout_default_preserved: sin env -> 20.0 (default productivo intacto).
- test_verify_timeout_invalid_env_falls_back_to_default: valores malos -> default, sin crash.
- test_verify_builder_start_bounded_by_env_not_host_default: el verify retorna <5s con env=0.5 (no paga el default de 20s).
- FAIL-sin/PASS-con: sin env -> _get_verify_timeout()=20.0 (el bucle pagaria 20s, medido en Fase 0); con env=0.5 -> los 2 tests pasan en 1.13s. Rutas builder_started_verified y builder_launch_unverified siguen cubiertas (semantica intacta).

### Gates
- Tests focales: `uv run python -m pytest tests/test_supervisor.py -k relaunch` -> 18 passed in 1.48s (+ 4 barreras = 22 passed).
- Ruff: All checks passed! | Ruff format: 2 files already formatted | Encoding: exit 0.
