# ticket_contracts.md -- Plan WOT-2026-008

> Solo contratos frozen pasan a work_plan.md. CONTRACT_GAP es la unica via para
> invalidar el contrato activo.

## T-008A-001 -- Manifiesto de taxonomia prompts/skills

- **ticket_id:** WOT-2026-008a
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_destino
- **Objective-Link:** OBJ-001, OBJ-002, OBJ-003
- **Plan-Link:** PLAN-001
- **Premise:** el layout del motor es mayoritariamente plano y los scripts de
  discovery/collision no soportan de forma canonica skills anidadas.
- **Premise Re-check (read-only):**
  - contar `prompts/*.md`, `skills/**/SKILL.md`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/*.md` y `skills/_shared/*.md`;
  - inspeccionar `scripts/discover_skills.py` y `scripts/check_skill_collisions.py`;
  - ejecutar discovery contract y collision check sin modificar archivos;
  - buscar referencias vivas a `prompts/`, `skills/`, `MANIFEST.*`, `llms*.txt`, scripts y docs excluyendo caches/reportes;
  - contrastar patron manifest-first con una referencia externa verificable (p.ej. mattpocock/skills plugin.json), marcando si `gh` no esta autenticado.
- **Context Baseline Evidence:** motor_head=ece7524; destino_head=28b24ce;
  prompts_md=19; skill_md=29; prompt_templates=2; skill_references=33; shared_docs=3; generated_at=2026-06-15.
- **Files Likely Touched:**
  - Builder: `.agent/docs/taxonomy_migration_WOT-2026-008a.md`
  - Builder: `.agent/collaboration/execution_log.md`
  - Read/inspect only: repo_motor `prompts/`, `skills/`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/`, `skills/_shared/`, `scripts/discover_skills.py`,
    `scripts/check_skill_collisions.py`, `scripts/build_llms.py`, `MANIFEST.*`, docs, tests, `llms*.txt` y referencias.
- **Forbidden Surfaces:** todo archivo del repo_motor; backlog/planning/work_plan
  salvo materializacion del Manager; `privada/`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] El manifiesto inventaria todas las rutas `prompts/*.md`, `skills/**/SKILL.md`, `skills/**/PROMPT_TEMPLATE.md`, `skills/**/references/*.md`, `skills/_shared/*.md`, scripts de discovery/build, manifests y `llms*.txt`; ninguna queda sin clasificacion.
  - [ ] Cada fila incluye ruta actual, API publica, consumidores, destino
    propuesto, compatibilidad, riesgo y ticket/fase propietaria.
  - [ ] Se separan referencias machine-executed, contract checks y documentacion.
  - [ ] Se demuestra con lineas de codigo que discovery/collision son planos o
    se corrige la premisa mediante CONTRACT_GAP.
  - [ ] La profundidad maxima de carpetas queda tratada como hipotesis evaluada, no como decision previa; cualquier recomendacion incluye evidencia, tradeoffs y DEC-008 correspondiente.
  - [ ] Se compara registry explicito manifest-first frente a discovery por glob/recursivo; la recomendacion distingue API publica, layout fisico e indice generado.
  - [ ] Se define una unica fuente canonica por recurso; los shims son read-only,
    temporales y tienen version/ticket de retirada.
  - [ ] Se propone descomposicion posterior: infraestructura discovery, migracion
    de prompts, migracion de skills y retirada de shims, con dependencias.
  - [ ] El manifiesto incluye riesgos, STOP conditions, estrategia rollback y
    gates exactos por fase.
  - [ ] `git status --short` del repo_motor permanece vacio.
  - [ ] encoding guard del entregable exit 0.
  - [ ] validate del repo_destino exit 0, 0 errors, 0 warnings al handoff.
- **Integracion cross-ticket:** serializar contra cualquier ticket que toque
  prompts, skills, discovery, manifests o referencias globales.
- **CONTRACT_GAP behavior:** si el inventario no puede ser completo, aparece un
  consumidor no clasificable o la premisa de discovery plano es falsa, emitir
  `CG-WOT-2026-008a.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. Las decisiones humanas pendientes se
  presentan como DEC-008-* con recomendacion; el usuario no edita el manifiesto.
- **STOP conditions:** no mover/renombrar/borrar; no editar motor; no crear shim;
  no ampliar a implementacion; parar ante cambio concurrente del HEAD del motor; parar si el entregable se escribe fuera de repo_destino.
- **Depende de:** WOT-2026-007d (COMPLETED 11e7ad8).

## T-010D-001 -- Lifecycle canonico de pausa/reanudacion

- **ticket_id:** WOT-2026-010d
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-004
- **Plan-Link:** PLAN-010D-001
- **Premise:** el motor no ofrece hoy un lifecycle canonico de pausa/reanudacion; `PAUSED` no existe en `TicketState`; el estado operativo debe seguir derivandose del bus y las proyecciones markdown pueden quedar desalineadas si no se fijan desde una unica autoridad.
- **Premise Re-check (read-only):**
  - verificar que `bus/state_machine.py` no contiene `PAUSED`;
  - verificar que `.agent/state_validation.py` no acepta `PAUSED`;
  - verificar que `.agent/agent_controller.py` no expone `--pause-ticket`, `--resume-ticket` ni `--abort-paused-ticket`;
  - verificar que `scripts/pre_handoff_guard.py` no inspecciona `paused/` ni diagnosticos `paused_ticket_*`;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de bootstrap para dejar constancia del estado pre-arranque.
- **Context Baseline Evidence:** motor_head=b0248b1; destino_head=3a5a25b; motor_status='main ahead 2, clean'; destino_status='main ahead 1, packet 010d pre-arranque'; validate_result='0 errors; warnings pre-bootstrap para 010d sin STATE_CHANGED'; generated_at=2026-06-16.
- **Files Likely Touched:**
  - Builder: `.agent/agent_controller.py`
  - Builder: `.agent/state_validation.py`
  - Builder: `bus/state_machine.py`
  - Builder: `bus/supervisor.py`
  - Builder: `bus/builder_locks.py`
  - Builder: `scripts/pre_handoff_guard.py`
  - Builder: `runtime/ui_state_projector.py`
  - Builder: `tests/unit/test_pause_ticket.py`
  - Builder: `tests/unit/test_resume_ticket.py`
  - Builder: `tests/test_pre_handoff_guard.py`
  - Builder: `tests/unit/test_state_projection_probe.py`
  - Read/inspect only: `bus/event_bus.py`, `INTERACTION_MODES.md`, `QUICKSTART.md`, `TURN.md`, `STATE.md`, `execution_log.md`
- **Forbidden Surfaces:** `privada/`, `.env`, `.agent/runtime/memory/`, bus editado manualmente, tickets `WOT-2026-010e`, `WOT-2026-010f`, `WOT-2026-010g`, `WOT-2026-010h`, `WOT-2026-010i`, `WOT-2026-008d`, y documentacion general (`QUICKSTART.md`, `INTERACTION_MODES.md`) en esta ronda v1.
- **DoD (criterios binarios de cierre):**
  - [ ] Existen `--pause-ticket`, `--resume-ticket` y `--abort-paused-ticket` en `.agent/agent_controller.py` con parser y salida coherentes.
  - [ ] `PAUSED` existe en `bus/state_machine.py` y `.agent/state_validation.py`.
  - [ ] `--pause-ticket` falla si el ticket activo no coincide o falta `--reason`.
  - [ ] Si no hay diff, `stash_ref=null`; si hay diff, se capturan `changed_paths` y `diff_stat` antes de persistir una ref estable no basada en `stash@{n}`.
  - [ ] `--pause-ticket` crea `repo_destino/.agent/collaboration/paused/<ticket>.json`, emite `TICKET_PAUSED`, proyecta `STATE=PAUSED` y mantiene `ACTIVE_TICKET`.
  - [ ] Solo se permite una pausa activa en v1.
  - [ ] `--resume-ticket` verifica artefacto, ref resoluble y ausencia de eventos posteriores del mismo ticket antes de restaurar.
  - [ ] `--resume-ticket` falla cerrado ante conflicto y no deja tree parcialmente mutado.
  - [ ] Existe un test explicito para `--abort-paused-ticket` fail-closed o stub auditable sin dejar estado parcial.
  - [ ] `pre_handoff_guard` y `--mark-ready` bloquean pausa activa ajena o corrupta.
  - [ ] `run_pytest_safe` termina con `0 failed` y `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings al cierre.
- **Integracion cross-ticket:** serializar contra cualquier ticket que toque bus, controller, supervisor, locks de Builder, state projection, pre-handoff o lifecycle runtime. No paralelizable segun `PLAN-010D-001`.
- **CONTRACT_GAP behavior:** si la premisa es falsa, aparece una superficie compartida no prevista, se requiere tocar docs generales en vez del runtime, o `resume` no puede garantizar fail-closed, emitir `CG-WOT-2026-010d.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. Si el Builder necesita decidir semantica de lifecycle o que autoridad manda entre bus y markdown, el contrato fallo.
- **STOP conditions:** parar si aparece otro ticket activo no terminal en el bus; parar si la unica forma de persistir pausa depende de `stash@{n}`; parar si `PAUSED` obliga a redisenar la state-machine mas alla de un cambio localizado; parar si se descubre que la documentacion general es necesaria para cerrar v1.
- **Depende de:** WOT-2026-010c (COMPLETED), WOT-2026-010e (COMPLETED, no dependencia funcional).
