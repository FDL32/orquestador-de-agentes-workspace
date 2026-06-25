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

## T-010J-001 -- Baseline de performance de suite

- **ticket_id:** WOT-2026-010j
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010J-001
- **Plan-Link:** PLAN-010J-001
- **Premise:** la suite canonica tarda varios minutos y hoy no existe una baseline reproducible que separe tiempo total, hotspots reales y peso relativo de `subprocess`/`git` frente a otros costes. La hipotesis "git/subprocess domina" es una inferencia por inspeccion de tests, NO un hecho medido.
- **Premise Re-check (read-only):**
  - verificar que `scripts/run_pytest_safe.py` acepta `--level all` y argumentos extra para pytest;
  - verificar que `pytest-cache` sigue deshabilitado en `pytest.ini` / runner;
  - verificar que `pytest-xdist` no esta instalado en `pyproject.toml` o lockfile;
  - verificar que `integration`/`slow` son una fraccion pequena de la suite;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** motor_head=dirty-local; destino_state=WOT-2026-010f COMPLETED; validate_result=0 errors / 0 warnings; generated_at=2026-06-17.
- **Files Likely Touched:**
  - Builder: `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`
  - Builder: `.agent/collaboration/work_plan.md`
  - Read/inspect only: `scripts/run_pytest_safe.py`, `scripts/run_gates_dispatch.py`, `pytest.ini`, `pyproject.toml`, `tests/`, `.agent/agent_controller.py`, `.agent/runtime/pytest-safe/`
