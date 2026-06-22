# Execution Log -- WOT-2026-013j

**Estado:** COMPLETED

## MANAGER - WOT-2026-013j - Bootstrap operativo

Ticket activado para eliminar la duplicidad estructural de `Files Likely Touched` entre la ficha detallada de `backlog.md` y el contrato frozen, manteniendo una sola fuente de verdad operativa.

Packet activo en repo_destino:
- `OBJ-013J-001` en `repo_charter.md`
- `PLAN-013J-001` en `plan_graph.md`
- `T-013J-001` congelado en `ticket_contracts.md`
- `work_plan.md`, `STRATEGY_WOT-2026-013j.md` y `AUDIT_WOT-2026-013j.md` activos para Builder

Premisa operativa del Builder:
- releer `backlog.md` real del destino y confirmar el patron de drift
- releer `scripts/check_backlog_contract.py` y su test para ubicar la barrera ciega actual
- mantener el fix acotado a gate/pipeline o bloquear por `CG-WOT-2026-013j.md`
- preservar la autoridad del contrato frozen / `work_plan.md` sobre el FLT

Baseline verificado antes del bootstrap:
- repo_motor HEAD = `848cb8a`
- repo_destino HEAD = `fae62ca`
- `validate --json --project-root <repo_destino>` = `0 errors / 0 warnings`
- evidencia disparadora: drift recurrente observado en packets `013h` y `013i`; `check_backlog_contract.py` valida hoy `Vista rapida + ficha header only`

## BUILDER - WOT-2026-013j - Fase 0 (diagnostico + repro)

Preflight: validate 0/0; STATE/TURN/work_plan=013j; bus seq 1349 IN_PROGRESS para 013j (013i COMPLETED seq 1347). Ambos repos sync. No anclado a 013i.

Seam confirmado [V]: `scripts/check_backlog_contract.py::validate_backlog` valida (a) la tabla `Vista rapida` y (b) que cada `### WOT-...` ficha header este bien formado. NO inspecciona el CUERPO de la ficha detallada, asi que un bullet `- **Files Likely Touched:**` con rutas pasa inadvertido.

Reproduccion del drift [V]:
- La unica ficha viva con FLT declarativo es 013j (linea 45 del backlog: `- **Files Likely Touched (a confirmar en Fase 0):**`). Muchas fichas historicas en `_archive/backlog_done.md` tambien lo llevan (170, 286, 336...).
- `cbc.validate_backlog(<backlog real del destino>)` => `[]` (PASA) pese a que la ficha 013j re-declara FLT. Confirmado: el gate es ciego a este patron.
- El contrato frozen (`ticket_contracts.md`) tiene 48 menciones de FLT: ahi vive la autoridad.

Decision tecnica (diseno A, dentro de FLT):
- El gate `check_backlog_contract.py` lee SOLO el backlog del destino (no tiene acceso al contrato frozen para comparar valores), asi que el diseno B "validar que el FLT de la ficha coincide con el del contrato" exigiria cruzar archivos y resolver que contrato aplica -> fuera de scope acotado.
- Diseno A elegido (fiel a la Decision Arquitectonica del work_plan: "el backlog solo puede resumir o referenciar, no re-declarar"): el gate FALLA-CERRADO si una ficha detallada contiene un bullet declarativo `- **Files Likely Touched...:**`. El FLT es autoridad EXCLUSIVA del contrato frozen / work_plan.
- Discriminador robusto: una linea que tras whitespace empieza por `- **Files Likely Touched` (clave de bullet declarativo). Una MENCION en prosa (p.ej. el bullet `- **Problema:** ... re-declaran el \`Files Likely Touched\` ...`) NO matchea, porque la clave del bullet es "Problema", no "Files Likely Touched". Esto distingue limpio la linea 45 (declarativa, prohibida) de la 43 (prosa, permitida).
- Esto NO toca scope_gate, pre_handoff_guard ni controller; mantiene una sola fuente de verdad; el backlog deja de poder re-declarar FLT divergente.

