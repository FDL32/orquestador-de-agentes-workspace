# STRATEGY_WOT-2026-011g

## Objetivo tecnico
Dejar una politica explicita y consistente de `loop rapido` vs `cierre canonico` en la documentacion operativa del motor, sin tocar tooling ni gates.

## Fase 0 - Baseline documental
1. Releer `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md`, `prompts/audit_agent_output.md` y `QUICKSTART.md`.
2. Confirmar donde ya existen fragmentos de la politica y donde falta una formulacion corta y sincronizada.
3. Confirmar que `011g` puede resolverse solo con texto; si aparece un hueco que exige tooling, detener con `CONTRACT_GAP`.

## Fase 1 - Politica canonica
1. Introducir una formulacion corta y estable:
   - `loop rapido`: diagnostico local, reruns focales, evidencia provisional, nunca handoff ni cierre.
   - `cierre canonico`: suite canonia en HEAD, `validate 0/0`, `mark-ready` con eventos reales, y `manager-approve` cuando aplique.
2. Usar una sola terminologia en todas las superficies tocadas.
3. Mantener el cambio minimo: alinear lenguaje, no reescribir el flujo entero.

## Fase 2 - Alineacion de consumidores
1. `orchestrator_launch_builder.md`: Builder no puede reportar evidencia de loop rapido como suite canonica o handoff.
2. `manager_review.md`: Manager debe rechazar cierres que intenten sustituir evidencia canonica por loop rapido.
3. `orchestrator_pipeline.md`: la orquestacion distingue claramente diagnostico local de cierre publicable.
4. `QUICKSTART.md`: deja una referencia publica y corta para humanos.

## Fase 3 - Gates documentales
1. Ejecutar `python scripts/check_encoding_guard.py` sobre los docs/prompts tocados.
2. Ejecutar `python .agent/agent_controller.py --validate --json --project-root <repo_destino>`.
3. Registrar en `execution_log.md` comandos exactos y resultados.

## Riesgos y contencion
- Riesgo: que una contradiccion documental destape deuda real de tooling.
  - Contencion: parar con `CG-WOT-2026-011g.md`; no ampliar a codigo.
- Riesgo: sobreeditar prompts y mezclar mejoras adyacentes.
  - Contencion: tocar solo las superficies declaradas y solo para fijar esta politica.
- Riesgo: dejar terminos distintos entre prompts.
  - Contencion: verificar literalmente las cuatro superficies antes del handoff.
