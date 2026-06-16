# Work Plan: WOT-2026-008b

## Metadata

- **ID:** WOT-2026-008b
- **Contract ID:** T-008B-001
- **Estado:** APPROVED
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Depends on:** WOT-2026-008a (COMPLETED), WOT-2026-009b (COMPLETED)

## Objetivo

Corregir el falso verde de BOM/frontmatter/discovery: un `SKILL.md` con BOM
puede quedar invisible en `discover_skills.py` mientras `--check-contract` pasa
con exit 0. Cerrar la DEC de modelo de registry y discovery sin implementar el
registry completo, sin mover/renombrar skills ni crear aliases o shims.

**Premisa verificada en vivo (2026-06-16):**
- `skills/man-review-implementation/SKILL.md` tiene BOM (`efbbbf`).
- `discover_skills.py` descubre 28 skills de 29 SKILL.md en disco.
- `discover_skills.py --check-contract` devuelve exit 0 — falso verde confirmado.

## Decision Arquitectonica

El Builder debe cerrar dos DECs como artefactos documentales en este ticket:

### DEC-008B-001: Modelo de registry
Comparar y decidir entre al menos cuatro opciones:
1. Registry central (`registry.json` en raiz motor)
2. Manifest por skill (`manifest.json` local en cada `skill/`)
3. `.claude-plugin/plugin.json` compatible con ecosystem Claude
4. Discovery recursivo sin manifest (estado actual)

La DEC debe declarar: tradeoffs, compatibilidad con host-first, coste de
migracion, si `registry.json` es autoridad logica o proyeccion, y relacion con
`INDEX.md` futuro (008c). Si se adopta registry-first, el contrato declara
`registry.json` como autoridad logica de API activa y `INDEX.md` como
proyeccion generada, nunca fuente manual.

### DEC-008B-002: Modelo de discovery de triggers
Decidir entre:
1. Mantener `triggers` en frontmatter como API propia
2. Migrar a discovery por `description` estilo Claude Code
3. Hibrido (triggers + description fallback)

La DEC debe declarar: compatibilidad, coste de migracion y efecto en
prompts/skills actuales.

## Non-goals

- NO implementar el registry completo (`registry.json` operativo con dispatch).
- NO renombrar, mover ni reorganizar carpetas de skills o prompts.
- NO crear aliases runtime, shims de compatibilidad ni archivos de redirect.
- NO tocar scope de 008c/008d/008e/008f.
- NO crear `skills/domain/...` ni `prompts/system/...`.
- Si el fix requiere reorganizar carpetas -> abrir 008d.
- Si el registry introduce fuente manual no validada -> BLOCKED.

## Files Likely Touched

### repo_motor
- `scripts/discover_skills.py`
- `scripts/check_skill_collisions.py`
- `scripts/check_encoding_guard.py` (solo si el gap real esta en su cobertura)
- `tests/unit/test_discover_skills.py` (nuevo o existente)
- `tests/unit/test_skill_collisions.py` (nuevo o existente)
- `tests/unit/test_encoding_guard.py` (nuevo o existente si aplica)
- `skills/man-review-implementation/SKILL.md` (solo para retirar BOM)
- `docs/decisions/DEC-008B-001-registry-model.md` (nuevo)
- `docs/decisions/DEC-008B-002-discovery-triggers.md` (nuevo)

### Read/inspect only
- `skills/**/SKILL.md` (29 archivos en disco, para barrido BOM y matriz de triggers)
- `prompts/*.md` (barrido BOM)
- `.agent/config/agents.json` (derivar matriz allowlist viva)
- `skills/orchestrate-pipeline/references/destination-preflight.md`

### Manager-only
- Validar que DECs existen y son verificables como artefactos en disco.
- Verificar barrido BOM documentado con rutas exactas.
- Ejecutar `validate --json` final.

## Evidencia viva derivada pre-Builder (2026-06-16)

**Matriz triggers derivada desde fuentes vivas:**

Allowlist en `agents.json`:
`/archive`, `/audit`, `/compare`, `/debug`, `/fix`, `/impl`, `/implement`,
`/inspect`, `/orchestrate`, `/refactor`, `/report`, `/review`, `/schedule`,
`/tdd`, `/test`, `/validate`

BOM-casualties (tienen triggers en frontmatter pero son invisibles al discover):
- `skills/man-review-implementation/SKILL.md` -> triggers: `/review`, `code-review`, `/approve`

Ghosts reales (en allowlist sin skill frontmatter vivo tras fix BOM):
- `/archive`, `/fix`, `/impl`, `/orchestrate`, `/report`, `/test`, `/validate`
- Clasificacion a confirmar por Builder: invented/retired vs pending-skill

Noise en allowlist (no son skills, son backend names):
- `/deepseek-v4-flash`, `/gpt-5`

## Criterios Binarios

- [ ] Test de regresion: un `SKILL.md` con BOM no puede quedar invisible
      mientras `discover_skills.py --check-contract` devuelve exit 0.
- [ ] `discover_skills.py` y `check_skill_collisions.py` tienen semantica
      compatible o diferencia documentada; el caso `man-review-implementation`
      es detectable con ambas herramientas.
- [ ] BOM eliminado de `skills/man-review-implementation/SKILL.md`; discovery
      ve 29/29 skills tras el fix.
- [ ] Barrido de BOMs en `skills/**/SKILL.md` y `prompts/*.md` documentado
      con rutas exactas (puede ser "ningun otro BOM detectado").
- [ ] DEC-008B-001 (registry) existe en disco con al menos 4 opciones
      comparadas y decision clara.
- [ ] DEC-008B-002 (discovery/triggers) existe en disco con decision clara.
- [ ] Matriz allowlist vs triggers: ghosts clasificados como `BOM-casualty`,
      `invented`, `retired` o `pending-skill`. `/review` NO se retira.
- [ ] `ruff check .` exit 0 en repo_motor.
- [ ] Tests focales de discovery/collision/encoding pasan con exit 0.
- [ ] `validate --json` destino 0 errors / 0 warnings al cierre.

## Forbidden Surfaces

- `.agent/collaboration/` del motor (seed neutro).
- `privada/` y `.env`.
- `bus/state_machine.py`.
- `scripts/validate_ticket_prose.py`.
- Cualquier skill distinta de `man-review-implementation` (solo barrido/doc).
- 008c/008d/008e/008f (no adelantar).
