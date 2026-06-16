# Work Plan: WOT-2026-010d

> Origen: durante WOT-2026-008c hubo que pausar el ticket para abrir el hotfix
> WOT-2026-010b. La pausa se resolvio a mano con stash path-limited y relato,
> pero no con estado canonico, evento de bus ni artefacto recuperable.

## Metadata

- **ID:** WOT-2026-010d
- **Contract ID:** T-010D-001
- **Estado:** READY_TO_START
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-010c (cerrado/COMPLETED)

## Pre-launch note

- `STATE.md` sigue mostrando `WOT-2026-010c / COMPLETED` porque 010d todavia NO ha emitido `STATE_CHANGED` al bus.
- `TURN.md` debe leerse como preparacion de packet / arranque pendiente, no como prueba de ticket activo.
- El arranque canonico de 010d ocurre despues de esta auditoria, no durante la preparacion del packet.

## Objetivo

Introducir lifecycle minimo `IN_PROGRESS -> PAUSED -> IN_PROGRESS` para el ticket activo, con razon obligatoria, evento de bus, artefacto legible en el `repo_destino`, recuperacion fail-closed y bloqueo de handoffs incompatibles.

Frase guia: "La pausa no es un stash; es un estado canonico recuperable tras corte de sesion, con artefacto legible, bus coherente y resume fail-closed."

## Decision Arquitectonica

- **DEC-010D-001 / T1a:** el bus es la autoridad de lectura. La pausa/reanudacion deriva el estado desde el event bus y usa `TURN.md` / `STATE.md` como proyecciones. No leer solo markdown para decidir si un resume es valido.
- **CLI nueva en `.agent/agent_controller.py`.** V1 introduce `--pause-ticket`, `--resume-ticket` y `--abort-paused-ticket`. El flag de abort debe existir en esta ronda; si el camino `ABORTED` no queda completo, la salida minima aceptable es fail-closed con diagnostico explicito y follow-up declarado.
- **Estado nuevo `PAUSED` canonico.** Debe vivir en `bus/state_machine.py`, en los validadores de `.agent/state_validation.py`, en las rutas del supervisor que escanean tickets no terminales y en cualquier guard que hoy enumera estados.
- **Artefacto canonico por ticket:** `repo_destino/.agent/collaboration/paused/<ticket>.json` con `ticket_id`, `status`, `reason`, `timestamp`, `repo`, `changed_paths`, `diff_stat`, `stash_ref`, `wip_commit`, `bus_last_seq_global`, `ticket_last_seq`, `state_snapshot`, `turn_snapshot`, `resume_instructions`, `abort_reason`, `aborted_at`, `aborted_by`.
- **DEC-010D-002 / T1a:** una sola pausa activa en v1. Cuando ya hay una pausa activa, otro `--pause-ticket` falla con diagnostico self-service.
- **DEC-010D-003 / T1a:** no vaciar `ACTIVE_TICKET`. `STATE.md` conserva el ticket activo y cambia solo `STATUS: PAUSED`.
- **DEC-010D-004 / T2:** cuando `changed_paths=[]`, no crear stash y guardar `stash_ref=null`. Cuando hay diff, capturar `changed_paths` + `diff_stat` antes de guardar un stash path-limited o ref estable equivalente; nunca usar `stash@{n}` como fuente de verdad.
- **Resume fail-closed.** `--resume-ticket` debe localizar el JSON, verificar que la ref guardada siga resoluble, comparar `ticket_last_seq` contra el bus del mismo ticket y fallar si hubo eventos posteriores para ese ticket. El avance global por otros tickets se permite, pero debe reportarse usando `bus_last_seq_global`.
- **Nada de autoresolucion de conflictos.** Si `git stash apply` o restauracion equivalente encuentra conflicto, el comando falla sin dejar el arbol a medias.
- **Handoff y review protegidos.** `scripts/pre_handoff_guard.py` y el flujo `--mark-ready` bloquean ante una pausa activa ajena o corrupta.

## Files Likely Touched

### repo_motor
- `.agent/agent_controller.py`
- `.agent/state_validation.py`
- `bus/state_machine.py`
- `bus/supervisor.py`
- `bus/builder_locks.py`
- `scripts/pre_handoff_guard.py`
- `runtime/ui_state_projector.py`
- `tests/unit/test_pause_ticket.py`
- `tests/unit/test_resume_ticket.py`
- `tests/test_pre_handoff_guard.py`
- `tests/unit/test_state_projection_probe.py`

### repo_destino (packaging del handoff)
- `.gitignore`

Notas (no son parte del FLT parseable):
- `.gitignore` (repo_destino): enmienda de contrato durante el handoff. El
  pre-handoff guard bloqueaba por `.vscode/` sin trackear (config del IDE, no
  artefacto del ticket). Se anadio `.vscode/` al ignore del destino (commit
  0f5418a) para limpiar el dirty tree. Superficie minima de packaging, no afecta
  al codigo del motor ni al lifecycle de pausa.
- `agent_controller.py` concentra parser CLI, escritura/lectura del artefacto `paused/<ticket>.json`, emision `TICKET_PAUSED` / `TICKET_RESUMED`, y sync de proyecciones.
- `bus/state_machine.py`, `state_validation.py`, `supervisor.py` y `builder_locks.py` deben quedar coherentes con `PAUSED` como estado legitimo no terminal.
- `runtime/ui_state_projector.py` solo se toca para exponer correctamente el nuevo estado en la proyeccion UI.

