# STRATEGY_WOT-2026-013h -- Cierre sin limbo del archivado canonico

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- `011a` endurecio el closeout y `011h` endurecio `--mark-ready`, pero ninguna de esas barreras elimino la deuda estructural del archivado.
- `013e`, `013f` y `013g` necesitaron reconcile manual del rename archivado antes del siguiente ciclo.
- El detector canonico del limbo ya existe en `scripts/delivery_hygiene_check.py`; no hay que inventar un segundo guard.
- El ticket es `code` y su frontera real es archivado/cierre, no xdist ni producto.

## Plan tecnico

1. Releer el flujo real:
   - `scripts/archive_collaboration_artifacts.py`
   - `scripts/closeout_steps/archival.py`
   - `scripts/session_closeout.py`
   - tests actuales del archivado y closeout
2. Reproducir el patron con repo git real en `tmp_path`, no con mocks de subprocess:
   - move de `STRATEGY_` / `AUDIT_`
   - delete+untracked visible para el guard
3. Elegir el cambio minimo que elimine la herencia del limbo:
   - o el closeout queda limpio en el mismo ciclo,
   - o falla cerrado antes de dejar residuos para el ticket siguiente
4. Mantener una sola fuente de verdad:
   - `archive_rename_uncommitted` sigue siendo la razon estable
   - `reconcile_ticket.py` sigue siendo recuperacion, no cierre normal
5. Cerrar con barreras reales:
   - tests focales de archiver/closeout/agent_controller/pre_handoff
   - `run_pytest_safe --level all`
   - `validate --json --project-root <repo_destino>`

## Riesgos y antidotos

- **Auto-commit encubierto:** prohibido; cualquier fix que dependa de eso es `CONTRACT_GAP`.
- **Arreglar solo `mark-ready` otra vez:** verificar el closeout real, no solo el handoff.
- **Pass-open silencioso:** preservar el fail-closed y la trazabilidad del historico.
- **Mock drift:** usar repos git reales y assertions sobre porcelain/guard real.

## No hacer

- No tocar runner, xdist, CI ni producto.
- No crear una segunda razon o un segundo detector para el mismo limbo.
- No declarar resuelto el problema si el siguiente ciclo todavia puede heredar el rename.
