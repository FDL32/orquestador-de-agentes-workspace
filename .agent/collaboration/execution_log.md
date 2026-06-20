# execution_log.md -- WOT-2026-011g
## Metadata
- **Ticket:** WOT-2026-011g
- **Estado:** IN_PROGRESS
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
## Manager Bootstrap
- Ticket siguiente seleccionado: WOT-2026-011g.
- Motivo: `011h` no se prepara como siguiente Builder porque la barrera de archive rename en handoff ya existe en `scripts/pre_handoff_guard.py` y esta cubierta por `tests/test_pre_handoff_guard.py`; `011g` sigue siendo deuda documental real y acotada.
- Contrato congelado: `T-011G-001`.
- Frontera fijada antes de Builder: `011g` solo alinea prompts/docs sobre `loop rapido` vs `cierre canonico`; tocar tooling, gates, tests o CI dispara `CONTRACT_GAP`.
- `013a` ya se retiro de la cola viva y pasa a historico documental antes del nuevo arranque.
## Premise Re-check requerido al Builder
- Releer `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md`, `prompts/audit_agent_output.md` y `QUICKSTART.md`.
- Confirmar que la politica actual aparece fragmentada y que el ticket puede resolverse solo con texto.
- Releer observaciones `obs-20260619-background-wallclock-not-canonical` y `obs-20260620-last-run-canonical-lives-in-motor` como evidencia de la confusion reciente.
- Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` antes de empezar la implementacion.
## Restriccion cross-ticket
- `011g` no reabre `011h`, `011i`, `010m` ni `010x`.
- Si la documentacion veraz exige tocar tooling, el ticket para con `CG-WOT-2026-011g.md`.

## BUILDER - WOT-2026-011g - Politica loop rapido vs cierre canonico (documental)

### Fase 0 - Baseline
- Ninguno de los 4 docs (launch_builder, manager_review, pipeline, QUICKSTART) tenia una formulacion NOMBRADA de "loop rapido vs cierre canonico". Las reglas de suite/handoff estaban dispersas (launch_builder ya tenia las mas fuertes tras el protocolo reciente). Confirmado: resoluble solo con texto, sin tocar tooling (sin CONTRACT_GAP).

### Fase 1 - Politica canonica (fuente unica)
- prompts/orchestrator_launch_builder.md: nueva seccion "## Loop rapido vs cierre canonico (politica WOT-2026-011g)" tras Quality gates. Define: loop rapido = diagnostico local (focal/-k/--select-from-diff/--level unit/background/aislados) que NO autoriza handoff ni cierre; cierre canonico = suite --level all en HEAD (last-run.json tested_sha==HEAD, exit 0) + validate 0/0 + mark-ready con BUILDER_EXIT+STATE_CHANGED + manager-approve cuando aplique. Es la fuente que los demas referencian.

### Fase 2 - Alineacion de consumidores (terminologia unica)
- manager_review.md: bullet en Paso 2 "Comprueba:" -> el Manager rechaza con CHANGES cualquier handoff que presente loop rapido como cierre canonico; referencia a la fuente.
- orchestrator_pipeline.md: bullet en 0.c "Reglas derivadas" -> la orquestacion distingue diagnostico local de publicable; loop rapido nunca autoriza handoff.
- QUICKSTART.md: nota publica corta tras "Quality gates diarios"; referencia a la fuente.
- Verificado: los 4 docs usan "loop rapido" + "cierre canonico" coherentemente.

### Gates (documental)
- Encoding: `python scripts/check_encoding_guard.py prompts/orchestrator_launch_builder.md prompts/manager_review.md prompts/orchestrator_pipeline.md QUICKSTART.md` -> exit 0.
- Diff: 100% documental (4 .md), 0 scripts/tests/controller/CI tocados.
- Validate: registrado abajo.
- Artefactos declarados existen en disco; deliverable_type documentation respetado (sin pytest/ruff como gate principal).
