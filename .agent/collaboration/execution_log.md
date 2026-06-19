# execution_log.md -- WOT-2026-011a

## Metadata

- **Ticket:** WOT-2026-011a
**Estado:** READY_FOR_REVIEW
- **deliverable_type:** code
- **delivery_authority:** repo_motor

## Manager Preflight

- Ticket siguiente seleccionado: `WOT-2026-011a`.
- Motivo: el cierre de `011d` confirmo que el limbo `D old + ?? new` sigue
  pudiendo nacer en `--session-close` aunque `010u` ya lo detecta mas tarde.
- Hechos verificados antes del handoff:
  - `check_archive_rename_complete()` ya expone la razon estable
    `archive_rename_uncommitted` con remediacion exacta.
  - `pre_handoff_guard.py` ya usa esa barrera; el gap es de timing, no de
    inexistencia del detector.
  - `closeout_steps/archival.py` hoy marca `PASS` si el script de archivado
    sale `0`, aunque la post-condicion deje rename sin commit.
  - `011d` exigio reconcile manual en `repo_destino` antes de que el Manager
    pudiera confirmar `validate 0/0`.
- Pendiente de Builder:
  1. enganchar la barrera de archival limbo en la ruta real de `session-close`;
  2. convertir el hallazgo en `FAIL` bloqueante con remediacion accionable;
  3. anadir regresion test del closeout;
  4. revalidar gates y `validate 0/0`.

## Manager Bootstrap

- `WOT-2026-011d` quedo cerrado canonicamente y registrado en commit
  `c71370d` de `repo_destino`.
- Packet materializado para `WOT-2026-011a`.
- `work_plan.md`, `STRATEGY_WOT-2026-011a.md` y `AUDIT_WOT-2026-011a.md`
  alineados al mismo contrato: fail-closed en closeout, no auto-commit.
- `execution_log.md` queda reinicializado en `IN_PROGRESS` para arranque
  directo del Builder.

## BUILDER - WOT-2026-011a - Fase 0 (diagnostico)

### Seams confirmados
- scripts/closeout_steps/archival.py:step_archive_collaboration() (lineas 38-43) devuelve PASS si archive_collaboration_artifacts.py sale 0; NO verifica la post-condicion del rename. WARN solo si exit != 0. Esta es la falsa salud.
- scripts/delivery_hygiene_check.py:check_archive_rename_complete(project_root) (linea 332) es la fuente de verdad: parsea `git status --porcelain --untracked-files=all`, empareja `D` collaboration artifact con `??` copia bajo _archive/plan_audit/, y devuelve HygieneResult(passed=False, message="ARCHIVE_RENAME_UNCOMMITTED", details=[reason estable "archive_rename_uncommitted" + origen + destino + comando exacto de reconcile]). Nunca auto-commitea ni borra.
- scripts/session_closeout.py: StepResult.status admite FAIL; CloseoutReport.overall_status devuelve FAIL si algun step es FAIL (linea 151); exit code 1 si FAIL (linea 638). Un FAIL en step_archive_collaboration propaga fail-closed sin tocar machinery adicional.
- _step_archive_collaboration (session_closeout.py:412) delega en el impl de archival.py inyectando run_script_fn + step_result_cls.
- Sin riesgo de import circular: delivery_hygiene_check.py no importa session_closeout ni closeout_steps.

### Recurrencia verificada del patron
- WOT-2026-010w y WOT-2026-011d: el cierre previo dejo el rename de archivado en limbo (D collaboration/<f>.md + ?? _archive/plan_audit/<f>.md); la contaminacion (validate scope warning archive_rename_uncommitted) aparecio en el ticket siguiente y solo se corrigio con reconcile manual en repo_destino.

### Decision de diseno (cambio minimo)
- Reutilizar check_archive_rename_complete() desde archival.py (punto de mutacion), no desde session_closeout, porque la barrera vive donde ocurre el rename y la propagacion a FAIL/exit-1 ya existe via overall_status. No se duplica logica ni se crea segundo gate. Sin auto-commit.

## BUILDER - WOT-2026-011a - Fases 1-2 (implementacion + tests)

### Cambio (repo_motor)
- scripts/closeout_steps/archival.py:step_archive_collaboration(): tras exit 0 del archivador, invoca la barrera canonica check_archive_rename_complete(project_root) (importada de scripts/delivery_hygiene_check.py). Si passed=False -> StepResult.status="FAIL" con detail = message + details (conserva reason estable "archive_rename_uncommitted" + origen + destino + comando exacto de reconcile). Propaga fail-closed via CloseoutReport.overall_status (FAIL -> exit 1). Sin auto-commit, sin borrado. Reutiliza la unica fuente de verdad; no crea segundo gate.

### Tests
- tests/test_session_closeout.py::TestArchiveRenameFailsClosed011a (2 tests):
  - test_uncommitted_rename_blocks_in_real_closeout: repo git real, work_plan apunta a ticket activo + AUDIT_ de ticket cerrado committeado; corre el ARCHIVADOR REAL via run_script_fn (shutil.move genuino, no mock vacio); verifica que el artefacto se movio, que el step da FAIL con reason estable + remediacion, y que NO hubo auto-commit (limbo sigue en git status).
  - test_clean_archive_still_passes: caso limpio (sin artefacto cerrado) sigue PASS, sin falso positivo.
- tests/unit/test_delivery_hygiene_check.py::test_stable_reason_is_contract_for_closeout_011a: bloquea que un futuro edit del helper deje caer el reason estable del que depende el closeout.

### Verificacion regresion (FAIL sin fix / PASS con fix)
- Revertido el branch barrera de archival.py a PASS-on-exit-0: test_uncommitted_rename_blocks_in_real_closeout FAIL (assert 'FAIL' == 'PASS', el limbo se colaba como PASS). Restaurado fix: 2 passed. Caso limpio PASS en ambos.

### Gates (comandos exactos + resultado literal)
- Tests focales: `python -m pytest tests/test_session_closeout.py tests/unit/test_delivery_hygiene_check.py -q` -> 63 passed in 2.43s
- Ruff: `uv run ruff check scripts/closeout_steps/archival.py scripts/session_closeout.py scripts/delivery_hygiene_check.py tests/test_session_closeout.py tests/unit/test_delivery_hygiene_check.py` -> All checks passed!
- Ruff format: `uv run ruff format --check <mismos>` -> 5 files already formatted (tras aplicar format a test_session_closeout.py)
- Encoding: `python scripts/check_encoding_guard.py` -> exit 0
- (suite canonica run_pytest_safe + validate: registrados al completar)

### Gates finales (suite canonica + validate)
- NOTA: el prompt del ticket indicaba `python scripts/run_pytest_safe.py --project-root <repo_destino>`, pero el CLI real de run_pytest_safe.py NO acepta --project-root (argparse error, no corre la suite). Se ejecuto la forma canonica sin esa flag.
- Suite canonica: `python scripts/run_pytest_safe.py` -> 3023 passed, 20 skipped, 5 deselected in 680.29s. EXIT=0. State-leak: silencioso.
- Validate: `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` -> errors=0 warnings=0.
- Solo 3 archivos tocados (todos en FLT): scripts/closeout_steps/archival.py (+17), tests/test_session_closeout.py (+121), tests/unit/test_delivery_hygiene_check.py (+17). session_closeout.py y delivery_hygiene_check.py NO modificados: el cambio minimo cupo en archival.py reutilizando el helper existente.
