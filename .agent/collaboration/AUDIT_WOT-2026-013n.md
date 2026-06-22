# AUDIT_WOT-2026-013n

## Pregunta de auditoria
El cambio introduce terminalidad honesta no-exito para `SUPERSEDED` y `BLOCKED_FINAL` sin falsear `COMPLETED`, y la propaga a las superficies operativas relevantes sin romper el cierre exitoso existente?

## Criterios binarios
- [ ] `TicketState` o helper canonico reconoce `SUPERSEDED` y `BLOCKED_FINAL` como terminales irreversibles.
- [ ] El string legacy `CLOSED` deja de actuar como pseudo-estado canonico y no reaparece como nuevo miembro de `TicketState`.
- [ ] `READY_TO_CLOSE` sigue sin ser terminal; `COMPLETED` sigue funcionando como cierre de exito.
- [ ] `archive_event_bus`, `reconcile_ticket`/`preflight_reconcile`, `session_closeout`/`archival`, `get_launcher_state` y `check_destino_publish_ready` quedan alineados con la misma autoridad.
- [ ] `bus/supervisor.py` no conserva una lista local divergente de no-terminalidad.
- [ ] Existe FAIL-sin/PASS-con para `SUPERSEDED`.
- [ ] Existe FAIL-sin/PASS-con para `BLOCKED_FINAL`.
- [ ] `tests/test_launcher_state_from_bus.py` demuestra que ambos estados caen del lado terminal del launcher.
- [ ] `tests/evals/test_eval_requeue.py` demuestra que ambos estados bloquean relaunch/requeue como terminales.
- [ ] `python scripts/run_pytest_safe.py --level all` queda verde sobre el commit entregado.
- [ ] `validate --json --project-root <repo_destino>` queda en 0 errors / 0 warnings.

## Anti-patrones a rechazar
- mapear los nuevos estados a `COMPLETED` ?por compatibilidad?
- conservar `CLOSED` como pseudo-estado vivo o promocionarlo a enum sin evidencia
- dejar listas locales divergentes de terminalidad en consumidores criticos
- meter `ABANDONED` sin evidencia de Fase 0
- tocar controller, handoff o CI para compensar una autoridad de estados incompleta

## Evidencia minima esperada en review
- diff productivo del motor dentro de FLT
- tests focales con comandos exactos y resultado literal
- suite canonica con `tested_commit_sha == HEAD`
- validate 0/0
- explicacion explicita de por que `239a` y `013c` ya no requieren `COMPLETED` para verse terminales

