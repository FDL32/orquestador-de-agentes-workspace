# work_plan.md -- WOT-2026-013f
## Metadata
- **ID:** WOT-2026-013f
- **Contract ID:** T-013F-001
- **Estado:** APPROVED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** code
- **Builder clarification budget:** 0
- **delivery_authority:** repo_motor
- **repo_motor:** <repo_motor>
- **repo_destino:** <repo_destino> (resuelto por --project-root / AGENT_PROJECT_ROOT)
## Objetivo
Retirar del motor `tests/deprecated/`, que hoy solo contiene tests Goose ya deprecados y excluidos del runner, dejando una justificacion durable del retiro en `tests/integration/RETIRED_TESTS.md` sin tocar el runner, otras familias legacy ni producto vivo.
## Non-goals
- No tocar `pytest.ini`, `scripts/run_pytest_safe.py` ni la politica del runner.
- No tocar `scripts/cleanup_legacy.py`.
- No tocar `tests/test_goose_native_skill.py` ni `tests/unit/test_ejemplo.py`.
- No mezclar el ticket con `013g` ni con follow-ups legacy adyacentes.
- No tocar CI/workflows ni producto fuera de `tests/deprecated/` y `tests/integration/RETIRED_TESTS.md`.
## Premisas verificadas antes de Builder
- `pytest.ini` excluye `tests/deprecated` via `norecursedirs`, asi que hoy esos archivos no se recolectan.
- `tests/deprecated/test_goose_triggers.py` y `tests/deprecated/test_goose_realworld.py` siguen marcados `DEPRECATED (WT-2026-254a)`.
- `013e` ya clasifico esta poda como follow-up pequeno y de bajo riesgo; no reabre runner, CI ni producto.
- `scripts/cleanup_legacy.py` menciona el antiguo `scripts/test_goose_realworld.py`, no el directorio `tests/deprecated/` que entra en scope aqui.
- `validate --json --project-root <repo_destino>` estaba en 0 errors / 0 warnings antes del bootstrap de `013f`.
## Decision Arquitectonica
`013f` es un ticket de `code` con blast radius minimo: la accion productiva es borrar tests ya excluidos del runner y registrar su retiro en el ledger canonico de tests retirados. La barrera real del ticket no es crear cobertura nueva, sino demostrar que la poda no cambia la recoleccion canonica ni fuerza tocar el runner o consumidores vivos.
## Files Likely Touched
### repo_motor
- tests/deprecated/
- tests/integration/RETIRED_TESTS.md
### repo_destino
- .agent/collaboration/execution_log.md
## Read/inspect only
- pytest.ini
- docs/test_performance/test_suite_audit_WOT-2026-013e.md
- scripts/cleanup_legacy.py
- tests/unit/test_cleanup_legacy.py
- tests/test_goose_native_skill.py
- tests/unit/test_ejemplo.py
## Forbidden Surfaces
- pytest.ini
- scripts/run_pytest_safe.py
- scripts/cleanup_legacy.py
- docs/test_performance/test_suite_audit_WOT-2026-013e.md
- tests/test_goose_native_skill.py
- tests/unit/test_ejemplo.py
- CI/workflows
- cualquier codigo de producto fuera de `tests/deprecated/` y `tests/integration/RETIRED_TESTS.md`
- privada/
- .env
- eventos del bus escritos manualmente
## Criterios binarios
- El diff productivo del motor se limita a borrar `tests/deprecated/` y documentar el retiro en `tests/integration/RETIRED_TESTS.md`.
- `python -m pytest tests --collect-only -q -p no:cacheprovider` mantiene 3111 tests tras la poda, y `execution_log.md` registra el conteo pre y post.
- `tests/integration/RETIRED_TESTS.md` deja explicito que los tests retirados cubrian Goose, subsistema deprecado por `WT-2026-254a`, ya excluido del runner.
- `python scripts/run_pytest_safe.py --level all` termina verde y la evidencia canonica final reconcilia `tested_commit_sha == HEAD`.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- No se tocan `pytest.ini`, runner, CI, `test_goose_native_skill.py`, `test_ejemplo` ni producto vivo.
## STOP conditions
- Parar si `tests/deprecated/` resulta ser fuente viva para algun consumidor canonico.
- Parar si el collect-only post-poda ya no da 3111.
- Parar si la unica salida verde exige tocar `pytest.ini`, `scripts/run_pytest_safe.py` o codigo fuera de las superficies declaradas.
## CONTRACT_GAP
Emitir `CG-WOT-2026-013f.md` si aparece un consumidor vivo de `tests/deprecated/`, si el borrado cambia el conteo recolectado, o si la justificacion del retiro exige tocar runner/producto o mezclar otros candidatos legacy.
