# Work Plan: WOT-2026-005c - Audit post-change: resolver integrity, hooks, CI e install-sync risk

## Metadata
- **ID:** WOT-2026-005c
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Auditoria post-cambio incluye tabla Resolver integrity + prueba de comportamiento de hooks + revision settings/CI/install-sync
- **Asignado a:** Builder
- **Severidad:** Media | **Riesgo:** Bajo (cambio documental; reversible via git)
- **Depende de:** WOT-2026-005b (completed)
- **Origen:** session-2026-06-14-host-extends-learnings

## Decision Arquitectonica
Los fallos recientes (resolvers rotos tras retirar copias, hooks fail-open, CI sin bus,
install --sync re-vendor) deben pasar de memoria a checklist de auditoria post-cambio. Se
endurece el prompt y la skill de system-health para que toda auditoria que toque
host-extends/hooks/CI/install incluya una tabla de Resolver integrity y pruebas de
comportamiento (no solo lectura de codigo). Documental: no se añaden gates ni runtime.

## Files Likely Touched (repo_motor)
prompts/audit_post_change_system_health.md
skills/system-health-audit/SKILL.md

## Read/inspect only
- `scripts/check_claude_settings_portability.py`, `.agent/hooks/claude_guard_entry.py` (referenciados).

## Manager-only
- Revision documental.
- `python scripts/check_skill_collisions.py` exit 0 y `python scripts/discover_skills.py`
  carga `system-health-audit` sin romper triggers/source_prompt.

## Non-goals
- NO añadir gates nuevos ni runtime; NO tocar el frontmatter/trigger de la skill.
- NO duplicar checklists de 005b; referenciar fuentes canonicas.

## Criterios binarios de cierre
- [ ] Fase de integracion exige revisar `.claude/settings.json`, `claude_guard_entry.py`,
      `check_claude_settings_portability.py`, CI y launchers.
- [ ] La auditoria pide prueba de comportamiento para hooks de escritura: externo bloquea,
      interno benigno permite, link/motor ausente falla cerrado.
- [ ] El prompt busca resolvers hacia `agent_system/`, `scripts/`, `skills/` y
      `.agent/hooks/` antes de declarar segura una retirada de copias.
- [ ] La fase destino indica que `.claude/settings.json` trackeado no debe tener grants personales.
- [ ] Los artefactos de salida incluyen/piden tabla `Resolver integrity`.
- [ ] `check_skill_collisions.py` exit 0 y `discover_skills.py` carga `system-health-audit`.
- [ ] encoding 0; validate destino 0; motor solo estos 2 archivos; commit con WOT-2026-005c.

## STOP / escalado
- Si la auditoria descubre un fail-open real, abrir ticket de seguridad/code (no seguir saneando docs).
- Si se propone borrar installer-managed, exigir demo/fixture de clone limpio o depender de WOT-2026-003d.

## Gates (deliverable_type: documentation)
- `check_encoding_guard.py` (2 archivos); `check_skill_collisions.py` exit 0; `discover_skills.py`;
  `validate --project-root .` 0; `check_motor_pristine --check` (solo 2 archivos).

## Entregables
- `prompts/audit_post_change_system_health.md`, `skills/system-health-audit/SKILL.md` endurecidos.
- `orchestrator_pipeline/reports/closeout_WOT-2026-005c.md`.