- **Forbidden Surfaces:** cualquier archivo productivo Python del motor; `.agent/agent_controller.py`; `scripts/run_pytest_safe.py`; `scripts/run_gates_dispatch.py`; `pytest.ini`; `pyproject.toml`; `uv.lock`; `privada/`; `.env`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Ejecuta `python scripts/run_pytest_safe.py --level all -- --durations=50` o documenta con evidencia por que no fue viable.
  - [ ] El reporte durable existe en `repo_motor/docs/test_performance/test_performance_baseline_WOT-2026-010j.md`.
  - [ ] El reporte incluye tiempo total, top tests lentos, top modulos lentos y peso relativo de `subprocess`/`git`.
  - [ ] El reporte separa hechos verificados de inferencias y confirma o refuta la hipotesis `git/subprocess`.
  - [ ] El reporte cuenta archivos/tests que usan `subprocess`, `git`, filesystem real, controller/bus y marcas `integration`/`slow`.
  - [ ] El reporte recomienda el siguiente ticket ejecutable con evidencia, no por intuicion.
  - [ ] `git diff` del `repo_motor` se limita al artefacto documental del ticket.
  - [ ] `check_encoding_guard.py` pasa sobre el reporte y los artefactos de packet tocados.
  - [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- **Integracion cross-ticket:** 010j es gate de premisa para 010k, 010l y 010m. Ninguno de esos tickets debe arrancar sin leer el reporte final de 010j.
- **CONTRACT_GAP behavior:** si la medicion no puede ejecutarse de forma reproducible, el reporte no puede quedar durable en `repo_motor`, o la suite no produce datos suficientes para decidir el siguiente ticket, emitir `CG-WOT-2026-010j.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. El Builder no decide politica de gates ni optimizaciones; solo mide y reporta.
- **STOP conditions:** parar si el ticket exige tocar codigo del motor para "facilitar" la medicion; parar si la unica forma de obtener datos requiere activar cache/sharding/xdist; parar si el reporte acabaria en `repo_destino` en vez de `repo_motor`; parar si `validate` deja warnings nuevos sin resolver.
- **Depende de:** WOT-2026-010c (COMPLETED).

## T-010N-001 -- Gate de deliverables namespaced por delivery_authority

- **ticket_id:** WOT-2026-010n
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010N-001
- **Plan-Link:** PLAN-010N-001
- **Premise:** `scripts/check_deliverables_exist.py` valida hoy los deliverables Builder solo relativos a `--project-root` y no resuelve correctamente rutas FLT que viven en `repo_motor`. El fallo fue evidenciado por `WOT-2026-010j`: un reporte real y existente en `repo_motor/docs/test_performance/` quedo bloqueado por el gate aunque el contrato declaraba `delivery_authority: repo_motor`.
- **Premise Re-check (read-only):**
  - reproducir el bloqueo de `WOT-2026-010j` sin duplicar el artefacto en `repo_destino`;
  - inspeccionar `scripts/check_deliverables_exist.py` y como interpreta `Files Likely Touched`;
  - contrastar con `scripts/scope_gate.py`, `delivery_authority` y FLT namespaced;
  - verificar que `Read/inspect only` y notas libres no cuentan como deliverables Builder.
- **Context Baseline Evidence:** trigger_ticket=WOT-2026-010j; report_commit=c05dbfe; packet_fix_commit=cb01f28; generated_at=2026-06-17.
- **Files Likely Touched:**
  - Builder: `scripts/check_deliverables_exist.py`
  - Builder: tests del gate de deliverables
  - Builder: documentacion puntual del gate solo si la regla namespaced necesita quedar explicita
  - Read/inspect only: `scripts/scope_gate.py`, `.agent/agent_controller.py`, `scripts/pre_handoff_guard.py`, `ticket_contracts.md`, `work_plan.md`, artefactos de `WOT-2026-010j`
- **Forbidden Surfaces:** duplicar artefactos entre `repo_motor` y `repo_destino` para satisfacer el gate; relajar el gate a pass-open; modificar el reporte de `010j`; cambiar politica de closeout ajena al bug; `privada/`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Existe una barrera de regresion que reproduce el caso real de `010j` y falla sin el fix.
  - [ ] Un deliverable Builder existente en `repo_motor` pasa el gate cuando el FLT o el contrato lo resuelven a `repo_motor`.
  - [ ] Un deliverable Builder existente en `repo_destino` sigue pasando sin regresion.
  - [ ] Una ruta namespaced invalida, ambigua o fuera de root falla cerrado con diagnostico claro.
  - [ ] El gate ignora `Read/inspect only`, `Manager-only` y notas no parseables como entregables Builder.
  - [ ] `WOT-2026-010j` puede cerrar canonicamente sin duplicar el reporte en `repo_destino`.
  - [ ] `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings tras la reparacion del gate y el cierre reintentado de `010j`.
- **Integracion cross-ticket:** desbloquea el cierre de `WOT-2026-010j`; cualquier ticket documental/analysis con entrega en `repo_motor` depende de esta correccion si usa `check_deliverables_exist.py`.
- **CONTRACT_GAP behavior:** si el bug no puede corregirse sin redisenar por completo el contrato FLT/delivery_authority, o aparecen consumidores incompatibles que exigen una migracion mayor, emitir `CG-WOT-2026-010n.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. El Builder no debe improvisar duplicacion de artefactos ni reinterpretar a mano el namespace correcto.
- **STOP conditions:** parar si la unica forma de pasar el gate exige copiar el deliverable de `repo_motor` a `repo_destino`; parar si el fix rompe deliverables existentes del destino; parar si la reproduccion depende de editar el ticket `010j` mas alla de usar su evidencia real.
- **Depende de:** WOT-2026-010j (IN_PROGRESS / CONTRACT_GAP confirmado).

## T-010K-001 -- Hotspots reales de suite: filesystem/scan y setup repetido

- **ticket_id:** WOT-2026-010k
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010K-001
- **Plan-Link:** PLAN-010K-001
- **Premise:** la baseline real de `WOT-2026-010j` refuto `git/subprocess` como hotspot dominante. El coste mayor de la suite vive en tests de filesystem/scan y en setup repetido caro; por tanto `010k` debe re-scopearse para optimizar esos hotspots reales sin cambiar la politica de gates.
- **Premise Re-check (read-only):**
  - releer `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`;
  - confirmar los tests o familias lentas priorizadas por tiempo wall-clock real;
  - verificar que los candidatos elegidos no son tests cuyo contrato observable exige precisamente scan completo o git/filesystem real;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** source_ticket=WOT-2026-010j; source_report_commit=c05dbfe; trigger_followup=WOT-2026-010k; generated_at=2026-06-17.
- **Files Likely Touched:**
  - Builder: tests o fixtures del `repo_motor` directamente implicados en los hotspots reales seleccionados
  - Builder: helper o fixture compartida si elimina setup repetido de forma localizada
  - Builder: `docs/test_performance/test_performance_followup_WOT-2026-010k.md`
  - Read/inspect only: `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`, `scripts/run_pytest_safe.py`, `pytest.ini`, `.agent/agent_controller.py`, tests relacionados no modificados
- **Forbidden Surfaces:** `run_gates_dispatch.py`; politica Builder/Manager; cache de pytest; paralelizacion/xdist; duplicar artefactos; `privada/`; `.env`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Solo optimiza tests o fixtures identificados por `010j` como hotspots reales de tiempo wall-clock.
  - [ ] La optimizacion se centra en filesystem/scan o setup repetido; no se persigue `git/subprocess` salvo que el diff real lo justifique con medicion.
  - [ ] Mantiene tests de contrato que validan comportamiento real del subsistema optimizado cuando ese comportamiento es la API observable.
  - [ ] Cada helper/fixture nueva que sustituya setup caro queda cubierta por al menos un smoke test sin el shortcut correspondiente.
  - [ ] Demuestra mejora con medicion antes/despues bajo condiciones comparables del mismo entorno.
  - [ ] No reduce cobertura semantica ni introduce falso-verde.
  - [ ] `validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings al cierre.
- **Integracion cross-ticket:** usa `010j` como fuente de verdad; no debe contaminar `010l` ni `010m` con cambios de politica.
- **CONTRACT_GAP behavior:** si los hotspots reales no admiten optimizacion local sin degradar el contrato observable, o si la mejora exige cambiar politica de gates/runner, emitir `CG-WOT-2026-010k.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. El Builder no debe reabrir la hipotesis vieja de `git/subprocess` sin evidencia nueva.
- **STOP conditions:** parar si la mejora exige cache, paralelizacion, sharding o selector focal; parar si el candidato optimizado deja de validar el comportamiento real que el test protege; parar si la medicion before/after no es comparable.
- **Depende de:** WOT-2026-010j (COMPLETED), WOT-2026-010n (COMPLETED).

## T-010I-001 -- Hardening de review packet, Forbidden Surfaces y tests semanticos

- **ticket_id:** WOT-2026-010i
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010I-001
- **Plan-Link:** PLAN-010I-001
- **Premise:** la review de WOT-2026-010e detecto fallos que llegaron tarde al Manager: packet sin commit visible, Forbidden Surfaces solo contractuales, test de fallback con falso verde y regresion semantica sobre campo leido frente a campo retornado. El bug funcional de `_resolve_destino()` ya esta corregido; este ticket lo blinda con barreras y tests reutilizables.
- **Premise Re-check (read-only):**
  - inspeccionar `scripts/pre_handoff_guard.py`, `scripts/scope_gate.py` y `scripts/check_deliverables_exist.py`;
  - confirmar como `--mark-ready` obtiene diff, commit visible y estado de packet;
  - confirmar que `_resolve_destino()` usa `destination_root` cuando existe `motor_destination_link.json`;
  - confirmar que `WOT-2026-010q` ya cubre suite canonica real y no debe reimplementarse aqui.
- **Context Baseline Evidence:** depends_on=WOT-2026-010e,WOT-2026-010q; motor_commits_010e=fec2766+b0248b1; motor_commit_010q=849e7d5; generated_at=2026-06-17.
- **Files Likely Touched:**
  - Builder: `scripts/pre_handoff_guard.py`
  - Builder: `scripts/scope_gate.py`
  - Builder: `scripts/check_deliverables_exist.py`
  - Builder: `scripts/encoding_post_write_hook.py`
  - Builder: `tests/test_pre_handoff_guard.py`
  - Builder: `tests/unit/test_scope_gate.py`
  - Builder: `tests/unit/test_check_deliverables_exist.py`
  - Builder: `tests/unit/test_encoding_post_write_hook.py`
  - Builder: `docs/protocol/review_packet_hardening_WOT-2026-010i.md`
  - Read/inspect only: `prompts/launch_builder.md`, `prompts/review_manager.md`, `prompts/audit_ticket_contract.md`, `.agent/runtime/pytest-safe/last-run.json`.
- **Forbidden Surfaces:** `scripts/run_pytest_safe.py`; cache pytest; xdist/sharding; politica de cierre Manager fuera del handoff; bus editado manualmente; `privada/`; `.env`.
- **DoD (criterios binarios de cierre):**
  - [ ] Un diff que toque una ruta de `Forbidden Surfaces` bloquea `--pre-handoff` o `--mark-ready` con diagnostico que nombre la ruta.
  - [ ] Un ticket `code` o `mixed` sin commit visible del ticket bloquea handoff con remediacion accionable.
  - [ ] Tickets `documentation`, `research` o `analysis` conservan el flujo documental cuando no tocan codigo.
  - [ ] Un test semantico prueba que `_resolve_destino()` retorna `destination_root`, no `motor_root`, cuando ambos campos difieren.
  - [ ] Un test de fallback observa el fallback real o su efecto, no un truco de entorno que el codigo anula internamente.
  - [ ] Diagnosticos de barrera son self-service.
  - [ ] Tests focales, ruff cuando aplique, encoding guard y validate 0/0 pasan al cierre.
- **Integracion cross-ticket:** desbloquea WOT-2026-010l; no mezclar con selector focal ni performance.
- **CONTRACT_GAP behavior:** si la barrera exige redisenar el contrato FLT completo, si rompe tickets documentales o si requiere cambiar `run_pytest_safe.py`, emitir CONTRACT_GAP y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar ante necesidad de relajar gates existentes, tocar bus manualmente, cambiar schema de `last-run.json`, o bloquear dirty tree fuera del handoff.
- **Depende de:** WOT-2026-010e (COMPLETED), WOT-2026-010q (COMPLETED).


## T-010L-001 -- Selector focal por diff con fail-open a suite canonica

- **ticket_id:** WOT-2026-010l
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010L-001
- **Plan-Link:** PLAN-010L-001
- **Premise:** `scripts/run_pytest_safe.py` ya acepta argumentos focales manuales y `010q` ya impide cerrar handoff con una corrida no canonica. Falta un selector conservador por diff/FLT para iteracion rapida del Builder, con fail-open explicito a la suite canonica completa cuando la cobertura no pueda justificarse.
- **Premise Re-check (read-only):**
  - verificar en `scripts/run_pytest_safe.py` como se distinguen `default_discovery` y `explicit_args`;
  - verificar como `scope_gate.get_changed_files()` y `pre_handoff_guard.get_changed_files()` resuelven el diff real;
  - releer `docs/test_performance/test_performance_baseline_WOT-2026-010j.md` y `docs/test_performance/test_performance_followup_WOT-2026-010k.md`;
  - confirmar que `010i` ya endurecio Forbidden Surfaces y commit-visible antes de introducir un atajo local;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** depends_on=WOT-2026-010j,WOT-2026-010i,WOT-2026-010q; source_report_010j=c05dbfe; hardening_010i=fdd55b6; handoff_gate_010q=849e7d5; generated_at=2026-06-17.
- **Files Likely Touched:**
  - Builder: `scripts/run_pytest_safe.py`
  - Builder: `scripts/test_selection.py`
  - Builder: `tests/unit/test_run_pytest_safe.py`
  - Builder: `tests/test_pre_handoff_guard.py`
  - Builder: `tests/unit/test_run_gates_dispatch.py`
  - Builder: `docs/test_performance/test_selection_WOT-2026-010l.md`
  - Read/inspect only: `pytest.ini`, `pyproject.toml`, `.agent/agent_controller.py`, `scripts/run_gates_dispatch.py`, `.agent/scope_gate.py`, `scripts/pre_handoff_guard.py`, `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`, `docs/test_performance/test_performance_followup_WOT-2026-010k.md`
- **Forbidden Surfaces:** cache de pytest; xdist/sharding; politica Manager/Builder de handoff; cambios al schema de `last-run.json`; pass-open silencioso; herramientas IA externas o SaaS; `privada/`; `.env`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Consume diff real y produce una lista reproducible de tests candidatos para iteracion.
  - [ ] Si `git diff` falla, si hay cambios en archivos troncales (`pyproject.toml`, `pytest.ini`, `.agent/**`), si el mapeo seguro no existe o si el conjunto resuelto es vacio, falla abierto a la suite canonica completa con razon auditable.
  - [ ] No cambia el contrato de cierre de `010c` ni debilita `010q`: el handoff sigue exigiendo `level=all` y `args_mode=default_discovery`.
  - [ ] Incluye tests de barrera para diff fallido, archivo troncal, resolucion vacia y mapeo parcial/inseguro.
  - [ ] Documenta como invocar el selector y como detectar cuando replega a suite canonica.
  - [ ] `ruff`, tests focales, encoding guard y `validate --json --project-root <repo_destino>` cierran en verde al handoff.
- **Integracion cross-ticket:** usa `010j` como evidencia de coste, `010i` como barrera de packet/scope y `010q` como red de seguridad del handoff. No mover estas responsabilidades de sitio.
- **CONTRACT_GAP behavior:** si el selector exige cambiar politica de closeout, ampliar el schema de `last-run.json` o relajar la suite canonica en handoff, emitir `CG-WOT-2026-010l.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el FLT requiere tocar un modulo distinto a los declarados; parar si el selector solo puede funcionar con pass-open silencioso; parar si la cobertura depende de heuristicas opacas no auditables; parar si el ticket deriva hacia cache, xdist o cambios de CI.
- **Depende de:** WOT-2026-010j (COMPLETED-VIA-010n), WOT-2026-010i (COMPLETED), WOT-2026-010q (COMPLETED).

## T-010R-001 -- Evaluacion de mattpocock/skills v1.0.0 contra taxonomia local

- **ticket_id:** WOT-2026-010r
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010R-001
- **Plan-Link:** PLAN-010R-001
- **Premise:** el release externo `mattpocock/skills@1.0.0` introduce una taxonomia `user-invoked/model-invoked` y vocabulario de diseno que pueden afectar la ruta de `WOT-2026-008c/008d`, pero adoptar esas ideas sin evaluar consumidores locales puede romper discovery, trigger_map o el flujo Builder/Manager.
- **External Source Baseline:** GitHub release `mattpocock/skills@1.0.0`; published_at=2026-06-17 14:45 UTC; release_commit=00ff03c; primary_change_commit=47bde84 as listed by the release page; license to verify from repo before recommending adoption.
- **Premise Re-check (read-only):**
  - verificar el release externo por `gh` si hay auth o por fetch web si `gh` no esta autenticado;
  - releer `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md`;
  - releer la cadena Plan 008 en `backlog.md`, en especial `008c`, `008d` y `008e`;
  - contar consumidores reales del campo `triggers` y de discovery local con `rg`, sin promover conteos provisionales a hechos sin comando reproducible;
  - confirmar que `disable-model-invocation` no existe aun en skills locales antes de proponer migracion.
- **Context Baseline Evidence:** source_ticket=WOT-2026-010g completed; release_tag=mattpocock-skills@1.0.0; release_commit=00ff03c; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder: `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
  - Read/inspect only: `CREDITS.md`
  - Read/inspect only: `.agent/docs/prompts_skills_inventory_WOT-2026-010g.md`
  - Read/inspect only: `skills/`
  - Read/inspect only: `prompts/`
  - Read/inspect only: `scripts/discover_skills.py`
  - Read/inspect only: `scripts/check_skill_collisions.py`
  - Read/inspect only: `scripts/local_audit.py`
  - Read/inspect only: `scripts/orquestador.py`
  - Read/inspect only: `scripts/validate_agent_config.py`
  - Read/inspect only: `bus/skill_resolver.py`
  - Read/inspect only: `.agent/collaboration/backlog.md`
  - Read/inspect only: `.agent/planning/ticket_contracts.md`
- **Forbidden Surfaces:** modificar skills o prompts locales; modificar discovery, resolver, bus, Manager review, `CREDITS.md`, `pyproject.toml`, `uv.lock`; copiar archivos del bundle externo; instalar dependencias externas; editar bus manualmente; `privada/`; `.env`.
- **DoD (criterios binarios de cierre):**
  - [ ] Existe `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md` en `repo_motor`.
  - [ ] El reporte separa `VERIFICADO` e `INFERENCIA` para cada claim relevante del release y de consumidores locales.
  - [ ] El reporte incluye tabla de piezas externas: `ask-matt`, `codebase-design`, `domain-modeling`, `diagnosing-bugs`, `writing-great-skills`, `resolving-merge-conflicts` y `docs/invocation.md`.
  - [ ] El reporte mapea impacto sobre `WOT-2026-008c`, `WOT-2026-008d`, `WOT-2026-010s` y `WOT-2026-010t`, con decision `adoptar`, `adaptar`, `rechazar` o `diferir`.
  - [ ] El reporte contiene inventario reproducible de consumidores locales de `triggers` y discovery, con comando exacto o limitacion explicita.
  - [ ] El reporte declara que `010r` no adopta ni porta nada; `CREDITS.md` queda como read-only y cualquier fila se difiere a `010s` o `010t` si adoptan ideas.
  - [ ] Si `gh` no esta autenticado, el reporte conserva el fallo literal y usa fetch web como fuente alternativa etiquetada.
  - [ ] Encoding guard pasa sobre el reporte y los artefactos del packet tocados.
  - [ ] `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.
- **Integracion cross-ticket:** `010r` es gate de decision para `010s` y `010t`, y debe informar la ejecucion de `008c/008d` sin bloquearlos por prosa.
- **CONTRACT_GAP behavior:** si el release no puede verificarse, si la licencia no puede confirmarse, si el impacto exige tocar codigo de discovery, o si el reporte no puede separar adopcion conceptual de portado de archivos, emitir `CG-WOT-2026-010r.md` y bloquear.
- **Builder clarification budget:** 0. El Builder no decide adopcion productiva; solo produce evidencia y recomendacion.
- **STOP conditions:** parar si aparece necesidad de modificar skills/prompts locales; parar si se propone instalar/copiar el bundle externo; parar si la unica fuente del release es un auto-reporte no verificable; parar si se necesita credencial GitHub para continuar y no hay fallback publico.
- **Depende de:** WOT-2026-010g (COMPLETED), WOT-2026-008b (COMPLETED).

## T-010T-001 -- Vocabulario de diseno profundo para review del Manager

- **ticket_id:** WOT-2026-010t
- **status:** frozen
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010T-001
- **Plan-Link:** PLAN-010T-001
- **Premise:** `WOT-2026-010r` concluyo que `mattpocock/skills v1.0.0` aporta vocabulario util de `codebase-design` para el Manager (`deep module`, `interface`, `seam`, `adapter`, `deletion test`) y que `diagnosing-bugs` puede complementar nuestro debugging sin reemplazar el limite local de 3 intentos. La adopcion debe ser conceptual y concreta en checklist, no una importacion de bundle ni una exigencia de nuevas abstracciones.
- **External Source Baseline:** usar el reporte `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md` como fuente local. Antes de escribir, re-anclar el origen externo: `v1.0.0` -> `dcfc232`; existe `v1.0.1` posterior. Si `v1.0.1` cambia `codebase-design` o `diagnosing-bugs`, documentarlo en el diff o emitir CONTRACT_GAP.
- **Premise Re-check (read-only):**
  - releer `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`;
  - verificar si `v1.0.1` cambia `skills/engineering/codebase-design` o `diagnosing-bugs` frente a `v1.0.0`;
  - leer `skills/man-review-implementation/references/review-checklist.md`;
  - leer `skills/_shared/anti-patterns.md` y `skills/_shared/ticket-anti-patterns.md`;
  - leer `skills/systematic-debugging/SKILL.md` para conservar el limite de 3 intentos;
  - encontrar un decision artifact o artefacto real existente donde ya aparezcan interface/seam/adapter sin inventar arquitectura nueva.
- **Context Baseline Evidence:** source_ticket=WOT-2026-010r completed; source_report_commit=42ee1fc; destino_closeout=5fa6b9a; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder: `skills/man-review-implementation/references/review-checklist.md`
  - Builder: `skills/_shared/anti-patterns.md`
  - Builder: `CREDITS.md`
  - Builder: `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`
  - Read/inspect only: `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`
  - Read/inspect only: `skills/_shared/ticket-anti-patterns.md`
  - Read/inspect only: `skills/systematic-debugging/SKILL.md`
  - Read/inspect only: `skills/man-review-implementation/SKILL.md`
  - Read/inspect only: `.agent/runtime/reviews/`
  - Read/inspect only: `.agent/collaboration/_archive/plan_audit/`
- **Forbidden Surfaces:** codigo Python; discovery/resolver/bus; `skills/` fuera de las dos rutas Builder declaradas; prompts; dependencias (`pyproject.toml`, `uv.lock`); copiar archivos del bundle externo; cambiar politica de debugging de 3 intentos; crear nuevas abstracciones productivas; bus editado manualmente; `privada/`; `.env`.
- **DoD (criterios binarios de cierre):**
  - [ ] `review-checklist.md` incluye preguntas accionables para `deep module`, `interface`, `seam`, `adapter`, `deletion test` y `interface is the test surface`.
  - [ ] `anti-patterns.md` incluye al menos un anti-patron nuevo o refinado que capture sobreingenieria por vocabulario (`seam/adapter` inventado) y lo diferencia de un seam real existente.
  - [ ] Existe `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md` con un ejemplo concreto aplicado a un artefacto real existente, preferiblemente el caso `WOT-2026-009b scope_gate`, sin inventar modulos nuevos.
  - [ ] El documento contrasta `diagnosing-bugs` con `skills/systematic-debugging/SKILL.md` y conserva explicitamente el limite de 3 intentos.
  - [ ] `CREDITS.md` incluye una fila para `WOT-2026-010t` con source pinneado y `Adapted`, no `Ported`.
  - [ ] El cambio no toca codigo ni modifica resolucion de skills.
  - [ ] Encoding guard pasa sobre todos los archivos tocados.
  - [ ] `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.
- **Integracion cross-ticket:** `010t` puede cerrar antes de `010s`; no cambia la taxonomia `user/model-invoked` ni el Plan 008. Su salida debe ayudar al Manager a revisar `010s/008c/008d` con mejor vocabulario.
- **CONTRACT_GAP behavior:** si el vocabulario solo puede aplicarse creando abstracciones nuevas, si `v1.0.1` invalida la base externa, si la fila CREDITS no puede pinnear fuente/licencia, o si tocar `review-checklist.md` obliga a normalizar encoding masivo no revisable, emitir `CG-WOT-2026-010t.md` y bloquear.
- **Builder clarification budget:** 0. El Builder adapta vocabulario a checklist y anti-patrones concretos; no decide cambios de arquitectura.
- **STOP conditions:** parar si hace falta tocar codigo; parar si se intenta copiar texto largo del repo externo; parar si el ejemplo de referencia no puede anclarse a un artefacto real; parar si el diff se convierte en re-encoding masivo no revisable.
- **Depende de:** WOT-2026-010r (COMPLETED).
## T-010S-001 -- Migracion hibrida user/model-invoked para skills

- **ticket_id:** WOT-2026-010s
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010S-001
- **Plan-Link:** PLAN-010S-001
- **Premise:** `WOT-2026-010r` recomendo adoptar la taxonomia user-invoked/model-invoked de forma hibrida. `triggers:` sigue siendo contrato vivo de dispatch; retirarlo ahora es breaking. `WOT-2026-010t` aporta AP-16 para evitar seams inventados durante esta migracion.
- **External Source Baseline:** `mattpocock/skills` `docs/invocation.md`, fuente pinneada por Builder antes del cambio. Usar MIT, Adapted, no bundle copiado. Si `v1.0.1` cambia materialmente la semantica, emitir CONTRACT_GAP.
- **Premise Re-check:** confirmar seis consumidores reales: `scripts/discover_skills.py`, `bus/skill_resolver.py`, `scripts/check_skill_collisions.py`, `scripts/local_audit.py`, `scripts/orquestador.py`, `scripts/validate_agent_config.py`; confirmar que `disable-model-invocation` aun no existe; capturar baseline de `trigger_map`.
- **Files Likely Touched:**
  - Builder: `scripts/discover_skills.py`
  - Builder: `bus/skill_resolver.py`
  - Builder: `scripts/check_skill_collisions.py`
  - Builder: `scripts/local_audit.py`
  - Builder: `scripts/orquestador.py`
  - Builder: `scripts/validate_agent_config.py`
  - Builder: `tests/test_discover_skills.py`
  - Builder: `tests/unit/test_skill_discovery.py`
  - Builder: `tests/test_check_skill_collisions.py`
  - Builder: `tests/test_approval_state_revision_and_skill_access.py`
  - Builder: `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`
  - Builder: `CREDITS.md`
- **Forbidden Surfaces:** removing `triggers:` from SKILL.md; prompts; bus runtime/events; dependency files; copied external bundle; `privada/`; `.env`.
- **DoD:** parse and expose `disable-model-invocation`; preserve `trigger_map` parity; resolver allowlists still work by name/trigger; tests cover true/absent/invalid field and parity; docs + CREDITS updated; no `triggers:` removal; validate 0/0.
- **CONTRACT_GAP behavior:** stop if safe migration requires removing `triggers:`, changing prompts, installing deps, or rewriting discovery architecture beyond the six declared consumers.
- **Builder clarification budget:** 0. Implement hybrid compatibility only.
- **Depende de:** WOT-2026-010r (COMPLETED), WOT-2026-010t (COMPLETED).
## T-010U-001 -- Guard fail-closed para archivado de plan/audit en limbo

- **ticket_id:** WOT-2026-010u
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010U-001
- **Plan-Link:** PLAN-010U-001
- **Premise:** El archivador mueve artefactos cerrados a `_archive/plan_audit/` pero el rename puede quedar sin commit (`D old` + `?? new`). La contaminacion se detecta tarde en el siguiente ticket. La solucion elegida es guard fail-closed con remediacion, no auto-commit.
- **Premise Re-check:** confirmar `archive_collaboration_artifacts.py` usa move sin commit; confirmar sitios de deteccion existentes; reproducir limbo en repo git real.
- **Files Likely Touched:**
  - Builder: `scripts/archive_collaboration_artifacts.py`
  - Builder: `.agent/agent_controller.py`
  - Builder: `scripts/pre_handoff_guard.py`
  - Builder: `scripts/delivery_hygiene_check.py`
  - Builder: `tests/test_pre_handoff_guard.py`
  - Builder: `tests/test_archive_collaboration_artifacts.py`
  - Builder: `tests/unit/test_delivery_hygiene_check.py`
  - Builder: `docs/protocol/archive_rename_hygiene_WOT-2026-010u.md`
- **Forbidden Surfaces:** bus runtime/events; destructive deletion of archived artifacts; dependency files; auto-commit inside archiver; `privada/`; `.env`.
- **DoD:** test reproduces limbo delete+untracked; guard blocks with stable reason and remediation; no auto-commit; artifacts preserved as rename; tests/ruff/encoding/validate pass.
- **CONTRACT_GAP behavior:** stop if fix requires auto-commit or destructive deletion.
- **Builder clarification budget:** 0. Implement guard fail-closed, not policy redesign.
- **Depende de:** WOT-2026-010s (COMPLETED).

## T-008C-001 -- INDEX generado por discovery recursivo de prompts y skills

- **ticket_id:** WOT-2026-008c
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008C-001
- **Plan-Link:** PLAN-008C-001
- **Premise:** `WOT-2026-008b` cerro `DEC-008B-001` con Opcion 4: discovery recursivo sin manifest. `008c` debe formalizar `docs/registry/INDEX.md` como proyeccion generada por discovery y anadir stale-check. No debe crear `registry.json` ni manifest central.
- **Premise Re-check (read-only):**
  - verificar que `WOT-2026-008b` esta completado;
  - releer `docs/decisions/DEC-008B-001-registry-model.md` y confirmar Opcion 4;
  - inspeccionar `docs/registry/INDEX.md`, `docs/registry/README.md`, `scripts/discover_skills.py`, `scripts/check_skill_collisions.py` y tests existentes;
  - confirmar el comando vivo que genera el indice, empezando por `scripts/discover_skills.py --generate-index`;
  - confirmar que `disable-model-invocation` de `010s` no rompe `trigger_map` ni el indice.
- **Context Baseline Evidence:** depends_on=WOT-2026-008b completed; DEC-008B-001=ADOPTED Opcion 4; CG-WOT-2026-008c resolved by re-scope; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/discover_skills.py`
  - Builder repo_motor: `scripts/check_skill_collisions.py`
  - Builder repo_motor: `docs/registry/README.md`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `tests/test_registry_catalog.py`
  - Builder repo_motor: `tests/test_discover_skills.py`
  - Builder repo_motor: `tests/test_check_skill_collisions.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008B-001-registry-model.md`; `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md`; `docs/skills_taxonomy/mattpocock_v1_impact_WOT-2026-010r.md`; `skills/`; `prompts/`; `scripts/local_audit.py`; `scripts/validate_agent_config.py`; `bus/skill_resolver.py`.- **Forbidden Surfaces:** crear `registry.json` o manifest central; mover, renombrar o borrar carpetas de prompts/skills; retirar `triggers:`; copiar bundles externos; instalar dependencias; tocar `pyproject.toml` o `uv.lock`; editar bus runtime/events manualmente; `privada/`; `.env`; migrar shims de `008d`.
- **DoD (criterios binarios de cierre):**
  - [ ] `docs/registry/INDEX.md` se genera desde `discover_skills.py --generate-index` o comando equivalente ya existente en discovery.
  - [ ] Existe un stale-check que falla si `INDEX.md` diverge del output generado.
  - [ ] El check no crea ni requiere `registry.json`.
  - [ ] El indice generado cubre las skills descubiertas y conserva metadata relevante ya soportada por discovery, incluido `status`, `triggers` y `disable-model-invocation` cuando aplique.
  - [ ] `docs/registry/README.md` documenta que el modelo vigente es discovery recursivo sin manifest central.
  - [ ] Se distingue layout fisico de alias logico; no se ejecuta ninguna migracion de naming/shims de `008d`.
  - [ ] Discovery/collision conservan paridad observable o documentan por que quedan read-only.
  - [ ] Tests focales, ruff, encoding guard, suite canonica y `validate --json --project-root <repo_destino>` terminan en verde.
- **Integracion cross-ticket:** `008c` desbloquea `008d` y `008f`. Debe incorporar el aprendizaje de `010s` como metadata aditiva, sin reabrir la taxonomia externa.
- **CONTRACT_GAP behavior:** si el INDEX no puede derivarse de discovery, si aparece consumidor vivo no clasificable, si el cambio exige crear `registry.json`, si exige migrar nombres/shims, o si el stale-check solo puede ser pass-open, emitir `CG-WOT-2026-008c.md` y bloquear.
- **Builder clarification budget:** 0. Las decisiones abiertas se registran como notas o follow-ups; no se pide al humano durante Builder salvo CONTRACT_GAP real.
- **STOP conditions:** parar si se requiere crear manifest central; parar si se requiere mover/renombrar/borrar prompts o skills; parar si se necesita tocar dependencias o bus; parar si se reabre la decision `DEC-008B-001` sin contrato nuevo.
- **Depende de:** WOT-2026-008b (COMPLETED).
## T-008D-001 -- Convencion de naming de prompts/skills con shims versionados

- **ticket_id:** WOT-2026-008d
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008D-001
- **Plan-Link:** PLAN-008D-001
- **Premise:** `WOT-2026-008c` cerro el INDEX generado sin `registry.json`. La migracion de naming debe operar sobre discovery/frontmatter/check-contract existentes, no sobre manifest central. Renombrar prompts o skills sin DEC congelada rompe `source_prompt`, `contract_id`, docs y consumidores externos.
- **Premise Re-check (read-only):**
  - verificar que `WOT-2026-008c` esta completado;
  - releer `docs/registry/README.md` y `docs/registry/INDEX.md` generados;
  - inspeccionar `scripts/discover_skills.py --check-contract` y `scripts/check_skill_collisions.py`;
  - localizar prompts/skills piloto con `source_prompt` vivo y referencias prose vivas antes de proponer rename;
  - confirmar si `audit_plan.md` sigue siendo stub-alias vivo y usarlo como patron de compatibilidad, no como caso a borrar; revalidar la premisa contra 010s y confirmar que naming lexico es ortogonal a `disable-model-invocation`.
- **Context Baseline Evidence:** depends_on=WOT-2026-008c completed; naming_discussion=2026-06-18; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `docs/decisions/DEC-008D-001-naming-convention.md`
  - Builder repo_motor: `docs/registry/README.md`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: prompts piloto y stubs legacy versionados
  - Builder repo_motor: skills piloto que referencian esos prompts por `source_prompt`
  - Builder repo_motor: `scripts/discover_skills.py`
  - Builder repo_motor: `scripts/run_gates_dispatch.py`
  - Builder repo_motor: tests de discovery, contract-check, naming, gate-dispatch, collision e INDEX si aplica
  - Read/inspect only: `scripts/check_skill_collisions.py` (no editar salvo que la DEC descarte explicitamente `discover_skills.py --check-naming` como autoridad)
  - Read/inspect only: `scripts/check_ticket_nomenclature.py`
  - Read/inspect only: `scripts/validate_ticket_prose.py`
  - Read/inspect only: `skills/`
  - Read/inspect only: `prompts/`
- **Forbidden Surfaces:** crear `registry.json` o manifest central; migracion masiva; mover carpetas completas de prompts/skills; retirar shims sin scan reproducible; romper `source_prompt`; tocar bus runtime/events; tocar dependencias; `privada/`; `.env`.
- **DoD (criterios binarios de cierre):**
  - [ ] Existe DEC de naming congelada como primer entregable de 008d y antes de cualquier rename.
  - [ ] La DEC fija patrones por tipo: prompts `snake_case`, skills `kebab-case`, scripts CLI verbo primero (`check_*`, `generate_*`, `validate_*`, `discover_*`, `archive_*`, `run_*`), shims/stubs versionados, prefijos de rol (`man`/`bui` vs `manager`/`builder`) y ortogonalidad con `disable-model-invocation`.
  - [ ] Si hay piloto de rename, el prompt, su frontmatter `source_prompt` y todas las referencias prose vivas en prompts/skills operativos se actualizan atomicamente.
  - [ ] Existe shim/stub legacy para cada nombre publico antiguo tocado, con retirada asignada a `008e`; la DEC define si el shim es alias documental o prompt ejecutable, y como conserva `source_prompt`/`contract_id` sin romper `--check-contract`.
  - [ ] `python scripts/discover_skills.py --check-contract` queda verde.
  - [ ] `python scripts/check_skill_collisions.py` queda verde.
  - [ ] Antes del piloto, capturar baseline de `python scripts/discover_skills.py --check-contract`, `python scripts/check_skill_collisions.py` y `python scripts/discover_skills.py --json`; despues del piloto, repetirlos y demostrar paridad salvo renames/aliases declarados en la DEC.
  - [ ] El INDEX generado expone `canonical_name`, `legacy_aliases` y `naming_status` o campos equivalentes; la fuente es frontmatter (`legacy_aliases:`) o derivacion por filename en `discover_skills.py`, sin sidecar JSON ni manifest central.
  - [ ] `rg` de nombres antiguos solo aparece en shims, docs historicas/deprecacion, changelog/backlog o tests de compatibilidad.
  - [ ] Existe `discover_skills.py --check-naming` antes del cierre, con test que bloquea fail-closed un nombre fuera de convencion; si se crea `check_naming_convention.py` o se extiende `check_skill_collisions.py`, la DEC lo justifica con evidencia de por que no encaja en discovery.
  - [ ] `scripts/run_gates_dispatch.py` invoca `discover_skills.py --check-naming` (o equivalente decidido por la DEC) en los perfiles aplicables; tests focales, ruff/format si toca Python, encoding guard, handoff verde (incluida barrera 010u archival-rename), suite canonica y `validate --json --project-root <repo_destino>` terminan en verde.
- **Integracion cross-ticket:** desbloquea `008e`; no debe mezclar lifecycle operativo de `008f` ni performance/CI. Debe preservar lo aprendido en `010s` y `010t`.
- **STOP conditions:** parar si `role: auditor` rompe `_check_contract()` de `manager|builder` y no puede resolverse sin ampliar scope; parar si discovery usa `role` con semantica incompatible y requiere rediseno mayor; parar si aparecen skills adicionales ambiguas fuera de las cinco declaradas; parar si el cambio deriva a rename de directorios o prompts; parar si el WIP en disco no puede reconciliarse con el contrato sin tocar superficies fuera de FLT.
- **Builder clarification budget:** 0. El Builder no decide la convencion por intuicion: primero DEC, despues piloto minimo.
- **STOP conditions:** parar si no hay DEC; parar si el rename elegido no tiene shim seguro; parar si el cambio deja referencias legacy vivas fuera de superficies permitidas; parar si exige gate nuevo sin justificar por que no basta `discover_skills.py --check-naming`; parar si deja `discover_skills.py` como read-only mientras exige modificarlo; parar si intenta poner la logica de naming dentro de `pre_handoff_guard` en vez de los quality gates; parar si no se revalida la premisa contra 010s; parar si la DEC no fija prefijos de rol.
- **Depende de:** WOT-2026-008e (COMPLETED); WOT-2026-008c satisfecho como premisa tecnica.
## T-008E-001 -- Rename versionado review_manager -> manager_review

- **ticket_id:** WOT-2026-008e
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008E-001
- **Plan-Link:** PLAN-008E-001
- **Premise:** `WOT-2026-008d` cerro `DEC-008D-001` y dejo `review_manager` como excepcion legacy temporal. `008e` ejecuta el rename versionado y retira esa excepcion sin romper `source_prompt`, prose viva ni discovery.
- **Premise Re-check:** confirmar `008d` COMPLETED; leer `DEC-008D-001`; ejecutar baseline `discover_skills.py --check-naming`, `--check-contract`, `check_skill_collisions.py`, `discover_skills.py --json`; ejecutar `rg "review_manager|manager_review" prompts skills scripts docs tests --glob "!**/sandbox/**"`.
- **Files Likely Touched:**
  - Builder repo_motor: `prompts/review_manager.md`
  - Builder repo_motor: `prompts/manager_review.md`
  - Builder repo_motor: `skills/man-review-implementation/SKILL.md`
  - Builder repo_motor: `skills/audit-pipeline/SKILL.md`
  - Builder repo_motor: `skills/orchestrate-pipeline/SKILL.md`
  - Builder repo_motor: `prompts/audit_complete_motor_destination.md`
  - Builder repo_motor: `prompts/audit_pipeline.md`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_motor: `scripts/discover_skills.py`
  - Builder repo_motor: `tests/test_check_naming.py`
  - Builder repo_motor: `tests/test_discover_skills.py`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `docs/registry/README.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/check_skill_collisions.py`, `scripts/run_gates_dispatch.py`, `scripts/pre_handoff_guard.py`, bus runtime/events, `docs/decisions/DEC-008D-001-naming-convention.md`.
- **Forbidden Surfaces:** editar bus runtime/events manualmente; crear manifest central o sidecar JSON; tocar dependencias; modificar `pre_handoff_guard.py`; ampliar el rename a otros prompts/skills; borrar el prompt legacy sin stub.
- **DoD:**
  - [ ] `prompts/manager_review.md` es la fuente canonica del prompt y estrena el patron de frontmatter YAML en prompts usando `parse_frontmatter()` existente.
  - [ ] `prompts/manager_review.md` incluye `legacy_aliases: [review_manager]` y conserva en el cuerpo, como texto buscable, las lineas literales `Skill canonica: skills/man-review-implementation/SKILL.md` y `contract_id: cid-man-review-v2`.
  - [ ] `prompts/review_manager.md` queda como stub-alias compatible estilo `audit_plan.md`; `audit_plan.md` es precedente solo de forma de stub, no del mecanismo de tolerancia.
  - [ ] Consumidores vivos declarados en DEC (`man-review-implementation`, `audit-pipeline`, `orchestrate-pipeline`, `audit_complete_motor_destination`, `audit_pipeline`, `orchestrator_pipeline`) quedan actualizados o documentan explicitamente el alias sin romper `--check-contract`.
  - [ ] `KNOWN_LEGACY_NAMES` ya no contiene `review_manager`; `--check-naming` tolera el stub solo por `legacy_aliases` del canonico parseado con `parse_frontmatter()` y tiene test de parse real de prompt con frontmatter.
  - [ ] `--check-contract`, `check_skill_collisions.py`, `--check-naming` y `discover_skills.py --json` pasan; trigger_map conserva paridad funcional.
  - [ ] `discover_skills.py --generate-index` actualiza `docs/registry/INDEX.md` y `discover_skills.py --check-index` queda verde.
  - [ ] `rg "review_manager" prompts skills scripts docs tests --glob "!**/sandbox/**"` solo devuelve stub, legacy_aliases, docs historicas/deprecacion o tests de compatibilidad.
  - [ ] Tests focales, ruff/format, encoding guard, run_pytest_safe --level all y validate --json 0/0 pasan.
- **CONTRACT_GAP behavior:** si aparecen consumidores vivos adicionales de alto riesgo, si el stub no puede mantener compatibilidad, o si el rename rompe `--check-contract`, emitir `CG-WOT-2026-008e.md` y bloquear.
- **STOP conditions:** parar si no hay baseline; parar si hay mas de 6 consumidores vivos no declarados; parar si se intenta borrar el alias legacy sin stub; parar si se toca bus/runtime.
- **Depende de:** WOT-2026-008d (COMPLETED).

## T-008F-001 -- Gate de integracion destino-motor y lifecycle operativo

- **ticket_id:** WOT-2026-008f
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008F-001
- **Plan-Link:** PLAN-008F-001
- **Premise:** el engranaje destino-motor y la preparacion operativa del destino ya estan cubiertos por piezas separadas (`destination_context.py`, `check_destino_publish_ready.py`, `classify_publication.py`, validaciones de autoridad/topologia), pero no existe una entrada unica que las orqueste de punta a punta sin duplicar logica. `validate_authority.main()` sigue siendo CLI-only para el motor; el ticket debe reutilizar sus helpers y no asumir que `main()` valida un `project_root` arbitrario.
- **Premise Re-check:** confirmar `008e` COMPLETED y `008c` satisfecho como premisa tecnica; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`; ejecutar `python scripts/check_destino_publish_ready.py --project-root <repo_destino> --motor-root <repo_motor>`; leer `scripts/destination_context.py`, `scripts/check_destino_publish_ready.py`, `scripts/classify_publication.py` y `scripts/validate_authority.py` para confirmar que el valor del ticket esta en la integracion, no en crear validadores paralelos.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/check_motor_destination_integration.py`
  - Builder repo_motor: `tests/test_check_motor_destination_integration.py`
  - Builder repo_motor: `docs/protocol/motor_destination_integration_WOT-2026-008f.md`
  - Builder repo_motor: `scripts/destination_context.py`
  - Builder repo_motor: `scripts/check_destino_publish_ready.py`
  - Builder repo_motor: `scripts/classify_publication.py`
  - Builder repo_motor: `scripts/validate_authority.py`
  - Builder repo_motor: `tests/test_destination_context.py`
  - Builder repo_motor: `tests/test_prepush_check.py`
  - Builder repo_motor: `tests/test_classify_publication.py`
  - Builder repo_motor: `prompts/destination_bootstrap.md`
  - Builder repo_motor: `prompts/audit_git_publication.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/install_agent_system.py`, `.agent/agent_controller.py`, `.agent/config/motor_destination_link.json`, `MANIFEST.distribute`, `MANIFEST.workspace`, `prompts/orchestrator_pipeline.md`, `prompts/audit_complete_motor_destination.md`, `tests/test_motor_root_gates.py`, bus runtime/events.
- **Forbidden Surfaces:** editar bus runtime/events manualmente; duplicar scanners de secretos o `validate`; mutar un destino real para probar guards/settings; tocar dependencias; redisenar `install_agent_system.py` o el launcher como parte de este ticket.
- **DoD:**
  - [ ] Existe `python scripts/check_motor_destination_integration.py --project-root <repo_destino> [--motor-root <repo_motor>]` con diagnostico self-service y exit codes documentados.
  - [ ] El wrapper reutiliza checks existentes cuando existen; no duplica la logica de `classify_publication.py`, `check_destino_publish_ready.py`, `destination_context.py` ni validaciones de autoridad/topologia ya presentes.
  - [ ] destination_context.py, check_destino_publish_ready.py, classify_publication.py y validate_authority.py solo pueden cambiarse para extraer helpers exportables sin alterar su contrato CLI; el wrapper delega via import, no via copia ni reescritura de su logica central.
  - [ ] El wrapper valida que `motor_destination_link.json` resuelve `motor_root` y `destination_root` coherentes con el contrato y falla cerrado ante link ausente o invalido, aunque `resolve_motor_link()` hoy solo garantice `motor_root`.
  - [ ] El wrapper distingue gate operativo pre-push de auditoria de primera publicacion; la auditoria historica solo corre con flag explicito y sigue siendo dry-run.
  - [ ] El wrapper demuestra que el contexto destino puede resolver el lifecycle/registry del motor sin depender de escribir sobre un destino real.
  - [ ] Las pruebas reproducen al menos: link roto, fallo propagado desde `check_destino_publish_ready`, modo auditoria opcional y fallo cerrado de autoridad/version/manifest sobre fixture o tmp.
  - [ ] Si se tocan prompts/destination_bootstrap.md o prompts/audit_git_publication.md, el cambio se limita a una referencia minima al wrapper nuevo y no reescribe su flujo operativo.
  - [ ] `ruff`, tests focales reales, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` pasan en verde.
- **CONTRACT_GAP behavior:** si el wrapper exige reimplementar scanners/validate, si la unica forma de probar guards requiere mutar un destino real, si obliga a cambiar la logica central o el contrato CLI de scripts ya vivos, o si la separacion entre gate operativo y auditoria de primera publicacion no puede mantenerse, emitir `CG-WOT-2026-008f.md` y bloquear.
- **STOP conditions:** parar si el wrapper reimplementa scanners de secretos o `validate`; parar si requiere escribir en `repo_destino` real para probar guards; parar si obliga a cambiar la logica central o el contrato CLI de scripts ya vivos en vez de delegar; parar si aparece dependencia nueva; parar si el cambio deriva en redisenar `install_agent_system.py` o el launcher.
- **Depende de:** WOT-2026-008e (COMPLETED); WOT-2026-008c satisfecho como premisa tecnica.
## T-008G-001 -- DEC de vocabulario y naming por rol

- **ticket_id:** WOT-2026-008g
- **status:** frozen
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008G-001
- **Plan-Link:** PLAN-008G-001
- **Premise:** el sistema usa "agente" para mezclar backends IA, roles y artefactos. `audit_*` es familia transversal de tarea, no propiedad del rol auditor. `supervisor` ya existe como actor runtime del bus. Sin una DEC nueva, los renames posteriores no tienen contrato verificable.
- **Premise Re-check (read-only):**
  - confirmar WOT-2026-008f COMPLETED;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`;
  - inventariar `prompts/*.md` y confirmar 21 archivos fisicos;
  - leer `docs/decisions/DEC-008D-001-naming-convention.md` y documentar que 008g formaliza un mecanismo implicito en `_PIPELINE_ACTIONS` / `--check-naming`;
  - verificar `bus/supervisor.py` y ocurrencias `actor="SUPERVISOR"` para documentar supervisor como runtime.
- **Context Baseline Evidence:** 008f_state=COMPLETED; prompts_fisicos=21; prompts_canonicos=19; prompts_stubs=2; skills_man_bui=8 dirs; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`
  - Builder repo_motor: `AGENTS.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
  - Read/inspect only: `prompts/`, `skills/`, `bus/supervisor.py`, `.agent/agent_controller.py`, `docs/decisions/DEC-008D-001-naming-convention.md`, `scripts/discover_skills.py`
- **Forbidden Surfaces:** renombrar prompts/skills/scripts; modificar frontmatter; tocar WOT-2026-008f; expandir `man-`/`bui-`; tocar bus runtime/events; dependencias; `privada/`; `.env`.
- **DoD:**
  - [ ] Existe `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`.
  - [ ] La DEC contiene vocabulario canonico, roles canonicos, supervisor-runtime, regla actor/family, criterio de desempate, tabla congelada de prompts y plan de lotes.
  - [ ] La tabla clasifica 21 prompts fisicos: 6 `orchestrator_*` relacionados (5 futuros renames y `orchestrator_pipeline.md` ya canonico), 1 `manager_*`, 11 `audit_*` family, 1 `memory_*` family, 1 `contract_formation_*` family y 2 stubs legacy (`audit_plan.md`, `review_manager.md`).
  - [ ] La DEC formaliza `audit_*` como familia transversal y no fuerza `auditor_*` para prompts multi-rol.
  - [ ] AGENTS.md contiene la seccion "Backends y roles".
  - [ ] `python scripts/discover_skills.py --check-naming` pasa.
  - [ ] Encoding guard pasa sobre DEC y AGENTS.md.
  - [ ] `validate --json --project-root <repo_destino>` termina en 0 errors / 0 warnings.
  - [ ] El diff del repo_motor se limita a DEC + AGENTS.md; no hay renames ni frontmatter.
- **CONTRACT_GAP behavior:** si algun prompt no puede clasificarse con actor/family, si AGENTS.md exige reescritura amplia, si la DEC requiere codigo/runtime, o si la tabla contradice el inventario real, emitir `CG-WOT-2026-008g.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si aparece rename, frontmatter edit, cambio de bus/runtime, dependencia nueva o cambio productivo ajeno a DEC/AGENTS.md.
- **Depende de:** WOT-2026-008f (COMPLETED), WOT-2026-008d (COMPLETED), WOT-2026-008e (COMPLETED).
## T-008H-001 -- Rename versionado de 5 prompts orchestrator con shims

- **ticket_id:** WOT-2026-008h
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008H-001
- **Plan-Link:** PLAN-008H-001
- **Premise:** `DEC-008G-001` ya congelo que cinco prompts deben migrar a nombres `orchestrator_*` y que `orchestrator_pipeline.md` ya es canonico y no se renombra. El ticket debe ejecutar el rename versionado con stubs y actualizar consumidores vivos sin tocar bus/runtime.
- **Premise Re-check:** confirmar `008g` COMPLETED; ejecutar baseline `python scripts/discover_skills.py --check-naming`, `python scripts/discover_skills.py --json`, `python scripts/discover_skills.py --check-index`; ejecutar `rg "prompts/(launch_builder|session_bootstrap|session_close_chat|destination_bootstrap|refactor_bootstrap)\.md" skills prompts scripts docs README.md QUICKSTART.md AGENTS.md CLAUDE.md MANIFEST.distribute llms.txt llms-full.txt tests`; confirmar que `launch_builder.md` sigue siendo exception lexical y que por eso la prueba de migracion NO puede descansar solo en `--check-naming`.
- **Context Baseline Evidence:** old_prompt_paths=5; canonical_new_paths=5; source_prompt_live=skills/bui-implement-from-plan/SKILL.md; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `prompts/launch_builder.md`
  - Builder repo_motor: `prompts/orchestrator_launch_builder.md`
  - Builder repo_motor: `prompts/session_bootstrap.md`
  - Builder repo_motor: `prompts/orchestrator_session_bootstrap.md`
  - Builder repo_motor: `prompts/session_close_chat.md`
  - Builder repo_motor: `prompts/orchestrator_session_close_chat.md`
  - Builder repo_motor: `prompts/destination_bootstrap.md`
  - Builder repo_motor: `prompts/orchestrator_destination_bootstrap.md`
  - Builder repo_motor: `prompts/refactor_bootstrap.md`
  - Builder repo_motor: `prompts/orchestrator_refactor_bootstrap.md`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_motor: `prompts/audit_complete_motor_destination.md`
  - Builder repo_motor: `prompts/audit_git_publication.md`
  - Builder repo_motor: `skills/bui-implement-from-plan/SKILL.md`
  - Builder repo_motor: `skills/orchestrate-pipeline/SKILL.md`
  - Builder repo_motor: `skills/setup-agent-system/SKILL.md`
  - Builder repo_motor: `skills/setup-agent-system/references/quickstart-checklist.md`
  - Builder repo_motor: `skills/refactor-manager/SKILL.md`
  - Builder repo_motor: `scripts/build_llms.py`
  - Builder repo_motor: `MANIFEST.distribute`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `README.md`
  - Builder repo_motor: `QUICKSTART.md`
  - Builder repo_motor: `AGENTS.md`
  - Builder repo_motor: `CLAUDE.md`
  - Builder repo_motor: `llms.txt`
  - Builder repo_motor: `llms-full.txt`
  - Builder repo_motor: `tests/test_migration_bootstrap.py`
  - Builder repo_motor: `tests/test_check_naming.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`, `scripts/discover_skills.py`, `bus/runtime/events`, `CHANGELOG.md`, historicos en docs/tests no declarados.
- **Forbidden Surfaces:** renombrar `prompts/orchestrator_pipeline.md`; tocar `man-*`/`bui-*`; tocar bus/runtime/events; tocar dependencias; editar frontmatter fuera de lo estrictamente necesario para `source_prompt`; tocar `privada/` o `.env`.
- **DoD:**
  - [ ] Existen los cinco prompts canonicos nuevos `orchestrator_*` y contienen el cuerpo operativo canonico.
  - [ ] Los cinco nombres viejos sobreviven como stubs/aliases de compatibilidad; no se borran.
  - [ ] `skills/bui-implement-from-plan/SKILL.md` actualiza `source_prompt` al nombre canonico nuevo.
  - [ ] Los consumidores vivos declarados en FLT usan el nombre canonico nuevo o documentan explicitamente el stub cuando procede.
  - [ ] `orchestrator_pipeline.md` permanece sin rename y sus referencias a prompts renombrados quedan actualizadas.
  - [ ] `MANIFEST.distribute`, `docs/registry/INDEX.md`, `llms.txt`, `llms-full.txt`, `README.md`, `QUICKSTART.md`, `AGENTS.md` y `CLAUDE.md` quedan alineados a los nombres canonicos donde aplique.
  - [ ] La prueba de migracion NO descansa solo en `--check-naming`; tambien se verifica por `rg` de consumidores vivos, stubs presentes y `source_prompt` actualizado.
  - [ ] `python scripts/discover_skills.py --check-naming`, `python scripts/discover_skills.py --check-index`, encoding guard, tests focales reales, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` pasan en verde.
- **CONTRACT_GAP behavior:** si algun prompt viejo no puede mantenerse como stub, si aparece un consumidor vivo no declarado de alto riesgo, si el rename exige tocar runtime/bus o si la compatibilidad requiere un cambio de gate no previsto, emitir `CG-WOT-2026-008h.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si falta baseline; parar si el rename se extiende a `orchestrator_pipeline.md`; parar si el cambio deriva a migracion de skills `man-*`/`bui-*`; parar si la unica evidencia de migracion es `--check-naming`.
- **Depende de:** WOT-2026-008g (COMPLETED).

## T-008K-001 -- Formalizar role: auditor en skills auditoras

- **ticket_id:** WOT-2026-008k
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008K-001
- **Plan-Link:** PLAN-008K-001
- **Premise:** `DEC-008G-001` congelo que `audit_*` en prompts es familia transversal, pero dejo serializado `008k` para formalizar `role: auditor` en las skills cuya propiedad real es el rol auditor. Opcion B hace visible ese rol en el catalogo como campo separado de `owner`, sin cambiar la semantica de `owner`.
- **Premise Re-check:** confirmar `WOT-2026-008g` y `WOT-2026-008h` COMPLETED; documentar que `008i` y `008j` quedan diferidos segun `DEC-008G-001`; releer `DEC-008G-001` secciones de vocabulario/roadmap; ejecutar `git status --short` en `repo_motor` y documentar que ya existe WIP parcial en `scripts/discover_skills.py`, cinco `SKILL.md` y `docs/registry/INDEX.md`; inventariar `skills/audit-git-publication`, `skills/audit-pipeline`, `skills/code-audit`, `skills/local-audit`, `skills/system-health-audit`; verificar el `role:` actual en frontmatter; leer `scripts/discover_skills.py` para confirmar que `auditor` ya entro en `_check_contract()` y que `_derive_owner()` sigue derivando de `author`/`role`.
- **Context Baseline Evidence:** roadmap_source=DEC-008G-001; audit_skill_count=5; manager_contract_validated=3; shared_without_source_prompt=2; builder_self_audit_excluded=true; catalog_role_column_required=true; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `skills/audit-git-publication/SKILL.md`
  - Builder repo_motor: `skills/audit-pipeline/SKILL.md`
  - Builder repo_motor: `skills/code-audit/SKILL.md`
  - Builder repo_motor: `skills/local-audit/SKILL.md`
  - Builder repo_motor: `skills/system-health-audit/SKILL.md`
  - Builder repo_motor: `scripts/discover_skills.py`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `docs/registry/README.md`
  - Builder repo_motor: `tests/test_discover_skills.py`
  - Builder repo_motor: `tests/test_check_naming.py`
  - Builder repo_motor: `tests/test_registry_catalog.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`; `skills/bui-self-audit/SKILL.md`; `prompts/audit_*.md`; `scripts/check_skill_collisions.py`; `scripts/run_gates_dispatch.py`; `bus/runtime/events`.
- **Forbidden Surfaces:** renombrar skills o prompts; tocar `skills/bui-self-audit/SKILL.md`; mover `audit_*` prompts a `auditor_*`; tocar bus/runtime/events manualmente; tocar dependencias; expandir `man-*`/`bui-*`; cambiar la semantica de `owner`; editar `source_prompt`/`contract_id` salvo que una prueba demuestre necesidad contractual real dentro de las tres skills contract-validated.
- **DoD:**
  - [ ] Las cinco skills auditoras declaradas en FLT usan `role: auditor` en frontmatter.
  - [ ] `skills/bui-self-audit/SKILL.md` conserva `role: builder`; no se reclasifica por el nombre.
  - [ ] `scripts/discover_skills.py` acepta y proyecta `role: auditor`, mantiene `auditor` en el opt-in de `_check_contract()`, y expone `role` como campo separado de `owner`.
  - [ ] `audit-git-publication`, `audit-pipeline` y `system-health-audit` conservan validacion de `source_prompt` y `contract_id` despues del cambio.
  - [ ] `docs/registry/INDEX.md` refleja `role` en columna separada y conserva `owner` con la semantica previa.
  - [ ] `tests/test_registry_catalog.py` exige el nuevo campo `role` y conserva los required fields anteriores.
  - [ ] Si `docs/registry/README.md` documenta roles/ownership/catalogo, queda alineado con la separacion `owner` vs `role`.
  - [ ] `python scripts/discover_skills.py --check-naming`, `--check-contract`, `--check-index` y `python scripts/check_skill_collisions.py` pasan en verde.
  - [ ] `python scripts/discover_skills.py --json` o evidencia equivalente demuestra que las cinco skills auditoras salen clasificadas coherentemente, con `role` visible y `bui-self-audit` fuera.
  - [ ] Tests focales reales cubren al menos: aceptacion de `role: auditor`, inclusion de `auditor` en `_check_contract()`, exclusion de `bui-self-audit`, required fields del catalogo con `role`, y no regresion del contrato `manager|builder` existente.
  - [ ] `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **CONTRACT_GAP behavior:** si formalizar `auditor` exige renombrar prompts `audit_*`, ampliar este ticket a `man-*`/`bui-*`, reescribir el contrato de `source_prompt` fuera de las tres skills contract-validated, o cambiar la semantica de `owner` mas alla de anadir `role` como campo separado, emitir `CG-WOT-2026-008k.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si `role: auditor` rompe `_check_contract()` de `manager|builder` y no puede resolverse sin ampliar scope; parar si discovery usa `role` con semantica incompatible y requiere rediseno mayor; parar si aparecen skills adicionales ambiguas fuera de las cinco declaradas; parar si el cambio deriva a rename de directorios o prompts; parar si el WIP en disco no puede reconciliarse con el contrato sin tocar superficies fuera de FLT.
- **Depende de:** WOT-2026-008g (COMPLETED); WOT-2026-008h (COMPLETED).
## T-008I-001 -- Rename atomico de 4 skills manager a manager-*

- **ticket_id:** WOT-2026-008i
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008I-001
- **Plan-Link:** PLAN-008I-001
- **Premise:** `DEC-008G-001` congelo que el siguiente lote tras `008h` es la expansion de `man-*` a `manager-*`. A diferencia de `008h`, aqui la compatibilidad NO depende de stubs ejecutables de skill: la API publica viva es `triggers` + `source_prompt` + referencias operativas, mientras que el nombre de directorio de la skill es detalle interno del bundle. Por tanto la migracion debe ser atomica sobre consumidores vivos y preservar `trigger_map`/`check-contract`, no introducir un segundo mecanismo de alias de skill.
- **Premise Re-check (read-only):** confirmar `WOT-2026-008g`, `WOT-2026-008e`, `WOT-2026-008h` y `WOT-2026-008k` COMPLETED; releer `DEC-008G-001` secciones 2/5/6; inventariar las cuatro skills `man-*`; capturar baseline de `python scripts/discover_skills.py --check-naming`, `--check-contract`, `--json`, `python scripts/check_skill_collisions.py` y `python scripts/discover_skills.py --check-index`; verificar consumidores vivos de `skills/man-*` y `man-*` en prompts, skills, docs y tests operativos; confirmar que `manager_review.md` ya es canonico desde `008e`.
- **Context Baseline Evidence:** roadmap_source=DEC-008G-001; manager_skill_dirs=4; live_operational_refs_confirmed=true; canonical_prompt_manager_review=true; generated_at=2026-06-18.
- **Files Likely Touched:**
  - Builder repo_motor: `skills/man-create-work-plan/`
  - Builder repo_motor: `skills/man-resolve-escalation/`
  - Builder repo_motor: `skills/man-review-implementation/`
  - Builder repo_motor: `skills/man-session-closeout/`
  - Builder repo_motor: `prompts/manager_review.md`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_motor: `prompts/orchestrator_session_close_chat.md`
  - Builder repo_motor: `skills/orchestrate-pipeline/SKILL.md`
  - Builder repo_motor: `skills/project-finalize/SKILL.md`
  - Builder repo_motor: `skills/audit-pipeline/SKILL.md`
  - Builder repo_motor: `skills/grill-work-plan/SKILL.md`
  - Builder repo_motor: `skills/session-close-observations/SKILL.md`
  - Builder repo_motor: `skills/README.md`
  - Builder repo_motor: `skills/validate_all.py`
  - Builder repo_motor: `skills/create-agent-skill/references/frontmatter-template.md`
  - Builder repo_motor: `skills/create-agent-skill/references/skill-anatomy.md`
  - Builder repo_motor: `docs/protocol/manager_review_design_vocabulary_WOT-2026-010t.md`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `tests/test_discover_skills.py`
  - Builder repo_motor: `tests/test_check_naming.py`
  - Builder repo_motor: `tests/test_agent_readme_references.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`; `docs/decisions/DEC-008D-001-naming-convention.md`; `prompts/review_manager.md`; historicos `CHANGELOG.md`, `backlog.md`, `ticket_contracts.md`; `tests/sandbox/**`; `bus/runtime/events`.
- **Forbidden Surfaces:** tocar `bui-*`; tocar `audit_*`; cambiar `triggers`; cambiar `contract_id`; introducir hardcode nuevo de dispatch; tocar bus/runtime/events manualmente; tocar dependencias; reabrir `008k`; tocar `privada/` o `.env`.
- **DoD:**
  - [ ] Existen los cuatro directorios canonicos `skills/manager-create-work-plan/`, `skills/manager-resolve-escalation/`, `skills/manager-review-implementation/` y `skills/manager-session-closeout/`.
  - [ ] Los cuatro directorios `man-*` dejan de ser consumidores vivos operativos; si sobrevive algun rastro, queda solo en historia, changelog, backlog, DEC o tests de compatibilidad explicitamente justificados.
  - [ ] `prompts/manager_review.md` referencia `skills/manager-review-implementation/SKILL.md` y conserva `contract_id: cid-man-review-v2` sin romper `--check-contract`.
  - [ ] Los consumidores vivos declarados en FLT usan los nombres `manager-*` al cierre.
  - [ ] `python scripts/discover_skills.py --check-contract` queda verde.
  - [ ] `python scripts/discover_skills.py --check-naming` queda verde.
  - [ ] `python scripts/check_skill_collisions.py` queda verde.
  - [ ] `python scripts/discover_skills.py --check-index` queda verde tras regenerar `docs/registry/INDEX.md`.
  - [ ] La paridad pre/post de discovery preserva los mismos triggers funcionales; cualquier diff del JSON queda limitado a rutas/nombres derivados por el rename declarado.
  - [ ] Existe al menos una barrera que detecta una referencia prose viva a `man-*` en superficies operativas del lote.
  - [ ] `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** ejecuta el lote de roadmap de `DEC-008G-001` para manager skills; deja `008j` (builder skills) intacto y no debe mezclar retirada de aliases de prompts ya resuelta en `008e/008h`.
- **CONTRACT_GAP behavior:** si aparece un consumidor runtime real del nombre de directorio `man-*`, si la compatibilidad exige un alias de skill no soportado limpiamente por discovery, si preservar `--check-contract` obliga a reabrir prompts fuera de FLT, o si el rename exige tocar `bui-*`, emitir `CG-WOT-2026-008i.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica via de compatibilidad exige un segundo mecanismo de alias de skill ad hoc; parar si el cambio deriva a migracion de `bui-*`; parar si la evidencia de migracion se basa solo en `--check-naming` y no en consumidores vivos; parar si aparece drift de packet no commiteado en repo_destino antes del handoff.
- **Depende de:** WOT-2026-008g (COMPLETED); WOT-2026-008e (COMPLETED); WOT-2026-008h (COMPLETED); WOT-2026-008k (COMPLETED).


## T-008J-001 -- Rename atomico de 4 skills builder a builder-*

- **ticket_id:** WOT-2026-008j
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-008J-001
- **Plan-Link:** PLAN-008J-001
- **Premise:** `DEC-008G-001` congelo `008j` como el lote de expansion `bui-*` -> `builder-*` despues de `008h`/`008i`. Igual que en `008i`, la compatibilidad NO depende de stubs ejecutables de skill: la API publica viva sigue siendo `triggers` + `source_prompt` + referencias operativas, mientras que el nombre de directorio de la skill es detalle interno del bundle. La migracion debe ser atomica sobre consumidores vivos y preservar `trigger_map`/`check-contract`, no introducir un segundo mecanismo de alias runtime.
- **Premise Re-check (read-only):** confirmar `WOT-2026-008g`, `008h`, `008i` y `008k` COMPLETED; releer `DEC-008G-001` secciones 2/5/6; inventariar las cuatro skills `bui-*`; capturar baseline de `python scripts/discover_skills.py --check-naming`, `--check-contract`, `--json`, `python scripts/check_skill_collisions.py` y `python scripts/discover_skills.py --check-index`; verificar consumidores vivos de `skills/bui-*` y `bui-*` en prompts, skills, `.claude`, docs operativos y tests; confirmar que `prompts/orchestrator_launch_builder.md` sigue siendo el prompt canonico del Builder y que conserva `contract_id: cid-bui-implement-v1`.
- **Context Baseline Evidence:** roadmap_source=DEC-008G-001; builder_skill_dirs=4; canonical_prompt_orchestrator_launch_builder=true; live_operational_refs_confirmed=true; generated_at=2026-06-19.
- **Leccion absorbida de 008i:** `Files Likely Touched` se declara a nivel fichero, no a nivel directorio, porque `scope_gate` compara contra `git diff --name-only` y no hace prefix matching sobre carpetas.
- **Files Likely Touched:**
  - Builder repo_motor: `skills/bui-implement-from-plan/SKILL.md`
  - Builder repo_motor: `skills/bui-implement-from-plan/references/code-rules.md`
  - Builder repo_motor: `skills/bui-implement-from-plan/references/log-format.md`
  - Builder repo_motor: `skills/builder-implement-from-plan/SKILL.md`
  - Builder repo_motor: `skills/builder-implement-from-plan/references/code-rules.md`
  - Builder repo_motor: `skills/builder-implement-from-plan/references/log-format.md`
  - Builder repo_motor: `skills/bui-run-quality-gates/SKILL.md`
  - Builder repo_motor: `skills/bui-run-quality-gates/references/common-fixes.md`
  - Builder repo_motor: `skills/builder-run-quality-gates/SKILL.md`
  - Builder repo_motor: `skills/builder-run-quality-gates/references/common-fixes.md`
  - Builder repo_motor: `skills/bui-self-audit/SKILL.md`
  - Builder repo_motor: `skills/bui-self-audit/references/.gitkeep`
  - Builder repo_motor: `skills/builder-self-audit/SKILL.md`
  - Builder repo_motor: `skills/builder-self-audit/references/.gitkeep`
  - Builder repo_motor: `skills/bui-write-deliverable/SKILL.md`
  - Builder repo_motor: `skills/bui-write-deliverable/references/.gitkeep`
  - Builder repo_motor: `skills/builder-write-deliverable/SKILL.md`
  - Builder repo_motor: `skills/builder-write-deliverable/references/.gitkeep`
  - Builder repo_motor: `prompts/orchestrator_launch_builder.md`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_motor: `skills/orchestrate-pipeline/SKILL.md`
  - Builder repo_motor: `.claude/agents/builder.md`
  - Builder repo_motor: `.claude/commands/agent-build.md`
  - Builder repo_motor: `scripts/closeout_steps/support.py`
  - Builder repo_motor: `skills/project-finalize/SKILL.md`
  - Builder repo_motor: `skills/refactor-manager/PROMPT_TEMPLATE.md`
  - Builder repo_motor: `skills/repo-compare/PROMPT_TEMPLATE.md`
  - Builder repo_motor: `skills/deep-research/SKILL.md`
  - Builder repo_motor: `skills/README.md`
  - Builder repo_motor: `skills/validate_all.py`
  - Builder repo_motor: `skills/create-agent-skill/SKILL.md`
  - Builder repo_motor: `skills/create-agent-skill/references/frontmatter-template.md`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `AGENTS.md`
  - Builder repo_motor: `llms-full.txt`
  - Builder repo_motor: `tests/test_discover_skills.py`
  - Builder repo_motor: `tests/test_check_naming.py`
  - Builder repo_motor: `tests/test_agent_readme_references.py`
  - Builder repo_motor: `tests/test_registry_catalog.py`
  - Builder repo_motor: `tests/test_migration_bootstrap.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`; `docs/decisions/DEC-008D-001-naming-convention.md`; `docs/decisions/DEC-008B-002-discovery-triggers.md`; historicos `CHANGELOG.md`, `backlog.md`, `ticket_contracts.md`; `.agent/runtime/memory/memory_rules.md`; `.agent/runtime/memory/UPSTREAM_LEARNINGS.md`; `bus/runtime/events`.
- **Forbidden Surfaces:** tocar `manager-*`; tocar `audit_*`; cambiar `triggers`; cambiar `contract_id`; introducir hardcode nuevo de dispatch o aliases runtime para skills; tocar prompts `audit_*`; tocar bus/runtime/events manualmente; tocar dependencias; tocar `privada/` o `.env`.
- **DoD:**
  - [ ] Existen los cuatro directorios canonicos `skills/builder-implement-from-plan/`, `skills/builder-run-quality-gates/`, `skills/builder-self-audit/` y `skills/builder-write-deliverable/`.
  - [ ] Los cuatro directorios `bui-*` dejan de ser consumidores vivos operativos; si sobrevive algun rastro, queda solo en historia, changelog, backlog, DEC o tests de compatibilidad explicitamente justificados.
  - [ ] `prompts/orchestrator_launch_builder.md` referencia `skills/builder-implement-from-plan/SKILL.md` y conserva `contract_id: cid-bui-implement-v1` sin romper `--check-contract`.
  - [ ] Los consumidores vivos declarados en FLT usan `builder-*` al cierre.
  - [ ] `python scripts/discover_skills.py --check-contract` queda verde.
  - [ ] `python scripts/discover_skills.py --check-naming` queda verde.
  - [ ] `python scripts/check_skill_collisions.py` queda verde.
  - [ ] `python scripts/discover_skills.py --check-index` queda verde tras regenerar `docs/registry/INDEX.md`.
  - [ ] La paridad pre/post de discovery preserva los mismos triggers funcionales; cualquier diff del JSON queda limitado a rutas/nombres derivados del rename declarado.
  - [ ] Existe al menos una barrera que detecta una referencia prose viva a `bui-*` en superficies operativas del lote.
  - [ ] `AGENTS.md`, `skills/README.md` y `llms-full.txt`, si mencionan estas skills, quedan alineados con `builder-*`.
  - [ ] Referencias en `.agent/runtime/memory/` se toleran como historia viva; no se actualizan en este ticket ni cuentan como consumidores operativos del lote.
  - [ ] `ruff`/`format` si toca Python, encoding guard, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** ejecuta el lote de roadmap de `DEC-008G-001` para builder skills; deja `manager-*` y `role: auditor` intactos; no debe reabrir `008h`, `008i` ni `008k`.
- **CONTRACT_GAP behavior:** si aparece un consumidor runtime real del path legacy `skills/bui-*`, si preservar compatibilidad exige un alias de skill no soportado limpiamente por discovery, si el rename deriva a `manager-*`/`audit_*`, o si la unica forma de cerrar el lote exige tocar dispatch/triggers, emitir `CG-WOT-2026-008j.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica via de compatibilidad exige un segundo mecanismo de alias de skill ad hoc; parar si el cambio deriva a migracion de prompts fuera de FLT o a cambios de trigger/dispatch; parar si la evidencia de migracion se basa solo en `--check-naming` y no en consumidores vivos; parar si aparece drift de packet no commiteado en `repo_destino` antes del handoff.
- **Depende de:** WOT-2026-008g (COMPLETED); WOT-2026-008h (COMPLETED); WOT-2026-008i (COMPLETED); WOT-2026-008k (COMPLETED).


## T-010V-001 -- Hardening de encoding guard para control chars ASCII no-whitespace

- **ticket_id:** WOT-2026-010v
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010V-001
- **Plan-Link:** PLAN-010V-001
- **Premise:** `WOT-2026-010e` introdujo deteccion temprana de encoding via `scripts.encoding_guard` compartido por `check_encoding_guard.py` y `encoding_post_write_hook.py`, pero el detector actual solo cubre BOM, mojibake y `?` intra-palabra. Tras `008f` y `008j` quedo verificado que control chars ASCII `<32` como `\x07`, `\x0b`, `\x0c` y `\x00` pueden corromper artefactos textuales y pasar los gates hasta handoff. El follow-up debe cerrar esa clase de fallo en la fuente de verdad compartida, no repararla caso a caso en packets.
- **Premise Re-check (read-only):** confirmar `WOT-2026-010e` y `WOT-2026-008j` COMPLETED; releer `AGENTS.md` seccion `Convencion de encoding y gap v1`; inspeccionar `scripts/encoding_guard.py`, `scripts/check_encoding_guard.py` y `scripts/encoding_post_write_hook.py`; confirmar que `file_issues()` es la fuente compartida; localizar tests existentes en `tests/test_encoding_integrity.py` y `tests/unit/test_encoding_post_write_hook.py`; registrar ejemplos reales de control chars detectados en `008j` (`\x07`, `\x0b`, `\x00`) como evidencia, no como fixtures historicos a reescribir.
- **Context Baseline Evidence:** shared_detector=`scripts.encoding_guard.file_issues`; cli_guard=`scripts/check_encoding_guard.py`; hook=`scripts/encoding_post_write_hook.py`; regressions_seen_in=008f,008j; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/encoding_guard.py`
  - Builder repo_motor: `scripts/check_encoding_guard.py`
  - Builder repo_motor: `scripts/encoding_post_write_hook.py`
  - Builder repo_motor: `tests/test_encoding_integrity.py`
  - Builder repo_motor: `tests/unit/test_encoding_post_write_hook.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `AGENTS.md`; historicos de `008f`/`008j` en `execution_log.md`, `backlog.md`, `ticket_contracts.md`; `bus/runtime/events`.
- **Forbidden Surfaces:** interceptar Bash/heredoc v1; ampliar scope a binarios/no-text; cambiar `TEXT_EXTENSIONS` sin necesidad contractual; introducir allowlists nuevas; tocar `validate`/bus/runtime/events; tocar dependencias; reescribir packets historicos para "limpiarlos".
- **DoD:**
  - [ ] `scripts/check_encoding_guard.py <archivo>` falla cerrado ante control chars ASCII `<32` no-whitespace en archivos de texto (`\x00`, `\x0b`, `\x0c`, etc.).
  - [ ] `\t`, `\n`, `\r` y CRLF legitimos NO disparan falso positivo.
  - [ ] La deteccion vive en la fuente compartida (`scripts/encoding_guard.py`) de forma que el hook post-write hereda el comportamiento sin un segundo detector divergente.
  - [ ] Existe al menos un test de regresion en `tests/test_encoding_integrity.py` para el CLI guard por ruta explicita y al menos un test en `tests/unit/test_encoding_post_write_hook.py` que demuestra fallo del hook ante control chars en archivo textual.
  - [ ] Los tests existentes de BOM/mojibake/question-mark siguen verdes; no se degrada cobertura previa.
  - [ ] `python -m pytest tests/test_encoding_integrity.py tests/unit/test_encoding_post_write_hook.py -v` pasa.
  - [ ] `ruff`/`format` sobre Python tocado, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **CONTRACT_GAP behavior:** si la correccion exige ampliar el ticket a interceptar Bash/heredoc, cambiar semantica de allowlist, escanear binarios o introducir una segunda fuente de verdad distinta de `scripts.encoding_guard`, emitir `CG-WOT-2026-010v.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica forma de detectar control chars rompe CRLF/tab/newline legitimos; parar si el hook post-write requiere un rediseno mayor fuera de FLT; parar si la barrera solo se demuestra en mocks sin pasar por `check_encoding_guard.py` o el hook real.
- **Depende de:** WOT-2026-010e (COMPLETED); WOT-2026-008j (COMPLETED).


## T-010W-001 -- Hardening de session-close: subprocess utf-8 en closeout_steps para Windows

- **ticket_id:** WOT-2026-010w
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010W-001
- **Plan-Link:** PLAN-010W-001
- **Premise:** el intento de `--session-close` posterior a `010v` revelo un blocker real de infraestructura del motor en Windows: `scripts/closeout_steps/support.py:40` ejecuta `subprocess.run(..., capture_output=True, text=True)` sin `encoding`, y al capturar salida no-ASCII de scripts del closeout lanza `UnicodeDecodeError` bajo cp1252. El mismo patron reaparece en `scripts/closeout_steps/support.py:287` (`git ls-files`) y `scripts/closeout_steps/rotation.py:367` (`git status --short`) como riesgo latente sobre paths no-ASCII. El fix correcto es local a los call sites del closeout: `encoding="utf-8", errors="replace"`, con regresion test que pruebe que el closeout no revienta al capturar un em dash u otra salida UTF-8 alta.
- **Premise Re-check (read-only):** confirmar `WOT-2026-010v` COMPLETED y publicado; reproducir el fallo con `python .agent/agent_controller.py --session-close --dry-run --force --project-root <repo_destino>`; releer `scripts/closeout_steps/support.py` y `scripts/closeout_steps/rotation.py`; verificar que los tres `subprocess.run(..., text=True)` carecen de `encoding`; localizar los tests de closeout existentes en `tests/test_session_closeout.py`; confirmar que NO hace falta tocar `scripts/session_closeout.py` ni el controller para corregir la ruta de decode.
- **Context Baseline Evidence:** blocker=UnicodeDecodeError cp1252 on Windows; central_call_site=`scripts/closeout_steps/support.py:40`; latent_call_sites=`support.py:287`,`rotation.py:367`; session_state_before_fix=`WOT-2026-010v/COMPLETED`; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/closeout_steps/support.py`
  - Builder repo_motor: `scripts/closeout_steps/rotation.py`
  - Builder repo_motor: `tests/test_session_closeout.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/session_closeout.py`; `.agent/agent_controller.py`; `AGENTS.md`; `backlog.md`; `ticket_contracts.md`; `bus/runtime/events`; salida fallida del dry-run de cierre en `execution_log.md`.
- **Forbidden Surfaces:** tocar la logica funcional del closeout; mover el fix al reader-thread del controller; tocar otros `subprocess.run` fuera de `closeout_steps`; tocar dependencias; cambiar semantica de `check_versioned_filenames`; tocar `bus/runtime/events` a mano.
- **DoD:**
  - [ ] `scripts/closeout_steps/support.py:run_script` fija `encoding="utf-8", errors="replace"` en su `subprocess.run`.
  - [ ] `scripts/closeout_steps/support.py:check_versioned_filenames` fija `encoding="utf-8", errors="replace"` en su `subprocess.run`.
  - [ ] `scripts/closeout_steps/rotation.py:step_git_clean` fija `encoding="utf-8", errors="replace"` en su `subprocess.run`.
  - [ ] Existe al menos un test de regresion en `tests/test_session_closeout.py` que ejecuta la ruta real de `run_script` contra un script temporal que imprime un em dash u otra salida UTF-8 alta y demuestra que la salida se captura sin `UnicodeDecodeError`.
  - [ ] Si se anade coverage para los otros dos call sites, se hace via tests focales del closeout o verificacion directa reproducible, no por relato.
  - [ ] `python .agent/agent_controller.py --session-close --dry-run --force --project-root <repo_destino>` deja de fallar por `UnicodeDecodeError` en Windows.
  - [ ] `python -m pytest tests/test_session_closeout.py -v` pasa.
  - [ ] `ruff`/`format` sobre Python tocado, `run_pytest_safe --level all` y `validate --json --project-root <repo_destino>` quedan verdes.
- **CONTRACT_GAP behavior:** si el fix exige mover la correccion al controller/reader-thread, tocar rutas de subprocess fuera de `closeout_steps` o reescribir la semantica funcional de los steps de cierre, emitir `CG-WOT-2026-010w.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la reproduccion real no pasa por `closeout_steps`; parar si el dry-run sigue explotando en un cuarto call site fuera del FLT; parar si la unica forma de probar la regresion es con mocks que no ejercitan la decodificacion real.
- **Depende de:** WOT-2026-010v (COMPLETED).


## T-011D-001 -- Retirada auditada de stubs legacy de prompts

- **ticket_id:** WOT-2026-011d
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011D-001
- **Plan-Link:** PLAN-011D-001
- **Premise:** los 7 stubs legacy de `prompts/` (`audit_plan.md`, `destination_bootstrap.md`, `launch_builder.md`, `refactor_bootstrap.md`, `review_manager.md`, `session_bootstrap.md`, `session_close_chat.md`) siguen existiendo por compatibilidad, pero todavia tienen consumidores operativos vivos y la proyeccion `docs/registry/INDEX.md` los publica como `active`. La retirada solo es segura si primero se corrige la fuente real del catalogo generado, se reapuntan consumidores vivos y cada delete queda precedido por evidencia `rg` de `0` consumidores no-historicos.
- **Premise Re-check (read-only):** confirmar que `docs/registry/INDEX.md` lleva header `AUTOGENERATED ... do not edit by hand`; releer `scripts/discover_skills.py` para verificar que `build_catalog()` publica hoy `prompts/*.md` por layout y que el `status` derivado via `_derive_status()` solo aplica a `skills/`; inventariar consumidores vivos de cada stub con `rg`; confirmar que `VALID_STATUS == ("active", "deprecated", "draft")`; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** index_generated=true; prompt_status_not_derived=true; valid_status_vocab=`active|deprecated|draft`; active_stubs=7; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/discover_skills.py`
  - Builder repo_motor: `docs/registry/INDEX.md`
  - Builder repo_motor: `MANIFEST.distribute`
  - Builder repo_motor: `prompts/audit_plan.md`
  - Builder repo_motor: `prompts/destination_bootstrap.md`
  - Builder repo_motor: `prompts/launch_builder.md`
  - Builder repo_motor: `prompts/refactor_bootstrap.md`
  - Builder repo_motor: `prompts/review_manager.md`
  - Builder repo_motor: `prompts/session_bootstrap.md`
  - Builder repo_motor: `prompts/session_close_chat.md`
  - Builder repo_motor: `AGENTS.md`
  - Builder repo_motor: `PROJECT.md`
  - Builder repo_motor: `CLOSURE_MODEL.md`
  - Builder repo_motor: `.claude/rules/00-startup.md`
  - Builder repo_motor: `tests/test_registry_catalog.py`
  - Builder repo_motor: `tests/test_migration_bootstrap.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/decisions/DEC-008D-001-naming-convention.md`; `docs/decisions/DEC-008G-001-vocabulary-and-role-naming.md`; `prompts/audit_portability_legacy_surface.md`; `tests/test_check_naming.py`; `CHANGELOG.md`; `CLAUDE.md`; `README.md`; `QUICKSTART.md`; `bus/runtime/events`.
- **Forbidden Surfaces:** editar `docs/registry/INDEX.md` manualmente; introducir un estado nuevo tipo `legacy-retained`; reescribir DEC/changelog/memoria historica; borrar un stub sin `rg` pre-delete con `0` consumidores no-historicos; mezclar la retirada con refactors de contenido no relacionados; tocar `privada/` o `.env`.
- **DoD:**
  - [ ] `scripts/discover_skills.py` deriva de forma determinista el lifecycle de prompts stub desde una fuente real del archivo y mantiene el vocabulario `active|deprecated|draft`.
  - [ ] `python scripts/discover_skills.py --generate-index` regenera `docs/registry/INDEX.md` y los 7 stubs dejan de aparecer como `active`.
  - [ ] `MANIFEST.distribute`, `.claude/rules/00-startup.md`, `PROJECT.md`, `CLOSURE_MODEL.md`, `AGENTS.md` y `tests/test_migration_bootstrap.py` apuntan al canonico o justifican compatibilidad residual explicitamente.
  - [ ] Cada stub borrado en este ticket tiene evidencia `rg` pre/post delete con `0` consumidores no-historicos.
  - [ ] Cada stub que no llegue a `0` consumidores no-historicos permanece en disco marcado como `deprecated`, sin delete forzado.
  - [ ] `python scripts/discover_skills.py --check-index`, `python -m pytest tests/test_registry_catalog.py -v`, `python -m pytest tests/test_migration_bootstrap.py -v`, `ruff check`, `python scripts/run_pytest_safe.py --project-root <repo_destino>` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** serializar contra cualquier ticket que toque prompts, catalogo derivado, `MANIFEST.distribute`, bootstrap docs o migraciones 008h/010a; no debe reabrir historia ni DEC como scope productivo.
- **CONTRACT_GAP behavior:** si la reclasificacion exige ampliar `VALID_STATUS`, si `--generate-index` / `--check-index` fallan de forma estructural antes del repoint, o si un stub con consumidores vivos no puede ni repointarse ni mantenerse `deprecated`, emitir `CG-WOT-2026-011d.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la fuente real del catalogo no puede derivar lifecycle para prompts stub sin ampliar el vocabulario `active|deprecated|draft`; parar si `--generate-index` o `--check-index` fallan antes de terminar el repoint; parar si un stub conserva consumidores operativos vivos que no pueden repointarse al canonico y tampoco pueden permanecer en `deprecated` sin romper el contrato vigente.
- **Depende de:** WOT-2026-010w (COMPLETED).


## T-011A-001 -- Session-close fail-closed ante archival-limbo

- **ticket_id:** WOT-2026-011a
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011A-001
- **Plan-Link:** PLAN-011A-001
- **Premise:** `WOT-2026-010u` ya detecta `archive_rename_uncommitted`, pero la deteccion vive en `delivery_hygiene` / `pre_handoff` y llega tarde. `WOT-2026-011d` confirmo otra vez el patron: `--session-close` puede mover `AUDIT_/STRATEGY_` a `_archive/plan_audit/` y dejar `D old + ?? new` sin fallar el cierre; la contaminacion aparece en el ticket siguiente. `011a` debe endurecer el closeout para que el mismo cierre falle cerrado con remediacion auditable o, si el punto exacto exige una reconciliacion asistida, la exprese sin auto-commit.
- **Premise Re-check (read-only):** confirmar `WOT-2026-010u`, `WOT-2026-010w` y `WOT-2026-011d` COMPLETED; releer `scripts/closeout_steps/archival.py`, `scripts/session_closeout.py`, `scripts/delivery_hygiene_check.py` y `scripts/archive_collaboration_artifacts.py`; verificar que `step_archive_collaboration()` hoy devuelve `PASS` con `returncode == 0` sin comprobar la post-condicion; confirmar que `check_archive_rename_complete()` ya expone `archive_rename_uncommitted` + remediacion exacta; localizar tests vigentes en `tests/test_session_closeout.py`, `tests/test_pre_handoff_guard.py` y `tests/unit/test_delivery_hygiene_check.py`.
- **Context Baseline Evidence:** recurrence_confirmed_in=`WOT-2026-011d`; existing_reason=`archive_rename_uncommitted`; late_detection_sites=`scripts/pre_handoff_guard.py`,`scripts/delivery_hygiene_check.py`; closeout_gap=`scripts/closeout_steps/archival.py`; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/closeout_steps/archival.py`
  - Builder repo_motor: `scripts/session_closeout.py`
  - Builder repo_motor: `scripts/delivery_hygiene_check.py`
  - Builder repo_motor: `tests/test_session_closeout.py`
  - Builder repo_motor: `tests/unit/test_delivery_hygiene_check.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/archive_collaboration_artifacts.py`; `tests/test_pre_handoff_guard.py`; `tests/unit/test_archive_collaboration_artifacts.py`; `.agent/runtime/memory/observations.jsonl`; `backlog.md`; `ticket_contracts.md`; `bus/runtime/events`.
- **Forbidden Surfaces:** auto-commit dentro del archivador; borrado destructivo de artefactos archivados; bus/runtime/events manuales; dependencias; `privada/`; `.env`.
- **DoD:**
  - [ ] La ruta real de `--session-close` o `step_archive_collaboration()` falla con `FAIL` bloqueante si deja un `archive_rename_uncommitted`.
  - [ ] El diagnostico conserva la razon estable y nombra origen, destino y el comando exacto de reconcile.
  - [ ] El ticket no introduce auto-commit del archivador ni borra artefactos archivados.
  - [ ] Existe al menos una prueba de regresion que falla sin el fix y pasa con el fix reproduciendo el limbo en la ruta real de closeout.
  - [ ] El caso limpio sigue cerrando en `PASS`.
  - [ ] `uv run ruff check`, tests focales, `python scripts/run_pytest_safe.py --project-root <repo_destino>` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** reutiliza la barrera introducida por `010u`; no reabre la politica de auto-commit rechazada en `011a`; no debe romper el cierre Windows de `010w`.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige auto-commit del archivador, cambiar el contrato de `archive_collaboration_artifacts.py` mas alla de plan/audit, o tocar politica de bus/controller fuera del closeout declarado, emitir `CG-WOT-2026-011a.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la deteccion solo puede expresarse como `dirty tree` generico y no como `archive_rename_uncommitted`; parar si la unica forma de cerrar el gap es mover la logica a un auto-commit silencioso; parar si el test no puede reproducir la mutacion real del closeout sin mocks vacios.
- **Depende de:** WOT-2026-010u (COMPLETED); WOT-2026-010w (COMPLETED); WOT-2026-011d (COMPLETED).

## T-012A-001 -- Backlog vivo vs historico + formato parseable

- **ticket_id:** WOT-2026-012a
- **status:** frozen
- **deliverable_type:** documentation
- **delivery_authority:** repo_destino
- **Objective-Link:** OBJ-012A-001
- **Plan-Link:** PLAN-012A-001
- **Premise:** `backlog.md` mezcla cola viva, fichas operativas e historico. `WT-2026-250c` queda absorbido por una familia nueva: `012a` fija formato parseable, separa vivo/historico por paso explicito del Manager y preserva el contrato operativo del Builder en `work_plan.md`, no en la propia seccion movible del backlog.
- **Premise Re-check (read-only):** releer `backlog.md`, `CHANGELOG.md`, `STATE.md`, `TURN.md`, `ticket_contracts.md`; confirmar que `011e <-> 010m` ya esta resuelto como `keep-both-with-boundary`; confirmar evidencia de preflight de `delivery_authority: repo_destino` con `check_deliverables_exist.py` sobre FLT namespaced `### repo_destino` y ruta bare; verificar `validate --json --project-root <repo_destino>` antes del arranque.
- **Context Baseline Evidence:** active_backlog_mixed_with_history=true; resolution_011e_010m=keep-both-with-boundary; repo_destino_deliverable_preflight=verified; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_destino: `.agent/collaboration/backlog.md`
  - Builder repo_destino: `.agent/collaboration/_archive/backlog_done.md`
  - Builder repo_destino: `.agent/collaboration/_archive/backlog_pre_012a.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `CHANGELOG.md`; `STATE.md`; `TURN.md`; `.agent/planning/ticket_contracts.md`; historico previo de `backlog.md`; filas `011e`..`011i`; `WOT-2026-010m`.
- **Forbidden Surfaces:** tocar `--session-close` / `--mark-ready`; introducir renames automaticos del archivador; perder la seccion `### WOT-2026-012a`; prosa vaga en `Reactivation`; editar bus/runtime/events manualmente.
- **DoD:**
  - [ ] La tabla activa queda como unica fuente parseable, con schema que incluye `Reactivation`.
  - [ ] `Reactivation` usa `-` solo para estados activos; `deferred` y `completed-partial` llevan trigger estructurado valido.
  - [ ] La cola viva queda limitada a `pending|blocked|deferred|ready-for-review|awaiting-manager|completed-partial`; los terminales salen del backlog activo.
  - [ ] Existe snapshot pre-corte como commit git explicito o `_archive/backlog_pre_012a.md` portable.
  - [ ] El corte del historico se hace por bloques logicos auditablemente reconocibles y conserva integra la seccion `### WOT-2026-012a` en el historico movido.
  - [ ] Existe evidencia mecanica antes/despues del movimiento (conteo de filas terminales y fichas `###` movidas) suficiente para auditar no-perdida de historico.
  - [ ] `backlog.md` muestra reduccion material verificable por diff; `<= 200` lineas de cola viva queda como objetivo operativo, no como gate binario.
  - [ ] `python scripts/check_encoding_guard.py` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** mantiene `011h` fuera de scope; no reabre `250c`; preserva `011e <-> 010m` con frontera runner-local-vs-CI.
- **CONTRACT_GAP behavior:** si el corte exige tocar el archivador del closeout, si el snapshot no puede materializarse de forma portable, o si la seccion `### WOT-2026-012a` no puede conservarse integra en el historico, emitir `CG-WOT-2026-012a.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si aparece perdida de historico no auditable; parar si el formato parseable exige leer HTML comments; parar si `delivery_authority: repo_destino` deja de pasar el preflight namespaced.
- **Depende de:** -.

## T-012B-001 -- Gate backlog fail-closed sobre cola viva

- **ticket_id:** WOT-2026-012b
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-012B-001
- **Plan-Link:** PLAN-012B-001
- **Premise:** tras `012a`, el backlog activo ya tiene formato parseable estable. `012b` convierte ese contrato en barrera automatica fail-closed desde `repo_motor`, leyendo `repo_destino` solo via `--project-root` o `AGENT_PROJECT_ROOT`.
- **Premise Re-check (read-only):** releer el backlog migrado por `012a`; confirmar que la tabla activa expone `Reactivation`; confirmar que el gate de deliverables y la resolucion de proyecto funcionan con `repo_destino`; verificar `run_gates_dispatch.py`, `check_deliverables_exist.py` y `validate_ticket_prose.py` antes de decidir la integracion.
- **Context Baseline Evidence:** gate_target=repo_destino_backlog_active; requires_project_root=true; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/check_backlog_contract.py`
  - Builder repo_motor: `tests/unit/test_check_backlog_contract.py`
  - Builder repo_motor: `scripts/run_gates_dispatch.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** backlog migrado por `012a`; `STATE.md`; `TURN.md`; `check_deliverables_exist.py`; `validate_ticket_prose.py`.
- **Forbidden Surfaces:** leer backlog relativo al cwd; depender de HTML comments o prose libre; degradar silenciosamente a warning fuera del rollout explicito; inventar vocabulario nuevo de estados; editar bus/runtime/events manualmente.
- **DoD:**
  - [ ] El gate falla con `exit != 0` ante cualquier violacion estructural o semantica obligatoria cuando opera en modo bloqueante.
  - [ ] Falla cerrado si faltan `--project-root` y `AGENT_PROJECT_ROOT`.
  - [ ] Parsea solo la tabla activa de `repo_destino` y valida estructura + contenido: columnas esperadas, encabezados `### WOT-...` exactos, vocabulario cerrado de `Status`, y valores permitidos de `Reactivation`.
  - [ ] La lista de estados de cola viva queda codificada en el propio gate: `pending|blocked|deferred|ready-for-review|awaiting-manager|completed-partial`.
  - [ ] Existe test que demuestra pass con `delivery_authority: repo_destino` / FLT namespaced correcto y fail-closed sin `--project-root` ni `AGENT_PROJECT_ROOT`.
  - [ ] Ruff, tests focales, suite aplicable y `validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** depende de `012a`; no reemplaza el archivador ni el closeout; no toca politica de rollout warning->error fuera de lo declarado.
- **CONTRACT_GAP behavior:** si el parser necesita HTML comments/prose, si el backlog post-012a no expone schema suficiente, o si la resolucion topologica del destino no puede fallar cerrada, emitir `CG-WOT-2026-012b.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el gate lee accidentalmente el seed del motor; parar si la validacion semantica de `Reactivation` no puede distinguir triggers validos de prosa vaga; parar si la integracion solo puede hacerse como warning permanente.
- **Depende de:** WOT-2026-012a.


## T-011C-001 -- BOM/control-char SOURCE audit (code-spike, sin fix)

- **ticket_id:** WOT-2026-011c
- **status:** frozen
- **deliverable_type:** research
- **delivery_authority:** repo_destino
- **Objective-Link:** OBJ-011C-001
- **Plan-Link:** PLAN-011C-001
- **Premise:** superficies vivas de `.agent/collaboration/` aparecen con BOM UTF-8 y, en la region historica del backlog, con 3 control chars que se comieron la primera letra de palabras (`\x07udit`->audit, `\x0Balidate`->validate, `\x08ui-self`->bui-self). El encoding guard (WOT-2026-010v) ya los DETECTA; la FUENTE que los inyecta NO esta identificada. Recurre en 008f/008k/008j/010w y bloqueo de 012a. Este ticket es un SPIKE: identifica la fuente con evidencia y PARA; no aplica fix de fuente (eso es follow-up).
- **Premise Re-check (read-only):** confirmar con bytes que el subconjunto {work_plan, TURN, backlog, execution_log} tiene BOM en working tree y NO en HEAD, mientras {STATE, notifications, review_queue} no lo tienen; confirmar que los 3 control chars viven en HEAD:backlog (region historica), no introducidos por edicion de agente.
- **Context Baseline Evidence:** bom_surfaces_worktree=work_plan,TURN,backlog,execution_log; bom_absent=STATE,notifications,review_queue; head_has_bom=false; control_chars_in_HEAD_backlog=true; guard_detects=true(010v); source_identified=false; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_destino: `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md` (reporte de hallazgo)
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only (NO modificar):** `scripts/launch_agent_terminals.ps1`; `scripts/encoding_post_write_hook.py`; `bus/` y `.agent/agent_controller.py` (escritores de proyecciones); cualquier `Out-File`/`Set-Content`/`encoding=` que toque `.agent/collaboration/`; git history de las superficies con BOM.
- **Forbidden Surfaces:** aplicar cualquier fix de fuente (strip BOM, reconstruir letras, cambiar el escritor); tocar el guard 010v; tocar superficies vivas para "limpiarlas"; tocar repo_motor (delivery_authority=repo_destino, solo lectura del motor permitida).
- **DoD:**
  - [ ] Existe `bom_source_audit_WOT-2026-011c.md` que nombra, con evidencia reproducible, el/los escritor(es) que inyectan BOM y, si es posible, el origen de los control chars.
  - [ ] El reporte distingue VERIFICADO (con comando/bytes) de INFERENCIA RAZONABLE; no presenta hipotesis como hecho.
  - [ ] El reporte declara explicitamente si hay fix de fuente viable o si 010v (defensa en profundidad) es suficiente, como RECOMENDACION, no como cambio aplicado.
  - [ ] El reporte abre follow-up(s) concretos (ticket id sugerido) para el fix, si procede.
  - [ ] `python scripts/check_encoding_guard.py <reporte> <execution_log>` verde sobre las superficies propias del ticket (el reporte nace limpio).
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` -> 0 errors / 0 warnings.
- **Integracion cross-ticket:** desbloquea WOT-2026-012a (su CG recomienda secuenciar 011c antes). NO cierra 012a; solo entrega el hallazgo que permite decidir como regenerar el snapshot/historico limpios.
- **CONTRACT_GAP behavior:** si identificar la fuente exigiera MODIFICAR un escritor (motor o destino) para probar la hipotesis, detener y emitir `CG-WOT-2026-011c.md`: el spike es read-only sobre escritores; probar-modificando ya es el fix, que es follow-up.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar y entregar el reporte en cuanto la fuente quede identificada con evidencia (no seguir hacia el fix); parar si la unica forma de avanzar es modificar un escritor; parar si la fuente resulta ser el entorno del host (PowerShell 5.1 Out-File default BOM) y el fix excede repo_destino.
- **Depende de:** WOT-2026-010v.

## T-011J-001 -- Corregir fuente BOM en writer PowerShell y preparar regeneracion limpia de 012a
- **ticket_id:** WOT-2026-011j
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011J-001
- **Plan-Link:** PLAN-011J-001
- **Premise:** WOT-2026-011c verifico que el BOM proviene de escrituras PowerShell 5.1 con `Set-Content`/`Out-File -Encoding UTF8`. A la vez, la cola viva actual (`backlog.md`) ya esta limpia; los 3 control chars que siguen bloqueando `012a` viven solo en `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md`. Por tanto `011j` no debe parchear esos archives a mano: debe endurecer el writer PowerShell in-scope en `repo_motor` y dejar la regeneracion limpia de los artefactos historicos para el relanzamiento de `012a`.
- **Premise Re-check (read-only):** confirmar que `python scripts/check_encoding_guard.py .agent/collaboration/backlog.md` sale verde y que el mismo guard sobre `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` falla por los 3 control chars historicos; releer `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`; inspeccionar `scripts/launch_agent_terminals.ps1` para localizar escrituras PowerShell BOM-prone in-scope y el patron BOM-safe ya existente de `WT-2026-248a`; localizar barreras existentes en `tests/test_opencode_config_stability.py` y `tests/test_launch_agent_terminals_script.py`; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** 011c_report=completed; active_backlog_encoding=clean; archive_backlog_encoding=3_control_chars; launcher_bom_primitives=`Set-Content -Encoding UTF8`,`Out-File -Encoding UTF8`; generated_at=2026-06-19.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/launch_agent_terminals.ps1`
  - Builder repo_motor: `tests/test_opencode_config_stability.py`
  - Builder repo_motor: `tests/test_launch_agent_terminals_script.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`; `.agent/collaboration/backlog.md`; `.agent/collaboration/_archive/backlog_done.md`; `.agent/collaboration/_archive/backlog_pre_012a.md`; `.agent/collaboration/CG-WOT-2026-012a.md`; `.agent/agent_controller.py`; `scripts/check_encoding_guard.py`; `tests/test_launcher_ps1_syntax.py`.
- **Forbidden Surfaces:** editar manualmente `_archive/backlog_done.md` o `_archive/backlog_pre_012a.md`; broad-strip de BOM/control chars en el repo; tocar `scripts/check_encoding_guard.py`; reintentar `WOT-2026-012a` dentro de `011j`; tocar `TURN.md` / `STATE.md` / bus manualmente; introducir un fix que dependa de relajar el guard.
- **DoD:**
  - [ ] El diff elimina las escrituras PowerShell BOM-prone que `011j` declare in-scope y las sustituye por un patron BOM-safe verificable.
  - [ ] Existe al menos una barrera de regresion que falla sin el fix y pasa con el fix para la primitiva o ruta tocada por `011j`.
  - [ ] `tests/test_opencode_config_stability.py` sigue verde y demuestra que el patron BOM-safe existente no regresa.
  - [ ] `011j` NO edita manualmente `_archive/backlog_done.md` ni `_archive/backlog_pre_012a.md`; deja explicito en `execution_log.md` que esos artefactos se regeneraran al relanzar `012a`.
  - [ ] `python scripts/check_encoding_guard.py` sobre las superficies propias del ticket queda verde.
  - [ ] `uv run ruff check` sobre los Python tocados, `python -m pytest` focal aplicable, `python scripts/run_pytest_safe.py --project-root <repo_destino>` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** desbloquea el relanzamiento de `WOT-2026-012a`, pero no lo cierra ni regenera sus archives dentro del mismo ticket. `012a` se relanza despues para reconstruir `_archive/backlog_done.md` y `_archive/backlog_pre_012a.md` desde la fuente viva ya limpia.
- **CONTRACT_GAP behavior:** si el re-check demuestra que ya no existe ningun writer BOM-prone in-scope en `repo_motor`, si el unico camino a verde exige editar manualmente los archives de `012a`, o si el fix real cae en `.agent/agent_controller.py` / guard de encoding fuera de la superficie declarada, emitir `CG-WOT-2026-011j.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el fix exige broadening a una caza general de writers PowerShell fuera de la superficie declarada; parar si el ticket deriva en reconstruccion manual de historico; parar si el rojo restante pertenece solo a `012a` y requiere relanzar ese ticket en lugar de seguir ampliando `011j`.
- **Depende de:** WOT-2026-011c (COMPLETED); WOT-2026-010v (COMPLETED).
## T-010M-001 -- Piloto CI xdist acotado sobre quality-gates

- **ticket_id:** WOT-2026-010m
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010M-001
- **Plan-Link:** PLAN-010M-001
- **Premise:** `011e` ya incorporo `pytest-xdist` al runner local con flag opt-in y mantuvo intacto el cierre canonico (`--level all`). `.github/workflows/quality-gates.yml` sigue ejecutando solo la ruta serial de `scripts/run_pytest_safe.py`. La frontera `011e <-> 010m <-> 011i` ya esta resuelta: `010m` solo puede pilotar CI, no mover el default del runner.
- **Premise Re-check (read-only):** releer `.github/workflows/quality-gates.yml`, `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `scripts/pre_handoff_guard.py`, `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`, `docs/test_performance/test_performance_followup_WOT-2026-010k.md` y `.agent/collaboration/_archive/backlog_done.md`; confirmar que `011e` quedo COMPLETED, que el workflow aun no usa `--xdist-workers` y que el cierre canonico sigue requiriendo `python scripts/run_pytest_safe.py --level all`.
- **Context Baseline Evidence:** quality_gates_serial_only=true; xdist_opt_in_available=true; canonical_close_all=true; boundary_011e_local_010m_ci_011i_default=true; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder repo_motor: `.github/workflows/quality-gates.yml`
  - Builder repo_motor: `tests/unit/test_quality_gates_workflow.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/run_pytest_safe.py`; `tests/unit/test_run_pytest_safe.py`; `scripts/pre_handoff_guard.py`; `.agent/runtime/pytest-safe/last-run.json`; `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`; `docs/test_performance/test_performance_followup_WOT-2026-010k.md`; `.agent/collaboration/backlog.md`; `.agent/collaboration/_archive/backlog_done.md`.
- **Forbidden Surfaces:** `scripts/run_pytest_safe.py`; `tests/unit/test_run_pytest_safe.py`; `scripts/pre_handoff_guard.py`; `scripts/run_gates_dispatch.py`; cambio implicito del default del runner o del camino canonico `--level all`; otros workflows; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD:**
  - [ ] `.github/workflows/quality-gates.yml` incorpora un piloto CI xdist aditivo y explicitamente acotado, sin eliminar ni alterar la corrida serial canonica existente.
  - [ ] El piloto usa `scripts/run_pytest_safe.py` con `--xdist-workers <N>` solo sobre la superficie permitida del ticket; el camino canonico en CI sigue sin xdist.
  - [ ] `tests/unit/test_quality_gates_workflow.py` aporta una barrera FAIL-sin/PASS-con que falla si desaparece el piloto o si la corrida canonica adopta xdist por accidente.
  - [ ] `execution_log.md` deja evidencia auditable de la separacion entre piloto CI y cierre canonico, con resultado o medicion del piloto.
  - [ ] `python -m pytest tests/unit/test_quality_gates_workflow.py -q`, `ruff check tests/unit/test_quality_gates_workflow.py`, `uv run ruff format --check tests/unit/test_quality_gates_workflow.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** consume la capacidad xdist creada por `011e`, pero no la reabre; no convierte el piloto en default (`011i`) ni toca la barrera canonica de handoff. Si los tests no parallel-safe exigen aislar subset adicional fuera del workflow/test declarados, el ticket debe parar.
- **CONTRACT_GAP behavior:** si el piloto CI no puede definirse sin tocar `scripts/run_pytest_safe.py`, si la unica via verde convierte xdist en default o lo mete en el camino canonico `--level all`, o si el subset seguro exige expansion a nuevas superficies del runner/selector, emitir `CG-WOT-2026-010m.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica implementacion viable toca el runner, el guard de handoff o el dispatcher; parar si el piloto solo puede validarse convirtiendo xdist en default o metiendolo en la corrida canonica `--level all`; parar si los tests no parallel-safe obligan a redisenar el selector/runner en vez de dejar un piloto CI acotado.
- **Depende de:** WOT-2026-010j (COMPLETED); WOT-2026-010k (COMPLETED); WOT-2026-011e (COMPLETED).
## T-011E-001 -- pytest-xdist opt-in local medido para subset unitario

- **ticket_id:** WOT-2026-011e
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011E-001
- **Plan-Link:** PLAN-011E-001
- **Premise:** `scripts/run_pytest_safe.py` ya soporta `level=unit|integration|all`, selector focal y cierre canonico por `last-run.json`, pero no ofrece un camino local, medido y opt-in para paralelizar un subset unitario con `pytest-xdist`. `010m` ya quedo acotado a CI (`keep-both-with-boundary`) y `011i` queda reservado a evaluar un cambio por defecto solo si este opt-in local sale estable.
- **Premise Re-check (read-only):** releer `scripts/run_pytest_safe.py`, `tests/unit/test_run_pytest_safe.py`, `scripts/pre_handoff_guard.py`, `pyproject.toml`, `uv.lock` y `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`; verificar que `pytest-xdist` aun no esta declarado; verificar que el guard de handoff sigue exigiendo `level=all` + `args_mode=default_discovery` y no debe cambiarse en este ticket.
- **Context Baseline Evidence:** canonical_suite_recent=`3051 passed, 20 skipped, 5 deselected in 449.14s`; xdist_declared=false; boundary_010m=`local-vs-CI`; generated_at=2026-06-20.
- **Files Likely Touched:**
  - Builder repo_motor: `pyproject.toml`
  - Builder repo_motor: `uv.lock`
  - Builder repo_motor: `scripts/run_pytest_safe.py`
  - Builder repo_motor: `tests/unit/test_run_pytest_safe.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/pre_handoff_guard.py`; `docs/test_performance/test_performance_baseline_WOT-2026-010j.md`; `docs/test_performance/test_performance_followup_WOT-2026-010k.md`; `.agent/runtime/pytest-safe/last-run.json`; `.agent/collaboration/backlog.md`.
- **Forbidden Surfaces:** `scripts/pre_handoff_guard.py`; `scripts/run_gates_dispatch.py`; CI/workflows; cambio implicito del default de `run_pytest_safe.py`; relax de `level=all` o `args_mode=default_discovery`; `privada/`; `.env`; `bus/runtime/events` manuales.
- **DoD:**
  - [ ] `pytest-xdist` queda declarado en dependencias dev y reflejado en `uv.lock`.
  - [ ] `scripts/run_pytest_safe.py` expone un flag opt-in de xdist con backward-compat total cuando no se usa.
  - [ ] El camino xdist solo se activa para subset unitario explicito; fuera de ese contrato el runner cae a serial con razon auditable, no a pass-open silencioso.
  - [ ] `last-run.json` registra `xdist_requested`, `xdist_enabled`, `xdist_workers` y `xdist_reason` (o equivalente semantico estable).
  - [ ] Existe al menos una barrera FAIL-sin/PASS-con para la ruta xdist y otra para el fallback seguro.
  - [ ] El Builder deja en `execution_log.md` una medicion serial-vs-xdist sobre el mismo subset unitario y el mismo host.
  - [ ] `ruff`, tests focales, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** mantiene `010m` fuera de scope (CI) y `011i` fuera de scope (default futuro). No puede tocar la barrera canonica de handoff ni degradar el cierre a un run focal.
- **CONTRACT_GAP behavior:** si el opt-in local exige cambiar `pre_handoff_guard.py`, si `pytest-xdist` no puede integrarse sin abrir el default del runner, o si el fallback seguro no puede distinguir subset unitario apto de suite canonica, emitir `CG-WOT-2026-011e.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica implementacion viable toca CI o cambia el default del runner; parar si xdist rompe state-leak/cobertura del subset; parar si el subset seguro no puede definirse sin mezclar `010m` o `011i`.
- **Depende de:** -.

## T-011F-001 -- Contrato PS1 multiplataforma + launcher sin BOM/mojibake

- **ticket_id:** WOT-2026-011f
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011F-001
- **Plan-Link:** PLAN-011F-001
- **Premise:** `.gitattributes` aun no declara `*.ps1`; `scripts/launch_agent_terminals.ps1` conserva BOM UTF-8 en origen y secuencias mojibake (`???` verificado en lineas 91/100) aunque ya usa CRLF; `scripts/encoding_guard.py` conoce `.ps1` como texto pero su barrido repo-wide omite `scripts/**/*.ps1`, dejando fuera la principal superficie PowerShell del motor. `011j` ya cerro los writers BOM-safe in-scope; `011f` fija el contrato de fuente, no reabre la logica funcional del fix anterior.
- **Premise Re-check (read-only):** releer `.gitattributes`, `scripts/launch_agent_terminals.ps1`, `scripts/encoding_guard.py`, `tests/test_encoding_integrity.py`, `tests/test_launch_agent_terminals_script.py`, `tests/test_opencode_config_stability.py` y el reporte `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`; verificar por bytes que `launch_agent_terminals.ps1` sigue con BOM y CRLF; confirmar que `test_manager_smoke.ps1` ya esta limpio; ejecutar `validate --json --project-root <repo_destino>` antes del arranque.
- **Context Baseline Evidence:** gitattributes_ps1_rule=false; launcher_bom=true; launcher_crlf=true; launcher_mojibake_lines=91,100; encoding_guard_ps1_extension=true; encoding_guard_repo_wide_ps1_scope=false; generated_at=2026-06-20.
- **Files Likely Touched:**
  - Builder repo_motor: `.gitattributes`
  - Builder repo_motor: `scripts/launch_agent_terminals.ps1`
  - Builder repo_motor: `scripts/encoding_guard.py`
  - Builder repo_motor: `tests/test_encoding_integrity.py`
  - Builder repo_motor: `tests/test_launch_agent_terminals_script.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `tests/test_opencode_config_stability.py`; `tests/unit/test_launcher_powershell_syntax.py`; `scripts/test_manager_smoke.ps1`; `.agent/runtime/audit/bom_source_audit_WOT-2026-011c.md`; `scripts/check_encoding_guard.py`.
- **Forbidden Surfaces:** reabrir la logica funcional del launcher ya corregida por `011j`; broad-strip de BOM/mojibake fuera de las superficies declaradas; tocar `pre_handoff_guard.py`; tocar CI/workflows; editar historicos de backlog/control-chars congelados en 012a.
- **DoD:**
  - [ ] `.gitattributes` declara explicitamente el contrato de `*.ps1` (line endings deterministas y portables).
  - [ ] `scripts/launch_agent_terminals.ps1` queda sin UTF-8 BOM y conserva line endings coherentes con el contrato fijado.
  - [ ] Las secuencias mojibake verificadas del launcher se reconstruyen desde contexto confiable; no se aceptan strips ciegos ni sustituciones ambiguas.
  - [ ] `scripts/encoding_guard.py` incluye `scripts/**/*.ps1` (o cobertura repo-wide equivalente) dentro del scope real del guard.
  - [ ] Existe al menos una barrera FAIL-sin/PASS-con que demuestra que el launcher entra en scope del guard y que el estado previo con BOM habria fallado.
  - [ ] `python scripts/check_encoding_guard.py scripts/launch_agent_terminals.ps1`, tests focales, `ruff` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** depende de `011c` (fuente del fenomeno) y `011j` (writers BOM-safe ya corregidos), pero no reabre `011i`, `010m` ni la semantica de xdist. Conserva `010w` como dependencia de cierre Windows ya resuelta.
- **CONTRACT_GAP behavior:** si reconstruir el mojibake del launcher exige adivinar contenido sin contexto confiable, si ampliar el guard a `scripts/**/*.ps1` destapa deuda nueva fuera de las dos superficies PowerShell actuales, o si normalizar el archivo obliga a tocar logica funcional del launcher ajena al contrato de fuente, emitir `CG-WOT-2026-011f.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el target de line endings no puede verificarse en este host Windows; parar si el launcher deja de parsear sintacticamente tras la normalizacion; parar si el guard repo-wide sobre `.ps1` rompe por artefactos no declarados fuera de `scripts/launch_agent_terminals.ps1` y `scripts/test_manager_smoke.ps1`.
- **Depende de:** WOT-2026-010w (COMPLETED); WOT-2026-011c (COMPLETED); WOT-2026-011j (COMPLETED).

## T-011B-001 -- Relaunch timeout determinism en tests de relaunch

- **ticket_id:** WOT-2026-011b
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011B-001
- **Plan-Link:** PLAN-011B-001
- **Premise:** `bus/builder_relaunch.py` ya expone la costura `_BUILDER_START_VERIFY_TIMEOUT_SECONDS` con default `20.0`, y la familia de relaunch en `tests/test_supervisor.py` ya distingue los outcomes `builder_started_verified`, `timeout` y `builder_launch_unverified`. La deuda abierta por `011b` no es funcional sino de determinismo: cualquier prueba que dependa de la verificacion temporizada debe fijar su timeout de forma explicita y auditable para no heredar esperas del host ni del default productivo.
- **Premise Re-check (read-only):** releer `bus/builder_relaunch.py`, `bus/supervisor.py`, `tests/test_supervisor.py` (casos `test_relaunch_outcome_builder_started_verified`, `test_relaunch_emits_event_timeout`, `test_relaunch_outcome_builder_launch_unverified_when_no_signal`) y `tests/test_relaunch_evidence_capsule.py`; verificar que `_BUILDER_START_VERIFY_TIMEOUT_SECONDS` sigue declarado en `bus/builder_relaunch.py` con default `20.0`; confirmar que la semantica canonica del relaunch no debe cambiarse en este ticket; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque.
- **Context Baseline Evidence:** verify_timeout_env_declared=true; verify_timeout_default=20.0; relaunch_outcomes_covered=builder_started_verified|timeout|builder_launch_unverified; generated_at=2026-06-20.
- **Files Likely Touched:**
  - Builder repo_motor: `bus/builder_relaunch.py`
  - Builder repo_motor: `tests/test_supervisor.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `bus/supervisor.py`; `tests/test_relaunch_evidence_capsule.py`; `.agent/runtime/pytest-safe/last-run.json`; `.agent/collaboration/backlog.md`.
- **Forbidden Surfaces:** `scripts/pre_handoff_guard.py`; `scripts/run_pytest_safe.py`; CI/workflows; cambio del default runtime fuera del contrato de prueba; relajar el cierre canonico (`--level all`); `.env`; `privada/`; eventos del bus escritos manualmente.
- **DoD:**
  - [ ] Las pruebas de relaunch que ejercen verificacion temporal fijan explicitamente `BUILDER_START_VERIFY_TIMEOUT_SECONDS` o una costura equivalente determinista dentro del propio test.
  - [ ] El contrato productivo conserva `_BUILDER_START_VERIFY_TIMEOUT_DEFAULT = 20.0` y el env var canonico, salvo refactor semantico neutro.
  - [ ] Existe al menos una barrera FAIL-sin/PASS-con que demuestra que la ruta temporizada deja de depender del timeout default del host.
  - [ ] Las rutas `builder_started_verified` y `builder_launch_unverified` siguen cubiertas sin cambiar su semantica observable.
  - [ ] `ruff`, tests focales, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** no reabre `011e`, `011i` ni `010m`; no cambia politica de xdist, runner ni handoff. `011b` solo endurece el seam de timeout del relaunch y sus pruebas.
- **CONTRACT_GAP behavior:** si volver deterministas los tests exige cambiar la semantica productiva del relaunch, si la costura real del timeout cae fuera de `bus/builder_relaunch.py` / `tests/test_supervisor.py`, o si la unica forma de probar la ruta temporizada depende de sleeps wall-clock no acotables, emitir `CG-WOT-2026-011b.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica implementacion viable toca `scripts/run_pytest_safe.py` o `pre_handoff_guard.py`; parar si el fix convierte el timeout productivo en parametro solo de test; parar si el rojo real pertenece a otra familia de relaunch fuera del scope declarado.
- **Depende de:** -.

## T-013A-001 -- Robustecer test_approved_pending contra drift de topologia sandbox

- **ticket_id:** WOT-2026-013a
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013A-001
- **Plan-Link:** PLAN-013A-001
- **Premise:** `tests/test_controller_integration.py::test_approved_pending_returns_builder_implement` sigue fallando en aislamiento (`pytest -k approved_pending`) con `AssertionError: No JSON en output del controller`, mientras el ticket documenta que la causa es topologica: el fixture copia `agent_controller.py` dentro de un sandbox y el controller resuelve el proyecto desde `__file__.parent.parent`, apuntando al sandbox copiado en vez del motor real. La deuda de `013a` es de robustez del fixture/entorno de prueba; no debe convertirse en un rediseno del controller ni en una feature nueva de topologia.
- **Premise Re-check (read-only):** releer `tests/test_controller_integration.py`, `tests/test_controller_integration.py::sandbox`, `_run()`, `_REAL_CONTROLLER`, `EventBus` y `.agent/agent_controller.py`; reejecutar `python -m pytest tests/test_controller_integration.py -k approved_pending -q` para confirmar el rojo aislado actual; verificar que el fallo no proviene de `run_pytest_safe --level all` sino del fixture sandbox.
- **Context Baseline Evidence:** isolated_test_red=true; failing_test=`test_approved_pending_returns_builder_implement`; failure_signature=`No JSON en output del controller`; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder repo_motor: `tests/test_controller_integration.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `.agent/agent_controller.py`; `runtime/`; `bus/`; `tests/test_controller_integration.py` adyacentes; `.agent/runtime/pytest-safe/last-run.json`; `.agent/collaboration/backlog.md`.
- **Forbidden Surfaces:** anadir `--validate-topology` o cualquier feature nueva del controller en este ticket; tocar `.agent/agent_controller.py`; tocar `runtime/`, `bus/`, `scripts/run_pytest_safe.py`, `pre_handoff_guard.py`, CI/workflows o eventos del bus; convertir el fix en una reescritura general del sandbox.
- **DoD:**
  - [ ] `python -m pytest tests/test_controller_integration.py -k approved_pending -q` pasa en aislamiento.
  - [ ] El fix permanece acotado al fixture/driver de `tests/test_controller_integration.py`; no toca codigo productivo del controller.
  - [ ] Existe barrera FAIL-sin/PASS-con para el mismo test aislado, demostrada con worktree o revert parcial seguro.
  - [ ] `python -m pytest tests/test_controller_integration.py -q`, `ruff` sobre Python tocado, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
  - [ ] `execution_log.md` registra explicitamente que `013a` resolvio drift de topologia del test sin introducir feature nueva en produccion.
- **Integracion cross-ticket:** no reabre `011g`, `011h`, `011i` ni la deuda arquitectonica opcional de `--validate-topology`; si esa feature se vuelve necesaria, debe salir como follow-up separado.
- **CONTRACT_GAP behavior:** si el rojo aislado no puede resolverse sin tocar `.agent/agent_controller.py` o anadir una feature nueva de topologia, emitir `CG-WOT-2026-013a.md` y bloquear; `013a` esta congelado como fix test-only.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el unico fix viable cae en codigo productivo del controller; parar si el sandbox necesita reescritura sistemica fuera del test; parar si el mismo test ya no reproduce el fallo aislado al re-check.
- **Depende de:** -.

## T-011G-001 -- Politica explicita de loop rapido vs cierre canonico

- **ticket_id:** WOT-2026-011g
- **status:** frozen
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011G-001
- **Plan-Link:** PLAN-011G-001
- **Premise:** la frontera entre `loop rapido` (diagnostico local, reruns focales, evidencia provisional) y `cierre canonico` (suite canonia en HEAD, `validate 0/0`, handoff con eventos reales y cierre Manager) existe hoy como reglas dispersas en prompts y docs, pero no como politica corta, explicita y consistente. Las sesiones 011j, 011e y 013a obligaron a corregir varias veces claims sobre suite stale, wall-clock en background, `READY_FOR_REVIEW` por narrativa y cuando un ticket documental debe o no exigir pytest/ruff.
- **Premise Re-check (read-only):** releer `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md`, `prompts/audit_agent_output.md`, `QUICKSTART.md` y `AGENTS.md`; releer observaciones persistentes `obs-20260619-background-wallclock-not-canonical` y `obs-20260620-last-run-canonical-lives-in-motor`; verificar que la politica actual aparece fragmentada y que no hace falta tocar tooling para dejarla explicita.
- **Context Baseline Evidence:** stale_suite_rule_fragmented=true; canonical_last_run_in_motor=true; background_wallclock_noncanonical=true; handoff_requires_events=true; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder repo_motor: `prompts/orchestrator_launch_builder.md`
  - Builder repo_motor: `prompts/manager_review.md`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_motor: `QUICKSTART.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `prompts/audit_agent_output.md`; `AGENTS.md`; `PROJECT.md`; `.agent/runtime/memory/observations.jsonl`; `.agent/runtime/memory/MEMORY.md`.
- **Forbidden Surfaces:** `scripts/run_pytest_safe.py`; `scripts/pre_handoff_guard.py`; `scripts/run_gates_dispatch.py`; `.agent/agent_controller.py`; `bus/review_bridge.py`; tests; CI/workflows; cualquier cambio de semantica de handoff/cierre mas alla de documentarla; normalizar o retirar `011h` dentro de este ticket.
- **DoD:**
  - [ ] Existe una seccion explicita y corta que nombre `loop rapido` y `cierre canonico`, y delimite que evidencia cuenta para cada uno.
  - [ ] `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md` y `QUICKSTART.md` quedan alineados entre si respecto a suite canonia, `validate`, handoff y cierre.
  - [ ] Ningun texto tocado sigue permitiendo presentar pytest focal, wall-clock en background o tests aislados verdes como sustituto de suite canonica / `READY_FOR_REVIEW` / cierre canonico.
  - [ ] El ticket permanece documental: no toca scripts, gates, controller, review bridge, tests ni CI.
  - [ ] `python scripts/check_encoding_guard.py <docs_tocados>` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** reutiliza y hace visible la politica ya fijada por `010c`/`010q` y por las lecciones de `011j`/`011e`/`013a`; no reabre `011h`, `011i`, `010m` ni cambia tooling.
- **CONTRACT_GAP behavior:** si dejar la documentacion veraz exige cambiar semantica de `run_pytest_safe.py`, `pre_handoff_guard.py`, `.agent/agent_controller.py`, `run_gates_dispatch.py` o `review_bridge.py`, emitir `CG-WOT-2026-011g.md` y bloquear: `011g` es solo politica/documentacion.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la unica forma de resolver contradicciones documentales es tocar tooling productivo; parar si el ticket deja de ser puramente documental; parar si aparece conflicto con un ticket activo que toque los mismos prompts/docs y requiera serializacion.
- **Depende de:** WOT-2026-010c (COMPLETED); WOT-2026-010q (COMPLETED).

## T-011H-001 -- Barrera de archivado tambien en mark-ready

- **ticket_id:** WOT-2026-011h
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-011H-001
- **Plan-Link:** PLAN-011H-001
- **Premise:** `011a` ya cerro fail-closed `--session-close` cuando el archivado deja `archive_rename_uncommitted`, pero `--mark-ready` sigue auto-archivando `PLAN_/AUDIT_` cerrados desde `.agent/agent_controller.py` y puede dejar el mismo limbo `D old + ?? new` despues del handoff. La razon estable, la remediacion exacta y la deteccion en higiene ya existen; falta hacer fail-closed el camino de handoff, no reabrir closeout.
- **Premise Re-check (read-only):** confirmar `WOT-2026-011a` y `WOT-2026-011d` COMPLETED; releer `.agent/agent_controller.py` (`_auto_archive_closed_artifacts()`, `_handle_mark_ready()`), `scripts/pre_handoff_guard.py`, `tests/test_agent_controller.py`, `tests/test_pre_handoff_guard.py`, `tests/unit/test_scope_gate.py`; verificar que el auto-archivado de mark-ready ocurre despues del guard y que hoy no promueve `archive_rename_uncommitted` a bloqueo propio; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque.
- **Context Baseline Evidence:** stable_reason=`archive_rename_uncommitted`; mark_ready_auto_archive=true; closeout_barrier_exists=true; pre_handoff_guard_knows_reason=true; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder repo_motor: `.agent/agent_controller.py`
  - Builder repo_motor: `tests/test_agent_controller.py`
  - Builder repo_motor: `tests/test_pre_handoff_guard.py`
  - Builder repo_motor: `tests/unit/test_scope_gate.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/closeout_steps/archival.py`; `scripts/session_closeout.py`; `scripts/delivery_hygiene_check.py`; `scripts/archive_collaboration_artifacts.py`; `.agent/runtime/events/events.jsonl`; `.agent/collaboration/backlog.md`.
- **Forbidden Surfaces:** reabrir `--session-close`; auto-commit dentro del archivador; borrado destructivo de artefactos archivados; tocar workflows/CI, `scripts/run_pytest_safe.py`, `scripts/pre_handoff_guard.py` fuera de la barrera estrictamente necesaria, `privada/`, `.env` o eventos del bus manualmente.
- **DoD:**
  - [ ] `--mark-ready` falla cerrado con razon estable `archive_rename_uncommitted` si su auto-archivado deja limbo `D old + ?? new`.
  - [ ] El diagnostico conserva origen, destino y comando de reconcile exacto, alineado con `011a`.
  - [ ] El caso limpio de `--mark-ready` sigue alcanzando `READY_FOR_REVIEW` sin falso positivo.
  - [ ] Existe al menos una barrera FAIL-sin/PASS-con sobre la ruta real de mark-ready, no solo sobre helper aislado.
  - [ ] El ticket no introduce auto-commit del archivador ni relaja el handoff canonico.
  - [ ] `python -m pytest tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py -q`, `ruff check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `uv run ruff format --check .agent/agent_controller.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py tests/unit/test_scope_gate.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** reutiliza la razon estable cerrada por `011a`; no reabre el closeout de `011a`, ni la retirada de legacy de `011d`, ni introduce renames automaticos de cierre.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige auto-commit del archivador, cambiar el contrato del archivado fuera de mark-ready o tocar politicas de bus/controller fuera del flujo declarado, emitir `CG-WOT-2026-011h.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la deteccion solo puede expresarse como `dirty tree` generico; parar si reproducir el limbo real exige tocar `--session-close` en vez de la ruta de handoff; parar si el fix solo puede vivir fuera de las superficies declaradas.
- **Depende de:** WOT-2026-011a (COMPLETED); WOT-2026-011d (COMPLETED).

## T-013B-001 -- [CANCELADO POR PREMISA FALSA / ABSORBED] Aislar tests no parallel-safe del subset unit

- **ticket_id:** WOT-2026-013b
- **status:** absorbed (cancelado por premisa falsa; absorbido por WOT-2026-011i)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **closed:** 2026-06-21
- **Evidence:** `CG-WOT-2026-013b.md` (FINAL); `_archive/backlog_done.md` (fila + ficha absorbed).
- **Por que se cancela (resumen, NO spec operativa):** el ticket presumio sucesivamente que el rojo del
  subset unit bajo xdist era (1) "3 tests" y luego (2) "la familia unica `test_project_root_resolution.py`".
  Ambas premisas fueron REFUTADAS por reproduccion: tres corridas del mismo subset dieron 12<->37 fallos con
  el archivo dominante cambiando entre corridas, y cada archivo implicado pasa aislado bajo `-n 8`. No es una
  familia de tests aislable: es contencion de reparto cross-archivo, propiedad del runner. La unica via verde
  (`--dist loadscope`) era Forbidden Surface de este contrato por pertenecer al runner.
- **Resolucion:** la deuda real (politica de distribucion del runner) se absorbe en `T-011I-001`. No se
  relanza Builder sobre 013b. Este bloque se conserva solo como registro historico; su antiguo cuerpo
  operativo (objetivo de "hacer parallel-safe un archivo", DoD, Forbidden Surfaces, `red_is_single_file_family=true`)
  queda anulado y NO debe leerse como especificacion activa.
- **Sucesor:** WOT-2026-011i (T-011I-001).

## T-011I-001 -- [NOT-PURSUED] Default xdist para `--level unit`

- **ticket_id:** WOT-2026-011i
- **status:** not-pursued (opt-in 011e + piloto CI 010m son el estado final)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **closed:** 2026-06-21
- **Evidence:** `CG-WOT-2026-011i.md`; `_archive/backlog_done.md` (fila + ficha not-pursued).
- **Por que se cierra (resumen, NO spec operativa):** el contrato (incluso tras absorber 013b) presumio que
  `--dist loadscope` estabilizaria el subset unit para activar xdist por defecto. REFUTADO por reproduccion:
  loadscope reduce pero no elimina el rojo (3 corridas: 3->1->3 failed, conjunto variable). Los 3 tests
  persistentes (test_upgrade_path_suggestion, test_scan_current_project, test_no_inline_ticket_regex) pasan
  SERIAL y dependen de estado global del proceso/repo (cwd, git, escaneo del proyecto vivo): ninguna politica
  de reparto de xdist los aisla.
- **Resolucion:** el default xdist NO se promueve. El opt-in local (`011e`) y el piloto CI non-blocking
  (`010m`) quedan como solucion suficiente y vigente. `--level all` permanece serial e intacto. El antiguo
  cuerpo operativo de este contrato (objetivo loadscope, DoD, evidencia `fix_is_distribution_policy`) queda
  ANULADO y no debe leerse como especificacion activa.
- **Follow-up opcional (no contratado):** robustecer esos 3 tests para ejecucion paralela (fixtures que
  aislen cwd/git/escaneo). Solo si compensa recuperar la ergonomia del default.

## T-010X-001 -- Sustituir gitleaks-action licenciado por CLI OSS

- **ticket_id:** WOT-2026-010x
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-010X-001
- **Plan-Link:** PLAN-010X-001
- **Premise:** `.github/workflows/security-audit.yml` aun invoca `gitleaks/gitleaks-action@v2`, mientras el motor ya dispone de semilla portable de configuracion (`agent_system/templates/gitleaks.config.toml`) y de una barrera de alineacion del workflow en `tests/unit/test_hook_ci_alignment.py`. La deuda abierta por `010x` es reemplazar la dependencia del action licenciado/runtime JS por una invocacion CLI OSS de gitleaks, no redisenar la politica de allowlists ni el resto del workflow de seguridad.
- **Premise Re-check (read-only):** releer `.github/workflows/security-audit.yml`, `tests/unit/test_hook_ci_alignment.py`, `agent_system/templates/gitleaks.config.toml`, `.pre-commit-config.yaml` y las notas historicas de `WOT-2026-004a` / `WOT-2026-004b` en `_archive/backlog_done.md`; verificar que el workflow sigue usando `gitleaks/gitleaks-action@v2`; confirmar que la semilla portable existe y que `test_hook_ci_alignment.py` sigue siendo la barrera natural del workflow; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de arrancar.
- **Context Baseline Evidence:** workflow_uses_licensed_action=true; portable_seed_exists=true; ci_alignment_test_exists=true; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder repo_motor: `.github/workflows/security-audit.yml`
  - Builder repo_motor: `tests/unit/test_hook_ci_alignment.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `agent_system/templates/gitleaks.config.toml`; `.pre-commit-config.yaml`; `scripts/install_agent_system.py`; `_archive/backlog_done.md`; `.agent/runtime/pytest-safe/last-run.json`.
- **Forbidden Surfaces:** `agent_system/templates/gitleaks.config.toml`; `.pre-commit-config.yaml`; `scripts/install_agent_system.py`; `tests/unit/test_install_agent_system.py`; `scripts/pip_audit_project.py`; otros workflows de GitHub Actions; cambios de politica de allowlist o de ignores de seguridad; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD:**
  - [ ] `.github/workflows/security-audit.yml` deja de referenciar `gitleaks/gitleaks-action@v2`.
  - [ ] El workflow ejecuta gitleaks por CLI OSS directa y no requiere `GITLEAKS_LICENSE` ni `GITHUB_TOKEN` para el paso de gitleaks.
  - [ ] La invocacion preserva semantica fail-closed ante leaks y usa una fuente de configuracion ya existente en el repo, sin reabrir la politica de allowlists.
  - [ ] `tests/unit/test_hook_ci_alignment.py` gana al menos una barrera FAIL-sin/PASS-con que falle si reaparece el action licenciado y pase con la invocacion CLI.
  - [ ] `python -m pytest tests/unit/test_hook_ci_alignment.py -v`, `ruff check tests/unit/test_hook_ci_alignment.py`, `uv run ruff format --check tests/unit/test_hook_ci_alignment.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** reutiliza el trabajo de politica/config ya fijado por `WOT-2026-004a` y `WOT-2026-004b`, pero no reabre esa politica ni mezcla `pip-audit`, `011g` o deudas de dependencias bloqueadas como `WT-2026-256a`.
- **CONTRACT_GAP behavior:** si la sustitucion OSS solo puede hacerse introduciendo otro action de terceros/licenciado, si exige tocar la politica/config de gitleaks fuera de las superficies declaradas, o si el unico camino verde relaja el fail-closed del escaneo, emitir `CG-WOT-2026-010x.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el workflow necesita redisenarse mas alla del paso de gitleaks; parar si la invocacion CLI exige cambios de politica/config fuera de scope; parar si la barrera de `tests/unit/test_hook_ci_alignment.py` no puede expresar la regresion sin tocar otras familias de tests o workflows.
- **Depende de:** -.

## T-013C-001 -- [BLOCKED-FINAL] Robustecer 3 tests global-state (cura en producto)

- **ticket_id:** WOT-2026-013c
- **status:** blocked-final (CG-WOT-2026-013c.md; la cura cae en superficie de producto / rompe invariante de test)
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **closed:** 2026-06-21
- **Evidence:** `CG-WOT-2026-013c.md`; `_archive/backlog_done.md` (fila + ficha blocked-final).
- **Por que se bloquea (resumen, NO spec operativa):** el contrato era tests-only. Fase 0 confirmo serial
  verde y xdist rojo en los 3 tests. Causa raiz: el `rglob` del arbol vivo recorre `tests/sandbox/session_<PID>`
  que otros workers borran -> `FileNotFoundError` antes del filtro de exclusion (que YA existe en producto,
  pero es post-rglob). En 2 de los 3 tests ese rglob vive en PRODUCTO (project_scanner / project_paths) =
  Forbidden Surface. La alternativa solo-conftest (sandbox fuera del arbol) volvia verde el triple xdist
  (estable x3) pero rompio `test_windows_safe_temp_runtime` (exige sandbox dentro): 10 failed en `--level all`.
  Conflicto de invariantes irreducible sin tocar producto.
- **Resolucion:** no se cierra como entregado; sin diff productivo (commit experimental revertido). El antiguo
  cuerpo operativo (objetivo, DoD, criterios tests-only) queda ANULADO. El opt-in xdist (011e) + piloto CI
  (010m) siguen vigentes; default xdist no perseguido (011i).
- **Sucesor recomendado (no contratado):** ticket de PRODUCTO acotado a hacer el escaneo robusto a borrados
  concurrentes (`scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`): os.walk con poda de
  `tests/sandbox` antes de descender, o tolerar `FileNotFoundError` de subdirs que desaparecen.
- **Depende de:** WOT-2026-011e (COMPLETED); WOT-2026-010m (COMPLETED).



## T-013D-001 -- Escaneo robusto de proyecto ante borrados concurrentes

- **ticket_id:** WOT-2026-013d
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013D-001
- **Plan-Link:** PLAN-013D-001
- **Premise:** `013c` cerro `BLOCKED-FINAL` con una causa raiz ya verificada en PRODUCTO, no en tests-only: `scripts/project_scanner.py` recorre el arbol vivo dos veces por `rglob` (`_collect_local_modules()` en la zona de la linea 344, `scan_project()` en la zona de la linea 615) y `agent_system/scripts/project_paths.py` lo hace una tercera vez por `rglob(".agent")` (linea 59 aprox.). Esos recorridos pueden bajar a `tests/sandbox/test_runtime/session_*` mientras otros workers borran subdirectorios, disparando `FileNotFoundError`/`Acceso denegado` antes del filtro de exclusion ya existente. La deuda correcta es endurecer el escaneo y su higiene de sandbox, no reabrir la politica xdist/default del runner.
- **Premise Re-check (read-only):** confirmar `T-013C-001` en `blocked-final`; releer `scripts/project_scanner.py`, `agent_system/scripts/project_paths.py`, `tests/unit/test_project_scanner.py`, `tests/test_project_paths.py`, `tests/unit/test_detect_version.py`, `tests/unit/test_no_inline_ticket_regex.py`, `tests/conftest.py` y `tests/unit/test_windows_safe_temp_runtime.py`; verificar que los tres recorridos `rglob` siguen existiendo y que `tests/sandbox/test_runtime` sigue siendo superficie volatil real; recapturar el baseline de `session_dirs` bajo `tests/sandbox/test_runtime`; ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque.
- **Context Baseline Evidence:** `rglob_sites=3 (project_scanner:_collect_local_modules + scan_project; project_paths:resolve_paths)`; `session_dirs=566`; `triple_xdist_red_verified=true`; `generated_at=2026-06-21`.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/project_scanner.py`
  - Builder repo_motor: `agent_system/scripts/project_paths.py`
  - Builder repo_motor: `tests/unit/test_project_scanner.py`
  - Builder repo_motor: `tests/test_project_paths.py`
  - Builder repo_motor: `tests/unit/test_detect_version.py`
  - Builder repo_motor: `tests/unit/test_no_inline_ticket_regex.py`
  - Builder repo_motor: `tests/conftest.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `CG-WOT-2026-013c.md`; `prompts/audit_agent_output.md`; `tests/README.md`; `tests/ARCHITECTURE.md`; `docs/test_performance/test_performance_followup_WOT-2026-010k.md`; `.agent/runtime/pytest-safe/last-run.json`.
- **Forbidden Surfaces:** `scripts/run_pytest_safe.py`; `.github/workflows/quality-gates.yml`; tickets cerrados `011e`/`010m`/`011i`; `runtime/project_root.py`; `.agent/agent_controller.py`; bus/supervisor/controller; mover el sandbox fuera del arbol como salida rapida; relajar asserts con mocks/floors/xfail/skip para ocultar el rojo; borrar historico o runtime fuera de `tests/sandbox/test_runtime`.
- **DoD:**
  - [ ] Los 3 puntos de escaneo verificados quedan robustos frente a borrados concurrentes y el fix cubre tambien el recorrido de `scan_project()` (no solo `_collect_local_modules()`).
  - [ ] Existe limpieza determinista del ruido en `tests/sandbox/test_runtime`, gestionada via fixture/harness en `tests/conftest.py` (el sandbox es efecto colateral controlado, no superficie de edicion manual), y `execution_log.md` registra baseline + reconciliacion usada para la verificacion final.
  - [ ] `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` queda verde en al menos 3 corridas consecutivas sobre el mismo host.
  - [ ] `python -m pytest tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py -q`, `ruff check scripts/project_scanner.py agent_system/scripts/project_paths.py tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `uv run ruff format --check scripts/project_scanner.py agent_system/scripts/project_paths.py tests/unit/test_project_scanner.py tests/test_project_paths.py tests/unit/test_detect_version.py tests/unit/test_no_inline_ticket_regex.py tests/conftest.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
  - [ ] El diff productivo queda acotado a escaneo de producto + tests/fixtures declarados; no toca runner, CI ni la politica xdist/default.
- **Integracion cross-ticket:** absorbe literalmente el hallazgo de `013c` sin reabrir la familia de politica xdist (`011e`/`010m`/`011i`). El objetivo no es promover default xdist, sino quitar una causa raiz de producto que hoy contamina pruebas y latencia.
- **CONTRACT_GAP behavior:** si la unica cura segura exige tocar `scripts/run_pytest_safe.py`, `quality-gates.yml`, la politica default/opt-in de xdist, o reconciliar la invariante sandbox-dentro-vs-fuera fuera de las superficies declaradas, emitir `CG-WOT-2026-013d.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el fix exige cambiar la politica del runner o CI; parar si la unica salida verde mueve el sandbox fuera del arbol o rompe la invariante cubierta por `tests/unit/test_windows_safe_temp_runtime.py`; parar si el rojo dominante se desplaza a otra familia no declarada y deja de ser reproducible con el triple xdist acordado.
- **Depende de:** WOT-2026-013c (BLOCKED-FINAL).

## T-013E-001 -- Inventario auditable de valor, uso y poda segura de la suite

- **ticket_id:** WOT-2026-013e
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013E-001
- **Plan-Link:** PLAN-013E-001
- **Premise:** despues de `010j`, `010k`, `011e`, `010m` y `013d`, el motor ya tiene evidencia verificada sobre hotspots, frontera xdist y algunos tests de alto coste o alto acoplamiento, pero sigue sin existir un inventario durable que distinga regresiones core, barreras estructurales, candidatos legacy, candidatos redundantes y zonas `unknown`. Sin ese inventario, cualquier poda futura corre el riesgo de mezclar protecciones reales con ruido historico o de reabrir familias ya cerradas por intuicion.
- **Premise Re-check (read-only):**
  - releer `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_followup.md` y `docs/test_performance/test_selection.md`;
  - releer `tests/README.md`, `tests/ARCHITECTURE.md`, `scripts/run_pytest_safe.py`, `pytest.ini` y `.agent/runtime/pytest-safe/last-run.json` para fijar el contrato actual de suite/runner;
  - verificar en `backlog.md`, `ticket_contracts.md` y `plan_graph.md` que `011e`, `010m`, `011i`, `013c` y `013d` ya cerraron la frontera runner/xdist/producto que `013e` NO debe reabrir;
  - inventariar read-only las familias top-level bajo `tests/` y los marcadores estructurales existentes (`slow`, `integration`, `skipif`, `xfail` o equivalentes);
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** motor_head=162e506; destino_head=0bd5171; validate_result=0 errors / 0 warnings; active_ticket=WOT-2026-013d COMPLETED; backlog_state=WOT-2026-013e pending; generated_at=2026-06-21.
- **Files Likely Touched:**
  - Builder: `docs/test_performance/test_suite_audit_WOT-2026-013e.md`
  - Builder: `.agent/collaboration/execution_log.md`
  - Read/inspect only: `tests/`, `tests/README.md`, `tests/ARCHITECTURE.md`, `scripts/run_pytest_safe.py`, `pytest.ini`, `pyproject.toml`, `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_followup.md`, `docs/test_performance/test_selection.md`, `.agent/runtime/pytest-safe/last-run.json`, `.agent/collaboration/backlog.md`
- **Forbidden Surfaces:** `tests/`; `scripts/run_pytest_safe.py`; `pytest.ini`; `pyproject.toml`; `uv.lock`; CI/workflows; `scripts/run_gates_dispatch.py`; `scripts/pre_handoff_guard.py`; `privada/`; `.env`; eventos del bus escritos manualmente; reabrir `011e`, `010m`, `011i` o `013d`; borrar, `xfail`, `skip` o relajar tests en este ticket.
- **DoD:**
  - [ ] Existe un reporte durable en `repo_motor/docs/test_performance/test_suite_audit_WOT-2026-013e.md`.
  - [ ] El reporte inventaria la suite por familias o subsistemas con conteo auditable y clasificacion `core regression`, `structural gate`, `legacy candidate`, `redundant candidate` o `unknown`.
  - [ ] Cada clasificacion explicita si esta soportada por evidencia verificada (docs previas, markers, runner/gates, historial de tickets, coste/uso observable) o si queda como inferencia limitada.
  - [ ] El reporte lista tests o familias lentas, marks/skip estructurales, barreras canonicas del runner/handoff y cualquier debt legacy detectable sin tocar codigo productivo.
  - [ ] El reporte identifica follow-ups pequenos y verificables para poda o refactor, cada uno con superficie acotada y sin mezclar runner, CI, producto y borrado masivo en una sola propuesta.
  - [ ] El reporte deja explicito que `013e` no borra ni relaja tests y que las fronteras cerradas por `011e`, `010m`, `011i` y `013d` quedan fuera de scope salvo evidencia nueva que obligue a `CONTRACT_GAP`.
  - [ ] `execution_log.md` registra una linea final: `Reporte docs/test_performance/test_suite_audit_WOT-2026-013e.md creado. Validate: exit code 0, 0 errors, 0 warnings.`
  - [ ] `git diff --name-only` del `repo_motor` se limita al artefacto documental del ticket.
  - [ ] `python scripts/check_encoding_guard.py docs/test_performance/test_suite_audit_WOT-2026-013e.md` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** `013e` consume evidencia de `010j`, `010k`, `011e`, `010m` y `013d`, pero no reabre sus decisiones. Ningun follow-up de poda o racionalizacion de tests debe arrancar sin leer primero el reporte final de `013e`.
- **CONTRACT_GAP behavior:** si el inventario no puede separar barreras core/estructurales de candidatos a poda sin tocar `tests/`, runner, CI o producto; si la evidencia actual no permite ni siquiera proponer follow-ups pequenos con criterio verificable; o si la auditoria exige reabrir una frontera ya cerrada de `011e`, `010m`, `011i` o `013d`, emitir `CG-WOT-2026-013e.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. El Builder audita y reporta; no poda, no relaja tests y no reinterpreta por intuicion la politica del runner.
- **STOP conditions:** parar si la unica forma de justificar una clasificacion exige editar tests o tooling; parar si el resultado depende de output viejo no reconciliado con el HEAD actual; parar si la recomendacion util solo puede expresarse como poda masiva o como reabrir la familia xdist/producto en vez de abrir follow-ups pequenos.
- **Depende de:** WOT-2026-010j (COMPLETED); WOT-2026-010k (COMPLETED); WOT-2026-011e (COMPLETED); WOT-2026-010m (COMPLETED); WOT-2026-013d (COMPLETED).


## T-013F-001 -- Podar tests/deprecated/ (Goose retirado, ya fuera del runner)

- **ticket_id:** WOT-2026-013f
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013F-001
- **Plan-Link:** PLAN-013F-001
- **Premise:** `WOT-2026-013e` confirmo que `tests/deprecated/` contiene solo dos tests Goose (`test_goose_triggers.py`, `test_goose_realworld.py`) ya marcados `DEPRECATED (WT-2026-254a)` y excluidos del runner por `pytest.ini:norecursedirs`, con 0 tests recolectados. La poda correcta es retirar ese directorio y dejar trazabilidad del retiro en `tests/integration/RETIRED_TESTS.md`, sin tocar el runner ni mezclar otros candidatos legacy como `test_ejemplo` o `test_goose_native_skill`.
- **Premise Re-check (read-only):**
  - verificar que `pytest.ini` sigue excluyendo `tests/deprecated` via `norecursedirs`;
  - verificar que `tests/deprecated/test_goose_triggers.py` y `tests/deprecated/test_goose_realworld.py` siguen marcados `DEPRECATED (WT-2026-254a)`;
  - buscar referencias vivas a `tests/deprecated/` y distinguirlas de referencias historicas o de contexto generado; en particular, confirmar que `scripts/cleanup_legacy.py` apunta al antiguo `scripts/test_goose_realworld.py`, no a `tests/deprecated/test_goose_realworld.py`;
  - verificar que `tests/integration/RETIRED_TESTS.md` existe como precedente canonico para documentar retiros seguros;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** motor_head=4eb0fbb; destino_head=b722c1b; repo_motor_status='main...origin/main clean'; repo_destino_status='main...origin/main clean'; collect_only_baseline=3111; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `tests/deprecated/`
  - Builder repo_motor: `tests/integration/RETIRED_TESTS.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `pytest.ini`; `docs/test_performance/test_suite_audit_WOT-2026-013e.md`; `scripts/cleanup_legacy.py`; `tests/unit/test_cleanup_legacy.py`; `tests/test_goose_native_skill.py`; `tests/unit/test_ejemplo.py`.
- **Forbidden Surfaces:** `pytest.ini`; `scripts/run_pytest_safe.py`; `docs/test_performance/test_suite_audit_WOT-2026-013e.md`; `scripts/cleanup_legacy.py`; `tests/test_goose_native_skill.py`; `tests/unit/test_ejemplo.py`; CI/workflows; cualquier codigo de producto fuera de `tests/deprecated/` y `tests/integration/RETIRED_TESTS.md`; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] El diff productivo del motor se limita a borrar `tests/deprecated/` y documentar el retiro en `tests/integration/RETIRED_TESTS.md`.
  - [ ] `python -m pytest tests --collect-only -q -p no:cacheprovider` mantiene 3111 tests tras la poda, y `execution_log.md` registra el conteo pre y post.
  - [ ] `tests/integration/RETIRED_TESTS.md` deja explicito que los tests retirados cubrian Goose, subsistema deprecado por `WT-2026-254a`, ya excluido del runner.
  - [ ] `python scripts/run_pytest_safe.py --level all` termina verde y el cierre lee la evidencia canonica sobre el commit entregado.
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
  - [ ] No se tocan `pytest.ini`, runner, CI, `test_goose_native_skill.py`, `test_ejemplo` ni producto vivo.
