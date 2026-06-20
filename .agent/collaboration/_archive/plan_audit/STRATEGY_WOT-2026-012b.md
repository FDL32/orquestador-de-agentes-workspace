# STRATEGY_WOT-2026-012b.md

## Objetivo tecnico
Materializar una barrera fail-closed en `repo_motor` que lea la cola viva post-`012a` desde `repo_destino`, valide su contrato parseable y detenga el ciclo cuando detecte drift estructural o semantico.

## Secuencia propuesta
1. Releer `.agent/collaboration/backlog.md` ya migrado por `012a` y fijar el schema consumible minimo.
2. Implementar `scripts/check_backlog_contract.py` con resolucion estricta via `--project-root` o `AGENT_PROJECT_ROOT`.
3. Codificar el vocabulario cerrado de estados y las reglas semanticas de `Reactivation`.
4. Construir tests de barrera que fallen sin root explicito, sin ficha obligatoria y con valores invalidos de `Status` o `Reactivation`.
5. Integrar el gate en `scripts/run_gates_dispatch.py` sin tocar el archivador ni el closeout.
6. Cerrar con `ruff`, tests focales, suite aplicable y `validate --json`.

## Restriccion deliberada
`012b` no vuelve a modelar el backlog ni reabre `012a`: consume el contrato que `012a` ya fijo y lo convierte en gate. Si para validar necesita HTML comments o prose libre, el problema vuelve a `012a` como CONTRACT_GAP.
