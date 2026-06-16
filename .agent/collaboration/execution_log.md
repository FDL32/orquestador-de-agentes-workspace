# Execution Log: WOT-2026-008c - Catalogo derivado + INDEX generado para prompts y skills

## Metadata

**Estado:** COMPLETED
- **ID:** WOT-2026-008c
- **Contract ID:** T-008C-001
- **deliverable_type:** mixed
- **delivery_authority:** repo_motor
- **Rol activo:** BUILDER
- **Accion:** IMPLEMENT

## Baseline

- Motor HEAD: 585fadb (naming gate nits after WOT-2026-010a)
- Destino: WOT-2026-010a cerrado canonico; runtime reproyectado a nuevo ciclo
- Dependencias verificadas vivas: WOT-2026-008b cerrado/publicado, WOT-2026-009g cerrado/publicado
- Backlog normalizado por Manager para reflejar cierre de 008b y 010a antes de activar 008c
- Validate preflight tras rebootstrap de 008c: 0 errors / 0 warnings

## Fase 0 — Inventario (VERIFICADO en codigo, 2026-06-16)

### Callers/seams de discovery/dispatch (VERIFICADO)
- `scripts/discover_skills.py`: SEAM CENTRAL. `_scan_skills_dir` deriva todo de
  frontmatter (`name`, `triggers`, `version`, `description`) + glob de directorio
  `skills/*/SKILL.md`. NO conoce aun status/deprecated/draft/alias.
- `scripts/validate_agent_config.py`: DELEGA en `discover_skills()` + `extract_frontmatter`.
- `scripts/run_gates_dispatch.py`: invoca `discover_skills.py --check-contract`.
- `bus/skill_resolver.py`: DELEGA en `discover_skills()` y cachea.
- `scripts/check_skill_collisions.py`: UNICO con glob+frontmatter propio.

CONCLUSION (VERIFICADO): `discover_skills.py` es el punto de integracion minimo.
3 de 5 consumidores delegan en el. Integrar metadata derivada ahi propaga
status/alias a validate_agent_config, run_gates_dispatch y skill_resolver sin
reescribirlos. `check_skill_collisions.py` sigue siendo consumidor independiente.

### Fuentes vivas (VERIFICADO)
- `prompts/*.md`
- `skills/*/SKILL.md`
- `skills/*/references/*.md`
- `skills/_shared/*.md`
- consumidores `scripts/*.py` / `bus/skill_resolver.py`

### Campos frontmatter reales (VERIFICADO)
- En `SKILL.md`: name, version, description, triggers, author, role, stage,
  writes_memory, quality_gate, tags, source_prompt, contract_id.
- En prompts: `contract_id` vive en el cuerpo, no en YAML frontmatter.
- Hoy no existe `status`/`deprecated`/`draft`/`alias` explicitos: la
  disponibilidad se infiere por presencia en disco.

## BLOCKER detectado y RESUELTO a nivel contractual (VERIFICADO)

### Diagnostico original (VERIFICADO)
El primer borrador de 008c proponia `docs/registry/registry.json` como fuente
canonica. Eso entraba en contradiccion directa con
`docs/decisions/DEC-008B-001-registry-model.md`:
- `ADOPTED: Opcion 4 - Discovery recursivo sin manifest`
- consecuencia literal: `registry.json no se crea en este ticket ni en 008c`
- `INDEX.md` debe ser proyeccion generada por `discover_skills --json`
- introducir un registry manual anadiria una segunda fuente de verdad
  desincronizable, contra CEM.

### Resolucion aplicada (VERIFICADO)
El contrato de 008c fue reescrito para alinearse con `DEC-008B-001`:
- NO hay `registry.json` autoritativo
- la autoridad sigue siendo `discover_skills.py` + frontmatter/layout vivo
- 008c pasa a implementar catalogo derivado en `discover_skills --json`
- `docs/registry/INDEX.md` sera proyeccion generada y stale-gated
- metadata nueva (`status`, `owner`, `canonical_source`, `kind`, `aliases`)
  debe derivarse de fuentes vivas, no de un manifest manual

### Decision del Manager/propietario (APLICADA)
Ruta A: reinterpretar 008c como `frontmatter + discovery + INDEX proyectado`,
coherente con `DEC-008B-001`. Builder puede relanzar sobre este contrato.

## Fase 1 pendiente

- Extender `discover_skills.py --json` con catalogo derivado
- Generar `docs/registry/INDEX.md` desde discovery
- Anadir stale gate/paridad
- Integrar metadata derivada minima en dispatch

## RESOLUCION blocker + Fase 1 (post-realineacion 2026-06-16)

