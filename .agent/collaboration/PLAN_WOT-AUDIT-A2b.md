# PLAN WOT-AUDIT-A2b - Manifiesto de triage por ruta

## Metadata
- **ID:** WOT-AUDIT-A2b
- **Estado:** APPROVED
- **deliverable_type:** analysis
- **Titulo:** Inventariar y clasificar por ruta el contenido trackeado del destino segun el contrato host-extends/motor-provides
- **Repo de autoridad:** repo_destino
- **Riesgo:** Bajo

## Objetivo operativo
Producir `repo_destino/.agent/docs/triage_manifest.md` como manifiesto de
triage por ruta. El deliverable debe clasificar las rutas tracked del destino en
los buckets `motor-provides`, `destino-keep`, `huerfano-needs-decision` y
`ci-portability-blocker`, con evidencia funcional y de invocacion viva por fila.

## Contrato cerrado
- No clasificar por basename. La equivalencia debe ser FUNCIONAL y verificable.
- No mover, borrar ni editar superficies ejecutables.
- No tocar `.claude/settings.local.json`.
- No tocar `.github/workflows/**`.
- No tocar prompts, skills o scripts del motor.
- El set `destino-keep por dominio` debe declararse `vacio-hasta-prueba`, nunca
  como conclusion cerrada sin evidencia por fila.

## Buckets y criterio
- **motor-provides:** equivalente funcional verificado en el motor y flujo
  invocable desde el destino.
- **destino-keep:** estado operativo, integracion local, configuracion del host,
  override autentico del host o funcionalidad de dominio del destino.
- **huerfano-needs-decision:** sin equivalente funcional en el motor y sin
  comportamiento de dominio del destino.
- **ci-portability-blocker:** superficie machine-executed de CI que hoy depende
  de copias locales y no puede asumir un sibling del motor en Actions.

## Separacion de superficies
- **Machine-executed local:** `.claude/settings.local.json`
- **Machine-executed CI:** `.github/workflows/**`
- **Documentation/reference only:** `.claude/rules/**`, `.agent/docs/**`,
  `agent_system/**/*.md`, `README*`, `AGENTS.md`, `CLAUDE.md`, `PROJECT.md`

## Files Likely Touched
- `.agent/docs/triage_manifest.md`
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/work_plan.md`
- `.agent/collaboration/PLAN_WOT-AUDIT-A2b.md`

## Builder deliverable
Crear `.agent/docs/triage_manifest.md` con estos 5 campos por fila:
1. `ruta`
2. `bucket`
3. `por que`
4. `quien la invoca hoy`
5. `accion posterior propuesta`

## Criterios binarios
- Existe `.agent/docs/triage_manifest.md`.
- El manifiesto cubre `scripts/`, `skills/`, `agent_system/`, `tests/`,
  `.agent/`, `.claude/` y root sin dejar rutas sin bucket.
- Cada fila usa equivalencia funcional o dominio real, no basename.
- Las superficies se separan en machine-executed local / CI / docs.
- `destino-keep por dominio` queda declarado como `vacio-hasta-prueba`.
- `python .agent/agent_controller.py --validate --json --project-root <destino>`
  devuelve exit 0 y 0 errors.

## STOP
- Si una ruta parece `motor-provides` pero no hay equivalente funcional
  confirmado: degradar a `huerfano-needs-decision`.
- Si aparece una ruta de dominio real del destino: clasificarla como
  `destino-keep` y registrarlo como cambio de conclusion.
- Si una superficie CI depende de copias locales: marcar
  `ci-portability-blocker`, no forzar decision de A2d.
