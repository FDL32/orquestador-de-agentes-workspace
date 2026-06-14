# AUDIT WOT-2026-005b - bootstrap/preflight host-extends

## Objetivo
Verificar que bootstrap y preflight exigen checks de topologia, settings portables, hooks
fail-closed y resolvers vivos antes de Builder en tickets host-extends, sin tocar trigger
ni runtime.

## Reglas de revision
- Leer el diff real de los 3 archivos.
- Confirmar los 6 criterios binarios del work_plan.
- Confirmar frontmatter de SKILL.md intacto (triggers/source_prompt/contract_id).
- Si SKILL.md cambia: check_skill_collisions exit 0 + discover carga orchestrate-pipeline.

## TP Check
TP-01: bootstrap exige topologia (motor/destino/AGENT_PROJECT_ROOT|link) para hooks/CI/install. (texto)
TP-02: preflight exige `check_claude_settings_portability.py` contra settings si existe. (texto)
TP-03: preflight reporta permissions.allow trackeado, hook ausente, hook fail-open, resolvers vivos. (texto)
TP-04: advertencia install --sync no es poda segura hasta WOT-2026-003d. (texto)
TP-05: trigger /pipeline y frontmatter intactos; sin gate/runtime nuevo. (diff)
TP-06: skill_collisions exit 0; discover carga orchestrate-pipeline; encoding 0; validate 0; motor solo 3 archivos. (command/git)

## Rechazo inmediato
- Falta un criterio; o se cambio el frontmatter/trigger; o se introdujo gate/runtime; o
  skill_collisions/discover rotos.