- **Integracion cross-ticket:** consume el follow-up FU-013E-2 sin reabrir `013e` ni mezclar FU-013E-1 (`test_ejemplo` / `test_goose_native_skill`) ni `013g` (coste unknown). Cualquier hallazgo que obligue a tocar runner o producto se devuelve por `CONTRACT_GAP`.
- **CONTRACT_GAP behavior:** si aparece un consumidor vivo de `tests/deprecated/`, si el borrado cambia el conteo recolectado, o si la justificacion del retiro exige tocar runner/producto o mezclar otros candidatos legacy, emitir `CG-WOT-2026-013f.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si `tests/deprecated/` resulta ser fuente viva para algun consumidor canonico; parar si el collect-only post-poda ya no da 3111; parar si la unica salida verde exige tocar `pytest.ini`, `scripts/run_pytest_safe.py` o codigo fuera de las superficies declaradas.
- **Depende de:** WOT-2026-013e (COMPLETED).


## T-013G-001 -- Diagnosticar coste no explicado de test_upgrade_path_suggestion

- **ticket_id:** WOT-2026-013g
- **status:** frozen
- **deliverable_type:** analysis
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013G-001
- **Plan-Link:** PLAN-013G-001
- **Premise:** `WOT-2026-013e` y la evidencia previa (`010j`, `010p`) dejaron a `tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion` como el unico hotspot `unknown`: aparece como outlier #2-#3 (~59-70s) pese a tener cuerpo trivial (3 asserts). La deuda correcta es medir y explicar el coste real con evidencia fresca y reproducible, sin tocar el test ni producto en este ticket.
- **Premise Re-check (read-only):**
  - releer `docs/test_performance/test_performance_baseline.md`, `docs/test_performance/test_performance_variance.md` y `docs/test_performance/test_suite_audit_WOT-2026-013e.md`;
  - releer `tests/unit/test_detect_version.py` y confirmar que `test_upgrade_path_suggestion` sigue teniendo cuerpo trivial y pertenece a `TestVersionDetection`;
  - verificar que `python -m pytest` acepta `--durations` para medicion focal aislada del archivo/clase/test;
  - verificar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado;
  - confirmar que el ticket sigue siendo `analysis` y que ninguna superficie de codigo entra en `Files Likely Touched`.
- **Context Baseline Evidence:** motor_head=bc658f8; destino_head=<post-closeout-013f>; baseline_010j='59.22s'; variance_010p='69.79s / 67.91s'; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `tests/unit/test_detect_version.py`; `docs/test_performance/test_performance_baseline.md`; `docs/test_performance/test_performance_variance.md`; `docs/test_performance/test_suite_audit_WOT-2026-013e.md`; `.agent/runtime/pytest-safe/last-run.json`.
- **Forbidden Surfaces:** `tests/unit/test_detect_version.py`; cualquier otro test; producto Python; `scripts/run_pytest_safe.py`; `pytest.ini`; CI/workflows; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Existe un reporte durable en `repo_motor/docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`.
  - [ ] El reporte documenta mediciones reproducibles que expliquen la mayor parte del coste observado o cierra explicitamente `sin optimizacion segura` con evidencia.
  - [ ] El reporte separa [V] verificado de [I] inferencia en cada conclusion sustantiva.
  - [ ] El reporte recomienda una optimizacion local concreta o descarta intervenir en este ticket, sin tocar test ni producto.
  - [ ] `execution_log.md` registra una linea final: `Reporte docs/test_performance/test_upgrade_cost_WOT-2026-013g.md creado. Validate: exit code 0, 0 errors, 0 warnings.`
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
- **Integracion cross-ticket:** consume FU-013E-3 sin reabrir `013e`, `010k` ni la familia xdist. Si la explicacion real exige editar el test o producto, devolver por `CONTRACT_GAP` y abrir ticket `code` separado.
- **CONTRACT_GAP behavior:** si la unica forma de explicar el coste exige editar `tests/unit/test_detect_version.py` o producto, si la medicion no es reproducible entre corridas comparables, o si el deliverable deja de ser puramente analitico, emitir `CG-WOT-2026-013g.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el analisis deriva en cambios de codigo; parar si la causa solo puede expresarse como intuicion no medida; parar si la medicion depende de output historico no reconciliado en vez de evidencia fresca.
- **Depende de:** WOT-2026-013e (COMPLETED).


