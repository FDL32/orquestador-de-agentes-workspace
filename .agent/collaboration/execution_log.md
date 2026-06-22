# Execution Log -- WOT-2026-013j

**Estado:** IN_PROGRESS

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
