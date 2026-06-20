# AUDIT_WOT-2026-011g

## Preguntas binarias de auditoria
- [ ] Existe una formulacion explicita de `loop rapido` vs `cierre canonico` en las superficies tocadas.
- [ ] `prompts/orchestrator_launch_builder.md`, `prompts/manager_review.md`, `prompts/orchestrator_pipeline.md` y `QUICKSTART.md` usan una politica coherente entre si.
- [ ] Ningun texto tocado permite presentar pytest focal, wall-clock en background o tests aislados verdes como sustituto de suite canonica / handoff / cierre.
- [ ] El diff toca solo archivos documentales declarados y `execution_log.md`.
- [ ] `python scripts/check_encoding_guard.py <docs_tocados>` queda verde.
- [ ] `python .agent/agent_controller.py --validate --json --project-root <repo_destino>` queda verde.

## Evidencia minima esperada
- Diff de los prompts/docs tocados.
- Salida literal de `check_encoding_guard.py`.
- Salida literal de `validate --json`.
- `execution_log.md` con comandos exactos y resumen de la politica fijada.
- Si aplica, `CG-WOT-2026-011g.md` con causa exacta del bloqueo.
