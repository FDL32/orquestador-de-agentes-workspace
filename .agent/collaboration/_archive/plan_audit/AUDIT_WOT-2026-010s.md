# Audit Checklist: WOT-2026-010s

## Blockers

- Se eliminaron `triggers:` de SKILL.md.
- `trigger_map` cambia sin decision explicita y test de paridad.
- `disable-model-invocation` oculta una skill del dispatch manual.
- Se copio bundle externo o se instalaron dependencias.
- Se tocaron prompts, bus runtime o eventos manuales.
- No hay tests de ausencia del campo y valor invalido.
- `validate --json` no termina 0/0.

## Acceptance Checks

- `discover_skills.py` expone metadata nueva sin romper claves existentes.
- `bus/skill_resolver.py` mantiene allowlist por nombre y trigger.
- Consumidores restantes toleran la nueva metadata.
- Tests focales cubren paridad de `trigger_map`.
- `docs/skills_taxonomy/user_model_invocation_WOT-2026-010s.md` existe y explica compatibilidad.
- `CREDITS.md` tiene fila `WOT-2026-010s`, source pinneado, MIT, Adapted.

## Manager adversarial checks

- Buscar `disable-model-invocation` en diff: debe aparecer como metadata semantica, no como filtro destructivo del catalogo.
- Comparar `trigger_map` antes/despues con evidencia del Builder.
- Revisar que cualquier helper nuevo sea deep enough; si es wrapper 1:1, marcar AP-03/AP-16.