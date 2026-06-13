# Execution Log WOT-AUDIT-A2b

**Estado:** IN_PROGRESS

## Metadata

- **ID:** WOT-AUDIT-A2b
- **deliverable_type:** analysis
- **Rol activo:** MANAGER
- **Accion:** CREATE_PLAN

## Resumen (A2b - RE-SCOPED)

- A2b RE-SCOPEADO tras revision adversarial: la version previa ("reapuntar
  comandos") se apoyaba en `.claude/settings.local.json` (personal/untracked) y
  era un no-op de portabilidad. Nuevo A2b = manifiesto de triage por ruta
  (analysis), sin tocar nada ejecutable.
- Criterio congelado (eje dev/creacion->motor; estado/integracion/dominio->destino),
  buckets (motor-provides | destino-keep | huerfano-needs-decision |
  ci-portability-blocker), superficies separadas (machine-local / CI / docs).
- Evidencia dura recolectada antes de escribir el ticket:
  - `MANIFEST.workspace` restringe el workspace a `.agent/`; el instalador solo
    sincroniza `.agent/`. `scripts/`, `skills/`, `agent_system/`, `tests/` son
    vestigiales respecto al contrato.
  - Mapa de invocacion viva: tooling = cadena interna de sistema; unicas
    superficies machine-executed a nivel destino = `settings.local.json` (personal)
    + `.github/workflows/` (CI). 5 huerfanos sin entrypoint vivo a nivel destino.
  - Sin codigo de dominio propio en el destino.
- Conclusion suavizada: `destino-keep por dominio` se declara vacio-hasta-prueba,
  NO cerrado. El Builder confirma por fila (equivalencia funcional + invocacion).
- A2a cerrado canonicamente (COMPLETED) y publicado; su log vive en git (26afa33).

## Pendiente (handoff, tras aprobacion humana)

- Finalizar contrato lanzable: Estado -> APPROVED, regenerar TURN.md para A2b,
  crear `PLAN_WOT-AUDIT-A2b.md` espejo. Luego Builder produce
  `.agent/docs/triage_manifest.md`.
- Tickets derivados: CI portability (gate de A2d), A2c clone limpio, A2d eliminacion.

## Builder - Fase 0 (diagnostico antes del cambio)

Rol BUILDER, accion IMPLEMENT. Evidencia recolectada el 2026-06-13 a HEAD
destino `13ee7e1` / motor `704939f` (read-only sobre arbol del destino + motor):

- **scripts/ (12):** 7 con basename en motor, 5 ausentes. CHEQUEO FUNCIONAL
  (diff destino vs motor, ignorando CRLF/BOM): `run_pytest_safe` 601 lineas
  distintas, `upgrade_agent_system` 485, `discover_skills` 304,
  `detect_agent_system_version` 230, `test_refactoring_impact` 64,
  `test_refactor_kit_portable` 3, `test_refactor_kit_performance` 2. Conclusion:
  las copias "comunes" son STALE/divergidas; basename NO prueba equivalencia.
  Motor-provides con flag de reconciliacion funcional antes de A2d.
- **skills/ (41):** 15 dirs de skill comunes con `motor/skills/`;
  `skills/validate_all.py` existe en `motor/skills/`. Todo el arbol es framework
  compartido -> motor-provides.
- **agent_system/ (113):** el motor tiene `agent_system/`; es el bundle del
  framework -> motor-provides (arbol completo).
- **tests/ (2):** `test_event_bus_hygiene.py` existe en `motor/tests/`
  (motor-provides); `test_ticket_007_context_recovery.py` NO existe en el motor
  ni el feature (`context_recovery`/`ticket_007` ausentes) -> huerfano.
- **.agent/ (125):** el destino NO vendoriza controller/bus/scope_gate (0
  archivos); usa el motor. Casi todo es estado: `collaboration/` 96, `audits/`
  12, `runtime/` 8, `config/` 3, `.version_manifest.json` -> destino-keep
  (coincide con MANIFEST.workspace). Flecos: `.agent/hooks/pre_compact_hook.py`,
  `.agent/microagents/onboarding.md`, `.agent/glossary.md` (ausentes en motor)
  -> huerfano-needs-decision; `.agent/README.md` (en motor) -> motor-provides.
- **.claude/ (11 tracked):** `settings.json`, `rules/`, `commands/`, `README.md`
  = integracion del host -> destino-keep. `settings.local.json` untracked =
  machine-executed local personal (fuera de contrato).
- **root (13):** docs de identidad/config del host -> destino-keep; `.goosehints`
  (Goose deprecado) -> huerfano.
- **Superficies machine-executed:** CI `.github/workflows/quality-gates.yml`
  (compileall scripts/tests + discover_skills guarded) -> ci-portability-blocker.

Desviaciones de scope: ninguna. Solo lectura + creacion del entregable declarado
`.agent/docs/triage_manifest.md`. Sin file-moves, sin edicion de CI/allowlist.

## Builder - Fase 1 (entregable) y gate final

- Entregable creado: `.agent/docs/triage_manifest.md` (11733 bytes), 7 superficies
  clasificadas en 4 buckets, 5 campos por fila, con conclusion `destino-keep por
  dominio` declarada vacio-hasta-prueba.
- Hallazgo nuevo del Builder (refuerza el criterio funcional): las 7 copias
  "comunes" de `scripts/` divergen del motor (run_pytest_safe 601, upgrade 485,
  discover_skills 304, detect 230, test_refactoring_impact 64; refactor-kit
  perf/portable 2-3) -> motor-provides con flag stale-diverged, reconciliar antes
  de A2d. 10 rutas huerfanas + 1 ci-portability-blocker (CI).
- Gate final: Doc `.agent/docs/triage_manifest.md` creado (ASCII-clean, no-BOM).
  Validate: exit 0, 0 errors, 0 warnings.

## Aprobacion humana y paquete lanzable

- Aprobacion humana recibida para lanzar A2b re-scopeado como ticket de
  `analysis`.
- `work_plan.md` actualizado a `APPROVED`.
- `PLAN_WOT-AUDIT-A2b.md` creado como espejo tecnico del contrato.
- Pendiente solo validar consistencia final y entregar `TURN.md` alineado al
  Builder.

---

## (Historico A2a, conservado para trazabilidad)

**Estado A2a:** COMPLETED

### Metadata A2a
- **ID:** WOT-AUDIT-A2a
- **deliverable_type:** documentation
- **Rol activo:** MANAGER
- **Accion:** CREATE_PLAN

## Resumen

- Manager redacto `work_plan.md` para WOT-AUDIT-A2a (subfase documentation de
  WOT-AUDIT-A2: host-extends/motor-provides).
- Alcance: documentar la regla de precedencia de recursos (host .agent -> motor
  read-only -> nunca legacy) y mapear los comandos del destino que apuntan a
  copias locales hacia su equivalente del motor externo. SIN mover/borrar nada.
- Evidencia de mapeo recolectada el 2026-06-13 a HEAD destino `13ee7e1` / motor
  `704939f` (ver tabla en work_plan.md).
- Bus inicializado con `--bootstrap-ticket` (STATE_CHANGED -> IN_PROGRESS).

## Hallazgos divergentes registrados como STOP para A2b

- `scripts/test_refactor_kit_performance.py`: copia local en el destino.
  CORRECCION 2026-06-13: NO es STOP. El motor SI tiene el test en
  `tests/test_refactor_kit_performance.py` (lo corre la suite `run_pytest_safe`);
  la afirmacion inicial "sin equivalente" solo miro `scripts/`. A2b retira la
  copia stale + allowlist; cobertura preservada por la suite del motor.
- `agent_system/refactor-kit/install_refactor_kit.py`: entrada allowlist stale
  (ruta hyphen inexistente; el motor lo tiene bajo `refactor_kit/` underscore).
  Limpieza en A2b, no bloqueante.

## Pendiente (Builder)

- Crear `repo_destino/.agent/docs/resource_precedence.md` con la decision
  arquitectonica + tabla de mapeo. Cierre con linea artefacto+gate.

## Builder - diagnostico antes del cambio

- Seams confirmados en codigo del motor:
  - `runtime/project_root.py` resuelve el root por `AGENT_PROJECT_ROOT`.
  - `scripts/run_pytest_safe.py` no expone `--project-root`; usa el resolver
    central y acepta `--status`.
  - `scripts/local_audit.py` no expone `--project-root`; solo acepta `--json`
    y `--quick`.
  - `scripts/discover_skills.py` no expone `--project-root`; su host-first
    discovery depende de `cwd/.agent/skills`.
- Evidencia runtime confirmada desde `cwd=repo_destino`:
  - `python <repo_motor>/scripts/discover_skills.py --json` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
  - `python <repo_motor>/scripts/run_pytest_safe.py --status` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
  - `python <repo_motor>/scripts/local_audit.py --json --quick` funciona con
    `AGENT_PROJECT_ROOT=<repo_destino>`.
- Desviacion de scope detectada y contenida:
  - el `work_plan.md` usa la forma abreviada `--project-root <repo_destino>` en
    la tabla de equivalencias, pero esa interfaz no existe hoy para al menos
    `run_pytest_safe.py`, `discover_skills.py` y `local_audit.py`. El
    entregable A2a documenta la forma invocable real sin modificar el scope del
    ticket ni tocar A2b.
- Artefacto creado:
  - `repo_destino/.agent/docs/resource_precedence.md`
- Gate final:
  - Doc `.agent/docs/resource_precedence.md` creado. Validate: exit 0, 0 errors,
    1 warning (`TP-STRUCT-01` esperado; `AUDIT_*` con `TP Check` pertenece al
    review artefact del Manager y no a A2a).


Manager approved canonical closeout for WOT-AUDIT-A2a
