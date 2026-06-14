# Work Plan: WOT-2026-003e - gates-dispatch: manejar destino sin tests locales

## Metadata
- **ID:** WOT-2026-003e
- **Estado:** APPROVED
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor (orquestador_de_agentes)
- **Titulo:** `run_gates_dispatch` detecta 'sin tests locales' y salta pytest auditablemente en vez de fallar exit 4
- **Asignado a:** Builder
- **Severidad:** Baja | **Riesgo:** Bajo (cambio acotado en dispatcher; reversible via git)
- **Depende de:** WOT-2026-002c (completed)
- **Alias historico:** MOTOR-FU-002
- **Origen:** session-2026-06-13-host-extends (hallazgo WOT-2026-002a)

## Decision Arquitectonica
Tras A2d el destino host-extends no tiene `tests/` local, asi que el target por defecto
de `run_pytest_safe` (`tests/`) no existe y pytest da exit 4 (usage error). El dispatcher
lo propaga como fallo de gate aunque no hay nada que testear localmente. Se elige DETECTAR
ausencia de tests locales y SALTAR pytest de forma auditable (log explicito), en vez de (a)
apuntar a `<motor>/tests` (correr la suite del motor no valida el codigo del destino y es
ruido) o (b) tragar cualquier exit code de pytest (ocultaria fallos reales). El skip solo
ocurre cuando NO hay tests locales; con tests presentes el gate corre igual que hoy. El CI
ya pivoto a validate-state (WOT-AUDIT-CI); este fix alinea el dispatch local.

## Bug confirmado (recon)
`scripts/run_gates_dispatch.py::run_code_gates` (lineas 82-88): corre
`scripts/run_pytest_safe.py` y `if rc_pytest != 0: return rc_pytest`. `run_pytest_safe`
devuelve el exit code crudo de pytest; con `tests/` ausente pytest devuelve 4.

## Files Likely Touched (repo_motor)
scripts/run_gates_dispatch.py
tests/unit/test_run_gates_dispatch.py

## Read/inspect only
- `scripts/run_pytest_safe.py` (semantica de exit code / default target `tests/`).
- `runtime/project_root.py` (resolucion de PROJECT_ROOT).

## Manager-only
- Revision: confirmar que el skip SOLO ocurre sin tests locales; con tests presentes el
  gate corre y un fallo real sigue propagandose. Barrera de test de `has_local_tests`.

## Non-goals
- NO cambiar `run_pytest_safe.py` ni su exit code.
- NO tragar exit codes de pytest cuando SI hay tests.
- NO apuntar el destino a `<motor>/tests`.
- NO añadir dependencias.

## Criterios binarios de cierre
- [ ] `has_local_tests(root)` helper testeable: False sin `tests/` o con `tests/` sin
      archivos `test_*.py`/`*_test.py`; True con al menos uno.
- [ ] `run_code_gates` salta pytest con log auditable cuando `has_local_tests` es False, y
      continua (no devuelve exit 4); corre pytest normalmente cuando es True.
- [ ] Test nuevo de barrera para `has_local_tests` (sin tests / con tests / dir vacio).
- [ ] `ruff check`+`format --check` limpio; `run_pytest_safe` del motor verde.
- [ ] `validate --project-root .` (destino) 0 errores.
- [ ] Commit en repo_motor con WOT-2026-003e.

## STOP / escalado
- Si detectar 'sin tests' requiere ejecutar pytest --collect-only (acopla a pytest), preferir
  deteccion estructural por filesystem (existencia de tests/ + archivos test_*).
- Si el skip pudiera ocultar un fallo real de un destino CON tests, parar: el skip debe ser
  imposible cuando hay tests locales.

## Gates (deliverable_type: code)
- `ruff check scripts/run_gates_dispatch.py tests/unit/test_run_gates_dispatch.py` + `ruff format --check`.
- `python scripts/run_pytest_safe.py` (cwd=motor).
- `agent_controller --validate --project-root .` (destino) 0 errores.
- `check_motor_pristine --check` vs snapshot.

## Entregables
- `run_gates_dispatch.py` con `has_local_tests()` + skip auditable.
- Test de barrera en `tests/unit/test_run_gates_dispatch.py`.
- `orchestrator_pipeline/reports/closeout_WOT-2026-003e.md`.
