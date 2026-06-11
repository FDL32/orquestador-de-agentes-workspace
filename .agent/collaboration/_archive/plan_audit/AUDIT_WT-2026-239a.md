# AUDIT_WT-2026-239a

## Riesgos Bloqueantes

### CRITICO - bypass demasiado amplio
Bloquear si el fix trata `mixed` o tickets con cambios productivos como si fueran
documentales y les salta commit/checkpoint del `repo_motor`.

### CRITICO - closeout documental sin prueba de ciclo
Bloquear si solo se anade una condicion en el controller pero no queda al menos
una prueba que demuestre Builder -> Manager -> Supervisor para el branch docs.

### ALTO - scope fuera del seam minimo
Bloquear si el ticket toca `review_bridge.py`, `supervisor.py` o `event_bus.py`
sin evidencia directa de que `pre-handoff` no basta.

### ALTO - regression en tickets code
Bloquear si el bypass degrada el comportamiento existente de tickets `code`:
deben seguir commiteando y creando checkpoint.

## TP Check

TP-01: confirmar primero en codigo real que `mark-ready` ya salta checkpoint para
tickets no-code y que el gap residual vive en `_handle_pre_handoff()`.

TP-02: el bypass debe estar guiado por `deliverable_type`, no por heuristicas de
paths o por ausencia de diff.

TP-03: para tickets `code`, `--pre-handoff` mantiene commit/tag del `repo_motor`
sin regresion.

TP-04: el test documental de `--pre-handoff` demuestra que no se crea commit ni
tag manual en `repo_motor`.

TP-05: el cierre Manager/Supervisor queda cubierto por prueba focal o por
reutilizacion explicita del harness existente de `manager-approve`.

TP-06: `pytest`, `ruff` y `validate --json --project-root <repo_destino>` quedan
registrados con salida real.

## Veredicto Previo

`APPROVED`

El ticket esta bien planteado si se mantiene pequeno: arreglar la asimetria de
`pre-handoff` para deliverables documentales, probar la rama real y no abrir aun
una segunda arquitectura de cierre.
