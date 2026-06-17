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
- **STOP conditions:** parar si el ticket exige tocar codigo del motor para "facilitar" la medicion; parar si la unica forma de obtener datos requiere activar cache/sharding/xdist; parar si el reporte acabaría en `repo_destino` en vez de `repo_motor`; parar si `validate` deja warnings nuevos sin resolver.
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
