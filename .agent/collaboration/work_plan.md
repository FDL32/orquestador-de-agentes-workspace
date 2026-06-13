# Work Plan: WOT-AUDIT-A2b - Manifiesto de triage por ruta (motor-provides vs destino-keep)

## Metadata
- **ID:** WOT-AUDIT-A2b
- **Estado:** APPROVED
- **deliverable_type:** analysis
- **Titulo:** Inventariar y clasificar por ruta el contenido trackeado del destino segun el contrato host-extends/motor-provides
- **Asignado a:** Builder
- **Repo de autoridad:** repo_destino
- **Severidad:** Alta | **Riesgo:** Bajo (solo inventario/analisis; cero file-moves, cero edicion de CI/allowlist)
- **Origen:** WOT-AUDIT-A2. RE-SCOPE: la version previa de A2b ("reapuntar comandos")
  se apoyaba en `.claude/settings.local.json` (personal/untracked) y resulto un
  no-op de portabilidad. Se reemplaza por este ticket de inventario.

## Objetivo
Producir un manifiesto de triage por ruta que clasifique cada ruta tracked del
destino en buckets accionables, con evidencia verificable por fila. El manifiesto
es el spec ejecutable para los tickets posteriores (CI portability, A2c clone
limpio, A2d eliminacion). A2b NO mueve, borra ni edita nada ejecutable.

## Decision Arquitectonica
Inventariar antes de actuar. El error de `test_refactor_kit_performance.py` (dado
por "sin equivalente" mirando solo `scripts/`) demostro que clasificar por
basename o por una sola superficie produce falsos positivos que llegan a commit.
Por eso A2b separa el inventario (analysis, riesgo bajo) de la ejecucion
(eliminacion en A2d, riesgo alto): el manifiesto fija la verdad por ruta con
evidencia funcional y de invocacion viva, y solo entonces los tickets de
ejecucion actuan sobre esa verdad. Clasificar por equivalencia FUNCIONAL (no
nominal) y por invocacion real es lo que evita sobre-migrar superficies legitimas
del destino (estado operativo, integracion, config, dominio).

## Criterio canonico (congelado)
Eje primario (regla del host-extends/motor-provides reformulada):
- **motor:** tooling reutilizable, framework, prompts/skills/scripts compartidos
  (cualquier cosa de desarrollo o creacion del sistema).
- **destino:** estado operativo, integracion local, configuracion del host,
  overrides autenticos del host, y funcionalidad de dominio del repo_destino.

Definiciones de bucket (NO clasificar por basename; exige equivalencia funcional):
- **motor-provides:** existe equivalente FUNCIONAL verificado en el motor y el
  flujo del destino puede invocarlo -> el destino no debe versionar la copia.
- **destino-keep:** estado operativo / integracion / config / override autentico /
  funcionalidad de dominio del repo_destino.
- **huerfano-needs-decision:** NO existe equivalente funcional en el motor y NO
  implementa dominio del destino (tooling comun que el motor dropeo). Decision:
  promover al motor vs archivar.
- **ci-portability-blocker:** superficie machine-executed (CI) que hoy depende de
  copias locales y no puede referenciar un motor sibling en GitHub Actions.

Regla de prueba para "particular/dominio": solo cuenta como destino-keep por
dominio si implementa comportamiento del repo_destino, no si es tooling de
sistema que casualmente solo existe en el destino.

## Separacion de superficies (obligatoria en el manifiesto)
- **Machine-executed local:** `.claude/settings.local.json` (personal/untracked).
- **Machine-executed CI:** `.github/workflows/**`.
- **Documentation/reference only:** `.claude/rules/**`, `.agent/docs/**`,
  `agent_system/**/*.md`, `README*`, `AGENTS.md`, `CLAUDE.md`, `PROJECT.md`.
El Builder NO debe tocar ninguna de estas en A2b; solo inventariar a que bucket
pertenece cada ruta.

## Evidencia ya recolectada (input, el Builder la verifica y amplia)
- **Contrato:** `MANIFEST.workspace` (motor) lista SOLO rutas `.agent/` (estado,
  runtime, context, config) como contenido del workspace. NO incluye `scripts/`,
  `skills/`, `agent_system/`, `tests/`. El instalador `install_agent_system.py`
  sincroniza por esa allowlist (solo `.agent/`).
- **Volumen tracked destino:** `.agent/` 125, `agent_system/` 113, `skills/` 41,
  `scripts/` 12, `.claude/` 11, `_legacy/` 5, `tests/` 2.
- **Sin codigo de dominio:** la busqueda de producto/dominio solo devolvio
  configs (`ruff.toml`, `repomix.config.json`, `.code-workspace`).
