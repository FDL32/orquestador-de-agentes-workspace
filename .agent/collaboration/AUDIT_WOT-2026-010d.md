# AUDIT_WOT-2026-010d -- Criterios de auditoria del ticket

> Criterios de aceptacion verificables que el Manager debe cruzar en review.
> Espejo de los Criterios Binarios de `work_plan.md`, expresados como checks.

## Barreras

- [ ] Existe barrera real para `--pause-ticket` sin `--reason`.
- [ ] Existe barrera real para ticket activo distinto en `--pause-ticket`.
- [ ] Existe test de pausa con tree limpio (`stash_ref=null`).
- [ ] Existe test de pausa con dirty tree (`changed_paths` + `diff_stat` antes de stash).
- [ ] Existe test de pausa unica (segunda pausa falla).
- [ ] Existe test de resume correcto con `TICKET_RESUMED`.
- [ ] Existe test de resume conflictivo fail-closed.
- [ ] Existe test de avance del mismo ticket tras pausa que bloquea el resume.
- [ ] Existe test de avance global de otro ticket que se reporta sin bloquear.
- [ ] Existe test explicito de `--abort-paused-ticket` fail-closed o stub auditable.
- [ ] Existe test de corte de sesion: pausa, nueva invocacion, deteccion de pausa activa.
- [ ] Existe test de `pre_handoff_guard` con pausa activa ajena o corrupta.

## Contrato estructural

- [ ] `PAUSED` existe en `bus/state_machine.py` y en `.agent/state_validation.py`.
- [ ] `STATE.md` mantiene `ACTIVE_TICKET` y proyecta `STATUS: PAUSED`.
- [ ] El artefacto `paused/<ticket>.json` contiene como minimo `ticket_id`, `status`, `reason`, `changed_paths`, `diff_stat`, `stash_ref`, `bus_last_seq_global` y `ticket_last_seq`.
- [ ] La ref persistida no depende de `stash@{n}`.
- [ ] `pre_handoff_guard.py` bloquea una pausa activa ajena o corrupta con diagnostico claro.
- [ ] `--validate --json` distingue `paused_ticket_active` y `paused_ticket_corrupt`.

## Gates de cierre (code)

- [ ] Diff y commit productivo del ticket visibles para el Manager.
- [ ] `ruff check .` exit 0.
- [ ] Tests focales de pausa/reanudacion exit 0.
- [ ] `python scripts/run_pytest_safe.py --project-root <repo_destino>` leido hasta `0 failed`.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` exit 0, 0 errors, 0 warnings.

## Anti-patrones a rechazar

- Pausa implementada solo como stash sin evento de bus ni JSON canonico.
- Resume que ignora eventos posteriores del mismo ticket.
- Resume que intenta resolver conflictos automaticamente.
- `ACTIVE_TICKET` vaciado durante la pausa.
- Tests cosmeticos que solo comprueban `json != None` o que un mock fue llamado.
- Cambios fuera de FLT o mezcla con 010e/010i.