## T-013H-001 -- Eliminar renames sin commitear del archivado canonico

- **ticket_id:** WOT-2026-013h
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013H-001
- **Plan-Link:** PLAN-013H-001
- **Premise:** `011a` y `011h` ya endurecieron las barreras fail-closed alrededor de `archive_rename_uncommitted`, pero la deuda estructural persiste en la ruta de archivado/cierre: tras `013e`, `013f` y `013g` el siguiente ciclo siguio heredando el limbo `D old + ?? new` y exigio reconcile manual en `repo_destino`. La solucion correcta pertenece al archivado canonico y su closeout, no a reabrir xdist, producto ni a relajar los guards.
- **Premise Re-check (read-only):**
  - releer `scripts/archive_collaboration_artifacts.py`, `scripts/closeout_steps/archival.py`, `scripts/session_closeout.py`, `.agent/agent_controller.py` y `scripts/delivery_hygiene_check.py`;
  - releer `tests/test_archive_collaboration_artifacts.py`, `tests/test_session_closeout.py`, `tests/test_agent_controller.py` y `tests/test_pre_handoff_guard.py`;
  - confirmar en el historico reciente del `repo_destino` que `013e`, `013f` y `013g` necesitaron reconcile manual del archivado (`archive_rename_uncommitted`);
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del handoff y dejar constancia del estado.
- **Context Baseline Evidence:** source_commits=`4eb0fbb -> bc658f8 -> cf5a4bc`; repeated_manual_reconcile=`013e, 013f, 013g`; previous_barriers=`011a closeout fail-closed`, `011h mark-ready fail-closed`; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/archive_collaboration_artifacts.py`
  - Builder repo_motor: `scripts/closeout_steps/archival.py`
  - Builder repo_motor: `scripts/session_closeout.py`
  - Builder repo_motor: `tests/test_archive_collaboration_artifacts.py`
  - Builder repo_motor: `tests/test_session_closeout.py`
  - Builder repo_motor: `tests/test_agent_controller.py`
  - Builder repo_motor: `tests/test_pre_handoff_guard.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `scripts/delivery_hygiene_check.py`; `scripts/reconcile_ticket.py`; `tests/test_mark_ready_motor_scope.py`; `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`; `.agent/runtime/memory/UPSTREAM_LEARNINGS.md`.