Consecuencia operativa: la ficha 013j actual (que YO escribi con FLT declarativo) tendra que perder ese bullet -- es read-only del backlog en este ticket, pero el gate fallaria sobre el propio destino. Lo resuelvo reemplazando el bullet declarativo de 013j por una referencia al contrato frozen (resumen, no re-declaracion), que es exactamente la norma que el ticket impone. Es edicion del backlog del destino como reconciliacion del propio drift, no como nueva autoridad.

Procedo a Fase 1 (gate + regla de pipeline) + Fase 2 (barrera de regresion).

## BUILDER - WOT-2026-013j - Fase 1 (gate + pipeline) + Fase 2 (barreras) + gates

Fix Fase 1:
- `scripts/check_backlog_contract.py`: nueva constante `_FLT_DECLARATION_RE` (matchea un bullet `- **Files Likely Touched...:**`, case-insensitive) + helper `_check_ficha_bodies(content)` (extraido para mantener complejidad <=10, C901) que recorre el cuerpo de las fichas, rastrea el ticket dueno y FALLA-CERRADO con diagnostico + remediacion si una ficha re-declara FLT. `validate_backlog` ahora delega en ese helper.
- `prompts/orchestrator_pipeline.md`: bloque de autoridad del FLT (WOT-2026-013j) en la seccion 2.a Contract Formation gate: el FLT canonico vive en el contrato frozen y work_plan.md; la ficha del backlog resume/referencia, no re-declara; al materializar work_plan se toma el FLT del contrato, no del backlog.

Fase 2 (tests/unit/test_check_backlog_contract.py):
- `test_ficha_redeclaring_flt_blocks`: ficha con bullet FLT declarativo -> el gate falla nombrando el ticket. FAIL-sin/PASS-con.
- `test_ficha_prose_mention_of_flt_is_allowed`: mencion de "Files Likely Touched" en prosa dentro de otro bullet -> NO bloquea (discriminador declaracion-vs-prosa).

Evidencia FAIL-sin/PASS-con [V]:
- REPRO inicial: `cbc.validate_backlog(<backlog real del destino>)` => `[]` (PASA) pese a la ficha 013j con FLT declarativo (linea 45). Gate ciego confirmado.
- FAIL-sin: neutralizando `_FLT_DECLARATION_RE` a un patron que nunca matchea, la ficha con FLT pasa (FLT errors = []). Confirmado via one-off.
- PASS-con: con el fix, el gate sobre el destino real detecta la ficha 013j con diagnostico exacto; las 15 entradas del test pasan.

Reconciliacion del propio destino (justificacion CEM): `backlog.md` es Read/inspect only en el FLT, pero el gate nuevo fallaba sobre el destino real porque la ficha 013j (que YO escribi al cerrar 013i) llevaba un bullet FLT declarativo. Apliqué la propia norma del ticket: reemplacé ese bullet por una "Superficie (resumen, no FLT autoritativo)" que referencia el contrato frozen, sin re-declarar. No es nueva autoridad ni scope-creep: es reconciliar el drift que el ticket existe para prohibir. Tras el cambio, `check_backlog_contract --project-root <destino>` => OK.

Gates (comandos exactos + resultados):
- Focal: `python -m pytest tests/unit/test_check_backlog_contract.py -q -p no:cacheprovider` => `15 passed`.
- Ruff check: `uv run ruff check scripts/check_backlog_contract.py tests/unit/test_check_backlog_contract.py` => `All checks passed!` (tras extraer `_check_ficha_bodies` por C901).
- Ruff format: `uv run ruff format --check <mismos>` => `2 files already formatted`.
- Encoding guard: `python scripts/check_encoding_guard.py prompts/orchestrator_pipeline.md` => exit 0.
- Suite canonica: `python scripts/run_pytest_safe.py --level all` => `3098 passed, 20 skipped in 118.79s`, exit 0. last-run.json: status=finished, level=all, args_mode=default_discovery, tested_commit_sha=c6e7eba == HEAD.
- backlog-contract gate sobre destino real: OK (ficha 013j reconciliada, sin FLT declarativo).
- State-leak: silencioso (solo artefactos del packet 013j untracked, del bootstrap).
- Validate: 0 errors / 0 warnings.

