# AUDIT WOT-2026-005c - audit post-change resolver integrity

## Objetivo
Verificar que la auditoria post-cambio exige Resolver integrity, prueba de comportamiento de
hooks, revision de settings/CI/install-sync, y check de grants en settings trackeado, sin
tocar trigger ni runtime.

## Reglas de revision
- Leer el diff real de los 2 archivos.
- Confirmar los criterios binarios del work_plan textualmente.
- Frontmatter de la skill intacto; skill_collisions exit 0; discover carga system-health-audit.

## TP Check
TP-01: Fase 5 revisa settings/claude_guard_entry/portability gate/CI/launchers. (texto)
TP-02: prueba de comportamiento del hook (externo bloquea / interno permite / ausente falla cerrado). (texto)
TP-03: busqueda de resolvers hacia agent_system/scripts/skills/.agent/hooks antes de retirar. (texto)
TP-04: Fase destino: settings trackeado sin grants personales. (texto)
TP-05: salida incluye/pide tabla Resolver integrity. (texto)
TP-06: skill_collisions 0; discover carga system-health-audit; encoding 0; validate 0; motor 2 archivos; commit WOT-2026-005c. (command/git)

## Rechazo inmediato
- Falta un criterio; frontmatter cambiado; gate/runtime nuevo; skill rota.