- **Forbidden Surfaces:** auto-commitear artefactos historicos desde el archivador; relajar o borrar la razon estable `archive_rename_uncommitted`; `scripts/run_pytest_safe.py`; CI/workflows; tickets cerrados `011e`/`010m`/`011i`/`013d`/`013g`; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] La ruta canonica de archivado/cierre deja de heredar `archive_rename_uncommitted` al ticket siguiente, o falla cerrado en el mismo ciclo antes de dejar el limbo persistente.
  - [ ] Existe al menos una barrera con repo git real que falla sin el fix y pasa con el fix sobre el patron repetido de delete+untracked del archivado.
  - [ ] `tests/test_archive_collaboration_artifacts.py`, `tests/test_session_closeout.py`, `tests/test_agent_controller.py` y `tests/test_pre_handoff_guard.py` cubren la semantica final sin auto-commit oculto.
  - [ ] La remediacion mantiene la trazabilidad de `STRATEGY_` / `AUDIT_` archivados y no convierte el cierre en pass-open.
  - [ ] `python -m pytest tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py -q`, `ruff check scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py`, `uv run ruff format --check scripts/archive_collaboration_artifacts.py scripts/closeout_steps/archival.py scripts/session_closeout.py tests/test_archive_collaboration_artifacts.py tests/test_session_closeout.py tests/test_agent_controller.py tests/test_pre_handoff_guard.py`, `python scripts/run_pytest_safe.py --level all` y `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` quedan verdes.
