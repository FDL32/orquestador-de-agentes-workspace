# AUDIT WT-2026-249b - Excluir BUILDER_BRIEF_ del guard de superficies vivas del workspace

## Tipo
code

## Veredicto esperado
APROBADO si el fix resuelve solo la exclusion de `BUILDER_BRIEF_`, mantiene
`UPSTREAM_LEARNINGS.md` fuera de exclusiones y deja barrera de regresion real.

## Checklist de auditoria

### Fase 1 - Contrato
- Verificar antes del arranque que `work_plan.md` activo del `repo_destino`
  apunte canonicamente a `WT-2026-249b`; `--mark-ready` no lee
  `PLAN_WT-2026-249b.md`.
- Verificar en codigo que el bloqueo observado en `249a` venia del guard de
  superficies vivas del workspace y no de otra gate posterior.
- Confirmar que el ticket no intenta reescribir el protocolo de closeout, solo
  la clasificacion de `BUILDER_BRIEF_`.
- Confirmar que el Builder inspecciona `.agent/agent_controller.py` y no
  desvia el fix hacia `bus/memory_loader.py` u otras capas de memoria.

### Fase 2 - Alcance minimo
- El diff productivo debe limitarse a:
  - `.agent/agent_controller.py`
  - `tests/test_agent_controller.py`
- Rechazar cualquier exclusion adicional sobre:
  - `.agent/runtime/memory/`
  - `UPSTREAM_LEARNINGS.md`
  - planes/audits en bloque
- Rechazar cualquier reapertura del hardening BOM o de `.opencode/opencode.json`
  dentro de este ticket.

### Fase 3 - Barrera de regresion
- Debe existir evidencia verificable de al menos estos dos contratos:
  - `BUILDER_BRIEF_WT-*` no bloquea `--pre-handoff`;
  - `UPSTREAM_LEARNINGS.md` sigue sin exclusion y puede bloquear.
- No aceptar tests cosmeticos; deben activar la rama real del guard o del
  helper de clasificacion de superficies vivas.
- El test negativo de `UPSTREAM_LEARNINGS.md` debe llamar `_is_live_surface()`
  con una ruta real/absoluta y verificar `False`; no basta con revisar la
  constante de prefijos excluidos.
- El test positivo de `BUILDER_BRIEF_WT-*` debe ser conductual: usar
  `_is_live_surface()` con ruta real o un escenario de `--pre-handoff` donde el
  brief sea el unico `??` relevante.

### Fase 4 - Riesgo de sobre-exclusion
- Revisar que la exclusion anadida sea exactamente:
  - `".agent/collaboration/BUILDER_BRIEF_"`
- Rechazar listas duplicadas por prefijo `WT-`/`WP-` o patrones mas amplios que
  conviertan `collaboration/` completa en superficie viva.
- Rechazar implementaciones inline en `_is_live_surface()` si el mismo efecto
  podia resolverse en `_WORKSPACE_EXCLUDED_PREFIXES`.

### Fase 5 - Gates
- `pytest tests/test_agent_controller.py -v`
- `ruff check .agent/agent_controller.py tests/test_agent_controller.py`
- `agent_controller.py --validate --json --project-root <repo_destino>`

## Blockers explicitos
- El diff toca `UPSTREAM_LEARNINGS.md` o la excluye del guard.
- El diff amplia exclusiones a memoria, plans o audits sin evidencia.
- No hay test negativo que mantenga `UPSTREAM_LEARNINGS.md` fuera de
  exclusiones.
- La exclusion se implementa con regex/lista duplicada cuando el plan exigia un
  prefijo unico `BUILDER_BRIEF_`.

## Notas para Manager
- `BUILDER_BRIEF_` es artefacto operativo del ticket; su exclusion es
  intencional.
- `UPSTREAM_LEARNINGS.md` no forma parte de este fix y debe seguir tratandose
  como hygiene/residuo si aparece en `repo_destino`.
- La evidencia en `execution_log.md` debe describir el comportamiento verificado
  del guard; no basta con una linea generica de "tests OK".
