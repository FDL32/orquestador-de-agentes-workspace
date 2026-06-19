# work_plan.md -- WOT-2026-011c

## Metadata

- **ID:** WOT-2026-011c
- **Contract ID:** T-011C-001
- **Estado:** COMPLETED
- **ROL activo esperado:** BUILDER
- **deliverable_type:** research
- **Builder clarification budget:** 0
- **delivery_authority:** repo_destino
- **repo_motor:** <repo_motor> (solo lectura para este ticket)
- **repo_destino:** <repo_destino> (resuelto por `--project-root` / `AGENT_PROJECT_ROOT`)

## Objetivo

Identificar con evidencia reproducible la fuente que inyecta BOM UTF-8 en las
superficies vivas de `.agent/collaboration/` y, si es posible, el origen de los
3 control chars preservados en la region historica de `backlog.md`. Este ticket
es un spike de investigacion: entrega un reporte de hallazgo y PARA, sin aplicar
fix de fuente.

## Non-goals

- No aplicar ningun fix de fuente (strip BOM, reconstruir letras, cambiar
  escritor, tocar hooks, controller o launcher).
- No tocar `scripts/check_encoding_guard.py` ni la defensa 010v.
- No limpiar superficies vivas "para dejarlo bonito".
- No tocar `repo_motor` salvo lectura de evidencia.

## Premisas verificadas antes de Builder

- `WOT-2026-012a` quedo bloqueado canonicamente en `CONTRACT_BLOCKED`; su
  `CG-WOT-2026-012a.md` recomienda secuenciar `011c` antes de reintentar el
  handoff.
- El encoding guard ya detecta el sintoma, pero la fuente sigue sin estar
  identificada.
- Evidencia base ya conocida:
  - `work_plan.md`, `TURN.md`, `backlog.md` y `execution_log.md` aparecen con
    BOM en working tree en determinados ciclos, mientras `STATE.md`,
    `notifications.md` y `review_queue.md` no.
  - `HEAD:backlog.md` contiene 3 control chars en la region historica
    (`\x07udit`, `\x0Balidate`, `\x08ui-self`).
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  esta en 0 errors / 0 warnings al arrancar `011c`.

## Decision Arquitectonica

`011c` es research puro. El Builder debe observar y correlacionar escritores,
bytes y comportamiento del host, producir un reporte durable en
`.agent/runtime/audit/`, y detenerse en cuanto la fuente quede identificada con
evidencia suficiente. Si demostrar la hipotesis exige modificar un escritor, eso
ya no es spike sino fix y debe bloquearse como `CONTRACT_GAP`.

## Files Likely Touched

### repo_destino

- `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`
- `.agent/collaboration/execution_log.md`

## Read/inspect only

- `scripts/launch_agent_terminals.ps1`
- `scripts/encoding_post_write_hook.py`
- `bus/`
- `.agent/agent_controller.py`
- cualquier `Out-File` / `Set-Content` / `encoding=` que toque `.agent/collaboration/`
- git history y bytes de las superficies con BOM/control chars
- `CG-WOT-2026-012a.md` y `CG-WOT-2026-012a.execution_log_snapshot.md`

## Forbidden Surfaces

- Aplicar cualquier fix de fuente.
- Tocar escritores del motor o del destino para "probar" la hipotesis.
- Tocar el guard 010v.
- Reescribir `backlog.md`, `work_plan.md`, `TURN.md` o `execution_log.md` para
  borrar sintoma en vez de identificar origen.
- Tocar `repo_motor` productivamente.

## Criterios binarios

- Existe `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md` con la fuente
  o fuentes candidatas nombradas con evidencia reproducible.
- El reporte distingue `VERIFICADO` de `INFERENCIA RAZONABLE`; no presenta
  hipotesis como hecho.
- El reporte declara si hay fix de fuente viable o si 010v es defensa
  suficiente, como recomendacion, no como cambio aplicado.
- El reporte abre follow-up(s) concretos para el fix, si procede.
- `python scripts/check_encoding_guard.py <reporte> <execution_log>` queda verde
  sobre las superficies propias del ticket.
- `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`
  queda en 0 errors / 0 warnings.

## STOP conditions

- Parar y entregar el reporte en cuanto la fuente quede identificada con
  evidencia suficiente.
- Parar si la unica forma de avanzar es modificar un escritor.
- Parar si la fuente resulta ser el entorno host (por ejemplo, comportamiento de
  PowerShell 5.1 / `Out-File`) y el fix excede `repo_destino`.

## CONTRACT_GAP

Emitir `CG-WOT-2026-011c.md` y bloquear si identificar la fuente exige MODIFICAR
un escritor del motor o del destino para probar la hipotesis, porque eso ya es
el fix y pertenece a un follow-up separado.