- **Integracion cross-ticket:** `013h` sucede a `013g` y refina la deuda historica detectada ya en `010u`/`011a`/`011h`; no reabre `013g`, no toca la familia xdist y no sustituye el reconcile manual por auto-commit opaco.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige auto-commitear historicos, reescribir la semantica de cierre completa o tocar superficies fuera del archivado/cierre declaradas, emitir `CG-WOT-2026-013h.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la reproduccion real deja de concentrarse en `archive_collaboration_artifacts.py` / closeout y pasa a otra deuda ajena; parar si la unica via verde rompe la trazabilidad de los artefactos archivados; parar si la solucion exige editar el bus a mano o introducir un cierre pass-open.
- **Depende de:** WOT-2026-011h (COMPLETED); WOT-2026-013g (COMPLETED).

## T-013I-001 -- Higiene de purge de sandbox para latencia operacional

- **ticket_id:** WOT-2026-013i
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013I-001
- **Plan-Link:** PLAN-013I-001
- **Premise:** `WOT-2026-013g` verifico que >99% del coste observado en el outlier `test_upgrade_path_suggestion` no vive en el test ni en producto, sino en el `sessionstart` de `tests/conftest.py`: `_purge_orphan_session_dirs()` purga sandboxes `session_*` huerfanos acumulados bajo `tests/sandbox/test_runtime/`. La barrera de `013d` es correcta y NO debe retirarse, pero la implementacion actual deja una latencia operacional visible cuando el volumen historico crece (568 dirs medidos en `013g`).
- **Premise Re-check (read-only):**
  - releer `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md` y confirmar que la atribucion principal del coste sigue anclada al purge de `tests/conftest.py`;
  - releer `tests/conftest.py` y ubicar `_purge_orphan_session_dirs()` y `_project_temp_environment()` como la ruta real de higiene;
  - releer `tests/unit/test_project_scanner.py`, `tests/unit/test_windows_safe_temp_runtime.py`, `tests/unit/test_detect_version.py` y `tests/unit/test_no_inline_ticket_regex.py` para fijar las barreras heredadas de `013d`;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** source_ticket=WOT-2026-013g; source_report_commit=cf5a4bc; current_motor_head=103849a; current_destino_head=06732f6; historical_orphan_dirs=568; validate_result=0 errors / 0 warnings; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `tests/conftest.py`
  - Builder repo_motor: `tests/unit/test_project_scanner.py`
  - Builder repo_motor: `tests/unit/test_windows_safe_temp_runtime.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `docs/test_performance/test_upgrade_cost_WOT-2026-013g.md`; `docs/test_performance/test_suite_audit_WOT-2026-013e.md`; `docs/test_performance/test_performance_variance.md`; `tests/unit/test_detect_version.py`; `tests/unit/test_no_inline_ticket_regex.py`; `scripts/project_scanner.py`; `agent_system/scripts/project_paths.py`; `scripts/run_pytest_safe.py`.