- **scripts/ (12):** todos dev/creacion por docstring (test-runners, audit,
  drift, rollback/upgrade, discovery, suites refactor-kit). 7 con equivalente en
  el motor; 5 ausentes del motor (`artifact_graph`, `audit_codebase`,
  `rollback_agent_system`, `state_drift`, `test_refactor_manager_skill`).
- **Mapa de invocacion viva (machine-executed, no-.md):** el tooling forma una
  cadena interna (`audit_codebase`->`artifact_graph`/`state_drift`/`run_pytest_safe`;
  `upgrade`->`rollback`->`detect_version`). Las unicas superficies machine-executed
  a nivel destino son `.claude/settings.local.json` y `.github/workflows/`.
  Los 5 huerfanos no tienen entrypoint vivo a nivel destino.

## Conclusion provisional (NO cerrar como definitiva)
No se ha encontrado aun ninguna herramienta claramente de DOMINIO del destino;
el contrato `MANIFEST.workspace` ademas restringe el workspace a `.agent/`. Queda
pendiente de confirmar por fila: equivalencia funcional real (no basename),
invocacion viva, y dependencia de launcher/CI. El manifiesto debe declarar el set
`destino-keep por dominio` como vacio-hasta-prueba, no como hecho cerrado.

## Entregable (Builder)
`repo_destino/.agent/docs/triage_manifest.md` con una fila por ruta tracked (o por
grupo homogeneo justificado), columnas minimas:
1. **ruta**
2. **bucket** (motor-provides | destino-keep | huerfano-needs-decision | ci-portability-blocker)
3. **por que** (criterio funcional aplicado, no basename)
4. **quien la invoca hoy** (machine-executed local / CI / framework-interno / solo-docs / nadie)
5. **accion posterior propuesta** (referenciar motor / conservar / promover-o-archivar / portar CI)

## Superficies
- **Builder (crea):** `.agent/docs/triage_manifest.md`; `execution_log.md`.
- **Read/inspect only:** `MANIFEST.workspace`, `MANIFEST.distribute`,
  `install_agent_system.py` (motor), arbol tracked del destino, `.github/workflows/**`,
  `.claude/settings.local.json`. NO se editan.
- **Manager-only:** review de coherencia del manifiesto contra el criterio congelado.

## Non-goals
- No mover, borrar ni `git mv` ninguna ruta (eso es A2d).
- No editar `.claude/settings.local.json` ni `.github/workflows/**` (CI ticket).
- No editar prompts/skills/scripts del motor.
- No cerrar la decision de los huerfanos (promover vs archivar): solo marcarlos.

## Criterios binarios de cierre
- [ ] Existe `.agent/docs/triage_manifest.md` que cubre las 7 superficies tracked
      (`scripts/`, `skills/`, `agent_system/`, `tests/`, `.agent/`, `.claude/`,
      root) sin dejar rutas sin bucket.
- [ ] Cada fila tiene los 5 campos; el campo "por que" usa equivalencia funcional
      o dominio, NUNCA basename como prueba.
- [ ] Las superficies se separan en machine-executed local / CI / docs.
- [ ] La conclusion sobre `destino-keep por dominio` se declara vacia-hasta-prueba,
      no cerrada.
- [ ] `agent_controller.py --validate --project-root <destino>` exit 0, 0 errors.

## STOP / escalado
1. Si una ruta clasificada como motor-provides resulta tener invocacion viva
   machine-executed sin equivalente funcional confirmado en el motor: marcar como
   huerfano-needs-decision o ci-portability-blocker, NO como motor-provides.
2. Si aparece una ruta que implementa dominio real del destino: marcar destino-keep
   y escalar (cambia la conclusion de "dominio vacio").
3. No inferir equivalencia por basename: si no se puede verificar equivalencia
   funcional, la fila va a huerfano-needs-decision.

## Files Likely Touched
- `.agent/docs/triage_manifest.md` (nuevo)
- `.agent/collaboration/execution_log.md`
- `.agent/collaboration/work_plan.md` / `PLAN_WOT-AUDIT-A2b.md` (fase de contrato)

## Gates (deliverable_type: analysis)
- `agent_controller.py --validate --project-root <destino>` exit 0.
- Deliverable existence check: `.agent/docs/triage_manifest.md` existe.
- NO se exige pytest/ruff/pip-audit (no toca codigo).

## Riesgos
- Bajo. Inventario/analisis sin efectos ejecutables. El riesgo real (eliminar una
  ruta viva) queda en A2d, gateado por este manifiesto y por el ticket de CI
  portability.

## Tickets derivados (posteriores, fuera de A2b)
- **CI portability:** el CI del destino debe traer el motor (checkout/instalar) o
  saltar; no puede referenciar sibling. Gate de A2d.
- **A2c:** demo de clone limpio (`install --sync` regenera link; motor visible).
- **A2d:** eliminar copias motor-provides + resolver huerfanos, tras CI + A2c.