Commit del entregable (repo_motor): HEAD `c6e7eba`. Diff = 3 files (check_backlog_contract.py + su test + orchestrator_pipeline.md), todos en FLT. 81 insertions, 4 deletions. Pre-commit hooks verdes.

Desviaciones CEM: una, justificada arriba (edicion de backlog.md del destino para reconciliar la ficha 013j al estandar que el ticket impone). No procede CG: el fix vive en gate/pipeline, no toca scope_gate/pre_handoff_guard/controller. Listo para --pre-handoff + --mark-ready.


Scope override: observations.jsonl pertenece al commit 848cb8a (memoria de deuda obs-backlog-contract-flt-drift registrada al cerrar 013i, que origino este ticket 013j); no es entrega productiva de 013j. La entrega de 013j vive en commit c6e7eba: check_backlog_contract.py + test + orchestrator_pipeline.md, todos en FLT.. Affected files: .agent/runtime/memory/observations.jsonl

Manager approved canonical closeout for WOT-2026-013j

## ORQUESTADOR - Cierre de sesion 2026-06-22 + auditoria de superficies

013j COMPLETED verificado en bus (seq 1358 STATE_CHANGED->COMPLETED, 1359 SUPERVISOR_CLOSED). Arco completo de la sesion: familia 013e-013j cerrada (audit de suite -> poda -> coste -> limbo archivado -> purge -> drift FLT). Salud audit versionada en .agent/audits/system_health/general_audit_20260622_1013/.

### Auditoria de superficies que crecen (peticion del usuario), VERIFICADA POR BYTES + GIT

Pregunta: que crece sin techo y debe limpiarse por ticket vs historico intencional.

Temporales de PRUEBA de tickets (efimeros) -- SANOS, sin crecimiento sin techo:
- tests/sandbox/ vacio; .agent/runtime/tmp/ acotado; .agent/runtime/pytest-safe/ = last-run.{json,log}. (013i dejo el purge funcionando.)

Superficies que SI crecen, separadas por impacto real (gitignored vs versionado):
- VERSIONADO (contamina repo + clones): collaboration/archive/notifications_*.md (~9.5MB, 12 trackeados, anadidos por agent_controller al rotar). => DEUDA REAL. Ticket WOT-2026-013k.
- GITIGNORED (solo disco local, NO contamina repo): runtime/reviews (~5.1MB), runtime/review_packets (~2MB), runtime/memory/observations.jsonl.bak.* (12). VERIFICADO: git check-ignore confirma gitignored; git ls-files .bak => 0 trackeados. => retencion menor. Ticket WOT-2026-013l.
- HISTORICO UTIL versionado (NO podar): events/archive, audits/system_health, _archive/plan_audit. Crecimiento lento e intencional.

### Hallazgo del cierre canonico: bug en session_closeout (WOT-2026-013m)

--session-close --dry-run revelo Overall: FAIL por paso 16 versioned_filenames (test_suite_audit_WOT-2026-013e.md, test_upgrade_cost_WOT-2026-013g.md): docs durables con ticket-id en el nombre, contra la convencion de 7f777ce.
- VERIFICADO EN CODIGO: ese paso esta marcado `blocking=False` (closeout_steps/support.py:327), pero `session_closeout.py::overall_status` (l.148-152) retorna FAIL ante CUALQUIER FAIL sin consultar `s.blocking`, contradiciendo su docstring. Efecto: un paso no-bloqueante tumba --session-close con exit 1.
- Decision (con el usuario): el defecto es del GATE, no de los nombres. NO se renombran los entregables de 013e/013g (tickets cerrados/aprobados); se abre WOT-2026-013m para que overall_status respete blocking=False.

