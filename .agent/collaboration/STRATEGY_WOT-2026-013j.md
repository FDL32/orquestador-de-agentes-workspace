# STRATEGY_WOT-2026-013j -- Una sola fuente de verdad para FLT

> Estrategia tecnica del ticket. El scope, FLT y criterios binarios viven en
> `work_plan.md`; aqui se detalla el COMO sin mover el contrato.

## Hechos verificados (no asumir)

- El drift no nace del scope gate ni del contrato frozen: nace de que la ficha detallada del backlog re-declara FLT.
- `check_backlog_contract.py` hoy no inspecciona el cuerpo de la ficha mas alla del header.
- El handoff y el scope gate ya tienen su propia autoridad sobre el FLT; no deben tocarse en esta ronda.
- El ticket correcto es gate/proceso del backlog, no lifecycle completo de packet.

## Plan tecnico

1. Releer el backlog contract actual:
   - `scripts/check_backlog_contract.py`
   - `tests/unit/test_check_backlog_contract.py`
   - `backlog.md` real del destino
2. Reproducir el patron de drift:
   - ficha bien formada con `Files Likely Touched` duplicado o divergente
   - gate actual la deja pasar
3. Elegir el cambio minimo:
   - o prohibir la re-declaracion de FLT en la ficha detallada,
   - o detectarla fail-closed con diagnostico explicito
4. Dejar clara la autoridad del proceso:
   - `ticket_contracts.md` / `work_plan.md` mandan
   - `backlog.md` no puede competir como segunda fuente de verdad
5. Cerrar con barreras reales:
   - tests focales del gate
   - `run_pytest_safe --level all`
   - `validate --json --project-root <repo_destino>`

## Riesgos y antidotos

- **Arreglar solo el sintoma documental:** exigir una barrera ejecutable, no solo prose.
- **Debilitar el scope gate por accidente:** mantener `scope_gate.py` y `pre_handoff_guard.py` en read-only.
- **Mover la autoridad al backlog:** rechazar cualquier solucion que mantenga dos fuentes de verdad.
- **Sobrescoped redesign:** si aparece lifecycle de packet mas grande, emitir `CONTRACT_GAP`.

## No hacer

- No tocar `scope_gate`, `pre_handoff_guard`, `agent_controller` ni `check_deliverables_exist`.
- No “sincronizar manualmente” dos copias como solucion estable.
- No declarar resuelto el problema con solo una nota humana si el gate sigue ciego.
