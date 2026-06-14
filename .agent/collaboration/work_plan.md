# Work Plan: WOT-2026-005b - Bootstrap/preflight destino: host-extends, settings y guard fail-closed

## Metadata
- **ID:** WOT-2026-005b
- **Estado:** COMPLETED
- **deliverable_type:** documentation
- **delivery_authority:** repo_motor
- **Repo de autoridad:** repo_motor
- **Titulo:** Endurecer bootstrap y preflight del destino con checks de host-extends, settings Claude, hooks fail-closed y resolvers vivos
- **Asignado a:** Builder
- **Severidad:** Alta | **Riesgo:** Bajo (cambio documental; reversible via git)
- **Depende de:** WOT-2026-003c (completed)
- **Origen:** session-2026-06-14-host-extends-learnings

## Decision Arquitectonica
A2d demostro que retirar copias motor-provides puede dejar consumidores vivos apuntando a
rutas locales retiradas, y que un hook puede quedar fail-open. El bootstrap y el preflight
documentales no obligan aun a verificar resolvers vivos, settings Claude portables y hooks
fail-closed antes de lanzar Builder. Se endurecen las TRES superficies documentales (no
codigo, no runtime): bootstrap exige confirmar topologia + settings/hooks/resolvers para
tickets que tocan hooks/CI/install; el preflight añade el gate de portabilidad de settings
y una tabla de integridad de resolvers; y se advierte que `install --sync` NO es mecanismo
seguro de poda host-extends hasta cerrar WOT-2026-003d. No se cambia el trigger `/pipeline`
ni logica runtime.

## Files Likely Touched (repo_motor)
prompts/destination_bootstrap.md
skills/orchestrate-pipeline/references/destination-preflight.md
skills/orchestrate-pipeline/SKILL.md

## Read/inspect only
- `scripts/check_claude_settings_portability.py` (gate referenciado).
- `.agent/hooks/claude_guard_entry.py` (entrypoint fail-closed referenciado).

## Manager-only
- Revision documental.
- Si se toca `SKILL.md`: `python scripts/check_skill_collisions.py` exit 0 y
  `python scripts/discover_skills.py` carga `orchestrate-pipeline` sin romper triggers/source_prompt.

## Non-goals
- NO cambiar el trigger `/pipeline` ni el frontmatter de la skill (triggers, source_prompt, contract_id).
- NO añadir gates nuevos ni logica runtime (solo documentar checks existentes).
- NO ejecutar shell arbitrario como check.

## Criterios binarios de cierre
- [ ] Bootstrap exige confirmar `repo_motor`, `repo_destino`, `AGENT_PROJECT_ROOT` o
      `motor_destination_link.json` antes de tickets que toquen hooks/CI/install.
- [ ] `destination-preflight.md` exige correr `check_claude_settings_portability.py` contra
      `.claude/settings.json` del destino cuando exista.
- [ ] El preflight detecta y reporta: `permissions.allow` trackeado, hook ausente, hook
      fail-open, y resolvers vivos hacia copias locales retirables.
- [ ] El texto advierte que `install --sync` NO es mecanismo seguro de poda host-extends
      hasta cerrar WOT-2026-003d.
- [ ] No se cambia el trigger `/pipeline` ni logica runtime (frontmatter intacto).
- [ ] Si se toca SKILL.md: `check_skill_collisions.py` exit 0 y `discover_skills.py` carga
      `orchestrate-pipeline` sin romper triggers.
- [ ] `check_encoding_guard.py` pasa sobre los 3 archivos; validate destino 0 errores; motor
      solo estos 3 archivos.
- [ ] Commit en repo_motor con WOT-2026-005b.

## STOP / escalado
- Si algun check requiere ejecutar shell arbitrario o crear un gate nuevo, documentarlo como
  follow-up code (no implementarlo aqui).
- Si el preflight no puede distinguir invocador vivo de referencia historica, exigir
  evidencia manual en el work_plan antes de Builder.

## Gates (deliverable_type: documentation)
- `check_encoding_guard.py` sobre los 3 archivos.
- `python scripts/check_skill_collisions.py` (exit 0) + `python scripts/discover_skills.py` (carga orchestrate-pipeline).
- `validate --project-root .` (destino) 0 errores.
- `check_motor_pristine --check` (solo los 3 archivos cambian).

## Entregables
- `prompts/destination_bootstrap.md`, `references/destination-preflight.md`, `SKILL.md` endurecidos.
- `orchestrator_pipeline/reports/closeout_WOT-2026-005b.md`.