### Follow-ups registrados (3 tickets en backlog + 3 memorias portable-motor)
- WOT-2026-013m (Alta): overall_status del closeout debe respetar blocking=False.
- WOT-2026-013k (Media): retencion de notifications_*.md versionado.
- WOT-2026-013l (Baja): retencion de runtime gitignored (reviews/packets/.bak).
- Memorias: obs-closeout-overall-status-ignores-blocking, obs-notifications-archive-grows-versioned, obs-runtime-gitignored-no-retention (validadas por bus/memory_loader).

### Estado del cierre de sesion
- 013j cerrado canonicamente (Manager-approved, bus COMPLETED).
- --session-close completo (pipeline de archivado) queda BLOQUEADO por WOT-2026-013m hasta que overall_status respete blocking=False: el versioned_filenames FAIL no-bloqueante fuerza exit 1. Reproducido en dry-run.
- Cierre de sesion por via commit-limpio: artefactos del cierre + auditoria + backlog + memorias commiteados; ambos repos limpios; validate 0/0. El archivado canonico de fin de sesion se completara tras cerrar 013m.

## ORQUESTADOR - Cierre final 2026-06-22 (post-013m): motor limpio para otros proyectos

Objetivo del usuario: dejar el motor limpio para usarlo en otros proyectos. Analisis verificado:
- VERIFICADO EN CODIGO: install_agent_system.py:46 `LOCAL_DIRS = {collaboration, runtime, audits}` => ese estado NO se copia a destinos nuevos; cada proyecto arranca con su .agent/ limpio + el seed neutro del motor.
- VERIFICADO POR BYTES: el seed del motor (collaboration/ que SI se distribuye) esta neutro (`# Work Plan - Seed`, READY_TO_START, sin contaminacion del dogfooding).
- VERIFICADO POR BYTES: notifications_* (013k) y runtime gitignored (013l) estan EXCLUIDOS de MANIFEST.distribute (l.112) y MANIFEST.workspace (l.92) => NO viajan. Su limpieza NO afecta la instalabilidad del motor; es higiene del dogfooding local.
- Conclusion: el motor portable YA esta limpio para otros proyectos (codigo git limpio, seed neutro, catalogo INDEX reconciliado, sin stubs legacy operativos).

013m (overall_status respeta blocking=False) IMPLEMENTADO Y VERIFICADO:
- commit motor 3bbfea2; 62 tests de session_closeout verdes; tests nuevos test_non_blocking_failure_gives_warn (regresion FAIL-sin/PASS-con) + test_blocking_fail_wins_over_non_blocking_fail.
- Efecto verificado en vivo: --session-close --dry-run paso de Overall FAIL a Overall WARN (exit 0). El cierre canonico queda DESBLOQUEADO.
- Cierre de 013m: registrado en _archive/backlog_done como `delivered-no-bus` (implementado+verificado fuera del lifecycle de bus; no se bootstrapeo como ticket activo; evidencia = commit+tests+efecto, no eventos de bus). Decision explicita del usuario para no fabricar eventos de bus sobre una implementacion ya cerrada.

Higiene del backlog: 013j (cerrado canonico) y 013m (delivered-no-bus) movidos a _archive/backlog_done; sacados de la cola viva. 013k/013l => `deferred` con reactivation condition:higiene-dogfooding-local-no-portable. Cola viva final: 002c (completed-partial), 013k/013l (deferred), 256a (blocked). Ningun ticket accionable bloqueante pendiente.

013k/013l diferidos (no implementados): decision del usuario, por ser higiene del repo dogfooding local que no viaja a otros proyectos (evidencia MANIFEST arriba). Documentados en backlog con esa justificacion.