## Read/inspect only

- `bus/event_bus.py` (API real de emision y secuencias)
- `.agent/agent_controller.py::_handle_resume_human_gate` (modelo de flag de recuperacion ya existente)
- `INTERACTION_MODES.md` y `QUICKSTART.md` como referencia documental del lifecycle

## Manager-only

- Ejecutar `python scripts/run_pytest_safe.py --project-root <repo_destino>` completo y leer hasta `0 failed`.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` final 0/0.
- Verificar review packet con commit visible del ticket y tree limpio antes de `--mark-ready` / handoff.

## Tests Esperados

- `--pause-ticket` falla si el ticket activo no coincide.
- `--pause-ticket` falla si falta `--reason`.
- pausa con tree limpio: crea JSON, no crea stash, emite `TICKET_PAUSED`.
- pausa con dirty tree: captura `changed_paths` + `diff_stat` antes del stash y persiste ref estable en el JSON.
- pausa unica: segunda pausa activa falla.
- resume correcto: restaura cambios, emite `TICKET_RESUMED`, vuelve a `IN_PROGRESS`.
- resume conflictivo: fail-closed, sin working tree parcialmente mutado.
- bus advance del mismo ticket tras pausa: bloquea resume.
- bus advance de otro ticket: permite resume pero reporta drift global.
- `--abort-paused-ticket` fail-closed o stub auditable: existe test explicito y no deja estado parcial.
- crash/restart: nueva sesion detecta pausa activa y no deja abrir/ejecutar otro ticket sin resolverla.
- `pre_handoff_guard` bloquea con pausa activa ajena o pausa corrupta.
- `validate --json` distingue `paused_ticket_active` y `paused_ticket_corrupt`.
- `STATE.md` mantiene `ACTIVE_TICKET` y proyecta `STATUS: PAUSED`.

## Criterios Binarios

- [ ] Existen las tres flags nuevas en `.agent/agent_controller.py` con parser y mensajes de uso coherentes con el contrato.
- [ ] `PAUSED` es un estado reconocido por `bus/state_machine.py` y por `.agent/state_validation.py`.
- [ ] `--pause-ticket` falla si el ticket activo no coincide o falta `--reason`.
- [ ] Antes de guardar stash/ref WIP, captura `changed_paths` y `diff_stat`.
- [ ] Cuando no hay diff, `stash_ref=null`; no se crean stashes vacios.
- [ ] Cuando hay diff, la ref persistida no depende de `stash@{n}`.
- [ ] `--pause-ticket` escribe `paused/<ticket>.json`, emite `TICKET_PAUSED`, proyecta `STATE=PAUSED` y deja `ACTIVE_TICKET` intacto.
- [ ] Solo se permite una pausa activa en v1.
- [ ] La resolucion de `repo_destino` desde `motor_destination_link.json` usa la clave `destination_root` (NO `motor_root`). Leccion de WOT-2026-010e: `_resolve_destino` devolvio `motor_root` y dejo la ruta multi-root via link incorrecta. El test debe cubrir la ruta por link, no solo por `AGENT_PROJECT_ROOT`.
- [ ] `--resume-ticket` verifica artefacto, ref resoluble y ausencia de eventos posteriores del mismo ticket antes de restaurar.
- [ ] El avance global del bus por otros tickets se reporta, pero no bloquea por si solo.
- [ ] `--resume-ticket` restaura de forma atomica o falla sin dejar tree a medias.
- [ ] `--abort-paused-ticket` tiene al menos un test de fail-closed o stub auditable.
- [ ] `pre_handoff_guard` / `--mark-ready` bloquean pausa activa ajena o corrupta.
- [ ] Test de corte `pause -> nueva sesion -> detecta pausa activa` existe y pasa.
- [ ] Tests demuestran pause limpio, pause dirty, no-stash, resume correcto, resume conflictivo, bus advance mismo ticket, bus advance otro ticket, pausa unica, abort fail-closed y bloqueo de handoff.
- [ ] `ruff check .` exit 0.
- [ ] Tests focales exit 0.
- [ ] `run_pytest_safe` completo leido hasta `0 failed`.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` exit 0, 0 errors, 0 warnings.

## Non-goals

- NO implementar pausas anidadas en v1.
- NO usar stash global ni `stash@{n}` como autoridad.
- NO vaciar `ACTIVE_TICKET` durante la pausa.
- NO permitir autoresolucion de conflictos en resume.
- NO mezclar con la gate `0 failed` de WOT-2026-010c ni con el hook de encoding de WOT-2026-010e.
- NO tocar `QUICKSTART.md` ni `INTERACTION_MODES.md` en esta ronda; si la feature requiere documentacion para cerrar, abrir follow-up en vez de colarla en v1.
- NO redisenar toda la state-machine mas alla de lo necesario para `PAUSED`.

## Forbidden Surfaces

- `privada/` y `.env`
- `.agent/runtime/memory/`
- tickets `WOT-2026-010e`, `WOT-2026-010f`, `WOT-2026-010g`, `WOT-2026-010h`, `WOT-2026-010i`, `WOT-2026-008d`
- scripts o docs no ligados al lifecycle de pausa/reanudacion