- **Forbidden Surfaces:** `scripts/project_scanner.py`; `agent_system/scripts/project_paths.py`; `tests/unit/test_detect_version.py`; `tests/unit/test_no_inline_ticket_regex.py`; `scripts/run_pytest_safe.py`; `pytest.ini`; `pyproject.toml`; `uv.lock`; CI/workflows; cualquier politica xdist/default ya cerrada por `011e`, `010m`, `011i`; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] `execution_log.md` registra medicion before/after comparable en el mismo host con comandos exactos que aislen el coste de setup/purge o lo acoten de forma reproducible.
  - [ ] El cambio reduce o acota con evidencia la latencia del setup ligada al purge de sandboxes huerfanos, sin reintroducir residuos bajo `tests/sandbox/test_runtime/`.
  - [ ] Existe al menos una barrera de regresion sobre `tests/conftest.py` que falla sin el fix o protege explicitamente la nueva semantica de purge/higiene.
  - [ ] `python -m pytest tests/unit/test_project_scanner.py tests/unit/test_windows_safe_temp_runtime.py -q -p no:cacheprovider` termina verde.
  - [ ] `python -m pytest tests/unit/test_detect_version.py::TestVersionDetection::test_upgrade_path_suggestion tests/unit/test_project_scanner.py::TestScanProjectRealProject::test_scan_current_project tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex -q -n 8 --dist load` termina verde en 3 corridas consecutivas.
  - [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
  - [ ] No se toca producto, runner, CI ni la politica xdist/default; la higiene sigue viviendo en harness/tests.
- **Integracion cross-ticket:** `013i` sucede a `013d` y `013g`: consume la atribucion de coste ya cerrada por `013g` y solo puede modificar la higiene del sandbox en `tests/conftest.py` y sus barreras. No reabre la familia xdist (`011e`/`010m`/`011i`) ni la cura de producto de `013d`.
- **CONTRACT_GAP behavior:** si la unica reduccion segura exige tocar producto, runner, CI, politica xdist/default, o si cualquier variante mas rapida reintroduce residuos/flake potencial en `tests/sandbox/test_runtime/`, emitir `CG-WOT-2026-013i.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si la mejora solo existe reabriendo `013d` como ticket de producto; parar si la medicion no puede aislar razonablemente el coste del purge en el mismo host; parar si la unica salida verde debilita la limpieza defensiva del sandbox o desplaza la latencia a una deuda operativa peor.
- **Depende de:** WOT-2026-013d (COMPLETED); WOT-2026-013g (COMPLETED).

## T-013J-001 -- Reconciliar duplicidad de FLT entre backlog y contrato frozen

- **ticket_id:** WOT-2026-013j
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013J-001
- **Plan-Link:** PLAN-013J-001
- **Premise:** el drift observado en `013h` y `013i` no nace del scope gate ni del contrato frozen, sino de una duplicidad estructural: las fichas detalladas de `repo_destino/.agent/collaboration/backlog.md` re-declaran `Files Likely Touched`, mientras el FLT canonico ya vive en `ticket_contracts.md` y luego en `work_plan.md`. Hoy `scripts/check_backlog_contract.py` valida la tabla viva y el header de cada ficha, pero NO detecta esa re-declaracion ni su divergencia; el resultado es reconciliacion manual recurrente antes de lanzar Builder.
- **Premise Re-check (read-only):**
  - releer `repo_destino/.agent/collaboration/backlog.md` y confirmar que `WOT-2026-013j` documenta el patron de drift backlog<->contrato;
  - releer `repo_destino/.agent/planning/ticket_contracts.md` y `work_plan.md` historicos recientes (`013h`, `013i`) para verificar que el FLT canonico vive en contrato/work_plan;
  - releer `scripts/check_backlog_contract.py` y `tests/unit/test_check_backlog_contract.py` para confirmar que hoy solo se valida la tabla `Vista rapida` y el header de las fichas, no su cuerpo ni un FLT duplicado;
  - releer `prompts/orchestrator_pipeline.md` y/o la skill de Manager que instruye leer la ficha detallada del backlog, para fijar donde debe quedar explicita la regla de autoridad del FLT;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** source_tickets=`WOT-2026-013h, WOT-2026-013i`; motor_head=848cb8a; destino_head=fae62ca; backlog_gate_current_scope=`Vista rapida + ficha header only`; validate_result=0 errors / 0 warnings; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/check_backlog_contract.py`
  - Builder repo_motor: `tests/unit/test_check_backlog_contract.py`
  - Builder repo_motor: `prompts/orchestrator_pipeline.md`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `repo_destino/.agent/collaboration/backlog.md`; `repo_destino/.agent/planning/ticket_contracts.md`; `repo_destino/.agent/collaboration/work_plan.md`; `scripts/pre_handoff_guard.py`; `.agent/scope_gate.py`; `skills/manager-create-work-plan/SKILL.md`; `prompts/audit_cf_ticket_contract.md`.
- **Forbidden Surfaces:** `.agent/scope_gate.py`; `scripts/pre_handoff_guard.py`; `.agent/agent_controller.py`; `scripts/check_deliverables_exist.py`; `repo_destino/.agent/planning/ticket_contracts.md` salvo packet del Manager; `repo_destino/.agent/collaboration/backlog.md` salvo packet/documentacion del Manager; CI/workflows; `privada/`; `.env`; eventos del bus escritos manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] Existe una sola fuente de verdad operativa para el FLT: la ficha detallada del backlog deja de poder re-declararlo de forma divergente, o el gate correspondiente falla cerrado con diagnostico explicito antes del handoff.
  - [ ] Existe al menos una barrera de regresion en `tests/unit/test_check_backlog_contract.py` que falla sin el fix sobre una ficha con `Files Likely Touched` duplicado/divergente y pasa con el fix.
  - [ ] `prompts/orchestrator_pipeline.md` deja explicita la autoridad del contrato frozen / `work_plan.md` sobre el FLT si el flujo seguira leyendo la ficha detallada del backlog.
  - [ ] `python -m pytest tests/unit/test_check_backlog_contract.py -q -p no:cacheprovider` termina verde.
  - [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
  - [ ] No se debilitan `scope_gate`, `pre_handoff_guard` ni la autoridad del contrato frozen.
- **Integracion cross-ticket:** `013j` sucede a `013i` como fix de proceso/contrato. Puede tocar el gate del backlog y la instruccion de pipeline, pero no debe reabrir tickets de scope gate/handoff (`010n`, `011h`) ni reinterpretar el FLT fuera del contrato frozen.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige redisenar el lifecycle completo de packet, tocar `scope_gate` / `pre_handoff_guard` / `agent_controller.py`, o convertir `backlog.md` en una segunda autoridad del FLT, emitir `CG-WOT-2026-013j.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si el patron real no vive en la validacion/generacion del backlog sino en otra superficie no declarada; parar si la unica salida verde consiste en aceptar dos fuentes de verdad “sincronizadas manualmente”; parar si el fix pide ampliar scope a lifecycle de packet completo en vez de un cambio acotado.
- **Depende de:** -.

## T-013L-001 -- Retencion local opt-in para runtime gitignored

- **ticket_id:** WOT-2026-013l
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013L-001
- **Plan-Link:** PLAN-013L-001
- **Premise:** la deuda de `013l` es estrictamente local y de disco del operador: `repo_destino/.agent/runtime/reviews/`, `repo_destino/.agent/runtime/review_packets/` y `repo_destino/.agent/runtime/memory/observations.jsonl.bak.*` estan gitignored y excluidos de `MANIFEST.distribute` / `MANIFEST.workspace`. Hoy existen productores legitimos para esas rutas, pero no una via auditable y de bajo riesgo para acotar su retencion sin tocar historico versionado ni cablear poda automatica en el lifecycle de cierre.
- **Premise Re-check (read-only):**
  - verificar en `.gitignore`, `MANIFEST.distribute` y `MANIFEST.workspace` que las tres superficies objetivo son local-only / gitignored;
  - inspeccionar `bus/review_bridge.py`, `bus/review_report.py`, `scripts/memory_consolidate.py` y `scripts/migrate_observations.py` para confirmar que producen artefactos en esas rutas, sin politica dedicada de retencion;
  - ejecutar `python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>` y dejar constancia del estado verde pre-arranque.
- **Files Likely Touched:**
  - Builder: `scripts/prune_runtime_retention.py`
  - Builder: `tests/unit/test_prune_runtime_retention.py`
  - Read/inspect only: `.gitignore`, `MANIFEST.distribute`, `MANIFEST.workspace`, `bus/review_bridge.py`, `bus/review_report.py`, `scripts/memory_consolidate.py`, `scripts/migrate_observations.py`, `.agent/agent_controller.py`, `scripts/run_pytest_safe.py`
- **Forbidden Surfaces:** `.agent/agent_controller.py`; `bus/**`; `runtime/**`; `scripts/memory_consolidate.py`; `scripts/migrate_observations.py`; `bus/review_bridge.py`; `bus/review_report.py`; `.gitignore`; `MANIFEST.distribute`; `MANIFEST.workspace`; `repo_destino/.agent/runtime/events/archive/**`; `repo_destino/.agent/audits/system_health/**`; `repo_destino/.agent/collaboration/archive/**`; `repo_destino/.agent/collaboration/_archive/**`; `privada/`; `.env*`; bus editado manualmente.
- **DoD (criterios binarios de cierre):**
  - [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_collects_only_gitignored_runtime_targets -q` pasa y demuestra que el selector solo considera `reviews`, `review_packets` y `observations.jsonl.bak.*`.
  - [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_keep_count_prunes_old_review_and_packet_entries -q` pasa; si se reintroduce spillover hacia otra ruta o se rompe el orden determinista, FALLA.
  - [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSelection::test_observation_backups_follow_the_same_retention_policy -q` pasa y cubre `observations.jsonl.bak.*` sin politica separada opaca.
  - [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_dry_run_reports_without_deleting tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionCLI::test_apply_deletes_only_selected_candidates -q` pasa; `dry-run` no borra nada y `apply` elimina solo los candidatos seleccionados.
  - [ ] `python -m pytest tests/unit/test_prune_runtime_retention.py::TestRuntimeRetentionSafety::test_versioned_history_surfaces_are_never_selected -q` pasa; si se intenta incluir `events/archive`, `collaboration/archive`, `_archive/plan_audit` o `audits/system_health`, FALLA.
  - [ ] `python -m ruff check scripts/prune_runtime_retention.py tests/unit/test_prune_runtime_retention.py` -> `All checks passed`.
  - [ ] `python scripts/run_pytest_safe.py --level all` -> `last-run.json`: `exit_code 0`, `level all`, `tested_commit_sha == HEAD`.
  - [ ] `python .agent/agent_controller.py --validate --json --force --project-root <repo_destino>` -> `0 errors / 0 warnings`.
- **Integracion cross-ticket:** no mezclar con `013k` ni con cambios al lifecycle de closeout; `013l` se limita al camino de menor riesgo (CLI standalone opt-in). Cualquier propuesta de integrar la poda en `session-close`, `mark-ready` o productores de runtime sale de scope y requiere CONTRACT_GAP.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige tocar `session-close`, `mark-ready`, `review_bridge`, `memory_consolidate` o cualquier productor de runtime; si la retencion necesita inspeccionar o borrar superficies versionadas/historico util; o si el selector no puede distinguir de forma determinista entre artefactos locales podables y artefactos utiles que deban preservarse, emitir `CG-WOT-2026-013l.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0. El Builder no decide si integrar la retencion en el closeout ni reabre la frontera entre superficies gitignored y historico versionado.
- **STOP conditions:** parar si el FLT real exige tocar un modulo fuera de `scripts/prune_runtime_retention.py` o `tests/unit/test_prune_runtime_retention.py`; parar si la cobertura depende de una heuristica opaca no auditable; parar si el contrato de conteo no puede expresarse con `--keep-reviews <N>`, `--keep-packets <N>` y `--keep-observation-baks <N>` de forma estable.
- **Depende de:** -

## T-013N-001 -- Estados terminales honestos no-exito

- **ticket_id:** WOT-2026-013n
- **status:** frozen
- **deliverable_type:** code
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013N-001
- **Plan-Link:** PLAN-013N-001
- **Premise:** el motor sigue modelando la terminalidad irreversible casi solo como `COMPLETED` en el runtime compartido. Existe ademas un residuo legacy no-canonico: el string suelto `"CLOSED"` en `scripts/reconcile_ticket.py`, pero `TicketState` NO define `CLOSED` como estado valido. Hay dos casos honestos ya verificados que no son de exito pero si terminales: `WT-2026-239a` quedo rechazado con bug critico y luego superseded por hijos; `WOT-2026-013c` quedo refutado como tests-only y hoy vive como `blocked-final` contractual. Varias superficies (`bus/state_machine.py`, `bus/supervisor.py`, `scripts/reconcile_ticket.py`, `scripts/preflight_reconcile.py`, `scripts/archive_event_bus.py`, `scripts/session_closeout.py`, `scripts/check_destino_publish_ready.py`, `scripts/get_launcher_state.py`) siguen usando listas locales que no reconocen esas salidas honestas, generando ruido cosmetico recurrente o presion a falsear `COMPLETED`.
- **Premise Re-check (read-only):**
  - releer `repo_destino/.agent/runtime/events/events.jsonl` para confirmar que `WT-2026-239a` se quedo en `READY_FOR_REVIEW` con evidencia viva de rechazo/supersession, no por trabajo incompleto;
  - releer `repo_destino/.agent/planning/plan_graph.md` y `CG-WOT-2026-013c.md` para confirmar que `013c` es `blocked-final` honesto, no ticket activo rescatable;
  - verificar en codigo que `TicketState.is_approved_or_terminal()`, `NON_TERMINAL_STATES`, `TERMINAL_STATES` locales y mapeos de launcher/publication no reconocen hoy `SUPERSEDED` ni `BLOCKED_FINAL`, y que el string legacy `CLOSED` vive fuera del enum;
  - verificar que `check_destino_publish_ready.py` y el closeout/archivado usan heuristicas de publicable/terminal distintas y pueden divergir si se anaden estados nuevos sin autoridad comun;
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** source_tickets=`WT-2026-239a, WOT-2026-013c`; motor_head=222da77; destino_head=f063692; live_bus_239a=`READY_FOR_REVIEW + MANAGER_REVIEW evidence`; plan_graph_013c=`BLOCKED-FINAL`; validate_result=0 errors / 0 warnings; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `bus/state_machine.py`
  - Builder repo_motor: `bus/supervisor.py`
  - Builder repo_motor: `bus/builder_locks.py`
  - Builder repo_motor: `scripts/get_launcher_state.py`
  - Builder repo_motor: `scripts/archive_event_bus.py`
  - Builder repo_motor: `scripts/reconcile_ticket.py`
  - Builder repo_motor: `scripts/preflight_reconcile.py`
  - Builder repo_motor: `scripts/session_closeout.py`
  - Builder repo_motor: `scripts/closeout_steps/archival.py`
  - Builder repo_motor: `scripts/check_destino_publish_ready.py`
  - Builder repo_motor: `tests/unit/test_terminal_states.py`
  - Builder repo_motor: `tests/test_launcher_state_from_bus.py`
  - Builder repo_motor: `tests/evals/test_eval_requeue.py`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `repo_destino/.agent/collaboration/_archive/backlog_done.md`; `repo_destino/.agent/runtime/events/events.jsonl`; `repo_destino/.agent/collaboration/MANAGER_REVIEW_WT-2026-239a.md`; `repo_destino/.agent/planning/plan_graph.md`; `repo_destino/.agent/planning/contract_gaps/CG-WOT-2026-013c.md`; `scripts/collect_system_health.py`; `prompts/audit_post_change_system_health.md`; `bus/event_bus.py`; `scripts/manager_review_bridge.py`.
- **Forbidden Surfaces:** `.agent/agent_controller.py`; CI/workflows; `repo_destino/.agent/runtime/events/events.jsonl` editado manualmente; reconciliar tickets reales a `COMPLETED` solo para silenciar vistas; introducir `ABANDONED` sin evidencia nueva de Fase 0; `privada/`; `.env`.
- **DoD (criterios binarios de cierre):
  - [ ] Existe una autoridad compartida de terminalidad irreversible que reconoce `SUPERSEDED` y `BLOCKED_FINAL` sin mapearlos a `COMPLETED`.
  - [ ] El string legacy `CLOSED` deja de actuar como pseudo-estado canonico: se elimina o se colapsa hacia la autoridad canonica sin introducir `TicketState.CLOSED` nuevo.
  - [ ] `TicketState` y sus consumidores de terminalidad (o helper comun equivalente) dejan de depender de listas locales divergentes para estos dos estados.
  - [ ] `bus/supervisor.py` deja de redeclarar localmente la nocion de no-terminalidad y consume la autoridad compartida del runtime en vez de mantener una lista paralela.
  - [ ] `scripts/archive_event_bus.py`, `scripts/reconcile_ticket.py`/`scripts/preflight_reconcile.py`, `scripts/session_closeout.py`/`closeout_steps/archival.py`, `scripts/get_launcher_state.py` y `scripts/check_destino_publish_ready.py` tratan esos estados como terminales honestos cuando aplique.
  - [ ] Existe al menos una barrera de regresion que falla sin el fix y pasa con el fix para `SUPERSEDED`, y otra para `BLOCKED_FINAL`, sin romper el camino `COMPLETED` existente.
  - [ ] `tests/unit/test_terminal_states.py` se crea como deliverable nuevo; `tests/test_launcher_state_from_bus.py` y `tests/evals/test_eval_requeue.py` se extienden sin duplicar suites paralelas.
  - [ ] `python -m pytest tests/unit/test_terminal_states.py tests/test_launcher_state_from_bus.py tests/evals/test_eval_requeue.py -q -p no:cacheprovider` termina verde.
  - [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
  - [ ] El fix no reabre `239a` ni `013c` como trabajo activo ni degrada el contrato de cierre exitoso (`READY_TO_CLOSE -> COMPLETED -> SUPERVISOR_CLOSED`).
- **Integracion cross-ticket:** serializar con cualquier ticket que toque bus, supervisor, lifecycle de cierre, closeout, launcher state o gates de publicacion. El objetivo es limpiar la semantica de terminalidad, no reescribir review/handoff ni la politica de `completed`.
- **CONTRACT_GAP behavior:** si la unica solucion segura exige redisenar el event schema completo, introducir un tercer estado no evidenciado (`ABANDONED`) para no dejar incoherencias, o tocar `.agent/agent_controller.py` / handoff / CI, emitir `CG-WOT-2026-013n.md`, bloquear y devolver a Contract Formation.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si `WT-2026-239a` o `WOT-2026-013c` no sostienen la premisa tras releer bus/contrato reales; parar si la terminalidad no puede centralizarse sin una migracion amplia de consumers no declarados; parar si la unica forma de demostrar verde exige mutar tickets historicos reales durante la implementacion.
- **Depende de:** -.

## T-013O-001 -- Saneamiento estricto de observations.jsonl portable

- **ticket_id:** WOT-2026-013o
- **status:** frozen
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Objective-Link:** OBJ-013O-001
- **Plan-Link:** PLAN-013O-001
- **Premise:** `repo_destino/.agent/runtime/memory/observations.jsonl` falla `python scripts/validate_observations.py --strict --file <obs>` con 17 errores verificados. El diagnostico correcto tiene dos clases distintas: 14 entradas tienen corrupcion de datos (`applies_to` contiene etiquetas que son claramente `domain`, como `review-quality`, `planning`, `supervisor`, `preflight`), y 3 entradas usan valores de `domain` fuera del enum canonico (`collaboration`, `test-performance`). Ya existe un seam de migracion (`scripts/migrate_observations.py` + `tests/test_migration_bootstrap.py`), asi que el trabajo NO es inventar migracion desde cero sino reconciliar datos vivos, validador estricto y decision de contrato sobre dominios antes de seguir promoviendo memoria portable.
- **Premise Re-check (read-only):**
  - ejecutar `python scripts/validate_observations.py --strict --file <repo_destino>/.agent/runtime/memory/observations.jsonl` y conservar el conteo/lineas exactas de error;
  - releer `scripts/migrate_observations.py`, `scripts/validate_observations.py`, `skills/_shared/ap-schema.md`, `bus/memory_loader.py` y `scripts/memory_consolidate.py`;
  - releer `tests/test_migration_bootstrap.py` y `tests/unit/test_validate_observations.py` para fijar la barrera existente;
  - separar con evidencia las 14 lineas de corrupcion de datos de las 3 lineas de posible decision de contrato (`collaboration`, `test-performance`);
  - ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes del arranque y dejar constancia del estado.
- **Context Baseline Evidence:** motor_head=f48191f; destino_head=85b76cb; validate_result=0 errors / 0 warnings; strict_validate_errors=17; split=`14 applies_to-corrupt + 3 domain-contract`; existing_migrator=`scripts/migrate_observations.py`; generated_at=2026-06-22.
- **Files Likely Touched:**
  - Builder repo_motor: `scripts/migrate_observations.py`
  - Builder repo_motor: `scripts/validate_observations.py`
  - Builder repo_motor: `skills/_shared/ap-schema.md`
  - Builder repo_motor: `tests/test_migration_bootstrap.py`
  - Builder repo_motor: `tests/unit/test_validate_observations.py`
  - Builder repo_destino: `.agent/runtime/memory/observations.jsonl`
  - Builder repo_destino: `.agent/collaboration/execution_log.md`
- **Read/inspect only:** `bus/memory_loader.py`; `scripts/memory_consolidate.py`; `prompts/memory_upload.md`; `.agent/runtime/memory/MEMORY.md`; `.agent/runtime/memory/memory_profile.md`; `.agent/audits/system_health/general_audit_20260622_1449/07_adversarial_review.md`.
- **Forbidden Surfaces:** `repo_motor/.agent/runtime/memory/observations.jsonl`; `repo_destino/.agent/runtime/memory/observations.jsonl` inserciones semanticas nuevas antes del verde estricto; `repo_destino/.agent/runtime/memory/MEMORY.md`; `repo_destino/.agent/runtime/memory/memory_profile.md`; `repo_destino/.agent/runtime/memory/memory_rules.md`; `repo_motor/bus/memory_loader.py` salvo `CONTRACT_GAP`; `repo_motor/scripts/session_close_observations.py`; CI/workflows; `privada/`; `.env`; editar a mano eventos del bus.
- **DoD (criterios binarios de cierre):**
  - [ ] `python scripts/validate_observations.py --strict --file <repo_destino>/.agent/runtime/memory/observations.jsonl` termina verde.
  - [ ] Las 14 entradas con `applies_to` corrupto quedan reparadas de forma determinista, con evidencia pre/post en `execution_log.md` o reporte adjunto.
  - [ ] Los 3 errores de `domain` quedan resueltos por decision explicita de contrato: o se mapean a dominios canonicos existentes con justificacion verificable, o se amplia el enum canonico en schema+validador+tests. No se permite fallback silencioso.
  - [ ] `scripts/migrate_observations.py` mantiene backup/rollback e idempotencia; existe al menos una barrera que falla sin el fix y pasa con el fix sobre el patron `applies_to <- domain`.
  - [ ] `python -m pytest tests/test_migration_bootstrap.py tests/unit/test_validate_observations.py -q -p no:cacheprovider` termina verde.
  - [ ] `python scripts/run_pytest_safe.py --level all` termina verde sobre el commit entregado.
  - [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` termina con 0 errors / 0 warnings.
  - [ ] El cierre deja explicito que `013o` NO inserta nueva memoria portable durante este ticket; cualquier promocion posterior (incluida la observacion diferida de `013n`) queda fuera de scope hasta partir de una base `--strict` verde.
- **Integracion cross-ticket:** serializar con cualquier ticket que toque `validate_observations.py`, `migrate_observations.py`, `ap-schema.md`, `memory_consolidate.py` o memorias portables. El objetivo es reparar la base y el contrato, no abrir una reforma general de taxonomia o tocar memoria del motor.
- **CONTRACT_GAP behavior:** si alguna de las 17 lineas requiere reinterpretacion semantica no verificable, si `collaboration`/`test-performance` fuerzan una reforma amplia de dominios/consumidores fuera de scope, o si la unica salida segura exige tocar `repo_motor/.agent/runtime/memory/observations.jsonl` o `bus/memory_loader.py`, emitir `CG-WOT-2026-013o.md` y bloquear.
- **Builder clarification budget:** 0.
- **STOP conditions:** parar si aparecen mas entradas invalidas de las 17 reportadas y cambian materialmente la premisa; parar si el arreglo de datos deja de ser determinista linea-a-linea; parar si la decision de dominio no puede cerrarse sin redisenar la memoria portable completa.
- **Depende de:** WOT-2026-013n (COMPLETED).