Blocker contractual RESUELTO: work_plan 008c realineado con DEC-008B-001.
Confirmado en work_plan lineas 4-6, 30-44: NO registry.json, autoridad =
discovery+frontmatter, INDEX.md = proyeccion generada. Procedo.

### Seam central RECONFIRMADO (VERIFICADO)
`discover_skills.py` sigue siendo el seam: validate_agent_config (delega),
run_gates_dispatch (--check-contract subproceso), skill_resolver (delega+cachea).
parse_frontmatter usa utf-8-sig (fix de 008b vivo). main() emite --json/--goose.

### Schema metadata derivada (Fase 1 — frontmatter-first, sin manifest)
Reglas de derivacion (todas de fuente viva verificable):
- kind: por layout. skill (skills/*/SKILL.md), prompt (prompts/*.md),
  reference (skills/*/references/*.md), shared (skills/_shared/*.md),
  script-consumer (los 5 consumidores declarados).
- path: ruta relativa al motor (forward slashes).
- status: frontmatter `status:` si existe; default `active`. Soporta
  active|deprecated|draft. Retrocompatible (ningun archivo lo declara hoy).
- owner: frontmatter `author`; fallback `role`; default `system`.
- canonical_source: == path (008c NO renombra; canonical == path actual).
- aliases: frontmatter `triggers` (los triggers SON los alias de invocacion).
  Solo skills tienen triggers; prompts/references aliases=[].

### Decision de integracion minima (INFERENCIA RAZONABLE, a probar con test)
discover_skills() excluye del trigger_map ACTIVO las skills con
status in {deprecated, draft}: la metadata tiene efecto real (no solo presencia
en disco). active sigue en trigger_map. skill_resolver hereda via delegacion.
Test de consumer path lo prueba.

### Superficie CLI nueva (en discover_skills.py, sin segunda fuente)
- `--catalog`: JSON del catalogo enriquecido (todos los kinds).
- `--generate-index`: escribe docs/registry/INDEX.md proyectado desde catalogo.
- `--check-index`: stale gate; exit 1 si INDEX.md diverge del catalogo vivo.

## Fases 2-6 — Implementacion (VERIFICADO)

### Fase 2: catalogo enriquecido en discover_skills.py (VERIFICADO)
- _derive_status(fm): frontmatter status:; default active; unknown->active
  (typo nunca esconde skill). VALID_STATUS=(active,deprecated,draft).
- _derive_owner(fm): author -> role -> system.
- _scan_skills_dir anade status/owner/aliases (aliases=triggers).
- discover_skills(): trigger_map SOLO enlaza skills active. deprecated/draft
  quedan en catalogo (visibles) pero NO despachan. Metadata con efecto real.
- build_catalog(): catalogo derivado completo (skill/prompt/reference/shared/
  script-consumer). Verificado: 90 entradas (29 skill, 20 prompt, 33 reference,
  3 shared, 5 script-consumer).
- _catalog_entry: canonical_source == path (008c NO renombra).

### Fase 3: INDEX.md + README.md generados (VERIFICADO)
- docs/registry/INDEX.md: proyeccion generada, marcador AUTOGENERATED en linea 1.
  `python scripts/discover_skills.py --generate-index` -> [OK] Generated.
- docs/registry/README.md: documenta autoridad=discovery+frontmatter, NO registry.json.

### Fase 4: stale gate (VERIFICADO con barrera FAIL/PASS)
- --check-index: exit 0 in-sync, exit 1 si diverge o falta.
- Barrera reproducida: append a INDEX.md -> [STALE] exit 1; restaurado -> exit 0.

### Fase 5: integracion minima consumer path (VERIFICADO)
- bus/skill_resolver delega en discover_skills() -> hereda status/owner/aliases
  + trigger_map filtrado por active. 29 skills, campos presentes. Sin romper.
- validate_agent_config, check_skill_collisions, --check-contract: exit 0 (no rotos).

### Fase 6: tests focales (VERIFICADO)
Comando: python -m pytest tests/test_registry_catalog.py tests/test_discover_skills.py
  tests/test_check_skill_collisions.py tests/test_approval_state_revision_and_skill_access.py
  tests/test_refactoring_impact.py -q
Resultado: 92 passed in 1.26s.
- tests/test_registry_catalog.py (NUEVO, 15 tests): derived metadata, status
  dispatch effect (active despacha / draft+deprecated no), aliases=triggers,
  catalogo cubre kinds, paridad status catalogo<->discovery, stale gate
  (in-sync/missing/divergent/marker/deterministic).
- test_refactoring_impact::test_code_quality (ruff sobre codigo): PASS.

### Gates de codigo (VERIFICADO)
- ruff check scripts/discover_skills.py tests/test_registry_catalog.py: All checks passed.
- ruff format: aplicado (2 files reformatted), re-check limpio.

### Encoding (VERIFICADO)
- INDEX.md/README.md usan algun caracter no-ASCII intencional (acentos espanol,
  em-dash en proyeccion). UTF-8 valido. Nota: el em-dash en render_index ("—")
  para aliases vacios es intencional en proyeccion humana, no en codigo fuente.

## Suite canonica + HALLAZGO de deuda preexistente (VERIFICADO)

### 008c focal: VERDE
run_pytest_safe.py exit 0. Tests focales del FLT: 92 passed.
ruff check+format limpios. encoding guard exit 0.

### HALLAZGO: 1 fallo en suite canonica, PREEXISTENTE de WOT-2026-010a (NO de 008c)
test: tests/unit/test_no_inline_ticket_regex.py::test_no_inline_ticket_regex
Causa: scripts/check_ticket_nomenclature.py (creado en 010a) contiene el patron
literal "(?:WP|WT)-" en ~14 lineas. La gate test_no_inline_ticket_regex
(barrera de WT-2026-251a) prohibe ese literal fuera de bus/ticket_id.py salvo
exencion inline "# ticket-id-exemption: <reason>".

VERIFICADO preexistente con git stash:
- Con cambios 008c stashed (HEAD 585fadb, post-010a): el test YA falla.
- Conclusion: 010a se cerro/publico con la suite canonica roja en este test.
  No fue detectado porque la suite focal de 010a no incluia esta barrera.
- 008c NO introduce este fallo. discover_skills.py no usa el patron literal.

### Naturaleza del caso (analisis)
check_ticket_nomenclature.py NECESITA los literales WP-/WT-: su funcion es
distinguir legacy de canonical. Importar TICKET_ID_PATTERN de bus/ticket_id.py
NO sirve: ese patron acepta WOT tambien, no distingue legacy. La exencion inline
es el fix correcto y previsto por la propia barrera.

### CONFLICTO DE SCOPE (detengo antes de tocar)
- No puedo emitir mark-ready de 008c con la suite canonica roja (handoff canonico
  lo exige).
- Pero el fallo es de 010a; check_ticket_nomenclature.py NO esta en el FLT de 008c.
  Arreglarlo en el commit de 008c contaminaria el scope del ticket.

Opciones para el propietario:
  (A) Micro-fix de 010a en commit SEPARADO antes de cerrar 008c: anadir
      "# ticket-id-exemption: gate detecta prefijos legacy por diseno" a las
      lineas de check_ticket_nomenclature.py. Commit chore(WOT-2026-010a). Luego
      cerrar 008c limpio. (Recomendado: desbloquea sin mezclar scope.)
  (B) Abrir ticket 010b para la deuda y cerrar 008c documentando el fallo
      preexistente como conocido (no-regresion de 008c).
  (C) Ampliar excepcionalmente el FLT de 008c con justificacion CEM para incluir
      el fix, dado que bloquea el cierre.

008c queda en espera de decision. Codigo de 008c: completo y verde en focal.

## HOTFIX WOT-2026-010b — salud de main heredada de 010a (en curso)

008c PAUSADO con stash path-limited (stash@{0}, path-limited a las 3 superficies
de 008c; 2 stashes ajenos preexistentes intactos). Motor a HEAD limpio.

### Criterio binario del hotfix (barrera verificada)
- [x] La suite canonica FALLA antes del fix por test_no_inline_ticket_regex
      (VERIFICADO con HEAD limpio: 1 failed).
- [x] PASA despues del fix (VERIFICADO: 1 passed).

### Fix aplicado (scripts/check_ticket_nomenclature.py)
1. Constante unica _LEGACY_PREFIX con exencion inline UNA sola vez
   (# ticket-id-exemption: gate must detect legacy-only prefixes). Todos los
   regex (LEGACY_HIT_RE, HISTORY_RE, GENERATOR_SIGNAL_RE) compuestos desde ella.
   Literal "(?:WP|WT)-" sin exencion: 0 ocurrencias. NO importa TICKET_ID_PATTERN
   (acepta WOT; este gate necesita detectar legacy especificamente).
2. BONUS (el test focal lo descubrio): el gate de 010a tenia un FALSO NEGATIVO.
   LEGACY_HIT_RE solo casaba \d{4}|YYYY|XXXX, dejaba escapar WP-XXX/WT-XXX (tres
   letras). 2 generadores vivos no detectados: man-resolve-escalation/SKILL.md:109
   y man-review-implementation/SKILL.md:188 (**Plan:** WP-XXX / WT-XXX).
   Fix: +XXX en LEGACY_HIT_RE, +**Plan:** signal, ambos generadores -> WOT-XXX.

### Test focal nuevo (tests/test_check_ticket_nomenclature.py)
14 tests. El gate de 010a se entrego SIN tests (otra deuda). Cubre:
generator detection (incl. regresion --ticket WP-2026-123a), history, legacy-tagged,
no-false-positive WOT, literal centralizado (1 vez), gate verde end-to-end.
Barrera verificada: el test encontro los 2 falsos negativos reales arriba.

### LECCION DE PROCESO (deuda nombrada)
- 010a se cerro/publico con la suite canonica ROJA en test_no_inline_ticket_regex.
- Causa: la suite FOCAL de 010a estaba verde, pero la canonica no se leyo hasta
  el final (se cito un conteo "passed" sin cruzar el "failed").
- Regla reforzada: el cierre canonico DEBE correr run_pytest_safe completo y leer
  el resultado hasta el final (passed Y failed), no solo la focal del ticket.
  Una focal verde NO autoriza mark-ready si la canonica tiene una barrera roja.
- Deuda explicita (candidata a gate futuro): el cierre canonico podria exigir
  evidencia literal de "0 failed" en run_pytest_safe, no solo "N passed".

### Gates 010b
- ruff check + format: All checks passed.
- test_check_ticket_nomenclature.py: 14 passed.
- test_no_inline_ticket_regex.py: 1 passed.
- run_pytest_safe completo: [en curso, se registra resultado final].

### Resultado canonico 010b (leido hasta el final)
run_pytest_safe completo: 2801 passed, 19 skipped, 5 deselected, 0 FAILED (376s).
Pre-fix era: 2801 passed, 1 FAILED (test_no_inline_ticket_regex).
El fix recupera la barrera sin romper nada. Suite canonica VERDE.

## 008c RETOMADO (post-cierre 010b, main sano)

010b cerrado/publicado (motor 69d53c1, canonica 2801 passed 0 failed).
008c restaurado via git stash pop del stash etiquetado (path-limited; 2 stashes
ajenos intactos). Working tree: discover_skills.py + docs/registry/ +
test_registry_catalog.py (las 3 superficies de 008c, nada mas).

### Re-verificacion 008c tras restaurar
- INDEX in-sync tras 010b (--check-index exit 0): el catalogo deriva de
  frontmatter, robusto a los cambios de cuerpo que hizo 010b en 2 SKILL.md.
- Suite focal 008c: 92 passed.
- ruff check scripts/discover_skills.py: All checks passed.
- Suite canonica completa: [en curso, leida hasta el final antes de mark-ready].

### Resultado canonico 008c (leido hasta el final - leccion aplicada)
run_pytest_safe completo: 2816 passed, 19 skipped, 5 deselected, 0 FAILED (296s).
(2816 = 2801 main + 15 nuevos test_registry_catalog.py). grep failed/error: vacio.
Suite canonica VERDE. Autorizado para mark-ready.

### Criterios binarios 008c (verificados contra evidencia)
- [x] discover_skills.py --json/--catalog expone catalogo enriquecido derivado,
      sin registry.json manual. VERIFICADO: 90 entradas, build_catalog().
- [x] docs/registry/INDEX.md proyeccion generada, falla si stale. VERIFICADO:
      --generate-index + --check-index (barrera FAIL/PASS reproducida).
- [x] metadata cubre kind/path/status/owner/canonical_source/aliases. VERIFICADO
      en test_catalog_entries_have_required_fields.
- [x] status soporta active/deprecated/draft, default active retrocompatible.
      VERIFICADO en TestDerivedMetadata + dispatch effect.
- [x] discovery/dispatch usa metadata para active/draft/deprecated/aliases.
      VERIFICADO: trigger_map solo active; skill_resolver hereda via delegacion.
- [x] catalogo cubre prompts/skills/references/_shared + 5 consumidores.
      VERIFICADO: counts {prompt:20,reference:33,script-consumer:5,shared:3,skill:29}.
- [x] gate stale que falla si INDEX stale. VERIFICADO: --check-index + tests.
- [x] no manifests manuales, no moves, no renames. VERIFICADO: solo discover_skills.py
      + docs/registry/ + test nuevo.
- [x] ruff exit 0; tests focales exit 0 (92); validate destino 0/0; canonica 0 failed.

### Nota de scope (CEM)
Toque MENOS archivos del FLT de los listados: NO reescribi check_skill_collisions.py,
validate_agent_config.py, run_gates_dispatch.py, bus/skill_resolver.py ni los 3
tests existentes. La integracion minima via el seam central (discover_skills.py)
propago la autoridad logica sin reescribir consumidores. FLT es whitelist, no
obligacion; el mandato pedia "no reescribir mas consumidores de los necesarios".


Manager approved canonical closeout for WOT-2026-008c