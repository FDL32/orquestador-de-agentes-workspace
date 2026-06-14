# PLAN WOT-2026-005b - bootstrap/preflight host-extends

## Pasos
1. `prompts/destination_bootstrap.md`: añadir subseccion "Preflight de seguridad
   (host-extends)" que para tickets que tocan hooks/CI/install exige confirmar
   `repo_motor`, `repo_destino`, `AGENT_PROJECT_ROOT`/`motor_destination_link.json`, correr
   el gate de portabilidad de settings, y verificar resolvers vivos (scripts/, skills/,
   agent_system/, .agent/hooks/) antes de operar.
2. `skills/orchestrate-pipeline/references/destination-preflight.md`: añadir checks 7 y 8:
   - Check 7: portabilidad de settings + guard fail-closed
     (`check_claude_settings_portability.py` contra `.claude/settings.json` si existe;
     reportar `permissions.allow` trackeado, hook ausente, hook fail-open).
   - Check 8: integridad de resolvers host-extends (resolvers vivos hacia copias locales
     retirables; install --sync NO es poda segura hasta WOT-2026-003d).
3. `skills/orchestrate-pipeline/SKILL.md`: en la seccion "## Preflight del destino" (body,
   NO frontmatter) añadir referencia a los checks 7-8 nuevos. No tocar triggers/source_prompt.
4. Verificar encoding; si SKILL.md cambia: check_skill_collisions + discover_skills.

## Seams / invariantes
- Frontmatter de la skill intacto (triggers, source_prompt, contract_id).
- Solo documentacion; sin gate nuevo ni runtime.

## Evidencia esperada
- Diff de los 3 archivos; encoding 0; skill_collisions exit 0; discover carga
  orchestrate-pipeline; validate destino 0; motor solo estos 3 archivos.

## STOP
- Shell arbitrario o gate nuevo -> follow-up code, no aqui.
