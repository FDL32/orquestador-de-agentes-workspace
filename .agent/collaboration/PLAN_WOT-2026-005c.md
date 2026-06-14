# PLAN WOT-2026-005c - audit post-change resolver integrity

## Pasos
1. `prompts/audit_post_change_system_health.md`:
   - Fase 4: añadir check de `.claude/settings.json` trackeado sin grants personales.
   - Fase 5: añadir tabla Resolver integrity + revision settings/entrypoint/portability gate
     + prueba de comportamiento del hook (externo bloquea / interno permite / link-motor
     ausente falla cerrado) + CI/launchers + aviso install --sync / WOT-2026-003d.
   - Estructura de salida: `03_integration_audit.md` menciona la tabla Resolver integrity.
2. `skills/system-health-audit/SKILL.md` (body): bullet de Contrato duro espejando Fase 5.
   Frontmatter intacto.
3. Verificar encoding; skill_collisions; discover carga system-health-audit.

## Evidencia esperada
- Diff de 2 archivos; encoding 0; skill_collisions 0; discover OK; validate 0; motor solo 2 archivos.

## STOP
- Fail-open real -> ticket seguridad. Borrar installer-managed -> demo clone / WOT-2026-003d.
