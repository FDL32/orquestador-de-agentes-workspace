# PLAN WOT-2026-005d - audit completo: patrones host-extends y memoria

## Pasos (todo en `prompts/audit_complete_motor_destination.md`)
1. Fuentes minimas: añadir `destination_bootstrap.md`, `orchestrate-pipeline/SKILL.md`,
   `destination-preflight.md`, `system-health-audit/SKILL.md` (memory_upload.md ya esta).
2. Seccion 5 (Portabilidad): añadir bullet de resolvers/bootstraps (no solo imports),
   referenciando `destination-preflight.md` checks 7-8.
3. Seccion 6 (Calidad): expandir "fail-open validators" a validators, hooks, launchers, CI y
   fallback/stubs de topologia (exit 0 sin dependencia resuelta = critico).
4. Seccion 7 (Observabilidad): añadir distincion bus ausente/no-verificable vs presente/violado
   (CI/clone limpio) + memoria por capas (Claude privada / portable motor / portable destino)
   con chequeo de promocion por schema, referenciando `memory_upload.md`.
5. Verificar encoding; validate; pristine.

## Evidencia esperada
- Diff del prompt; encoding 0; validate 0; motor solo este archivo.

## STOP
- No duplicar 005b/005c; referenciar. Mojibake masivo -> ticket aparte.
