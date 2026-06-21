# Execution Log -- WOT-2026-013d

**Estado:** IN_PROGRESS

## MANAGER - WOT-2026-013d - Bootstrap operativo

Ticket abierto como sucesor correcto de `013c`: la familia xdist/default ya quedo cerrada y la deuda real vive en producto (`project_scanner` / `project_paths`) con ruido concurrente de `tests/sandbox/test_runtime`.

Packet congelado y actualizado en repo_destino:
- backlog vivo + ficha `013d`
- `T-013D-001` en `ticket_contracts.md`
- `PLAN-013D-001` en `plan_graph.md`
- aclaracion explicita: la limpieza del sandbox se expresa via fixture/harness en `tests/conftest.py`, no por edicion manual del arbol

Premisa operativa del Builder:
- recapturar baseline de `tests/sandbox/test_runtime` antes del fix
- reproducir el triple xdist (`test_upgrade_path_suggestion`, `test_scan_current_project`, `test_no_inline_ticket_regex`) con `-n 8 --dist load`
- cubrir los 3 sitios `rglob` verificados, incluido `scan_project()`
- demostrar triple xdist verde en 3 corridas consecutivas
- cualquier necesidad de tocar runner/CI/default xdist o mover el sandbox fuera del arbol dispara STOP + `CG-WOT-2026-013d.md`
